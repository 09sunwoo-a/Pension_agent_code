# -*- coding: utf-8 -*-
"""
Minimal End-to-End Mock v0 — 단일 Raw Customer JSON에서 Final Brief까지.

    Raw Mock JSON (prototype/mock/MOCK_001_raw.json)
      → [adapter] Canonical Evidence (기존 canonical.py 계약·검증 그대로)
      → derive() 결정론 파생 / build_constraint_context() Hard Constraint
      → CALL 1  LLM Knowledge Need Generation   (Human-defined Need 최초 제거)
      → Hybrid Knowledge Selection              (deterministic → LLM prune → gate)
      → CALL 2  LLM Management Judgment / Direction / Product Need
      → Hybrid Product Candidate Selection      (deterministic → eligibility 표시 → prune)
      → CALL 3  Final Product Fit + Employee Brief (기존 SYSTEM_ROLE_V3 / OUTPUT_INSTRUCTION_V3)
      → 기존 deterministic validators
      → prototype/mock/MOCK_001_RUN.json / MOCK_001_RUN.md

새 Framework 없음 — runtime/canonical/selector/hybrid_selector 재사용.
HT/TALK/SCR 자동 Selection 없음(supply에 최소 화면만 수동 연결, tips 없음).
Usage:  GEMINI_API_KEY=... python3 prototype/mock_pipeline.py [MOCK_001]
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runtime  # noqa: E402
import canonical as cx  # noqa: E402
import hybrid_selector as hy  # noqa: E402

MOCK_ROOT = Path(__file__).resolve().parent / "mock"


# ---------------------------------------------------------------------------
# Raw → Canonical adapter (deterministic — 의미 라벨 생성 금지)
# ---------------------------------------------------------------------------
def build_canonical(raw: Dict[str, Any]) -> Dict[str, Any]:
    ev: List[Dict[str, Any]] = []
    n = 0

    def add(block: int, etype: str, stype: str, text: str,
            as_of: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
        nonlocal n
        n += 1
        item: Dict[str, Any] = {"id": f"E{n:03d}", "block": block, "evidence_type": etype,
                                "source_type": stype, "text": text}
        if as_of:
            item["as_of"] = as_of
        if data:
            item["data"] = data
        ev.append(item)

    c = raw["customer"]
    base = raw["base_date"]
    add(1, "fact", "account_system", f"고객 연령: 만 {c['age']}세", base, {"kind": "age", "years": c["age"]})
    add(1, "fact", "account_system", f"개인형IRP 가입일: {c['irp_join_date']}", base,
        {"kind": "join_date", "date": c["irp_join_date"]})
    add(1, "fact", "account_system",
        f"퇴직급여 포함 여부: {'포함' if c['retirement_benefit_included'] else '미포함'}", base,
        {"kind": "retirement_benefit", "included": c["retirement_benefit_included"]})
    add(1, "fact", "account_system",
        f"투자성향: {c['investment_profile']} (분석일 {c['profile_analyzed_at']}, 유효)", base)
    add(1, "fact", "account_system",
        f"재직 상태: {c['employment']} / 스타뱅킹 이용: {'Y' if c['starbanking_user'] else 'N'}", base)

    a = raw["irp_account"]
    add(2, "fact", "account_system",
        f"IRP 평가금액: {a['balance_total']:,}원 (현금성자산 {a['balance_cash']:,}원 포함)", a["as_of"],
        {"kind": "current_balance", "cash": a["balance_cash"], "total": a["balance_total"]})
    for h in a["holdings"]:
        txt = f"보유상품: {h['name']} {h['amount']:,}원"
        data = None
        if h.get("maturity"):
            txt += f" (만기 {h['maturity']}"
            if h.get("rate_note"):
                txt += f", {h['rate_note']}"
            txt += ")"
            data = {"kind": "maturity", "date": h["maturity"], "amount": h["amount"], "product": h["name"]}
        add(2, "fact", "account_system", txt, a["as_of"], data)
    add(2, "fact", "account_system",
        f"디폴트옵션 등록 여부: {'등록' if a['do_registration']['registered'] else '미등록'}", a["as_of"],
        {"kind": "do_registration", "registered": a["do_registration"]["registered"]})
    add(2, "fact", "account_system",
        f"당해년도 IRP 개인부담금 실납입액(irp_personal_contribution_ytd): {a['irp_personal_contribution_ytd']:,}원",
        a["as_of"])

    s = raw["balance_snapshot_30d"]
    add(3, "fact", "account_system",
        f"{s['date']} 기준 잔액 스냅샷: 현금성자산 {s['cash']:,}원 / 전체 평가금액 {s['total']:,}원",
        s["date"], {"kind": "balance_snapshot", "date": s["date"], "cash": s["cash"], "total": s["total"]})

    for t in raw["transactions"]:
        add(4, "fact", "transaction",
            f"{t['date']} {t['kind']} {t['amount']:,}원 (사유: {t['reason']})", t["date"],
            {"kind": "deposit", "date": t["date"], "amount": t["amount"], "reason": t["reason"]})

    for t in raw["trades_12m"]:
        add(5, "fact", "transaction", f"최근 1년 매매: {t['date']} {t['action']}", t["date"])

    for b in raw["digital_behavior"]:
        add(6, "signal", "digital_behavior",
            f"{b['date']} {b['action']} (실행 이력 {'있음' if b.get('executed') else '없음'})", b["date"],
            {"kind": "behavior_event", "date": b["date"], "action": b["action"],
             "executed": bool(b.get("executed"))})

    w = raw["wider_context"]
    add(7, "fact", "external_account", f"총 금융자산: {w['total_financial_assets']:,}원", base)
    add(7, "fact", "external_account", f"타 연금계좌: {w['other_pension_accounts']}", base)

    # block 8은 파생(만기 D-n)으로 채워짐, block 9는 CRM 없음(비움)
    supply = {
        "product_candidates": [],   # Hybrid Product Selection이 런타임에 구성
        "hot_tips": [],             # Mock v0: HT/TALK 자동 Selection 없음
        "screens": [                # SCR 수동 최소 연결 (SCR-001·SCR-009 근거)
            {"screen_id": "S01", "surface": "staff", "screen_no": "[04-12-642]",
             "screen_name": "적립금및수익률조회", "actions": "보유상품·평가금액/수익률 확인 및 운용현황 점검"},
            {"screen_id": "S02", "surface": "starbanking",
             "menu_path": "전체메뉴 > 가입상품관리 > 퇴직연금 > 변경관리 > 보유상품변경",
             "actions": "고객이 직접 운용상품 변경/매수 실행"},
        ],
    }
    return {"case_id": raw["case_id"], "base_date": base, "evidence": ev, "supply": supply}


# ---------------------------------------------------------------------------
# CALL 1 — Knowledge Need Generation (판단·추천·화법 금지)
# ---------------------------------------------------------------------------
CALL1_INSTRUCTION = """당신은 은행 퇴직연금 사후관리 파이프라인의 Knowledge Need 생성기다.

아래 Customer Evidence(9-Block)와 파생 사실만 보고, 이 고객의 상태를 판단하기 위해
어떤 제도·업무 Knowledge가 필요한지(Knowledge Need)만 생성한다.

금지:
- Management Judgment(관리판단)를 내리지 않는다.
- 상품을 추천하거나 상품 필요 여부를 판단하지 않는다.
- 상담 화법을 만들지 않는다.
- 고객 상태에 의미 라벨(방치·운용 필요 등)을 붙이지 않는다.

각 Need는 제도/절차/세제/시한/실행경로 확인 목적이어야 하며 2~5개로 제한한다.
keywords는 행내 Knowledge Registry 검색용 명사 키워드다 (각 2~8자, 3~6개).

다음 JSON 객체 하나만 출력한다 (다른 텍스트 금지):
{"knowledge_needs": [{"purpose": "rule_confirmation 등 한 단어", "topic": "필요한 Knowledge 한 줄", "keywords": ["키워드", "..."]}]}"""


# ---------------------------------------------------------------------------
# CALL 2 — Management Judgment / Direction / Product Need
# ---------------------------------------------------------------------------
CALL2_INSTRUCTION = """당신은 은행 직원의 개인형IRP 사후관리 판단을 지원하는 의사결정 지원 Agent다.
아래 Evidence·Constraint·Knowledge만 근거로 이 고객에 대한 관리판단을 구조화한다.
(SYSTEM 원칙: 추론과 사실 구분 / Signal은 의사가 아님 / 어느 방향도 기본값 아님 /
Knowledge·Evidence에 없는 제도 사실·수치 생성 금지 / 확인 전 분기 확정 금지 /
은행의 영업 목적을 관리 필요성의 근거로 쓰지 않는다.)

이 단계에서는 상담 화법과 최종 상품 추천을 만들지 않는다.
product_need는 "어떤 유형의 상품 재료가 검토에 필요한가"까지만 정의한다 —
characteristics는 상품 자체의 intrinsic 특성(TDF/채권형/정기예금/GIC 등 유형 키워드)만 쓰고
고객 상황 라벨을 쓰지 않는다. 상품이 불필요하면 needed=false.

다음 JSON 객체 하나만 출력한다 (다른 텍스트 금지):
{
  "customer_state_interpretation": "사실/추론 구분한 현재 상태 해석",
  "management_judgment": {"judgment": "개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가 중 하나 이상 '/'구분", "reasoning": "근거 (Evidence ID 인용)"},
  "required_confirmation": ["확인 필요 사항"],
  "management_direction": {"directions": [{"condition": "전제 (무조건이면 빈 문자열)", "direction": "관리 방향"}]},
  "product_need": {"needed": true, "solution_types": [{"solution_type": "이 상품 재료가 지원하는 방향/분기", "characteristics": ["유형 키워드"], "maturity": ""}]}
}"""


def _llm_json(prompt: str, purpose: str, calls: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    resp = runtime.call_gemma(prompt)
    rec = {"purpose": purpose, "status": resp.status, "usage": resp.usage,
           "finish_reason": resp.finish_reason, "error": resp.error, "raw_text": resp.text}
    calls.append(rec)
    if resp.status != runtime.SUCCESS:
        return None
    obj, _, perr = runtime.parse_model_json(resp.text)
    if obj is None:
        rec["status"] = "PARSE_ERROR"
        rec["error"] = perr
    rec["parsed"] = obj
    return obj


def run_mock(case_id: str = "MOCK_001") -> Dict[str, Any]:
    calls: List[Dict[str, Any]] = []   # 모든 API call을 숨기지 않고 기록
    record: Dict[str, Any] = {"case_id": case_id, "pipeline": "MOCK_V0",
                              "started_at": _dt.datetime.now().isoformat(timespec="seconds"),
                              "model": runtime.MODEL_ID, "git_head": runtime._git_head()}

    # [0] Raw → Canonical (adapter) → 기존 Layer 1~3
    raw = json.loads((MOCK_ROOT / f"{case_id}_raw.json").read_text(encoding="utf-8"))
    record["raw_input"] = raw
    canonical_obj = build_canonical(raw)
    case_dir = MOCK_ROOT / "cases" / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "canonical.json").write_text(
        json.dumps(canonical_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    case = cx.load_canonical(case_id, root=MOCK_ROOT)   # 기존 검증 그대로 통과해야 함
    derived = cx.derive(case)
    constraint = runtime.build_constraint_context(runtime._CanonicalTextShim(case))
    evidence_text = cx.render_blocks(case, derived)
    record["canonical_evidence"] = [vars(it) for it in case.evidence]
    record["derived_context"] = [vars(it) for it in derived]
    record["constraint"] = {"profile": constraint.investment_profile,
                            "allowed": constraint.allowed_levels,
                            "forbidden": constraint.forbidden_levels}

    # [1] CALL 1 — Knowledge Need Generation
    p1 = CALL1_INSTRUCTION + "\n\n## Customer Evidence\n" + evidence_text
    call1 = _llm_json(p1, "CALL1_knowledge_need", calls)
    kn_raw = (call1 or {}).get("knowledge_needs") or []
    needs = []
    for i, kn in enumerate(kn_raw, 1):
        needs.append({"need_id": f"KN-M{i:02d}", "origin": "LLM-generated (Mock CALL1)",
                      "purpose": str(kn.get("purpose", "")),
                      "authority_required": "T1/T2",   # 제도류 기본 gate — LLM이 Trust를 정하지 않는다
                      "topics": [str(k) for k in (kn.get("keywords") or [])] + [str(kn.get("topic", ""))],
                      "need_text": str(kn.get("topic", ""))})
    record["knowledge_needs"] = needs

    # [2] Hybrid Knowledge Selection (deterministic retrieval → LLM prune → gate)
    if needs:
        k_items, k_log = hy.select_knowledge_hybrid(case_id, needs=needs, manual_keep=[],
                                                    log_name=f"mock_hybrid_knowledge_{case_id}.json")
    else:
        k_items, k_log = [], {"note": "CALL1 실패 또는 need 없음 — Knowledge 없이 진행"}
    record["knowledge_selection"] = k_log
    knowledge_text = "\n\n".join(k.as_text() for k in k_items) if k_items else \
        "(선택된 Knowledge 없음 — Knowledge에 없는 제도 사실을 생성하지 않는다)"

    # [3] CALL 2 — Management Judgment / Direction / Product Need
    p2 = (CALL2_INSTRUCTION + "\n\n## Customer Evidence\n" + evidence_text
          + "\n\n## 적용 Constraint\n" + constraint.as_text()
          + "\n\n## Knowledge\n" + knowledge_text)
    call2 = _llm_json(p2, "CALL2_management_decision", calls) or {}
    record["management_decision"] = call2

    # [4] Hybrid Product Candidate Selection (Product Need → PRD → eligibility → prune)
    pneed = (call2.get("product_need") or {})
    pool: List[Dict[str, Any]] = []
    if pneed.get("needed"):
        pneeds = []
        for i, st in enumerate(pneed.get("solution_types") or [], 1):
            pneeds.append({"need_id": f"PN-M{i:02d}",
                           "solution_type": str(st.get("solution_type", "")),
                           "characteristics": [str(c) for c in (st.get("characteristics") or [])],
                           "maturity": str(st.get("maturity", "") or ""),
                           "origin": "LLM-generated (Mock CALL2)"})
        pool, p_log = hy.build_pool_hybrid(case_id, needs=pneeds,
                                           investment_profile=constraint.investment_profile,
                                           log_name=f"mock_hybrid_product_{case_id}.json")
        record["product_selection"] = p_log
    else:
        record["product_selection"] = {"needed": False,
                                       "reason": pneed.get("reason", "CALL2가 상품 불필요로 판단")}
    case.supply["product_candidates"] = pool

    # [5] CALL 3 — Final Product Fit + Employee Brief (기존 v3 계약 그대로)
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
    call3 = _llm_json(p3, "CALL3_final_brief", calls)

    # [6] 기존 deterministic validators
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
    record["llm_call_count"] = {"decision_level": 3,
                                "selection_prune": sum(1 for c in calls if False)  # prune calls는 hybrid log에 기록
                                }
    # prune call 수는 hybrid log에서 집계
    prune_calls = 0
    for key in ("knowledge_selection", "product_selection"):
        lp = (record.get(key) or {}).get("llm_prune") or {}
        if lp.get("model_status"):
            prune_calls += 1
    record["llm_call_count"] = {"decision_level": len(calls), "selection_prune": prune_calls,
                                "total": len(calls) + prune_calls}

    (MOCK_ROOT / f"{case_id}_RUN.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    render_md(record, MOCK_ROOT / f"{case_id}_RUN.md")
    return record


def render_md(r: Dict[str, Any], path: Path) -> None:
    L: List[str] = [f"# {r['case_id']} — Minimal End-to-End Mock v0 RUN", ""]
    L.append(f"- 실행: {r['started_at']} / model {r['model']} / git {r['git_head'][:9]} / status **{r.get('status')}**")
    cc = r.get("llm_call_count", {})
    L.append(f"- LLM Call: decision-level {cc.get('decision_level')} + selection prune {cc.get('selection_prune')} = 총 {cc.get('total')}")
    L.append("")
    L.append("## 1. Raw Input → Canonical Evidence")
    L.append(f"- Raw: `prototype/mock/{r['case_id']}_raw.json` (합성 고객 — 의미 라벨 없음)")
    L.append(f"- Canonical: E-item {len(r['canonical_evidence'])}건 / Derived {len(r['derived_context'])}건 (기존 canonical.py 검증 통과)")
    for it in r["derived_context"]:
        L.append(f"  - [{it['id']}] {it['text']}")
    c = r["constraint"]
    L.append(f"- Hard Constraint: 투자성향 {c['profile']} → 허용 {c['allowed']} / 금지 {c['forbidden']}")
    L.append("")
    L.append("## 2. CALL 1 — LLM Knowledge Need Generation")
    for nd in r["knowledge_needs"]:
        L.append(f"- {nd['need_id']} [{nd['purpose']}] {nd['need_text']} (keywords: {', '.join(nd['topics'][:-1])})")
    L.append("")
    L.append("## 3. Hybrid Knowledge Selection")
    ks = r.get("knowledge_selection", {})
    L.append(f"- deterministic 후보: {ks.get('deterministic_candidates')}")
    lp = ks.get("llm_prune") or {}
    L.append(f"- LLM prune: keep {lp.get('keep')} / removed {lp.get('removed')} / fallback {ks.get('fallback')}")
    for s in ks.get("final_selected") or []:
        L.append(f"- 최종 {s['kid']} [{s['kind']}] {s['registry_ref']} (need {s['need_ref']})")
    L.append("")
    L.append("## 4. CALL 2 — Management Judgment / Direction / Product Need")
    md = r.get("management_decision", {})
    mj = md.get("management_judgment") or {}
    L.append(f"- judgment: **{mj.get('judgment')}**")
    L.append(f"- reasoning: {str(mj.get('reasoning'))[:400]}")
    L.append(f"- required_confirmation: {md.get('required_confirmation')}")
    for d in (md.get("management_direction") or {}).get("directions") or []:
        L.append(f"- direction: [{d.get('condition','')}] → {d.get('direction','')}")
    L.append(f"- product_need: {json.dumps(md.get('product_need'), ensure_ascii=False)[:400]}")
    L.append("")
    L.append("## 5. Hybrid Product Candidate Selection")
    ps = r.get("product_selection", {})
    if ps.get("needed") is False:
        L.append(f"- 상품 불필요 (CALL2) — 빈 Pool 정상: {ps.get('reason')}")
    else:
        L.append(f"- deterministic pool: {ps.get('deterministic_pool')}")
        plp = ps.get("llm_prune") or {}
        L.append(f"- LLM prune keep: {plp.get('keep')} / removed {plp.get('removed')} / fallback {ps.get('fallback')}")
        L.append(f"- 최종 Pool: {ps.get('final_pool')}")
    L.append("")
    L.append("## 6. CALL 3 — Final Employee Brief (S1~S5)")
    obj = r.get("parsed_output") or {}
    eb = obj.get("employee_brief") or {}
    if eb:
        L.append(f"### S1\n{eb.get('s1_customer_situation','')}")
        s2 = eb.get("s2_management_point") or {}
        L.append(f"### S2\n{s2.get('point','')}")
        L.append(f"- 상담 전 확인: {s2.get('check_before_consult')}")
        L.append(f"- 고객과 확인: {s2.get('check_with_customer')}")
        L.append("### S3")
        for d in (eb.get("s3_direction") or {}).get("directions") or []:
            L.append(f"- [{d.get('condition','')}] {d.get('direction','')} / {d.get('solution_type','')} (risk: {d.get('risk_level','')})")
        for p in (eb.get("s3_direction") or {}).get("product_candidates") or []:
            L.append(f"- 후보 {p.get('product_id')}: {'; '.join(p.get('reasons') or [])[:200]}")
        L.append("### S4")
        for sc in (eb.get("s4_consult_script") or {}).get("scripts") or []:
            L.append(f"> {sc}")
        for cs in (eb.get("s4_consult_script") or {}).get("conditional_scripts") or []:
            L.append(f"> [if {cs.get('if','')}] {cs.get('script','')}")
        L.append("### S5")
        s5 = eb.get("s5_tips_and_screens") or {}
        L.append(f"- tips: {s5.get('tips')} / screens: {s5.get('screens')}")
    L.append("")
    L.append("## 7. Validators")
    for k in ("schema_errors", "validation", "validation_c2", "validation_c3",
              "validation_forbidden_words", "validation_evidence_ids",
              "validation_supply_refs", "validation_screen_refs", "validation_latex"):
        v = r.get(k)
        if isinstance(v, dict):
            L.append(f"- {k}: {v.get('overall')}" + (f" {v.get('findings')}" if v.get("findings") else ""))
        else:
            L.append(f"- {k}: {v if v else 'PASS(없음)'}")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    runtime.force_utf8_stdio()  # Windows cp949 콘솔에서 한글 출력 깨짐 방지
    cid = sys.argv[1] if len(sys.argv) > 1 else "MOCK_001"
    rec = run_mock(cid)
    print(f"status: {rec.get('status')} | calls: {rec.get('llm_call_count')}")
    print(f"records: prototype/mock/{cid}_RUN.json / .md")
