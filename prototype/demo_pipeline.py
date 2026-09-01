# -*- coding: utf-8 -*-
"""
Demo End-to-End Runner — design/DEMO_GOLDEN_CASE_DESIGN.md의 시연 Case 실행용.

mock_pipeline.py(Mock v0)와 동일한 파이프라인을 재사용하되,
Raw adapter를 거치지 않고 demo/cases/<CASE>/canonical.json을 직접 로드한다.

    demo/cases/<CASE>/canonical.json  (수기 작성 — supply에 HT/TALK/SCR 수동 동봉)
      → canonical.py Layer 1~3 (기존 검증·파생·렌더 그대로)
      → CALL 1  LLM Knowledge Need Generation
      → Hybrid Knowledge Selection (deterministic → LLM prune → gate)
      → CALL 2  LLM Management Judgment / Direction / Product Need
      → Hybrid Product Candidate Selection
      → CALL 3  Final Product Fit + Employee Brief (SYSTEM_ROLE_V3)
      → 기존 deterministic validators
      → demo/<CASE>_RUN.json / <CASE>_RUN.md

새 Framework 없음 — runtime/canonical/hybrid_selector/mock_pipeline 재사용.
Usage:  GEMINI_API_KEY=... python3 prototype/demo_pipeline.py DEMO-A [DEMO-B ...]
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runtime  # noqa: E402
import canonical as cx  # noqa: E402
import hybrid_selector as hy  # noqa: E402
import mock_pipeline as mp  # noqa: E402  (CALL1/CALL2 instruction·_llm_json·render_md 재사용)

DEMO_ROOT = Path(__file__).resolve().parent.parent / "demo"


def run_demo(case_id: str) -> Dict[str, Any]:
    calls: List[Dict[str, Any]] = []
    record: Dict[str, Any] = {"case_id": case_id, "pipeline": "DEMO_V0 (mock_pipeline 재사용)",
                              "started_at": _dt.datetime.now().isoformat(timespec="seconds"),
                              "model": runtime.MODEL_ID, "git_head": runtime._git_head()}

    # [0] canonical.json 직접 로드 (Raw adapter 없음)
    case = cx.load_canonical(case_id, root=DEMO_ROOT)
    derived = cx.derive(case)
    constraint = runtime.build_constraint_context(runtime._CanonicalTextShim(case))
    evidence_text = cx.render_blocks(case, derived)
    record["canonical_evidence"] = [vars(it) for it in case.evidence]
    record["derived_context"] = [vars(it) for it in derived]
    record["constraint"] = {"profile": constraint.investment_profile,
                            "allowed": constraint.allowed_levels,
                            "forbidden": constraint.forbidden_levels}

    # [1] CALL 1 — Knowledge Need Generation
    p1 = mp.CALL1_INSTRUCTION + "\n\n## Customer Evidence\n" + evidence_text
    call1 = mp._llm_json(p1, "CALL1_knowledge_need", calls)
    kn_raw = (call1 or {}).get("knowledge_needs") or []
    needs = []
    for i, kn in enumerate(kn_raw, 1):
        needs.append({"need_id": f"KN-D{i:02d}", "origin": "LLM-generated (Demo CALL1)",
                      "purpose": str(kn.get("purpose", "")),
                      "authority_required": "T1/T2",
                      "topics": [str(k) for k in (kn.get("keywords") or [])] + [str(kn.get("topic", ""))],
                      "need_text": str(kn.get("topic", ""))})
    record["knowledge_needs"] = needs

    # [2] Hybrid Knowledge Selection
    if needs:
        k_items, k_log = hy.select_knowledge_hybrid(case_id, needs=needs, manual_keep=[],
                                                    log_name=f"demo_hybrid_knowledge_{case_id}.json")
    else:
        k_items, k_log = [], {"note": "CALL1 실패 또는 need 없음 — Knowledge 없이 진행"}
    record["knowledge_selection"] = k_log
    knowledge_text = "\n\n".join(k.as_text() for k in k_items) if k_items else \
        "(선택된 Knowledge 없음 — Knowledge에 없는 제도 사실을 생성하지 않는다)"

    # [3] CALL 2 — Management Judgment / Direction / Product Need
    p2 = (mp.CALL2_INSTRUCTION + "\n\n## Customer Evidence\n" + evidence_text
          + "\n\n## 적용 Constraint\n" + constraint.as_text()
          + "\n\n## Knowledge\n" + knowledge_text)
    call2 = mp._llm_json(p2, "CALL2_management_decision", calls) or {}
    record["management_decision"] = call2

    # [4] Hybrid Product Candidate Selection
    pneed = (call2.get("product_need") or {})
    pool: List[Dict[str, Any]] = []
    if pneed.get("needed"):
        pneeds = []
        for i, st in enumerate(pneed.get("solution_types") or [], 1):
            pneeds.append({"need_id": f"PN-D{i:02d}",
                           "solution_type": str(st.get("solution_type", "")),
                           "characteristics": [str(c) for c in (st.get("characteristics") or [])],
                           "maturity": str(st.get("maturity", "") or ""),
                           "origin": "LLM-generated (Demo CALL2)"})
        pool, p_log = hy.build_pool_hybrid(case_id, needs=pneeds,
                                           investment_profile=constraint.investment_profile,
                                           log_name=f"demo_hybrid_product_{case_id}.json")
        record["product_selection"] = p_log
    else:
        record["product_selection"] = {"needed": False,
                                       "reason": pneed.get("reason", "CALL2가 상품 불필요로 판단")}
    case.supply["product_candidates"] = pool

    # [5] CALL 3 — Final Employee Brief
    call2_context = (
        "## 선행 관리판단 (앞 단계 결과 — Brief는 이 판단·방향과 일관되게 작성하되, "
        "미확인 사항의 조건성은 그대로 유지한다)\n"
        + json.dumps({k: call2.get(k) for k in ("management_judgment", "required_confirmation",
                                                "management_direction")}, ensure_ascii=False, indent=1))
    knowledge_ctx = knowledge_text
    supply_text = cx.render_supply(case)
    if supply_text:
        knowledge_ctx += "\n\n" + supply_text
    p3 = "\n\n".join([
        "## 역할과 원칙\n" + runtime.SYSTEM_ROLE_V3,
        "## 고객정보\n" + evidence_text,
        "## 적용 Constraint\n" + constraint.as_text(),
        "## Knowledge (판단 근거로 사용할 업무지식)\n" + knowledge_ctx,
        call2_context,
        "## 출력 형식\n" + runtime.OUTPUT_INSTRUCTION_V3,
    ])
    record["prompt_chars"] = {"call1": len(p1), "call2": len(p2), "call3": len(p3)}
    call3 = mp._llm_json(p3, "CALL3_final_brief", calls)

    # [6] deterministic validators (기존 그대로)
    if call3 is not None:
        obj = call3
        record["parsed_output"] = obj
        record["schema_errors"] = runtime.check_schema_v3(obj)
        record["validation"] = runtime.validate_c1(obj, constraint)
        record["validation_c3"] = runtime.validate_c3_default_option(obj, constraint)
        record["validation_c2"] = runtime.validate_c2_fund_grade(obj, constraint)
        record["validation_forbidden_words"] = runtime.validate_forbidden_words(obj)
        record["validation_latex"] = runtime.validate_latex_residue(obj)
        record["validation_evidence_ids"] = runtime.validate_evidence_ids(obj, cx.all_ids(case, derived))
        record["validation_supply_refs"] = runtime.validate_supply_refs(case, obj, constraint)
        record["validation_screen_refs"] = runtime.validate_screen_refs(case, obj)
        hard = ("validation", "validation_c3", "validation_c2", "validation_forbidden_words",
                "validation_evidence_ids", "validation_supply_refs", "validation_screen_refs")
        fails = [k for k in hard if record[k]["overall"] == "FAIL"]
        record["status"] = ("VALIDATION_ERROR" if fails else
                            ("SCHEMA_ERROR" if record["schema_errors"] else "SUCCESS"))
        record["error"] = "; ".join(fails)
    else:
        record["status"] = "CALL3_FAILED"

    record["llm_calls"] = [{k: v for k, v in c.items() if k != "raw_text"} for c in calls]
    prune_calls = 0
    for key in ("knowledge_selection", "product_selection"):
        lp = (record.get(key) or {}).get("llm_prune") or {}
        if lp.get("model_status"):
            prune_calls += 1
    record["llm_call_count"] = {"decision_level": len(calls), "selection_prune": prune_calls,
                                "total": len(calls) + prune_calls}

    (DEMO_ROOT / f"{case_id}_RUN.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    mp.render_md(record, DEMO_ROOT / f"{case_id}_RUN.md")
    return record


if __name__ == "__main__":
    ids = sys.argv[1:] or ["DEMO-A"]
    for cid in ids:
        rec = run_demo(cid)
        print(f"{cid}: status={rec.get('status')} calls={rec.get('llm_call_count')}")
        print(f"  records: demo/{cid}_RUN.json / .md")
