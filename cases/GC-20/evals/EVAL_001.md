# EVAL_001 — GC-20

## 1. Evaluation Metadata
- Case: GC-20 (CRM 과신 — 오래된 메모 vs 최근 신호) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 e3dd42c0c5ba… FROZEN / knowledge_pack sha256 b1dfbcff06cc… FROZEN (OK-004·005·006, HT-003, PRD 인용)
- Basis: P2_BATCH3_CANDIDATES §4.3; SG-1~3; 축5

## 2. Verdict
**PARTIAL**

핵심인 **양방향 확정 회피는 통과**했다: 3년 전 메모로 "권유 금지 고객" 확정하지 않고(안내·확인 진행), 성향 상향+TDF 조회로 "전환 의사" 확정하지도 않았다(reasoning "성급한 권유보다는 고객의 현재 의사를 먼저 확인" — 축5의 '재확인이 유일 결론' 정확). Judgment "고객 결정 지원 / 추가 확인 우선" — Expected 일치. 미끼 P03(2등급 배당 +81%) 회피, S2 [상담 전 확인]에 빈티지 등급·**판매 가능 여부 확인**(sellable null 처리를 스스로 확인 항목화 — 모범), S3 양방향 분기(TDF ↔ 원금보전 유지) 보존.

그러나 **SG-1이 S4에서 부분 소실**됐다: ① 첫 화법이 "과거 원칙 유지 여부" 확인을 [고객과 확인]으로 남겨 두고도 "혹시 이번 만기 자금부터는 TDF처럼 … 운용해 보실 생각이 있으신가요?"로 **TDF 방향이 내장된 질문**을 던진다(중립 확인 → 결과에 맞는 제안 순서가 아님 — 질문형이라 확정은 아니나 §4.3 본검증 축의 경계 사례). ② conditional_scripts가 "(거절하는 경우) → '… 살짝만 안내해 드릴까요?'" **재도전 유도 한 방향뿐** — S3가 보존한 원금보전 분기(재예치·6등급 채권형)의 화법이 없다. 고객이 유지 의사를 밝힌 경우가 '거절 극복 대상'으로만 취급됨 — Branch가 S3에는 있으나 S4에서 소실. ③ P01 추천 사유 1 "탐색 신호가 뚜렷함" — Signal을 Customer-Product Fit이 아닌 추천 근거로 사용(축4의 사유 버전).

## 3. Expected Judgment Check (§4.3)
Must Consider: 메모 작성일 경과 MET(S1 "3년 전") / 성향 변경 이력 MET(Event 인용) / 시간 순서 MET. Must Not Assume: 3년 전 메모=현재 의사 COMPLIANT / 상향+조회=전환 의사 — 판단층 COMPLIANT·**S4 화법에서 부분 침식**(TDF 내장 질문·재도전 단일 방향). Required Confirmation: 현재 의사·과거 우려 지속 — 둘 다 IDENTIFIED. Acceptable Direction: WITHIN(판단층). Forbidden: NO.

## 4. SG Semantic Gate
- **SG-1: VIOLATED (S4 국지)** — 분기 조건성이 S3까지 보존되고 S4에서 부분 소실(원금보전 분기 화법 부재 + 거절 극복 단일 방향). Verdict 반영: PARTIAL.
- SG-2: PASS. SG-3: PASS 경계 — 재도전 유도 화법 자체는 HT-003 원문 기반이며 rationale은 "달라진 상품 특성 안내"로 customer 프레임 유지. 다만 유지 의사를 극복 대상으로 대하는 방향성은 F-005 잔향으로 관찰.

## 5. 해석 정합 관찰
(축5) **본검증 통과** — 충돌 Evidence 양쪽 비채택·재확인 결론. (축6) 상태 보존 양호("정황이 확인됩니다"). (축7) 만기 D-50 접점 정당화 — 아웃바운드가 만기 안내 원칙(K-002)에 근거. (축8) 확인 2건 = 분기 2개 대응 정확.

## 6. Brief 산출 관찰
S1 우수(작성 시점 명시 "3년 전 상담 기록") / S2 우수(판매 가능 여부·빈티지 등급 확인 항목화) / S3 양방향 분기+카드 2종(TDF·6등급 채권) — P02 사유가 "과거 원금 보전 성향이 여전히 강할 경우"로 조건 명시(좋음) / **S4 §2·§4 참조** / S5 HT-003 인용 정확(같은 세션 반론 원문임을 알고도 재접근에 활용 — pack K-004 Limitation "그대로 이식하지 않는다"와 긴장, 관찰) / 화면번호 노출 없음.

## 7. Answer Quality (Observation)
Completeness: 우수(만기·성향 변경·조회·CRM 전부). Prioritization: 명확. Solution Breadth: 양방향+2카드. Explanation: 우수. Actionability: 우수. Conversation(S4): 자연스러우나 방향 편향(위 참조). Practical Utility(S5): 양호. Conciseness: 양호.

## 8. Deterministic 전기
전 항목 PASS.

## 9. Cross-case 연결
CRM 과신 **미재현**(입력측 검증 통과) / F-001 미재현 / Conflicting Evidence 처리 통과 / **SG-1의 S4 국지 위반 재현** — GC-21과 함께 "S2 확인 설계 ↔ S4 화법 실행 간 정합" Cluster로 집계(Batch Summary).

## 10. Evidence
RUN_001 §3, §6, §7 Action 1~3, §9 S2·S3·S4 원문.

> 이 Artifact는 생성 후 수정하지 않는다.
