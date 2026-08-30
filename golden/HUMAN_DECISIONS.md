# Human Decisions — Golden Discovery Batch

확정된 Human Decision 의 기록. 여기 있는 항목은 더 이상 `Human Review Needed` 가 아니다. 운영 규칙은 `AGENTS.md` §20, Case 별 적용은 `golden/GOLDEN_SET_DRAFT.md` §11 을 본다.

| ID | 일자 | 결정 | 상태 |
|---|---|---|---|
| HD-1 | 2026-08-30 | 연금·세제 영역 Agent Scope | 확정 |
| HD-2 | 2026-08-30 | 투자성향 적합성 = Hard Constraint (펀드 위험등급·디폴트옵션 Eligibility) | 확정 |
| HD-3 | 2026-08-30 | 영업점 Hot Tip / Field Know-how = Operational Knowledge | 확정 |
| HD-4 | 2026-08-30 | 첫 Golden Discovery Batch = P0 8 Case, CASE_001 은 GC-00 Baseline 유지 | 확정 |
| HD-5 | 2026-08-30 | Human Approval 단위 = 업무 Semantic Boundary 와 변경 범위 (Step 별 승인 폐지) | 확정 |
| HD-2.1 | 2026-09-01 | 투자성향 ↔ 펀드 위험등급 Eligibility Mapping 공식 확인 (C2 deterministic validator) | 확정 |
| HD-6 | 2026-09-01 | Architecture Revision #1 승인 — F-005 Action/Change Bias 재정의·교정, F-006 Knowledge Usage Context 전달, C2 validator; P0 RUN_002 Regression | 확정 |

---

## HD-1. 연금·세제 영역 Agent Scope

Agent 가 수행하는 것: 제도 구조 이해 · 적용요건 판단 · 관련 시한 판단 · 고객 상황에서 고려할 제도적 요소 식별 · Required Confirmation 도출 · 직원이 확인할 화면/업무 절차 안내 · 고객에게 설명할 판단 방향 구성.
(예: 연금개시 가능 여부, 연금수령 적용요건, 세액공제 구조, 과세상 고려사항, 관련 시한, 업무 화면에서 확인할 값)

Agent Scope 에서 제외: 고객별 **최종 확정 계산값** — 최종 세액, 최종 수령액, 시스템별 확정 금액, 개별 조건에 따른 최종 세무 결과. 이는 공식 업무 화면·계산기·시스템 조회 결과 확인으로 연결한다.

Agent 가 제도 산식과 구조를 이해하여 판단에 활용하는 것은 허용한다. 프로젝트를 세무계산 Agent 로 확장하지 않는다. Golden Evaluation 도 이 Scope 를 기준으로 한다.

## HD-2. 투자성향 적합성 = Hard Constraint

투자성향 5단계: `안정형 < 안정추구형 < 위험중립형 < 적극투자형 < 공격투자형`.
투자성향은 **가입 가능한 상품 위험수준의 상한을 제한하는 Hard Constraint** 다.

- **펀드**: `Customer Investment Profile → Fund Risk-grade Eligibility Mapping → 가입 불가능 후보 제거 → LLM Reasoning → Post-Reasoning Validation`
- **디폴트옵션**: `Customer Investment Profile → Default Option Eligibility Mapping → 가입 불가능 후보 제거 → LLM Reasoning → Post-Reasoning Validation`
- **해석**: 투자성향은 해당 수준까지 위험을 부담하도록 요구하는 기준이 아니다. 공격투자형 고객도 더 낮은 위험수준을 선택할 수 있다. `투자성향-운용상태 불일치 → 자동 관리 필요 / 자동 리밸런싱` Rule 을 만들지 않는다.
- **Source Traceability**: Corpus 내 공식 Eligibility Mapping Source 가 부족·불완전해도 이 Business Fact 를 약화하거나 잠정 상태로 되돌리지 않는다. `Source Traceability Gap` 으로 별도 기록하고, 공식 원문 확보 시 Source-grounded Constraint 로 교체한다. 기존 CASE_001 Artifact 는 소급 수정하지 않는다.

### HD-2.1 투자성향 ↔ 펀드 위험등급 Eligibility Mapping (2026-09-01, 공식 확인)

| 투자성향 | 권유 가능 등급 |
|---|---|
| 안정형 | 6등급 |
| 안정추구형 | 5~6등급 |
| 위험중립형 | 4~6등급 |
| 적극투자형 | 3~6등급 |
| 공격투자형 | 1~6등급 |

상품 위험등급: 1 매우높은위험 · 2 높은위험 · 3 다소높은위험 · 4 보통위험 · 5 낮은위험 · 6 매우낮은위험. 투자성향은 최소 위험수준 요구가 아니라 최대 허용 위험수준 제한이다. Source: SRC-096 (`sources/corpus/06_공식기준_Human확인/…`, Human-confirmed Official; 원문 확보 시 교체). Runtime: `prototype/runtime.py` `validate_c2_fund_grade` — Reasoning 전 허용 범위 전달 + Post-Reasoning deterministic validation. C2 DETECT_ONLY 상태 종료.

## HD-3. 영업점 Hot Tip / Field Know-how = Operational Knowledge

Source Authority 순서: `공식 법·제도·내규·시스템 기준 > 행내 공식 업무가이드/매뉴얼 > 영업점 Hot Tip / Field Know-how`.

Hot Tip 을 적극 활용하는 영역: 직원이 먼저 확인하는 것 · 화면/채널 · 준비사항 · 상담 순서 · 현장 예외 · 실행 전 확인사항 · 고객 커뮤니케이션.

Hot Tip **단독으로 확정하지 않는 것**: Hard Constraint · 법·제도 Constraint · 가입 가능/불가능 · 실행 가능/불가능의 최종 판정.

Hot Tip 에만 존재하는 실행 제약은 `Operational Check Needed / Required Confirmation / 실행 전 공식 기준 확인 필요` 로 처리한다. 공식 Source 또는 시스템 기준에서도 확인되면 Execution Constraint 로 승격할 수 있다. Source 충돌 시 임의로 평균·통합하지 않고 공식성·최신성·적용범위로 판단하며 필요 시 `Source Conflict` 로 기록한다.

## HD-4. Batch 범위

첫 Golden Discovery Batch 대상: **GC-01, GC-03, GC-04, GC-06, GC-10, GC-12, GC-14, GC-16** (P0 8개). 각 Case 1회 실행.
CASE_001 은 기존 Baseline / GC-00 으로 유지 — 재작성하지 않고, RUN_001 / EVAL_001 을 수정하지 않으며, Batch 실행 대상에 포함하지 않는다. P1 Case 는 1차 Batch 완료 후 검토.

## HD-5. Human Approval 단위

Human 은 업무의 경계와 중요한 변경을 결정하고, Agent 는 승인된 경계 안에서 Case 개발·실행·평가를 자율적으로 반복한다. 자율 범위·Human Gate·Stop Condition 의 구체 규칙은 `AGENTS.md` §20.

### HD-5.1 Runtime Autonomy 경계 (2026-08-31, HD-5 하위 실행규칙)

> Human-approved Golden Semantic Boundary 를 구현하기 위한 최소 Runtime 확장은 Agent 에게 위임한다. 단, Agent 의 판단 의미·허용 Solution·Constraint·Grounding·Evaluation Boundary 를 새롭게 변경하는 Runtime 설계는 Human Gate 대상이다.

- **Execution-enabling Runtime Change (자율)**: 승인된 Case 의 Customer Fact 를 받는 입력 필드·parser·serialization 확장; HD-2 Eligibility Mapping 의 deterministic validator 구현; 승인된 Constraint·Knowledge 를 Prompt 에 전달하는 구조 — 판단 규칙을 새로 만들지 않는 구현.
- **Runtime Semantic Change (Human Gate)**: Solution / Decision Outcome 분리, 새 Output Schema, 새 Hard Constraint, 기존 Constraint 삭제·완화·의미 변경, Retrieval 범위 변경, Execution Validation·Solution Conflict 의 새 판정 규칙, Agent / Planner / Node 구조 도입, Model·Generation Parameter 변경.
- 판단 기준과 Batch 중 처리 절차는 `AGENTS.md` §9 · §20.9. 구현 중 기존 Decision 으로 정의되지 않은 판단 기준이 필요해지면 Human Gate 로 전환한다.

## HD-6. Architecture Revision #1 (2026-09-01)

P0 Batch Cross-case Evidence(F-005 6 Case, F-006 8/8)에 근거한 Semantic Revision 승인. 상세는 `prototype/REVISIONS.md` REV-001.

- **F-005 재정의**: "Non-change Path Absent" 가 아니라 **Action / Change Bias** — Customer Context에 대한 Management Judgment를 충분히 완료하기 전에 Solution 생성 압력 때문에 변경·개입 방향으로 조기 수렴하는 현상. 변경도 유지도 정답일 수 있다; 문제는 판단 전에 Action이 나오는 것이다.
- **구조**: `Customer Situation → Management Judgment(개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가) → Next Action`. 목록은 Ontology로 고정하지 않는다. 방향 중립 — Intervention Avoidance Bias 도 금지.
- **Knowledge**: 양을 늘리지 않고 Case Relevance · Usage Boundary · Authority · As-of · Source 를 함께 전달. F-002 Over-application은 Secondary Observation.
- **Employee Brief**: 현재는 Decision Meaning Preservation 확인용 Diagnostic Output. 최종 UX 설계 아님. 평가 대상: Unknown→Fact, 조건부→무조건, Hard Constraint 소실, Judgment 왜곡, 고객 의사 왜곡.
- **보류**: F-001/F-008 전용 Validator, Reusable KB, Retrieval/Graph, Multi-Agent, 자동 Evaluator, 통계 반복 평가.
- **Regression**: P0 8 Case RUN_002/EVAL_002 (Builder Gemma 4, Evaluator Claude). Trade-off 확인 필수(GC-01/06 Action 약화 여부, GC-04/10 유지 반영, GC-03 확인 우선, GC-12/14/16 구체성).
