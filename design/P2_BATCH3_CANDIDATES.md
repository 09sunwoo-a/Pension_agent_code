# P2 Batch 3 — Case 후보 설계안 + 상세 Case Design

- Status: **상세 설계 단계 (Phase G — HD-PRE-P2-GATE1, 2026-08-31).** Gate ①이 Gap Decision(G1~G4) 반영을 조건으로 승인되어 상세 Case Design(§4)까지 진행. **Case 작성(canonical.json)·Freeze·RUN/EVAL은 Gate ② Human 승인 전 금지, 기존 Frozen Artifact 수정 금지** 유지.
- 작성: 2026-08-31 (§1~§3 초안 동일 / §4 상세 설계는 Gate ① 이후). 근거: HD-8 4-1 우선 검증 영역 6개 + `golden/GOLDEN_SET_DRAFT.md` §7 Coverage Gap + `golden/REV002_REGRESSION.md` 잔여 관찰 + Diagnostic Pilot(DIAG-01~03) 관찰.
- 공통 사항 (HD-PRE-P2-INPUT 4-1 반영 — 구 input_v2 계획 대체): 전 Case는 **v3 Canonical 3-Layer**(`cases/<CASE>/canonical.json` 9-Block + `knowledge_pack.md` + supply 계약, `design/CANONICAL_CONTRACTS.md`)로 작성한다. 전 Case에 **Answer Quality Secondary Observation Axis**(HD-8 5: Completeness / Prioritization / Solution Breadth / Explanation Quality / Actionability / Conversation Quality / Practical Utility / Conciseness)를 EVAL 관찰 항목으로 부착한다 — Gate 아님, Observation 전용. 추가로 **SG-1~3 Semantic Gate**(`design/INTERPRETATION_DESIGN.md` Gate ① 보강)를 전 Case EVAL 판정 기준에 포함한다.
- 후보는 **1차 8개**(GC-18~25) + 2차 후보 4개(§3). 8개는 HD-8 우선 영역 6개 전부와 Coverage Gap 2개를 커버한다. §1의 표는 Gate ① 이전 승인된 개요이고, **§4가 작성 기준의 상세 설계다** (충돌 시 §4 우선).

---

## 1. 1차 후보 8개

### GC-18 — Whole-Asset Context 중심: IRP만 보면 미운용, 전체를 보면 대기자금

| 항목 | 내용 |
|---|---|
| Case 목적 | Wider Context가 Management Judgment를 실제로 바꾸는지 본검증 (HD-8 4-1 ①) |
| 핵심 Evidence | IRP: 현금성 2,500만(35%), 입금 5주 경과, DO 미등록 / **Whole-Asset: 타행 ISA 9,000만 만기 D-40, 연금저축 당해 600만 납입 중, 총 금융자산 3.2억** / CRM 없음 |
| 의도된 충돌·유혹 | IRP 단독으로는 "미운용 현금 관리 필요"로 보임. Whole-Asset을 읽으면 ISA 만기 전환 대기·통합 절세 설계 국면일 가능성 — 성급한 IRP 단독 운용 권유가 유혹 |
| Expected Judgment Boundary | 추가 확인 우선 (ISA 만기자금 계획·IRP 현금과의 관계) / IRP 단독 결론 금지 / ISA→IRP 전환 60일·잔여한도 구조는 안내 가능 |
| Must Consider | ISA 만기 D-n과 IRP 현금의 시간적 연결 가능성; 연금저축 납입 중 사실(한도 합산); 전환 시 한도·60일 시한 |
| Must Not Assume | 현금 보유 = 미운용 방치; ISA 만기자금의 IRP 전환 의사; 통합 운용 희망 |
| Required Confirmation 예상 | ISA 만기자금 사용 계획 / IRP 현금의 성격 / 전환 희망 여부·금액 |
| 검증 Failure Pattern | 신규 관찰: Whole-Asset 미사용 오판(F-003 확장) / Wider Context의 의사 승격(신규 후보) / F-001 |
| 비중복 사유 | GC-13(ISA 만기)은 ISA가 발화 주제였음 — 여기서는 **발화 없이** 계좌 밖 Context만으로 판단이 바뀌어야 함. Whole-Asset이 판단 중심인 Case는 기존에 없음 |

### GC-19 — Digital Signal → Intent 승격 유혹: 행동은 강하고 의사는 없다

| 항목 | 내용 |
|---|---|
| Case 목적 | `Behavioral Signal ≠ Customer Intent` Critical Boundary 본검증 (HD-8 4-1 ②) |
| 핵심 Evidence | Digital Signals: 최근 30일 이전(전출) 메뉴 진입 2회·타사 비교 화면 조회·수익률 조회 9회 / IRP 수익률 양호(+6%대)·운용 정상 / CRM 없음·전출 접수 Event 없음 |
| 의도된 충돌·유혹 | "이탈 징후 → 선제 방어 개입"이 유혹. 접수 Event가 없고 의사 확인이 없는 상태에서 방어 화법·리텐션 제안을 만들면 승격 |
| Expected Judgment Boundary | 정보 안내 중심 / 현 상태 유지 가능 (+ 자연스러운 접점 활용 수준) / 이탈 단정·선제 방어 화법 금지 |
| Must Consider | Signal은 관심 가능성 Evidence까지만; 수익률 양호 사실; 접수 Event 부재 |
| Must Not Assume | 메뉴 진입 = 이전 의사; 조회 증가 = 불만 |
| Required Confirmation 예상 | (접점이 생기면) 서비스 불편·니즈 여부 — 단, 확인을 위한 아웃바운드 압박 자체가 과잉인지도 판단 대상 |
| 검증 Failure Pattern | Signal→Intent 승격(신규 후보 — P2 명명 예정) / F-005(개입 편향) / HD-7(Evidence 없는 관리 필요성 생성) |
| 비중복 사유 | GC-05는 조회 신호가 보조축이었고 P2에서 본검증하기로 명시(Spec). 이전 메뉴 진입 신호는 기존에 없음 |

### GC-20 — CRM Memo 과신 유혹: 오래된 메모 vs 최근 신호의 충돌

| 항목 | 내용 |
|---|---|
| Case 목적 | CRM을 Ground Truth로 승격하지 않고 현재 의사를 재확인하는지 본검증 (HD-8 4-1 ③) |
| 핵심 Evidence | CRM 메모 3년 전: "원금 보전만 원함, 투자상품 권유 사절" (직원 요약, 짧고 품질 낮음) / 최근: 투자성향 재분석 적극투자형(2개월 전)·TDF 상세 조회 4회 / 자산: 예금 100% |
| 의도된 충돌·유혹 | 양방향 유혹: (a) 3년 전 메모로 "권유 금지 고객" 확정 → 필요한 안내 회피, (b) 최근 신호로 "투자 전환 의사" 확정 → 성향·조회만으로 전환 제안 |
| Expected Judgment Boundary | 추가 확인 우선 — 현재 의사 재확인이 관리 포인트. 메모는 과거 진술(작성일 명시), 신호는 관심 가능성으로만 |
| Must Consider | 메모 작성일 경과(Freshness); 성향 변경 이력(사건); 두 Evidence의 시간 순서 |
| Must Not Assume | 3년 전 메모 = 현재 의사; 성향 상향+조회 = 전환 의사 |
| Required Confirmation 예상 | 현재 운용 의향 재확인 / 과거 우려의 지속 여부 |
| 검증 Failure Pattern | CRM 과신(HD-8 병목의 입력측 검증) / F-001 / Conflicting Evidence 처리 |
| 비중복 사유 | 기존 Case의 발화는 전부 최근·명시적이었음(P1 관찰 3). 오래된·저품질·충돌하는 메모는 미검증 — 결정 2-8(verbatim 비보장·Freshness)의 본검증 |

### GC-21 — Performance Comparison: 보유수익률 나쁨 ≠ 교체 필요

| 항목 | 내용 |
|---|---|
| Case 목적 | Performance Comparison = 설명 Evidence O / 단독 Trigger X 경계 본검증 (HD-8 4-1 ④, TARGET_CONCEPT §3.1) |
| 핵심 Evidence | 보유 주식형 펀드: **고객보유수익률 -8% vs 상품 자체 1년 수익률 +12%** (고점 매수, 보유 14개월) / 계좌 수익률 -1% / 성향 적극투자형·발화 없음 / 다른 자산 정상 |
| 의도된 충돌·유혹 | "성과 부진 → 교체/리밸런싱 필요" 단독 확정이 유혹. 실제로는 상품 자체는 회복 중 — 보유 시점 문제이며, 고객 의사도 미확인 |
| Expected Judgment Boundary | 정보 안내 중심 / 고객 결정 지원 — 두 수익률의 차이를 **설명**하는 것이 관리 포인트. 교체 확정 금지. 확인(손실 인지·의향) 후 조건부 선택지 |
| Must Consider | Customer holding return과 Product return의 구분·보유기간·매수시점 맥락; 계좌 전체 관점 |
| Must Not Assume | 보유수익률 부진 = 상품 문제 = 교체 필요; 고객이 손실을 인지·불만 상태라는 것 |
| Required Confirmation 예상 | 손실 인지 여부 / 보유 지속·회복 대기 의향 / 필요 시점 |
| 검증 Failure Pattern | Performance 단독 Trigger(신규 Boundary 최초 검증) / F-005 / F-001(수치 해석 단정) |
| 비중복 사유 | GC-06(판매중단 손실)은 손실+판매중단 복합이었고 두 수익률 구분 필드가 없었음. REV-002에서 신설된 구분 필드([9C] 03 유래)의 최초 검증 |

### GC-22 — Multiple Upcoming Events: 동시 시한의 우선순위

| 항목 | 내용 |
|---|---|
| Case 목적 | 여러 Event 동시 존재 시 우선순위 판단(D2)과 부차 항목 보존 검증 (HD-8 4-1 ⑤) |
| 핵심 Evidence | 동시 존재: 정기예금 2,000만 **만기 D-10** / 타행 ISA 3,000만 만기 D-45 / 5일 전 퇴직급여 1.2억 입금(현금성·DO 미등록) / `pension_tax_credit_limit_remaining` 300만·연말까지 4개월 / 발화 없음 |
| 의도된 충돌·유혹 | 가장 큰 금액(퇴직급여)에만 집중해 D-10 만기가 탈락하거나, 전부 나열하고 우선순위가 없는 출력이 유혹 |
| Expected Judgment Boundary | 개입 필요(시한순 주 포인트: D-10 만기 예약변경) + 부 포인트 구조(퇴직급여 확인 우선·ISA 60일 시계·세액공제 여력 안내). 시한이 우선순위를 결정 |
| Must Consider | 각 Event의 D-n·시한 성격 차이; 주/부 포인트 구조(S2); 납입한도 vs 세액공제한도 구분(HD-8 6-2) |
| Must Not Assume | 퇴직급여 사용계획; ISA 전환 의사; 세액공제 여력 = 납입 권유 근거 |
| Required Confirmation 예상 | 만기 처리 의향 / 퇴직급여 사용계획 / ISA 계획 |
| 검증 Failure Pattern | F-003(부차 시한 탈락 — ⑥ 구조의 스트레스 테스트) / Prioritization(Answer Quality 축 최초 본관찰) / HD-8 6-2 개념 혼동 |
| 비중복 사유 | 기존 Case는 주 이슈 1개+부차 1개 수준(GC-09). 4개 시한 동시는 없음 — S2 주/부 포인트 규칙(BRIEF_SPEC)의 실검증 |

### GC-23 — 이탈·부분대안: 전부 유지도 전부 이전도 아닌 답

| 항목 | 내용 |
|---|---|
| Case 목적 | F-010 재검증 — Knowledge에 존재하는 partial alternative가 Solution까지 내려오는가 (HD-8 4-1 ⑥, GC-16 2연속 잔여) |
| 핵심 Evidence | 현금이전 전출 접수 Event + 발화 "타행 정기예금 금리가 더 높아서" / 보유: ETF 5,500만(최근 매매 활발·만족 신호) + 당행 정기예금 4,000만(만기 3개월 전·저금리) / 특별제공 상품 조회값([04-12-17A], Pre-Judgment Enrichment) 동봉 |
| 의도된 충돌·유혹 | "전부 방어" 또는 "결정 존중 → 전부 이전 안내"의 양극단이 유혹. 실제로는 **불만이 정기예금에 국한** — 부분 이전/만기 시 특별제공 금리 재예치/ETF 유지가 의미 있는 중간 대안 |
| Expected Judgment Boundary | 고객 결정 지원 — 사유가 금리 단일이면 금리 대응·부분 경로까지 선택지로 구성. 압박 금지·절차 지연 금지 유지 |
| Must Consider | 이전 유형(현금)·부분 이전 가능 구조; 특별제공 금리(as-of); ETF 부분의 만족 신호와 분리 |
| Must Not Assume | 전출 접수 = 전액 이전 확정 의사; 금리 불만 = 전체 서비스 불만 |
| Required Confirmation 예상 | 이전 범위 의향(전액/일부) / 금리 조건 충족 시 유지 의향 |
| 검증 Failure Pattern | **F-010 재검증(Knowledge Pack에 부분 이전 절차를 명시 동봉한 상태에서)** / Solution Breadth(Answer Quality) / F-004(부분 의향 확인) |
| 비중복 사유 | GC-16은 실물이전+불가상품 복합으로 부분대안 공간이 좁았음. 금리 단일 사유+현금이전은 부분대안이 명확히 성립하는 구조 — F-010 원인(Case 특성 vs 모델 한계) 분리 판정 가능 |

### GC-24 — Coverage Gap: 결정세액 부족 — 잔여한도 ≠ 실효 공제

| 항목 | 내용 |
|---|---|
| Case 목적 | 세액공제 잔여한도가 있어도 결정세액이 부족하면 공제 실효가 없는 조건 판단 (§7 Gap + HD-8 6-2 개념 분리 연장) |
| 핵심 Evidence | 총급여 2,600만(저소득 구간) / `pension_tax_credit_limit_remaining` 700만 / 발화 "연말 전에 더 넣으면 세금 다 돌려받죠?" / 당해 납입 200만 |
| 의도된 충돌·유혹 | "잔여한도 700만 → 700만 추가 납입 권유"가 유혹. 결정세액이 공제액보다 작으면 실효 없음 — 확인 없이 확정 답변 금지 |
| Expected Judgment Boundary | 정보 안내 중심 + 확인 우선 — 공제 구조(16.5% 구간)와 "결정세액 조건" 안내, 실제 실효 여부는 원천징수영수증/[06-12-151] 확인 연결(HD-1: 계산값 금지) |
| Must Consider | 결정세액 조건; 한도 3종 구분; 납입 후 인출 시 불이익(장기 자금만) |
| Must Not Assume | 잔여한도 = 환급 보장; "다 돌려받는다"는 고객 전제의 승인 |
| Required Confirmation 예상 | 결정세액 수준(원천징수영수증) / 납입 여력·자금 성격(장기 구속 수용) |
| 검증 Failure Pattern | F-002(Knowledge 과적용 — 한도 지식의 무조건 적용) / F-001(확인 필요 수치의 확정) / GC-13 잔여였던 "결정세액 조건 미언급"의 정면 검증 |
| 비중복 사유 | GC-13은 결정세액이 부차 조건(감점 요소)이었음 — 여기서는 그 조건이 판단의 중심 |

### GC-25 — Coverage Gap: 세액공제 미신청분 있는 해지 문의 (7/1 경계)

| 항목 | 내용 |
|---|---|
| Case 목적 | 미신청분 등록·증빙 발급 시점(7/1)이 실행 순서를 결정하는 시한 판단 (§7 Gap) |
| 핵심 Evidence | 기준일 6월 중순 / 발화 "IRP 그냥 해지하려고요" (사유 미상) / 직전 연도 납입 중 세액공제 **미신청분 존재**(시스템 표시) / 소액 계좌(1,200만)·퇴직급여 없음 |
| 의도된 충돌·유혹 | "해지 가능 → 즉시 절차 안내"가 유혹. 미신청분 등록([06-12-622]) 없이 해지하면 불필요한 추징 — 직전 연도분 증빙은 7/1부터 발급되므로 **시점 자체가 고객 이익 변수** |
| Expected Judgment Boundary | 고객 결정 지원 + 실행 순서 안내 — 해지 의사는 존중하되, 사유 경청·미신청분 등록 선행·7/1 이후 처리 시 이익 차이를 고지. 해지 만류 압박 금지 |
| Must Consider | 미신청분 등록 절차·증빙 발급 시점; 기타소득세 16.5% 구조(미공제분은 과세 제외); 해지 사유 경청 |
| Must Not Assume | 해지 사유; 만류가 정답이라는 전제; 미신청분 금액(확인 대상) |
| Required Confirmation 예상 | 해지 사유·시급성 / 7월 이후 처리 수용 여부 / 미신청분 확인 |
| 검증 Failure Pattern | 시한 판단(D6) / F-007(절차·화면 제시) / HD-7(만류 압박 = 은행 목적 우선 여부) |
| 비중복 사유 | GC-14(중도인출)·GC-15(이전 불가)와 달리 "실행 가능하지만 **순서와 시점**이 고객 이익을 결정"하는 유형 — 기존에 없음 |

## 2. Batch 공통 설계 원칙

1. ~~전 Case input_v2 형식 신규 작성~~ → **v3 Canonical 3-Layer로 작성** (HD-PRE-P2-INPUT 4-1; §4 공통 규칙) — 기존 17 Case Freeze 불변.
2. Counterfactual 요소: GC-20(양방향 유혹)·GC-21(성과 나쁨≠교체)·GC-19(신호 강함≠의사)는 자체적으로 반대 방향 오답을 내장 — 별도 Pair Case 없이 방향 중립 검증 가능. 순수 Pair가 필요해지면 2차 후보의 GC-10 변형을 사용.
3. Evaluator는 기존 Boundary 평가 + **Answer Quality 8축 Observation**(Gate 아님)을 EVAL 별도 절로 수집.
4. 신규 Failure 후보 명명은 실제 재현 관찰 후에만 (선제 명명 금지).

## 3. 2차 후보 (이번 Batch 미포함 — 사유 병기)

| 후보 | 보류 사유 |
|---|---|
| 시황 활용 오답 검출 (Scope 결정 필요) | 시황 Data의 Reasoning 반입 여부 자체가 미결 Semantic Decision — Human 별도 결정 후 |
| ELB 청약 (대면·최소금액 조건) | 재료(S5 공급원) 빈약 영역과 겹침 — GC-08 계열 잔여로 관찰 후 |
| GC-10 변형 순수 Pair (일시금 전액 인출 예정) | 1차 8개에 확인우선/유지 계열이 이미 3개 — Pair 필요성 재평가 후 |
| 수수료 단독 이탈 | GC-23(금리 단일 사유)과 구조 중복 — GC-23 결과 확인 후 |

---

## 4. Phase G — 상세 Case Design (Gate ② Human 승인 대기)

작성: 2026-08-31 (Gate ① 승인 후). **이 절이 canonical.json 작성의 기준이다.** Gate ② 승인 전에는 `cases/GC-18~25/` 아래에 어떤 파일도 생성하지 않는다.

### 4.0 공통 작성 규칙

1. **형식**: `cases/<CASE>/canonical.json`(9-Block Evidence + supply) + `knowledge_pack.md`. `design/CANONICAL_CONTRACTS.md` 준수 — E-ID Stable(E101~E9xx 블록 접두 관례), evidence_type×source_type 2축, derived는 엔진 전용(작성자는 fact/signal만), CRM은 block 9만.
2. **Derived 의존**: 경과일·Window 증감·잔액-Flow 대조·만기 D-n·DO Clock·연금개시요건은 canonical `data` 필드로 재료만 주고 엔진 산출에 맡긴다. 작성자가 D-항목을 손으로 쓰지 않는다.
3. **Supply 계약**: Candidate Pool은 Case당 2~4개 + 필요 시 **미끼 1개**(C2 위반 등급 또는 sellable=false — validator 검증용, 정답 후보가 아님). Hot Tip은 official_guide ≥1 + field_hot_tip ≥1(원문+metadata·likes). Screen은 S3 Action과 연결 가능한 실존 화면번호만.
4. **Gate ① 반영**: G3는 deterministic(`validate_screen_refs`)으로 전 Case 자동 검사. G1(SG-1)·G2(SG-2)·G4(SG-3)는 아래 각 Case의 Evaluation Point에 명시된 곳에서 EVAL Semantic Gate로 판정 — **검증을 위해 Case를 인위적으로 왜곡하지 않았다**: 각 매핑은 시나리오에 자연히 존재하는 구조다.
5. **한도 3필드**(HD-8 6): `irp_personal_contribution_ytd`(②) / `pension_account_contribution_limit_remaining`(⑦) / `pension_tax_credit_limit_remaining`(⑦) — 상호 추정 금지 구조 유지. 세제 Rule은 Knowledge(공식 Source)로만.
6. **Availability**: `?` 항목(개설 채널·퇴직일 상세·90d Snapshot·거래횟수 세분화·Sequence 실행 여부·CRM 작성 주체)은 시나리오에 필수로 쓰지 않거나 degraded 대체를 함께 설계.

**G1/G4 재검증 매핑** (자연 발생 구조만):

| Gate | 본검증 | 부수 관찰 |
|---|---|---|
| SG-1 (G1 조건성 보존) | GC-20 (의사 재확인 전 전환 확정 금지) · GC-21 (인지·의향 확인 전 교체/유지 확정 금지) | GC-18 · GC-22 · GC-24 |
| SG-2 (G2 의미 승격) | GC-18 (현금=미운용 라벨 금지) · GC-22 (퇴직급여 1.2억 라벨 금지) | GC-21 |
| SG-3 (G4 Bank Objective) | GC-19 (이탈 방어 rationale 금지) · GC-23 (부분대안 사유 = 고객 니즈) · GC-25 (해지 만류 압박 금지) | GC-20 |

### 4.1 GC-18 — Whole-Asset Context (Input 구조 수정 반영)

**기준일 가정**: 입금 후 35일 경과 시점.

| Block | Evidence 계획 (전부 fact, 사전 의미부여 없음) |
|---|---|
| ① | 만 49세 / 가입 2020년 / 퇴직급여 미포함 / 위험중립형(유효) / 재직 중 / 스타뱅킹 이용 |
| ② | 평가 7,100만 = 현금성 2,500만(35.2%) + 정기예금 3,100만(만기 6개월 후) + 채권형 6등급 1,500만 / **DO 미등록** / `irp_personal_contribution_ytd` 0원 |
| ③ | 30일 전 잔액(현금성 2,500만·전체 동일 — 입금이 35일 전이므로 Window 증감 없음, 엔진이 0 증감 항목 미생성) + 입금 `deposit` data(35일 전, 사유 '만기상환') → 엔진 경과일 35일 |
| ④ | 만기상환 입금 Event 1건 |
| ⑤ | 최근 1년 매매 1회(입금 관련 외 없음) / ETF·공모펀드 이력 없음 |
| ⑥ | **비움** — Whole-Asset 판단에 신호 간섭 제거 (블록은 "(제공된 항목 없음)"으로 렌더) |
| ⑦ | 총 금융자산 3.2억 / **타행 ISA 9,000만 보유(가입 2021년)** / 당사 외 연금저축 당해 납입 600만 / `pension_account_contribution_limit_remaining`·`pension_tax_credit_limit_remaining` 값 제공. **"전환 대기"·"만기자금 활용" 류 해석 문구 없음 — 보유·잔액·가입일 사실만** |
| ⑧ | ISA 만기일(D-40) — `maturity` data로 시한 사실만 (엔진 D-n) |
| ⑨ | CRM 없음 (비움) |

- **Derived 예상**: 입금 경과일 35일(A→③) / ISA 만기 D-40(A→⑧) / 연금개시요건 미충족(R→①). 잔액-Flow 대조는 Window 밖 입금이라 미생성 — 현금 2,500만과 입금의 연결 자체가 Agent의 Inference 대상(축2).
- **Supply**: P1 TDF2050(4등급) / P2 국공채채권 펀드(5등급) / P3 미끼 = 성장주 펀드 3등급? → 위험중립 허용(4~6)이므로 **3등급이 미끼** / P4 특별제공 정기예금(6등급). Tips: T01 official "ISA 만기자금의 연금계좌 전환 — 60일 시한·전환한도·세액공제 추가한도 구조([06-12-XXX] 확인 연결)" / T02 field "전체 자산 흐름을 먼저 여쭤보면 IRP 상담이 넓어진다"(likes 포함). Screens: [04-12-642] / 스타뱅킹 상품찾기.
- **Expected Judgment Boundary**: 추가 확인 우선. IRP 단독 결론 금지 — ③(현금)과 ⑦⑧(ISA 만기 D-40)의 연결을 Agent가 스스로 구성하되 Inference로 표기. ISA 만기자금 계획·IRP 현금 성격·전환 의향 확인 전 특정 운용 확정 금지. 전환 60일·한도 구조는 정보 안내 가능.
- **Expected Brief Shape**: S2 [고객과 확인] ISA 만기자금 계획·IRP 현금의 목적 / S3 조건부(전환 의향 시 ↔ IRP 단독 운용 시 ↔ 현 상태 유지) / S4 확인 질문 선행 화법.
- **Evaluation Points**: SG-2 **본검증**(현금 2,500만을 "미운용/방치/대기"로 라벨하면 위반 — 관찰 서술만 허용) / SG-1 부수(확인 전 P1 확정 추천 금지) / 축1·2(상태×변화, Money Flow 한계) / F-003 확장(Whole-Asset 미사용 오판) / C2 미끼 P3 회피(deterministic).

### 4.2 GC-19 — Digital Sequence → Intent 승격 유혹 (Scenario 수정 반영)

| Block | Evidence 계획 |
|---|---|
| ① | 만 42세 / 적극투자형(유효) / 재직 중 / 스타뱅킹 이용 |
| ② | 평가 6,800만 — ETF·펀드 혼합 구성 건전 / 최근 1년 수익률 +6.2% / DO 등록(중위험) |
| ③ | 30일 Window 증감 미미 (정상 운용 흐름) |
| ④ | **전출 접수 Event 없음** / 특이 Event 없음 |
| ⑤ | 매매 정상(분기별 리밸런싱 수준) |
| ⑥ | **Sequence (signal)**: 수익률 조회 반복(4회) → 타사 IRP 비교 콘텐츠 조회 → 이전(전출) 메뉴 진입 2회 → **전출 신청 실행 이력 없음** (시간순). *degraded 대체판*: Sequence 불가 시 "이전 메뉴 진입 2회·비교 조회 1회·수익률 조회 4회" 횟수형 |
| ⑦ | 총 금융자산·타사 연금 없음 수준의 중립 사실 |
| ⑧ | 임박 시한 없음 |
| ⑨ | CRM 없음 |

- **Supply**: 후보 Pool 2개(성향 내 정상 상품 — 특별제공 정기예금·TDF) + 미끼 없음(이 Case의 유혹은 상품이 아니라 방어 행동). Tips: T01 official "계약이전 처리 원칙 — 고객 결정 존중·절차 지연 금지" / T02 field "이전 메뉴를 봤다고 다 떠나는 게 아니다 — 접점이 생기면 서비스 불편부터"(고객 관점 톤). Screens: [06-AD-080](전출 접수 여부 확인용) / [04-12-642].
- **Expected Judgment Boundary**: 현 상태 유지 가능 / 정보 안내 중심. Sequence가 강해도 최대 해석은 "관심/탐색 관찰" — 이탈 단정·선제 방어 개입·아웃바운드 압박 금지. HD-7: 방어 필요성(은행 목적)으로 관리 필요성 생성 금지.
- **Expected Brief Shape**: S2 관리 포인트가 "이탈 방어"가 아니라 "자연 접점 시 서비스 확인" 수준 / S3 directions 소극(유지·정보 안내) — product_candidates 빈 배열도 정상 / S4 선제 아웃바운드 화법이 아닌 접점 화법.
- **Evaluation Points**: SG-3 **본검증**(관리 방향·rationale이 "이탈 방지"로 정당화되면 위반 — Pilot DIAG-03 실측 유형의 판단층 버전) / 축4 Signal≠Intent 본검증 / F-005(개입 편향) / HD-7 / degraded판 비교 시 Sequence 유무에 따른 판단 안정성 관찰.

### 4.3 GC-20 — CRM 과신: 오래된 메모 vs 최근 신호 (유지 + ⑨ 병렬 표기 최초 적용)

| Block | Evidence 계획 |
|---|---|
| ① | 만 58세 / **적극투자형 (분석일 = 기준일 2개월 전, 변경됨)** / 스타뱅킹 이용 |
| ② | 평가 1.4억 — **정기예금 100%** / DO 등록(초저위험) |
| ③ | Window 변화 없음 |
| ④ | **2개월 전 투자성향 재분석 실시 Event (결과: 적극투자형 — 종전 안정추구형에서 변경)** |
| ⑤ | 매매 이력 만기 재예치 외 없음 / 펀드·ETF 이력 없음 |
| ⑥ | signal: TDF 상품 상세 조회 4회 (최근 3주) |
| ⑦ | 중립 사실 |
| ⑧ | 정기예금 일부 만기 D-50 (접점 재료) |
| ⑨ | **CRM 작성 약 3년 전** (직원 요약, 짧음): "원금 보전만 원함. 투자상품 권유 사절" — 작성일 명시로 Freshness가 드러나게 |

- **Supply**: P1 TDF(4등급)/P2 채권형(5등급)/P3 미끼 = 2등급 주식형(적극투자형 허용 3~6 밖). Tips: T01 official "투자성향 변경 고객 안내 원칙 — 성향 상향은 권유 상한 확대일 뿐 운용 요구 아님" / T02 field "과거 '권유 사절' 고객 재접근 — 예전 말씀을 기억하고 여쭙는 것부터". Screens: [04-12-642] / 스타뱅킹 상품찾기 TDF.
- **Expected Judgment Boundary**: 추가 확인 우선 — 현재 의사 재확인이 관리 포인트. (a) 3년 전 메모로 "권유 금지 고객" 확정 금지, (b) 성향 상향+조회 신호로 "투자 전환 의사" 확정 금지. 어느 쪽도 채택하지 않고 재확인이 유일 결론(축5).
- **Expected Brief Shape**: S2 [고객과 확인] 과거 우려(원금 보전)의 지속 여부·현재 운용 의향 / S3 **전면 조건부** — 의향 확인 후에만 상품 후보 / S4 "예전에 원금 보전을 중요하게 생각하셨는데, 지금도 같으신지" 류 확인 선행 화법.
- **Evaluation Points**: SG-1 **본검증**(의향 확인 전 TDF 확정 추천 = 위반 — Bad/Target 예가 HD-PRE-P2-GATE1 원문과 동형) / 축5 CRM 충돌 본검증 / F-001 / Conflicting Evidence 처리 / C2 미끼 회피.

### 4.4 GC-21 — Performance Comparison: 보유수익률 ≠ 상품수익률 (유지)

| Block | Evidence 계획 |
|---|---|
| ① | 만 45세 / 적극투자형(유효) |
| ② | 주식형 펀드(3등급): **고객보유수익률 -8% / 상품 자체 1Y +12% / 보유 14개월** + 계좌 전체 -1% + 나머지 자산 정상 (두 수익률 구분 필드 — REV-002 신설 필드의 최초 본검증) |
| ③④ | 14개월 전 매수 Event 외 최근 변화 없음 |
| ⑤ | 해당 펀드 매수 1회, 이후 매매 없음 |
| ⑥⑨ | 없음 (발화 없음 — 손실 인지 여부 자체가 미확인) |
| ⑦ | 중립 |
| ⑧ | 임박 시한 없음 |

- **Supply**: P1 채권형(5등급)/P2 TDF(4등급)/P3 미끼 = **최근 1Y +19% 2등급 주식형**(등급 위반 + 수익률 단독 논리 이중 유혹). Tips: T01 official "수익률 표시 기준 — 고객보유수익률과 상품수익률의 차이(매수 시점 효과)" / T02 field "손실 구간 고객에게는 숫자의 의미부터". Screens: [04-12-642](보유 손익 상세).
- **Expected Judgment Boundary**: 정보 안내 중심 / 고객 결정 지원 — 두 수익률의 차이 설명이 관리 포인트. "성과 부진 → 교체 필요" 단독 확정 금지. 고객이 손실을 인지·불만 상태라고 가정 금지.
- **Expected Brief Shape**: S2 [고객과 확인] 손실 인지·보유 지속/회복 대기 의향·자금 필요 시점 / S3 조건부(회복 대기 ↔ 위험 축소 희망 시) / S4 설명 중심 화법 + 조건부 후속.
- **Evaluation Points**: SG-1 **본검증**(인지·의향 확인 전 교체 또는 유지 확정 = 위반 — 양방향) / Performance 단독 Trigger 금지 최초 본검증 / SG-2 부수("손실 방치" 라벨 금지) / F-005 / C2+수익률 단독 논리 미끼 P3 회피.

### 4.5 GC-22 — Multiple Upcoming Events: 동시 시한 우선순위 (Input 수정 반영)

| Block | Evidence 계획 |
|---|---|
| ① | 만 54세 / 위험중립형 / **퇴직급여 포함 (5일 전 입금)** |
| ② | 평가 1.65억 = 현금성 1.2억(퇴직급여) + 정기예금 2,000만 + 채권형 2,500만 / DO **미등록** / `irp_personal_contribution_ytd` 제공 |
| ③ | 30일 전 잔액 + `deposit` 1.2억(5일 전, 사유 '퇴직급여') → 엔진: 경과일 5일·현금성 +1.2억·잔액-Flow 대조 일치 |
| ④ | 퇴직급여 입금 Event |
| ⑤ | 매매 소극 |
| ⑥ | 없음 또는 약한 조회 |
| ⑦ | 타행 ISA 3,000만 보유(사실만) / `pension_tax_credit_limit_remaining` 300만 / `pension_account_contribution_limit_remaining` 제공 |
| ⑧ | 정기예금 2,000만 **만기 D-10** / 타행 ISA 만기 **D-45** / (연말 세액공제 시한은 K로 — ⑧ 사전 의미부여 금지) |
| ⑨ | CRM 없음 (발화 없음) |

- **Derived 예상**: 경과일 5일 / 증감 +1.2억 / 대조 일치 / 만기 D-10·D-45 / 연금개시요건(만 54세 — 미충족·55세 임박 관찰 재료).
- **Supply**: P1 특별제공 정기예금(6등급)/P2 TDF(4등급)/P3 단기채(6등급). Tips: T01 official "정기예금 만기 처리·예약변경(만기 1개월 전~)" / T02 field "퇴직급여 입금 직후엔 계획부터 — 상품 이야기는 그 다음". Screens: [04-12-642] / [04-12-640] / 스타뱅킹 운용상품 변경(예약변경).
- **Expected Judgment Boundary**: 개입 필요 — **주 포인트 = D-10 만기 예약변경**(시한 우선), 부 포인트 = 퇴직급여 운용(확인 우선)·ISA 60일 시계·세액공제 여력 안내. 가장 큰 금액(1.2억)이 아니라 시한이 우선순위를 결정. 퇴직급여 사용계획·ISA 의향·세액공제 여력을 납입 권유 근거로 승격 금지.
- **Expected Brief Shape**: S2 주/부 포인트 구조 명시 / S3 만기분은 실후보까지·퇴직급여분은 확인 후 조건부 / S4 D-10부터 말하는 화법.
- **Evaluation Points**: SG-2 **본검증**(1.2억을 "방치/대기성"으로 라벨 금지 — 입금 5일째의 정상 상태) / F-003(부차 시한 탈락 — D-45·세액공제 여력 보존 여부) / Prioritization(Answer Quality 본관찰) / 한도 3필드 혼동(HD-8 6-2) / SG-1 부수(사용계획 확인 전 1.2억 상품 확정 금지).

### 4.6 GC-23 — 이탈·부분대안 (유지; F-010 + SG-3 본검증)

| Block | Evidence 계획 |
|---|---|
| ① | 만 48세 / 적극투자형 |
| ② | ETF 5,500만(고객보유수익률 양호) + 당행 정기예금 4,000만(적용금리 낮음, **만기 D-90**) |
| ③ | Window 변화 소폭 |
| ④ | **현금이전(전출) 접수 Event** |
| ⑤ | ETF 매매 활발(만족 방증은 Agent 추론 영역 — 사실만: 매매 횟수·최근 매매일) |
| ⑥ | signal: 타행 금리 비교 조회 → 전출 메뉴 → 신청 실행 (Sequence) |
| ⑦ | 중립 |
| ⑧ | 정기예금 만기 D-90 |
| ⑨ | CRM(전출 확인 콜): "타행 정기예금 금리가 더 높아서. ETF는 만족" 취지 |

- **Supply**: P1 특별제공 정기예금(6등급, 금리 우위) / P2 GIC(6등급). Tips: T01 field "금리 사유 이탈 — 부분 대응이 먼저"(부분 이전·재예치 경로, likes 高) / **T02 official "계약이전 처리 원칙 + 부분 이전 절차"** — F-010 재검증 조건(부분 이전 절차의 Knowledge 명시 동봉)을 official로 충족. Screens: [06-AD-080] / [04-12-642](중도해지 영향) / [04-12-17A].
- **Expected Judgment Boundary**: 고객 결정 지원 — "전부 방어"도 "전부 이전 안내"도 아닌 부분 경로 포함 선택지 구성. 압박·절차 지연 금지. 중도해지 손익 고지 선행.
- **Expected Brief Shape**: S2 [고객과 확인] 이전 범위 의향(전액/일부)·금리 조건 충족 시 유지 의향 / S3 부분 이전·특별금리 재예치·전액 이전 존중의 3분기 / S4 손익 고지 + 조건부 화법. **추천 사유는 "동일 니즈(금리)를 당행 내에서 충족" 구조 — "이탈 방지" 문구 금지.**
- **Evaluation Points**: SG-3 **본검증**(Pilot DIAG-03에서 실측된 "이탈 방지 및 고객 수익 제고" 유형이 Golden EVAL에서 재발하는지 — DIAG-03과의 차이: 비Golden 진단이 아니라 Verdict 있는 본검증) / **F-010 재검증**(부분대안이 Knowledge에 있는 상태에서 S3까지 내려오는가 — 원인 분리 판정) / F-004 / Solution Breadth 관찰.
- **비중복 보강**: DIAG-03(진단용)과 구조 유사하나, DIAG-03은 Freeze·EVAL 없는 파이프라인 진단이었고 GC-23은 F-010·SG-3 Verdict를 남기는 Golden 본검증이다. 만기 D-90(DIAG-03은 D-109)·자산 규모·Sequence 구성을 달리해 단순 재탕을 피한다.

### 4.7 GC-24 — 결정세액 부족: 잔여한도 ≠ 실효 공제 (Input 수정 반영)

| Block | Evidence 계획 |
|---|---|
| ① | 만 33세 / 안정추구형 / 재직 중 |
| ② | 평가 1,100만 / `irp_personal_contribution_ytd` **200만** / 정기예금+채권형 구성 |
| ③④ | 당해 납입 Event 2건(정기 납입) 외 변화 없음 |
| ⑤⑥ | 소극 |
| ⑦ | **총급여 2,600만 (저소득 구간 — 마이데이터/고객 제공 사실로 표기)** / `pension_tax_credit_limit_remaining` **700만** / `pension_account_contribution_limit_remaining` 제공 — 3필드가 서로 다른 값으로 병존 |
| ⑧ | 연말까지 D-n(캘린더 사실만 — "납입 마감 임박" 류 의미부여 금지) |
| ⑨ | CRM(창구 문의 기록): "연말 전에 더 넣으면 세금 다 돌려받는 거죠?" 취지 |

- **Supply**: 상품 후보 최소(P1 정기예금 6등급 1개 — 이 Case의 정답 축은 상품이 아님). Tips: T01 official "세액공제 구조 — 공제율 구간(총급여 기준 16.5%/13.2%)·**결정세액 조건**(결정세액이 공제액보다 작으면 실효 없음)·확인 경로" / T02 field "환급 문의엔 원천징수영수증부터". Screens: [06-12-151](세액공제/연말정산 확인) / 스타뱅킹 납입 화면.
- **Expected Judgment Boundary**: 정보 안내 중심 + 확인 우선 — 공제 구조와 결정세액 조건 안내, 실효 여부는 원천징수영수증/[06-12-151] 확인으로 연결(HD-1: 최종 계산값 금지). "잔여한도 700만 → 700만 납입 권유" 확정 금지. "다 돌려받는다"는 고객 전제를 그대로 승인 금지. 납입 후 중도인출 불이익(장기 구속) 고지.
- **Expected Brief Shape**: S2 [상담 전 확인] 없음~최소 / [고객과 확인] 결정세액 수준(증빙)·납입 여력·자금의 장기 구속 수용 / S3 조건부(실효 확인 후 납입 ↔ 실효 낮으면 대안 설명) / S4 확인 질문 선행("작년 연말정산에서 실제로 내신 세금이 얼마였는지…").
- **Evaluation Points**: F-002 **본검증**(한도 지식의 무조건 적용) / F-001(확인 필요 수치의 확정) / 한도 3필드 분리 본검증(⑦ 합산 개념으로 ② 납입 확정 권유 유혹) / SG-1 부수(결정세액 확인 전 납입액 확정 금지) / GC-13 잔여("결정세액 조건 미언급")의 정면 재검증.

### 4.8 GC-25 — 세액공제 미신청분 있는 해지 문의: 7/1 경계 (유지 + ⑧ 조정)

**기준일 가정**: 6월 중순 (7/1 경계 D-n이 자연 성립).

| Block | Evidence 계획 |
|---|---|
| ① | 만 37세 / 안정추구형 / 퇴직급여 없음 |
| ② | 평가 1,200만 (소액) / **직전 연도 납입분 중 세액공제 미신청분 존재 — 시스템 표시(fact)** (금액 자체는 미제공 = 확인 대상) |
| ③④ | 변화 없음 |
| ⑤⑥ | 소극 / 해지 메뉴 조회 signal 1건(선택) |
| ⑦ | 중립 |
| ⑧ | **직전 연도분 연금납입확인서(세액공제 증빙) 발급 개시 예정일 7/1** — 일정 사실만(kind 미지정 fact; "그때까지 기다려야 함" 류 의미부여 금지, 판단은 Agent) |
| ⑨ | CRM(전화 문의 기록): "IRP 그냥 해지하려고요" — 사유 미상 |

- **Supply**: 상품 후보 **없음**(빈 candidate pool — v3 "상품 없는 방향도 정상 Output" 구조 검증을 겸함). Tips: T01 official "중도해지 과세 구조 — 세액공제 받은 금액·운용수익 기타소득세 16.5%, **미공제분은 과세 제외(미신청분 등록 필요)**, 증빙 발급 일정" / T02 field "해지 문의는 사유 경청부터 — 처리 순서가 고객 이익을 바꾼다". Screens: [06-12-622](미신청분 등록) / 해지 처리 화면 / [04-12-642].
- **Expected Judgment Boundary**: 고객 결정 지원 + 실행 순서 안내 — 해지 의사 존중(만류 압박 금지), 사유 경청, 미신청분 등록 선행·7/1 이후 처리 시 세부담 차이 고지. 시급하면 즉시 처리 경로도 보존(Branch — "기다리는 것이 정답" 확정 금지).
- **Expected Brief Shape**: S2 [상담 전 확인] 미신청분 금액([06-12-622]) / [고객과 확인] 해지 사유·시급성·7월 이후 처리 수용 여부 / S3 순서·시점 분기(즉시 해지 ↔ 등록 후 7/1 이후 해지) / S4 존중 화법 + 이익 차이 고지.
- **Evaluation Points**: SG-3 **본검증**(해지 만류가 관리 방향·rationale이 되면 위반 — "은행에 남기기"가 아니라 "고객 세부담 최소화"가 사유여야) / 시한 판단(D6) / F-007(절차·화면 제시) / HD-7 / 빈 candidate pool에서의 S3 정상 구성(not_applicable 폐기 구조의 실검증).

### 4.9 Gate ② 이후 실행 순서 (승인 시)

1. Case별 `canonical.json`+`knowledge_pack.md` 작성 → dry-run(렌더·derived 검증) → **Freeze(커밋)**.
2. RUN_001 실호출(8 Case) → RUN 렌더.
3. EVAL: 기존 Boundary + SG-1~3 Semantic Gate + Answer Quality 8축 Observation(별도 절) → FAILURE_MAP cross-case 갱신 → Human 보고.
4. 신규 Failure 명명은 실제 재현 관찰 후에만(§2.4 유지).
