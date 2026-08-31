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
| HD-6.1 | 2026-08-31* | Employee Brief를 직원용 Target Output으로 승격 (Diagnostic → Recommendation Brief; REV-002 Step 3) | 확정 |
| HD-7 | 2026-08-31* | Business 원칙 — 관리 필요성은 Customer Evidence에서만 출발 (REV-002 Step 3) | 확정 |
| HD-8 | 2026-08-31* | REV-002 Step 6 — Regression 해석·Operational 보강 3건·REV-003 보류·P2 설계 착수·Answer Quality 축·한도 3필드 분리·REV-002 종료 조건 | 확정 |
| HD-PRE-P2-INPUT | 2026-08-31* | Pre-P2 Input Architecture — 9-Block 승인(수정 2건)·Window 변화 구조·Sequence 방향·3-Layer(Stable ID·JSON·type 2축 분리)·Brief는 별도 Gate·GC-18~25 재분류 원칙 승인·Av `?` 5건 유지 | 확정 |
| HD-PRE-P2-BRIEF | 2026-08-31* | Employee Brief Target Design — Decision & Action Brief 재정의: S3 제안 방향+실제 추천 후보(비해당 폐기), S4 완성형 맞춤 화법, S5 Hot Tip 원문+실행 화면 2역할; 내부 안전원칙 비노출; 구현·Schema·P2는 별도 게이트 | 확정 |

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

## HD-6.1 Employee Brief 승격 (2026-08-31, HD-6 하위 갱신 — REV-002 Step 3)

HD-6에서 "Decision Meaning Preservation 확인용 Diagnostic Output"으로 규정했던 Employee Brief를 **직원용 실제 Target Output(Recommendation Brief)** 으로 승격한다. 구조는 5-섹션(고객 상황 / 핵심 관리 포인트+먼저 확인 / 추천 운용 방향 / 상담 Point / 관련 TIP & GUIDE) — 상세는 `design/EMPLOYEE_BRIEF_SPEC.md`.

단, 이 승격은 **운영 검증 완료를 의미하지 않는다.** REV-002/P2 Regression과 향후 직원 검증의 대상이다.

*날짜 표기: HD-6(2026-09-01)은 P1 Batch 문서 기준 일자와 정합하도록 기록된 값이며, 본 결정의 확정일은 2026-08-31이다.

## HD-7. Business 원칙 — 관리 필요성의 출발점 (2026-08-31, REV-002 Step 3)

> **고객의 관리 필요성은 Customer Evidence에서 출발해야 한다. 은행의 Business Objective가 관리 필요성을 만들어내서는 안 된다. 독립적으로 유효한 고객 관리기회가 존재하는 경우에만, 허용된 범위 안에서 은행의 관리행동(운용 활성화·장기 운용 연결·만기 재운용·추가납입·리밸런싱·이탈방어·연금관계 지속·후속관리)으로 적극 연결할 수 있다.**

- 기존 D10(고객이익-영업압력 분리)·F-009(Marketing Trigger as Management Basis)와 정합 — 폐기가 아니라 명문화·정밀화다.
- REV-002부터 TM Target·Campaign·Badge·LMS/SMS 등 Bank Signal은 Customer Reasoning Input에서 제거된다(Evidence Pack 8-섹션 — `design/EVIDENCE_PACK_SPEC.md`). 검증 축은 Evidence Provenance로 이동: Management Point는 실제 Customer Evidence(`supporting_evidence_ids`)로 추적 가능해야 하며, 근거 없는 관리 포인트는 REVIEW/FAIL.
- 함께 확정된 Step 3 결정(Evidence Pack 8-섹션·Availability·Candidate Pool 원칙·화면값 3계층·Regression 8 Case)의 전체 기록은 `design/TARGET_CONCEPT.md` §6.

## HD-8. REV-002 Step 6 결정 — Regression 해석·Operational 마무리·P2 방향 (2026-08-31)

**Regression 해석**: REV-002는 성공한 Revision으로 확정한다. 유효 설계 효과로 기록: Decision Variable 14개 제거 후에도 Required Confirmation 자가 도출 / Snapshot+Timeline+Upcoming+Calculated 구조의 Fact 누락·시간맥락 개선 / DO 예상 기준일·실제 적용 분리로 확정 판단 감소 / REV-001 Judgment-first·Action Bias 방지 유지 / GC-04↔05 Pair 차이 유지 / 5-섹션 Brief·S4 화법·S5 구조 실출력 / Evidence Provenance 검증의 실제 오류 탐지. **핵심 잔여 병목은 `Structured Result → Employee Brief Semantic Preservation`으로 기록한다** — 구조화 판단에서는 불확실성·조건·출처가 유지되나 Brief 산문 변환에서 일부가 확정 Fact로 승격되는 문제 (단순 금지어 문제가 아님).

**(a) Operational 보강 3건 — 전부 적용** (Semantic Revision 아님, Output Contract 보강):
1. **Epistemic State 보존 (일반 원칙)**: Structured에서 미확인/추론/조건부/고객·CRM 진술/확인 필요 상태인 정보는 Brief에서도 동일 상태 유지. 금지 승격: 고객·CRM 진술→시스템 확인 Fact, 추론→확정, 조건 가능성→충족 확정, 확인 필요 수치→확정 판정, 예정/예상→실제 발생·적용 완료. CRM에 한정하지 않고 Digital Signal·Performance·Whole-Asset 등 모든 Evidence에 적용.
2. **F-011 Provenance 슬롯**: supporting_evidence_ids = E-ID 전용; K-ID는 supporting_knowledge_ids/knowledge_ids_used 전용; 혼합 금지.
3. **F-012 S5 출처**: 내부 K-ID를 직원용 출처로 노출 금지. 우선순위: 자료명 > SRC-ID > 화면번호+화면명 > 공식 가이드/부서명.
- **선택 Regression**: GC-05·GC-11·GC-14만 재실행. 검증 목적 3가지 한정(불확실성 보존 / 슬롯 혼동 해소 / S5 출처 형식). 통과 시 REV-002 마무리 수정으로 확정.

**(b) REV-003 보류**: F-006이 5/9→2/8 경미로 감소, 원인 혼재(Knowledge 부족 vs downstream 미활용) — 지금 구조 변경 시 귀속 불가. Candidate 유지. P2에서 조건/예외 반복 탈락·Pack 내 대안의 Solution 미전달·F-006/F-010 반복·동일 Knowledge 불안정 해석이 cross-case 재현되면 Human Gate 재상정.

**(c) P2 Batch 3 설계 착수**: Case 작성·Freeze·RUN 전에 후보 설계안을 Human에 보고(각 후보: 목적·핵심 Evidence·의도된 충돌/유혹·Expected Judgment Boundary·Must Consider·Must Not Assume·Required Confirmation 예상·검증 Failure Pattern·기존 Case와의 비중복 사유). 우선 검증 영역: Whole-Asset 중심 / Digital Signal→Intent 승격 유혹 / CRM 과신 유혹 / Performance Comparison(단독 Trigger 금지 검증; Peer 제외 유지) / Multiple Upcoming Events·Conflicting Evidence 우선순위 / 이탈·부분대안(F-010 재검증).

**Answer Quality — P2부터 Secondary Observation Axis 추가**: PASS/FAIL Gate 아님. 관찰축: Completeness / Prioritization / Solution Breadth / Explanation Quality / Actionability / Conversation Quality(S4) / Practical Utility(S5) / Conciseness·Signal-to-Noise. Observation으로만 수집, 반복 패턴 발견 시 별도 Failure Pattern 또는 Revision 후보로 상정.

**(d) Availability 최종 갱신**: 당해년도 IRP 개인부담금 납입액·연금계좌 연 납입한도 잔여·연금계좌 세액공제 잔여한도 = **O 확정**. 단 세 값의 개념 분리 필수(별도 필드): `irp_personal_contribution_ytd`(해당 IRP 당해 개인부담금 실납입 — 퇴직급여 이전금 등과 합산 금지) / `pension_account_contribution_limit_remaining`(관계 법령상 합산 대상 연금계좌 기준 연간 납입 가능 잔여 — 단일 IRP 독립 한도로 해석 금지, ISA 전환 등 특례 존재 가능) / `pension_tax_credit_limit_remaining`(연금저축·퇴직연금 합산 세액공제 잔여 — 납입 가능 금액과 다른 개념). **추가 납입 가능 금액 ≠ 추가 세액공제 가능 금액; Agent가 한 값을 다른 값으로 추정 금지.** 세제 Rule은 Prompt 상수 금지 — Rule-derived 계산 시 rule_source·rule_as_of·적용 Rule ID 추적, Human 승인 공식 Source/Registry 근거만. 잔여 `?` = **개설 채널 1건** (Source 확인 전까지 유지, 임의 O 처리 금지).

**R4 위험자산 한도**: Rule-derived 후보 유지하되 공식 rule_source 확보 전 deterministic Rule 비활성화. Hot Tip·설명자료만으로 확정 금지(HD-3). Source Traceability Gap 유지, 공식 근거 확보 시 별도 Human Decision 후 활성화.

**REV-002 종료 조건**: ① Operational 3건 적용 ② GC-05/11/14 선택 Regression ③ 불확실성 보존 확인 ④ F-011 해소 확인 ⑤ F-012 해소 확인 ⑥ Availability Spec 갱신 ⑦ 결과·FAILURE_MAP 최종 기록 — 완료 시 종료. 선택 Regression에서 신규 Semantic Failure 미발견 시 종료 처리하며, 문구·형식 오류로 새 Revision 번호를 만들지 않는다.

## HD-PRE-P2-INPUT. Pre-P2 Input Refinement 결정 (2026-08-31)

범위: **Input Architecture와 P2 진행 조건만.** Employee Brief Refinement는 제외 — 별도 Human Design Prompt로 재설계 후 별도 승인 예정. 상세·반영 위치: `design/PRE_P2_REFINEMENT_PROPOSAL.md` §6·§7.

1. **9-Block Target Input Architecture 승인** (Lifecycle / Snapshot / Recent Changes & Money Flow / Event Timeline / Investment Behavior / Digital Behavior & Sequence / Wider Financial Context / Upcoming Decision Horizon / Supplementary Human-authored Context). 승인 방향: Recent Changes 분리, Sequence 확장, CRM 재위치(삭제 아님)·System-observable ①~⑧ 선직렬화, 합산 한도의 ⑦ 배치, DO Rule Clock의 ⑧ 배치. 수정 반영: **1-1** 잔액-Flow 연결은 산술 reconciliation(금액 일치)까지 — "미운용/대기성/남아 있는 자금" 류 의미 부여 금지(What happened/changed까지, What it means는 Agent); **1-2** ⑧에서 "만기→재예치/변경 결정 필요" 류 사전 의미부여 제거 — 객관적 시점 정보(상품명·만기일·D-n·Rule Clock·예정 Event)까지만.
2. **Recent Changes는 Window 기반 구조** — 30d 우선, 90d 확보 시 추가, 특정 기간 강결합 금지. 90d Snapshot Av `?` 유지.
3. **Digital Behavior Sequence 방향 승인** — Sequence도 Signal이지 Intent 아님, "이탈 준비 중/투자 의사 있음" 류 사전 Label 금지. Av `?` 유지, P2는 Sequence Case 사용 가능하되 횟수/행동 Event 형태로 degraded 가능해야 함.
4. **3-Layer 승인** (Raw → Canonical Evidence Object → Deterministic Derived Context → 9-Block Rendering → Agent). 4-1 P2 신규 Case부터 적용, 기존 Frozen input_v2·RUN·EVAL 절대 불변. 4-2 **Evidence ID = Canonical Stable ID** (렌더 순서 무관 Provenance 보존). 4-3 Canonical 형식 **JSON 우선안**. 4-4 **evidence_type(fact/arithmetic_derived/rule_derived/signal)과 source_type(account_system/transaction/digital_behavior/crm/external_account/rule_engine/…) 2축 분리** — 혼합 금지가 핵심. 현 단계 구현 금지.
5. **Brief Refinement 5건 미승인** — Reject 아님, 별도 Brief Design Gate로 이동. Target Brief 확정 금지, Brief Schema/Prompt/Validator 변경 금지. Proposal §4는 `Pending separate Human Brief Design` 표시.
6. **GC-18~25 재분류 원칙 승인** (유지: GC-20·21·23·25 / Input 수정: GC-18·22·24 / Scenario 수정: GC-19 / 보류 없음). GC-18: ISA-IRP 목적 연결 사전 해석 금지(Fact만, 관계는 Agent 구성). GC-19: Sequence 우선 Target + degraded 버전 설계 가능. **Case 작성·Expected Output·Evaluation 설계는 새 Brief 구조 확정 이후에만.**
7. **Availability `?` 5건 유지** (퇴직일 상세 / 90d Snapshot·변화 / 거래횟수 기간 세분화 / Sequence·실행 여부 / CRM 작성 주체) — 임의 O/X 확정 금지, 실제 Source·DB·원천 확인으로만 갱신.

Gate 상태: REV-002 CLOSED 유지 / Pre-P2 Input = Direction Approved / **Brief = Separate Gate Pending** / GC-18~25 = HOLD / Runtime·Schema·Parser 구현 금지 / P2 RUN·EVAL 시작 금지.

## HD-PRE-P2-BRIEF. Employee Brief Target Design (2026-08-31)

REV-002의 5-Section 구조는 유지하되 각 Section의 역할·최종 Output 수준을 **직원용 Decision & Action Brief**로 재정의한다 (직원이 관리 대상·제안 방향·보여줄 상품·할 말·실행 위치를 다시 조립하지 않아도 되는 수준). 전문·Target Output 예시·Section Boundary·필요 Input/Knowledge·구현 전 확인 사항은 **`design/PRE_P2_REFINEMENT_PROPOSAL.md` §4 (재작성본)**.

- **S1**: 자연어 한 문단 유지(2단 Block 강제 안 함) + 실제 숫자·시점 보존 + 절제 해석 허용/의미 승격 금지 경계.
- **S2**: why_now·rationale 필드 비노출(내부 판단, 문장에 녹임) · 방어문구 비노출 · "먼저 확인"을 [상담 전 확인]/[고객과 확인] 2영역으로(구 [직원]/[고객] Label 폐기) · 빈 Section 강제 금지 · 기지 사실 재질문 금지.
- **S3**: "추천 운용 방향" → **"제안 방향 및 추천 후보"** — Management Direction 전 범위(유지·신규운용·재운용·조정·체계 변경·세제·수령 관리·중도인출·이전·의사결정 지원·대안경로)를 정상 Output으로, **비해당 구조 폐기**. Direction→Solution Type→Product Candidate 순서. 상품 필요 시 Candidate Pool 내 실제 상품 카드(상품명·유형·등급·수익률+측정기간+기준일·특징·Metadata·**Customer–Product Fit 추천 사유**)까지. 수익률 단독 추천 논리 금지.
- **S4**: 가이드가 아니라 **S1~S3+Hot Tip 화법 Knowledge+실제 고객 데이터를 합성한 완성형 맞춤 상담 화법**. Peer/Performance/연령은 방향 도출 이후의 설명 재료로만(단독 Trigger 금지). 조건부 후속 화법 허용(강제 아님). 성공 기준: S4만 읽어도 "뭐라고 말하지" 고민 없음.
- **S5**: 두 역할 — (1) Hot Tip/Guide **원문 발췌+Metadata**(작성자·작성일·좋아요 등; 좋아요=공감 Signal이지 공식성 아님, 제도·세제·실행 가능 여부는 공식 Guide 우선) (2) **다음 Action 실행 화면**(직원 단말+고객 StarBanking, S3 관련 화면만). 관계: S3=무엇을 / S4=어떻게 말할까 / S5=어디서 실행.
- **유지**: Judgment-first·HD-7·Hard Constraint·Epistemic Preservation·Evidence Provenance·Candidate Pool·Branch Preservation·Performance 단독 Trigger 금지·Signal≠Intent·CRM≠ground truth — 단 이 내부 원칙을 Final Brief에 자기검열 문구로 노출하지 않는다.
- **미변경**: Brief Schema·Prompt·Validator·Runtime·Candidate Pool 구현·Knowledge Retrieval·P2 Case·Freeze·RUN/EVAL — 전부 별도 구현 게이트. 구현 전 확인 4건은 Proposal §4.6.
