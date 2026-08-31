# P2 Batch 3 — Case 후보 설계안 (Human 승인 대기)

- Status: **HOLD 유지 (HD-PRE-P2-INPUT, 2026-08-31).** 재분류 **방향만 승인** — 유지 4(GC-20·21·23·25) / Input 구조 수정 3(GC-18·22·24) / Scenario 수정 1(GC-19), 상세는 `design/PRE_P2_REFINEMENT_PROPOSAL.md` §5. **Case 작성·Expected Output·Evaluation 설계·Freeze·RUN/EVAL 금지** — Employee Brief가 별도 Human Design Gate에서 변경될 예정이므로 새 Brief 구조 확정 이후에만 착수.
- 작성: 2026-08-31. 근거: HD-8 4-1 우선 검증 영역 6개 + `golden/GOLDEN_SET_DRAFT.md` §7 Coverage Gap + `golden/REV002_REGRESSION.md` 잔여 관찰.
- 공통 사항: 전 Case는 처음부터 REV-002 Evidence Pack(input_v2 형식·8-섹션·machine 블록)으로 작성한다. 전 Case에 **Answer Quality Secondary Observation Axis**(HD-8 5: Completeness / Prioritization / Solution Breadth / Explanation Quality / Actionability / Conversation Quality / Practical Utility / Conciseness)를 EVAL 관찰 항목으로 부착한다 — Gate 아님, Observation 전용.
- 후보는 **1차 8개**(GC-18~25) + 2차 후보 4개(§3). 8개는 HD-8 우선 영역 6개 전부와 Coverage Gap 2개를 커버한다.

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

1. 전 Case input_v2 형식 신규 작성(원본 case.md도 처음부터 REV-002 어휘로) — 기존 17 Case Freeze 불변.
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
