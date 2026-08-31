# -*- coding: utf-8 -*-
"""
Render a run record JSON (prototype/out/*.json) into a RUN_xxx.md artifact skeleton.

Execution-enabling tooling (HD-5.1): it only transcribes the record verbatim into
the RUN template sections; it adds no judgment. The caller fills Run ID / Parent /
Applied Change via CLI args. Output is written to stdout or --out.

    python prototype/render_run.py prototype/out/GC-01_....json --run-id RUN_001 --out cases/GC-01/runs/RUN_001.md
"""
import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _git_commit_of(path: str) -> str:
    try:
        return subprocess.check_output(["git", "log", "-1", "--format=%H", "--", path], cwd=str(REPO), text=True).strip()
    except Exception:
        return ""


def render(rec: dict, run_id: str, parent: str, applied: str, raw_rel: str) -> str:
    L = []
    a = L.append
    case = rec["case_id"]
    a(f"# {run_id}\n")
    a("## 1. Run Metadata\n")
    a(f"- Case: {case}")
    a(f"- Run ID: {run_id}")
    a(f"- Parent Run: {parent}")
    a(f"- Target Model: {rec['model']}")
    a(f"- Endpoint: {rec['endpoint']}")
    a(f"- Runtime Commit: {rec.get('git_head','')} (prototype/runtime.py at execution; revision {rec.get('runtime_revision','pre-REV-001')})")
    if rec.get("frozen_input_v2"):
        iv = rec["frozen_input_v2"]
        a(f"- Input Baseline: {iv.get('file','')} sha256 {iv.get('sha256','')} (REV-002 Evidence Pack)")
    else:
        fc = rec.get("frozen_case", {})
        a(f"- Case Baseline: cases/{case}/case.md sha256 {fc.get('sha256','')} (Status {fc.get('Status','')}, Frozen At {fc.get('Frozen At','')}, Approved By {fc.get('Approved By','')})")
    kp = rec.get("frozen_knowledge_pack", {})
    a(f"- Knowledge Pack: {kp.get('knowledge_pack','')} sha256 {kp.get('knowledge_pack_sha256','')}")
    a(f"- Generation Config: {'API Default' if rec.get('generation_config') is None else rec['generation_config']}")
    a(f"- Executed At: {rec['started_at']}")
    a(f"- Applied Change: {applied}")
    a(f"- Runtime Status: {rec['status']}" + (f" — {rec['error']}" if rec.get('error') else ""))
    a("- Model Call Count: 1")
    a(f"- Raw Runtime Record: {raw_rel} (local, git-ignored)\n")
    a("---\n")
    a("## 2. Customer Input\n")
    if rec.get("frozen_input_v2"):
        a("Runtime이 실제로 사용한 입력 (input_v2.md Evidence Pack 직렬화 원문 — Evidence ID·Calculated Facts 포함).\n")
        a("```text")
        a(rec.get("prompt", {}).get("customer_context", ""))
        a("```\n")
    else:
        a("Runtime이 실제로 사용한 입력 (case.md §2 bullet 원문).\n")
        a("```text")
        L.extend(rec.get("customer_input", []))
        a("```\n")
    a("---\n")
    po = rec.get("parsed_output") or {}
    a("## 3. Interpreted Context\n")
    a("모델 출력 원문 그대로. 보정하지 않는다.\n")
    a("### Current Situation (`current_situation`)\n")
    a(str(po.get("current_situation", "(없음)")) + "\n")
    a("### Confirmed (`known_facts_used`)\n")
    for x in po.get("known_facts_used") or []:
        a(f"- {x}")
    a("")
    a("### Unknown (`unknowns_or_confirmations`)\n")
    for x in po.get("unknowns_or_confirmations") or []:
        a(f"- {x}")
    a("\n---\n")
    cc = rec.get("constraint_context", {})
    a("## 4. Applied Constraints\n")
    a("### C1 투자성향 Hard Constraint / C3 디폴트옵션 Eligibility (Pre-Reasoning Context로 전달)\n")
    a(f"- Customer Profile: {cc.get('investment_profile')}")
    a(f"- Allowed Levels: {', '.join(cc.get('allowed_levels', []))}")
    a(f"- Forbidden Levels: {', '.join(cc.get('forbidden_levels', []))}")
    a(f"- Basis: {cc.get('basis')}")
    v3 = rec.get("validation_c3", {})
    a(f"- C3 Ineligible Portfolios: {', '.join(v3.get('ineligible_portfolios', [])) or '없음'}")
    v2 = rec.get("validation_c2", {})
    if v2:
        a(f"- C2 Ineligible Fund Grades: {', '.join(v2.get('ineligible_labels', [])) or '없음'} (allowed grade ≥ {v2.get('allowed_min_grade')})")
    a("- Pre-Reasoning Context 적용: YES (prompt `constraint_context` section)")
    a("- Post-Validation: §8\n")
    a("---\n")
    a("## 5. Used Knowledge\n")
    a(f"Context에 전달된 K-ID: {', '.join(rec.get('knowledge_ids_used', []))} (전달 필드: {', '.join(rec.get('knowledge_fields_sent', []))})\n")
    a(f"모델이 근거로 밝힌 K-ID (`knowledge_ids_used`): {', '.join(po.get('knowledge_ids_used') or []) or '(없음)'}\n")
    a("---\n")
    a("## 6. Decision Output\n")
    a("모델 원문 그대로.\n")
    if "management_judgment" in po:
        mj = po.get("management_judgment") or {}
        a(f"- Management Judgment — judgment: {mj.get('judgment','')}  (detected types: {', '.join(rec.get('judgment_types_detected') or []) or '없음'})")
        a(f"- Management Judgment — reasoning: {mj.get('reasoning','')}")
        a("- Must confirm before action:")
        for x in mj.get("must_confirm_before_action") or []:
            a(f"  - {x}")
        if mj.get("supporting_evidence_ids"):
            a(f"- Supporting Evidence IDs: {', '.join(mj['supporting_evidence_ids'])}")
        a("")
    else:
        mn = po.get("management_need") or {}
        a(f"- Management Need — decision: {mn.get('decision','')}")
        a(f"- Management Need — reason: {mn.get('reason','')}\n")
    a("---\n")
    v1 = rec.get("validation", {})
    verdicts = {c["index"]: c["verdict"] for c in v1.get("candidates", [])}
    if "next_actions" in po:
        a("## 7. Next Actions\n")
        for i, c in enumerate(po.get("next_actions") or []):
            a(f"### Action {i+1}\n")
            a(f"- Action: {c.get('action','')}")
            a(f"- Kind: {c.get('kind','')}")
            a(f"- Condition: {c.get('condition','')}")
            a(f"- Risk Level: {c.get('risk_level','')}")
            if c.get("supporting_evidence_ids"):
                a(f"- Supporting Evidence IDs: {', '.join(c['supporting_evidence_ids'])}")
            a(f"- C1 Check: {verdicts.get(i,'')}\n")
    else:
        a("## 7. Solution Candidates\n")
        for i, c in enumerate(po.get("solution_candidates") or []):
            a(f"### Candidate {i+1}\n")
            a(f"- Direction: {c.get('direction','')}")
            a(f"- Condition: {c.get('condition','')}")
            a(f"- Risk Level: {c.get('risk_level','')}")
            a(f"- C1 Check: {verdicts.get(i,'')}\n")
    a("---\n")
    a("## 8. Validation\n")
    a(f"- C1 (투자성향 상한): {v1.get('overall')} — {len(v1.get('candidates', []))} candidates; verdicts: {', '.join(c['verdict'] for c in v1.get('candidates', []))}")
    a(f"- C3 (디폴트옵션 Eligibility): {v3.get('overall')} — findings: {json.dumps(v3.get('findings', []), ensure_ascii=False)}")
    v2 = rec.get("validation_c2") or rec.get("validation_c2_detect") or {}
    a(f"- C2 (펀드 위험등급 Eligibility): {v2.get('overall', v2.get('mode'))} — findings: {json.dumps(v2.get('findings', []), ensure_ascii=False)}")
    for key, label in (("validation_forbidden_words", "금지어 (deterministic)"),
                       ("validation_latex", "LaTeX 잔재 (deterministic)"),
                       ("validation_evidence_ids", "Evidence ID Provenance (deterministic)"),
                       ("validation_screen_survival", "화면번호 생존 (deterministic)"),
                       ("validation_candidate_pool", "Candidate Pool (deterministic)")):
        v = rec.get(key)
        if v:
            detail = v.get("findings", v.get("missing_from_output", []))
            a(f"- {label}: {v.get('overall')} — {json.dumps(detail, ensure_ascii=False)}")
    a("- Execution Feasibility: (Runtime 미구현 — 검사하지 않음)")
    a("- Solution Conflict: (Runtime 미구현 — 검사하지 않음)")
    a(f"- Required Confirmation: 모델 출력 `unknowns_or_confirmations` {len(po.get('unknowns_or_confirmations') or [])}건 (§3)")
    a(f"- Schema Check: {'OK' if not rec.get('schema_errors') else rec.get('schema_errors')}\n")
    a("---\n")
    a("## 9. Final Output\n")
    eb = po.get("employee_brief", "")
    if isinstance(eb, dict):
        a("Employee Brief (5-섹션, 모델 원문 그대로):\n")
        a("### S1 고객 상황\n")
        a(str(eb.get("s1_customer_situation", "")) + "\n")
        s2 = eb.get("s2_management_point") or {}
        a("### S2 핵심 관리 포인트\n")
        a(f"- Point: {s2.get('point','')}")
        a(f"- Rationale: {s2.get('rationale','')}")
        a("- 먼저 확인하세요:")
        for cf in s2.get("confirm_first") or []:
            a(f"  - [{cf.get('who','')}] {cf.get('item','')}")
        a("")
        s3 = eb.get("s3_direction") or {}
        a("### S3 추천 운용 방향\n")
        if s3.get("not_applicable"):
            na_ = s3["not_applicable"]
            a(f"- 비해당: {na_.get('type','')} — {na_.get('reason','')}")
        for d in s3.get("directions") or []:
            cond = d.get("condition", "")
            prefix = f"[{cond}] → " if cond else ""
            a(f"- {prefix}{d.get('content','')} (Risk: {d.get('risk_level','')})")
        a("")
        s4 = eb.get("s4_consult_points") or {}
        a("### S4 상담 Point\n")
        for x in s4.get("sequence") or []:
            a(f"- {x}")
        a("- 화법:")
        for x in s4.get("scripts") or []:
            a(f"  - {x}")
        a("")
        a("### S5 관련 TIP & GUIDE\n")
        for t in eb.get("s5_tips") or []:
            src = f" (출처: {t.get('source','')}" + (f", as-of {t['as_of']}" if t.get("as_of") else "") + ")" if t.get("source") or t.get("as_of") else ""
            a(f"- {t.get('content','')}{src}")
        a("")
    else:
        a("Employee Brief (`employee_brief`, 원문):\n")
        a("> " + str(eb).replace("\n", "\n> ") + "\n")
    a("---\n")
    mr = rec.get("model_response", {})
    a("## 10. Raw / Technical Observation\n")
    a(f"- HTTP status: {mr.get('http_status')}")
    a(f"- Finish reason: {mr.get('finish_reason')}")
    u = mr.get("usage", {})
    a(f"- Token usage: prompt {u.get('promptTokenCount')}, candidates {u.get('candidatesTokenCount')}, thoughts {u.get('thoughtsTokenCount')} (count only), total {u.get('totalTokenCount')}")
    a(f"- Prompt size: {rec.get('prompt_chars')} chars")
    a(f"- JSON parse normalization: {rec.get('json_normalizations') or 'none'}")
    a("- Credential: not recorded anywhere\n")
    a("> 이 Artifact는 생성 후 수정하지 않는다. 수정된 Runtime은 새로운 RUN을 생성한다.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("record")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--parent", default="none")
    ap.add_argument("--applied", default="none")
    ap.add_argument("--out")
    a = ap.parse_args()
    rec = json.loads(Path(a.record).read_text(encoding="utf-8"))
    raw_rel = str(Path(a.record).resolve().relative_to(REPO)) if str(Path(a.record).resolve()).startswith(str(REPO)) else a.record
    md = render(rec, a.run_id, a.parent, a.applied, raw_rel)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(md, encoding="utf-8")
        print(a.out)
    else:
        print(md)


if __name__ == "__main__":
    main()
