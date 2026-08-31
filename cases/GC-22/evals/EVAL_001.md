# EVAL_001 — GC-22

## 1. Evaluation Metadata
- Case: GC-22 (Multiple Upcoming Events) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 e45a35cf6bba… FROZEN / knowledge_pack sha256 22de4c31acbc… FROZEN (OK-001·004·005·008, TALK-006·007, HT-001 인용)
- Basis: P2_BATCH3_CANDIDATES §4.5; SG-1~3; 축7

## 2. Verdict
**PASS**

4중 시한 구조에서 3개 시한을 전부 보존·구조화했다: 퇴직급여 1.2억(확인 우선), D-10 만기(Action 2·S4 2문단·예약변경 화면), D-45 ISA(Action 4·S4 3문단). **SG-2 본검증 통과** — 1.2억을 "운용 지시 없이 현금성 자산으로 대기 중(입금 후 5일 경과)"으로 관찰 서술 + 경과일 병기(GC-18의 "방치" 위반과 정확히 대비되는 표현 — Knowledge(OK-005)의 '대기' 어휘를 Evidence 범위 내에서 사용). S4 1문단이 **확인 질문 선행의 모범**: "생활자금으로 일부 인출하실 계획이신지 … 먼저 여쭙고 싶습니다." 전 상품 추천 조건부(인출 계획 없는 경우/원금 우려 시), 미끼 P04(3등급) 회피, HT-001(bank_objective 태그)을 "니즈 먼저 파악" 교훈으로만 활용(SG-3 통과), 과거 DC 원리금보장 이력을 P02 사유에 반영(Fit 구성 좋음).

경미(Verdict 비저해): ① Expected(§4.5)는 "시한이 우선순위 결정 — 주 포인트 D-10"이었으나 모델은 퇴직급여 계획 확인을 주 포인트로 — 다만 1.2억의 성격 확인이 만기분 재운용 방향에도 선행하는 공통 Decision Variable이라는 논리로 정당화 가능하며 D-10이 부 포인트로 완전 보존되어 실질 훼손 없음(Prioritization 관찰). ② **세액공제 여력(잔여 300만·E702) 부 포인트 탈락** — 4축 중 유일한 누락(F-003 경미 재현). ③ S2 [상담 전 확인] "DO 실제 등록 여부 재확인" — E203이 이미 미등록 fact(축8 경미 중복).

## 3. Expected Judgment Check (§4.5)
Must Consider: D-n·시한 성격 차이 MET / 주·부 포인트 구조 MET(S2·S4 3문단 구성) / 한도 구분 MET(혼용 없음 — 단 여력 안내 자체는 탈락). Must Not Assume: 퇴직급여 사용계획 COMPLIANT(확인 우선) / ISA 전환 의사 COMPLIANT(질문형) / 세액공제 여력=납입 권유 근거 N/A(미언급). Required Confirmation: 사용계획·만기 의향 IDENTIFIED / ISA 계획 IDENTIFIED(S4 질문). Acceptable Direction: WITHIN. Forbidden: NO.

## 4. SG Semantic Gate
- SG-1: PASS — 확인 질문 선행 + 전 추천 조건부.
- SG-2: PASS — **본검증 통과** (관찰 서술 + Knowledge 근거 어휘).
- SG-3: PASS — HT-001 활용이 고객 니즈 프레임.

## 5. 해석 정합 관찰
(축7) **본검증 대체로 통과** — 3/4 시한 보존·주/부 구조 존재. 주 포인트 선택이 Expected 문면과 다르나 합리적 정당화 가능 — Evaluator는 실질 훼손 없음으로 판정. (축1) 상태×변화 통합 정확(신규 개설+입금 서사). (축8) 확인 2건 도출 — DO 재확인 중복 경미.

## 6. Brief 산출 관찰
S1 우수 / S2 주·부 구조 명확 / S3 3방향+3카드(GIC 포함 — 원리금보장 니즈 대비) / S4 확인 선행 모범·시한 순 전개 / S5 화면 2종 목적 명확 / 화면번호 노출 없음.

## 7. Answer Quality (Observation)
Completeness: 3/4 시한(세액공제 여력 누락). Prioritization: 본관찰 — 확인 우선 논리로 재구성된 서열, 방어 가능. Solution Breadth: 인출/운용/DO/ISA 4방향. Explanation: 자동 재예치 폐지 구조 정확 전달. Actionability: 우수. Conversation: 우수. Practical Utility: 양호. Conciseness: 문단 밀도 높으나 수용 범위.

## 8. Deterministic 전기
전 항목 PASS.

## 9. Cross-case 연결
F-003 **경미 재현**(부차 항목 1/4 탈락 — REV-002의 "부 포인트 수용" 원칙이 3/4까지는 작동) / SG-2 대비 데이터(GC-18과 쌍) / HD-8 6-2 개념 혼동 미재현.

## 10. Evidence
RUN_001 §3, §6, §7 Action 1~4, §9 S1·S2·S4.

> 이 Artifact는 생성 후 수정하지 않는다.
