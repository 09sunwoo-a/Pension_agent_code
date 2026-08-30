# -*- coding: utf-8 -*-
"""
CLI for the minimal Pension Agent prototype.

    python prototype/run_case.py CASE_001               # live call to gemma-4-31b-it
    python prototype/run_case.py CASE_001 --dry-run     # build & show prompt, no API call
    python prototype/run_case.py CASE_001 --out path.json

Requires GEMINI_API_KEY in the environment for a live run. The key is never
printed or written to the output file.
"""
import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runtime  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent / "out"


def main() -> int:
    ap = argparse.ArgumentParser(description="Run one Frozen Case against the Target Base LLM.")
    ap.add_argument("case_id", help="e.g. CASE_001")
    ap.add_argument("--dry-run", action="store_true", help="build the prompt only; do not call the API")
    ap.add_argument("--out", help="write the run record JSON to this path (default: prototype/out/<case>_<ts>.json)")
    ap.add_argument("--show-prompt", action="store_true", help="print the full prompt text")
    args = ap.parse_args()

    record = runtime.run_case(args.case_id, dry_run=args.dry_run)

    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = Path(args.out) if args.out else OUT_DIR / f"{args.case_id}_{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"case        : {record['case_id']}")
    print(f"model       : {record['model']}")
    print(f"status      : {record['status']}")
    if record.get("error"):
        print(f"error       : {record['error'][:500]}")
    if "constraint_context" in record:
        cc = record["constraint_context"]
        print(f"C1          : {cc['investment_profile']} → allowed {cc['allowed_levels']} / forbidden {cc['forbidden_levels']}")
        print(f"knowledge   : {', '.join(record['knowledge_ids_used'])}  (fields: {', '.join(record['knowledge_fields_sent'])})")
        print(f"prompt size : {record['prompt_chars']} chars")
    if args.show_prompt and "prompt" in record:
        p = record["prompt"]
        print("\n" + "=" * 30 + " PROMPT " + "=" * 30)
        print("\n\n".join([p["system_role"], p["customer_context"], p["constraint_context"], p["knowledge_context"], p["output_instruction"]]))
        print("=" * 68)
    mr = record.get("model_response")
    if mr:
        print(f"api         : {mr['status']} http={mr['http_status']} finish={mr['finish_reason']} usage={mr.get('usage')}")
    if "json_normalizations" in record:
        print(f"json norm   : {record['json_normalizations'] or 'none'}")
    if record.get("schema_errors"):
        print(f"schema      : {record['schema_errors']}")
    v = record.get("validation")
    if v:
        print(f"validation  : C1 {v['overall']}")
        for c in v["candidates"]:
            print(f"   [{c['index']}] {c['verdict']:12s} risk_level={c['risk_level']!r}  direction={str(c['direction'])[:70]!r}")
    v3 = record.get("validation_c3")
    if v3:
        print(f"validation  : C3 {v3['overall']}  (ineligible: {v3['ineligible_portfolios']}; findings: {len(v3['findings'])})")
    v2 = record.get("validation_c2_detect")
    if v2 and v2["findings"]:
        print(f"C2 detect   : {v2['findings']}")
    po = record.get("parsed_output")
    if po:
        mn = po.get("management_need", {})
        print(f"\nmanagement_need.decision: {mn.get('decision')}")
        print(f"unknowns_or_confirmations: {len(po.get('unknowns_or_confirmations') or [])} items")
        print(f"knowledge_ids_used (model): {po.get('knowledge_ids_used')}")
        print(f"\nemployee_brief:\n{po.get('employee_brief')}")
    print(f"\nrun record  : {out_path}")
    return 0 if record["status"] in (runtime.SUCCESS, "DRY_RUN") else 1


if __name__ == "__main__":
    sys.exit(main())
