# Customer State Interpretation / Management Judgment — Design Check (Phase B)

- Status: **Phase B 산출물 (2026-08-31)** — 새 9-Block Input이 기존 Judgment 6유형(불변)으로 어떻게 연결되는지의 설계 점검. **새 Rule-base 대량 추가가 아니다** — Input이 풍부해졌는데 Reasoning이 구 Input 전제에 머무는 것을 막기 위한 해석 지침이며, SYSTEM_ROLE v3(Phase F 상당)와 Evaluator 해석 기준의 원천이다.
- 검증 방법: 각 축을 기존 18개 Case(+REV-002 Regression)의 실사례에 대입해 "이 지침이 있었으면 그 Case에서 무엇이 달라졌는가"를 병기했다.
- 불변: Judgment 6유형(개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가), Judgment-first, 방향 중립, HD-7, Hard Constraint.

---

## 축 1. Current State × Recent Change 통합 독해

- **지침**: 상태(②)는 결과이고 변화(③④)는 그 결과의 형성 과정이다. 해석은 항상 "현재 상태 서술 → 그 상태를 만든 최근 변화의 연결"의 2단으로 구성한다. 변화가 상태를 설명하면(입금→현금 증가) 그 연결을 명시하고, 설명하지 못하면(현금은 많은데 최근 Flow 없음 = 장기 형성) **형성 시점이 오래됐다는 사실**까지만 서술한다.
- **경계**: 변화가 없다고 "방치"가 되지 않는다 — "최근 90일 내 관련 Flow가 관찰되지 않음"이 서술의 상한.
- **사례 대입**: CASE_001(10개월 전 운용지시·현금 75%)에서 이 지침이 있었다면 "최근 변화 없음 = 장기 형성 상태, 원인은 미확인"으로 서술되어 "방치" 확정이 원천 차단된다. GC-03은 "3일 전 입금이 현금 100%를 설명"으로 즉시 연결된다.

## 축 2. Money Flow ↔ 현재 잔액 추론의 한계

- **지침**: reconciliation(금액 일치)은 시스템이 준 **산술 사실**이므로 그대로 사용한다("현금성 3,000만은 8-10 만기상환 입금액과 금액이 일치한다"). 그 다음 단계 — "따라서 이 현금은 그 만기자금이다"까지는 **Inference로 표기**해 사용 가능(합리적 추론), "따라서 재예치 대기 중이다/쓸 곳이 없다"는 **금지**(자금 목적은 Decision Variable).
- **단계**: 산술 일치(Fact, 시스템) → 동일 자금 추정(Inference, Agent 표기) → 자금의 목적(Unknown → 고객과 확인).
- **사례 대입**: GC-11에서 사유 분해가 해준 일("연금지급 1,800만=지급 대기")을 reconciliation이 일반화한다 — 단 GC-11의 "대기"는 지급 예정 Event(⑧)가 있어서 Fact였음을 주의: **⑧에 대응 Event가 있으면 연결은 Fact 수준, 없으면 Inference 수준**이 구분 기준이다.

## 축 3. Digital Sequence의 Situation Interpretation 활용

- **지침**: Sequence는 "고객이 무엇을 탐색해 왔는가"라는 **행동 서사**로 상황 해석에 쓴다 — 탐색 주제(수익률·상품·이전), 시간 순서, 실행 도달 여부(진입 후 미실행 = 탐색이 결정으로 이어지지 않은 상태)까지. 해석 산출물은 "~에 대한 관심/탐색이 관찰된다"와 "탐색이 실행으로 이어지지 않았다"는 관찰 서술이다.
- **활용처**: 상담 접점 소재(S4에서 "최근 수익률을 자주 확인하신 것 같습니다" 류), 확인 질문의 우선순위(탐색 주제를 먼저 확인).
- **사례 대입**: GC-05의 "수익률 조회 6회 + 변경 화면 미진입"은 이 지침으로 "성과에 대한 관심은 관찰되나 변경 탐색은 없음 → 확인 우선"이라는 해석이 표준이 된다(RUN_002가 실제로 이렇게 함 — 지침은 이를 명문화).

## 축 4. Signal → Intent 비승격 경계 (Critical Boundary 유지)

- **지침**: Sequence가 아무리 강해도(이전 메뉴 진입 포함) 산출 가능한 최대 해석은 "~가능성/관심"이다. Intent로 기록되려면 ⑨(CRM)나 고객의 직접 발화·신청 Event(④)가 필요하다. **Signal 만으로 Judgment가 '개입 필요'가 되려면, 개입의 근거가 Signal이 아닌 다른 Evidence(시한·제도·자산 상태)에 있어야 한다** — Signal은 접점 타이밍의 근거는 될 수 있어도 관리 필요성의 근거가 될 수 없다(HD-7의 Signal 판).
- **사례 대입**: P2 GC-19의 통과 조건이 곧 이 지침이다. GC-05 TM 제거 후에도 이 경계는 Digital Signal에 그대로 적용된다.

## 축 5. CRM ↔ System Evidence 충돌·시점차 처리

- **지침**: CRM은 "그 시점에 직원이 그렇게 기록했다"는 사실이다. 해석 시 3요소를 함께 읽는다 — ① 작성 경과일(⑨의 A-Fact), ② 이후 발생한 System Event(④: 성향 재분석·매매·신청), ③ 이후 행동 신호(⑥). **CRM 이후의 System Evidence가 CRM 기록과 다른 방향을 시사하면, 어느 쪽도 채택하지 않고 '재확인'이 유일한 해석 결론이다** — 이때 Judgment는 보통 '추가 확인 우선'이 된다. CRM이 최근이고 이후 상충 Evidence가 없으면 CRM 기반 해석을 유지하되 진술임을 표기.
- **순서 원칙**: 시점이 다른 Evidence는 항상 시간순으로 배열해 읽는다(오래된 CRM을 현재로 당겨오지 않는다).
- **사례 대입**: GC-04(6개월 전 메모, 이후 상충 Event 없음 → 메모 기반 유지 판단 정당) vs P2 GC-20(3년 전 메모, 이후 성향 상향+TDF 조회 → 재확인이 유일 결론). 두 Case가 이 지침의 양 끝 검증이다.

## 축 6. Fact / Signal / Inference / Unknown 상태 유지

- **지침**: 입력의 evidence_type(fact/signal/derived)이 해석의 출발 상태다. Agent가 생성하는 해석은 반드시 넷 중 하나의 상태를 가진다 — Fact(입력 그대로/산술 결합), Signal(행동 기반 관심 관찰), Inference(합리적 추론 — "~로 보인다/추정된다" 표기 의무), Unknown(확인 필요). **상태는 파이프라인 끝(Brief 산문)까지 보존된다**(Epistemic Preservation — HD-8 (a)-1). 상태 상승(Signal→Fact, Inference→Fact)은 새 Evidence 없이 불가.
- **사례 대입**: GC-14 "무주택"(CRM 진술 → Brief에서 '진술' 유지 — 선택 Regression에서 검증됨)이 표준 사례. REV-002의 잔여 병목(Brief Semantic Preservation)이 이 축의 존재 이유.

## 축 7. 다중 Event의 Why-now·우선순위

- **지침**: 복수의 시한·변화가 동시에 있을 때 우선순위는 **①시한 임박도(D-n, 되돌릴 수 없는 마감 우선) → ②고객 이익 영향 크기(금액·세제 효과) → ③고객 접점 자연스러움(문의 주제·탐색 주제와의 연결)** 순으로 정한다. 단 이것은 나열 순서 규칙이지 판단 대체 규칙이 아니다 — 주 포인트 1개를 정하되 나머지를 버리지 않고 부 포인트/후속관리로 수용한다(F-003 대책 유지). Why-now는 반드시 ③④⑧의 실제 Event/변화/시한에서 나와야 한다(캠페인·영업 목적 불가 — HD-7).
- **사례 대입**: GC-09(발화 주제=성향 상향 vs 부차 시한=11월 만기)에서 주 포인트는 고객 발화 연결(③접점)이지만 만기(①시한)가 부 포인트로 반드시 생존해야 했다 — REV-002에서 ⑧구조로 해소된 것을 해석 지침으로 명문화. P2 GC-22가 본검증.

## 축 8. Direction 확정 전 Decision Variable 도출

- **지침**: Management Direction이 달라지게 만드는 미확인 변수만이 Required Confirmation이다. 도출 절차: ① 각 후보 Direction에 대해 "이것이 틀리게 되는 조건"을 묻는다 → ② 그 조건이 System Evidence로 닫히면 확인 불요 → ③ 닫히지 않으면 [고객과 확인](Decision Variable) 또는 [상담 전 확인](Operational — 시스템/단말로 닫을 수 있는 것)으로 분류. **이미 Evidence에 있는 것을 확인 목록에 넣지 않는다.** 확인 항목 수는 Direction 분기 수와 대응해야 한다(분기 없는 확인 나열 금지, 확인 없는 분기 금지 — Branch Preservation의 확인측 대응).
- **사례 대입**: GC-17(은퇴 시기 → 빈티지가 달라짐 = 정당한 확인) vs GC-05의 잔여 F-004("자금 목적의 기간" 누락 — 기간이 Direction을 바꾸므로 도출됐어야 함). 역예: 만기일을 고객에게 묻는 것(Evidence에 있음 — 금지).

---

## 종합: 해석 파이프라인 (v3 프롬프트에 반영될 순서)

```
9-Block 읽기 (①~⑧ 시스템 관찰 → ⑨ 보조)
→ 상태×변화 연결 (축1·2) + 행동 서사 (축3·4) + CRM 시점 배치 (축5)
→ 상태 표기 유지 (축6)
→ Why-now·우선순위 (축7)
→ Management Judgment (6유형 — 불변)
→ Decision Variable 도출 (축8)
→ Direction/후보/화법 (Brief 영역)
```

Evaluator 사용법: 각 축은 EVAL의 해석 품질 판정 기준으로도 쓰인다(예: 축5 위반 = CRM 과신, 축4 위반 = Signal 승격). Answer Quality 8축과는 별개 — 이쪽은 정합성, 그쪽은 품질.

---

## Gate ① 보강 — Semantic Gate 3건 (HD-PRE-P2-GATE1, 2026-08-31)

Diagnostic Pilot(DIAG-01~03) Gap Review에서 위 8축에 더해 확정된 Evaluator Semantic Gate 기준. 축의 재정의가 아니라 **축6(상태 유지)·축8(Decision Variable)의 Output-side 확장**이다.

### SG-1. Decision Variable / Conditionality Preservation (G1 — Core Semantic Principle)
- **기준**: 축8에서 도출된 미확인 Decision Variable이 Direction/Product/화법을 실질적으로 바꾸는 경우, 그 변수가 확인되기 전에 특정 Branch가 확정되면 위반. S3의 조건부 구조와 S4 화법의 조건성이 함께 보존되어야 하며, 필요 시 화법은 "확인 질문 → 확인 결과에 맞는 설명·추천" 순.
- **판정 사례 (Pilot 실측)**: DIAG-01 — S2에서 "은퇴시점 고객과 확인"을 도출하고도 S4 첫 화법이 "TDF2045를 추천드립니다"로 확정 = 위반. Target: "은퇴를 어느 시점 정도로 예상하고 계신지 먼저 여쭤봐도 될까요?" → "2045년 전후라면 TDF2045 계열을 후보로".
- **성격**: Branch Preservation·Epistemic Preservation의 Section 간 확장. Answer Quality Observation이 아니라 Semantic Correctness Gate.

### SG-2. Unsupported Semantic Labeling (G2 — 의미 승격 통제)
- **기준**: Evidence가 뒷받침하지 않는데 자금의 의미·목적·관리상태를 확정하는 표현("운용 대기 중"·"미운용 자금"·"대기성 자금"·"방치된 자금")이 있으면 Semantic Review. Evidence 기반의 관찰 상태 서술("입금 이후 추가 매매·운용지시가 확인되지 않았습니다")은 정상.
- **경계**: 금지어 Dictionary 확장이 아니다 — "남아 있다"도 문맥상 객관적 사실일 수 있다. 판단 기준은 단어가 아니라 **의미 승격 여부**. deterministic 층은 "방치" 등 고위험 표현만 유지(runtime `validate_forbidden_words`), 나머지는 Evaluator 판단.

### SG-3. Bank-Objective Rationale (G4 — HD-7 Output-side)
- **기준**: Management Direction 또는 Product Candidate의 supporting rationale이 Customer Need/Benefit/Fit이 아니라 Bank Objective("이탈 방지"·"AUM 유지"·"실적"·"판매 확대")로 정당화되면 위반.
- **구분**: 고객이 이전을 고려한다는 사실 = Situation Evidence로 사용 가능 / "떠나지 않게 해야 한다" = Recommendation Reason 불가.
- **판정 사례 (Pilot 실측)**: DIAG-03 — 추천 사유 "이탈 방지 및 고객 수익 제고 가능" = 위반. Target: "전출 사유가 정기예금 금리에 국한되어 있고, 현 보유 예금(2.6%)보다 높은 특별제공 금리(3.6%)로 동일한 니즈를 충족할 수 있기 때문".

참고: G3(화면 Reference S5 단일 위치)는 해석 축이 아니라 구조 규칙 — deterministic `validate_screen_refs`와 `design/EMPLOYEE_BRIEF_SPEC.md` v2 배너에서 관리.

### SG 판정 보강 — FC-1 (P2 Batch 3, 2026-08-31)

P2 Batch 3에서 3/8 Case 재현된 **FC-1(S4 화법층의 확실성 인플레이션)**을 SG-1·SG-2 판정에 명시 편입한다 (신규 Gate 아님 — 기존 Gate의 판정 위치 보강):
- SG-1 판정 시 **S4 scripts/conditional_scripts를 반드시 별도 확인**한다 — S1~S3에서 보존된 조건성·Unknown이 S4에서 소실되는 패턴이 P2의 주 위반 위치였다 (GC-20: 분기 축소 / GC-21: [상담 전 확인] 사항의 선행 설명).
- SG-2 판정에 **Knowledge 등급 승격**을 포함한다 — T3 단독·PROVISIONAL·CONFLICT 지식이 S4에서 확정·최적 표현("가장 유리합니다")으로 승격되면 위반 (GC-25; HD-3의 화법층 적용).
- GC-18 계열(관찰 상태 → "방치·관리 소홀·수익률 저하 우려" 자동 승격, 판단 reasoning 포함)은 축6/SG-2의 기존 범위 — FC-2(Interpretation→Judgment 승격)로 위치만 구분해 관찰한다.
