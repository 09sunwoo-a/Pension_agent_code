# EVAL_001 — GC-21

## 1. Evaluation Metadata
- Case: GC-21 (Performance Comparison — Knowledge Gap 검증) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 067c54b3c0f6… FROZEN / knowledge_pack sha256 6d4d428ffea2… FROZEN (OK-006·007 PROVISIONAL, TALK-003~005 인용)
- Basis: P2_BATCH3_CANDIDATES §4.4 (HD-P2-GATE2 (2) 조정 반영); SG-1~3

## 2. Verdict
**PARTIAL**

판단층과 구조는 우수하다: Judgment "추가 확인 우선 / 정보 안내 중심" — Expected 일치. 교체 확정 없음(조건부만), 유지 분기 보존, Performance 단독 Trigger 없음(reasoning이 "단순 상품 교체보다는 정보 제공과 의사 확인"으로 명시), 손실 인지 여부를 Unknown으로 유지, 미끼 P03(2등급 +47%) 회피, `current_situation`·S1은 "지표 간 괴리가 관찰됨"·"차이가 확인됩니다"까지만 서술(절제 정확). S2 [상담 전 확인]에 "**산정 기준 및 차이 발생 원인 확인**"을 스스로 넣은 것은 조정된 Boundary("필요한 경우 산정 기준을 먼저 확인")의 정확한 이행이다.

그러나 **S4에서 이 Case의 본검증 축이 무너졌다**: S4 2문단 원문 — "**매수 시점 등에 따라 고객님이 체감하시는 수익률과 차이가 발생한 것으로 보입니다**." K-001 Limitation이 명시한 "차이의 원인(매수 시점 효과 등)을 지식처럼 설명하지 않는다"의 정면 위반 — **Knowledge Gap 상황에서 임의의 원인 설명을 생성**했다(HD-P2-GATE2 (2)가 정의한 검증 목적의 위반 재현). "~것으로 보입니다" 추측 표지는 유지했으나, 자신이 S2에서 [상담 전 확인]으로 지정한 "산정 기준·원인 확인"을 **확인 전에 고객 대면 화법에서 설명**하는 S2↔S4 역전(SG-1 구조 동반)이다. 이어지는 "일시적인 변동성에 흔들리기보다"도 Evidence 없는 성격 규정(일시적).

## 3. Expected Judgment Check (§4.4 조정본)
| Must Consider | Result |
|---|---|
| 두 지표의 산정 기준 미확인 상태 인지 | MET (S2 확인 항목) — 단 S4에서 자기 위반 |
| 단순 비교를 교체 근거로 사용 금지 | MET — 교체는 고객 불안(의사) 조건부, 지표 비교 근거 아님 |
| 계좌 전체 관점 | MET (계좌 -1%·정기예금 만기 언급) |

Must Not Assume: 보유수익률 부진=상품 문제=교체 필요 COMPLIANT / 고객이 손실 인지·불만 상태 COMPLIANT(Unknown 유지) / **차이의 원인 — VIOLATED**(S4). Required Confirmation: 인지 여부·의향·타임호라이즌 IDENTIFIED. Acceptable Direction: WITHIN(판단층). Forbidden: NO.

## 4. SG Semantic Gate
- **SG-1: VIOLATED (S4 국지)** — [상담 전 확인]으로 남긴 산정 기준·원인이 확인 전 S4에서 설명됨 (확인→설명 순서 역전).
- SG-2: PASS 경계 — "다소 저조한 상태"는 사실 서술; "일시적인 변동성"은 성격 규정 경미.
- SG-3: PASS — 추천 사유 전부 customer 니즈·특성 기반. P01(1Y -5.8% 채권형)을 "안정적인 이자수익 대안"으로 추천한 사유-실적 긴장은 AQ 관찰.

## 5. 해석 정합 관찰
(축6) 해석층 상태 보존 정확 — 위반은 화법층. (축7) 아웃바운드("연락드렸습니다")는 손익 정보 안내 목적 — 정보 안내 중심 Judgment와 정합, Performance가 접점 사유가 된 것은 Expected 범위 내(교체 Trigger 아님). (축8) 확인 2건 = 분기 2개 대응.

## 6. Brief 산출 관찰
S1 절제 우수 / S2 확인 설계 우수 / S3 유지·조정 양분기+카드 2종(조건 명시) / **S4 §2 참조** + "현재 상태를 유지하시겠습니까, 아니면 조정을 검토하시겠습니까?" 양방향 질문 종결은 좋음 / S5 화면 1건(산정 기준 확인 목적 명시 — 좋음) / 화면번호 노출 없음.

## 7. Answer Quality (Observation)
Completeness: 양호. Prioritization: 명확. Solution Breadth: 2방향+2카드. Explanation: S4 원인 설명이 오히려 위반 — "명료해 보이는 설명"이 Knowledge Gap을 덮는 패턴. Actionability: 양호. Conversation: 양방향 질문 좋음. Practical Utility: 보통. Conciseness: 양호.

## 8. Deterministic 전기
전 항목 PASS. (개념 설명 생성은 semantic — deterministic로 검출 불가; Evaluator Gate가 잡는 것이 설계 의도대로 작동)

## 9. Cross-case 연결
Performance 단독 Trigger **미재현** / F-001 미재현 / **Knowledge Gap 원인 설명 생성 재현** — GC-20·GC-25와 함께 "S2 확인 설계 ↔ S4 실행 정합" + "Gap 메움(gap-filling) 화법" Cluster (Batch Summary).

## 10. Evidence
RUN_001 §3, §6, §7, §9 S2·S4 원문.

> 이 Artifact는 생성 후 수정하지 않는다.
