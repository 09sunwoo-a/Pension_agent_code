# EVAL_001 — GC-24

## 1. Evaluation Metadata
- Case: GC-24 (결정세액 부족 — 잔여한도 ≠ 실효 공제) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 cfbda2bc231b… FROZEN / knowledge_pack sha256 fc4aa2215a4c… FROZEN (OK-006·008·009 인용)
- Basis: P2_BATCH3_CANDIDATES §4.7; SG-1~3; HD-1

## 2. Verdict
**PASS**

이 Batch에서 가장 결함이 적은 수행. **결정세액 조건의 정면 처리**: Unknown #1("원천징수영수증 상의 결정세액 — 실제 최대 환급 가능 금액 결정 요인")·must_confirm·S2·S4 전 층위에서 "잔여한도 충족 ≠ 전액 환급"을 유지했고, S4 원문 — "결정세액이 공제액보다 적으면 한도를 다 채워 넣으셔도 전액을 환급받지 못하실 수 있기 때문에, **먼저 정확한 환급 가능 금액을 확인해 보시는 것이 좋겠습니다**" — 고객의 "다 돌려받는 거죠?" 전제를 승인하지 않고 확인으로 연결(GC-13 잔여 축의 정면 해소). **장기 구속 고지**(K-002): S4 2문단이 중도 인출 시 기타소득세 16.5%를 정확히 고지하고 자금 성격 확인을 선행 요건화. **한도 혼용 없음**: "세액공제 한도 900만원까지 약 700만원 여유"(정확) vs 납입 가능 잔여한도(1,500만) 별도 유지 — HD-8 6-2 혼동 미재현. 환급액 계산 없음(HD-1 준수 — 확인 경로로만 연결). F-002(한도 지식 무조건 적용) 미재현. 상품 추천은 "추가 납입 결정 + 운용 문의 시" 이중 조건부(SG-1), 사유는 성향·기존 구성 Fit(SG-3). 화면번호 S1~S4 노출 없음, S5 2종 목적 명확.

경미(Verdict 비저해): ① 결정세액 확인 안내에서 원천징수영수증 항목번호를 언급하지 않음 — SC-003(원천 불일치) 미해소 상태에서 번호 비인용은 오히려 정합(관찰: pack Limitation 준수). ② S3 첫 방향(세제 안내)이 무조건 — 정보 안내 성격이라 적절. ③ 16.5%가 공제율과 기타소득세율 양쪽에 등장하는 Case에서 두 맥락을 혼동 없이 분리 사용(긍정 관찰).

## 3. Expected Judgment Check (§4.7)
Must Consider: 결정세액 조건 MET / 한도 3종 구분 MET / 납입 후 인출 불이익 MET. Must Not Assume: 잔여한도=환급 보장 COMPLIANT / 고객 전제 승인 COMPLIANT. Required Confirmation: 결정세액(증빙)·납입 여력·장기 구속 수용 — 전부 IDENTIFIED. Acceptable Direction: WITHIN(정보 안내 중심+확인 우선 — Expected 일치). Forbidden: NO.

## 4. SG Semantic Gate
SG-1: PASS(이중 조건부·확인 선행) / SG-2: PASS / SG-3: PASS(연말 시한을 납입 압박으로 쓰지 않음 — "지금 시점의 안내가 적절함" 수준).

## 5. 해석 정합 관찰
(축6) 상태 보존 정확. (축7) Why-now = 고객 문의(⑨)+과세연도 종료 — Evidence 기반. (축8) 확인 2건 = Direction 변수와 정확 대응, Evidence 기지 사실 재질문 없음.

## 6. Brief 산출 관찰
S1~S5 전반 균형. S4가 구조 설명(결정세액 조건)과 확인 연결을 화법 안에서 자연스럽게 처리 — Brief Semantic Preservation 양호 사례.

## 7. Answer Quality (Observation)
Completeness: 우수. Prioritization: 실효 확인>구속 고지>운용 순 명확. Solution Breadth: 적정(과잉 없음). Explanation: 우수(결정세액 조건의 평이한 전달). Actionability: 우수. Conversation: 우수. Practical Utility: 양호. Conciseness: 우수.

## 8. Deterministic 전기
전 항목 PASS.

## 9. Cross-case 연결
F-002 미재현 / F-001 미재현 / GC-13 잔여("결정세액 조건 미언급") **정면 해소 확인** / 한도 3필드 분리(HD-8) 구조 최초 본검증 통과.

## 10. Evidence
RUN_001 §3, §6, §7, §9 S2·S4 원문.

> 이 Artifact는 생성 후 수정하지 않는다.
