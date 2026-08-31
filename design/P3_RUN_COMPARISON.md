# P3 실 RUN 비교 — P3-A·P3-B Selector pack vs Human pack (2026-08-31)

- 실행: GEMINI_API_KEY 확보 후 gemma-4-31b-it 실호출. **양 모드(A=Human pack / B=Selector pack) 동일 시점 신규 RUN**으로 비교 — Frozen RUN_001/002와의 직접 대조는 모델 비결정성 혼입을 피하기 위해 참고로만 사용. Frozen `cases/*/runs` 무수정.
- 기록: `prototype/p3_runs/` (run record 14건 + selection log 8건 — 전 프롬프트·원출력 포함). GC-21 selector 1회 네트워크 절단(IncompleteRead) 재시도 — P2 GC-02/07 timeout 재실행 관례와 동일 처리.
- 이 문서는 P3-A(`P3A_SELECTION_REPORT.md` §4~6)·P3-B(`P3B_SELECTION_REPORT.md` §6~8)의 "RUN 미검증" 잔여 축을 닫는다.

## 1. Deterministic 결과 (14 RUN)

- C1/C2/C3·금지어·LaTeX·Evidence ID·screen_refs: **14/14 PASS** — Selector pool에 자연 회수된 미끼(TDF 3등급, GC-18·22)도 모델이 후보로 올리지 않음(C2 회피 유지).
- supply_refs FAIL 3건: GC-25 manual·GC-25 selector·GC-23 selector — 전부 동일 패턴 **K-ID를 S5 tip_id 슬롯에 기재**(tips가 빈 supply Case에서만 발생). GC-25는 A/B 양쪽에서 발생 → **baseline 소비 변동성이며 Selector 귀속 아님**. F-011(슬롯 혼동)의 tip_id 변형 — validator가 전 건 차단(안전망 정상). 신규 관찰로 기록.

## 2. P3-A (OK/KG Selection) — Case별 판정

| Case | Judgment A→B | Gap/Authority 축 | 판정 |
|---|---|---|---|
| GC-21 | 동일 (추가 확인 우선/정보 안내 중심) | **B의 S4 조건 화법에서 "매수 시점이나 평가 기준에 따라 차이가 발생할 수 있는데" 원인 설명 생성 — KG-001 [사용 경계] 위반.** A는 원인 명명 회피("다르게 나타나는 기준 안내" 약속까지) | B에서 **FC-1 재현** — Pack에는 KG-001 전문이 정확히 있었음 → **Consumption/S4 Semantic Failure** (Selection Failure 아님; Study ⑥-10 예측과 일치: Gap 1급 명시로도 S4 화법 압력은 못 막음) |
| GC-23 | **변화**: 추가 확인 우선/고객 결정 지원 → 개입 필요/고객 결정 지원 | 양쪽 모두 부분이전 가능/불가 비확정·확인 연결 유지 ✓. B의 '개입 필요'는 "현금이전이 고객의 ETF 유지 의사와 다르게 처리될 위험" 근거 — Evidence 기반으로 방어 가능하나 Judgment 변화로 기록 | 경계 위반 없음. over-selected OK-009(과세)는 미사용(F-002 미발생). B의 supply_refs FAIL은 §1의 슬롯 혼동 |
| GC-24 | 동일 (정보 안내 중심/고객 결정 지원) | 양쪽 결정세액 조건·장기 구속 고지 유지 ✓. **A(manual)가 "최대 115만 5천 원 환급 가능" 산출** — HD-1 경계 관찰(이론상 최대 단서 有, baseline 변동성) / B는 계산값 없이 더 깨끗 | B 우세. over-selected OK-015·OK-011 오용 없음 |
| GC-25 | 동일 (고객 결정 지원/정보 안내 중심) | **A·B 모두 7/1 발급을 확정 서술 + 방향 추천("등록 후 해지 추천"/"세금을 최대한 줄이는 방법")** — T3 단독 시점 규칙의 승격, KG-004 동봉(B)에도 발생 | **FC-1 재현 (양 모드)** — Selector 귀속 아님·KG로도 미차단. 반면 B는 over-selected OK-015로 "법정 사유 시 전체 해지 대신 필요 금액만 중도인출" 대안을 지식 근거로 추가 — **over-selection의 긍정적 Solution Breadth 사례** |

**P3-A RUN 축 종합**: Judgment 안정 3/4·변화 1/4(방어 가능) / Hallucination(무근거 사실 생성) 신규 0 / F-002(over-selected 항목 오용) 0 / FC-1 3건(B 2·A 1) — **전부 Pack이 정확한 상태에서의 S4 소비 문제**로, P2 FC-1과 동일 위치. Selection 층 도입이 만든 신규 실패는 관찰되지 않음.

## 3. P3-B (Product Retrieval) — Case별 판정

| Case | Judgment A→B | Agent 선택 (A → B) | 판정 |
|---|---|---|---|
| GC-18 | 동일 (개입 필요/정보 안내 중심) | TDF④+단기채⑥+GIC → TDF④+GIC (12개 pool에서 2개 선별) | 정상 — 나열 없음, Fit reason 고객 기반(성향·은퇴시점·원리금보장 선호 조건부), ISA 확인 조건부 유지, 미끼 3등급 TDF 미선택 |
| GC-20 | 동일 유형·순서만 교체 | TDF③+단기채⑥ → **TDF 4종 전부 나열** | **Over-selection의 소비 전이 실증** — pool의 동일 유형 시리즈 4종을 모두 후보로 나열, '원금 보전 유지' 분기용 저위험 후보(채권형 3종 pool 존재)는 미선택 → 분기-후보 정합 약화. 조건부 구조 자체는 유지(의향 확인 후) |
| GC-22 | 동일 (추가 확인 우선/개입 필요) | GIC+단기채+TDF → GIC 1종+TDF 1종 (10개 pool, GIC 5종 중 1종만) | 정상 — GIC 라인업 나열 없음, D-10 우선·퇴직급여 조건부 유지, 미끼 미선택 |
| GC-25 | (양 모드 프롬프트 동일 — 빈 Pool) | 상품 없음 유지 | 빈 Pool 정상 소비 — 억지 후보 0 |

**P3-B RUN 축 종합**: Direction 역전 0 / 수익률 단독 추천 0(금리 언급은 조건부 선호·신용등급과 병기) / Fit reason 전 건 고객 Evidence·조건 기반 / Hard Constraint 유지 / **Consumption Failure 1건(GC-20 유형 내 나열)** — P3-B Report §7-1(pool 폭 규칙)의 필요 증거가 RUN에서 확보됨.

## 4. Failure 분류 갱신

| 관찰 | 분류 | 귀속 |
|---|---|---|
| GC-21(B)·GC-25(A·B) S4 확정 승격/Gap 메움 | **S4 Semantic Failure (FC-1 재현 — 이제 P2 1회+P3 재현으로 정식 F-번호 부여 요건 충족 후보)** | Selection 아님 — SYSTEM_ROLE 원칙 19 강화가 별도 Human Gate 대상 (P2 Summary §5(a)) |
| K-ID→tip_id 슬롯 (GC-23 B·GC-25 A·B) | **Consumption(형식) — F-011 tip 변형** | baseline 포함 — tips 빈 supply Case 한정, validator 차단 중. OUTPUT_INSTRUCTION s5 주석 보강 후보(Operational) |
| GC-20(B) TDF 4종 나열 | **Consumption — pool 희석의 소비 전이** | P3-B over-selection이 원인 제공 → pool 폭 규칙(최소 Revision §7-1) Human 결정 필요 |
| GC-24(A) 환급액 산출 | HD-1 경계 관찰 (baseline) | Selector 무관 — Observation으로만 기록 |
| Retrieval/Authority/Gap/State/Constraint Failure | **0건** | — |

## 5. 결론

1. **P3-A·P3-B 종료 조건 충족 (제안)**: 잔여였던 RUN-level 검증 완료 — 두 Selector 모두 Judgment·Hard Constraint·Epistemic 경계를 훼손하지 않았고, 신규 실패는 전부 소비(S4·슬롯·나열) 층에 위치하며 그중 2종은 baseline에도 존재.
2. **Human Gate 상정 3건**: (a) FC-1 정식 F-번호 부여 + 원칙 19 S4 강화 여부 (b) P3-B pool 폭 규칙(유형당 상한/대표 선정 — 수익률 정렬 금지 하의 기준) (c) P3-A 매칭 정밀도 규칙. (a)는 Selection과 독립.
3. **Knowledge Architecture v1 Freeze**: RUN 검증 1회전 완료로 보류 사유 ①이 해소 — (b)(c) 결정 반영 후 Freeze 상정 가능. 수동 유지 영역(HT/TALK/SCR·Need 생성)의 범위 명시는 Freeze 문서에 포함할 것.
