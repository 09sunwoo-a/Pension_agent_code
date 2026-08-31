# -*- coding: utf-8 -*-
"""
P3-C LLM Selector Baseline Experiment.

Same input/output boundary as the P3-A/P3-B deterministic selectors — only the
*relevance decision* is delegated to the LLM:

    Knowledge:  Human-defined Need (P3A_KNOWLEDGE_NEEDS.md, unchanged)
                + compact OK/KG Registry Index (registry fields verbatim)
                -> LLM returns selected IDs (JSON only)
                -> deterministic gates (ID existence / status / authority)
                -> Registry content loaded deterministically (never from LLM)
                -> same K-item 5-field structure as P3-A

    Product:    Human-defined Product Need (P3B_PRODUCT_NEEDS.md, unchanged)
                + compact PRD Index
                -> LLM returns selected product IDs (JSON only)
                -> deterministic gates (ID existence / status / card completeness)
                -> ProductCandidate cards assembled verbatim from the registry

The LLM never: writes/summarises registry content, generates needs, judges the
customer, recommends products, promotes authority, or mutates null/status/as_of.
Those stay in code (P3-C instruction §8/§12). `selection_reason` is log/eval
material only — it is NOT passed to the Decision Agent.

Opt-in only:  P3A_LLM_SELECTION=1 / P3B_LLM_SELECTION=1. Default runtime paths
(Human pack, P3-A deterministic, P3-B deterministic) are unchanged.

No vector search / embedding / reranker / ontology (instruction §20).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import runtime
import selector as _ksel            # P3-A: needs loader, registry parsers, K-item assembly rules
import product_selector as _psel    # P3-B: needs loader, PRD parser, card completeness gate

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent / "out"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Compact Index rendering — registry fields verbatim, no authored description.
# (Instruction §5: start with title/topics/applicability_tags; do not create
#  a new short description.)
# ---------------------------------------------------------------------------
def render_ok_index(ok_items: List[Dict[str, Any]]) -> str:
    lines = []
    for it in ok_items:
        lines.append(
            f"{it['id']}\n"
            f"  title: {it['title']}\n"
            f"  topics: {it['topics']}\n"
            f"  applicability_tags: {it['applicability_tags'] or '-'}\n"
            f"  authority: {it['authority']}\n"
            f"  status: {it['status']}")
    return "\n".join(lines)


def render_kg_index(kg_items: List[Dict[str, Any]]) -> str:
    lines = []
    for it in kg_items:
        lines.append(
            f"{it['id']}\n"
            f"  title: {it['title']}\n"
            f"  topic: {it['topic']}\n"
            f"  gap_type: {it['gap_type']}\n"
            f"  what_is_missing: {it['what_is_missing']}\n"
            f"  status: {it['status']}")
    return "\n".join(lines)


def _prd_key(entry: Dict[str, Any]) -> str:
    """Stable selectable ID. PRD-018 has multiple real product rows, so those
    are addressed as 'PRD-018|<name>' (§10 — contract unchanged downstream)."""
    if entry["prd_id"] == "PRD-018":
        return f"PRD-018|{entry['card']['name']}"
    return entry["prd_id"]


def render_prd_index(registry: List[Dict[str, Any]]) -> str:
    lines = []
    for e in registry:
        c = e["card"]
        grade = c.get("risk_grade")
        ret = c.get("return_recent")
        if ret is not None:
            ret_txt = f"{ret:+.2%} ({c.get('return_period')}, {c.get('return_as_of')})"
        else:
            ret_txt = "미확인"
        lines.append(
            f"{_prd_key(e)}\n"
            f"  name: {c.get('name')}\n"
            f"  product_type: {c.get('product_type')}\n"
            f"  risk_grade: {grade if grade is not None else 'null(원리금보장형 여부는 product_type 참조)'}\n"
            f"  maturity: {c.get('maturity_note') or '-'}\n"
            f"  return: {ret_txt}\n"
            f"  characteristics: {c.get('features', '')}\n"
            f"  status: {e['status'] or 'ACTIVE'}\n"
            f"  sellable: {c.get('sellable')} / channels: {c.get('channels') or []} / as_of: {e.get('as_of', '')}")
    return "\n".join(lines)


def render_knowledge_needs(needs: List[Dict[str, Any]]) -> str:
    lines = []
    for n in needs:
        lines.append(
            f"{n['need_id']}\n"
            f"  purpose: {n['purpose']}\n"
            f"  authority_required: {n['authority_required']}\n"
            f"  topic: {'; '.join(n['topics'])}\n"
            f"  need_text: {n['need_text']}")
    return "\n".join(lines)


def render_product_needs(needs: List[Dict[str, Any]]) -> str:
    lines = []
    for n in needs:
        lines.append(
            f"{n['need_id']}\n"
            f"  solution_type: {n['solution_type']}\n"
            f"  characteristics: {'; '.join(n['characteristics'])}\n"
            f"  maturity: {n.get('maturity') or '-'}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Selector prompts — ID selection only. No judgment / consulting / brief /
# recommendation is requested (§15).
# ---------------------------------------------------------------------------
KNOWLEDGE_SELECTOR_PROMPT = """당신은 Knowledge Registry에서 관련 항목의 ID만 고르는 selection 도구다.
아래 [Knowledge Need]는 사람이 정의한 것이며, [Registry Index]는 등록된 지식 항목의 목록이다.

선택 원칙:
1. Need를 실제로 해결하는 데 필요한 Knowledge만 선택한다.
2. 단어가 겹친다는 이유만으로 선택하지 않는다.
3. 같은 주제의 주변 Knowledge를 포괄적으로 수집하지 않는다.
4. 필요한 최소 항목만 선택한다.
5. Need가 요구하는 내용이 Knowledge Gap(KG)으로 등록되어 있으면 해당 KG도 선택한다.
6. Index에 없는 내용에 대해 Knowledge가 존재하지 않는다고 추론하지 않는다.
7. authority/status 값을 해석하거나 승격하지 않는다 — 그 처리는 이후 코드가 한다.
8. Knowledge의 내용으로 고객의 관리 필요성을 판단하지 않는다.
9. 이 작업은 관련성 선택(relevance selection)이며 최종 업무 판단이 아니다.

출력은 아래 JSON 객체 하나만 출력한다. 다른 텍스트·코드펜스를 붙이지 않는다.
selection_reason은 "이 Need의 무엇을 이 항목이 다루는가"만 짧게 쓴다 — 고객에 대한 판단·추천을 쓰지 않는다.

{{
  "selected_ok_ids": ["OK-xxx"],
  "selected_gap_ids": ["KG-xxx"],
  "selection_reason": {{"OK-xxx": "짧은 관련성 이유", "KG-xxx": "짧은 관련성 이유"}}
}}

[Knowledge Need]
{needs}

[Registry Index — OK (Official Knowledge)]
{ok_index}

[Registry Index — KG (Knowledge Gaps: 확인되지 않음이 등록된 항목)]
{kg_index}
"""

PRODUCT_SELECTOR_PROMPT = """당신은 Product Registry에서 후보 재료(Candidate Material)의 ID만 고르는 selection 도구다.
아래 [Product Need]는 사람이 확정한 Management Direction/Solution Type에서 전사된 것이며,
[PRD Index]는 등록된 상품 재료 목록이다.

선택 원칙:
1. 각 Need의 solution_type·intrinsic characteristics(상품 유형 특성)·maturity에 부합하는 후보 재료만 선택한다.
2. 이것은 후보 재료 선택이지 추천이 아니다 — "이 상품이 좋다/최적이다/수익률이 높다" 같은 판단을 하지 않는다.
3. 같은 유형의 후보가 여럿이면 Need 충족에 필요한 최소 수만 선택한다 (동일 유형 전체 나열 금지).
4. 고객 상황을 추정하거나 고객 적합성을 판단하지 않는다 — 그것은 이후 단계(Hard Constraint·Decision Agent)의 몫이다.
5. sellable/status/as_of 값을 해석·보완하지 않는다.
6. Index에 없는 상품을 만들지 않는다.

출력은 아래 JSON 객체 하나만 출력한다. 다른 텍스트·코드펜스를 붙이지 않는다.
selection_reason은 "이 Need의 어떤 intrinsic characteristic과 부합하는가"만 쓴다.

{{
  "selected_product_ids": ["PRD-xxx 또는 PRD-018|상품명"],
  "selection_reason": {{"PRD-xxx": "부합 이유"}}
}}

[Product Need]
{needs}

[PRD Index]
{prd_index}
"""


def _call_selector(prompt_text: str) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
    """One selector call via the existing Gemma transport. Returns (obj, meta)."""
    resp = runtime.call_gemma(prompt_text)
    meta = {"status": resp.status, "http_status": resp.http_status,
            "finish_reason": resp.finish_reason, "usage": resp.usage, "error": resp.error}
    if resp.status != runtime.SUCCESS or not resp.text:
        return None, meta
    obj, norms, perr = runtime.parse_model_json(resp.text)
    meta["json_normalizations"] = norms
    if obj is None:
        meta["parse_error"] = perr
        meta["raw_text"] = resp.text[:2000]
    return obj, meta


# ---------------------------------------------------------------------------
# P3-C Knowledge selection (LLM relevance -> deterministic gates -> K-items)
# ---------------------------------------------------------------------------
def select_knowledge_llm(case_id: str) -> Tuple[List["runtime.KnowledgeItem"], Dict[str, Any]]:
    needs, manual_keep = _ksel.load_needs(case_id)
    ok_items = _ksel.parse_official_knowledge()
    kg_items = _ksel.parse_knowledge_gaps()
    ok_by_id = {it["id"]: it for it in ok_items}
    kg_by_id = {it["id"]: it for it in kg_items}

    prompt = KNOWLEDGE_SELECTOR_PROMPT.format(
        needs=render_knowledge_needs(needs),
        ok_index=render_ok_index(ok_items),
        kg_index=render_kg_index(kg_items))
    obj, call_meta = _call_selector(prompt)

    log: Dict[str, Any] = {"case_id": case_id, "mode": "P3C_LLM", "call": call_meta,
                           "llm_output": obj, "gates": [], "selected": [],
                           "manual_keep": manual_keep,
                           "prompt_chars": len(prompt)}
    if obj is None:
        raise RuntimeError(f"P3-C knowledge selector call failed for {case_id}: {call_meta}")

    sel_ok = [str(x) for x in (obj.get("selected_ok_ids") or [])]
    sel_kg = [str(x) for x in (obj.get("selected_gap_ids") or [])]
    reasons = obj.get("selection_reason") or {}

    # Deterministic gates (LLM output is never auto-approved — §8):
    picked: List[Tuple[str, Dict[str, Any], List[str]]] = []
    # authority gate scope: every need in these cases requires T1/T2 (the file
    # says so); apply the same demotion rule as the deterministic selector.
    t1t2_required = any(n["authority_required"].startswith("T1/T2") for n in needs)
    for oid in sel_ok:
        it = ok_by_id.get(oid)
        if it is None:
            log["gates"].append({"id": oid, "gate": "DROPPED (id not in registry)"})
            continue
        if it["status"].startswith("SUPERSEDED"):
            log["gates"].append({"id": oid, "gate": "DROPPED (status=SUPERSEDED)"})
            continue
        flags: List[str] = []
        if it["status"].startswith("PROVISIONAL"):
            flags.append("PROVISIONAL — 확정 Fact 아님, 확인 필요 상태로만 사용")
        if it["status"].startswith("CONFLICT"):
            flags.append("CONFLICT — SOURCE_CONFLICTS의 SC 항목 참조, 임의 통합·해소 금지")
        if t1t2_required and not _ksel._has_official_authority(it["authority"]):
            flags.append("공식(T1/T2) 근거 미확보 — 판단 근거 아님, 확인 필요 상태로만 전달"
                         " (Operational Check Needed)")
        picked.append(("OK", it, flags))
        log["gates"].append({"id": oid, "gate": "PASSED", "flags": flags})
    for gid in sel_kg:
        it = kg_by_id.get(gid)
        if it is None:
            log["gates"].append({"id": gid, "gate": "DROPPED (id not in registry)"})
            continue
        picked.append(("KG", it, []))
        log["gates"].append({"id": gid, "gate": "PASSED (Knowledge Gap)"})

    # K-item assembly — registry content loaded deterministically, identical
    # 5-field structure to P3-A. Case Relevance is machine text; the LLM's
    # selection_reason goes to the log ONLY (§6 — not a Knowledge Fact).
    need_summary = "; ".join(f"{n['need_id']}: {n['need_text']}" for n in needs)
    items: List[runtime.KnowledgeItem] = []
    for kind, it, flags in picked:
        kid = f"K-{len(items) + 1:03d}"
        if kind == "OK":
            authority = it["authority"] + f" / status={it['status']} / as_of={it['as_of']}"
            if flags:
                authority += " / ⚠ " + " · ".join(flags)
            limitation = "\n".join(f"  · {b}" for b in it["limitation"]).lstrip() or "—"
            if flags:
                limitation += "\n  · (Selector 부착) " + " · ".join(flags)
            fields = {
                "Knowledge": "\n".join(f"  · {b}" for b in it["content"]).lstrip(),
                "Case Relevance": f"이 Case의 Human-defined Knowledge Need 대응 ({need_summary})",
                "Limitation": limitation,
                "Authority / Status": authority,
                "Source / Location": f"{it['id']} ({it['source']})",
            }
            items.append(runtime.KnowledgeItem(kid, it["title"], "Source-derived (Registry)", fields))
        else:
            fields = {
                "Knowledge": it["consume_text"],
                "Case Relevance": f"이 Case의 Human-defined Knowledge Need 대응 ({need_summary})",
                "Limitation": ("Knowledge Gap(부정 확인) 항목 — 본문 [사용 경계]가 Usage Boundary다. "
                               "확인되지 않음(부재)을 '불가'·'불존재'로 승격하지 않는다. "
                               f"인접 확인 자료: {it['what_exists_instead']}"),
                "Authority / Status": (f"Knowledge Gap ({it['gap_type']}) / status={it['status']} "
                                       f"/ verified_by: {it['verified_by']}"),
                "Source / Location": f"{it['id']} (knowledge/KNOWLEDGE_GAPS.md; related: {it['related']})",
            }
            items.append(runtime.KnowledgeItem(kid, it["title"],
                                               "Negative-confirmation (Knowledge Gap)", fields))
        log["selected"].append({"kid": kid, "kind": kind, "registry_ref": it["id"],
                                "llm_reason": reasons.get(it["id"], ""), "flags": flags})

    if manual_keep:
        frozen_items, _, _ = runtime._load_knowledge_items_manual(case_id)
        by_id = {k.kid: k for k in frozen_items}
        for orig_kid in manual_keep:
            src = by_id.get(orig_kid)
            if src is None:
                raise ValueError(f"{case_id}: manual_keep {orig_kid} not in Frozen pack")
            kid = f"K-{len(items) + 1:03d}"
            items.append(runtime.KnowledgeItem(kid, src.title, src.basis_type, dict(src.fields)))
            log["selected"].append({"kid": kid, "kind": "MANUAL_KEEP",
                                    "registry_ref": f"frozen:{orig_kid}", "llm_reason": "", "flags": []})
    return items, log


def load_knowledge_items_llm(case_id: str):
    """Drop-in for runtime.load_knowledge_items (P3A_LLM_SELECTION=1)."""
    items, log = select_knowledge_llm(case_id)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    log["registry_sha256"] = {"OFFICIAL_KNOWLEDGE.md": _sha(_ksel.OK_FILE),
                              "KNOWLEDGE_GAPS.md": _sha(_ksel.KG_FILE),
                              "P3A_KNOWLEDGE_NEEDS.md": _sha(_ksel.NEEDS_FILE)}
    (OUT_DIR / f"p3c_knowledge_{case_id}.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return items, f"llm_selector:{_ksel.NEEDS_FILE.relative_to(REPO_ROOT)}", _sha(_ksel.NEEDS_FILE)


# ---------------------------------------------------------------------------
# P3-C Product selection
# ---------------------------------------------------------------------------
def select_products_llm(case_id: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    needs, none_reason = _psel.load_product_needs(case_id)
    log: Dict[str, Any] = {"case_id": case_id, "mode": "P3C_LLM", "none_reason": none_reason,
                           "gates": [], "selected": []}
    if none_reason:
        # Same as deterministic: no product_need => empty pool is the normal
        # outcome; no LLM call is made (nothing to select against).
        log["call"] = None
        return [], log

    registry = _psel.parse_product_registry()
    by_key = {_prd_key(e): e for e in registry}
    prompt = PRODUCT_SELECTOR_PROMPT.format(
        needs=render_product_needs(needs), prd_index=render_prd_index(registry))
    obj, call_meta = _call_selector(prompt)
    log["call"] = call_meta
    log["llm_output"] = obj
    log["prompt_chars"] = len(prompt)
    if obj is None:
        raise RuntimeError(f"P3-C product selector call failed for {case_id}: {call_meta}")

    reasons = obj.get("selection_reason") or {}
    pool: List[Dict[str, Any]] = []
    seen = set()
    for pid in [str(x) for x in (obj.get("selected_product_ids") or [])]:
        entry = by_key.get(pid)
        if entry is None:
            log["gates"].append({"id": pid, "gate": "DROPPED (id not in registry)"})
            continue
        if entry["status"].startswith("SUPERSEDED"):
            log["gates"].append({"id": pid, "gate": "DROPPED (SUPERSEDED)"})
            continue
        ok, why = _psel._card_complete(entry["card"])
        if not ok:
            log["gates"].append({"id": pid, "gate": f"DROPPED ({why})"})
            continue
        if pid in seen:
            continue
        seen.add(pid)
        card = dict(entry["card"])  # registry values verbatim — null preserved
        card["product_id"] = f"P{len(pool) + 1:02d}"
        pool.append(card)
        log["gates"].append({"id": pid, "gate": "PASSED", "product_id": card["product_id"]})
        log["selected"].append({"product_id": card["product_id"], "prd": pid,
                                "name": card.get("name"), "product_type": card.get("product_type"),
                                "risk_grade": card.get("risk_grade"),
                                "sellable": card.get("sellable"),
                                "llm_reason": reasons.get(pid, "")})
    return pool, log


def build_pool_llm(case_id: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Entry point used by runtime (P3B_LLM_SELECTION=1). Writes the log."""
    pool, log = select_products_llm(case_id)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    log["registry_sha256"] = {"PRODUCT_REGISTRY.md": _sha(_psel.PRD_FILE),
                              "P3B_PRODUCT_NEEDS.md": _sha(_psel.NEEDS_FILE)}
    (OUT_DIR / f"p3c_pool_{case_id}.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return pool, log
