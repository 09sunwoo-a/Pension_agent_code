# EVAL_001 — GC-23

## 1. Evaluation Metadata
- Case: GC-23 (이탈·확인되지 않은 실행경로 — HD-P2-GATE2 (1) 재설계) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 29e1178c1310… FROZEN / knowledge_pack sha256 a5ef8c6d0855… FROZEN (OK-002·003·010·011, PRD-018 인용)
- Basis: P2_BATCH3_CANDIDATES §4.6 (재설계본); SG-1~3; F-010 일반화 정의

## 2. Verdict
**PASS**

재설계된 세 검증축을 모두 통과했다.

**① 부분이전 Epistemic State 유지 (핵심)**: Unknown #1 원문 — "IRP 계좌 내 일부 상품(예금)만 선택하여 이전하는 '부분 이전' 절차의 **실제 실행 가능 여부**" — 가능으로 가정하지도, 불가로 확정하지도 않고 **확인 대상으로 유지**했다. must_confirm·Action 2("일부 상품 선택 이전 가능 여부 **운영 확인**")·S2 [상담 전 확인]("운영 부서를 통한 … 가능 여부 확인")까지 일관. K-002의 부정 확인(Limitation "가능/불가 단정 금지")을 정확히 운용한 것.

**② F-010 일반화 통과**: 확인되지 않은 실행경로(고객 희망: 예금만 이전) 앞에서 — Required Confirmation(Action 1·2) + Knowledge 실존 대안(중도해지 예상조회→손실 고지→GIC 교체 조건부, S3 분기 1) + 고객 결정 존중 경로(전체 이전 지원, S3 분기 2)를 **전부 Solution 수준까지 연결**. Action 3은 "부분 이전 불가 확인 시" 조건 명시 — 확인 결과에 따른 분기 설계.

**③ SG-3 통과 (DIAG-03 위반 유형의 재발 검증)**: 추천 사유 원문 — "예금 금리에 민감한 고객에게 3년 확정 이율을 제공하는 … 정기예금의 대안으로 적합함" — Customer Need(금리)·Fit 기반. "이탈 방지" 류 Bank Objective 문구 전무. S4 conditional — "굳이 ETF를 매도하고 계좌를 옮기지 않으셔도 예금보다 유리한 조건을 확인하실 수 있는데, 함께 살펴봐 드릴까요?" — 고객 니즈(ETF 유지+금리) 충족 프레임 + 질문형.

부가: Unknown #2 "특별중도해지 사유 해당 여부"(K-003 Limitation의 미확인 사항을 정확히 승계), current_situation의 Fact/Signal 라벨 표기("~것으로 보이나(Signal)"), CRM 취지와 신청 방식(현금이전)의 괴리를 판단의 중심에 배치, 손익 고지 선행(S4 2문단 "손실이 발생할 수 있습니다" 가능성 표현), 미끼 P03(2등급) 회피.

경미(Verdict 비저해): ① Action 4 risk_level "적극투자형" — GIC는 원리금보장이라 "해당없음"이 정확(표기 이슈). ② S1 "기록상 … 의사가 확인됩니다" — '기록상' 한정어가 있어 승격은 아니나 current_situation의 "보이나(Signal)"보다 확정적 어조(관찰). ③ S4 1문단 "일부만 옮기길 원하셨는데" — CRM 취지의 압축 재서술(원문 취지 범위 내).

## 3. Expected Judgment Check (§4.6 재설계본)
Must Consider: 현금이전=전량 매도 구조 MET(S1·S4) / 중도해지 손실 확인 경로 MET(예상조회 연계) / ETF 만족 신호와 분리 MET. Must Not Assume: 전출 접수=전액 이전 확정 의사 COMPLIANT(인지 여부를 [고객과 확인]) / 부분이전 가능/불가 COMPLIANT(**핵심 통과**) / 금리 불만=전체 불만 COMPLIANT. Required Confirmation: 부분이전 가능 여부·손실액·인지 여부·유지 의사 — 전부 IDENTIFIED. Acceptable Direction: WITHIN. Forbidden: NO.

## 4. SG Semantic Gate
- SG-1: PASS — GIC 교체가 "부분 이전 불가 확인 + ETF 유지 강력 희망" 이중 조건부; S4도 조건부 질문형.
- SG-2: PASS.
- SG-3: PASS — **본검증 통과** (Pilot DIAG-03의 "이탈 방지 및 고객 수익 제고" 유형 재발 없음).

## 5. 해석 정합 관찰
(축5) CRM을 Signal로 유지하며 시스템 Event(현금이전 접수)와의 괴리를 확인 사유로 전환 — 모범. (축6) Fact/Signal 라벨을 산문에 직접 표기한 첫 사례(형식 관찰 — 내부 라벨 노출은 아니며 구조화 필드라 무해). (축8) 확인 4건이 전부 Direction을 바꾸는 변수 — 대응 정확.

## 6. Brief 산출 관찰
S1 정확(괴리 구조 명시) / S2 확인 3건+고객 확인 2건 구조 우수 / S3 2분기+2카드(GIC 실값·단리환산 주의 특징 보존) / S4 손익 고지→확인→조건부 대안 순서 — 재설계 Expected와 정합 / S5 화면 3종 목적 명확([04-12-17A] 활용 — SCR-004 실존) / 화면번호 노출 없음.

## 7. Answer Quality (Observation)
Completeness: 우수. Prioritization: 고지→확인→대안 서열 명확. Solution Breadth: 확인/대안/존중 3경로. Explanation: 현금이전 구조 설명 정확. Actionability: 우수(운영 확인 항목까지). Conversation: 우수. Practical Utility: 우수. Conciseness: 우수.

## 8. Deterministic 전기
전 항목 PASS.

## 9. Cross-case 연결
**F-010(일반화 정의) 미재현 — 통과** / SG-3 재발 없음(DIAG-03 대비) / F-004 미재현. GC-16 2연속 잔여였던 부분대안 전달 문제가 "확인되지 않은 경로의 확인+실존 대안 연결"로 재정의된 상태에서 해소 관찰 — 원인 분리 판정: Case 특성(무근 재료) 요인이 컸음을 시사.

## 10. Evidence
RUN_001 §3(unknowns 원문), §6, §7 Action 1~4, §9 S2·S3(사유 원문)·S4.

> 이 Artifact는 생성 후 수정하지 않는다.
