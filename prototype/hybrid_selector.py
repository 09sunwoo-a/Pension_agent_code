# -*- coding: utf-8 -*-
"""
P3 Integration — Hybrid Selection orchestration (thin layer).

    Deterministic Retrieval (selector.py / product_selector.py — High Recall)
      → LLM Pruning (llm_selector.py — 명백히 불필요한 후보만 제거)
      → Deterministic Safety/Authority/Constraint Gate (기존 selector 조립 +
        기존 runtime C1/C2/C3·supply validator — 여기로 이동하지 않음)
      → Final Context

Fallback (모든 LLM 실패): deterministic candidate set을 그대로 사용하고
log에 기록한다 — Precision은 낮아져도 Recall을 잃지 않는다.

No new precision rules on the deterministic layer (P3 Integration §3),
no per-type product caps (§4). Standard library only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import runtime
import selector as _ks
import product_selector as _ps
import llm_selector as _llm

OUT_DIR = Path(__file__).resolve().parent / "out"


def _write_log(name: str, log: Dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / name).write_text(json.dumps(log, ensure_ascii=False, indent=2, default=str),
                                encoding="utf-8")


# ---------------------------------------------------------------------------
# Knowledge: deterministic candidates → LLM prune → deterministic assembly
# ---------------------------------------------------------------------------
def select_knowledge_hybrid(case_id: str, needs: Optional[List[Dict[str, Any]]] = None,
                            manual_keep: Optional[List[str]] = None,
                            log_name: Optional[str] = None):
    """Returns (items, log). Same K-item 5-field contract as selector.py."""
    if needs is None:
        needs, manual_keep = _ks.load_needs(case_id)
    # [1] deterministic high-recall retrieval (assembly discarded — 후보 집합만 사용)
    _, det_log = _ks.select_for_case(case_id, needs=needs, manual_keep=manual_keep)
    det_candidates = [s for s in det_log["selected"] if s["kind"] in ("OK", "KG")]
    cand_summaries = []
    reg_titles = {it["id"]: (it["title"], it["topics"]) for it in _ks.parse_official_knowledge()}
    reg_titles.update({it["id"]: (it["title"], it["topic"]) for it in _ks.parse_knowledge_gaps()})
    for s in det_candidates:
        title, topics = reg_titles.get(s["registry_ref"], (s["registry_ref"], ""))
        cand_summaries.append({"id": s["registry_ref"], "kind": s["kind"], "title": title,
                               "topics": topics, "need_ref": s["need_ref"]})
    # [2] LLM pruning (요약만 전달 — 원문/Trust 판단 없음)
    fallback_reason = None
    keep_ids = None
    prune: Dict[str, Any] = {}
    if cand_summaries:
        prune = _llm.prune_knowledge(needs, cand_summaries)
        if prune.get("ok"):
            keep_ids = set(prune["keep"])
        else:
            fallback_reason = prune.get("fallback_reason", "unknown")
    # [3] deterministic gates + assembly (kept subset; fallback = 전체)
    items, sel_log = _ks.select_for_case(case_id, needs=needs, manual_keep=manual_keep,
                                         keep_registry_ids=keep_ids)
    log = {
        "case_id": case_id, "mode": "hybrid_knowledge",
        "deterministic_candidates": [s["registry_ref"] for s in det_candidates],
        "llm_prune": {"ok": prune.get("ok", False),
                      "keep": prune.get("keep"), "removed": prune.get("removed"),
                      "unmentioned_kept": prune.get("unmentioned_kept"),
                      "reason": prune.get("reason"),
                      "model_status": (prune.get("call") or {}).get("status"),
                      "usage": (prune.get("call") or {}).get("usage")},
        "fallback": fallback_reason,
        "final_selected": sel_log["selected"],
        "excluded": sel_log["excluded"],
    }
    _write_log(log_name or f"hybrid_knowledge_{case_id}.json", log)
    return items, log


def load_knowledge_items_hybrid(case_id: str):
    """Drop-in for runtime.load_knowledge_items (same return shape)."""
    items, _ = select_knowledge_hybrid(case_id)
    return items, f"hybrid:{_ks.NEEDS_FILE.relative_to(_ks.REPO_ROOT)}", \
        hashlib.sha256(_ks.NEEDS_FILE.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Product: deterministic pool → eligibility annotation(기존 C2 매핑 재사용)
#          → LLM prune → final pool (Hard Constraint는 runtime validator 그대로)
# ---------------------------------------------------------------------------
def _eligibility_annotation(card: Dict[str, Any], profile: Optional[str]) -> str:
    """Reuse the existing C2 single source of truth (runtime.PROFILE_MIN_FUND_GRADE).
    표시만 한다 — 필터·차단 책임은 기존 runtime validator에 남는다."""
    g = card.get("risk_grade")
    if profile is None or g is None:
        return "권유 가능 여부: 원리금보장/등급 해당없음" if g is None else ""
    min_g = runtime.PROFILE_MIN_FUND_GRADE[profile]
    return ("권유 가능 (성향 범위 내)" if g >= min_g
            else f"고객 성향({profile}) 밖 — 신규 권유 불가(기존 C2가 차단)")


def build_pool_hybrid(case_id: str, needs: Optional[List[Dict[str, Any]]] = None,
                      none_reason: Optional[str] = None,
                      investment_profile: Optional[str] = None,
                      log_name: Optional[str] = None):
    """Returns (pool, log). Pool cards are the deterministic cards verbatim —
    pruning only subsets, ids/values unchanged."""
    det_pool, det_log = _ps.select_products(case_id, needs=needs, none_reason=none_reason)
    needs_used = needs if needs is not None else [
        {"need_id": n["need_id"], "solution_type": n["solution_type"],
         "characteristics": n["characteristics"]} for n in det_log["needs"]] if det_log["needs"] else []
    need_by_pid = {s["product_id"]: s["need_ref"] for s in det_log["selected"]}
    fallback_reason = None
    final_pool = det_pool
    prune: Dict[str, Any] = {}
    if det_pool:
        cand = []
        for c in det_pool:
            cand.append({"product_id": c["product_id"], "name": c.get("name", ""),
                         "product_type": c.get("product_type", ""),
                         "risk_grade": c.get("risk_grade"),
                         "maturity_note": c.get("maturity_note"),
                         "need_ref": need_by_pid.get(c["product_id"]),
                         "eligibility": _eligibility_annotation(c, investment_profile)})
        note = (f"고객 투자성향: {investment_profile} — 아래 '권유 가능 여부'는 기존 C2 기준의 표시이며, "
                f"최종 차단은 이후 단계의 기존 validator가 수행한다.") if investment_profile else ""
        prune = _llm.prune_products(needs_used, cand, eligibility_note=note)
        if prune.get("ok"):
            keep = set(prune["keep"])
            final_pool = [c for c in det_pool if c["product_id"] in keep]
        else:
            fallback_reason = prune.get("fallback_reason", "unknown")
    log = {
        "case_id": case_id, "mode": "hybrid_product",
        "investment_profile": investment_profile,
        "deterministic_pool": [c["product_id"] + " " + c.get("name", "")[:30] for c in det_pool],
        "llm_prune": {"ok": prune.get("ok", False), "keep": prune.get("keep"),
                      "removed": prune.get("removed"),
                      "unmentioned_kept": prune.get("unmentioned_kept"),
                      "reason": prune.get("reason"),
                      "model_status": (prune.get("call") or {}).get("status"),
                      "usage": (prune.get("call") or {}).get("usage")},
        "fallback": fallback_reason,
        "none_reason": det_log.get("none_reason"),
        "final_pool": [c["product_id"] + " " + c.get("name", "")[:30] for c in final_pool],
        "det_excluded": det_log["excluded"],
    }
    _write_log(log_name or f"hybrid_product_{case_id}.json", log)
    return final_pool, log
