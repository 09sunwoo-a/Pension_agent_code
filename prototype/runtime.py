# -*- coding: utf-8 -*-
"""
Minimal CASE_001 runtime for the Pension Agent prototype.

Purpose: run one Frozen Case end-to-end against the Target Base LLM
(gemma-4-31b-it via the Google Generative Language REST API) and make every
step observable, so that failures can be located by layer.

Conceptual flow (00_Core_Concept_Design.md) is NOT mapped 1:1 to functions.
This file deliberately contains only what CASE_001 needs:

    Frozen Customer Input   (cases/<CASE>/case.md  §2)
    → Constraint Context    (C1, deterministic; cases/<CASE>/case.md §4)
    → Knowledge Context     (cases/<CASE>/knowledge_pack.md, selected fields)
    → Prompt                (5 identifiable sections)
    → Gemma 4 REST call     (urllib, GEMINI_API_KEY from environment only)
    → JSON parse + minimal schema check
    → Deterministic post-validation (C1)
    → Run record (dict) for inspection

Standard library only. Python 3.9+.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Fixed target model (AGENTS.md §17 Base LLM). Changing model / generation
# settings is a Semantic Change and requires Human approval.
# ---------------------------------------------------------------------------
MODEL_ID = "gemma-4-31b-it"
ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL_ID}:generateContent"
)
API_KEY_ENV = "GEMINI_API_KEY"
HTTP_TIMEOUT_SEC = 120

REPO_ROOT = Path(__file__).resolve().parent.parent

# Run status vocabulary (kept as plain strings on purpose)
CONFIG_ERROR = "CONFIG_ERROR"
HTTP_ERROR = "HTTP_ERROR"
API_ERROR = "API_ERROR"
EMPTY_RESPONSE = "EMPTY_RESPONSE"
JSON_PARSE_ERROR = "JSON_PARSE_ERROR"
SCHEMA_ERROR = "SCHEMA_ERROR"
VALIDATION_ERROR = "VALIDATION_ERROR"
SUCCESS = "SUCCESS"

# ---------------------------------------------------------------------------
# C1 — Investment profile Hard Constraint (Human-approved, case.md §4).
# The 5-level scale below is copied from the Frozen case, not from a Source.
# ---------------------------------------------------------------------------
INVESTMENT_PROFILE_SCALE: List[str] = [
    "안정형",
    "안정추구형",
    "위험중립형",
    "적극투자형",
    "공격투자형",
]
# Accepted risk_level labels for candidates that are not investment directions
# (e.g. "confirm first", "keep as is"). Anything else outside the scale is
# reported as UNVERIFIABLE by the validator, never silently accepted.
NON_INVESTMENT_RISK_LABELS = {"해당없음", "N/A", "n/a", "없음"}


# ===========================================================================
# 1. Frozen Customer Input
# ===========================================================================
@dataclass
class CustomerInput:
    case_id: str
    source_file: str
    source_sha256: str
    lines: List[str]  # bullet lines exactly as written in case.md §2

    def as_text(self) -> str:
        return "\n".join(self.lines)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_customer_input(case_id: str) -> CustomerInput:
    """Extract the bullet lines of `## 2. Customer Input` from the Frozen case.

    Deliberately minimal: no Markdown parser. Only bullet lines (`- ` / `  - `)
    between the §2 heading and the next `---` are taken. Prose in §2 (synthetic
    origin note, excluded-fields note) is NOT sent to the model.
    """
    path = REPO_ROOT / "cases" / case_id / "case.md"
    if not path.is_file():
        raise FileNotFoundError(f"Frozen case not found: {path}")
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^## 2\. Customer Input\n(.*?)^---", text, re.S | re.M)
    if not m:
        raise ValueError("case.md: '## 2. Customer Input' section not found")
    lines = [ln.rstrip() for ln in m.group(1).splitlines() if re.match(r"^\s*- ", ln)]
    if not lines:
        raise ValueError("case.md §2 contains no bullet lines")
    return CustomerInput(case_id, str(path.relative_to(REPO_ROOT)), _sha256(path), lines)


def _frozen_status(case_id: str) -> Dict[str, str]:
    """Read the Freeze block of case.md (for the run record only)."""
    path = REPO_ROOT / "cases" / case_id / "case.md"
    text = path.read_text(encoding="utf-8")
    out = {}
    for key in ("Status", "Frozen At", "Approved By"):
        m = re.search(rf"^- {key}: ?(.*)$", text, re.M)
        out[key] = (m.group(1).strip() if m else "")
    return out


# ===========================================================================
# 2. Constraint Context (deterministic, pre-reasoning)
# ===========================================================================
@dataclass
class ConstraintContext:
    constraint_id: str
    investment_profile: str
    allowed_levels: List[str]
    forbidden_levels: List[str]
    basis: str

    def as_text(self) -> str:
        return (
            f"[{self.constraint_id}] 투자성향 Hard Constraint\n"
            f"- 고객 투자성향(확인됨): {self.investment_profile}\n"
            f"- 투자성향 5단계: {' < '.join(INVESTMENT_PROFILE_SCALE)}\n"
            f"- 허용 위험수준 (Solution 방향에 사용 가능): {', '.join(self.allowed_levels)}\n"
            f"- 제외 위험수준 (Solution 후보로 생성 금지): {', '.join(self.forbidden_levels)}\n"
            f"- 근거: {self.basis}"
        )


def build_constraint_context(customer: CustomerInput) -> ConstraintContext:
    """C1: derive allowed / forbidden levels from the Known investment profile.

    The profile is read from the Frozen Customer Input (not guessed). The rule
    "same or lower risk level only" is the Human-approved C1 (case.md §4).
    """
    joined = customer.as_text()
    m = re.search(r"투자성향:\s*\**([가-힣]+)\**", joined)
    if not m:
        raise ValueError("Customer Input has no '투자성향:' line — C1 cannot be built")
    profile = m.group(1)
    if profile not in INVESTMENT_PROFILE_SCALE:
        raise ValueError(f"Unknown investment profile label: {profile!r}")
    idx = INVESTMENT_PROFILE_SCALE.index(profile)
    return ConstraintContext(
        constraint_id="C1",
        investment_profile=profile,
        allowed_levels=INVESTMENT_PROFILE_SCALE[: idx + 1],
        forbidden_levels=INVESTMENT_PROFILE_SCALE[idx + 1 :],
        basis="Human-approved Constraint (cases/%s/case.md §4 C1). 공식 적합성 기준 Source는 미확보."
        % customer.case_id,
    )


# ===========================================================================
# 3. Knowledge Context (static selection from the Frozen knowledge pack)
# ===========================================================================
# Which bullet labels of each K-item are sent to the model.
# NOT sent on purpose: "Case Relevance" and "Case-local Interpretation"
# (they pre-apply the knowledge to this very case = answer hints) and
# "Limitation" (usage boundaries phrased in Evaluator vocabulary — they
# belong to the Evaluator, not to the runtime prompt).
KNOWLEDGE_FIELDS_SENT = ("Knowledge", "Authority / Status")


@dataclass
class KnowledgeItem:
    kid: str
    title: str
    basis_type: str
    fields: Dict[str, str]  # label -> text (only labels in KNOWLEDGE_FIELDS_SENT)

    def as_text(self) -> str:
        parts = [f"### {self.kid}. {self.title}  (Basis: {self.basis_type})"]
        for label in KNOWLEDGE_FIELDS_SENT:
            if label in self.fields:
                parts.append(f"- {label}: {self.fields[label]}")
        return "\n".join(parts)


_BULLET_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*:\s*(?P<body>.*)$")


def load_knowledge_items(case_id: str) -> Tuple[List[KnowledgeItem], str, str]:
    """Parse `### K-xxx.` sections of the Frozen knowledge pack.

    Returns (items, relative path, sha256). Bullets are captured by their bold
    label; continuation lines (sub-bullets / wrapped text) are appended to the
    last label. Labels are normalised so that e.g. 'Knowledge (Source-derived)'
    → label 'Knowledge' with basis_type 'Source-derived', and
    'Limitation (사용 범위 한정)' → 'Limitation'.
    """
    path = REPO_ROOT / "cases" / case_id / "knowledge_pack.md"
    if not path.is_file():
        raise FileNotFoundError(f"Frozen knowledge pack not found: {path}")
    text = path.read_text(encoding="utf-8")
    items: List[KnowledgeItem] = []
    blocks = re.split(r"^(?=### K-\d{3}\. )", text, flags=re.M)
    for block in blocks:
        head = re.match(r"^### (K-\d{3})\. (.+)$", block, re.M)
        if not head:
            continue
        kid, title = head.group(1), head.group(2).strip()
        body = block[head.end():]
        # stop at section separators / next top-level heading
        body = re.split(r"^---\s*$|^## ", body, maxsplit=1, flags=re.M)[0]
        fields: Dict[str, str] = {}
        basis_type = ""
        current: Optional[str] = None
        for ln in body.splitlines():
            m = _BULLET_RE.match(ln)
            if m:
                raw_label = m.group("label").strip()
                base = re.sub(r"\s*\(.*\)\s*$", "", raw_label).strip()
                if base == "Knowledge":
                    bt = re.search(r"\((.+)\)", raw_label)
                    basis_type = bt.group(1).strip() if bt else ""
                current = base
                fields[current] = m.group("body").strip()
            elif current and ln.strip():
                fields[current] += "\n" + ln.rstrip()
        kept = {k: v for k, v in fields.items() if k in KNOWLEDGE_FIELDS_SENT}
        items.append(KnowledgeItem(kid, title, basis_type or "unspecified", kept))
    if not items:
        raise ValueError("knowledge_pack.md: no '### K-xxx.' items found")
    return items, str(path.relative_to(REPO_ROOT)), _sha256(path)


# ===========================================================================
# 4. Prompt (five identifiable sections)
# ===========================================================================
SYSTEM_ROLE = """당신은 은행 직원의 개인형IRP 사후관리 판단을 지원하는 의사결정 지원 Agent다.

역할 원칙:
1. 확인된 사실(제공된 고객정보)과 그로부터 추론한 가능성을 분리해서 다룬다. 추론을 사실처럼 쓰지 않는다.
2. 제공된 고객정보로 확인되지 않은 고객의 의도·사정·계획은 임의로 채우지 않고, 추가 확인이 필요한 사항으로 명시한다.
3. 업무적 판단은 제공된 Knowledge에 근거한다. Knowledge와 고객정보에 없는 업무 사실, 제도 규칙, 수치(금리·수익률·비중 등)를 생성하지 않는다.
4. 제공된 Constraint를 위반하는 Solution 방향을 생성하지 않는다.
5. 특정 상품명을 추천하지 않는다. 판단은 관리 필요성과 관리방향·Solution 유형 수준에서 한다.
6. 판단의 근거로 사용한 고객정보와 Knowledge를 밝힌다.
7. 최종 결과는 직원이 고객관리를 수행하기 위한 판단 지원 정보이며, 고객에게 직접 전달하는 문장이 아니다."""

CUSTOMER_CONTEXT_NOTE = (
    "아래 항목은 시스템에서 조회된 정보(Observed / Calculated)다. "
    "고객이 직접 밝힌 정보(Customer-stated)는 포함되어 있지 않다. "
    "아래에 없는 정보는 제공되지 않은 것이다."
)

OUTPUT_INSTRUCTION = """다음 JSON 객체 하나만 출력한다. JSON 앞뒤에 다른 텍스트, 설명, 코드펜스를 붙이지 않는다. 모든 문자열 값은 한국어로 쓴다.

{
  "current_situation": "고객정보로부터 해석한 현재 상황 (사실과 추론을 구분해서 서술)",
  "known_facts_used": ["판단에 사용한 확인된 사실을 고객정보 항목 그대로 나열"],
  "unknowns_or_confirmations": ["판단에 중요하지만 제공된 정보로 확인되지 않아 추가 확인이 필요한 사항"],
  "management_need": {
    "decision": "현재 이 고객에게 관리가 필요한지에 대한 판단 (자유 서술)",
    "reason": "그 판단의 근거 (사용한 사실·Knowledge를 포함)"
  },
  "solution_candidates": [
    {
      "direction": "Solution 방향 또는 유형 (상품명 아님)",
      "condition": "이 방향이 유효하기 위한 전제 조건 또는 확인 사항",
      "risk_level": "이 방향에 해당하는 투자성향 위험수준. 5단계(안정형/안정추구형/위험중립형/적극투자형/공격투자형) 중 하나. 투자 방향이 아닌 경우(예: 확인 우선, 현 상태 관련) '해당없음'"
    }
  ],
  "knowledge_ids_used": ["근거로 사용한 Knowledge ID (예: K-001)"],
  "employee_brief": "직원용 요약: 왜 지금 이 고객을 봐야 하는지(또는 아닌지), 무엇을 먼저 확인할지, 어떤 방향을 검토할 수 있는지, 어떤 제약이 있는지"
}"""


@dataclass
class Prompt:
    system_role: str
    customer_context: str
    constraint_context: str
    knowledge_context: str
    output_instruction: str
    knowledge_ids: List[str] = field(default_factory=list)

    def as_text(self) -> str:
        return "\n\n".join(
            [
                "## 역할과 원칙\n" + self.system_role,
                "## 고객정보\n" + self.customer_context,
                "## 적용 Constraint\n" + self.constraint_context,
                "## Knowledge (판단 근거로 사용할 업무지식)\n" + self.knowledge_context,
                "## 출력 형식\n" + self.output_instruction,
            ]
        )


def build_prompt(
    customer: CustomerInput,
    constraint: ConstraintContext,
    knowledge: List[KnowledgeItem],
) -> Prompt:
    knowledge_text = (
        "각 Knowledge에는 근거 유형(Basis)이 표시되어 있다. Source-derived는 행내 자료에서 확인된 내용, "
        "Human-approved는 담당자가 확정한 기준, Case-local Interpretation은 자료를 바탕으로 정리한 해석이다.\n\n"
        + "\n\n".join(k.as_text() for k in knowledge)
    )
    return Prompt(
        system_role=SYSTEM_ROLE,
        customer_context=CUSTOMER_CONTEXT_NOTE + "\n\n" + customer.as_text(),
        constraint_context=constraint.as_text(),
        knowledge_context=knowledge_text,
        output_instruction=OUTPUT_INSTRUCTION,
        knowledge_ids=[k.kid for k in knowledge],
    )


# ===========================================================================
# 5. Gemma 4 REST adapter
# ===========================================================================
@dataclass
class ModelResponse:
    status: str
    text: str = ""
    finish_reason: str = ""
    usage: Dict[str, Any] = field(default_factory=dict)
    http_status: Optional[int] = None
    error: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)  # API body (no headers)


def _api_key() -> str:
    key = os.environ.get(API_KEY_ENV, "").strip()
    if not key:
        raise EnvironmentError(f"{API_KEY_ENV} is not set")
    return key


def call_gemma(prompt_text: str, timeout: int = HTTP_TIMEOUT_SEC) -> ModelResponse:
    """POST the prompt to generateContent and extract the model text.

    No generationConfig is sent (API defaults) — changing generation settings
    is a Semantic Change. No retry / backoff / streaming.
    """
    try:
        key = _api_key()
    except EnvironmentError as e:
        return ModelResponse(status=CONFIG_ERROR, error=str(e))

    body = {"contents": [{"parts": [{"text": prompt_text}]}]}
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            http_status = resp.status
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:  # pragma: no cover
            err_body = ""
        return ModelResponse(status=HTTP_ERROR, http_status=e.code, error=f"HTTP {e.code}: {err_body[:2000]}")
    except urllib.error.URLError as e:
        return ModelResponse(status=HTTP_ERROR, error=f"URL error: {e.reason}")
    except Exception as e:  # timeout, decode, ...
        return ModelResponse(status=HTTP_ERROR, error=f"{type(e).__name__}: {e}")

    if isinstance(payload, dict) and "error" in payload:
        return ModelResponse(status=API_ERROR, http_status=http_status, error=json.dumps(payload["error"], ensure_ascii=False)[:2000], raw=payload)

    candidates = payload.get("candidates") or []
    if not candidates:
        return ModelResponse(
            status=EMPTY_RESPONSE,
            http_status=http_status,
            error="no candidates; promptFeedback=" + json.dumps(payload.get("promptFeedback", {}), ensure_ascii=False),
            raw=payload,
        )
    cand = candidates[0]
    parts = (cand.get("content") or {}).get("parts") or []
    # Only visible text parts are kept; any part flagged as thought is skipped
    # (we do not store hidden chain-of-thought).
    texts = [p.get("text", "") for p in parts if isinstance(p, dict) and "text" in p and not p.get("thought")]
    text = "".join(texts).strip()
    if not text:
        return ModelResponse(status=EMPTY_RESPONSE, http_status=http_status, error="candidate has no text part", raw=payload,
                             finish_reason=str(cand.get("finishReason", "")))
    return ModelResponse(
        status=SUCCESS,
        text=text,
        finish_reason=str(cand.get("finishReason", "")),
        usage=payload.get("usageMetadata", {}),
        http_status=http_status,
        raw=payload,
    )


# ===========================================================================
# 6. JSON parse + minimal schema check (standard library only)
# ===========================================================================
REQUIRED_TOP = ["current_situation", "known_facts_used", "unknowns_or_confirmations",
                "management_need", "solution_candidates", "employee_brief"]


def parse_model_json(text: str) -> Tuple[Optional[Dict[str, Any]], List[str], str]:
    """Return (obj, normalizations_applied, error).

    Allowed normalisation: strip Markdown code fences; slice from first '{' to
    last '}'. Nothing inside the JSON is rewritten.
    """
    norms: List[str] = []
    s = text.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", s, re.S)
    if fence:
        s = fence.group(1).strip()
        norms.append("stripped_code_fence")
    if not s.startswith("{"):
        i, j = s.find("{"), s.rfind("}")
        if i != -1 and j != -1 and j > i:
            s = s[i : j + 1]
            norms.append("sliced_outer_braces")
    try:
        obj = json.loads(s)
    except json.JSONDecodeError as e:
        return None, norms, f"JSONDecodeError: {e}"
    if not isinstance(obj, dict):
        return None, norms, f"top-level JSON is {type(obj).__name__}, expected object"
    return obj, norms, ""


def check_schema(obj: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing key: {k}")
    mn = obj.get("management_need")
    if mn is not None:
        if not isinstance(mn, dict):
            errs.append("management_need must be an object")
        else:
            for k in ("decision", "reason"):
                if not str(mn.get(k, "")).strip():
                    errs.append(f"management_need.{k} is empty")
    sc = obj.get("solution_candidates")
    if sc is not None:
        if not isinstance(sc, list):
            errs.append("solution_candidates must be a list")
        else:
            for i, c in enumerate(sc):
                if not isinstance(c, dict):
                    errs.append(f"solution_candidates[{i}] must be an object")
                    continue
                for k in ("direction", "risk_level"):
                    if not str(c.get(k, "")).strip():
                        errs.append(f"solution_candidates[{i}].{k} is empty")
    for k in ("known_facts_used", "unknowns_or_confirmations"):
        if k in obj and not isinstance(obj[k], list):
            errs.append(f"{k} must be a list")
    if "employee_brief" in obj and not str(obj["employee_brief"]).strip():
        errs.append("employee_brief is empty")
    return errs


# ===========================================================================
# 7. Deterministic post-reasoning validation (C1 only, by design)
# ===========================================================================
def validate_c1(obj: Dict[str, Any], constraint: ConstraintContext) -> Dict[str, Any]:
    """Check each solution candidate's risk_level against C1.

    FAIL    : risk_level names a forbidden level.
    PASS    : risk_level is an allowed level or a non-investment label.
    UNVERIFIABLE: any other label (reported, not silently accepted).
    """
    results = []
    overall = "PASS"
    for i, c in enumerate(obj.get("solution_candidates") or []):
        lvl = str(c.get("risk_level", "")).strip() if isinstance(c, dict) else ""
        if lvl in constraint.forbidden_levels:
            verdict = "FAIL"
            overall = "FAIL"
        elif lvl in constraint.allowed_levels or lvl in NON_INVESTMENT_RISK_LABELS:
            verdict = "PASS"
        else:
            verdict = "UNVERIFIABLE"
            if overall != "FAIL":
                overall = "UNVERIFIABLE"
        results.append({"index": i, "direction": (c.get("direction") if isinstance(c, dict) else None), "risk_level": lvl, "verdict": verdict})
    return {
        "constraint_id": constraint.constraint_id,
        "investment_profile": constraint.investment_profile,
        "allowed_levels": constraint.allowed_levels,
        "forbidden_levels": constraint.forbidden_levels,
        "candidates": results,
        "overall": overall,
    }


# ===========================================================================
# 8. Orchestration
# ===========================================================================
def _git_head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), text=True).strip()
    except Exception:
        return ""


def prepare(case_id: str) -> Tuple[CustomerInput, ConstraintContext, List[KnowledgeItem], Prompt, Dict[str, str]]:
    customer = load_customer_input(case_id)
    constraint = build_constraint_context(customer)
    knowledge, kp_path, kp_sha = load_knowledge_items(case_id)
    prompt = build_prompt(customer, constraint, knowledge)
    meta = {"knowledge_pack": kp_path, "knowledge_pack_sha256": kp_sha}
    return customer, constraint, knowledge, prompt, meta


def run_case(case_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """Execute the case and return an observable run record (dict)."""
    started = _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    record: Dict[str, Any] = {
        "case_id": case_id,
        "started_at": started,
        "model": MODEL_ID,
        "endpoint": ENDPOINT,
        "generation_config": None,  # API defaults; changing this is a Semantic Change
        "git_head": _git_head(),
        "status": None,
        "error": "",
    }
    try:
        customer, constraint, knowledge, prompt, meta = prepare(case_id)
    except Exception as e:
        record.update(status=CONFIG_ERROR, error=f"{type(e).__name__}: {e}")
        return record

    record.update(
        {
            "frozen_case": {"file": customer.source_file, "sha256": customer.source_sha256, **_frozen_status(case_id)},
            "frozen_knowledge_pack": meta,
            "customer_input": customer.lines,
            "constraint_context": {
                "constraint_id": constraint.constraint_id,
                "investment_profile": constraint.investment_profile,
                "allowed_levels": constraint.allowed_levels,
                "forbidden_levels": constraint.forbidden_levels,
                "basis": constraint.basis,
            },
            "knowledge_ids_used": prompt.knowledge_ids,
            "knowledge_fields_sent": list(KNOWLEDGE_FIELDS_SENT),
            "prompt": {
                "system_role": prompt.system_role,
                "customer_context": prompt.customer_context,
                "constraint_context": prompt.constraint_context,
                "knowledge_context": prompt.knowledge_context,
                "output_instruction": prompt.output_instruction,
            },
            "prompt_chars": len(prompt.as_text()),
        }
    )
    if dry_run:
        record.update(status="DRY_RUN")
        return record

    resp = call_gemma(prompt.as_text())
    record["model_response"] = {
        "status": resp.status,
        "http_status": resp.http_status,
        "finish_reason": resp.finish_reason,
        "usage": resp.usage,
        "error": resp.error,
    }
    record["raw_model_output"] = resp.text
    if resp.status != SUCCESS:
        record.update(status=resp.status, error=resp.error)
        return record

    obj, norms, perr = parse_model_json(resp.text)
    record["json_normalizations"] = norms
    if obj is None:
        record.update(status=JSON_PARSE_ERROR, error=perr)
        return record
    record["parsed_output"] = obj

    schema_errs = check_schema(obj)
    record["schema_errors"] = schema_errs
    if schema_errs:
        record.update(status=SCHEMA_ERROR, error="; ".join(schema_errs))
        # still run C1 on whatever candidates exist, for observability
        record["validation"] = validate_c1(obj, constraint)
        return record

    validation = validate_c1(obj, constraint)
    record["validation"] = validation
    record["employee_brief"] = obj.get("employee_brief", "")
    record.update(status=(VALIDATION_ERROR if validation["overall"] == "FAIL" else SUCCESS),
                  error=("C1 violated by a solution candidate" if validation["overall"] == "FAIL" else ""))
    return record
