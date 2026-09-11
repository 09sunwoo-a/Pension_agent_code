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

Architecture Revision #1 (REV-001, Human-approved 2026-09-01; see prototype/REVISIONS.md):
  - Management Judgment is formed before any Next Action (F-005 Action/Change Bias)
  - Knowledge is rendered with Case Relevance / Usage Boundary / Source (F-006)
  - C2 fund risk-grade eligibility validator (HD-2.1 mapping) replaces DETECT_ONLY

Architecture Revision #2 (REV-002, Human-approved Step 3 2026-08-31; see
prototype/REVISIONS.md and design/TARGET_CONCEPT.md / EVIDENCE_PACK_SPEC.md /
EMPLOYEE_BRIEF_SPEC.md):
  - Input: 8-section Customer Evidence Pack (cases/<CASE>/input_v2.md).
    A case runs on the REV-002 path IFF input_v2.md exists; otherwise the
    legacy REV-001 path below is used unchanged (regression comparability).
  - Preprocessing: Arithmetic Derived (elapsed days, D-n) and Rule-derived
    Facts (pension-open eligibility, DO expected application base date) are
    computed deterministically from a fenced ```json machine block; Rule-derived
    facts carry rule_source / rule_as_of. No semantic labels ("방치" 류) are
    ever produced by preprocessing.
  - Output: REV-001 structured judgment + supporting_evidence_ids provenance
    + employee_brief as a 5-section object (S1 situation / S2 management point
    with confirm-first / S3 direction with branch preservation / S4 consult
    points with scripts / S5 tips with sources).
  - Validators added (deterministic only — semantic checks stay with the
    Evaluator): forbidden judgment words, LaTeX residue, evidence-id validity,
    screen-number survival, candidate-pool violation; C1/C2/C3 kept and the
    C2/C3 scan extended over the serialized brief.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
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
HTTP_TIMEOUT_SEC = 300  # network read timeout only (Operational; no generation setting)

REPO_ROOT = Path(__file__).resolve().parent.parent


def force_utf8_stdio() -> None:
    """stdout/stderr를 UTF-8로 강제한다.

    Windows 콘솔/리다이렉트 환경은 기본 인코딩이 cp949라서 한글·특수문자
    (→, · 등) 출력 시 UnicodeEncodeError 또는 깨짐이 발생할 수 있다.
    모든 CLI 진입점에서 가장 먼저 호출한다.
    """
    for stream in (sys.stdout, sys.stderr):
        if stream is None:
            continue
        enc = (getattr(stream, "encoding", None) or "").lower().replace("-", "")
        if enc != "utf8":
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass  # 재설정 불가 환경(파이프 등)에서는 조용히 넘어간다

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

# ---------------------------------------------------------------------------
# C3 — Default-option portfolio eligibility by investment profile
# (Human-approved HD-2, golden/HUMAN_DECISIONS.md; mapping per SRC-089 L43-54,
#  recorded in cases/CONSTRAINT_MAP.md C3). Execution-enabling implementation
#  (HD-5.1): the approved mapping is coded as-is, no new rule is introduced.
# Value = minimum profile index (INVESTMENT_PROFILE_SCALE) allowed to hold it.
# ---------------------------------------------------------------------------
DEFAULT_OPTION_MIN_PROFILE: Dict[str, int] = {
    "지켜드림": 0,   # 초저위험 — 모든 투자성향
    "알파드림": 1,   # 저위험   — 안정추구형 이상
    "뿔려드림": 2,   # 중위험   — 위험중립형 이상
    "모두드림": 4,   # 고위험   — 공격투자형만
}
# ---------------------------------------------------------------------------
# C2 — Fund risk-grade eligibility by investment profile (Human-approved
# HD-2 / HD-2.1; official KB 투자권유 기준, SRC-096). Grade 1 = highest risk.
# The profile caps the MAXIMUM risk the customer may be offered; lower-risk
# grades are always allowed.
# ---------------------------------------------------------------------------
FUND_RISK_GRADES: Dict[str, int] = {
    "매우높은위험": 1,
    "높은위험": 2,
    "다소높은위험": 3,
    "보통위험": 4,
    "낮은위험": 5,
    "매우낮은위험": 6,
}
# Minimum (i.e. riskiest) grade number the profile may be offered.
PROFILE_MIN_FUND_GRADE: Dict[str, int] = {
    "안정형": 6,
    "안정추구형": 5,
    "위험중립형": 4,
    "적극투자형": 3,
    "공격투자형": 1,
}
# Longest label first so that "매우높은위험" is not matched as "높은위험".
FUND_RISK_GRADE_LABELS = sorted(FUND_RISK_GRADES, key=len, reverse=True)


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
        idx = INVESTMENT_PROFILE_SCALE.index(self.investment_profile)
        do_ok = [n for n, m in DEFAULT_OPTION_MIN_PROFILE.items() if idx >= m]
        do_no = [n for n, m in DEFAULT_OPTION_MIN_PROFILE.items() if idx < m]
        min_g = PROFILE_MIN_FUND_GRADE[self.investment_profile]
        g_ok = [f"{g}등급 {n}" for n, g in FUND_RISK_GRADES.items() if g >= min_g]
        g_no = [f"{g}등급 {n}" for n, g in FUND_RISK_GRADES.items() if g < min_g]
        return (
            f"[{self.constraint_id}] 투자성향 Hard Constraint\n"
            f"- 고객 투자성향(확인됨): {self.investment_profile}\n"
            f"- 투자성향 5단계: {' < '.join(INVESTMENT_PROFILE_SCALE)}\n"
            f"- 허용 위험수준 (Solution 방향에 사용 가능): {', '.join(self.allowed_levels)}\n"
            f"- 제외 위험수준 (Solution 후보로 생성 금지): {', '.join(self.forbidden_levels)}\n"
            f"- 투자성향은 허용 가능한 최대 위험수준의 상한이다. 고객이 그 수준까지 위험을 부담해야 한다는 뜻이 아니며, "
            f"더 낮은 위험수준의 운용은 항상 허용된다. 투자성향과 현재 운용상태의 차이만으로 관리 필요·변경 필요를 판정하지 않는다.\n"
            f"- 근거: {self.basis}\n\n"
            f"[C2] 펀드 위험등급 Eligibility (Human-approved, KB 투자권유 기준 SRC-096)\n"
            f"- 상품 위험등급: 1등급 매우높은위험 < 2등급 높은위험 < 3등급 다소높은위험 < 4등급 보통위험 < 5등급 낮은위험 < 6등급 매우낮은위험\n"
            f"- 이 고객에게 권유 가능한 펀드 위험등급: {', '.join(g_ok)}\n"
            f"- 권유 불가 (Action으로 생성 금지): {', '.join(g_no) if g_no else '없음'}\n"
            f"- 이미 보유 중인 상위 등급 상품은 위반이 아니다. 신규 매수·교체 방향에만 적용한다.\n\n"
            f"[C3] 디폴트옵션 포트폴리오 Eligibility (Human-approved)\n"
            f"- 이 고객이 가입 가능한 디폴트옵션 포트폴리오: {', '.join(do_ok)}\n"
            f"- 가입 불가 (Action으로 생성 금지): {', '.join(do_no) if do_no else '없음'}\n"
            f"- 매핑: 지켜드림(초저위험)=모든 성향 / 알파드림(저위험)=안정추구형 이상 / 뿔려드림(중위험)=위험중립형 이상 / 모두드림(고위험)=공격투자형만"
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
        basis="Human-approved Constraint (golden/HUMAN_DECISIONS.md HD-2·HD-2.1; cases/%s/case.md §4). C2 매핑은 KB 투자권유 기준(SRC-096)."
        % customer.case_id,
    )


# ===========================================================================
# 3. Knowledge Context (static selection from the Frozen knowledge pack)
# ===========================================================================
# Which bullet labels of each K-item are sent to the model.
# REV-001 (F-006): "Case Relevance" and "Limitation" (rendered as Usage
# Boundary) and "Source / Location" are now sent so the model knows WHY the
# knowledge matters here and WHAT it must not conclude from it.
# Still NOT sent: "Case-local Interpretation" (pre-applied answer hints).
KNOWLEDGE_FIELDS_SENT = ("Knowledge", "Case Relevance", "Limitation", "Authority / Status", "Source / Location")
KNOWLEDGE_FIELD_RENDER = {
    "Knowledge": "Knowledge",
    "Case Relevance": "Case Relevance (왜 이 고객에게 지금 중요한가)",
    "Limitation": "Usage Boundary (이 Knowledge만으로 단정하면 안 되는 것)",
    "Authority / Status": "Authority / As-of",
    "Source / Location": "Source",
}


@dataclass
class KnowledgeItem:
    kid: str
    title: str
    basis_type: str
    fields: Dict[str, str]  # label -> text (only labels in KNOWLEDGE_FIELDS_SENT)

    def as_text(self) -> str:
        parts = [f"### {self.kid}. {self.title}  (Basis: {self.basis_type})"]
        for label in KNOWLEDGE_FIELDS_SENT:
            if label in self.fields and self.fields[label].strip() not in ("", "—", "-"):
                parts.append(f"- {KNOWLEDGE_FIELD_RENDER.get(label, label)}: {self.fields[label]}")
        return "\n".join(parts)


_BULLET_RE = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*:\s*(?P<body>.*)$")


def load_knowledge_items(case_id: str) -> Tuple[List[KnowledgeItem], str, str]:
    """Knowledge Context entry point (interface unchanged since REV-001).

    Default: parse the Frozen per-case knowledge_pack.md (manual pack).
    P3-A: when the environment variable P3A_KNOWLEDGE_SELECTION=1 is set, the
    Minimal Selection Layer (prototype/selector.py) supplies the Official
    Knowledge / Knowledge Gap portion instead, returning the same K-item
    structure — everything downstream (prompt, validators, record) unchanged.
    Frozen runs are unaffected unless the flag is explicitly set.
    """
    if os.environ.get("P3_HYBRID_KNOWLEDGE_SELECTION") == "1":
        import hybrid_selector as _hybrid
        return _hybrid.load_knowledge_items_hybrid(case_id)
    if os.environ.get("P3A_KNOWLEDGE_SELECTION") == "1":
        import selector as _selector
        return _selector.load_knowledge_items_selected(case_id)
    return _load_knowledge_items_manual(case_id)


def _load_knowledge_items_manual(case_id: str) -> Tuple[List[KnowledgeItem], str, str]:
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
7. 최종 결과는 직원이 고객관리를 수행하기 위한 판단 지원 정보이며, 고객에게 직접 전달하는 문장이 아니다.
8. Action보다 Management Judgment가 먼저다. 이 고객에게 지금 어떤 종류의 관리판단이 맞는지(개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가)를 Customer Context — 왜 이 상태인가, 최근 입금·교체매매 과정인가, 고객이 의도적으로 유지 중인가, 사용계획이 있는가, 관리 필요성이 실제로 존재하는가 — 를 근거로 먼저 확정한 뒤, 그 판단에 맞는 Next Action을 만든다.
9. 어느 방향도 기본값이 아니다. 변경·유지·확인·정보안내·고객선택존중·실행불가 중 근거가 요구하는 것을 고른다. 근거가 개입을 요구하면 구체적인 변경 Action을, 유지가 맞으면 유지와 재점검 조건을, 확인이 먼저면 확인 전에는 상품·운용 결론을 내리지 않는다. "관리 필요"는 "변경 필요"와 같은 말이 아니며, 투자성향은 허용 상한이지 그 수준까지 운용하라는 요구가 아니다.
10. Knowledge는 Case Relevance와 Usage Boundary까지 사용한다. 관련도가 높은 Knowledge의 시한·조건·절차·화면 같은 세부를 판단과 Action에 실제로 반영하고, Usage Boundary가 금지한 단정은 하지 않는다."""

CUSTOMER_CONTEXT_NOTE_OBSERVED_ONLY = (
    "아래 항목은 시스템에서 조회된 정보(Observed / Calculated)다. "
    "고객이 직접 밝힌 정보(Customer-stated)는 포함되어 있지 않다. "
    "아래에 없는 정보는 제공되지 않은 것이다."
)
CUSTOMER_CONTEXT_NOTE_MIXED = (
    "아래 항목은 별도 표시가 없으면 시스템에서 조회된 정보(Observed / Calculated)다. "
    "`[Customer-stated]` 표시가 있는 항목은 고객이 상담·문의에서 직접 밝힌 내용이며, 그 시점의 발화이지 확정된 현재 의사가 아니다. "
    "`[Event]` 표시는 시스템에서 발생한 사건이다. 아래에 없는 정보는 제공되지 않은 것이다."
)
CUSTOMER_STATED_TAG = "[Customer-stated]"


def customer_context_note(customer: "CustomerInput") -> str:
    """Pick the provenance note that is actually true for this input (serialization correctness)."""
    if any(CUSTOMER_STATED_TAG in ln for ln in customer.lines):
        return CUSTOMER_CONTEXT_NOTE_MIXED
    return CUSTOMER_CONTEXT_NOTE_OBSERVED_ONLY


# kept for backward reference in run records
CUSTOMER_CONTEXT_NOTE = CUSTOMER_CONTEXT_NOTE_OBSERVED_ONLY

OUTPUT_INSTRUCTION = """다음 JSON 객체 하나만 출력한다. JSON 앞뒤에 다른 텍스트, 설명, 코드펜스를 붙이지 않는다. 모든 문자열 값은 한국어로 쓴다. 키 순서대로 생각한다: 상황 → 사실/미확인 → 관리판단 → 다음 행동 → 요약.

{
  "current_situation": "고객정보로부터 해석한 현재 상황 (사실과 추론을 구분해서 서술)",
  "known_facts_used": ["판단에 사용한 확인된 사실을 고객정보 항목 그대로 나열"],
  "unknowns_or_confirmations": ["판단에 중요하지만 제공된 정보로 확인되지 않아 추가 확인이 필요한 사항"],
  "management_judgment": {
    "judgment": "이 고객에게 지금 맞는 관리판단 유형. 다음 중 하나 이상을 '/'로 구분해 기재: 개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가",
    "reasoning": "왜 그 판단인지 — 왜 이 상태가 나타났는지, 고객 의도·사용계획·시한을 어떻게 해석했는지, 관리 필요성이 실제로 존재하는지를 사실·Knowledge로 근거",
    "must_confirm_before_action": ["Action을 확정하기 전에 먼저 확인해야 할 것 (없으면 빈 배열)"]
  },
  "next_actions": [
    {
      "action": "위 판단에 맞는 다음 행동 (변경·유지·확인·정보안내·절차·연계 모두 가능; 상품명 아님)",
      "kind": "변경 / 유지 / 확인 / 정보안내 / 절차 / 연계 중 하나",
      "condition": "이 행동이 유효하기 위한 전제 조건 또는 확인 사항",
      "risk_level": "운용 방향(변경 또는 유지)이면 그 방향의 투자성향 위험수준. 5단계(안정형/안정추구형/위험중립형/적극투자형/공격투자형) 중 하나. 운용 방향이 아니면 '해당없음'"
    }
  ],
  "knowledge_ids_used": ["근거로 사용한 Knowledge ID (예: K-001)"],
  "employee_brief": "직원용 요약: 관리판단과 그 이유, 무엇을 먼저 확인할지, 어떤 다음 행동을 어떤 조건에서 할지, 어떤 제약이 있는지. 위 판단·조건·제약의 의미를 바꾸지 않는다."
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
        "Human-approved는 담당자가 확정한 기준, Case-local Interpretation은 자료를 바탕으로 정리한 해석이다. "
        "Case Relevance는 이 Knowledge가 이 고객에게 왜 지금 중요한지, Usage Boundary는 이 Knowledge만으로 단정하면 안 되는 것이다. "
        "관련도가 높은 Knowledge의 시한·조건·절차·화면 세부를 실제로 사용하고, Usage Boundary를 넘는 결론을 만들지 않는다.\n\n"
        + "\n\n".join(k.as_text() for k in knowledge)
    )
    return Prompt(
        system_role=SYSTEM_ROLE,
        customer_context=customer_context_note(customer) + "\n\n" + customer.as_text(),
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
                "management_judgment", "next_actions", "employee_brief"]
JUDGMENT_TYPES = ["개입 필요", "추가 확인 우선", "현 상태 유지 가능", "정보 안내 중심", "고객 결정 지원", "실행 불가"]
ACTION_KINDS = ["변경", "유지", "확인", "정보안내", "절차", "연계"]


def detect_judgment_types(obj: Dict[str, Any]) -> List[str]:
    mj = obj.get("management_judgment") or {}
    text = str(mj.get("judgment", "")) if isinstance(mj, dict) else ""
    return [t for t in JUDGMENT_TYPES if t in text]


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
    mj = obj.get("management_judgment")
    if mj is not None:
        if not isinstance(mj, dict):
            errs.append("management_judgment must be an object")
        else:
            for k in ("judgment", "reasoning"):
                if not str(mj.get(k, "")).strip():
                    errs.append(f"management_judgment.{k} is empty")
            if "must_confirm_before_action" in mj and not isinstance(mj["must_confirm_before_action"], list):
                errs.append("management_judgment.must_confirm_before_action must be a list")
            if isinstance(mj.get("judgment"), str) and not detect_judgment_types(obj):
                errs.append("management_judgment.judgment names none of the judgment types")
    na = obj.get("next_actions")
    if na is not None:
        if not isinstance(na, list):
            errs.append("next_actions must be a list")
        else:
            for i, c in enumerate(na):
                if not isinstance(c, dict):
                    errs.append(f"next_actions[{i}] must be an object")
                    continue
                for k in ("action", "kind", "risk_level"):
                    if not str(c.get(k, "")).strip():
                        errs.append(f"next_actions[{i}].{k} is empty")
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
    for i, c in enumerate(obj.get("next_actions") or []):
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
        results.append({"index": i, "action": (c.get("action") if isinstance(c, dict) else None), "kind": (c.get("kind") if isinstance(c, dict) else None), "risk_level": lvl, "verdict": verdict})
    return {
        "constraint_id": constraint.constraint_id,
        "investment_profile": constraint.investment_profile,
        "allowed_levels": constraint.allowed_levels,
        "forbidden_levels": constraint.forbidden_levels,
        "candidates": results,
        "overall": overall,
    }


def _candidate_texts(obj: Dict[str, Any]) -> List[Tuple[int, str, str]]:
    out = []
    for i, c in enumerate(obj.get("next_actions") or []):
        if isinstance(c, dict):
            out.append((i, str(c.get("action", "")), str(c.get("condition", ""))))
    return out


def validate_c3_default_option(obj: Dict[str, Any], constraint: ConstraintContext) -> Dict[str, Any]:
    """C3: a default-option portfolio the customer is not eligible for must not be
    proposed as a next action.

    FAIL   : ineligible portfolio name appears in an action's `action` text.
    REVIEW : ineligible name appears only in `condition` or in employee_brief
             (may be a negation such as '모두드림은 불가') — Evaluator decides.
    PASS   : otherwise.
    """
    idx = INVESTMENT_PROFILE_SCALE.index(constraint.investment_profile)
    ineligible = [n for n, m in DEFAULT_OPTION_MIN_PROFILE.items() if idx < m]
    findings = []
    overall = "PASS"
    for i, d, c in _candidate_texts(obj):
        for name in ineligible:
            if name in d:
                findings.append({"index": i, "portfolio": name, "where": "action", "verdict": "FAIL"})
                overall = "FAIL"
            elif name in c:
                findings.append({"index": i, "portfolio": name, "where": "condition", "verdict": "REVIEW"})
                if overall != "FAIL":
                    overall = "REVIEW"
    brief = str(obj.get("employee_brief", ""))
    for name in ineligible:
        if name in brief:
            findings.append({"index": None, "portfolio": name, "where": "employee_brief", "verdict": "REVIEW"})
            if overall != "FAIL":
                overall = "REVIEW"
    return {"constraint_id": "C3", "investment_profile": constraint.investment_profile,
            "ineligible_portfolios": ineligible, "findings": findings, "overall": overall}


def validate_c2_fund_grade(obj: Dict[str, Any], constraint: ConstraintContext) -> Dict[str, Any]:
    """C2: a fund risk grade the customer may not be offered must not be proposed.

    Mapping (HD-2.1 / SRC-096): 안정형 6 · 안정추구형 5~6 · 위험중립형 4~6 ·
    적극투자형 3~6 · 공격투자형 1~6 (grade 1 = highest risk).
    FAIL   : an ineligible grade label appears in an action's `action` text.
    REVIEW : it appears only in `condition` or employee_brief (may be a
             negation or an existing holding) — Evaluator decides.
    Existing holdings mentioned in current_situation are never checked.
    """
    min_g = PROFILE_MIN_FUND_GRADE[constraint.investment_profile]
    ineligible = [n for n, g in FUND_RISK_GRADES.items() if g < min_g]

    def _hits(text: str) -> List[str]:
        found, rest = [], text
        for lab in FUND_RISK_GRADE_LABELS:  # longest first
            if lab in rest:
                found.append(lab)
                rest = rest.replace(lab, " ")
        return found

    findings = []
    overall = "PASS"
    for i, a, c in _candidate_texts(obj):
        for lab in _hits(a):
            if lab in ineligible:
                findings.append({"index": i, "grade_label": lab, "grade": FUND_RISK_GRADES[lab], "where": "action", "verdict": "FAIL"})
                overall = "FAIL"
        for lab in _hits(c):
            if lab in ineligible:
                findings.append({"index": i, "grade_label": lab, "grade": FUND_RISK_GRADES[lab], "where": "condition", "verdict": "REVIEW"})
                if overall != "FAIL":
                    overall = "REVIEW"
    for lab in _hits(str(obj.get("employee_brief", ""))):
        if lab in ineligible:
            findings.append({"index": None, "grade_label": lab, "grade": FUND_RISK_GRADES[lab], "where": "employee_brief", "verdict": "REVIEW"})
            if overall != "FAIL":
                overall = "REVIEW"
    return {"constraint_id": "C2", "investment_profile": constraint.investment_profile,
            "allowed_min_grade": min_g, "ineligible_labels": ineligible, "findings": findings, "overall": overall}


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
    """Execute the case and return an observable run record (dict).

    Dispatch (frozen artifacts stay on their original path):
      canonical.json → v3 (PRE-P2-REFINEMENT) / input_v2.md → REV-002 / else REV-001.
    """
    if (REPO_ROOT / "cases" / case_id / "canonical.json").is_file():
        return run_case_v3(case_id, dry_run=dry_run)
    if (REPO_ROOT / "cases" / case_id / "input_v2.md").is_file():
        return run_case_rev002(case_id, dry_run=dry_run)
    return run_case_rev001(case_id, dry_run=dry_run)


def run_case_rev001(case_id: str, dry_run: bool = False) -> Dict[str, Any]:
    """Legacy REV-001 execution (unchanged behavior)."""
    started = _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    record: Dict[str, Any] = {
        "case_id": case_id,
        "runtime_revision": "REV-001",
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
    record["validation_c3"] = validate_c3_default_option(obj, constraint)
    record["validation_c2"] = validate_c2_fund_grade(obj, constraint)
    record["judgment_types_detected"] = detect_judgment_types(obj)
    record["employee_brief"] = obj.get("employee_brief", "")
    failed = any(record[k]["overall"] == "FAIL" for k in ("validation", "validation_c3", "validation_c2"))
    errs = []
    if validation["overall"] == "FAIL":
        errs.append("C1 violated by a next action")
    if record["validation_c3"]["overall"] == "FAIL":
        errs.append("C3 ineligible default-option portfolio proposed")
    if record["validation_c2"]["overall"] == "FAIL":
        errs.append("C2 ineligible fund risk grade proposed")
    record.update(status=(VALIDATION_ERROR if failed else SUCCESS), error="; ".join(errs))
    return record


# ===========================================================================
# 9. REV-002 — Customer Evidence Pack (8 sections) + 5-section Employee Brief
#    Spec: design/EVIDENCE_PACK_SPEC.md / design/EMPLOYEE_BRIEF_SPEC.md
#    Path taken iff cases/<CASE>/input_v2.md exists (see run_case dispatch).
# ===========================================================================
RUNTIME_REVISION_V2 = "REV-002"

EVIDENCE_SECTION_TITLES = [
    "Customer / Pension Profile",
    "IRP Current Snapshot",
    "IRP Event Timeline",
    "Whole-Asset Context",
    "Investment Activity",
    "Upcoming Events",
    "Digital / Behavioral Signals",
    "Customer Interaction / CRM Memo",
]
CALCULATED_SECTION_TITLE = "Calculated Facts (시스템 계산)"

SIGNAL_BOUNDARY_NOTE = (
    "(경계) 조회·검색·메뉴 진입·클릭 등의 행동은 관심 가능성 또는 행동 Evidence일 뿐, "
    "고객 의사 자체를 의미하지 않는다. Signal을 고객 의사로 직접 승격하지 않는다."
)
CRM_BOUNDARY_NOTE = (
    "(경계) 아래는 직원이 작성한 상담메모다. 고객 발화 원문(verbatim)이라고 보장하지 않으며, "
    "현재 고객 의사를 확정하는 근거(Ground Truth)가 아니다. 작성일이 오래된 메모는 "
    "재확인 대상이 될 수 있다. 명시 의사인지 부수 언급인지의 해석은 메모를 다른 Evidence와 "
    "함께 읽고 판단한다."
)
EVIDENCE_INTRO = (
    "아래는 Customer Evidence Pack이다. 각 항목 앞의 [E-번호]는 Evidence ID이며, "
    "판단 근거로 사용한 항목의 ID를 출력의 supporting_evidence_ids에 기재한다.\n"
    "항목 라벨: [F]=시스템 확인 사실, [A]=산술 파생값(시스템 계산), [R]=Rule 판정값"
    "(rule_source·rule_as_of 병기), [S]=행동 신호, [CRM]=직원 작성 상담메모.\n"
    "값 표기: NULL(값 없음)·0(수량 0)·해당없음(대상 아님)은 서로 다른 의미다. "
    "여기에 없는 정보는 제공되지 않은 것이며 임의로 채우지 않는다."
)

FORBIDDEN_JUDGMENT_WORDS: List[str] = ["방치"]
LATEX_RESIDUE_RE = re.compile(r"\\rightarrow|\$[^$\n]{1,40}\$")
SCREEN_NO_RE = re.compile(r"\[\d{2}-[0-9A-Z]{2}-[0-9A-Z]{3}\]")


@dataclass
class EvidenceItem:
    eid: str
    section: str
    text: str  # bullet text without the leading "- "


@dataclass
class EvidencePack:
    case_id: str
    source_file: str
    source_sha256: str
    machine: Dict[str, Any]
    sections: List[Tuple[str, List[EvidenceItem]]]
    calculated_records: List[Dict[str, Any]]

    def all_items(self) -> List[EvidenceItem]:
        return [it for _, items in self.sections for it in items]

    def all_ids(self) -> List[str]:
        return [it.eid for it in self.all_items()]

    def as_text(self) -> str:
        return "\n".join(it.text for it in self.all_items())

    def context_text(self) -> str:
        parts = [EVIDENCE_INTRO]
        for title, items in self.sections:
            parts.append(f"### {title}")
            if title.startswith("Digital"):
                parts.append(SIGNAL_BOUNDARY_NOTE)
            if title.startswith("Customer Interaction"):
                parts.append(CRM_BOUNDARY_NOTE)
            if not items:
                parts.append("- (이 섹션에 제공된 항목 없음)")
            for it in items:
                parts.append(f"- [{it.eid}] {it.text}")
        return "\n".join(parts)


_MACHINE_FENCE_RE = re.compile(r"```json[^\n]*\n(.*?)```", re.S)


def _to_date(value: Any) -> _dt.date:
    return _dt.date.fromisoformat(str(value))


def build_calculated_facts(machine: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Deterministic preprocessing (EVIDENCE_PACK_SPEC §4).

    Arithmetic Derived: elapsed days, D-n, passthrough deltas.
    Rule-derived Fact: pension-open eligibility (R1), DO expected application
    base date (R2), tax-credit remaining passthrough (R3) — each with
    rule_source / rule_as_of. Never emits semantic labels ("방치" 류); R2
    states the expected base date and that actual application status needs
    separate confirmation (결정 2-4).
    """
    recs: List[Dict[str, Any]] = []
    base = machine.get("base_date")
    base_d = _to_date(base) if base else None

    def add(kind: str, label: str, text: str) -> None:
        recs.append({"kind": kind, "label": label, "text": text})

    for dep in machine.get("deposits", []) or []:
        if base_d and dep.get("date"):
            days = (base_d - _to_date(dep["date"])).days
            amt = f"{int(dep['amount']):,}원 " if dep.get("amount") is not None else ""
            reason = f"(사유: {dep['reason']}) " if dep.get("reason") else ""
            add("arithmetic", "A",
                f"입금 경과일: {dep['date']} {amt}{reason}→ 기준일까지 {days}일 경과")
    for mat in machine.get("maturities", []) or []:
        if base_d and mat.get("date"):
            dn = (_to_date(mat["date"]) - base_d).days
            amt = f"{int(mat['amount']):,}원 " if mat.get("amount") is not None else ""
            prod = f"{mat['product']} " if mat.get("product") else ""
            when = f"D-{dn}" if dn >= 0 else f"만기 경과 {-dn}일"
            add("arithmetic", "A", f"만기 시한: {prod}{amt}만기 {mat['date']} → {when}")
    if machine.get("one_month_cash_delta") is not None:
        add("arithmetic", "A",
            f"최근 1개월 고유계정대 증감액: {int(machine['one_month_cash_delta']):+,}원")

    if base_d and machine.get("age") is not None and machine.get("join_date"):
        years = (base_d - _to_date(machine["join_date"])).days / 365.25
        has_ret = bool(machine.get("retirement_benefit_included"))
        eligible = int(machine["age"]) >= 55 and (years >= 5 or has_ret)
        add("rule", "R",
            "연금개시요건 충족 여부: {} (만 {}세, 가입 {:.1f}년, 퇴직급여 포함 {}) "
            "| rule_source=만55세 이상 + 가입 5년 이상(퇴직급여 포함 시 55세만) — 행내 공식 기준 "
            "| rule_as_of={}".format("충족" if eligible else "미충족",
                                     machine["age"], years, "Y" if has_ret else "N", base))
    do_trig = machine.get("do_trigger") or {}
    if base_d and machine.get("do_registered") and do_trig.get("date"):
        weeks = 2 if do_trig.get("type") == "최초입금" else 6
        expected = _to_date(do_trig["date"]) + _dt.timedelta(weeks=weeks)
        delta = (base_d - expected).days
        if delta > 0:
            status = f", 기준일 대비 {delta}일 경과 — 실제 적용 여부는 별도 확인 필요(적용 여부 원천값 미보유)"
        elif delta < 0:
            status = f", 도래까지 {-delta}일"
        else:
            status = ", 기준일 당일 도래"
        add("rule", "R",
            f"디폴트옵션 적용 예상 기준일: {expected.isoformat()} "
            f"({do_trig.get('type', '만기')} {do_trig['date']} + {weeks}주){status} "
            f"| rule_source=최초입금 2주 / 만기 4+2주 — 행내 기준 | rule_as_of={base}")
    # HD-8 6-2: 세 한도 개념 분리 — 서로 다른 값이며 상호 추정 금지.
    # (irp_personal_contribution_ytd 는 raw Fact 이므로 input bullet 로 제공한다)
    tax_credit = machine.get("pension_tax_credit_limit_remaining",
                             machine.get("tax_credit_remaining"))
    if tax_credit is not None:
        add("rule", "R",
            f"연금계좌 세액공제 잔여한도(연금저축·퇴직연금 합산): {int(tax_credit):,}원 "
            f"— 추가 납입 가능 금액과 다른 개념 "
            f"| rule_source=시스템 산출값 수신(전처리 자체 계산 아님) | rule_as_of={base}")
    if machine.get("pension_account_contribution_limit_remaining") is not None:
        add("rule", "R",
            f"연금계좌 연 납입한도 잔여(관계 법령상 합산 대상 연금계좌 기준): "
            f"{int(machine['pension_account_contribution_limit_remaining']):,}원 "
            f"— 이 IRP 하나의 독립 한도가 아니며, 세액공제 잔여한도와 다른 개념 "
            f"| rule_source=시스템 산출값 수신(전처리 자체 계산 아님) | rule_as_of={base}")
    return recs


def load_evidence_pack(case_id: str) -> EvidencePack:
    """Parse cases/<CASE>/input_v2.md into an 8-section Evidence Pack.

    Format: one fenced ```json block (machine-readable raw values used only by
    build_calculated_facts) + `## <n>. <section title>` headings whose bullet
    lines are the evidence items. Evidence IDs (E001…) are assigned in file
    order; calculated facts are appended as a synthetic section and share the
    same ID space so the model can cite them.
    """
    path = REPO_ROOT / "cases" / case_id / "input_v2.md"
    if not path.is_file():
        raise FileNotFoundError(f"input_v2 not found: {path}")
    text = path.read_text(encoding="utf-8")
    m = _MACHINE_FENCE_RE.search(text)
    machine: Dict[str, Any] = {}
    if m:
        machine = json.loads(m.group(1))
        text = _MACHINE_FENCE_RE.sub("", text)

    sections: List[Tuple[str, List[EvidenceItem]]] = []
    counter = 0
    for block in re.split(r"^(?=## )", text, flags=re.M):
        head = re.match(r"^## \d+\.\s*(.+?)\s*$", block, re.M)
        if not head:
            continue
        title = head.group(1)
        items: List[EvidenceItem] = []
        for ln in block.splitlines():
            bm = re.match(r"^\s*- (.+)$", ln)
            if bm:
                counter += 1
                items.append(EvidenceItem(f"E{counter:03d}", title, bm.group(1).strip()))
        sections.append((title, items))
    if counter == 0:
        raise ValueError("input_v2.md contains no bullet evidence items")
    known = [t for t, _ in sections]
    missing_sections = [t for t in EVIDENCE_SECTION_TITLES if t not in known]
    if missing_sections:
        raise ValueError(f"input_v2.md missing sections: {missing_sections}")

    calc = build_calculated_facts(machine)
    calc_items: List[EvidenceItem] = []
    for rec in calc:
        counter += 1
        rec["eid"] = f"E{counter:03d}"
        calc_items.append(EvidenceItem(rec["eid"], CALCULATED_SECTION_TITLE,
                                       f"[{rec['label']}] {rec['text']}"))
    if calc_items:
        sections.append((CALCULATED_SECTION_TITLE, calc_items))
    return EvidencePack(case_id, str(path.relative_to(REPO_ROOT)), _sha256(path),
                        machine, sections, calc)


# ---------------------------------------------------------------------------
# REV-002 prompt
# ---------------------------------------------------------------------------
SYSTEM_ROLE_V2 = """당신은 은행 직원의 개인형IRP 사후관리 판단을 지원하는 의사결정 지원 Agent다.

역할 원칙:
1. 확인된 사실(제공된 Evidence)과 그로부터 추론한 가능성을 분리해서 다룬다. 추론을 사실처럼 쓰지 않는다.
2. 제공된 Evidence로 확인되지 않은 고객의 의도·사정·계획은 임의로 채우지 않고, 추가 확인이 필요한 사항으로 명시한다. 확인 사항은 Evidence와 판단 결과로부터 스스로 도출한다.
3. 업무적 판단은 제공된 Knowledge에 근거한다. Knowledge와 Evidence에 없는 업무 사실, 제도 규칙, 수치를 생성하지 않는다.
4. 제공된 Constraint를 위반하는 Solution 방향을 생성하지 않는다.
5. 상품 연결은 다음 순서를 따른다: 먼저 운용 방향/상품 유형을 판단하고, 특정 상품이 필요한 경우에만 제공된 Candidate Pool 안의 상품을 후보로 제시한다. Pool에 없는 상품명을 임의로 생성·추천하지 않는다. 고객 의사·기간·자금성격 등 핵심 조건이 미확인이면 반드시 조건부로 제시하고, 최종 선택은 고객에게 있음을 전제한다.
6. 판단의 근거로 사용한 Evidence ID와 Knowledge ID를 밝힌다.
7. 최종 결과는 직원이 고객관리를 수행하기 위한 Recommendation Brief이며, 고객에게 직접 전달하는 문서가 아니다.
8. Action보다 Management Judgment가 먼저다. 이 고객에게 지금 어떤 종류의 관리판단이 맞는지(개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가)를 Evidence를 근거로 먼저 확정한 뒤, 그 판단에 맞는 다음 행동과 Brief를 만든다.
9. 어느 방향도 기본값이 아니다. 변경·유지·확인·정보안내·고객선택존중·실행불가 중 근거가 요구하는 것을 고른다. "관리 필요"는 "변경 필요"와 같은 말이 아니며, 투자성향은 허용 상한이지 그 수준까지 운용하라는 요구가 아니다.
10. Knowledge는 Case Relevance와 Usage Boundary까지 사용한다. 시한·조건·절차·화면 같은 세부를 판단과 Brief에 실제로 반영하고, Usage Boundary가 금지한 단정은 하지 않는다.
11. 상담메모(CRM)는 직원 작성 기록이다. 현재 고객 의사의 확정 근거로 승격하지 않으며, 작성일이 오래되었으면 재확인을 계획에 넣는다.
12. 행동 신호(조회·클릭 등)는 관심 가능성까지만 해석한다. 신호를 고객 의사로 승격하지 않는다.
13. 수익률 비교(고객 보유수익률 vs 상품 자체 수익률 등)는 상황 이해와 상담 설명의 근거로 쓸 수 있으나, 수익률 비교 단독으로 교체·리밸런싱·위험 확대·특정 상품 가입의 필요성을 확정하지 않는다. 보유기간·자금성격·투자성향·고객 의사와 함께 해석한다.
14. 관리 필요성은 고객의 Evidence에서 출발해야 한다. 은행의 영업 목적을 관리 필요성의 근거로 만들지 않는다.
15. 조건 분기는 실제 Management Decision을 바꾸는 미확인 변수가 있을 때만 만든다. Evidence만으로 방향이 충분히 결정되면 단일 추천 방향을 제시한다. 존재하는 분기를 누락하지도, 불필요한 분기를 만들어내지도 않는다.
16. 구조화 판단에서 '미확인', '추론', '조건부', '고객 진술/CRM 기반', '확인 필요' 상태로 다룬 정보는 Employee Brief 산문에서도 같은 상태를 유지한다. 다음 승격을 금지한다: 고객·CRM 진술 → 시스템 확인 사실("무주택 기록" → "무주택자" 금지), 추론 → 확정 사실, 조건 충족 가능성 → 조건 충족 확정, 확인 필요 수치 → 확정 수치 판정("기준 초과 여부 확인 필요" → "초과" 금지), 예정·예상 → 실제 발생·적용 완료("적용 예상 시점 경과·적용 여부 미확인" → "적용 예정/미적용 상태" 금지). 이 원칙은 CRM에 한정되지 않고 행동 신호·수익률·계좌 밖 정보 등 모든 Evidence에 적용된다."""

OUTPUT_INSTRUCTION_V2 = """다음 JSON 객체 하나만 출력한다. JSON 앞뒤에 다른 텍스트, 설명, 코드펜스를 붙이지 않는다. 모든 문자열 값은 한국어로 쓴다. 화살표가 필요하면 일반 문자 "→"만 쓴다(LaTeX 표기 금지). 키 순서대로 생각한다: 상황 → 사실/미확인 → 관리판단 → 다음 행동 → Employee Brief.

{
  "current_situation": "Evidence로부터 해석한 현재 상황 (사실과 추론을 구분해서 서술)",
  "known_facts_used": ["판단에 사용한 확인된 사실을 Evidence 항목 그대로 나열"],
  "unknowns_or_confirmations": ["판단에 중요하지만 확인되지 않아 추가 확인이 필요한 사항 (스스로 도출)"],
  "management_judgment": {
    "judgment": "다음 중 하나 이상을 '/'로 구분해 기재: 개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가",
    "reasoning": "왜 그 판단인지 — Evidence를 근거로",
    "must_confirm_before_action": ["Action 확정 전 먼저 확인할 것 (없으면 빈 배열)"],
    "supporting_evidence_ids": ["이 판단의 근거 Evidence ID — E로 시작하는 Evidence ID만 기재한다 (예: E003). K-로 시작하는 Knowledge ID를 여기에 넣지 않는다"],
    "supporting_knowledge_ids": ["이 판단의 근거 Knowledge ID만 기재 (예: K-001; 없으면 빈 배열)"]
  },
  "next_actions": [
    {
      "action": "판단에 맞는 다음 행동 (변경·유지·확인·정보안내·절차·연계 모두 가능)",
      "kind": "변경 / 유지 / 확인 / 정보안내 / 절차 / 연계 중 하나",
      "condition": "이 행동이 유효하기 위한 전제 조건 또는 확인 사항 (무조건 실행 가능하면 빈 문자열)",
      "risk_level": "운용 방향(변경 또는 유지)이면 그 방향의 투자성향 위험수준(5단계 중 하나), 아니면 '해당없음'",
      "supporting_evidence_ids": ["근거 Evidence ID"]
    }
  ],
  "knowledge_ids_used": ["근거로 사용한 Knowledge ID (예: K-001)"],
  "employee_brief": {
    "s1_customer_situation": "S1 고객 상황 — 핵심만 간결히. 확인된 사실과 추론을 구분하는 절제된 서술. 미확인 사항을 단정하지 않는다.",
    "s2_management_point": {
      "point": "S2 핵심 관리 포인트 — 지금 이 고객에게 무엇을 관리하는 것이 중요한가에 대한 한 문장 커밋",
      "rationale": "그 근거 한두 문장 (고객 Evidence에서 출발)",
      "confirm_first": [{"item": "먼저 확인할 사항", "who": "고객 또는 직원"}]
    },
    "s3_direction": {
      "directions": [{"condition": "이 방향의 전제 조건 (Evidence만으로 결정 가능하면 빈 문자열)", "content": "추천 운용 방향 — 유형 수준, 필요 시 Candidate Pool 내 상품", "risk_level": "5단계 중 하나 또는 '해당없음'"}],
      "not_applicable": null
    },
    "s4_consult_points": {
      "sequence": ["1) 상담 접근 순서를 번호 목록으로"],
      "scripts": ["직원이 고객에게 그대로 쓸 수 있는 설명 문구 1개 이상 (쉬운 용어, 단정·압박 금지)"]
    },
    "s5_tips": [{"content": "관련 화면([번호] 화면명 용도), 업무 절차, 유의사항 등 실무 재료", "source": "직원이 실제로 찾아갈 수 있는 출처 — 우선순위: 자료명 > SRC-ID > 화면번호+화면명 > 공식 가이드/부서명. K-로 시작하는 내부 Knowledge ID는 여기에 쓰지 않는다. 제공된 재료에 없는 팁을 만들지 않는다", "as_of": "시점 의존 수치인 경우 기준일, 아니면 빈 문자열"}]
  }
}

employee_brief 규칙:
- s3_direction은 상품 권유가 부적절한 상담(중도인출 지원, 실행 불가 안내, 이탈 대응 등)이면 directions를 빈 배열로 두고 not_applicable에 {"type": "...", "reason": "..."}를 기재한다. 그 외에는 not_applicable을 null로 둔다.
- s5_tips에 쓸 재료가 제공되지 않았으면 [{"content": "관련 행내 자료 없음 — 공식 화면/담당 부서 확인 필요", "source": "", "as_of": ""}]로 쓴다.
- 불확실성 보존: 구조화 판단(unknowns, must_confirm, condition)에 있는 미확인·추론·조건부·고객 진술 기반 정보는 s1~s5 산문에서도 같은 상태로 쓴다. 확정 사실로 바꿔 쓰지 않는다(역할 원칙 16)."""


def build_prompt_v2(pack: EvidencePack, constraint: ConstraintContext,
                    knowledge: List[KnowledgeItem]) -> Prompt:
    knowledge_text = (
        "각 Knowledge에는 근거 유형(Basis)이 표시되어 있다. Case Relevance는 이 Knowledge가 이 고객에게 왜 지금 "
        "중요한지, Usage Boundary는 이 Knowledge만으로 단정하면 안 되는 것이다. 관련도가 높은 Knowledge의 "
        "시한·조건·절차·화면 세부를 실제로 사용하고, Usage Boundary를 넘는 결론을 만들지 않는다.\n\n"
        + "\n\n".join(k.as_text() for k in knowledge)
    )
    pool = (pack.machine.get("candidate_pool") or [])
    if pool:
        knowledge_text += (
            "\n\n### Candidate Pool (이 Case에서 특정 상품 수준 연결이 허용되는 후보 — 이 밖의 상품명 생성 금지)\n"
            + "\n".join(f"- {p}" for p in pool)
        )
    return Prompt(
        system_role=SYSTEM_ROLE_V2,
        customer_context=pack.context_text(),
        constraint_context=constraint.as_text(),
        knowledge_context=knowledge_text,
        output_instruction=OUTPUT_INSTRUCTION_V2,
        knowledge_ids=[k.kid for k in knowledge],
    )


# ---------------------------------------------------------------------------
# REV-002 schema check + deterministic validators (semantic checks stay with
# the Evaluator — EMPLOYEE_BRIEF_SPEC §3)
# ---------------------------------------------------------------------------
def check_schema_v2(obj: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing key: {k}")
    mj = obj.get("management_judgment")
    if isinstance(mj, dict):
        for k in ("judgment", "reasoning"):
            if not str(mj.get(k, "")).strip():
                errs.append(f"management_judgment.{k} is empty")
        if isinstance(mj.get("judgment"), str) and not detect_judgment_types(obj):
            errs.append("management_judgment.judgment names none of the judgment types")
        if not isinstance(mj.get("supporting_evidence_ids", []), list):
            errs.append("management_judgment.supporting_evidence_ids must be a list")
        if not isinstance(mj.get("supporting_knowledge_ids", []), list):
            errs.append("management_judgment.supporting_knowledge_ids must be a list")
    elif mj is not None:
        errs.append("management_judgment must be an object")
    na = obj.get("next_actions")
    if isinstance(na, list):
        for i, c in enumerate(na):
            if not isinstance(c, dict):
                errs.append(f"next_actions[{i}] must be an object")
                continue
            for k in ("action", "kind", "risk_level"):
                if not str(c.get(k, "")).strip():
                    errs.append(f"next_actions[{i}].{k} is empty")
    elif na is not None:
        errs.append("next_actions must be a list")

    eb = obj.get("employee_brief")
    if not isinstance(eb, dict):
        if eb is not None:
            errs.append("employee_brief must be an object (5-section)")
        return errs
    if not str(eb.get("s1_customer_situation", "")).strip():
        errs.append("employee_brief.s1_customer_situation is empty")
    s2 = eb.get("s2_management_point")
    if not isinstance(s2, dict) or not str(s2.get("point", "")).strip():
        errs.append("employee_brief.s2_management_point.point is empty")
    elif not isinstance(s2.get("confirm_first", []), list):
        errs.append("employee_brief.s2_management_point.confirm_first must be a list")
    s3 = eb.get("s3_direction")
    if not isinstance(s3, dict):
        errs.append("employee_brief.s3_direction must be an object")
    else:
        dirs = s3.get("directions")
        n_a = s3.get("not_applicable")
        if not isinstance(dirs, list):
            errs.append("employee_brief.s3_direction.directions must be a list")
        elif not dirs and not isinstance(n_a, dict):
            errs.append("employee_brief.s3_direction: directions empty and not_applicable missing")
        else:
            for i, d in enumerate(dirs):
                if not isinstance(d, dict) or not str(d.get("content", "")).strip():
                    errs.append(f"employee_brief.s3_direction.directions[{i}].content is empty")
                elif "condition" not in d:
                    errs.append(f"employee_brief.s3_direction.directions[{i}].condition field missing")
    s4 = eb.get("s4_consult_points")
    if not isinstance(s4, dict) or not isinstance(s4.get("sequence"), list) or not s4.get("sequence"):
        errs.append("employee_brief.s4_consult_points.sequence must be a non-empty list")
    elif not isinstance(s4.get("scripts"), list) or not any(str(s).strip() for s in s4.get("scripts", [])):
        errs.append("employee_brief.s4_consult_points.scripts must contain at least one script")
    s5 = eb.get("s5_tips")
    if not isinstance(s5, list) or not s5:
        errs.append("employee_brief.s5_tips must be a non-empty list")
    else:
        for i, t in enumerate(s5):
            if not isinstance(t, dict) or not str(t.get("content", "")).strip():
                errs.append(f"employee_brief.s5_tips[{i}].content is empty")
    return errs


def _output_text(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _brief_text(obj: Dict[str, Any]) -> str:
    return json.dumps(obj.get("employee_brief", {}), ensure_ascii=False)


def validate_forbidden_words(obj: Dict[str, Any]) -> Dict[str, Any]:
    """FAIL if a forbidden judgment word appears anywhere in the output.

    Word list per EMPLOYEE_BRIEF_SPEC §3.1 (실제 발생 사례가 있는 것만).
    Semantic variants ("Unknown의 사실 승격" 일반)은 Evaluator 몫.
    """
    findings = []
    text = _output_text(obj)
    for w in FORBIDDEN_JUDGMENT_WORDS:
        if w in text:
            for loc in ("current_situation", "employee_brief"):
                loc_text = str(obj.get(loc, "")) if loc != "employee_brief" else _brief_text(obj)
                if w in loc_text:
                    findings.append({"word": w, "where": loc, "verdict": "FAIL"})
            if not any(f["word"] == w for f in findings):
                findings.append({"word": w, "where": "other", "verdict": "FAIL"})
    return {"check": "forbidden_words", "findings": findings,
            "overall": "FAIL" if findings else "PASS"}


def validate_latex_residue(obj: Dict[str, Any]) -> Dict[str, Any]:
    hits = LATEX_RESIDUE_RE.findall(_output_text(obj))
    return {"check": "latex_residue", "findings": hits[:10],
            "overall": "REVIEW" if hits else "PASS"}


def validate_evidence_ids(obj: Dict[str, Any], valid_ids: List[str]) -> Dict[str, Any]:
    """Deterministic provenance check (결정 3-4·3-5).

    FAIL   : a cited evidence id does not exist in the Evidence Pack.
    REVIEW : management_judgment cites no evidence ids at all (근거 없는 관리
             포인트 후보 — 논리 정합은 Evaluator가 본다).
    """
    valid = set(valid_ids)
    findings = []
    overall = "PASS"
    mj = obj.get("management_judgment") or {}
    mj_ids = mj.get("supporting_evidence_ids") if isinstance(mj, dict) else None
    cited: List[Tuple[str, List[str]]] = [("management_judgment", mj_ids or [])]
    for i, c in enumerate(obj.get("next_actions") or []):
        if isinstance(c, dict):
            cited.append((f"next_actions[{i}]", c.get("supporting_evidence_ids") or []))
    if not mj_ids:
        findings.append({"where": "management_judgment", "issue": "no supporting_evidence_ids",
                         "verdict": "REVIEW"})
        overall = "REVIEW"
    for where, ids in cited:
        for eid in ids:
            if eid not in valid:
                findings.append({"where": where, "issue": f"unknown evidence id {eid}",
                                 "verdict": "FAIL"})
                overall = "FAIL"
    return {"check": "evidence_ids", "findings": findings, "overall": overall}


def validate_screen_survival(input_text: str, knowledge_text: str,
                             obj: Dict[str, Any]) -> Dict[str, Any]:
    """REVIEW if a screen number present in input/knowledge appears nowhere in
    the output (GC-08·GC-16 탈락 사례 대책; GC-11이 유지 준거)."""
    provided = set(SCREEN_NO_RE.findall(input_text)) | set(SCREEN_NO_RE.findall(knowledge_text))
    out = set(SCREEN_NO_RE.findall(_output_text(obj)))
    missing = sorted(provided - out)
    return {"check": "screen_survival", "provided": sorted(provided),
            "missing_from_output": missing,
            "overall": "REVIEW" if missing else "PASS"}


_KID_RE = re.compile(r"\bK-\d{3}\b")


def validate_s5_sources(obj: Dict[str, Any]) -> Dict[str, Any]:
    """REVIEW if an internal K-ID appears as a staff-facing S5 source (F-012,
    HD-8 (a)-3 Output Contract). K-IDs live only in knowledge provenance
    fields; S5 sources must be staff-traceable (자료명/SRC-ID/화면번호/부서)."""
    eb = obj.get("employee_brief") or {}
    findings = []
    for i, t in enumerate(eb.get("s5_tips") or [] if isinstance(eb, dict) else []):
        if isinstance(t, dict):
            hits = _KID_RE.findall(str(t.get("source", "")))
            if hits:
                findings.append({"index": i, "kids": hits, "verdict": "REVIEW"})
    return {"check": "s5_sources", "findings": findings,
            "overall": "REVIEW" if findings else "PASS"}


def validate_candidate_pool(machine: Dict[str, Any], obj: Dict[str, Any]) -> Dict[str, Any]:
    """FAIL if a product known NOT to be in the approved pool appears in S3.

    Only names listed in machine["known_products_not_in_pool"] are checked —
    a deterministic subset. "임의 상품명 생성" 일반 검출은 Evaluator 몫.
    """
    excluded = machine.get("known_products_not_in_pool") or []
    pool = machine.get("candidate_pool") or []
    eb = obj.get("employee_brief") or {}
    s3_text = json.dumps(eb.get("s3_direction", {}) if isinstance(eb, dict) else {},
                         ensure_ascii=False)
    findings = [{"product": name, "where": "s3_direction", "verdict": "FAIL"}
                for name in excluded if name in s3_text]
    used_pool = [name for name in pool if name in s3_text]
    return {"check": "candidate_pool", "pool": pool, "pool_used_in_s3": used_pool,
            "findings": findings, "overall": "FAIL" if findings else "PASS"}


# ---------------------------------------------------------------------------
# REV-002 orchestration
# ---------------------------------------------------------------------------
def prepare_v2(case_id: str):
    pack = load_evidence_pack(case_id)
    constraint = build_constraint_context(pack)  # reads 투자성향 from evidence text
    knowledge, kp_path, kp_sha = load_knowledge_items(case_id)
    prompt = build_prompt_v2(pack, constraint, knowledge)
    meta = {"knowledge_pack": kp_path, "knowledge_pack_sha256": kp_sha}
    return pack, constraint, knowledge, prompt, meta


def run_case_rev002(case_id: str, dry_run: bool = False) -> Dict[str, Any]:
    started = _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    record: Dict[str, Any] = {
        "case_id": case_id,
        "runtime_revision": RUNTIME_REVISION_V2,
        "started_at": started,
        "model": MODEL_ID,
        "endpoint": ENDPOINT,
        "generation_config": None,
        "git_head": _git_head(),
        "status": None,
        "error": "",
    }
    try:
        pack, constraint, knowledge, prompt, meta = prepare_v2(case_id)
    except Exception as e:
        record.update(status=CONFIG_ERROR, error=f"{type(e).__name__}: {e}")
        return record

    record.update(
        {
            "frozen_input_v2": {"file": pack.source_file, "sha256": pack.source_sha256},
            "frozen_knowledge_pack": meta,
            "evidence_sections": {t: [it.eid for it in items] for t, items in pack.sections},
            "machine_block": pack.machine,
            "calculated_facts": pack.calculated_records,
            "constraint_context": {
                "constraint_id": constraint.constraint_id,
                "investment_profile": constraint.investment_profile,
                "allowed_levels": constraint.allowed_levels,
                "forbidden_levels": constraint.forbidden_levels,
                "basis": constraint.basis,
            },
            "knowledge_ids_used": prompt.knowledge_ids,
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

    schema_errs = check_schema_v2(obj)
    record["schema_errors"] = schema_errs
    if schema_errs:
        record.update(status=SCHEMA_ERROR, error="; ".join(schema_errs))
        record["validation"] = validate_c1(obj, constraint)
        return record

    record["validation"] = validate_c1(obj, constraint)
    record["validation_c3"] = validate_c3_default_option(obj, constraint)
    record["validation_c2"] = validate_c2_fund_grade(obj, constraint)
    record["validation_forbidden_words"] = validate_forbidden_words(obj)
    record["validation_latex"] = validate_latex_residue(obj)
    record["validation_evidence_ids"] = validate_evidence_ids(obj, pack.all_ids())
    record["validation_screen_survival"] = validate_screen_survival(
        prompt.customer_context, prompt.knowledge_context, obj)
    record["validation_s5_sources"] = validate_s5_sources(obj)
    record["validation_candidate_pool"] = validate_candidate_pool(pack.machine, obj)
    record["judgment_types_detected"] = detect_judgment_types(obj)
    record["employee_brief"] = obj.get("employee_brief", {})

    hard_fail_keys = ("validation", "validation_c3", "validation_c2",
                      "validation_forbidden_words", "validation_evidence_ids",
                      "validation_candidate_pool")
    errs = []
    if record["validation"]["overall"] == "FAIL":
        errs.append("C1 violated by a next action")
    if record["validation_c3"]["overall"] == "FAIL":
        errs.append("C3 ineligible default-option portfolio proposed")
    if record["validation_c2"]["overall"] == "FAIL":
        errs.append("C2 ineligible fund risk grade proposed")
    if record["validation_forbidden_words"]["overall"] == "FAIL":
        errs.append("forbidden judgment word in output")
    if record["validation_evidence_ids"]["overall"] == "FAIL":
        errs.append("unknown evidence id cited")
    if record["validation_candidate_pool"]["overall"] == "FAIL":
        errs.append("product outside candidate pool proposed in S3")
    failed = any(record[k]["overall"] == "FAIL" for k in hard_fail_keys)
    record.update(status=(VALIDATION_ERROR if failed else SUCCESS), error="; ".join(errs))
    return record


# ===========================================================================
# 10. v3 — Pre-P2 Architecture Refinement (Canonical 9-Block + Decision &
#     Action Brief). Specs: design/CANONICAL_CONTRACTS.md,
#     design/INTERPRETATION_DESIGN.md, design/EMPLOYEE_BRIEF_SPEC.md v2.
#     Path taken iff cases/<CASE>/canonical.json exists (dispatch below).
# ===========================================================================
import canonical as _cx

RUNTIME_REVISION_V3 = "PRE-P2-REFINEMENT"

SYSTEM_ROLE_V3 = """당신은 은행 직원의 개인형IRP 사후관리 판단을 지원하는 의사결정 지원 Agent다. 최종 산출물은 직원이 그대로 사용할 수 있는 Decision & Action Brief다.

[Evidence 읽기]
1. 입력은 9-Block Customer Evidence Pack이다. ①~⑧은 시스템 관찰 Evidence, ⑨는 사람이 작성한 보조 맥락(CRM 메모)이다. 고객 상태의 재구성은 ①~⑧을 기본으로 하고, ⑨는 참고로만 결합한다.
2. 현재 상태(②)와 최근 변화(③④)를 항상 함께 읽는다 — 상태는 결과이고 변화는 형성 과정이다. 변화가 상태를 설명하면 그 연결을 명시하고, 최근 변화가 없으면 "최근 관련 변화가 관찰되지 않음"까지만 서술한다.
3. 잔액-Flow의 "금액 일치"는 산술 사실로 사용한다. 동일 자금으로 보는 것은 추론으로 표기하고, 그 자금의 목적은 확인 대상이다. 예정 Event(⑧)가 뒷받침할 때만 사실 수준으로 다룬다.
4. 행동 신호(⑥)는 시간순 서사(무엇을 탐색해 왔고 실행에 도달했는가)로 상황 해석과 상담 접점에 쓴다. 단 Sequence가 아무리 강해도 산출 가능한 최대 해석은 "관심/탐색 관찰"이며, 고객 의사로 승격하지 않는다. 관리 필요성의 근거는 행동 신호가 아니라 시한·제도·자산 상태 등 다른 Evidence에 있어야 한다.
5. CRM(⑨)은 그 시점의 기록이다. 작성 경과일과 이후의 시스템 Event·행동 신호를 시간순으로 함께 읽고, 이후 Evidence가 기록과 다른 방향을 시사하면 어느 쪽도 채택하지 않고 재확인을 결론으로 삼는다.
6. 모든 해석은 Fact / Signal / Inference(추론 표기 의무) / Unknown 중 하나의 상태를 가지며, 그 상태는 Brief 산문까지 보존된다. 새 Evidence 없이 상태를 올리지 않는다: 고객·CRM 진술→시스템 확인 사실, 추론→확정, 조건 가능성→충족 확정, 확인 필요 수치→확정 판정, 예정·예상→실제 발생의 승격을 금지한다. 자금의 의미·목적·관리상태도 Evidence 없이 확정하지 않는다 — "운용 대기 중"·"미운용 자금" 류의 의미 부여 대신 "입금 이후 추가 매매·운용지시가 확인되지 않았다"처럼 관찰 가능한 상태로 서술한다. 현금 보유·최근 입금·운용지시 미확인 등은 관찰 가능한 상태일 뿐이다 — 별도 Evidence 없이 이를 "방치"·"관리 소홀"·"수익률 저하 우려" 등으로 자동 승격하지 않으며, 이런 승격을 관리 판단(Why-now·reasoning)의 근거로도 쓰지 않는다.

[판단]
7. Action보다 Management Judgment가 먼저다. 이 고객에게 지금 맞는 관리판단(개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가)을 Evidence로 먼저 확정한다. 어느 방향도 기본값이 아니며, "관리 필요"는 "변경 필요"와 같은 말이 아니다.
8. Why-now는 반드시 실제 Event·변화·시한(③④⑧)에서 나와야 한다. 복수 이슈가 있으면 시한 임박도 → 고객 이익 영향 → 접점 자연스러움 순으로 주 포인트를 정하되, 나머지를 버리지 않고 부 포인트나 후속관리로 남긴다. 은행의 영업 목적을 관리 필요성의 근거로 만들지 않는다.
9. 확인 사항은 Management Direction을 실제로 바꾸는 미확인 변수만 도출한다. 시스템/단말/공식자료로 닫을 수 있으면 '상담 전 확인', 고객만 답할 수 있으면 '고객과 확인'이다. 이미 Evidence에 있는 사실을 고객에게 다시 묻지 않는다.
10. 조건 분기는 실제 판단을 바꾸는 미확인 변수가 있을 때만 만든다. Evidence만으로 충분하면 단일 방향을 제시한다.
11. 업무 판단은 제공된 Knowledge에 근거하고, Knowledge와 Evidence에 없는 업무 사실·제도 규칙·수치를 생성하지 않는다. 제공된 Constraint를 위반하는 방향을 만들지 않는다. 투자성향은 허용 가능한 최대 위험의 상한이다.

[전달 — Brief]
12. 관리 방향은 유지·신규자금 운용·만기 재운용·조정·운용체계 변경·세제 활용·연금수령 관리·중도인출 지원·계약이전/부분이전 지원·고객 의사결정 지원·불가 시 대안 안내를 모두 포함한다 — 상품 추천이 없는 상담도 정상적인 방향이다. 사고 순서는 관리 방향 → Solution 유형 → 실제 상품 후보다. 상품부터 고르지 않는다.
13. 특정 상품은 제공된 Candidate Pool 안에서만 product_id로 참조한다. Pool 밖 상품명을 만들지 않는다. 판매 불가 상품·고객 성향을 초과하는 등급의 상품은 후보로 올리지 않는다. 추천 사유는 최근 수익률이 높다는 사실이 아니라 고객의 운용기간·자금 목적·투자성향·현재 포트폴리오·운용 경험·의사와 상품 특성의 적합성으로 작성한다. 수익률·연령 등은 이미 정해진 방향을 고객이 이해하기 쉽게 설명하는 재료로만 쓴다. 관리 방향과 추천 사유는 고객 필요·고객 이익·고객-상품 적합성으로만 정당화한다 — "이탈 방지"·"자산 유지"·"실적" 등 은행의 목적을 추천 사유로 쓰지 않는다. 고객이 이전을 고려한다는 사실은 상황 Evidence로 쓸 수 있으나, 고객이 떠나지 않게 한다는 것이 추천의 이유가 될 수는 없다.
14. 상담 화법은 지침이 아니라 완성된 문장이다 — 이 고객의 실제 금액·시점·자산구성·상품명·관리 방향이 문장 안에 들어간 Customer-specific Script를 만든다. Hot Tip 화법 Knowledge가 있으면 원문을 복사하지 말고 이 고객의 실제 데이터와 합성한다. 쉬운 용어를 쓰고("고유계정대" 대신 "운용 지시가 되지 않은 현금성 자산" 등), 단정·압박·과장하지 않는다.
15. Tip/Guide 원문과 실행 화면은 제공된 목록에서 tip_id/screen_id로만 참조한다. 원문을 재작성하거나 없는 화면번호·경로를 만들지 않는다. 제안한 Action과 직접 연결된 것만 고른다. 화면번호·메뉴 경로의 표시 위치는 S5 하나다 — S1~S4 본문에는 "[04-12-XXX]" 같은 화면번호를 쓰지 않고 "단말에서 디폴트옵션 실제 적용 여부 확인"처럼 무엇을 확인·실행할지만 쓴다(화면명을 일반명사 수준으로 자연스럽게 설명하는 것은 허용).
16. 내부 안전원칙("~로 단정할 수 없습니다", "Signal은 Intent가 아닙니다" 류의 방어문구)을 Brief에 노출하지 않는다. 원칙은 판단에서 지키고, Brief에는 그 결과를 자연스러운 문장으로 쓴다. Brief는 직원용이며 고객에게 직접 주는 문서가 아니다.
17. 판단 근거로 사용한 Evidence ID(E/D)와 Knowledge ID를 밝힌다. supporting_evidence_ids에는 Evidence ID만, Knowledge ID는 supporting_knowledge_ids/knowledge_ids_used에만 쓴다.
18. [Decision Variable / Conditionality Preservation] S2에서 '고객과 확인'으로 남긴 미확인 변수가 S3의 방향·상품 후보 또는 S4 화법을 실제로 바꾸는 경우, 확인 전에 특정 분기를 확정하지 않는다: S3는 그 변수를 조건으로 하는 조건부 추천을 유지하고, S4도 같은 조건성을 보존한다. 필요하면 화법을 "확인 질문 → 확인 결과에 맞는 설명·추천" 순서로 구성한다. (예: 은퇴시점이 미확인이면 "은퇴를 어느 시점 정도로 예상하고 계신지 먼저 여쭤봐도 될까요?" 이후 "2045년 전후라면 TDF2045 계열을 후보로 살펴볼 수 있습니다" — 확인 전 "TDF2045를 추천드립니다" 확정 금지.)
19. [S4 확실성 비인플레이션] S4 화법은 S1~S3보다 확실성(Epistemic Certainty)을 높이지 않는다. 구체적으로: (a) S2·S3에서 미확인·확인 필요·Knowledge 부재로 남긴 것을 S4에서 자연스러운 설명으로 메우지 않는다 — 원인·정의·산정 기준이 Knowledge에 없으면 설명을 만들지 말고 확인으로 연결한다. (b) S3가 분기로 나눈 방향은 S4에서도 각 분기의 화법을 유지한다 — 한 분기(특히 변경·재도전 방향)만 화법으로 만들지 않으며, 고객이 유지·거절을 택한 분기도 존중하는 화법을 가진다. (c) 현장 Tip 단독 근거·잠정(PROVISIONAL)·충돌 중인 지식은 "가장 유리합니다"·"가능합니다" 같은 확정·최적 표현으로 승격하지 않는다 — "~할 가능성이 있어, 실행 전 공식 기준·화면에서 확인이 필요합니다" 수준을 유지한다. (d) 정보가 미확인 상태이면 그 내용을 설명문으로 만들지 말고 질문 또는 확인 연결 문장으로 변환한다 — 예: 두 수익률의 산정 기준이 Knowledge에서 확인되지 않았다면 "매수 시점에 따라 수익률 차이가 발생합니다"(원인 설명 생성 — 금지)가 아니라 "두 수익률이 어떤 기준으로 산정되는지 먼저 확인해 보겠습니다"로 쓴다. "~에 따라 차이가 발생할 수 있는데" 같은 가능성 화법으로 원인을 대신 채우는 것도 같은 위반이다. (e) T3 단독 시점 규칙(예: 증빙 발급 개시일)은 "~부터 가능합니다"·"~이 세금을 줄이는 방법입니다" 같은 확정 서술·방향 확정의 근거로 쓰지 않는다 — 가능성 안내 + 공식 확인 연결까지만."""

OUTPUT_INSTRUCTION_V3 = """다음 JSON 객체 하나만 출력한다. JSON 앞뒤에 다른 텍스트·코드펜스를 붙이지 않는다. 모든 문자열은 한국어, 화살표는 "→"만 사용한다.

{
  "current_situation": "Evidence로 재구성한 현재 상황 — 상태와 최근 변화를 함께, Fact/추론 구분",
  "known_facts_used": ["판단에 사용한 확인된 사실"],
  "unknowns_or_confirmations": ["판단에 중요하지만 확인되지 않은 사항 (스스로 도출)"],
  "management_judgment": {
    "judgment": "개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가 중 하나 이상을 '/'로 구분",
    "reasoning": "왜 그 판단인지 — Why-now(어떤 Event·변화·시한 때문에 지금인지) 포함",
    "must_confirm_before_action": ["Direction을 바꾸는 미확인 변수만 (없으면 빈 배열)"],
    "supporting_evidence_ids": ["근거 Evidence ID (E/D로 시작; K- 금지)"],
    "supporting_knowledge_ids": ["근거 Knowledge ID (K-)"]
  },
  "next_actions": [
    {"action": "다음 행동", "kind": "변경 / 유지 / 확인 / 정보안내 / 절차 / 연계 중 하나",
     "condition": "전제 조건 (무조건이면 빈 문자열)",
     "risk_level": "운용 방향이면 5단계 성향 중 하나, 아니면 '해당없음'",
     "supporting_evidence_ids": ["근거 Evidence ID"]}
  ],
  "knowledge_ids_used": ["사용한 Knowledge ID"],
  "employee_brief": {
    "s1_customer_situation": "S1 — 현재 상태 + 최근 중요 변화가 함께 보이는 자연어 요약. 관리 판단에 중요한 실제 숫자·시점(금액·만기일·입금액 등)은 추상화하지 않고 그대로 쓴다. 미확인 사항을 단정하지 않는다. CRM 내용을 쓰면 기록임이 드러나게 쓴다.",
    "s2_management_point": {
      "point": "S2 — 이번 접점에서 무엇을 관리하는 것이 핵심인지 한두 문장. Why-now를 문장 안에 자연스럽게 녹인다 (별도 필드·방어문구 없이)",
      "check_before_consult": ["상담 전 확인 — 시스템/단말/공식자료로 직원이 미리 확인할 것 (필요할 때만, 없으면 빈 배열)"],
      "check_with_customer": ["고객과 확인 — 시스템으로 알 수 없는 Decision Variable만 (이미 아는 사실 재질문 금지, 없으면 빈 배열)"]
    },
    "s3_direction": {
      "directions": [{"condition": "이 방향의 전제 (Evidence만으로 결정되면 빈 문자열)",
                       "direction": "관리 방향 (유지·재운용·수령 관리·인출 지원·이전 지원·대안 안내 등 모두 정상)",
                       "solution_type": "Solution 유형 (상품 유형/절차/안내 등; 상품이 불필요하면 그 자체를 쓴다)",
                       "risk_level": "운용 방향이면 5단계 중 하나, 아니면 '해당없음'"}],
      "product_candidates": [{"product_id": "Candidate Pool의 id만 (임의 상품명 금지; 상품 제안이 불필요하면 빈 배열)",
                               "reasons": ["이 고객에게 이 상품을 후보로 보는 이유 — 운용기간·자금 목적·성향·포트폴리오·경험·의사와 상품 특성의 적합성으로"]}]
    },
    "s4_consult_script": {
      "scripts": ["직원이 고객에게 그대로 쓸 완성형 화법 1개 이상 — 이 고객의 실제 금액·시점·구성·상품이 문장 안에 들어가야 한다. 확실성은 S1~S3 수준을 넘지 않는다: 미확인 사항은 확인 질문으로, Knowledge에 없는 원인·기준은 설명하지 않고 확인 연결로"],
      "conditional_scripts": [{"if": "고객 반응 (예: 원금손실 우려 시)", "script": "후속 화법 — S3의 분기가 여럿이면 각 분기(유지·거절 포함)의 화법을 만든다"}]
    },
    "s5_tips_and_screens": {
      "tips": [{"tip_id": "제공된 Hot Tip/Guide의 id만", "why_relevant": "이 Case에 왜 도움이 되는지 한 줄"}],
      "screens": [{"screen_id": "제공된 화면의 id만 — S3 Action과 직접 연결된 것만", "purpose_here": "이 Case에서 이 화면을 쓰는 목적"}]
    }
  }
}

규칙: s5_tips_and_screens.tips의 tip_id에는 제공된 Tip 목록의 id만 쓸 수 있다 — Knowledge ID(K-/OK-/KG-)를 tip_id에 넣지 않는다. Tip이 제공되지 않았다면 tips를 빈 배열로 두고 tip_id를 생성하지 않는다. s3_direction.directions는 비우지 않는다 — 상품 권유가 부적절한 상담(중도인출·실행 불가·이탈 대응)도 해당 지원/안내가 곧 방향이다. product_candidates·tips·screens·conditional_scripts는 해당 재료가 없거나 불필요하면 빈 배열. conditional_scripts를 모든 경우에 만들 필요는 없다. check_with_customer의 미확인 변수가 상품·방향 선택을 바꾸면, 그 변수에 걸린 추천은 directions.condition과 S4의 조건성(확인 질문 선행 또는 conditional_scripts)으로 보존한다 — 확인 전 확정 화법 금지. employee_brief의 s1~s4 문자열에는 화면번호("[04-12-XXX]" 류)를 쓰지 않는다 — 화면 참조는 s5_tips_and_screens.screens의 screen_id로만."""


def build_prompt_v3(case, derived, knowledge: List[KnowledgeItem], constraint: ConstraintContext) -> Prompt:
    knowledge_text = (
        "각 Knowledge에는 Case Relevance(왜 지금 중요한가)와 Usage Boundary(단정하면 안 되는 것)가 있다. "
        "세부(시한·조건·절차)를 실제로 사용하고 Boundary를 넘지 않는다.\n\n"
        + "\n\n".join(k.as_text() for k in knowledge)
    )
    supply_text = _cx.render_supply(case)
    if supply_text:
        knowledge_text += "\n\n" + supply_text
    return Prompt(
        system_role=SYSTEM_ROLE_V3,
        customer_context=_cx.render_blocks(case, derived),
        constraint_context=constraint.as_text(),
        knowledge_context=knowledge_text,
        output_instruction=OUTPUT_INSTRUCTION_V3,
        knowledge_ids=[k.kid for k in knowledge],
    )


def check_schema_v3(obj: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    for k in REQUIRED_TOP:
        if k not in obj:
            errs.append(f"missing key: {k}")
    mj = obj.get("management_judgment")
    if isinstance(mj, dict):
        for k in ("judgment", "reasoning"):
            if not str(mj.get(k, "")).strip():
                errs.append(f"management_judgment.{k} is empty")
        if isinstance(mj.get("judgment"), str) and not detect_judgment_types(obj):
            errs.append("management_judgment.judgment names none of the judgment types")
        for k in ("supporting_evidence_ids", "supporting_knowledge_ids", "must_confirm_before_action"):
            if k in mj and not isinstance(mj[k], list):
                errs.append(f"management_judgment.{k} must be a list")
    elif mj is not None:
        errs.append("management_judgment must be an object")
    na = obj.get("next_actions")
    if isinstance(na, list):
        for i, c in enumerate(na):
            if not isinstance(c, dict):
                errs.append(f"next_actions[{i}] must be an object")
                continue
            for k in ("action", "kind", "risk_level"):
                if not str(c.get(k, "")).strip():
                    errs.append(f"next_actions[{i}].{k} is empty")
    elif na is not None:
        errs.append("next_actions must be a list")

    eb = obj.get("employee_brief")
    if not isinstance(eb, dict):
        if eb is not None:
            errs.append("employee_brief must be an object")
        return errs
    if not str(eb.get("s1_customer_situation", "")).strip():
        errs.append("employee_brief.s1_customer_situation is empty")
    s2 = eb.get("s2_management_point")
    if not isinstance(s2, dict) or not str(s2.get("point", "")).strip():
        errs.append("employee_brief.s2_management_point.point is empty")
    else:
        for k in ("check_before_consult", "check_with_customer"):
            if k in s2 and not isinstance(s2[k], list):
                errs.append(f"employee_brief.s2_management_point.{k} must be a list")
    s3 = eb.get("s3_direction")
    if not isinstance(s3, dict) or not isinstance(s3.get("directions"), list) or not s3.get("directions"):
        errs.append("employee_brief.s3_direction.directions must be a non-empty list (no not_applicable in v3)")
    else:
        for i, d in enumerate(s3["directions"]):
            if not isinstance(d, dict) or not str(d.get("direction", "")).strip():
                errs.append(f"employee_brief.s3_direction.directions[{i}].direction is empty")
        if not isinstance(s3.get("product_candidates", []), list):
            errs.append("employee_brief.s3_direction.product_candidates must be a list")
        else:
            for i, p in enumerate(s3.get("product_candidates") or []):
                if not isinstance(p, dict) or not str(p.get("product_id", "")).strip():
                    errs.append(f"employee_brief.s3_direction.product_candidates[{i}].product_id missing")
                elif not p.get("reasons"):
                    errs.append(f"employee_brief.s3_direction.product_candidates[{i}].reasons is empty")
    s4 = eb.get("s4_consult_script")
    if not isinstance(s4, dict) or not isinstance(s4.get("scripts"), list) or \
            not any(str(x).strip() for x in s4.get("scripts", [])):
        errs.append("employee_brief.s4_consult_script.scripts must contain at least one script")
    s5 = eb.get("s5_tips_and_screens")
    if not isinstance(s5, dict):
        errs.append("employee_brief.s5_tips_and_screens must be an object")
    else:
        for k, idf in (("tips", "tip_id"), ("screens", "screen_id")):
            if not isinstance(s5.get(k, []), list):
                errs.append(f"employee_brief.s5_tips_and_screens.{k} must be a list")
            else:
                for i, x in enumerate(s5.get(k) or []):
                    if not isinstance(x, dict) or not str(x.get(idf, "")).strip():
                        errs.append(f"employee_brief.s5_tips_and_screens.{k}[{i}].{idf} missing")
    return errs


def validate_supply_refs(case, obj: Dict[str, Any], constraint: ConstraintContext) -> Dict[str, Any]:
    """Deterministic supply-reference checks (Contract §3).

    FAIL: id outside supply / sellable=false product recommended / product
    risk grade above the customer's eligibility (C2 via supply metadata).
    """
    ids = _cx.supply_ids(case)
    grade_by_id = {p["product_id"]: p.get("risk_grade")
                   for p in case.supply.get("product_candidates") or []}
    min_grade = PROFILE_MIN_FUND_GRADE[constraint.investment_profile]
    eb = obj.get("employee_brief") or {}
    s3 = eb.get("s3_direction") or {} if isinstance(eb, dict) else {}
    s5 = eb.get("s5_tips_and_screens") or {} if isinstance(eb, dict) else {}
    findings, overall = [], "PASS"

    def fail(**kw):
        nonlocal overall
        findings.append({**kw, "verdict": "FAIL"})
        overall = "FAIL"

    for p in s3.get("product_candidates") or []:
        pid = p.get("product_id")
        if pid not in ids["products"]:
            fail(where="product_candidates", id=pid, issue="not in candidate pool")
        else:
            if pid in ids["unsellable_products"]:
                fail(where="product_candidates", id=pid, issue="sellable=false product recommended")
            g = grade_by_id.get(pid)
            if isinstance(g, int) and g < min_grade:
                fail(where="product_candidates", id=pid,
                     issue=f"risk grade {g} exceeds profile eligibility (min allowed {min_grade})")
    for t in s5.get("tips") or []:
        if t.get("tip_id") not in ids["tips"]:
            fail(where="tips", id=t.get("tip_id"), issue="tip not in supply")
    for sc in s5.get("screens") or []:
        if sc.get("screen_id") not in ids["screens"]:
            fail(where="screens", id=sc.get("screen_id"), issue="screen not in supply")
    return {"check": "supply_refs", "findings": findings, "overall": overall}


# Screen numbers as they appear in text, e.g. [04-12-642], [06-AD-080], [04-12-17A].
_SCREEN_NO_RE = re.compile(r"\[[0-9]{2}-[0-9A-Z]{2,3}-[0-9A-Z]{2,4}\]")


def validate_screen_refs(case, obj: Dict[str, Any]) -> Dict[str, Any]:
    """G3 (Gate ① 2026-08-31): S5 is the single display position for screen references.

    Deterministic string/structure check only:
    - screen number in model output that is not among supplied screens -> FAIL
    - supplied screen number written directly into Brief S1~S4 prose -> REVIEW
      (screen references belong in s5 as screen_id; internal structured fields
       such as must_confirm_before_action are not the Brief and are not flagged)
    """
    known = {s.get("screen_no") for s in (case.supply.get("screens") or []) if s.get("screen_no")}

    def walk(node, path):
        if isinstance(node, str):
            for m in _SCREEN_NO_RE.findall(node):
                yield path, m
        elif isinstance(node, dict):
            for k, v in node.items():
                yield from walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from walk(v, f"{path}[{i}]")

    findings, overall = [], "PASS"
    for path, num in walk(obj, "$"):
        if num not in known:
            findings.append({"where": path, "screen_no": num, "verdict": "FAIL",
                             "issue": "screen number not provided in supply (fabrication)"})
            overall = "FAIL"
        elif ".employee_brief." in path and ".s5_tips_and_screens" not in path:
            findings.append({"where": path, "screen_no": num, "verdict": "REVIEW",
                             "issue": "screen number exposed outside S5 (S5 is the single reference position)"})
            if overall != "FAIL":
                overall = "REVIEW"
    return {"check": "screen_refs", "findings": findings, "overall": overall}


class _CanonicalTextShim:
    """Adapter so build_constraint_context can read 투자성향 from canonical evidence."""

    def __init__(self, case):
        self.case_id = case.case_id
        self._text = "\n".join(it.text for it in case.evidence)

    def as_text(self) -> str:
        return self._text


def run_case_v3(case_id: str, dry_run: bool = False) -> Dict[str, Any]:
    started = _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    record: Dict[str, Any] = {
        "case_id": case_id,
        "runtime_revision": RUNTIME_REVISION_V3,
        "started_at": started,
        "model": MODEL_ID,
        "endpoint": ENDPOINT,
        "generation_config": None,
        "git_head": _git_head(),
        "status": None,
        "error": "",
    }
    try:
        case = _cx.load_canonical(case_id, root=REPO_ROOT)
        # P3-B (opt-in): Minimal Product Selector replaces ONLY supply.product_candidates.
        # Direction/Solution Type input is Human-defined (design/P3B_PRODUCT_NEEDS.md);
        # Hard Constraint / supply validators / Fit-reason generation stay unchanged below.
        if os.environ.get("P3_HYBRID_PRODUCT_SELECTION") == "1":
            import hybrid_selector as _hy
            _profile = build_constraint_context(_CanonicalTextShim(case)).investment_profile
            _pool, _pool_log = _hy.build_pool_hybrid(case_id, investment_profile=_profile)
            record["p3_hybrid_product_selection"] = {
                "frozen_pool_product_ids": [p.get("product_id") for p in case.supply.get("product_candidates") or []],
                "deterministic_pool": _pool_log["deterministic_pool"],
                "final_pool": _pool_log["final_pool"],
                "fallback": _pool_log["fallback"],
            }
            case.supply["product_candidates"] = _pool
        elif os.environ.get("P3B_PRODUCT_SELECTION") == "1":
            import product_selector as _ps
            _pool, _pool_log = _ps.build_pool(case_id)
            record["p3b_product_selection"] = {
                "needs_file": "design/P3B_PRODUCT_NEEDS.md",
                "frozen_pool_product_ids": [p.get("product_id") for p in case.supply.get("product_candidates") or []],
                "selector_pool": _pool_log["selected"],
                "none_reason": _pool_log["none_reason"],
            }
            case.supply["product_candidates"] = _pool
        derived = _cx.derive(case)
        constraint = build_constraint_context(_CanonicalTextShim(case))
        # v3 cases carry the profile in canonical.json, not case.md — cite the real source.
        constraint.basis = (
            "Human-approved Constraint (golden/HUMAN_DECISIONS.md HD-2·HD-2.1; "
            f"cases/{case_id}/canonical.json 투자성향 Evidence). C2 매핑은 KB 투자권유 기준(SRC-096)."
        )
        knowledge, kp_path, kp_sha = load_knowledge_items(case_id)
        prompt = build_prompt_v3(case, derived, knowledge, constraint)
    except Exception as e:
        record.update(status=CONFIG_ERROR, error=f"{type(e).__name__}: {e}")
        return record

    record.update({
        "frozen_canonical": {"file": str(Path(case.source_file).resolve().relative_to(REPO_ROOT)) if str(case.source_file).startswith(str(REPO_ROOT)) else case.source_file,
                             "sha256": case.source_sha256},
        "frozen_knowledge_pack": {"knowledge_pack": kp_path, "knowledge_pack_sha256": kp_sha},
        "evidence_blocks": {f"{n}. {_cx.BLOCK_TITLES[n]}":
                            [it.id for it in _cx.all_items(case, derived) if it.block == n]
                            for n in range(1, 10)},
        "derived_items": [{"id": it.id, "block": it.block, "type": it.evidence_type, "text": it.text}
                          for it in derived],
        "supply_summary": {k: sorted(v) for k, v in _cx.supply_ids(case).items()},
        "supply": case.supply,  # cards/originals/paths restored at render time (Contract §3)
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
    })
    if dry_run:
        record.update(status="DRY_RUN")
        return record

    resp = call_gemma(prompt.as_text())
    record["model_response"] = {"status": resp.status, "http_status": resp.http_status,
                                "finish_reason": resp.finish_reason, "usage": resp.usage, "error": resp.error}
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

    schema_errs = check_schema_v3(obj)
    record["schema_errors"] = schema_errs
    if schema_errs:
        record.update(status=SCHEMA_ERROR, error="; ".join(schema_errs))
        record["validation"] = validate_c1(obj, constraint)
        return record

    valid_eids = _cx.all_ids(case, derived)
    record["validation"] = validate_c1(obj, constraint)
    record["validation_c3"] = validate_c3_default_option(obj, constraint)
    record["validation_c2"] = validate_c2_fund_grade(obj, constraint)
    record["validation_forbidden_words"] = validate_forbidden_words(obj)
    record["validation_latex"] = validate_latex_residue(obj)
    record["validation_evidence_ids"] = validate_evidence_ids(obj, valid_eids)
    record["validation_supply_refs"] = validate_supply_refs(case, obj, constraint)
    record["validation_screen_refs"] = validate_screen_refs(case, obj)
    record["judgment_types_detected"] = detect_judgment_types(obj)
    record["employee_brief"] = obj.get("employee_brief", {})

    hard = ("validation", "validation_c3", "validation_c2", "validation_forbidden_words",
            "validation_evidence_ids", "validation_supply_refs", "validation_screen_refs")
    errs = [f"{k}: FAIL" for k in hard if record[k]["overall"] == "FAIL"]
    record.update(status=(VALIDATION_ERROR if errs else SUCCESS), error="; ".join(errs))
    return record
