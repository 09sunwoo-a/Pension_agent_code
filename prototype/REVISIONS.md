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

## REV-002 — Architecture Revision #2: Customer Evidence Pack (8-Section Input) / 5-Section Employee Brief / Evidence Provenance

- **Revision ID**: REV-002
- **Approved**: 2026-08-31 (Human, Step 3 Human Gate 2회 — `design/TARGET_CONCEPT.md` §6, `golden/HUMAN_DECISIONS.md` HD-6.1·HD-7)
- **Target Failures / Evidence**: F-001("방치" 단정 — 18 Case 감사에서 5건 전부 S1 서술부 귀속), F-003(부차 만기 탈락), F-004(확인 축 — 입력 힌트 없이 도출로 전환), F-008(Brief 변환 중 조건 소실), F-009(구조적 차단 — Bank Signal 입력 제거), F-010(분기 축소 — Branch Preservation). 근거: `design/evidence/` 5건.
- **Change Objective**: (1) Input을 판단 완료형 라벨 없는 8-섹션 Customer Evidence Pack으로 재조직 — `value+as_of`, F/A/R/S 라벨, NULL·0·해당없음 3분, Bank Signal(TM·Campaign·Badge·LMS) 전면 제외. (2) 전처리에서 Arithmetic Derived(경과일·D-n·증감)와 Rule-derived Fact(개시요건·DO 적용 예상 기준일·세액공제 잔여한도 수신·`rule_source`/`rule_as_of`)를 deterministic 계산 — 의미 판단("방치"류)은 전처리 금지, DO는 예상 기준일까지만(실제 적용 여부 원천값 없이는 미제공). (3) Output을 5-섹션 Employee Brief(S1 상황/S2 관리 포인트+먼저 확인/S3 방향 — Branch Preservation·Candidate Pool/S4 상담 순서+화법/S5 TIP&GUIDE 출처 표기)로 분해, `supporting_evidence_ids`/`supporting_knowledge_ids` Provenance 추가. (4) SYSTEM_ROLE 개정: 상품명 전면 금지 → Candidate Pool 조건부 허용(원칙 5), CRM·Signal·Performance Comparison·Business 원칙 경계(원칙 11~14), 분기 규칙(원칙 15).
- **Change Scope**:
  - `prototype/runtime.py`: `run_case` dispatch(`input_v2.md` 존재 시 REV-002, 아니면 REV-001 경로 불변 — 기존 Run 비교 가능성 보존); `load_evidence_pack`(8-섹션 파싱·Evidence ID 자동 부여·machine JSON 블록); `build_calculated_facts`; `SYSTEM_ROLE_V2`/`OUTPUT_INSTRUCTION_V2`; `check_schema_v2`; deterministic validator 5종 신설(`validate_forbidden_words`·`validate_latex_residue`·`validate_evidence_ids`·`validate_screen_survival`·`validate_candidate_pool`) — 의미 판정은 Evaluator 몫(EMPLOYEE_BRIEF_SPEC §3.2); C1/C2/C3 유지(C2/C3 스캔은 직렬화된 Brief 포함).
  - `prototype/render_run.py`: REV-002 record 렌더(Evidence Pack 입력·5-섹션 Brief·신규 validator 결과·Evidence ID) — 구 record 렌더 유지.
  - `input_v2.md` 형식: fenced ```json machine 블록(전처리 원천값) + `## <n>. <섹션명>` 8개 + bullet 항목. Frozen case.md·knowledge_pack.md는 불변.
- **Not in scope (보류 — §20.8)**: Retrieval/자동 색인, Reusable KB, Multi-Agent, 자동 Evaluator, Brief↔원재료 의미 수준 대조(Evaluator 수행).
- **검증**: 스모크 테스트(8-섹션 파싱, A/R Fact 산출 — 개시요건 미충족/DO 도래 전·경과 두 변형, 스키마 정상/이상 케이스, validator PASS/FAIL 양방향, 렌더러) 통과. 레거시 경로 GC-04·GC-11 dry-run으로 REV-001 무변경 확인.
- **Before Runtime Commit**: a84c8e9 (Step 3 Spec 확정) / **After**: 본 항목이 포함된 커밋 (RUN record `git_head` 참조)
- **Regression**: 8 Case (GC-03·04·05·09·11·14·16·17) `input_v2` RUN/EVAL — 변환 규칙·N/A 표기는 `design/EMPLOYEE_BRIEF_SPEC.md` §5.
