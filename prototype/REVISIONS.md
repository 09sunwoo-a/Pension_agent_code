# Runtime Revisions (Semantic — Human-approved)

Execution-enabling change는 여기 기록하지 않고 Run Record·Case status에 남긴다(AGENTS.md §9). 여기에는 Human-approved Semantic Revision만 기록한다.

## REV-001 — Architecture Revision #1: Management Judgment First / Knowledge Usage Context / C2 Validator

- **Revision ID**: REV-001
- **Approved**: 2026-09-01 (Human, `golden/HUMAN_DECISIONS.md` HD-6)
- **Target Failures**: F-005 Action / Change Bias (재정의, 6 Case), F-006 Provided Knowledge Under-use (8/8). Secondary observation: F-001, F-002, F-008.
- **Change Objective**: (1) Customer Context에 대한 Management Judgment를 Action 생성 전에 명시적으로 확정하고, 판단 유형(개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가) 어느 것도 기본값이 되지 않게 한다; 판단에 맞는 Next Action(변경·유지·확인·정보안내·절차·연계)을 만든다. (2) Knowledge를 "무엇"뿐 아니라 "왜 지금"(Case Relevance)·"어디까지"(Usage Boundary)·Source와 함께 전달한다 — Knowledge 양은 늘리지 않는다. (3) HD-2.1 투자성향↔펀드 위험등급 Eligibility를 deterministic validator로 구현한다(DETECT_ONLY 종료).
- **Change Scope**:
  - `prototype/runtime.py`: SYSTEM_ROLE 원칙 8~10 추가(판단 우선·방향 중립·Knowledge Usage); OUTPUT_INSTRUCTION 스키마 `management_need/solution_candidates` → `management_judgment{judgment, reasoning, must_confirm_before_action}` + `next_actions[{action, kind, condition, risk_level}]`; `KNOWLEDGE_FIELDS_SENT`에 Case Relevance·Limitation(Usage Boundary로 렌더)·Source / Location 추가(Case-local Interpretation은 계속 미전달); C2 매핑 상수·Constraint Section 전달·`validate_c2_fund_grade`(action에 불가 등급 → FAIL, condition/brief → REVIEW); C1/C3 validator를 next_actions 기준으로; `judgment_types_detected` 기록; schema check 갱신.
  - `prototype/run_case.py`, `prototype/render_run.py`: 새 스키마 출력·전사 (구 스키마 record도 렌더 가능).
  - Knowledge Pack 내용은 변경하지 않음(Frozen). 전달 필드만 확장.
- **Not in scope (보류)**: F-001/F-008 전용 Brief Validation, Reusable Knowledge Base, 최종 Employee Brief UX, Retrieval/RAG/Graph, Multi-Agent, 자동 Evaluator.
- **Before Runtime Commit**: 601aa1b (P0 Batch RUN_001)
- **After Runtime Commit**: 8cf3787 (RUN_002 record `git_head` 참조)
- **Affected Files**: prototype/runtime.py, prototype/run_case.py, prototype/render_run.py, prototype/README.md, sources/corpus/06_공식기준_Human확인/투자성향별_펀드위험등급_투자권유기준.md, sources/source_registry.md (SRC-096), golden/HUMAN_DECISIONS.md (HD-2.1, HD-6), cases/CONSTRAINT_MAP.md (C2), cases/FAILURE_MAP.md (F-005 재정의)
- **Regression**: P0 8 Case RUN_002 / EVAL_002 (각 1회, GC-01→04→03→06→10→12→14→16). 결과: `golden/REVISION_001_REGRESSION.md`.
