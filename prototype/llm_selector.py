# -*- coding: utf-8 -*-
"""
P3 Integration — LLM Pruning layer for Hybrid Selection.

Role boundary (Human instruction, P3 Integration §2):
    Deterministic Retrieval = 놓치지 않는 것 (High-Recall Candidate Set)
    LLM (this module)       = 후보 중 명백히 불필요한 것만 제거
    Deterministic Gate      = 사용할 수 있는 범위 통제 (Authority/Status/Constraint)

The LLM never retrieves from the Registry, never decides trust level, never
creates content, never picks the final recommendation. Any LLM failure
(timeout / HTTP / parse / out-of-candidate ids / abnormal empty keep) falls
back to the full deterministic candidate set — LLM 실패 ≠ Retrieval 실패.

Uses the same fixed model adapter as the runtime (runtime.call_gemma).
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

import runtime  # call_gemma / parse_model_json


KNOWLEDGE_PRUNE_PROMPT = """당신은 Knowledge 검색기가 아닙니다.

앞 단계에서 관련 가능성이 있는 Knowledge를 넓게 회수했습니다.
당신의 역할은 주어진 Knowledge Need를 기준으로 후보 중 명백히 불필요한 항목만 제거하는 것입니다.

KEEP:
- Need를 직접 해결하는 Knowledge
- 직접 Knowledge를 해석하거나 적용하는 데 필요한 보조 Knowledge
- 판단의 불확실성 또는 확인 필요 상태를 나타내는 관련 Knowledge Gap (KG-)

REMOVE:
- 단어만 겹치고 실제 Need와 관련 없는 주변 Knowledge
- 다른 의사결정 주제를 다루는 Knowledge

애매하면 REMOVE보다 KEEP을 우선하십시오.
Knowledge의 내용을 새로 생성하거나 수정하지 마십시오.
후보에 없는 ID를 추가하지 마십시오.
고객의 Management Judgment나 Solution을 판단하지 마십시오.

다음 JSON 객체 하나만 출력하십시오 (다른 텍스트 금지):
{"keep_ids": ["..."], "remove_ids": ["..."], "reason": {"<removed_id>": "한 줄 사유"}}"""


PRODUCT_PRUNE_PROMPT = """당신은 상품 추천기가 아닙니다.

앞 단계에서 Product Need의 상품 유형에 해당하는 후보를 넓게 회수했습니다.
당신의 역할은 Product Need에 실질적으로 필요한 Candidate만 유지하는 것입니다.

원칙:
- 동일 유형의 후보가 여러 개라면, 차별화되는 source-backed characteristic(위험등급·만기 구조·상품 특성)이 없는 단순 중복 후보는 제거할 수 있다.
- 그러나 서로 다른 조건/분기(Product Need의 solution_type들)를 지원하는 후보는 함께 유지한다 — 각 분기를 지원하는 후보를 모두 제거하지 않는다. 새로운 분기를 만들지 않는다.
- 수익률이 높다는 이유만으로 대표 후보를 선택하지 않는다.
- 후보에 '고객 성향 밖(권유 불가)' 표시가 있는 항목을 유지해도 이후 단계가 차단하지만, 해당 유형의 '권유 가능' 후보를 모두 제거하여 유형이 통째로 사라지게 하지 않는다.
- 고객에게 최종 추천할 상품을 결정하지 않는다. Final Candidate Pool만 구성한다.

애매하면 제거보다 유지를 우선한다. 후보에 없는 ID를 추가하지 않는다.

다음 JSON 객체 하나만 출력하십시오 (다른 텍스트 금지):
{"keep_product_ids": ["..."], "remove_product_ids": ["..."], "reason": {"<removed_id>": "한 줄 사유"}}"""


def _call_and_parse(prompt_text: str) -> Dict[str, Any]:
    resp = runtime.call_gemma(prompt_text)
    out: Dict[str, Any] = {"status": resp.status, "error": resp.error, "obj": None,
                           "usage": resp.usage, "raw_text": resp.text}
    if resp.status != runtime.SUCCESS:
        return out
    obj, _, perr = runtime.parse_model_json(resp.text)
    if obj is None:
        out["status"] = "PRUNE_PARSE_ERROR"
        out["error"] = perr
        return out
    out["obj"] = obj
    return out


def _resolve_keep(obj: Dict[str, Any], keep_key: str, remove_key: str,
                  candidate_ids: List[str]) -> Dict[str, Any]:
    """Validate the pruner output against the candidate set.

    Fallback triggers (→ ok=False, caller uses full deterministic set):
      out-of-candidate id in either list / abnormal empty keep.
    Ids mentioned in neither list are KEPT (애매하면 KEEP).
    """
    cand = set(candidate_ids)
    keep = [str(x) for x in (obj.get(keep_key) or [])]
    remove = [str(x) for x in (obj.get(remove_key) or [])]
    outside = [x for x in keep + remove if x not in cand]
    if outside:
        return {"ok": False, "fallback_reason": f"out-of-candidate ids: {outside}"}
    if not keep and cand:
        return {"ok": False, "fallback_reason": "empty keep over non-empty candidates"}
    unmentioned = [x for x in candidate_ids if x not in keep and x not in remove]
    final = [x for x in candidate_ids if x in set(keep) or x in unmentioned]  # order 보존
    return {"ok": True, "keep": final, "removed": [x for x in candidate_ids if x not in final],
            "unmentioned_kept": unmentioned, "reason": obj.get("reason") or {}}


def prune_knowledge(needs: List[Dict[str, Any]], candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """candidates: [{id, kind(OK/KG), title, topics, need_ref}] — summaries only,
    Registry 원문은 프루닝 입력에 넣지 않는다(내용 재작성 여지 차단).
    Returns {"ok", "keep"(registry ids), "removed", "fallback_reason", "call"}."""
    need_lines = [f"- {n['need_id']}: [{n.get('purpose','')}] {n.get('need_text') or n.get('topic','')}"
                  for n in needs]
    cand_lines = [f"- {c['id']} [{c['kind']}] (need {c.get('need_ref','?')}) {c['title']} | topics: {c.get('topics','')}"
                  for c in candidates]
    prompt = (KNOWLEDGE_PRUNE_PROMPT
              + "\n\n## Knowledge Need\n" + "\n".join(need_lines)
              + "\n\n## 후보\n" + "\n".join(cand_lines))
    call = _call_and_parse(prompt)
    if call["obj"] is None:
        return {"ok": False, "fallback_reason": f"{call['status']}: {call['error'][:200]}", "call": call}
    res = _resolve_keep(call["obj"], "keep_ids", "remove_ids", [c["id"] for c in candidates])
    res["call"] = call
    return res


def prune_products(needs: List[Dict[str, Any]], candidates: List[Dict[str, Any]],
                   eligibility_note: str = "") -> Dict[str, Any]:
    """candidates: [{product_id, name, product_type, risk_grade, maturity_note,
    features_short, need_ref, eligibility}] — eligibility는 기존 C2 매핑의 재사용
    표시일 뿐 판정 책임은 runtime validator에 남는다."""
    need_lines = [f"- {n['need_id']}: {n.get('solution_type','')} (특성: {', '.join(n.get('characteristics', []))})"
                  for n in needs]
    cand_lines = []
    for c in candidates:
        g = c.get("risk_grade")
        cand_lines.append(
            f"- {c['product_id']} (need {c.get('need_ref','?')}) {c['name']} | 유형 {c['product_type']}"
            f" | 등급 {g if g is not None else '해당없음(원리금보장)'}"
            f"{' | ' + c['maturity_note'] if c.get('maturity_note') else ''}"
            f" | {c.get('eligibility','')}")
    prompt = (PRODUCT_PRUNE_PROMPT
              + ("\n\n" + eligibility_note if eligibility_note else "")
              + "\n\n## Product Need (조건/분기)\n" + "\n".join(need_lines)
              + "\n\n## 후보\n" + "\n".join(cand_lines))
    call = _call_and_parse(prompt)
    if call["obj"] is None:
        return {"ok": False, "fallback_reason": f"{call['status']}: {call['error'][:200]}", "call": call}
    res = _resolve_keep(call["obj"], "keep_product_ids", "remove_product_ids",
                        [c["product_id"] for c in candidates])
    res["call"] = call
    return res
