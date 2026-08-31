# -*- coding: utf-8 -*-
"""
P3-B Minimal Product Candidate Retrieval.

Automates ONLY:  Management Direction / Solution Type (Human-defined,
design/P3B_PRODUCT_NEEDS.md)  ->  PRD Registry 검색  ->  Candidate Pool 구성.

Preserved unchanged (P3-B instruction §4):
  - Management Judgment: the Agent's job — this module never generates
    judgments and its input needs are transcribed from Human case design,
    so Product never creates a Customer Management Need (order is
    Direction -> Retrieval, never reversed).
  - Hard Constraint (C1/C2/C3, sellable=false, deterministic validators):
    stays in prototype/runtime.py — this module does NOT filter by 투자성향.
  - Final candidate choice + Customer-Product Fit reasons: Decision Agent.
  - OK/KG selection (P3-A), HT/TALK/SCR retrieval: untouched.

Retrieval logic (minimal, no ranking):
  1. product_need.characteristics (intrinsic type keywords) match against
     PRD product_type (normalized substring). No customer-situation tags.
  2. status gate: SUPERSEDED excluded; PROVISIONAL flagged.
  3. card completeness gate (supply contract minimum — CANONICAL_CONTRACTS
     §2.1 / HD-PRE-P2-BRIEF S3 카드): 실명 name + risk_grade(원리금보장형은
     면제) + 수익률(측정기간·기준일 포함; 원리금보장형은 금리·기준월).
     미달 항목은 Pool 제외 + 사유 로그 (개별 상품 데이터 미확보 등).
  4. sellable/channels/as_of: Registry 값 그대로 전달 — null을 보완·추정하지
     않는다 (HD-P2-GATE2 (4) / DB-003 §5).
  5. `### none` 케이스는 빈 Pool이 정상 결과 (Retrieval Failure 아님).

No embedding / vector / rerank / return-based ranking. Standard library only.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
NEEDS_FILE = REPO_ROOT / "design" / "P3B_PRODUCT_NEEDS.md"
PRD_FILE = REPO_ROOT / "knowledge" / "PRODUCT_REGISTRY.md"
OUT_DIR = Path(__file__).resolve().parent / "out"

PRINCIPAL_PROTECTED_TYPES = ("정기예금", "GIC")


def _norm(s: str) -> str:
    return re.sub(r"[\s\[\]()·…]+", "", s or "").casefold()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# PRD Registry parsing
# ---------------------------------------------------------------------------
def _parse_kv_row_table(block: str) -> Dict[str, str]:
    """PRD header tables are one row of alternating key/value cells."""
    fields: Dict[str, str] = {}
    for line in block.splitlines():
        if not line.startswith("|") or re.match(r"^\|[\s\-|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] in ("source",):
            for i in range(0, len(cells) - 1, 2):
                fields[cells[i]] = cells[i + 1]
            break
    return fields


def parse_product_registry(path: Path = PRD_FILE) -> List[Dict[str, Any]]:
    """Return candidate materials with registry provenance.

    - PRD entries with a ```json card block are read verbatim (values never
      rewritten). PRD-018 (GIC 라인업) rows become one material per row,
      assembled only from values stated in that entry.
    - PRD-021(DO 포트폴리오)·PRD-022(판매중단 목록)는 카드 재료가 아니므로
      제외 (DO 등록·Execution Eligibility의 별도 경로).
    """
    text = path.read_text(encoding="utf-8")
    out: List[Dict[str, Any]] = []
    for block in re.split(r"^(?=### PRD-\d{3}\. )", text, flags=re.M):
        head = re.match(r"^### (PRD-\d{3})\. (.+)$", block, re.M)
        if not head:
            continue
        prd_id, title = head.group(1), head.group(2).strip()
        meta = _parse_kv_row_table(block)
        status = meta.get("status", "")
        if prd_id == "PRD-018":
            # GIC 라인업 — 상품 행 테이블 (상품명/신용등급/계약기간/금리/잔여한도)
            for m in re.finditer(
                    r"^\|\s*([^|]*이율보증형[^|]*)\s*\|\s*(A{1,3}[+\-]?)\s*\|\s*(\d+년)\s*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|",
                    block, re.M):

                name, rating, term, rate, limit_rem = (m.group(i).strip() for i in range(1, 6))
                out.append({
                    "prd_id": prd_id, "status": status, "as_of": meta.get("as_of", ""),
                    "card": {
                        "name": name,
                        "product_type": "GIC(이율보증형보험)",
                        "risk_grade": None, "risk_level_label": None,
                        "return_recent": float(rate) / 100.0,
                        "return_period": "공시이율(연복리)",
                        "return_as_of": "2026-07",
                        "features": (f"보험사 발행 원리금보장상품 — 예금자보호 대상, IRP 연금지급 가능, "
                                     f"최소금액 제한 없음, 별도 신청 없이 거래 가능(운용지시서 상품종류 '보험'). "
                                     f"신용등급 {rating}, 계약기간 {term}, 잔여한도 {limit_rem}억원(금리·한도 월단위 변동). "
                                     f"금리는 공시이율(연복리) — 타 상품 비교 시 단리 환산 필요"),
                        "maturity_note": f"계약기간 {term}",
                        "sellable": None, "channels": [],
                    },
                })
            continue
        jm = re.search(r"```json\s*\n(.*?)```", block, re.S)
        if not jm:
            continue
        try:
            card = json.loads(jm.group(1))
        except json.JSONDecodeError:
            continue
        card.setdefault("sellable", None)
        card.setdefault("channels", [])
        out.append({"prd_id": prd_id, "status": status,
                    "as_of": meta.get("as_of", ""), "card": card})
    return out


# ---------------------------------------------------------------------------
# Needs parsing (Human-defined — design/P3B_PRODUCT_NEEDS.md)
# ---------------------------------------------------------------------------
def load_product_needs(case_id: str, path: Path = NEEDS_FILE) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Return (needs, none_reason). none_reason set => empty pool is the
    expected normal outcome for this case."""
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(case_id)}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise ValueError(f"P3B_PRODUCT_NEEDS.md has no section for {case_id}")
    section = m.group(1)
    needs: List[Dict[str, Any]] = []
    none_reason: Optional[str] = None
    for block in re.split(r"^(?=### )", section, flags=re.M):
        head = re.match(r"^### (PN-\d+|none)", block)
        if not head:
            continue
        fields: Dict[str, str] = {}
        for row in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", block, re.M):
            if row.group(1).strip() != "필드":
                fields[row.group(1).strip()] = row.group(2).strip()
        if head.group(1) == "none":
            none_reason = fields.get("reason", "product_need 없음")
        else:
            needs.append({
                "need_id": head.group(1),
                "solution_type": fields.get("solution_type", ""),
                "characteristics": [c.strip() for c in fields.get("characteristics", "").split(";") if c.strip()],
                "maturity": fields.get("maturity", ""),
                "origin": fields.get("origin", ""),
            })
    if needs and none_reason:
        raise ValueError(f"{case_id}: both PN- needs and 'none' declared")
    return needs, none_reason


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------
def _card_complete(card: Dict[str, Any]) -> Tuple[bool, str]:
    name = card.get("name") or ""
    if not name or "미확보" in name:
        return False, "실명 상품 아님 (유형 정보만 — 개별 상품 데이터 미확보)"
    protected = any(t in (card.get("product_type") or "") for t in PRINCIPAL_PROTECTED_TYPES)
    if card.get("risk_grade") is None and not protected:
        return False, "risk_grade 미확인 (원리금보장형 아님) — C2 검증 불가 카드"
    if card.get("return_recent") is None or not card.get("return_as_of"):
        return False, "수익률/기준일 미확보 — S3 카드 최소 필드 미달"
    return True, ""


def select_products(case_id: str, needs: Optional[List[Dict[str, Any]]] = None,
                    none_reason: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Return (candidate pool in ProductCandidate contract shape, log).

    needs default to the Human-defined file (P3-B path); callers may pass a
    programmatic product_need list (Hybrid/Mock) with the same shape
    (need_id / solution_type / characteristics / maturity)."""
    if needs is None and none_reason is None:
        needs, none_reason = load_product_needs(case_id)
    needs = needs or []
    registry = parse_product_registry()
    log: Dict[str, Any] = {"case_id": case_id, "needs": [], "selected": [],
                           "excluded": [], "none_reason": none_reason}
    pool: List[Dict[str, Any]] = []
    seen: set = set()

    for need in needs:
        nlog = {"need_id": need["need_id"], "solution_type": need["solution_type"],
                "characteristics": need["characteristics"], "hits": []}
        for entry in registry:
            ptype = _norm(entry["card"].get("product_type", ""))
            matched = [kw for kw in need["characteristics"] if _norm(kw) in ptype]
            if not matched:
                continue
            if need.get("maturity") and entry["card"].get("maturity_note"):
                if _norm(need["maturity"]) not in _norm(entry["card"]["maturity_note"]):
                    nlog["hits"].append({"prd": entry["prd_id"], "name": entry["card"].get("name", ""),
                                         "gate": f"EXCLUDED (maturity {need['maturity']} 불일치)"})
                    continue
            if entry["status"].startswith("SUPERSEDED"):
                nlog["hits"].append({"prd": entry["prd_id"], "name": entry["card"].get("name", ""),
                                     "gate": "EXCLUDED (SUPERSEDED)"})
                log["excluded"].append({"need": need["need_id"], "prd": entry["prd_id"],
                                        "reason": "SUPERSEDED"})
                continue
            ok, why = _card_complete(entry["card"])
            if not ok:
                nlog["hits"].append({"prd": entry["prd_id"], "name": entry["card"].get("name", ""),
                                     "gate": f"EXCLUDED ({why})"})
                log["excluded"].append({"need": need["need_id"], "prd": entry["prd_id"],
                                        "name": entry["card"].get("name", ""), "reason": why})
                continue
            key = (entry["prd_id"], entry["card"].get("name"))
            if key in seen:
                continue
            seen.add(key)
            card = dict(entry["card"])  # registry values verbatim; only id added
            card["product_id"] = f"P{len(pool) + 1:02d}"
            flags = []
            if entry["status"].startswith("PROVISIONAL"):
                flags.append("PROVISIONAL")
            pool.append(card)
            nlog["hits"].append({"prd": entry["prd_id"], "name": card["name"],
                                 "gate": "SELECTED", "product_id": card["product_id"],
                                 "matched": matched, "flags": flags})
            log["selected"].append({"product_id": card["product_id"], "prd": entry["prd_id"],
                                    "name": card["name"], "product_type": card["product_type"],
                                    "risk_grade": card.get("risk_grade"),
                                    "sellable": card.get("sellable"),
                                    "need_ref": need["need_id"], "matched": matched,
                                    "flags": flags})
        log["needs"].append(nlog)
    return pool, log


def build_pool(case_id: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Entry point used by runtime (P3B_PRODUCT_SELECTION=1). Writes the log."""
    pool, log = select_products(case_id)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    log["registry_sha256"] = {"PRODUCT_REGISTRY.md": _sha256(PRD_FILE),
                              "P3B_PRODUCT_NEEDS.md": _sha256(NEEDS_FILE)}
    (OUT_DIR / f"p3b_pool_{case_id}.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return pool, log
