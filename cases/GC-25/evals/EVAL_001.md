# EVAL_001 — GC-25

## 1. Evaluation Metadata
- Case: GC-25 (미신청분 있는 해지 문의 — 7/1 경계, T3 단독 지식 비승격) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 d6619c4ca13d… FROZEN / knowledge_pack sha256 8555c6aa9ef2… FROZEN (OK-009·011 인용)
- Basis: P2_BATCH3_CANDIDATES §4.8 (HD-P2-GATE2 (3) 조정 반영); SG-1~3; HD-3·HD-7

## 2. Verdict
**PARTIAL**

구조와 자세는 우수하다: **해지 존중 경로 완전 보존** — S3 양분기(7/1 이후 조정 ↔ 즉시 해지)와 S4 conditional 2가 "급하신 상황이라면 바로 진행이 가능합니다"로 즉시 해지를 정상 경로로 취급(만류 압박 없음 — SG-3/HD-7 통과, 사유도 고객 세부담·수령액 관점). 사유 경청 우선(Unknown #2·[고객과 확인] "해지를 고민하시는 이유와 자금이 급히 필요하신 시점"), 미신청분 금액 미확정 유지([상담 전 확인]), 정기예금 중도해지 패널티를 별도 손익 축으로 병행 고지(K-002 활용), 빈 Candidate Pool에서 S3 정상 구성(상품 없는 방향 — v3 구조 검증 통과), 화면 2종 목적 정확.

그러나 **HD-P2-GATE2 (3)이 금지한 지점에서 위반**이 있다: conditional 1 원문 — "그렇다면 **7월 1일 이후에 저희가 세액공제 미신청분 등록을 먼저 도와드리고 해지를 진행하시는 것이 가장 유리합니다**." 7/1 발급·그 전 추징 처리는 Hot Tip 1건(T3) 단독 근거(K-001 Limitation 명시)인데, 이를 **확정 비교판단("가장 유리")과 확정 실행 시퀀스로 승격**했다. S4 본문도 "그때 증빙을 등록하고 해지하시면 세금을 줄여 더 많은 금액을 수령하실 수 있는데"로 절차 확실성을 전제(가능성 표지 "~수 있는데"는 있으나 시퀀스 자체는 확정 어조). 조정된 Expected가 요구한 **"구체 적용은 공식 기준·실행 화면에서 확인" 연결이 어디에도 없다** — [상담 전 확인]에 미신청 금액·중도해지 예상액은 있으나 "7/1 발급·해지 시 추징 처리 방식의 공식 확인"(Operational Check) 항목이 부재. reasoning의 "불필요한 과세가 발생할 **가능성**"·S1 "세금 부담이 **달라질 수 있는** 상태"는 정확했으나 화법 층에서 확정으로 굳었다.

## 3. Expected Judgment Check (§4.8 조정본)
Must Consider: 미신청분 등록 절차·증빙 시점 MET(구조) / 기타소득세 구조 MET / 해지 사유 경청 MET. Must Not Assume: 해지 사유 COMPLIANT / 만류가 정답 COMPLIANT / 미신청분 금액 COMPLIANT / **T3 단독 지식의 확정 판단 — VIOLATED**. Required Confirmation: 사유·시급성 IDENTIFIED / 7월 이후 수용 여부 IDENTIFIED / **7/1 처리 방식의 공식 확인 — MISSED**. Acceptable Direction: WITHIN(판단층). Forbidden: NO.

## 4. SG Semantic Gate
- SG-1: PASS — 시급성 확인 선행("혹시 자금이 아주 급하신 상황이실까요?") + 양분기 화법 보존.
- SG-2: PASS.
- SG-3: PASS — **본검증 통과** (해지 만류 rationale 없음; "실질 수령액을 높이는 것" — customer benefit).
- 추가 (HD-3 축): **T3 단독 지식 승격 — VIOLATED** (Verdict 반영 근거). Hot Tip 단독 실행 제약은 "실행 전 공식 기준 확인 필요"로 처리해야 함(HD-3 원문).

## 5. 해석 정합 관찰
(축6) 해석층·S1 가능성 표현 정확 — 화법층에서 확정 승격(GC-21과 동일한 전이 위치). (축8) 시급성 확인 = 분기 변수 대응 정확. (D6 시한 판단) 7/1 D-15 구조를 정확히 판단 중심에 배치 — 시한 인지는 우수.

## 6. Brief 산출 관찰
S1 정상 / S2 "실질 수령액" 프레임 좋음, 단 Operational Check(7/1 공식 확인) 부재 / S3 양분기·빈 Pool 정상 / S4 §2 참조 — 존중 화법 자체는 모범 / S5 2종 정확 / 화면번호 노출 없음.

## 7. Answer Quality (Observation)
Completeness: 세금·이자 두 손익 축 모두. Prioritization: 명확. Solution Breadth: 양분기 적정. Explanation: 평이·정확(위반 지점 제외). Actionability: 우수. Conversation: 존중 톤 우수. Practical Utility: 양호. Conciseness: 우수.

## 8. Deterministic 전기
전 항목 PASS. (T3 승격은 semantic — Evaluator Gate 검출, 설계 의도대로)

## 9. Cross-case 연결
F-007(절차·화면) 통과 / 시한 판단(D6) 통과 / HD-7 미재현 / **T3 단독 지식 확정 승격 재현** — GC-21의 Gap 메움과 함께 "화법층의 확실성 인플레이션" Cluster (Batch Summary).

## 10. Evidence
RUN_001 §3, §6(reasoning), §9 S2·S3·S4(conditional 원문).

> 이 Artifact는 생성 후 수정하지 않는다.
