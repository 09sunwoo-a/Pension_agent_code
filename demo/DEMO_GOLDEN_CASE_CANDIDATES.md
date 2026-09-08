# Demo Golden Case Candidate Mining

> 상태: **Candidate 단계 (Freeze 아님)**. 최종 15개 선정과 고객 상세 설계는 Human Review 이후 별도 작업이다.
> 이 문서는 고객명·구체 금액을 만들지 않는다. Candidate 안의 수치는 전부 `knowledge/`·`sources/` 에 실존하는 제도 값이며 Registry ID 를 병기한다.

## 1. 목적

현재 Demo Target(`demo/`)이 보여주는 Case 밀도 — 김서연(타행 ISA 만기 × 세액공제 × ETF 조회), 이수민(정기예금 만기 × 현금성 대기 × DO 미등록), 박정호(퇴직급여 일반통장 수령 × 60일 과세이연 × 상담이력) — 를 Benchmark 로 삼아, 최종 Demo Portfolio 15개를 고를 수 있는 **후보 36개**를 발굴하고 **Shortlist 20개**를 제안한다.

찾는 것은 «단일 Rule 에 걸리는 고객» 이 아니라 **Trigger × Customer Context × Additional Evidence × Knowledge × Agent Discovery × Employee Action** 이 결합돼야 비로소 의미가 보이는 고객이다. 그리고 Portfolio 전체가 «상품을 바꾸세요» 로 수렴하지 않도록, 확인 우선·현 상태 유지·실행 제약 같은 **Negative / Preservation** 결과를 의도적으로 포함한다.

## 2. 탐색한 Repository 범위

| 우선순위 | 영역 | 실제로 읽은 것 | 용도 |
|---|---|---|---|
| 1 | `demo/` | README · DEMO_TARGET_SPEC · HTML_EXTRACTION_AUDIT · seed_cases 3종 | Case 밀도·Brief S1~S5·Chat·Badge 의 기준 |
| 2 | `knowledge/` | OFFICIAL_KNOWLEDGE (OK-001~031 전문) · PRODUCT_REGISTRY (PRD-001~034, 018~022·033·034 상세) · HOTTIP_REGISTRY (HT-001~049 메타·요약) · TALK_REGISTRY (TALK-001~032 audience·caution) · SCREEN_REGISTRY (SCR-001~091) · SOURCE_CONFLICTS (SC-001~005) · KNOWLEDGE_GAPS (KG-001~008) · DECISIONS_B | Grounding Status 판정 · Required Knowledge ID 연결 |
| 2 | `sources/` | `source_registry.md` SRC-001~098 색인 (원문은 Registry 가 가리키는 위치로만 Trace) | 원천 존재 확인 |
| 3 | `references/` | `06_주제별_추출지식/` 01~05 전문 · `planning/README.md` · planning xlsx 2건(더미 9 Cases · 타겟 룰베이스 14종) | 아이디어 발굴 — Grounding 근거로 쓰지 않음 |
| 4 | `golden/` + `cases/` | HUMAN_DECISIONS · GOLDEN_SET_DRAFT · P0/P1/P2 Batch Summary · REV Regression · cases/CASE_001·GC-01~24·DIAG-01~03 · FAILURE_MAP · CONSTRAINT_MAP | 기존 판단축·Critical Mistake·중복 확인 |
| 5 | `design/` | EMPLOYEE_BRIEF_SPEC · P2_BATCH3_CANDIDATES (기각·보류 후보 확인용) | Architecture 이해만 — 후보를 거르는 기준으로 쓰지 않음 |

HTML Dashboard-only 고객 15명(`demo/HTML_EXTRACTION_AUDIT.md` §3)의 Theme 도 Candidate Source 로 썼다. 단 그 안의 8월 11일 기준 dormant 데이터와 내부 충돌(C-11·C-12)은 가져오지 않고 Theme 만 취해 `sources/knowledge` 로 다시 구성했다.

## 3. Mining Method

```text
Round 1  Broad Mining        references 5개 파일 + planning xlsx + Hot Tip 49건 + TALK 32건 + OK 31건 + 기존 GC 24건 + HTML Theme 15건
                             → Situation Idea 약 120건 (본문 §7 각 Candidate 의 «Why This Case Exists» 에 출처 기록)
Round 2  Combination         단일 Situation 을 2~5개 Evidence 결합으로 승격 (예: DO 미등록 → 만기 임박 + DO 미등록 + 현금성 대기 + 재만기 T+1 규칙)
Round 3  Knowledge Enrich    OK / PRD / HT / TALK / SCR / KG / SC 를 붙여 Grounding Status 판정
Round 4  Demo Fit            S1~S5 + Chat 2~3문항이 자연스럽게 나오는지 검토
Round 5  Deduplication       판단능력이 같은 후보 병합·제거 (§14) → Candidate 36 → Shortlist 20
```

Grounding Status 기준:

| 등급 | 기준 |
|---|---|
| STRONG | 핵심 판단 지식이 OK(T1/T2) 에 있고 Screen·Talk 또는 Hot Tip 이 붙는다 |
| MEDIUM | 좋은 후보이나 일부 지식이 T3/Public 단독이거나 KG·SC 가 걸려 보강이 필요하다 |
| WEAK | references·HTML Theme 아이디어만 있고 공식 Grounding 이 부족하다 |

## 4. Demo Case 평가기준

각 Candidate 를 8축 × 5점 = 40점으로 채점한다. 점수는 **상대 순위용 휴리스틱**이며 Freeze 근거가 아니다.

| 축 | 5점의 의미 |
|---|---|
| 발견성 | 직원이 화면만 봐서는 못 찾고, Agent 가 여러 원장·행동·이력을 이어야 보인다 |
| 데이터 결합성 | 서로 다른 Evidence 3개 이상이 결합돼야 Story 가 성립한다 |
| Knowledge 활용성 | OK + PRD + HT + TALK + SCR 중 4종 이상이 실제로 쓰인다 |
| 직원 실용성 | 오늘 통화·내점에서 바로 쓸 화법·화면·순서가 나온다 |
| Agent 판단성 | 확인 우선·조건부·유지·실행 제약 같은 «데이터만으로 확정하지 않는» 판단이 들어간다 |
| Demo Wow | 발표에서 «이런 것까지?» 가 나온다 |
| 기존 Case 대비 차별성 | golden/cases 및 Seed 3명과 판단축이 겹치지 않는다 |
| Brief Fit | `demo/DEMO_TARGET_SPEC.md` §6 의 S1~S5 에 무리 없이 들어간다 |

Portfolio 관점의 추가 기준: Capability(§11)·Outcome(§12)·Knowledge(§13) Coverage 가 특정 축에 편중되지 않을 것.

## 5. Segment Candidate Taxonomy

Candidate 에서 자연스럽게 도출된 다축 Segment. 한 고객이 여러 축을 동시에 가진다. **이 표는 Rule 이 아니라 어휘**다 — Segment 가 곧 정답 Action 이 되지 않는다(`00_Core_Concept_Design.md` 의 «Customer → Action Rule Base 금지» 와 같은 취지).

| 축 | 값 (이번 Candidate 에서 쓰인 것) |
|---|---|
| Lifecycle | 재직기 · 은퇴준비기(50대) · 퇴직 직전(만기·DC 보유) · 퇴직 직후(60일 창구) · 연금개시 가능(만 55세·5년) · 연금수령기 · 재취업/이직 · 소득 공백기 · 사업자/법인대표 · 청년(39세 미만) |
| Portfolio State | 원리금 100% · 원리금 중심(80%↑) · 현금성 비중 높음 · 현금성 100% · 실적배당 중심 · 위험자산 한도 근접/초과 · 특정 펀드 편중 · 판매중단 펀드 보유 · TDF 단일 · DO 초저위험 지정 · AI일임 운용 중 · 장기 무지시 |
| Opportunity | 외부 만기자금(ISA·타행 예금·보험) · 재운용 시점(정기예금/GIC 만기) · 추가납입(잔여 한도·1,800만 예외) · 절세(세액공제·이월공제·미공제분 등록) · 과세이연(퇴직금 60일) · 연금개시 설계(수령한도·1,500만) · 이전/이탈(전출 접수·실물이전·계열사) · 수수료(비대면 전환·연금개시 면제) |
| Behavior | ETF 조회 · TDF 조회 · 수익률 반복 조회 · 상품변경 화면 진입 · 이전 메뉴 조회 · 앱 접속 급증 · 콜센터 문의 · 과거 발화(사용계획·거절·재취업) · 발화 후 행동 변화 |
| Risk / Constraint | 성향 상한(C2) · 위험자산 70% · 사용계획 확인 필요 · 환급 전 지급 제한 · 일임 중 제한 · 연금개시 후 추가입금 불가 · 6/30 이전 해지 추징(T3) · 비대면 권유 경계(OK-029) |

## 6. Badge Candidate Taxonomy

Badge 는 Dashboard 에서 직원이 1초에 읽는 Signal 이다. **Badge 는 Agent 의 최종 판단이 아니다** — 판단은 S2·S3 에서 Evidence 를 결합해 내린다. Event Badge 는 시간축에 따라 Label 이 바뀌고 사라진다(§10 원칙).

| Category | Badge 후보 (HTML AS-IS 표기 관례 «주체 + 이벤트 + D-n» 유지) | 생성 Evidence | 소멸 |
|---|---|---|---|
| Event | 타행 ISA 만기 D-n → ISA 만기자금 → ISA 전환기한 D-n | 타행 ISA 만기일(마이데이터/고객 발화) | 만기 후 60일 경과(OK-001) |
| Event | 정기예금 만기 D-n · GIC 만기 D-n · ELB 만기 D-n | IRP 원장 만기일 | 만기 처리 완료 또는 예약변경 등록 |
| Event | 퇴직급여 입금 D+n → 과세이연 시한 D-n | 입출금계좌 입금 + 퇴직 사실 | 재입금 완료 또는 60일 경과(OK-014) |
| Event | 만 55세 D-n · 연금개시 가능 | 생년월일 + 가입 5년(OK-013) | 개시 등록 |
| Event | 전출 접수 D+0 · 의사확인 대기 | [06-AD-080] 전출 알림(OK-002·031) | 취소 또는 이전 완료 |
| Event | 만기 후 대기 n주 · DO 자동적용 D-n | 만기 후 현금성 + DO 지정 여부(OK-005) | 운용지시 또는 DO 실행 |
| Opportunity | 세액공제 여력 n만 · 이월공제 가능 · 1,800만 예외 납입 가능 | 당해 납입액·한도(OK-008·018) | 연말 경과 |
| Opportunity | 과세이연 가능 · 연금개시 가능 · 수수료 면제 조건 충족 · 비대면 전환 가능 | OK-014·013·016 | 조건 소멸 |
| Behavior Signal | ETF 조회 · TDF 조회 · 수익률 조회 증가 · 상품변경 탐색 · 이전 메뉴 조회 · 앱 접속 급증 | 스타뱅킹 로그 | 기간 경과(예: 2~4주) |
| Attention | DO 미등록 · 현금성 대기 · 현금성 100% · 판매중단 펀드 보유 · 위험자산 한도 초과 · 성향-지정 불일치 · 장기 무지시 · 일임 운용 중 · 환급 대기 중 | 원장 상태(OK-005·028·017·012·006·027·014) | 상태 해소 |
| Attention | 사용계획 확인 필요 · 재취업 확인 필요 · 은퇴시점 미확인 | 상담이력·발화 | 확인 완료 |
## 7. Candidate 36개

표기 규약: `[HTML-Theme]` = HTML Dashboard-only 고객 Theme 참조, `[Seed]` = Seed 3명 구조 참조, `[GC-xx]` = 기존 Golden Case 와의 관계, `[Gap-n]` = golden digest §8.6 빈칸 번호. Grounding 등급 근거는 §8 Required Knowledge 의 authority 로 판단. 점수는 §4 기준의 상대 휴리스틱.

---

### DC-001 — 퇴직 예정 고객의 «퇴직 전 만기 보유 vs 퇴직 시 현금화» 선택

#### 1. Case Concept
당행 DC(또는 기업형IRP)에 정기예금을 보유한 퇴직 예정 고객에게, 퇴직일이 정기예금 만기보다 앞서 도래해 «퇴직 시 현금화 손실 vs 만기까지 보유» 와 «퇴직용 IRP 개설·과세이연 준비» 를 퇴직 전에 함께 정리해야 하는 것을 Agent 가 발견하는 Case.

#### 2. Why This Case Exists
```text
Reference:   06_주제별_추출지식 05_업무처리절차 (퇴직 전 절차) · 01_고객세그먼트 «퇴직 예정» 세그먼트
Knowledge:   OK-014(과세이연 5-Step) · OK-019(퇴직용/적립겸용 계좌 유형·서류) · OK-011(일반/특별중도해지 이율) · OK-022(DC→IRP 는 동일 제도 유형 간 이전이 아니라는 취지 — 공식 확인 필요, TALK-027 caution) · HT-021(퇴직 전 [04-12-642] 정기예금 만기 확인 → 만기 보유 권유) · HT-015(퇴직 직원 상담 자료)
Source:      SRC-003 CASE③ · SRC-011 · SRC-056 · SRC-027
Golden/Case: GC-03·12·22 는 모두 «이미 IRP 에 입금된 뒤». 퇴직 전 단계는 golden §7 에서 «마케팅 성격 → 의도적 제외» — [Gap-10]. Seed 박정호(퇴직 후 60일)의 «전 단계» Pair.
```

#### 3. Trigger
퇴직 예정일(사용자 신고·인사 데이터·고객 발화)이 D-45 이내로 들어옴 + 당행 DC 계좌 정기예금 만기가 퇴직일 이후.

#### 4. Customer Context
```text
퇴직 직전 · 50대 후반 · 안정추구형 · DC 원리금보장 중심 · 당행 IRP 미보유 또는 적립용만 보유
```

#### 5. Interesting Evidence Combination
```text
퇴직 예정 D-45
+ DC 정기예금 만기가 퇴직일 이후(예: 퇴직 후 4개월)
+ 당행 IRP 미보유(퇴직용 계좌 개설 필요)
+ 스타뱅킹 «퇴직연금 수령» 콘텐츠 조회
+ 퇴직 후 재취업 여부 미확인
```

#### 6. Potential Segment
`퇴직 직전` × `DC 원리금 중심` × `과세이연 예정` × `계좌 개설 필요` × `수령 콘텐츠 관심`

#### 7. Potential Badges
```text
Primary:   퇴직 예정 D-45
Secondary: DC 예금 만기 퇴직 후 · 퇴직용 IRP 미개설
Signal:    수령 콘텐츠 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-014 (60일·5-Step·환급 전 지급 제한) · OK-019 (퇴직용 계좌·서류: 퇴직소득원천징수영수증) · OK-011 (중도해지 이율 구조 — 퇴직 사유 해지가 특별중도해지인지는 원천 서술 없음, 단정 금지)
Product:            (해당 없음 — 퇴직 전 단계는 상품 제안 아님)
Hot Tip:            HT-021 (퇴직 전 만기 확인 루틴 · [04-12-646] 세금 상세정보) · HT-015 · HT-023(과세이연 실무, T3)
Talk:               TALK-027 (퇴직금을 타은행 IRP 로 받으려는 고객 — 현금화 경고; caution 참조) · TALK-006 (사용 계획 확인 선행)
Screen:             SCR-001 [04-12-642] · SCR-039 [04-12-646] · SCR-021 [06-12-501] · SCR-023 [04-12-648] · SCR-031 [00-12-210] 퇴직연금 신규
Knowledge Gap / Conflict: «DC 정기예금이 퇴직 시 전량 매도·현금화되는가» 는 TALK-027 caution 대로 공식 확인 필요 · 퇴직 사유 해지의 특별중도해지 해당 여부 미서술(OK-011 Limitation)
```

#### 9. Expected Agent Discovery
퇴직일과 예금 만기의 순서 관계가 «어느 쪽을 먼저 처리하느냐» 를 결정한다는 것. 퇴직 전에 (a) 만기 보유가 가능한지, (b) 퇴직용 IRP 개설과 과세이연정보 등록을 퇴직 전에 미리 걸어둘 수 있는지, (c) 현금화 시 이율 손실이 어느 정도인지([04-12-642] 예상조회)를 순서대로 확인해야 함을 짚는다.

#### 10. Required Confirmation
```text
Employee Check: DC 계좌 만기일·중도해지 예상조회 결과 · 퇴직 시 현금화 규칙(공식 확인) · 퇴직용 IRP 개설 서류
Customer Check: 퇴직 예정일 확정 여부 · 퇴직급여 수령 방식 희망(IRP/일시금) · 재취업 예정 · 퇴직 후 단기 사용 자금
```

#### 11. Potential Management Direction
```text
If 퇴직 후 사용 계획 없음 + 만기 보유 가능:
→ 퇴직용 IRP 개설·과세이연 정보 준비, 예금은 만기까지 보유 여부를 규칙 확인 후 결정
If 퇴직 직후 목돈 필요:
→ 현금화 손실 vs 일시금 수령 세부담을 화면([02-12-221] 시뮬레이션)으로 비교하는 결정 지원
If 재취업 예정:
→ 적립용 IRP 분리 구성 안내 (HT-001 3단 구성은 T3 — 확정 아님)
```

#### 12. Forbidden Shortcut
```text
«퇴직하면 무조건 IRP 로» 확정 (HD-7 은행 목적) · 퇴직 시 예금이 자동으로 현금화된다고 단정 (공식 확인 필요) · 퇴직소득세 환급액 계산값 제시 (HD-1) · 재취업 여부 확인 없이 계좌 3단 구성 확정
```

#### 13. Expected Brief Fit
- **S1 고객 상황**: 퇴직 예정 D-45, DC 정기예금 만기가 퇴직 후, 당행 IRP 미보유, 수령 콘텐츠 조회.
- **S2 확인할 점** — Main: 퇴직 전에 정할 것 3가지(수령 계좌·예금 처리·재취업). Why now: 퇴직일이 만기보다 먼저라 순서에 따라 손실이 갈린다(OK-011·014). Customer check: 퇴직일·사용 계획·재취업.
- **S3 관리 방향**: 퇴직용 IRP 개설 준비 + 예금 처리 방식은 규칙 확인 후 결정 + 60일 창구 사전 안내.
- **S4 상담 Point**: Opening «퇴직 준비 중이시라 들었어요 — 예금 만기가 퇴직 뒤라서 미리 봐드리려고요». 반론 «그냥 통장으로 받을게요» → TALK-006 사용 계획 확인 선행.
- **S5 TIP & 실행**: HT-021 · [04-12-642] 예상조회 · [00-12-210] 신규 · [06-12-501] 과세이연정보 등록 · 후속: 퇴직일 D-7 재통화.

#### 14. Potential Chat Questions
```text
퇴직하면 DC 에 있던 정기예금은 어떻게 돼?
퇴직 전에 IRP 를 미리 만들어 둘 수 있어?
퇴직금 받고 60일 지나면 뭐가 달라져?
```

#### 15. Demo Wow
박정호(퇴직 후)의 «전 단계» 를 보여준다 — Agent 가 퇴직일과 만기일의 **순서**를 읽고 손실을 피하는 처리 순서를 미리 짜 준다.

#### 16. Grounding Status
```text
MEDIUM
- 과세이연 절차·계좌 유형은 OK-014·019 (T2) 로 충분. 퇴직 시 DC 예금 현금화 규칙과 특별중도해지 해당 여부는 원천 미서술 — 공식 확인 필요.
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **34** |

---

### DC-002 — 퇴직급여 입금 5일차 · DO 등록 계좌 · 2주 자동적용 임박 · «다음 달 잔금» 발화

#### 1. Case Concept
퇴직급여가 IRP 에 막 입금됐고 디폴트옵션이 **등록돼 있어** 2주 뒤 자동 운용될 계좌인데, 고객이 «다음 달 아파트 잔금에 쓴다» 고 말한 것을 Agent 가 결합해, 지금 해야 할 일은 운용 권유가 아니라 **자동적용 전에 자금 성격을 확정하고 현금 상태를 유지**하는 것임을 발견하는 Negative Case.

#### 2. Why This Case Exists
```text
Reference:   06_주제별_추출지식 02_IRP관리방법론 (현금성자산의 4가지 해석) · 00_Core_Concept_Design §1 «퇴직금 최근 입금 → 일시적 대기자금»
Knowledge:   OK-005(최초 입금 후 2주 무지시 → DO 자동 운용) · OK-028(사용계획 있는 현금성자산은 권유 제외) · OK-015(중도인출 법정 사유 — 주택구입은 무주택자 한정) · OK-013(55세 개시 요건)
Source:      SRC-089 · SRC-002 L50 · SRC-003
Golden/Case: GC-03 은 DO «미등록» 53세 (2주 후에도 자동 운용 안 됨). 본 후보는 DO «등록» 계좌라 시계가 반대로 작동 — 사용계획 확인이 늦으면 자동으로 투자상품에 들어간다. [Gap-4] «접촉 과잉/현 상태 유지» 계열이면서 시한이 있는 변형.
```

#### 3. Trigger
퇴직급여 입금 D+5 (입금사유 «과세이연/계약이전입금») + 사전지정 DO 등록 + 운용지시 없음 → DO 자동적용 예정일 D-9([04-12-640] 사전지정운용제도 상세조회).

#### 4. Customer Context
```text
퇴직 직후 · 50대 · 위험중립형 · DO 뿔려드림(중위험) 등록 · 현금성 100% · CRM 최근 발화 «다음 달 잔금»
```

#### 5. Interesting Evidence Combination
```text
퇴직급여 입금 D+5
+ DO 등록(중위험) → 2주 자동적용 D-9
+ 고객 발화 «다음 달 아파트 잔금에 쓴다»
+ 만 55세 미만(개시 불가) · 무주택 여부 미확인(중도인출 사유 판정 불가)
```

#### 6. Potential Segment
`퇴직 직후` × `현금성 100%` × `DO 등록` × `단기 사용계획 있음` × `개시 요건 미충족`

#### 7. Potential Badges
```text
Primary:   DO 자동적용 D-9
Secondary: 퇴직급여 입금 D+5 · 사용계획 확인 필요
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-005 (2주 규칙·옵트인·[06-12-918]) · OK-028 (사용계획 있는 자금 권유 제외) · OK-015 (주택구입 사유 요건·최대 90%·세전 신청) · OK-013 (개시 요건) · OK-009 (인출 시 과세 구조)
Product:            (없음 — 유지가 방향)
Hot Tip:            HT-011 (중도인출 세전 신청·창구 접수) · HT-006 (은퇴 예정 시기 질문으로 시작 — PROVISIONAL)
Talk:               TALK-006 · TALK-007 (자금 계획 확인이 먼저)
Screen:             SCR-002 [04-12-640] 사전지정 상세조회 · SCR-016 [06-12-918] · SCR-038 [02-12-220] 지급
Knowledge Gap / Conflict: 2주 기산 방식(영업일/역일) 원문 없음(OK-005 Limitation)
```

#### 9. Expected Agent Discovery
«DO 등록 = 안전» 이 아니라, 이 고객에게는 **DO 자동적용이 곧 단기 사용자금을 투자상품에 넣는 사건**이 된다는 것. 잔금 자금이 IRP 안에 있으면 인출 경로(중도인출 사유 해당 여부·해지·과세) 자체가 문제라는 점까지 이어 읽는다.

#### 10. Required Confirmation
```text
Employee Check: DO 자동적용 예정일 · 무주택 여부(시스템 미확인) · 입금 금액 중 잔금 소요액
Customer Check: 잔금 일자·금액 · 퇴직급여 중 IRP 에 남길 금액 · 재취업 여부
```

#### 11. Potential Management Direction
```text
If 잔금에 실제로 쓴다:
→ 자동적용 전 인출 경로 정리(중도인출 사유 해당 여부 → 해당 없으면 해지·과세 구조 안내) — 운용 권유 없음
If 잔금은 다른 자금으로 충당:
→ 자금 성격 확정 후 운용 논의 (DO 자동적용 수용 / 옵트인 / 입금예정상품)
```

#### 12. Forbidden Shortcut
```text
현금 100% → «미운용 방치» 라벨 후 운용 권유 · DO 등록 계좌라 «알아서 운용되니 괜찮다» 로 종결 · 주택구입 중도인출 가능을 무주택 확인 없이 단정 · 인출 세액 계산값 제시
```

#### 13. Expected Brief Fit
- **S1**: 퇴직급여 입금 5일, DO 자동적용 D-9, «잔금» 발화.
- **S2** — Main: 자동적용 전 자금 성격 확정. Why now: 2주 규칙(OK-005). Customer check: 잔금 일정·금액.
- **S3**: 유지(현금) 또는 인출 경로 정리 — 상품 후보 없음이 정상.
- **S4**: Opening «퇴직금이 들어오고 열흘쯤 지나면 등록하신 자동운용으로 넘어가는데, 잔금 말씀하셔서 먼저 확인드려요». 반론 «그냥 두면 안 되나요?» → 자동적용 후 매도·인출 절차가 생긴다는 사실 고지.
- **S5**: [04-12-640] 실행예정 확인 · [06-12-918] 대기자금 처리 · 후속: 잔금일 이후 재접점.

#### 14. Potential Chat Questions
```text
2주 지나면 진짜 자동으로 투자돼?
잔금 때문에 빼야 하는데 중도인출 되는 거야?
지금 인출하면 세금은 어떻게 돼?
```

#### 15. Demo Wow
«DO 등록 고객은 안전» 이라는 대시보드 상식을 뒤집는다 — Agent 가 시한과 발화를 붙여 **아무것도 사지 않는 것**이 정답임을 보여준다.

#### 16. Grounding Status
```text
STRONG
- OK-005·028·015·013 (T2/Public) 로 판단 전체가 서고 화면도 실존.
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 5 |
| 데이터 결합성 | 5 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 5 |
| Demo Wow | 5 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 5 |
| **총점** | **37** |

---

### DC-003 — 연말 D-70 · 상여 입금 · 세액공제 잔여 · 결정세액이 낮을 수 있는 고객

#### 1. Case Concept
급여계좌에 상여가 들어오고 세액공제 잔여 한도가 남은 고객을 Agent 가 «추가납입 적기» 로 잡되, 올해 휴직·소득 감소로 **결정세액이 공제액보다 적을 수 있다**는 조건을 함께 발견해, «다 돌려받는다» 대신 원천징수영수증 확인을 먼저 연결하는 Case.

#### 2. Why This Case Exists
```text
Reference:   06_주제별_추출지식 04_제도상품팩트 (세액공제 구간·결정세액) · [HTML-Theme] 홍성우(상여 입금 + 잔여 300만 + 49.5만)
Knowledge:   OK-008(900만·16.5/13.2·결정세액 조건·[06-12-151]·[04-10-099]) · OK-018(한도 초과분 익년 공제 신청) · HT-029(D-70 절세 점검 — 11~12월 적기, 배우자 IRP) · HT-024([04-10-099] 루틴)
Source:      SRC-003 L123~135 · SRC-087 L70 · SRC-064
Golden/Case: GC-24 는 «총급여 2,600만·다 돌려받냐» 발화형(PASS). 본 후보는 발화 없이 상여 입금 Signal + 휴직 이력에서 Agent 가 결정세액 조건을 스스로 세운다. HTML 홍성우는 결정세액 축이 없어 «49.5만 환급» 을 단정 — 그 오류를 복제하지 않는 재구성.
```

#### 3. Trigger
급여계좌 상여 입금(D+2) + 당해 세액공제 잔여 한도 존재 + 과세연도 종료 D-70.

#### 4. Customer Context
```text
재직기 · 40대 · 위험중립형 · 올해 상반기 육아휴직(급여 이력 공백) · IRP 자동이체 월 25만
```

#### 5. Interesting Evidence Combination
```text
상여 입금 D+2
+ 세액공제 잔여 300만 · 납입한도 잔여 1,300만 (3필드 분리, HD-8)
+ 올해 급여 입금 공백 4개월(휴직 추정 — 사실 아님, Inference)
+ 과세연도 종료 D-70
+ 배우자 IRP 미보유(마이데이터, 참고)
```

#### 6. Potential Segment
`재직기` × `추가납입 여력` × `절세` × `결정세액 확인 필요` × `납입 시점 창구`

#### 7. Potential Badges
```text
Primary:   세액공제 여력 300만
Secondary: 과세연도 종료 D-70
Signal:    상여 입금 D+2 (직원 확인용 — 고객에게 «입금 확인했다» 표현 금지)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-008 · OK-018 · OK-009 (납입 후 중도인출 시 16.5% — 장기 구속 고지)
Product:            (납입금 운용처는 후속 — PRD-033 월간 포트폴리오 참고 수준)
Hot Tip:            HT-029 (11월 유도·배우자 IRP) · HT-024 · HT-022 (심사숙고 고객 안내장 + [75-08-850])
Talk:               TALK-031 (추가납 스크립트 — «골든타임» 류 단정 표현은 조건부로 변환)
Screen:             SCR-005 [06-12-151] · SCR-015 [04-10-099] · SCR-059 [04-12-653] 원천징수영수증 발급 · SCR-091 [75-08-850]
Knowledge Gap / Conflict: KG-005 결정세액 조건의 행내 근거 부재(Public 단독) · SC-003 원천징수영수증 항목번호
```

#### 9. Expected Agent Discovery
잔여 한도가 있어도 실효 공제는 결정세액에 달려 있고, 이 고객은 소득 공백 때문에 그 조건이 실제로 걸릴 수 있다는 것. «얼마 넣으면 얼마 환급» 을 말하지 않고 확인 경로를 먼저 세운다.

#### 10. Required Confirmation
```text
Employee Check: 세액공제 잔여·납입 잔여 3필드 · 원천징수영수증 결정세액(항목번호는 SC-003 미해소)
Customer Check: 올해 소득 규모(휴직 여부) · 연말까지 납입 가능 금액 · 배우자 소득 유무(HT-029 대안)
```

#### 11. Potential Management Direction
```text
If 결정세액 충분:
→ 11월 내 납입 안내(회사 마감 고려) + 납입금 운용처는 성향 범위 내 유형
If 결정세액 부족 가능:
→ 납입 규모 조정 또는 배우자 명의 검토 — 확정 계산은 화면·영수증
```

#### 12. Forbidden Shortcut
```text
«잔여 300만 → 300만 납입 → 49.5만 환급» 확정 (HD-1·F-002) · 상여 입금을 고객에게 언급 · 납입 가능 금액과 공제 가능 금액 혼동(3필드)
```

#### 13. Expected Brief Fit
- **S1**: 잔여 한도·자동이체·소득 공백 관찰·D-70.
- **S2** — Main: 실효 공제 확인 후 납입 규모. Why now: 납입 시점 기준 연말 창구(HT-029). Customer check: 소득·납입 여력.
- **S3**: 조건부 추가납입 + 배우자 대안(정보).
- **S4**: Opening «연말정산 준비 시즌이라 한도 점검해 드리려고요»(HT-048 취지 — 입금 언급 금지). 반론 «다 돌려받는 거죠?» → GC-24 검증 화법.
- **S5**: [06-12-151] · [04-10-099] · [04-12-653] · HT-029 · 후속: 11월 말 리마인드.

#### 14. Potential Chat Questions
```text
올해 휴직했는데 넣어도 환급돼?
한도 넘겨 넣으면 어떻게 돼?
배우자 이름으로 넣는 게 나아?
```

#### 15. Demo Wow
HTML 홍성우의 «49.5만 환급» 을 Agent 가 «조건부» 로 바꾼다 — 절세 숫자를 말하지 않는 것이 더 똑똑해 보이는 장면.

#### 16. Grounding Status
```text
STRONG (조건은 Public 단독 — KG-005 명시 필요)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 5 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 3 |
| Brief Fit | 5 |
| **총점** | **34** |

---

### DC-004 — 60세 이상 부부의 주택 다운사이징 매도대금 · 6개월 이내 1,800만 예외 납입

#### 1. Case Concept
60세 이상 고객의 입출금계좌에 주택 매도대금이 들어오고, 마이데이터·발화로 «더 작은 집으로 이사» 가 확인될 때, Agent 가 연간 1,800만 한도와 **별도로** 차액을 IRP 에 넣을 수 있는 예외(양도일부터 6개월, 생애 1억)를 발견해 정보 안내하는 Case.

#### 2. Why This Case Exists
```text
Reference:   06_주제별_추출지식 04_제도상품팩트 (납입한도 예외) · 01_고객세그먼트 «은퇴준비기 고령가구»
Knowledge:   OK-018(예외 ② 1주택 고령가구 다운사이징 차액 — 양도일 6개월 이내, ②+③ 생애 1억) · OK-008 · HT-002(다운사이징/양도차익 추가납입 실무 지식)
Source:      SRC-003 L139~145 · SRC-087 L77~79 · SRC-070
Golden/Case: 기존 24 Case 어디에도 «1,800만 예외 납입» 없음. OK-018 미사용 [Gap-11 인접].
```

#### 3. Trigger
입출금계좌 대규모 입금(부동산 매도대금 추정, Inference) + 고객 연령 60세 이상 + 최근 «이사» 발화 또는 주소 변경.

#### 4. Customer Context
```text
은퇴준비기/연금개시 가능 · 60대 초반 · 안정추구형 · IRP 정기예금 중심 · 부부 1주택(진술)
```

#### 5. Interesting Evidence Combination
```text
매도대금 입금 D+10
+ 주소 변경 / «작은 집으로 옮겼다» 발화
+ 60세 이상 (예외 요건)
+ 당해 납입한도 잔여 소진 상태 (일반 한도로는 못 넣는 상황)
+ 양도일 기준 6개월 시한
```

#### 6. Potential Segment
`은퇴준비기` × `외부 자금 유입` × `한도 외 납입 가능` × `절세` × `요건 판정 필요`

#### 7. Potential Badges
```text
Primary:   1,800만 예외 납입 가능성 (요건 확인)
Secondary: 양도일 +6개월 시한
Signal:    매도대금 입금
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-018 (요건·시한·생애 1억) · OK-008 (세액공제와의 관계) · OK-013 (개시 요건 — 개시 후 추가입금 불가 [02-12-223], HT-048)
Product:            (납입 후 운용은 후속)
Hot Tip:            HT-002 (다운사이징·양도차익 추가납입 실무) · HT-048 ([02-12-223] 연금개시 여부 확인)
Talk:               TALK-031 (추가납 스크립트 취지)
Screen:             SCR-005 [06-12-151] · SCR-008 [04-12-644] · SCR-080 [02-12-223]
Knowledge Gap / Conflict: 예외 ②③ 세부 요건(주택가격 판정·증빙)의 법령 원문 부재 — 개별 판정은 공식 확인(OK-018 Limitation)
```

#### 9. Expected Agent Discovery
«한도가 다 찼다» 로 끝나는 고객에게 별도 납입 창구가 있다는 것, 그리고 그 창구에 **6개월 시한**과 **연금개시 전** 이라는 조건이 붙어 있다는 것.

#### 10. Required Confirmation
```text
Employee Check: 연금개시 여부([02-12-223]) · 당해 납입 이력 · 요건 판정 절차(공식)
Customer Check: 양도일 · 종전/신규 주택 가격 관계 · 부부 1주택 여부 · 매도대금 사용 계획
```

#### 11. Potential Management Direction
```text
If 요건 충족 가능성 + 개시 전:
→ 예외 납입 안내(정보) + 증빙·판정은 공식 절차, 시한 기록
If 개시 후 계좌:
→ 추가입금 불가 — 신규 IRP 개설 요건 안내(OK-019)
```

#### 12. Forbidden Shortcut
```text
«6개월 안에 1억까지 넣으세요» 확정 (요건 판정 없이) · 매도대금 전액 납입 권유 (사용계획 미확인) · 세액공제 효과 계산값
```

#### 13. Expected Brief Fit
- **S1**: 매도대금 입금·이사 발화·60대·한도 소진.
- **S2** — Main: 예외 납입 요건·시한 확인. Why now: 양도일 6개월. Customer check: 주택·양도일·사용 계획.
- **S3**: 정보 안내 + 요건 충족 시 납입 경로.
- **S4**: Opening «이사하셨다고 들었는데, 집 줄이신 경우에 쓸 수 있는 IRP 납입 제도가 있어서요». 반론 «한도 넘는다던데» → 별도 한도 설명.
- **S5**: OK-018 원문 · [06-12-151] · [02-12-223] · 후속: 증빙 준비 후 내점.

#### 14. Potential Chat Questions
```text
1,800만 한도 넘겨서 넣는 게 정말 가능해?
6개월은 언제부터 세?
이걸로 세액공제도 받아?
```

#### 15. Demo Wow
직원도 잘 모르는 제도를 Agent 가 «자금 유입 + 나이 + 이사» 로 캐낸다.

#### 16. Grounding Status
```text
STRONG (제도 T2+Public 교차) — 요건 판정은 공식 확인 필요
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 5 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 3 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 5 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **34** |

---

### DC-005 — ISA 만기 · 금융소득종합과세 대상 고객 · ISA 재가입 불가

#### 1. Case Concept
ISA 만기 D-n 고객 가운데 이자·배당이 연 2,000만원을 넘어 금융소득종합과세 대상이 된 고객을 Agent 가 골라, «만기 후 ISA 재가입이 막힌 자금을 어디에 둘지» 의 선택지 중 하나로 IRP 전환입금(과세이연·종합과세 제외)을 정보 안내하는 Case. 세율·상속 화법은 T3 이므로 확정 인용하지 않는다.

#### 2. Why This Case Exists
```text
Reference:   06_주제별_추출지식 04_제도상품팩트 (금융소득종합과세 절) · 03_영업화법 (ISA 유형별 화법)
Knowledge:   OK-021(IRP 내 이자·배당 종합과세 제외·2,000만 기준) · OK-001(60일·10%/300만) · HT-045(ISA 보유 고객 유형별 — 금소종과 재가입 불가 유형; T3, 확실성_주의)
Source:      SRC-003 L510~527 · SRC-083
Golden/Case: GC-13·18·22 의 ISA 는 «세액공제 추가한도» 축. 종합과세 축은 OK-021 미사용 [Gap 8.5]. Seed 김서연의 «부유층 변형».
```

#### 3. Trigger
타행/당행 ISA 만기 D-20 + 전년 금융소득 2,000만 초과(마이데이터·발화).

#### 4. Customer Context
```text
은퇴준비기 · 50대 · 적극투자형 · IRP 는 소액 · 금융자산 큼(마이데이터)
```

#### 5. Interesting Evidence Combination
```text
ISA 만기 D-20
+ 금융소득 2,000만 초과(종합과세 대상)
+ 당해 IRP 납입 0 (세액공제 여력 900만 전액)
+ ISA 만기자금 규모가 세액공제 추가한도 상한(3,000만 전환 시 300만)을 넘음
+ 고객 «ISA 다시 못 든다던데» 발화
```

#### 6. Potential Segment
`은퇴준비기` × `외부 만기자금` × `종합과세 대상` × `절세` × `IRP 저활용`

#### 7. Potential Badges
```text
Primary:   ISA 만기 D-20
Secondary: 종합과세 대상 · 세액공제 여력 900만
Signal:    «재가입 불가» 발화
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-021 (종합과세 제외·1,500만 수령 단계) · OK-001 · OK-018 (1,800만 별도)
Product:            (전환 후 운용은 후속 — 성향 범위 내)
Hot Tip:            HT-045 (유형별 화법 — «최소 3.3%»·상속 저율 등 T3 단독 서술 → 확정 인용 금지) · HT-004 · HT-042
Talk:               TALK-031 (ISA 스크립트)
Screen:             SCR-015 [04-10-099] · SCR-014 [01-12-213]
Knowledge Gap / Conflict: 9.9% vs 3.3~5.5% 세율 비교는 HT-045 T3 단독 — 김서연 Audit P0-3 과 동일 이슈. 종합과세 세율 49.5%·분리과세 15.4% 는 OK-021 (T2)
```

#### 9. Expected Agent Discovery
같은 «ISA 만기» 라도 이 고객의 관심축은 세액공제가 아니라 **종합과세 회피**라는 것. 그래서 안내의 무게가 «추가 공제 300만» 이 아니라 «IRP 안의 이자·배당은 종합과세에서 빠진다» 로 옮겨간다.

#### 10. Required Confirmation
```text
Employee Check: ISA 만기일·만기금액([04-10-099] 저축종류 83) · 당해 납입 이력
Customer Check: 만기자금 사용계획 · 종합과세 대상 여부(본인 확인) · 전환 규모 · 55세 이후 수령 계획
```

#### 11. Potential Management Direction
```text
If 장기 노후자금:
→ 60일 내 전부/일부 전환 정보 + 세액공제 추가한도는 부수 안내
If 단기 사용:
→ 전환 규모 축소, 나머지는 IRP 밖에서 — 권유 없음
```

#### 12. Forbidden Shortcut
```text
«IRP 로 옮기면 세금이 3.3% 로 끝난다» 확정 (T3) · 상속 절세 화법 단정 · 전환 세액 계산값 · 전액 전환 권유
```

#### 13. Expected Brief Fit
- **S1**: ISA 만기 D-20·종합과세 대상·IRP 미납입.
- **S2** — Main: 만기자금의 세 갈래(재가입 불가·IRP·일반). Why now: 60일. Customer check: 사용계획·규모.
- **S3**: IRP 전환 정보 + 운용 유형(성향 범위).
- **S4**: Opening «ISA 만기 앞두고 계시고, 종합과세 쪽 고민 있으실 것 같아서요». 사전고지: 세율 비교는 공식 기준 확인 후.
- **S5**: OK-021·001 · [04-10-099] · [01-12-213] · HT-045(주의 표시).

#### 14. Potential Chat Questions
```text
IRP 안에서 난 이자도 종합과세에 잡혀?
ISA 만기금 다 넣어도 돼? 한도는?
연금으로 받을 때 1,500만 넘으면 어떻게 돼?
```

#### 15. Demo Wow
«같은 ISA 만기, 다른 이유» — Agent 가 고객의 소득 구조를 읽고 안내의 축을 바꾼다.

#### 16. Grounding Status
```text
MEDIUM
- 종합과세 제외·2,000만·1,500만은 OK-021 (T2). 화법의 세율 비교는 T3 단독 — 보강 필요.
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 3 |
| Agent 판단성 | 3 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 3 |
| Brief Fit | 4 |
| **총점** | **29** |

---

### DC-006 — 타사 연금저축보험 보유 · 만 55세 + 가입 5년 «충족 도래» · 수익 불만

#### 1. Case Concept
GC-15(요건 미충족 → 실행 불가)의 Pair. 이전 요건(만 55세 + 5년)이 **이번 달 충족되는** 고객에게 «이제 이전이 가능해졌다» 는 사실과 «보험사 이전 가능 여부·해지환급금 확인이 먼저» 라는 확인 선행 구조를 함께 제시하는 조건부 Case.

#### 2. Why This Case Exists
```text
Reference:   03_영업화법 (연금저축보험 이전 제안) · 01_고객세그먼트 «타사 연금저축 보유»
Knowledge:   OK-020(연저→IRP 55세+5년) · TALK-024(공시이율 비교·«보험사에 이전 가능 여부 문의» 확인 선행 구조) · HT-007([04-10-099] 55세+5년 확인 후 권유) · HT-010(MY연금자산조회) · HT-041(요건 정리·0원 계좌 규칙)
Source:      SRC-003 L453 · SRC-009 · SRC-039 · SRC-042 · SRC-079
Golden/Case: GC-15 = 52세·3년 → 실행 불가(PASS). 본 후보는 요건 충족 «직후» — Pair 로 판단 차이를 보여줌. TALK-024·HT-007 미사용.
```

#### 3. Trigger
[04-10-099] 저축종류 36(연금저축) 보유 + 생일 도래로 만 55세 + 가입 5년 경과 (이번 달) + CRM «보험 수익이 안 나서» 발화.

#### 4. Customer Context
```text
은퇴준비기 · 55세 · 안정추구형 · 당행 IRP 원리금 중심 · 타사 연금저축보험(공시이율 2%대, 해지환급금 미확인)
```

#### 5. Interesting Evidence Combination
```text
만 55세 도달(이번 달)
+ 연금저축보험 가입 5년 경과
+ «수익이 안 난다» 발화 (6개월 전 CRM)
+ 당행 IRP 세액공제 잔여 (연저 600+IRP 300 구조 → 이전 시 한도 통합)
+ 보험사 이전 가능 여부 미확인
```

#### 6. Potential Segment
`은퇴준비기` × `외부 연금계좌` × `이전 요건 충족 직후` × `확인 선행` × `수익률 불만`

#### 7. Potential Badges
```text
Primary:   연금저축 이전 요건 충족
Secondary: 만 55세 도달 · 세액공제 구조 변경 가능
Signal:    «수익 불만» 발화(6개월 전)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-020 (요건·0원 계좌·가입일 승계) · OK-008 (연저 600 / 합산 900) · OK-016 (이전 후 수수료)
Product:            (이전 후 운용은 후속)
Hot Tip:            HT-007 · HT-010 · HT-041 · HT-008 (섭외 전 연금납입현황 확인 — 국민지갑 전자증명서 [06-7E-001] · [06-10-182])
Talk:               TALK-024 (확인 선행 구조 · «훨씬 이득» 단정 금지)
Screen:             SCR-015 [04-10-099] · SCR-081 [06-10-182] · SCR-083 [06-7E-001] · SCR-003 [06-AD-080]
Knowledge Gap / Conflict: 연저 이전 요건이 «연금개시 여부» 와 어떻게 관계되는지 원문 요약 서술(OK-020 Limitation) · 6개월 전 CRM 의 현재 유효성(GC-20 취지)
```

#### 9. Expected Agent Discovery
«이전 불가» 였던 고객이 **달력 때문에** 가능 고객으로 바뀌었다는 것 — 그리고 가능해졌다고 곧바로 이전이 유리한 것은 아니며, 해지환급금·보험사 가능 여부·수령 개시 여부를 먼저 봐야 한다는 것.

#### 10. Required Confirmation
```text
Employee Check: [04-10-099] 연저 가입일·개시 여부 · 당행 IRP 0원 계좌 필요 여부(OK-020)
Customer Check: 지금도 이전 의향인지(6개월 전 발화 재확인) · 보험사 해지환급금·이전 가능 여부 문의 결과 · 수령 계획
```

#### 11. Potential Management Direction
```text
If 이전 의향 유지 + 보험사 확인 완료:
→ 이전 절차(0원 계좌·가입일 승계) 안내 — 조건부
If 해지환급금 손실 큼:
→ 유지 + 납입 배분 조정 (GC-15 대안 (c) 계열)
```

#### 12. Forbidden Shortcut
```text
«이제 되니까 옮기세요» (은행 목적·손실 미고지) · 공시이율 비교 단정 · 6개월 전 발화를 현재 의사로 승격 · 해지 후 재입금 권유
```

#### 13. Expected Brief Fit
- **S1**: 55세 도달·5년 경과·과거 발화·당행 IRP 구조.
- **S2** — Main: 이전 가능해진 사실 + 확인 3가지. Why now: 요건 충족 시점. Customer check: 의향·환급금·보험사.
- **S3**: 조건부 이전 / 유지 + 배분 조정.
- **S4**: Opening «작년에 보험 수익 말씀하셨죠 — 이번 달부터 IRP 로 옮기는 게 제도상 가능해져서요. 다만 먼저 확인할 게 있어요». 반론 «해지하면 손해 아니에요?» → 해지환급금 확인 선행.
- **S5**: [04-10-099] · HT-008 전자증명서 · TALK-024 · 후속: 보험사 확인 후 재통화.

#### 14. Potential Chat Questions
```text
연금저축보험 옮기면 가입일은 어떻게 돼?
옮기면 세액공제 한도가 달라져?
보험사가 이전 안 해주면 어떻게 해?
```

#### 15. Demo Wow
GC-15 와 같은 화면에 놓으면 «날짜 하나로 판단이 바뀌는» Pair 가 된다.

#### 16. Grounding Status
```text
STRONG (OK-020 T2 + 화법 T3 확인 선행 구조)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **32** |

---

### DC-007 — 연금개시된 타사 연금저축을 IRP 로 «0원 계좌» 이전 요청

#### 1. Case Concept
이미 연금을 받고 있는 타사 연금저축(복수 건)을 당행 IRP 로 합치고 싶어 하는 고객에게, Agent 가 «수령 중 계좌는 0원 계좌로만 이전 가능 · 건별 반복 · 이전분 추가입금 불가» 라는 실행 순서와 부담을 먼저 정리해 주는 절차 Case.

#### 2. Why This Case Exists
```text
Reference:   05_업무처리절차 (계약이전 절차)
Knowledge:   OK-020(수령 중 계좌 → 0원 계좌 · 가입일 승계) · OK-019(1인 1계좌·추가 개설) · HT-027(연금개시된 연금저축보험 3건 이전 실무 — 건별 반복·추가입금 불가·서류 순차)
Source:      SRC-003 L427~429 · SRC-062
Golden/Case: 없음 [Gap-11]. OK-020·HT-027 미사용.
```

#### 3. Trigger
고객 발화/내점 «연금 받고 있는 보험 3개를 한 군데로» + [04-10-099] 연금저축 복수 보유.

#### 4. Customer Context
```text
연금수령기 · 60대 · 안정형 · 당행 적립겸용 IRP 보유(미개시) · 타사 연금저축보험 3건 수령 중
```

#### 5. Interesting Evidence Combination
```text
«한 군데로 합치고 싶다» 발화
+ 연금저축 3건 수령 중(개시 상태)
+ 당행 IRP 는 미개시(→ 0원 계좌 별도 필요)
+ 안정형(운용은 지켜드림·6등급만 — C2/C3)
```

#### 6. Potential Segment
`연금수령기` × `외부 연금계좌 복수` × `이전(수령 중)` × `절차 부담` × `안정형`

#### 7. Potential Badges
```text
Primary:   연금개시 계좌 이전 요청
Secondary: 0원 계좌 필요 · 건별 절차
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-020 · OK-019 · OK-013 (수령 방식) · OK-016 (연금수령 고객 수수료 면제 — 1년 내 이전 시 미적용 조건)
Product:            (안정형 — 지켜드림·정기예금 유형만, PRD-021 C3)
Hot Tip:            HT-027 (실무 반복 절차·수시인출 10만원) · HT-041 (0원 계좌 규칙)
Talk:               (해당 화법 없음 — 절차 안내형)
Screen:             SCR-015 [04-10-099] · SCR-031 [00-12-210] 신규 · SCR-003 [06-AD-080] · SCR-012 스타뱅킹 연금 수령관리
Knowledge Gap / Conflict: 0원 계좌·가입일 승계의 내규 원문 부재(OK-020 Limitation) · 반복 절차는 T3 실무
```

#### 9. Expected Agent Discovery
«합치기» 가 한 번의 이전이 아니라 **건별 3회 반복 + 계좌 3개 신설**이라는 것, 그리고 이전받은 계좌에는 추가입금이 안 된다는 것 — 고객이 기대한 «관리 편의» 와 실제 절차 사이의 간극을 미리 보여준다.

#### 10. Required Confirmation
```text
Employee Check: 각 연저의 개시 상태·가입일 · 보험사별 이전 가능 여부
Customer Check: 합치려는 이유(관리 편의/수익) · 수령 방식 유지 희망 · 절차 부담 수용 여부
```

#### 11. Potential Management Direction
```text
If 절차 부담 수용:
→ 건별 «0원 계좌 개설 → 이전 → 개시» 순서 안내 + 서류 순차 징구
If 부담 큼:
→ 현 상태 유지 + 수령 관리만 통합 조회(정보)
```

#### 12. Forbidden Shortcut
```text
기존 IRP 로 그대로 이전 가능 안내 · 이전 후 추가입금 가능 안내 · 안정형 고객에게 실적배당 제안 · 수수료 면제 무조건 적용
```

#### 13. Expected Brief Fit
- **S1**: 연저 3건 수령 중·당행 IRP 미개시·요청.
- **S2** — Main: 이전 구조(0원 계좌·건별)와 부담 확인. Why now: 고객 요청. Customer check: 이유·수용 여부.
- **S3**: 절차 안내(순번) / 유지.
- **S4**: Opening «합치는 건 가능한데, 방식이 좀 특이해서 미리 설명드릴게요». 반론 «왜 계좌를 또 만들어요?» → 0원 계좌 규칙.
- **S5**: HT-027 · [00-12-210] · [06-AD-080] · [04-10-099].

#### 14. Potential Chat Questions
```text
받고 있는 연금저축도 옮길 수 있어?
옮기면 지금 받는 연금은 끊겨?
옮긴 계좌에 돈 더 넣을 수 있어?
```

#### 15. Demo Wow
«가능하지만 이렇게 복잡하다» 를 순번으로 보여주는 절차형 Case — 박정호 S5 순번 UI 의 강점을 살린다.

#### 16. Grounding Status
```text
MEDIUM (구조 T2, 실무 반복은 T3)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 3 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 3 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **30** |

---

### DC-008 — 만기 후 4주 통지 발송 · DO 등록 · 자동적용 D-14 · «다른 상품으로 하고 싶다» 발화

#### 1. Case Concept
정기예금 만기 후 4주간 운용지시가 없어 가입자 통지가 나갔고, 2주 뒤 등록된 DO 로 자동 매수될 계좌의 고객이 «그 상품 말고 다른 걸로» 라고 말했을 때, Agent 가 «옵트인으로 즉시 다른 상품 지시 vs 자동적용 대기 vs 변경 등록 후 옵트인» 의 시계와 제약(이미 DO 운용 중이면 같은 상품만)을 정리하는 Case.

#### 2. Why This Case Exists
```text
Reference:   02_IRP관리방법론 (만기 후 처리) · 04_제도상품팩트 (디폴트옵션 적용시점)
Knowledge:   OK-005(4+2주·통지·옵트인 — DO 미운용 중이면 원하는 상품, 운용 중이면 같은 상품만 · [04-12-640] 상세조회 · [06-12-918]) · OK-026(변경 시 기존 적립금 매도 불요) · TALK-008(DO 거부감 3단계) · TALK-010(일부만 변경 완충)
Source:      SRC-089 · SRC-098 L52~69·L236~305 · SRC-007
Golden/Case: GC-01 은 만기 «전»(D-18) · GC-09 는 DO 자동적용 «후». 만기 후 4주~6주 사이의 «통지 발송 후 창구» 는 없음. Seed 이수민(만기 전 D-22)의 «후 단계». [Gap-4 시한형]
```

#### 3. Trigger
만기 후 28일 경과 · 운용지시 없음 · 가입자 통지 발송 기록 · DO 자동적용 예정 D-14 + 고객 콜센터 발화.

#### 4. Customer Context
```text
재직기 · 40대 · 위험중립형 · DO 알파드림(저위험) 등록 · 만기 자금 현금성 · 다른 DO(뿔려드림)를 앱에서 조회
```

#### 5. Interesting Evidence Combination
```text
만기 후 4주 경과 + 통지 발송 완료
+ 자동적용 D-14
+ 발화 «등록한 거 말고 다른 걸로»
+ 앱 «뿔려드림» 조회 2회
+ 이 계좌에 이미 DO 상품 운용 중인지 여부(옵트인 제약 결정)
```

#### 6. Potential Segment
`재직기` × `만기 후 대기` × `DO 등록` × `자동적용 임박` × `상품변경 탐색`

#### 7. Potential Badges
```text
Primary:   DO 자동적용 D-14
Secondary: 만기 후 대기 4주 · 통지 발송됨
Signal:    DO 상품 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-005 · OK-026 (변경·지정 규칙, SC-004 구성 인용 금지) · OK-006 (성향 상한 — 뿔려드림은 위험중립 이상 C3)
Product:            PRD-021 (DO 4단계 명칭 — 구성·종수 확정 인용 금지)
Hot Tip:            HT-006 (DO 등록+교체매매 세트 — PROVISIONAL) · HT-035 (앱 운용지시 지원)
Talk:               TALK-008 · TALK-010 · TALK-028 §34 (만기+DO)
Screen:             SCR-002 [04-12-640] · SCR-016 [06-12-918] · SCR-010 스타뱅킹 보유상품변경 · SCR-047 [06-12-610] 입금예정상품
Knowledge Gap / Conflict: 6주 기산·IRP/DC 공통 여부 원문 부재 · SC-004 DO 종수 · «옵트인은 같은 상품만» 규칙은 Public+T2
```

#### 9. Expected Agent Discovery
«기다리면 알아서 된다» 와 «지금 바꾸면 된다» 사이에 **옵트인 제약**이 있다는 것 — 이미 DO 상품이 운용 중이면 다른 DO 로 옵트인할 수 없고, 등록 변경 → 매수의 2단계가 필요하다는 것을 D-14 안에 정리해야 한다.

#### 10. Required Confirmation
```text
Employee Check: [04-12-640] 실행예정 내역 · 계좌 내 DO 상품 기운용 여부 · 성향-상품 C3
Customer Check: 원하는 상품이 무엇인지(유형) · 자금 사용계획 · 직접 지시 가능 여부(앱)
```

#### 11. Potential Management Direction
```text
If DO 미운용 + 성향 범위 내:
→ 옵트인으로 원하는 상품 즉시 지시 (앱/창구)
If DO 기운용:
→ 등록 변경 → 보유상품 변경 2단계 안내, D-14 내 처리
If 결정 못 함:
→ 자동적용 수용 후 변경 가능(매도 불요) 정보
```

#### 12. Forbidden Shortcut
```text
«등록 바꾸면 만기자금도 바뀐다» · 뿔려드림 구성 확정 서술(SC-004) · 성향 확인 없이 중위험 권유 · «방치» 라벨
```

#### 13. Expected Brief Fit
- **S1**: 만기 후 4주·통지·D-14·발화·조회.
- **S2** — Main: 자동적용 전 선택. Why now: 6주 규칙. Customer check: 원하는 유형·사용계획.
- **S3**: 옵트인 / 2단계 변경 / 수용 후 변경 — 조건부.
- **S4**: Opening «지난주 안내문 받으셨죠 — 2주 뒤 자동으로 들어가기 전에 원하시는 걸로 맞춰드리려고요». 반론 «귀찮은데 그냥 두면요?» → TALK-008.
- **S5**: [04-12-640] · [06-12-918] · 스타뱅킹 보유상품변경 · 후속: D-7 확인.

#### 14. Potential Chat Questions
```text
2주 안에 안 하면 어떻게 돼?
등록만 바꾸면 만기된 돈도 그쪽으로 가?
지금 있는 DO 상품 말고 다른 DO 로 바로 살 수 있어?
```

#### 15. Demo Wow
Badge 가 시간에 따라 «만기 D-n → 대기 n주 → 자동적용 D-n» 으로 바뀌는 것을 한 고객에서 보여준다(§10 시간축).

#### 16. Grounding Status
```text
STRONG (OK-005 Public+T2 교차)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 5 |
| **총점** | **35** |

---

### DC-009 — 위험자산 한도 초과 계좌 · «ETF 100% 되던데요» 추가 매수 요청

#### 1. Case Concept
평가 상승으로 위험자산 비중이 70% 를 넘은 계좌의 고객이 게시글에서 본 «ETF 100% 운용» 을 근거로 주식형 ETF 추가 매수를 요청할 때, Agent 가 «100% 는 DO·TDF·채권형/채권혼합 ETF 예외로 구성한 것이지 주식형 100% 가 아니다» 를 정정하고, 실행 가능한 경로(비위험 상품으로 추가입금·교체)를 제시하는 실행 제약 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (위험자산 한도) · 03_영업화법 (ETF 100% 운용지시 게시글)
Knowledge:   OK-012(70%·예외·[04-12-354]·페널티 없음 T3·산정 기준 표현 상이) · HT-043(ETF 100% 구성 — 주식형 70+채권형 30 · 체결 소요) · HT-039(100% 투자 가능 상품 정리) · OK-023(체결 구조)
Source:      SRC-087 L68 · SRC-098 L60 · SRC-077 · SRC-081
Golden/Case: GC-07 은 «팔기 싫다»(평가 상승형, 정보안내). 본 후보는 «더 사겠다» + 마케팅 게시글 오해 — [Gap-12]. HT-043 미사용.
```

#### 3. Trigger
[04-12-354] 위험자산투자한도위반 조회 대상 + 콜센터/앱 «ETF 추가 매수 안 되는데요» 문의.

#### 4. Customer Context
```text
재직기 · 30대 후반 · 적극투자형 · 나스닥·S&P ETF 중심 · DO 뿔려드림 · 앱 매수 시도 실패 로그
```

#### 5. Interesting Evidence Combination
```text
위험자산 비중 74%(한도 초과)
+ 앱 주식형 ETF 매수 실패
+ 발화 «ETF 100% 된다고 봤는데»
+ 납입한도 잔여 1,300만(추가입금 경로 존재)
+ 채권형 ETF 미보유
```

#### 6. Potential Segment
`재직기` × `실적배당 중심` × `위험자산 한도 초과` × `ETF 관심` × `앱 실행 실패`

#### 7. Potential Badges
```text
Primary:   위험자산 한도 초과
Secondary: 추가 매수 요청
Signal:    앱 매수 실패 · ETF 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-012 · OK-023 (금액주문·3분 분할) · OK-006 (적극투자형 3~6등급 — 1등급 ETF 신규 매수는 C2 위반) · OK-018 (납입한도)
Product:            (채권형·채권혼합 ETF 유형 — 개별 상품은 [04-12-17A] 조회)
Hot Tip:            HT-043 (bank_objective_포함 · 확실성_주의 — 구성 산술은 설명 재료만) · HT-039
Talk:               TALK-016 (ETF 허와 실) · TALK-022
Screen:             SCR-020 [04-12-354] · SCR-004 [04-12-17A] (투자가능한도 필터) · SCR-010 스타뱅킹 보유상품변경
Knowledge Gap / Conflict: 70% 산정 기준(평가금액 vs 적립금) 표현 상이 — 판정 계산 금지 · 예외 상품 정확 범위 T3 나열 · 페널티 없음 T3
```

#### 9. Expected Agent Discovery
고객의 «100%» 는 마케팅 게시글의 **구성 산술**(주식형 70 + 채권형 30)이지 규정이 아니라는 것. 지금 계좌는 이미 초과 상태라 주식형 추가 매수는 실행 불가이며, 가능한 것은 비위험 상품으로의 추가입금·교체라는 것.

#### 10. Required Confirmation
```text
Employee Check: [04-12-354] 초과금액·보유가능금액 · [04-12-17A] 상품별 투자가능한도 · 성향 등급(1등급 ETF 는 적극투자형 신규 매수 불가)
Customer Check: 원하는 상품 유형 · 추가입금 의향 · 채권형 ETF 로 대체 가능 여부
```

#### 11. Potential Management Direction
```text
If 추가입금 가능:
→ 추가입금 후 비위험(채권형·채권혼합 ETF/정기예금) 운용지시로 비중 하락 → 이후 주식형 여력
If 추가입금 불가:
→ 일부 교체매매(주식형 → 채권형) 후 재매수 — 고객 결정
```

#### 12. Forbidden Shortcut
```text
«주식형 ETF 100% 가능» 동조 · 강제 매도·페널티 공포 · 1등급 ETF 추가 매수 권유(C2) · 초과 금액 계산값 제시
```

#### 13. Expected Brief Fit
- **S1**: 한도 초과·매수 실패·발화·잔여 한도.
- **S2** — Main: 100% 오해 정정 + 실행 가능 경로. Why now: 매수 실패 직후. Customer check: 유형·추가입금.
- **S3**: 추가입금+비위험 / 일부 교체 — 조건부.
- **S4**: Opening «앱에서 안 사졌던 게 한도 때문인데, 100% 얘기는 채권형을 섞는 구성이라서요». 반론 «그럼 팔아야 해요?» → 페널티는 확인 필요, 대안 경로.
- **S5**: [04-12-354] · [04-12-17A] 필터 · HT-039 · 후속: 추가입금 후 재확인.

#### 14. Potential Chat Questions
```text
ETF 100% 로 굴리는 게 진짜 돼?
한도 넘으면 벌금 있어?
채권형 ETF 는 왜 예외야?
```

#### 15. Demo Wow
«게시글 마케팅» 을 Agent 가 규정으로 되돌려 놓는다 — 현장 노하우(T3)와 제도(T2)의 등급 차이를 화면에서 보여준다.

#### 16. Grounding Status
```text
STRONG (OK-012 Public+T2; R4 deterministic 은 비활성이므로 판정 계산은 화면 값으로만)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **33** |

---

### DC-010 — 안정형 고객의 TDF 요청 · 앱 매수 차단 · «성향 다시 하면 되죠?»

#### 1. Case Concept
투자성향이 안정형(6등급만 권유 가능)인 고객이 «친구가 TDF 좋다더라» 며 앱에서 TDF 매수를 시도했다가 차단되고, «성향 검사 다시 하면 되죠?» 라고 물을 때, Agent 가 성향=상한 원칙·재분석은 권유 수단이 아님(KG-006 원문 부재)·안정형이 쓸 수 있는 자동운용(지켜드림)의 범위를 정확히 안내하는 C2/C3 최협 Case.

#### 2. Why This Case Exists
```text
Reference:   01_고객세그먼트 «안정형» · 03_영업화법 (상품 5종 프레임)
Knowledge:   OK-006(성향=최대 허용 위험·부적합 절차는 범위 밖·재분석 원문 없음) · OK-024(5단계 정의) · OK-025(TDF 구조) · TALK-022(선택 두 축·위험=변동성) · TALK-019(50대라고 무조건 안정형 아님 — 조건부)
Source:      SRC-096 · SRC-088 · SRC-090 · SRC-024 · SRC-020
Golden/Case: 안정형 고객 0명 [Gap-1]. GC-17(위험중립 TDF 선택)·GC-09(성향 상향)의 반대 방향.
```

#### 3. Trigger
앱 TDF 매수 시도 차단 로그 + 콜센터 «성향 재분석» 문의.

#### 4. Customer Context
```text
재직기 · 50대 · 안정형(2025-11 분석) · 정기예금 100% · DO 지켜드림 · 친구 권유 발화
```

#### 5. Interesting Evidence Combination
```text
앱 TDF 상세 조회 3회 → 매수 화면 진입 → 차단
+ 성향 안정형(10개월 전)
+ «다시 검사하면 되죠?» 발화
+ 은퇴까지 10년 이상(연령) — 투자기간은 길지만 성향이 상한
+ 정기예금 100% · 지켜드림
```

#### 6. Potential Segment
`재직기` × `안정형` × `원리금 100%` × `TDF 관심` × `앱 실행 실패` × `재분석 문의`

#### 7. Potential Badges
```text
Primary:   성향 상한 초과 요청
Secondary: 안정형 · 재분석 문의
Signal:    TDF 조회 · 매수 차단
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-006 (T1 Human-confirmed) · OK-024 · OK-025 · OK-026 (지켜드림은 모든 성향)
Product:            PRD-021 지켜드림 · (TDF 는 C2 상 안정형 신규 매수 불가 — PRD-004 마이다스 «보통» 도 불가)
Hot Tip:            (해당 없음 — HT-019 «무조건 가입» 류는 확실성_주의)
Talk:               TALK-022 · TALK-019 · TALK-021 (투자 4단계 — 설명 재료)
Screen:             SCR-004 [04-12-17A] (성향별 조회) · SCR-011 스타뱅킹 운용상품 찾기
Knowledge Gap / Conflict: KG-006 성향 재분석·상향 안내 원문 부재 — «재분석하면 된다» 도 «안 된다» 도 확정 금지 · 부적합 확인 절차는 OK-006 범위 밖
```

#### 9. Expected Agent Discovery
차단은 오류가 아니라 **제도**이고, 재분석은 고객이 스스로 원할 때의 절차이지 직원이 유도할 수단이 아니라는 것. 안정형 안에서도 «자동운용(지켜드림)·만기 예약변경» 같은 관리 편의는 제공할 수 있다.

#### 10. Required Confirmation
```text
Employee Check: 성향 분석일·유효기간(원문 없음 — 시스템 확인) · 부적합 절차 공식 기준
Customer Check: TDF 를 원하는 실제 이유(수익/친구) · 손실 감내 의사(재분석은 본인 결정) · 투자 기간
```

#### 11. Potential Management Direction
```text
If 고객이 스스로 재분석 원함:
→ 재분석 절차 안내(정보) — 결과에 따라 상한 재적용, 권유는 그 후
If 원금 보전이 실제 우선:
→ 현 상태 유지 + 지켜드림·예약변경 편의 안내
```

#### 12. Forbidden Shortcut
```text
«성향 다시 하시면 TDF 됩니다» 유도 (HD-2 위반) · 안정형에게 TDF 추천 (C2) · «안정형이라 투자 못 한다» 단정(상한이지 요구 아님)
```

#### 13. Expected Brief Fit
- **S1**: 차단 로그·발화·안정형·예금 100%.
- **S2** — Main: 성향 상한의 의미와 재분석의 위치. Why now: 앱 차단 직후 문의. Customer check: 실제 이유·감내 의사.
- **S3**: 유지 + 편의 / 재분석은 고객 결정.
- **S4**: Opening «앱에서 안 됐던 건 고객님 성향 결과 때문이고, 그건 보호 장치예요». 사전고지: 재분석은 본인 판단.
- **S5**: OK-006 · [04-12-17A] · 스타뱅킹 상품찾기.

#### 14. Potential Chat Questions
```text
성향 검사 다시 하면 TDF 살 수 있어?
안정형이면 아무 투자도 못 해?
지켜드림은 뭘로 돌아가?
```

#### 15. Demo Wow
«팔지 않는 Agent» — 규제 경계를 고객 편에서 설명하는 장면. 기존 Portfolio 에 안정형이 0명이라 신선하다.

#### 16. Grounding Status
```text
STRONG (OK-006 T1) — 재분석 절차는 KG-006 으로 «모른다» 를 명시
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **33** |

---

### DC-011 — 공격투자형 · 예금 100% · «2년 안에 집 산다» → 현 상태 유지가 합리

#### 1. Case Concept
성향은 공격투자형이지만 IRP 가 예금 100% 인 고객을 TM 리스트가 «성향-운용 불일치» 로 올려놓았을 때, Agent 가 «2년 내 주택구입 자금» 이라는 발화를 결합해 **지금 안정 운용이 합리적**이며 관리 필요성이 낮다고 결론 내는 Negative Case.

#### 2. Why This Case Exists
```text
Reference:   02_IRP관리방법론 (성향-운용 불일치는 관리 필요의 근거 아님) · [HTML-Theme] 윤소라(공격투자형 × 초저위험 DO)
Knowledge:   OK-006(성향=상한) · OK-028(사용계획 있는 자금) · OK-015(주택구입 중도인출 요건) · HD-2 «성향-운용 불일치 → 자동 관리 필요 Rule 금지» · HD-7(TM Signal 은 Reasoning Input 아님)
Source:      SRC-096 · SRC-002 L50 · SRC-007 §33
Golden/Case: GC-04 는 «원금손실 우려» 명시 의사 기반 유지. 본 후보는 의사가 아니라 **자금 목적·기간** 기반 유지 — 지시서 §7 의 예시 그대로. HTML 윤소라의 «재지정 제안» 을 반대로 뒤집는다.
```

#### 3. Trigger
TM 리스트 «공격투자형인데 초저위험 등록»(TALK-028 §33 유형) 배분 + 최근 CRM «2년 내 주택 구입 예정».

#### 4. Customer Context
```text
재직기 · 30대 후반 · 공격투자형(최근 상향) · 정기예금 100% · DO 지켜드림 · 무주택
```

#### 5. Interesting Evidence Combination
```text
성향 공격투자형 상향(3개월 전)
+ 예금 100% + 지켜드림
+ CRM «2년 안에 집 살 계획, 이 돈도 쓸 수 있으면»
+ 무주택(진술 — 중도인출 사유 가능성)
+ TM 리스트 배분(Bank Signal — 판단 입력 아님)
```

#### 6. Potential Segment
`재직기` × `원리금 100%` × `성향-운용 불일치(관찰)` × `단기 사용계획` × `현 상태 유지`

#### 7. Potential Badges
```text
Primary:   (관리 필요 Badge 없음이 정답)
Secondary: 사용계획 있음(2년 내 주택)
Signal:    성향 상향
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-006 · OK-028 · OK-015 (무주택자 주택구입 사유·90%·세전) · OK-009 (인출 과세)
Product:            (없음)
Hot Tip:            (없음)
Talk:               TALK-028 §33 (TM 스크립트 — 사용 금지, 대비 재료로만)
Screen:             SCR-001 · SCR-002
Knowledge Gap / Conflict: 중도인출 사유 판정은 공식 절차
```

#### 9. Expected Agent Discovery
«성향 상향 = 운용 요구» 가 아니라는 것, 그리고 2년 뒤 쓸 돈에 변동성을 얹는 것이 고객 이익이 아니라는 것. 오히려 짚을 것은 «IRP 자금을 주택구입에 쓸 수 있는가(중도인출 사유·90%·과세)» 라는 실행 가능성.

#### 10. Required Confirmation
```text
Employee Check: 없음(개입 불필요) — 중도인출 요건은 고객이 물을 때
Customer Check: 주택 자금에 IRP 를 실제로 쓸 계획인지 (아니면 확인도 불필요)
```

#### 11. Potential Management Direction
```text
If 자금 목적 유지:
→ 현 상태 유지 합리 · 접점은 «중도인출 요건 정보» 정도
If 주택 계획 취소·연기:
→ 그때 성향 범위 내 운용 논의(재확인)
```

#### 12. Forbidden Shortcut
```text
«공격투자형이니 모두드림으로» (HD-2·C3 방향 위반은 아니나 목적 무시) · TM 리스트를 관리 근거로(F-009) · 성향 재분석 권유 · «불일치 해소» 프레임
```

#### 13. Expected Brief Fit
- **S1**: 성향·예금 100%·주택 계획.
- **S2** — Main: 지금 관리 필요 없음 + 인출 가능성 정보. Why now: (없음 — TM 배분은 이유 아님). Customer check: 계획 유지 여부.
- **S3**: 유지.
- **S4**: 접점 시 «지금 구성은 집 계획과 잘 맞아요» + 중도인출 요건 정보.
- **S5**: OK-015 요건 · [02-12-220].

#### 14. Potential Chat Questions
```text
성향이 공격형인데 예금만 두면 문제 있어?
집 살 때 IRP 돈 뺄 수 있어?
지금 뭘 바꿔야 하는 거야?
```

#### 15. Demo Wow
대시보드가 «불일치» 라고 빨갛게 표시한 고객을 Agent 가 «건드리지 마세요» 로 돌려세운다.

#### 16. Grounding Status
```text
STRONG (OK-006 T1 · OK-028 T2 · HD-2)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 3 |
| 직원 실용성 | 3 |
| Agent 판단성 | 5 |
| Demo Wow | 5 |
| 기존 Case 대비 차별성 | 3 |
| Brief Fit | 4 |
| **총점** | **31** |

---

### DC-012 — 판매중단 펀드 보유 고객의 «같은 펀드 더 사고 싶다» 요청

#### 1. Case Concept
성과부진으로 판매중단된 펀드를 보유한 고객이 최근 반등을 보고 추가 매수를 요청할 때, Agent 가 «신규 자금 유입 불가(판매중단) · 판매 재개 가능성은 시점 의존 · 현재 상태는 [04-12-17A] 조회로만 확정» 을 안내하고, 보유 유지 여부는 별개의 결정임을 분리하는 실행 불가 Case.

#### 2. Why This Case Exists
```text
Reference:   02_IRP관리방법론 (성과부진 펀드 관리 유형 C) · [HTML-Theme] 문세영·박은영(환매추천 편입)
Knowledge:   OK-017(판매중단 = 신규 유입 불가·보유 유지 가능·재개 가능·[04-12-17A]) · PRD-022(21종 목록 — As-of 불명, 현재 상태 단정 금지) · KG-008(sellable 현재값 미확인) · TALK-004(성과부진 펀드 해피콜 — 민감·비대면 특정펀드 금지)
Source:      SRC-002 L18~35·L215~245 · SRC-097
Golden/Case: GC-06 은 −38% 손실 + «비교 요청». 본 후보는 «더 사겠다» 요청 → 실행 불가 축 [Gap-5]. HTML 문세영은 «환매추천» 용어(repo 는 «판매중단/성과부진») — 용어 차이 TO REVIEW.
```

#### 3. Trigger
고객 앱 매수 시도 실패(판매중단 상품) 또는 발화 «이거 더 사고 싶은데 안 보여요».

#### 4. Customer Context
```text
재직기 · 40대 · 위험중립형 · 보유 펀드 중 1종이 판매중단 목록(문서 시점) · 최근 3개월 반등
```

#### 5. Interesting Evidence Combination
```text
판매중단 펀드 보유(문서 시점 기준)
+ 앱 매수 시도 실패
+ 3개월 수익률 반등
+ [04-12-17A] 미조회 상태(현재 sellable 미확인)
+ 성향 위험중립(대체 유형은 4~6등급)
```

#### 6. Potential Segment
`재직기` × `판매중단 펀드 보유` × `추가 매수 요청` × `실행 불가` × `시점 의존`

#### 7. Potential Badges
```text
Primary:   판매중단 펀드 보유 (As-of 표시)
Secondary: 추가 매수 요청
Signal:    앱 매수 실패
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-017 · OK-006 (대체 유형 등급)
Product:            PRD-022 (목록·As-of 불명) · PRD-033 (위험중립 월간 포트폴리오 — 유형 참고)
Hot Tip:            HT-044 (매도 우선순위·리밸런싱 계산기 — 교체 시)
Talk:               TALK-004 (한계 인정 교체 화법 · 민감) · TALK-005
Screen:             SCR-004 [04-12-17A] · SCR-001 · SCR-010
Knowledge Gap / Conflict: KG-008 sellable 현재값 · PRD-022 As-of · «환매추천»(HTML) vs «판매중단»(repo) 용어
```

#### 9. Expected Agent Discovery
«사고 싶다» 는 요청은 지금 실행이 안 되며, 그 이유(판매중단)는 **손실과 별개**라는 것. 판매 재개 여부는 시점 의존이라 화면 확인 없이는 «영구 불가» 도 «곧 재개» 도 말할 수 없다.

#### 10. Required Confirmation
```text
Employee Check: [04-12-17A] 현재 조회 여부(재개 시 표시) · 보유 펀드 현재 상태
Customer Check: 추가 매수 이유(반등 기대) · 보유 유지 의사 · 대체 유형 관심
```

#### 11. Potential Management Direction
```text
If 판매중단 유지 확인:
→ 추가 매수 불가 안내 + (원하면) 위험중립 범위 대체 유형 정보 — 내점
If 재개 확인:
→ 매수 가능 안내 (성향 범위 내)
```

#### 12. Forbidden Shortcut
```text
«곧 재개된다/영구 불가» 단정 · 판매중단이므로 즉시 매도 권유 · 유선 특정 펀드 대체 권유(OK-029) · 반등 지속 전망
```

#### 13. Expected Brief Fit
- **S1**: 보유·매수 실패·반등·요청.
- **S2** — Main: 실행 불가 사유와 유지 결정 분리. Why now: 요청 직후. Customer check: 이유·유지 의사.
- **S3**: 정보 + 조건부 대체(내점).
- **S4**: Opening «앱에서 안 보인 건 그 펀드가 지금 신규 판매를 안 받아서예요 — 가지고 계신 건 그대로예요». 반론 «그럼 나쁜 펀드예요?» → TALK-004 한계 인정.
- **S5**: [04-12-17A] · HT-044 · 후속: 재개 여부 월간 확인.

#### 14. Potential Chat Questions
```text
판매중단이면 가진 것도 팔아야 해?
다시 살 수 있게 되기도 해?
비슷한 펀드로 바꾸면 뭐가 있어?
```

#### 15. Demo Wow
«못 산다» 를 «나쁘다» 와 분리해 말하는 Agent — 판매 상태의 시점 의존성을 화면 확인으로 연결한다.

#### 16. Grounding Status
```text
MEDIUM (OK-017 T2 / 목록 As-of 불명 — KG-008 명시 필수)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 3 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **29** |

---

### DC-013 — 현금성자산 증가 · 입금사유 «교체매매» · 자동 LMS 발송 예정 → 접촉 불필요

#### 1. Case Concept
현금성자산이 늘어 «현금성 대기» 리스트에 올라온 고객을 Agent 가 [04-12-644] 입금사유로 되짚어 **교체매매 진행 중**임을 확인하고, 매월 자동 발송되는 현금성자산 안내 LMS 까지 겹치면 «지금 연락은 과잉» 이라고 판단하는 Negative Case.

#### 2. Why This Case Exists
```text
Reference:   02_IRP관리방법론 (현금성자산 «미운용» 판별 2요건) · 00_Core_Concept_Design §1 «교체매매 진행 중 → 정상 거래 과정»
Knowledge:   OK-028(판별 기준 ① 1개월 이상 무변동 ② 입금사유가 교체매매·연금지급이 아닐 것 / 100만 이상 매월 LMS 자동 발송 / [75-08-430] 발송이력) · OK-005
Source:      SRC-002 L176~185 · SRC-001
Golden/Case: CASE_001·GC-18·22 는 «현금 = 대기 가능성» 을 유지하는 확인 우선형. «관리 불필요가 유일 정답 + 접촉 자체 과잉» 은 GC-11(연금지급 대기)뿐 — [Gap-4]. SCR-086·OK-028 판별 기준 미사용.
```

#### 3. Trigger
현금성자산 최근 1주 +2,000만 (TG-001 류 고유대 편중 리스트 진입) — 단, 입금사유 «교체매매».

#### 4. Customer Context
```text
재직기 · 40대 · 위험중립형 · 실적배당 중심 · 앱에서 직접 운용(매매 잦음)
```

#### 5. Interesting Evidence Combination
```text
현금성 +2,000만 (7일 전)
+ [04-12-644] 입금사유 «교체매매» (매도 후 재매수 대기)
+ 앱 «보유상품변경» 화면 진입 2회(재매수 탐색)
+ 현금성 100만 이상 → 이달 자동 LMS 발송 예정([75-08-430] 이력)
+ 무변동 기간 7일 (판별 요건 ① 1개월 미충족)
```

#### 6. Potential Segment
`재직기` × `현금성 비중 높음(일시)` × `교체매매 진행` × `직접 운용` × `접촉 불필요`

#### 7. Potential Badges
```text
Primary:   (관리 Badge 없음이 정답 — «현금성 대기» Badge 는 판별 요건 미충족으로 미생성)
Secondary: 교체매매 진행 중
Signal:    상품변경 화면 진입
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-028 (판별 2요건·자동 LMS·용어) · OK-005 (DO 등록 계좌라면 2주 규칙은 «최초 입금» 에만 — 교체매매 대기는 해당 없음: 원문 확인 필요)
Product:            (없음)
Hot Tip:            HT-048 ([04-12-657] 고유대 과다계좌 조회 — 금리 매일 변동)
Talk:               (없음 — 접촉 자체가 과잉)
Screen:             SCR-008 [04-12-644] · SCR-086 [75-08-430] · SCR-073 [04-12-657]
Knowledge Gap / Conflict: 교체매매 대기 자금에 DO 2주/6주 규칙이 적용되는지 원문 미서술 — 단정 금지
```

#### 9. Expected Agent Discovery
«현금성 급증» Badge 가 뜨는 고객의 절반은 정상 거래 과정일 수 있다는 것. 판별 요건과 입금사유를 읽으면 오늘 통화 대상이 아니며, 자동 LMS 가 나가는 달에 사람이 또 연락하면 «감시당한다» 는 인상만 남긴다.

#### 10. Required Confirmation
```text
Employee Check: 없음 (판별 요건 미충족 확인으로 종료) — 2주 후 재조회만 예약
Customer Check: 없음
```

#### 11. Potential Management Direction
```text
If 2주 후에도 무변동:
→ 그때 «미운용 가능성» 으로 재평가(OK-028 요건 ①)
If 재매수 완료:
→ 종료
```

#### 12. Forbidden Shortcut
```text
현금성 비중만 보고 «미운용 방치» 라벨(SG-2) · 자동 LMS 와 별개로 통화 배정 · «고유계정대» 용어로 고객 안내
```

#### 13. Expected Brief Fit
- **S1**: 현금성 증가·입금사유·화면 진입·LMS 예정.
- **S2** — Main: 오늘 관리 대상 아님. Why now: (없음). Customer check: 없음.
- **S3**: 유지 + 2주 후 재조회.
- **S4**: (통화 없음) — 내점 시 «바꾸시는 중이시죠, 필요하면 도와드릴게요» 한 줄.
- **S5**: [04-12-644] · [75-08-430] · 후속: D+14 재조회.

#### 14. Potential Chat Questions
```text
이 고객 현금 늘었는데 전화해야 해?
교체매매 중인 돈도 2주 지나면 DO 로 가?
자동 문자 언제 나갔어?
```

#### 15. Demo Wow
Agent 가 «하지 마세요» 를 근거와 함께 말하는 첫 장면 — 대시보드 15명 중 실제로 연락할 사람을 줄여 준다.

#### 16. Grounding Status
```text
STRONG (OK-028 T2 판별 기준·발송 화면 실존) — DO 규칙 적용 여부만 확인 필요
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 5 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 3 |
| 직원 실용성 | 4 |
| Agent 판단성 | 5 |
| Demo Wow | 5 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 3 |
| **총점** | **33** |

---

### DC-014 — 만기 D-10 · 예약변경 이미 등록 · TM 리스트 «만기 임박 + DO 미등록» → 아무것도 하지 말 것

#### 1. Case Concept
TM 스크립트 §34 유형(1개월 내 만기 + DO 미등록)에 뜬 고객이 실은 지난주 스타뱅킹에서 **만기상품 예약변경을 이미 등록**한 것을 Agent 가 [06-12-611]/[04-12-640] 에서 확인해, DO 등록 안내만 남기고 «만기 재예치 통화» 는 하지 않도록 정리하는 Negative Case.

#### 2. Why This Case Exists
```text
Reference:   05_업무처리절차 (예약변경) · 02_IRP관리방법론
Knowledge:   OK-004(만기 1개월 전 예약변경 · [06-12-611] 즉시/예약/만기예약) · OK-005(DO 미등록이면 만기 후 현금 대기 — 예약변경이 있으면 해당 없음) · OK-026(DO 지정 의무)
Source:      SRC-002 L116 · SRC-041 · SRC-027 L67 · SRC-089
Golden/Case: GC-01·08·22 는 «예약변경을 권하는» 방향. «이미 됐다» 는 시스템 상태에서 개입을 멈추는 Case 는 없음 — [Gap-4] P3-1 취지. SCR-017 미사용.
```

#### 3. Trigger
TM 리스트 배분(만기 D-10 + DO 미등록) — Bank Signal, 판단 입력 아님(HD-7). Agent 의 실제 Trigger 는 만기 D-10 이벤트.

#### 4. Customer Context
```text
재직기 · 50대 · 안정추구형 · 정기예금 중심 · 스타뱅킹 능숙
```

#### 5. Interesting Evidence Combination
```text
정기예금 만기 D-10
+ [06-12-611] 만기예약변경 등록 완료(D-9 전 등록, 같은 유형 정기예금)
+ DO 미등록
+ 앱 «만기상품 예약변경» 메뉴 이용 로그
+ TM 리스트 배분(무시 대상)
```

#### 6. Potential Segment
`재직기` × `원리금 중심` × `만기 처리 완료` × `DO 미등록` × `자기 관리형`

#### 7. Potential Badges
```text
Primary:   만기 D-10 (예약 완료 표시)
Secondary: DO 미등록
Signal:    앱 예약변경 이용
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-004 · OK-005 · OK-026 (DO 지정 의무·계좌별)
Product:            (없음)
Hot Tip:            HT-009 (스타뱅킹 이용 안내 — DO 등록 경로)
Talk:               TALK-008 (DO 거부감 — 등록 안내 시)
Screen:             SCR-017 [06-12-611] · SCR-002 [04-12-640] · SCR-009 스타뱅킹 만기상품 예약변경
Knowledge Gap / Conflict: 없음
```

#### 9. Expected Agent Discovery
Badge(만기 임박)와 리스트(TM)가 가리키는 «해야 할 일» 이 이미 고객 손으로 끝났다는 것. 남는 것은 만기와 무관한 **DO 등록 의무** 하나이고, 그것도 급하지 않다.

#### 10. Required Confirmation
```text
Employee Check: 예약변경 내용(상품·기간)이 정상 등록됐는지 [06-12-611]
Customer Check: 없음 (DO 등록은 앱 안내로 충분)
```

#### 11. Potential Management Direction
```text
현 상태 유지 · 통화 배정 취소 · DO 등록은 앱 안내 메시지(정보) 또는 다음 접점
```

#### 12. Forbidden Shortcut
```text
TM 리스트를 근거로 재예치 통화(F-009) · «DO 미등록 = 만기 후 방치 위험» 으로 통화 명분 생성(예약변경이 있으므로 허위) · 예약된 상품을 바꾸라는 권유
```

#### 13. Expected Brief Fit
- **S1**: 만기 D-10·예약 등록 완료·DO 미등록.
- **S2** — Main: 개입 불필요. Why now: (없음). Customer check: 없음.
- **S3**: 유지 + DO 등록 정보.
- **S4**: (통화 없음) — 메시지 초안 한 줄: «예약변경 확인했어요. 디폴트옵션 등록도 앱에서 1분이면 돼요».
- **S5**: [06-12-611] · 스타뱅킹 DO 등록 경로 · HT-009.

#### 14. Potential Chat Questions
```text
이 고객 만기 통화 해야 해?
예약변경 해놨으면 DO 는 안 해도 돼?
예약해 둔 상품은 뭐야?
```

#### 15. Demo Wow
«Agent 가 통화 목록에서 사람을 빼 준다» — 직원의 시간을 아끼는 관리자 관점 장면.

#### 16. Grounding Status
```text
STRONG
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 3 |
| 직원 실용성 | 5 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 3 |
| **총점** | **32** |

---

### DC-015 — AI투자일임(로보어드바이저) 운용 중 계좌의 «이전/중도인출» 요청

#### 1. Case Concept
IRP 를 AI투자일임으로 운용 중인 고객이 타행 이전 또는 중도인출을 원할 때, Agent 가 «일임 운용 중에는 이전·지급·인출·해지가 제한되고, 해지 시 포트폴리오 전액 자동 매도에 수일이 걸린다» 는 순서 제약을 먼저 세우는 실행 제약 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (AI투자일임)
Knowledge:   OK-027(제휴 3사 · 1인 1계좌 · 연금수령 개시 고객 제외 · 연 900만 · 일임 중 이전/지급/인출/해지 제한 · 해지 시 전액 매도 수일 · 별도 일임 보수 — Public 단독) · OK-015 · OK-002
Source:      SRC-091 · SRC-003
Golden/Case: golden §7 «AI투자일임 계약 중 제약 Case 없음(P2 후보)» — 미해소. GC-11 Critical 에 «AI투자일임 권유» 가 금지로만 등장. SCR-049·050 미사용.
```

#### 3. Trigger
[06-12-604] 포트폴리오 운용현황에 일임 운용 표시 + 고객 발화 «급전이 필요해서 일부 빼고 싶다» 또는 전출 메뉴 진입.

#### 4. Customer Context
```text
재직기 · 40대 · 적극투자형 · IRP 전액 일임 포트폴리오 · 무주택 전세(중도인출 사유 가능성)
```

#### 5. Interesting Evidence Combination
```text
일임 운용 중(연 900만 한도 내 계약 2년차)
+ «전세 잔금에 일부 필요» 발화
+ 잔금일 D-20
+ 중도인출 창구 접수·후선 처리 소요(T3)
+ 일임 해지 → 전액 매도 수일 소요
```

#### 6. Potential Segment
`재직기` × `AI일임 운용 중` × `중도인출 필요` × `실행 순서 제약` × `시한`

#### 7. Potential Badges
```text
Primary:   일임 운용 중 (인출·이전 제한)
Secondary: 중도인출 요청 · 잔금 D-20
Signal:    전출/인출 메뉴 진입
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-027 · OK-015 (전세보증금 사유·잔금일 후 1개월·세전·창구) · OK-009 (과세) · OK-016 (일임 보수 별도)
Product:            (없음)
Hot Tip:            HT-011 (중도인출 세전 신청·창구 접수)
Talk:               (없음)
Screen:             SCR-050 [06-12-604] 운용현황 · SCR-049 [06-12-605] 운용중단 · SCR-038 [02-12-220] · SCR-021 [06-12-501]
Knowledge Gap / Conflict: OK-027 은 Public 단독 — 행내 처리 절차·확인 화면 원문 미확보 · 일임 여부 확인 화면은 SRC-027 Master 의 [06-12-604]/[06-12-605] 로 추정(SCR 등록됨)
```

#### 9. Expected Agent Discovery
중도인출 자체는 사유가 되어도, **일임 해지가 선행**되어야 하고 그 매도에 수일이 걸리므로 잔금일 역산 일정이 달라진다는 것. 이전 요청도 같은 제약을 받는다.

#### 10. Required Confirmation
```text
Employee Check: 일임 계약 상태·해지 소요일(운용사) · 무주택 요건 · 신청 시기(잔금 후 1개월)
Customer Check: 필요 금액·시점 · 일임 전체 해지 수용 여부(일부 해지 가능 여부는 원문 미서술)
```

#### 11. Potential Management Direction
```text
If 잔금 시급:
→ 일임 해지 → 매도 완료 → 중도인출(세전 신청) 순서와 일정 역산 — 정보+절차
If 이전 목적:
→ 일임 해지 후 이전 절차(OK-002) — 고객 결정
```

#### 12. Forbidden Shortcut
```text
일임 중 즉시 인출 가능 안내 · 일부 해지 가능 단정 · 인출 세액 계산값 · 일임 해지 만류(은행 목적)
```

#### 13. Expected Brief Fit
- **S1**: 일임 운용·발화·잔금 D-20.
- **S2** — Main: 순서 제약(해지 선행). Why now: 잔금 시한과 매도 소요. Customer check: 금액·시점·수용.
- **S3**: 절차 순서(순번) + 일정 역산.
- **S4**: Opening «로보 운용 중이라 바로 빼는 게 아니라 순서가 있어서 미리 말씀드려요». 사전고지: 일임 보수·매도 소요.
- **S5**: [06-12-604] · [06-12-605] · [02-12-220] · [06-12-501] · 후속: 매도 완료 확인.

#### 14. Potential Chat Questions
```text
로보로 굴리는 중인데 돈 일부 뺄 수 있어?
일임 해지하면 며칠 걸려?
해지하면 일임 보수는 어떻게 돼?
```

#### 15. Demo Wow
«실행 불가» 가 아니라 «순서가 있다» 를 보여주는 Case — 로보어드바이저라는 신규 요소가 Demo 에 신선하다.

#### 16. Grounding Status
```text
MEDIUM (OK-027 Public 단독 — 행내 절차 원문 보강 필요)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **33** |

---

### DC-016 — 보유 TDF 빈티지 · 은퇴 예정 변경(CRM) · «TDF 하나 더 사야 하나»

#### 1. Case Concept
TDF2035 를 보유한 고객이 최근 상담에서 «은퇴를 65세로 늦췄다» 고 말했을 때, Agent 가 «빈티지 = 출생연도 + 예상 은퇴연령» 산식으로 재산정이 필요함을 짚되, 특정 상품을 단정하지 않고 «빈티지·H/UH·성향 등급(4~6)·운용사별 등급 차이» 의 선택 기준을 안내하는 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (TDF 빈티지 선택법) · [HTML-Theme] 윤소라(TDF 2038 vs 은퇴 목표 2045)
Knowledge:   OK-025(빈티지 산식·글라이드패스·H/UH·적격 100%) · PRD-034(운용사×빈티지 위험자산 비중표 — 판독불확실, 확정 인용 금지) · PRD-001~004(TDF 시리즈 등급) · TALK-019(투자가능기간 재산정 논리) · HT-040(TDF 운용지시 변경 경험담 — 시장 방향 단정 주의)
Source:      SRC-090 · SRC-094 · SRC-020 · SRC-078
Golden/Case: GC-17 은 «TDF 골라달라»(34세, 미보유). 본 후보는 **보유 중 + 은퇴 계획 변경** — 재산정 축. HTML 윤소라 Theme 를 «수익률 비교» 가 아니라 «기간 재산정» 으로 재구성(HTML 의 +3.8% vs +5.2% 비교는 KG-001 수익률 정의 Gap 때문에 쓰지 않음).
```

#### 3. Trigger
CRM 최근 발화 «은퇴 65세로 연기» + 보유 TDF 빈티지가 종전 은퇴 계획(60세) 기준.

#### 4. Customer Context
```text
재직기 · 50세(1976년생) · 위험중립형 · TDF2035 40% + 정기예금 60% · DO 알파드림
```

#### 5. Interesting Evidence Combination
```text
CRM «은퇴 65세로 연기» (2주 전)
+ 보유 TDF2035 (1976+60 기준)
+ 산식상 재산정 → 2040 (1976+65 = 2041 → 5년 단위)
+ 성향 위험중립(4~6등급) — 운용사별 같은 빈티지도 등급 상이(PRD-003 노트)
+ 앱 TDF 상세 조회 2회
```

#### 6. Potential Segment
`은퇴준비기` × `TDF 보유` × `은퇴 시점 변경` × `TDF 관심` × `기준 안내`

#### 7. Potential Badges
```text
Primary:   은퇴 예정 변경
Secondary: TDF 빈티지 재산정 필요
Signal:    TDF 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-025 · OK-006 (등급 상한) · OK-012 (TDF 100% 예외)
Product:            PRD-001 KB온국민(다소높은) · PRD-002 신한(다소높은) · PRD-003 한화(다소높은) · PRD-004 마이다스(보통) — 위험중립형은 «보통» 이하만 신규 매수 가능(C2) · PRD-034 (참고, 확정 인용 금지)
Hot Tip:            HT-040 (주기 점검 — 시장 단정 주의)
Talk:               TALK-019 · TALK-021
Screen:             SCR-004 [04-12-17A] · SCR-011 스타뱅킹 운용상품 찾기 · SCR-010 보유상품변경
Knowledge Gap / Conflict: PRD-034 판독불확실 · 빈티지 «교체» 시 매도·재매수 공백(환매 T+3, HT-043 T3) · 수익률 비교는 KG-001 로 사용 금지
```

#### 9. Expected Agent Discovery
빈티지는 «수익률» 이 아니라 **은퇴 시점**으로 정한다는 것, 그리고 은퇴 계획이 바뀌면 산식이 바뀐다는 것. 다만 같은 2040 이라도 운용사에 따라 등급이 달라 위험중립형은 «보통» 이하만 신규 매수 가능하다는 제약을 함께 본다.

#### 10. Required Confirmation
```text
Employee Check: 후보 빈티지의 운용사별 위험등급([04-12-17A]) · 보유 TDF 등급
Customer Check: 은퇴 시점 확정 여부 · 기존 TDF 유지/교체 의향 · 환헤지 선호(H/UH)
```

#### 11. Potential Management Direction
```text
If 은퇴 연기 확정:
→ 신규 자금은 재산정 빈티지·등급 범위 내 유형 안내, 기존 TDF 는 유지도 합리(교체 강요 없음)
If 미확정:
→ 확인 후 결정, 현 상태 유지
```

#### 12. Forbidden Shortcut
```text
«TDF2040 으로 바꾸세요» 상품 확정(G1) · 수익률 차이로 교체 근거 생성(KG-001) · 빈티지 불일치 = 관리 필요 단정 · 3등급 TDF 권유(C2)
```

#### 13. Expected Brief Fit
- **S1**: 보유 TDF·은퇴 연기 발화·조회.
- **S2** — Main: 빈티지 재산정 기준. Why now: 은퇴 계획 변경. Customer check: 확정 여부·H/UH.
- **S3**: 기준 안내 + 유형 후보(등급 범위) — 단정 없음.
- **S4**: Opening «은퇴를 65세로 보신다고 하셨죠 — TDF 는 그 해에 맞춰 고르는 상품이라 한 번 같이 볼까요». 반론 «지금 것 팔아야 해요?» → 유지도 합리.
- **S5**: OK-025 · [04-12-17A] · HT-040 · 후속: 결정 후 앱 매수 안내.

#### 14. Potential Chat Questions
```text
TDF 뒤 숫자는 어떻게 정해?
은퇴 늦추면 지금 TDF 는 팔아야 해?
H 랑 UH 는 뭐가 달라?
```

#### 15. Demo Wow
HTML 윤소라의 «빈티지 불일치» Theme 를 «수익률 비교» 대신 **산식·기간**으로 다시 세운 정합적 재구성.

#### 16. Grounding Status
```text
STRONG (OK-025 T2+Public) — 개별 빈티지 등급은 화면 확인
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 3 |
| Brief Fit | 4 |
| **총점** | **30** |

---

### DC-017 — ELB 만기 · 연금개시 예정 · «연금지급 가능 여부는 상품별로 다르다»

#### 1. Case Concept
ELB(파생결합사채)를 보유한 연금개시 예정 고객에게, Agent 가 «ELB 는 상품기관별로 연금지급 가능/불가가 갈리고 예금자보호 비대상이며 최소 청약 5천만·협의등록 필요» 라는 특성을 결합해, 만기 재운용 전에 **직원이 먼저 확인할 것**을 세우는 직원 확인 우선 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (원리금보장상품 4종 · ELB) · 05_업무처리절차 (상품협의 등록)
Knowledge:   OK-010(ELB — 예금자보호 비대상·최소 5천만·청약기간·[06-12-650] 협의등록·연금지급 가능/불가 구분) · OK-011(연금지급 예정 고객은 ELB 연금지급 가능 여부 확인 필수 — 메리츠 가능/교보·IBK 불가 예) · OK-013 · TALK-009(원픽 가이드 — 연금개시 예정 행)
Source:      SRC-097 L175~197 · SRC-001 L261~264 · SRC-027 L?(파생상품청약)
Golden/Case: golden §7 «ELB 실제 청약 없음(P2 후보 — 보류)». GC-08 은 ELB 를 «대면·5천만·비보호» 조건으로만 언급. SCR-048·019·OK-011 미사용.
```

#### 3. Trigger
ELB 만기 D-30 + 만 55세·가입 5년 충족 + CRM «내년부터 연금 받을 생각».

#### 4. Customer Context
```text
연금개시 예정 · 60세 · 안정추구형 · ELB 3년물 4,000만(만기 D-30) + 정기예금 · DO 지켜드림
```

#### 5. Interesting Evidence Combination
```text
ELB 만기 D-30
+ 연금개시 예정(내년) 발화
+ 재운용 후보로 «ELB 재청약» 고려 중(앱 청약 안내 조회)
+ 상품기관별 연금지급 가능 여부 상이
+ ELB 는 예금자보호 비대상·최소 5천만 청약
```

#### 6. Potential Segment
`연금개시 예정` × `원리금 중심` × `ELB 보유` × `재운용 시점` × `직원 확인 우선`

#### 7. Potential Badges
```text
Primary:   ELB 만기 D-30
Secondary: 연금개시 예정 · 상품 확인 필요
Signal:    청약 안내 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-010 · OK-011 · OK-013 (개시 요건·수령 방식) · OK-017 ([04-12-17A] 협의 필요 상품 미표시)
Product:            PRD-018 GIC 라인업(연금지급 가능·예보 대상 — 대안 유형) · 시중은행 정기예금 유형(OK-010)
Hot Tip:            (없음)
Talk:               TALK-009 (연금개시 예정 고객 원리금보장 구성 — bank_objective 행 제외)
Screen:             SCR-048 [06-12-159] 파생상품청약 · SCR-019 [06-12-650] 상품협의 · SCR-007 [02-12-221] · SCR-004
Knowledge Gap / Conflict: ELB 상품별 연금지급 가능 여부는 원문 예시(3개사)만 — 개별 상품은 확인 필요 · 특별중도해지 적용 범위(OK-011 Limitation)
```

#### 9. Expected Agent Discovery
«원리금보장이니 아무거나» 가 아니라, 연금개시 예정 고객에게 ELB 는 **지급 가능 여부·예보 비대상·최소 금액** 세 가지가 걸린다는 것. 직원이 먼저 확인해야 상담에서 잘못 안내하지 않는다.

#### 10. Required Confirmation
```text
Employee Check: 보유 ELB 발행사 연금지급 가능 여부 · 재청약 후보 상품의 지급 가능 여부·청약기간·최소금액 · [06-12-650] 협의 필요 여부
Customer Check: 개시 시점·수령 방식 · 재운용 유형 선호(GIC/정기예금/ELB)
```

#### 11. Potential Management Direction
```text
If 개시 시점이 ELB 만기 내:
→ 연금지급 가능 상품 또는 GIC·정기예금(예보 대상) 유형으로 재운용 안내 — 조건부
If 개시가 3년 후:
→ ELB 재청약도 선택지(청약 조건·비보호 고지)
```

#### 12. Forbidden Shortcut
```text
«ELB 도 원리금보장이니 예금자보호 된다» · 발행사 확인 없이 «연금지급 가능» 안내 · 비대면 ELB 청약 안내(대면·최소금액) · GIC 금리(연복리)와 ELB 금리 단순 비교
```

#### 13. Expected Brief Fit
- **S1**: ELB 만기 D-30·개시 예정·조회.
- **S2** — Main: 재운용 전 직원 확인 3가지. Why now: 만기 D-30 + 개시 시점. Customer check: 개시 시점·유형.
- **S3**: 지급 가능 유형 재운용 / ELB 재청약(조건부).
- **S4**: Opening «만기 앞둔 상품이 연금 받을 때 지급이 되는지부터 저희가 먼저 확인했어요». 사전고지: 예보 비대상·최소 청약.
- **S5**: [06-12-159] · [06-12-650] · [02-12-221] · TALK-009 · 후속: 확인 후 재통화.

#### 14. Potential Chat Questions
```text
ELB 는 예금자보호 돼?
연금 받을 때 ELB 에서 지급이 안 될 수도 있어?
ELB 청약은 앱으로 돼?
```

#### 15. Demo Wow
«직원이 먼저 확인할 것» 이 관리 포인트가 되는 Case — 상품 지식의 깊이로 신뢰를 만든다.

#### 16. Grounding Status
```text
STRONG (OK-010·011 T2) — 개별 상품 지급 가능 여부는 확인 필요
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **34** |

---

### DC-018 — 연금개시 예정 · 정기예금 만기 2년 잔여 · «연금 받으려면 예금 깨야 하니 손해 아니냐» 오해

#### 1. Case Concept
개시 요건을 충족한 고객이 «예금 만기가 2년 남아서 연금 신청을 미루겠다» 고 말할 때, Agent 가 «연금지급 사유 해지는 특별중도해지로 약정이율을 일할 지급한다(중도해지 불이익 없음)» 는 제도 사실로 오해를 정정하고, 그래도 개시 여부는 고객 결정임을 유지하는 정보 안내 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (일반/특별중도해지) · 03_영업화법 (연금수령 상담)
Knowledge:   OK-011(일반중도해지 약정이율 50~90% vs 특별중도해지 약정이율 일할 — 연금지급 사유) · OK-013(요건·수령방식·[02-12-221]) · OK-016(연금수령 고객 수수료 면제) · HT-005(연금수령한도 내 일시금·자유인출)
Source:      SRC-097 L193~196 · SRC-003 §02-4 · SRC-046
Golden/Case: GC-08 은 «중도해지 손실 계산 후 유지» (일반중도해지 축). 본 후보는 **특별중도해지 오해 정정** — 세제/이율 오해 정정형 [Gap-6]. OK-011 은 GC-23 K-003 으로만 사용.
```

#### 3. Trigger
CRM «예금 깨면 손해라 연금은 나중에» 발화 + 개시 요건 충족 + 정기예금 만기 2027-09.

#### 4. Customer Context
```text
연금개시 가능 · 57세 · 안정추구형 · 정기예금 3년물 70% + GIC 30% · 소득 공백(퇴직)
```

#### 5. Interesting Evidence Combination
```text
발화 «예금 깨야 해서 손해»
+ 개시 요건 충족(55세+5년)
+ 정기예금 만기 2년 잔여
+ 소득 공백(재취업 미정) — 생활비 필요 가능성
+ 연금수령 시 수수료 면제(OK-016 ①)
```

#### 6. Potential Segment
`연금개시 가능` × `원리금 중심` × `제도 오해` × `소득 공백` × `고객 결정`

#### 7. Potential Badges
```text
Primary:   연금개시 가능
Secondary: 개시 보류 사유 = 오해 가능성
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-011 · OK-013 · OK-016 · OK-009 (수령 시 과세 구조 — 계산은 화면)
Product:            (없음)
Hot Tip:            HT-005 (금액지정 vs 자유인출 실무 — T3) · HT-016 (개시 절차)
Talk:               TALK-007 (인출 구조 점검) · TALK-012 (부분 인출 대안 구조)
Screen:             SCR-007 [02-12-221] · SCR-012 스타뱅킹 연금 수령관리 · SCR-001 (중도해지 예상조회)
Knowledge Gap / Conflict: «약정이율 50~90%» 수준·특별중도해지 사유 범위는 연수 교재 서술 — 개별 상품 약관 확인(OK-011 Limitation)
```

#### 9. Expected Agent Discovery
고객이 개시를 미루는 이유가 **사실이 아닌 전제**(중도해지 손실)에 서 있다는 것. 전제를 바로잡아도 «개시할지» 는 소득·생활비·수령 방식에 달린 고객 결정이며, Agent 는 결정을 대신하지 않는다.

#### 10. Required Confirmation
```text
Employee Check: 보유 예금의 특별중도해지 적용 여부(상품별 약관) · [02-12-221] 수령 예상
Customer Check: 생활비 필요 시점·규모 · 수령 방식 선호 · 재취업 여부
```

#### 11. Potential Management Direction
```text
If 생활비 필요:
→ 오해 정정 + 수령 방식 3가지 정보 + [02-12-221] 예상조회 — 결정은 고객
If 필요 없음:
→ 운용 지속(개시 강요 금지, GC-10 취지)
```

#### 12. Forbidden Shortcut
```text
«그러니 지금 개시하세요» (GC-10 Critical) · 특별중도해지를 모든 상품에 단정 · 수령액·세액 계산값 · 수수료 면제 무조건 적용(1년 내 이전 시 미적용)
```

#### 13. Expected Brief Fit
- **S1**: 요건 충족·발화·예금 만기·소득 공백.
- **S2** — Main: 오해 정정 + 개시는 고객 결정. Why now: 소득 공백. Customer check: 생활비·방식.
- **S3**: 정보 안내 / 운용 지속 — 복수 방향.
- **S4**: Opening «예금 깨야 해서 미루신다고 들었는데, 연금 지급 사유로 해지하면 이자 손해가 없는 구조라 그 걱정은 안 하셔도 돼요». 사전고지: 상품별 확인.
- **S5**: OK-011 · [02-12-221] · HT-016 · 후속: 방식 결정 후 절차.

#### 14. Potential Chat Questions
```text
연금 받으려고 예금 깨면 이자 손해 봐?
연금 받기 시작하면 수수료는?
소득 없으면 지금 받는 게 유리해?
```

#### 15. Demo Wow
Agent 가 고객의 «잘못된 전제» 를 찾아낸다 — 판단이 아니라 **사실 하나**로 상담이 열리는 장면.

#### 16. Grounding Status
```text
STRONG (OK-011·013·016 T2) — 상품별 약관 확인 필요
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 5 |
| **총점** | **34** |

---

### DC-019 — «금리 높은 GIC 로 전부 바꿔달라» · 연복리/단리 환산 · 저축은행 매수한도 · 예금자보호 한도 충돌

#### 1. Case Concept
정기예금 만기자금 1.2억을 «금리 제일 높은 데로 다» 넣어 달라는 안정추구형 고객에게, Agent 가 «GIC 는 연복리 공시이율이라 단리 환산이 필요하다 · 저축은행은 예보 한도 이내 매수한도(9,500/9,000만)가 있다 · 예보 한도는 원천 간 충돌(SC-001)이라 확정 안내 금지» 를 결합해 조건부로 구성하는 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (원리금보장상품 4종·단리환산) · [HTML-Theme] 김형준·최지현(«3년 이율보증형 4.38% 비교»)
Knowledge:   OK-010(4종 특성·단리 환산 계산기·저축은행 매수한도·예보 1억(SC-001)) · PRD-018(GIC 라인업 연복리·as_of 2026-07) · PRD-019(저축은행 유형·KG-007 개별 상품 부재) · SC-001 · TALK-009(원픽 가이드 — 고금리 추구 행)
Source:      SRC-097 · SRC-001 · SRC-002 L112
Golden/Case: GC-01·08 이 원리금보장 «내» 대안 비교를 다루지만 단리 환산·매수한도·SC 전달은 없음 — P3-4(CONFLICT 전달)·P3-7(Freshness) 미검증. HTML 김형준 Case 의 «4.38% vs 3.30%» 병렬 표시 오류(Audit P1-10)를 복제하지 않는 재구성.
```

#### 3. Trigger
정기예금 만기 D-15 + 내점 «제일 높은 금리로 전부».

#### 4. Customer Context
```text
은퇴준비기 · 58세 · 안정추구형 · 정기예금 1.2억 만기 · DO 지켜드림 · 예금자보호에 민감
```

#### 5. Interesting Evidence Combination
```text
만기 1.2억 D-15
+ 발화 «제일 높은 금리로 다»
+ GIC 4.4%대(연복리) vs 정기예금 3.2~3.7%(단리) — 표시 기준 상이
+ 저축은행 1년제 매수한도 9,500만 (1.2억 전액 불가)
+ 예보 한도 5천만(구자료) vs 1억(2026) — SC-001 OPEN
```

#### 6. Potential Segment
`은퇴준비기` × `원리금 100%` × `재운용 시점` × `고금리 추구` × `예보 민감` × `Source Conflict`

#### 7. Potential Badges
```text
Primary:   정기예금 만기 D-15
Secondary: 전액 고금리 요청 · 매수한도 확인
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-010 · OK-017 (월 단위 라인업 변동 · [04-12-17A]) · OK-011 (GIC 3·5년물 중도해지 조건)
Product:            PRD-018 (as_of 2026-07·08 — 시점 명시) · PRD-019 (유형만) · PRD-020 (수협 — bank_objective 주의)
Hot Tip:            HT-044 (리밸런싱 계산기) · HT-048 (예금금리 월단위 확정)
Talk:               TALK-009 (bank_objective 행 제외) · TALK-030 유형1 (예보 5천만 표기 인용 금지)
Screen:             SCR-004 [04-12-17A] · SCR-018 [04-12-179] 금리·한도 · SCR-017 [06-12-611]
Knowledge Gap / Conflict: SC-001 예보 한도(OPEN — HD-P2-GATE2 (5) 비노출·확정 안 함) · KG-007 저축은행 개별 상품 · 금리 as_of 월 변동
```

#### 9. Expected Agent Discovery
«제일 높은 금리» 가 표시 기준 때문에 착시일 수 있다는 것(단리 환산), 전액을 한 저축은행에 넣을 수 없다는 것(매수한도), 그리고 예보 한도는 **원천이 충돌해 지금 확정 안내할 수 없다**는 것 — 세 겹의 제약을 고객에게 정직하게 보여준다.

#### 10. Required Confirmation
```text
Employee Check: 이달 특별제공 라인업·금리 as_of([04-12-17A]·Info-zone) · 단리 환산 계산기 결과 · 예보 한도 현행 기준(공식)
Customer Check: 기간 선호(1·3·5년) · 분할 의향 · 중도해지 가능성(GIC 조건)
```

#### 11. Potential Management Direction
```text
If 분할 수용:
→ 기관 분산(매수한도 내) + 기간 사다리 — 유형 수준, 금리는 as_of 병기
If 단일 상품 고집:
→ 시중은행 정기예금(가입금액 제한 없음) 또는 GIC — 단리 환산 후 비교
```

#### 12. Forbidden Shortcut
```text
연복리 GIC 와 단리 예금 금리 병렬 비교 · 예보 한도 «1억» 또는 «5천만» 확정 안내 · 지난달 금리 인용(as_of 누락) · 수협 예금을 «이탈 방어» 사유로 추천(G4)
```

#### 13. Expected Brief Fit
- **S1**: 만기 1.2억·요청·성향.
- **S2** — Main: 세 제약(환산·한도·예보 충돌). Why now: D-15. Customer check: 기간·분할.
- **S3**: 분산 구성 유형 — 조건부, 금리는 «이달 기준».
- **S4**: Opening «높은 금리로 다 넣고 싶으신 건 맞는데, 표시가 달라서 같은 기준으로 바꿔 보면 순서가 바뀔 수 있어요». 사전고지: 예보 한도는 확인 후 안내.
- **S5**: 단리 환산 계산기 경로 · [04-12-17A] · [04-12-179] · HT-044.

#### 14. Potential Chat Questions
```text
GIC 4.4% 랑 예금 3.5% 진짜 그만큼 차이 나?
저축은행에 1억 넘게 넣으면 안 돼?
예금자보호 한도가 5천만이야 1억이야?
```

#### 15. Demo Wow
Agent 가 «모른다(충돌)» 를 화면에 그대로 내는 장면 — SOURCE_CONFLICTS 를 소비하는 첫 Case.

#### 16. Grounding Status
```text
STRONG (OK-010 T2) — SC-001 은 의도적으로 «미확정» 으로 전달
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 5 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **34** |

---

### DC-020 — «개시하겠다» 결정 고객의 실행 순서 — 미신청분 등록 → 자동이체 정리 → 지급설계

#### 1. Case Concept
연금개시를 결정한 고객에 대해 Agent 가 «개시 전에 세액공제 미신청분을 [06-12-622] 에 등록하지 않으면 과세제외분이 과세되고, 자동이체가 살아 있으면 개시 후 추가입금 불가와 충돌하며, 지급설계는 [02-12-221] 에서 방식·한도를 정한다» 는 **순서 함정**을 순번으로 정리하는 실행 지원 Case.

#### 2. Why This Case Exists
```text
Reference:   05_업무처리절차 (연금지급 절차) · 04_제도상품팩트 (미공제분 과세제외)
Knowledge:   OK-009(미신청분 등록 [06-12-622] · 소득·세액공제확인서 · 7/1 은 T3) · OK-013(수령방식·최소기간·한도·[02-12-221]) · OK-019(개시 후 신규 IRP 당일 개설) · HT-016(개시 절차 — 개시 전 [04-10-099] 이전 가능 상품 확인 «개시 후 이전 불가» · ①[06-12-622] → ②[02-12-221]) · HT-017/049(미신청금액 계산기) · HT-048([02-12-223] 개시 시 추가입금 불가)
Source:      SRC-003 · SRC-049 · SRC-050 · SRC-054 · SRC-086
Golden/Case: GC-10·12 는 «정보 준비» 로 끝남 — 실행 순서 Case 없음 [Gap-3]. SCR-006·007·064·012, HT-016 미사용.
```

#### 3. Trigger
CRM «다음 달부터 연금 받겠다» + 자동이체 월 30만 진행 중 + 미신청분 존재(시스템 표시).

#### 4. Customer Context
```text
연금개시 결정 · 60세 · 안정추구형 · 정기예금+GIC · 세액공제 받은 부담금 + 미신청분 혼재 · 타사 연금저축 보유
```

#### 5. Interesting Evidence Combination
```text
개시 결정 발화
+ 자동이체 진행 중(개시 후 추가입금 불가와 충돌)
+ 직전 연도 미신청분 존재
+ 타사 연금저축 보유 → 개시 후 이전 불가(HT-016) — 합칠지 먼저 결정
+ 수령 방식 미정
```

#### 6. Potential Segment
`연금개시 결정` × `원리금 중심` × `실행 순서` × `절세(미신청분)` × `외부 연금계좌`

#### 7. Potential Badges
```text
Primary:   연금개시 결정
Secondary: 자동이체 진행 중 · 미신청분 미등록 · 타사 연금저축 보유
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-009 · OK-013 · OK-019 · OK-020 (개시 전 이전 요건) · OK-016 (개시 시 수수료 면제)
Product:            (없음)
Hot Tip:            HT-016 · HT-017 · HT-049 · HT-048 · HT-005
Talk:               (없음 — 절차형)
Screen:             SCR-006 [06-12-622] · SCR-007 [02-12-221] · SCR-064 [06-12-619] 자동이체 · SCR-015 [04-10-099] · SCR-080 [02-12-223] · SCR-012 스타뱅킹 연금 수령관리
Knowledge Gap / Conflict: KG-004 7/1 발급 T3 · SC-002 미신청금액 화면번호(06-12-622 vs 651/627 — Master 는 622) · 미신청분 등록 절차 상세는 T3
```

#### 9. Expected Agent Discovery
개시는 «버튼 하나» 가 아니라 **되돌리기 어려운 순서**라는 것 — 이전·추가입금·미신청분 등록은 개시 «전» 에만 가능하다. Agent 는 순서를 세우고, 각 단계에서 고객이 결정할 것(합칠지·방식)을 구분한다.

#### 10. Required Confirmation
```text
Employee Check: 미신청분 금액(소득·세액공제확인서) · 자동이체 등록 상태 · [04-10-099] 이전 가능 계좌
Customer Check: 타사 연금저축 통합 여부 · 수령 방식·기간 · 개시 희망일
```

#### 11. Potential Management Direction
```text
순번: ① 이전 여부 결정(개시 전만 가능) → ② 미신청분 등록 [06-12-622] → ③ 자동이체 정리 [06-12-619] → ④ 지급설계 [02-12-221](방식·한도) → ⑤ 개시
If 통합 원함: ①에서 0원 계좌·요건(OK-020) 확인 선행
```

#### 12. Forbidden Shortcut
```text
«바로 개시 등록해 드릴게요» (미신청분·이전 미확인) · 개시 후 추가입금 가능 안내 · 수령액·세액 계산값 · 7/1 규칙 확정 인용(T3)
```

#### 13. Expected Brief Fit
- **S1**: 결정·자동이체·미신청분·타사 연저.
- **S2** — Main: 개시 전 3가지. Why now: 개시 후 불가 항목. Customer check: 통합·방식.
- **S3**: 순번 절차(순번 UI).
- **S4**: Opening «개시하시기 전에 딱 세 가지만 먼저 정리하면 나중에 아쉬운 게 없어요». 사전고지: 개시 후 이전·입금 불가.
- **S5**: 순번 화면 5개 · HT-016 · HT-017.

#### 14. Potential Chat Questions
```text
연금 시작하면 더 못 넣어?
세액공제 안 받은 돈은 어떻게 등록해?
연금 받기 시작하고 나서 다른 데로 옮길 수 있어?
```

#### 15. Demo Wow
박정호 S5 «순번 실행 화면» 의 강점을 연금개시에서 재현 — 실수를 막는 절차 Agent.

#### 16. Grounding Status
```text
STRONG (OK-009·013·019 T2) — 등록 실무·7/1 은 T3 표시
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 5 |
| **총점** | **36** |

---

### DC-021 — 자유인출로 수령 중 · 사적연금 1,500만 경계 · 올해 남은 인출 계획

#### 1. Case Concept
자유인출 방식으로 연금을 받는 고객이 하반기에 목돈 인출을 계획할 때, Agent 가 «연금수령한도(11−연차)×120% · 사적연금 1,500만 초과 시 종합과세/16.5% 분리과세 선택 · 한도 초과분은 원천별 과세» 의 구조를 세우고, 실제 세액은 [02-12-221]·골든라이프센터로 연결하는 결정 지원 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (연금수령한도·분리과세 선택) · 03_영업화법
Knowledge:   OK-013(한도 산식·연차·초과분 과세) · OK-021(1,500만 초과 시 Min(종합, 16.5%) · 인출 조정으로 관리) · OK-030(골든라이프센터 — 연금·세금·보험료) · HT-047(자유인출로 소득 공백기·1,500만 관리 — T3) · HT-005
Source:      SRC-003 L277~279·L301~304·L603~630 · SRC-085 · SRC-046
Golden/Case: 수령 중은 GC-11(금액지정·ETF 불가)뿐 [Gap-2]. OK-021 미사용. HTML 오경숙 Theme(«일시금 vs 연금 세후 차액 2,600만») 의 «계산값 제시» 오류를 복제하지 않고 구조만 제시.
```

#### 3. Trigger
자유인출 수령 중 + 앱 «수시인출» 화면 진입 + 당해 누적 연금소득이 1,500만 근접(시스템 계산).

#### 4. Customer Context
```text
연금수령기 · 63세 · 안정추구형 · 자유인출 3년차 · 정기예금+채권형 · 타사 연금저축도 수령 중(합산 대상)
```

#### 5. Interesting Evidence Combination
```text
자유인출 수령 중(연차 3)
+ 당해 사적연금 수령 누적 1,300만(당행) + 타사 연저(합산 미확인)
+ 앱 수시인출 화면 진입 · «자녀 결혼» 발화
+ 연금수령한도 잔여([02-12-221])
+ 1,500만 경계 · 한도 초과분 과세
```

#### 6. Potential Segment
`연금수령기` × `자유인출` × `절세 경계` × `목돈 인출 계획` × `외부 연금계좌 합산`

#### 7. Potential Badges
```text
Primary:   사적연금 1,500만 경계 근접
Secondary: 연금수령한도 확인 필요
Signal:    수시인출 화면 진입
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-013 · OK-021 · OK-009 (원천별 과세) · OK-030
Product:            (없음)
Hot Tip:            HT-047 (T3 — 전략 표현 주의) · HT-005
Talk:               TALK-020 (월분배 — 무관) · TALK-007
Screen:             SCR-007 [02-12-221] (한도/잔여한도·수령예상) · SCR-012 스타뱅킹 연금 수령관리 · SCR-055 [04-12-651] 증명서
Knowledge Gap / Conflict: 1,500만 기준·세율 선택의 세법 원문 부재(OK-021) · 타사 수령액 합산은 고객 확인 · 최종 세액 = HD-1 밖
```

#### 9. Expected Agent Discovery
«얼마 빼도 되냐» 의 답이 두 겹(연금수령한도 · 1,500만 합산 경계)이고, 타사 수령액까지 합산된다는 것. Agent 는 구조와 확인 순서를 주고 숫자는 화면·센터로 넘긴다.

#### 10. Required Confirmation
```text
Employee Check: [02-12-221] 당해 잔여 한도 · 당행 누적 수령액
Customer Check: 타사 연금 수령액 · 인출 필요 금액·시점 · 내년 분산 가능 여부
```

#### 11. Potential Management Direction
```text
If 한도·경계 내 가능:
→ 인출 시점·분할 정보 + 자유인출 신청 경로
If 초과 예상:
→ 초과분 과세 구조 안내 + 연말/내년 분산 선택지 + 골든라이프센터 연계 — 고객 결정
```

#### 12. Forbidden Shortcut
```text
세액·수령액 계산값 제시(HD-1) · «1,500만 넘으면 무조건 손해» 단정 · 타사 수령액 미확인 상태에서 «경계 내» 확정 · 인출 자제 압박(고객 자금)
```

#### 13. Expected Brief Fit
- **S1**: 자유인출·누적·발화·화면 진입.
- **S2** — Main: 두 겹 경계 확인. Why now: 하반기 인출 계획. Customer check: 타사 수령·금액.
- **S3**: 시점·분할 정보 + 센터 연계.
- **S4**: Opening «결혼 자금 말씀하셨죠 — 올해 안에 빼실 금액이 세금 기준선에 가까워서 순서만 같이 보면 좋겠어요». 사전고지: 정확한 세액은 화면.
- **S5**: [02-12-221] · 스타뱅킹 수령관리 · 골든라이프센터 예약 · HT-047(주의 표시).

#### 14. Potential Chat Questions
```text
올해 얼마까지 빼야 세금이 안 늘어?
다른 회사 연금도 합쳐서 계산해?
한도 넘겨서 빼면 어떻게 돼?
```

#### 15. Demo Wow
수령기 고객에서 Agent 가 «경계» 를 관리하는 장면 — 지금까지 Portfolio 가 비어 있던 축.

#### 16. Grounding Status
```text
MEDIUM (OK-013·021 T2 이나 세법 원문 부재 — 구조까지만)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 5 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **34** |

---

### DC-022 — 만 55세 도달 · 퇴직급여 포함 계좌 · 법정 사유 없는 목돈 필요 → 중도인출 불가 vs 해지 vs 개시 후 한도 내 인출

#### 1. Case Concept
이번 달 만 55세가 된 고객(퇴직급여 포함 → 5년 요건 불요)이 «자녀 유학비로 3,000만 필요» 라고 할 때, Agent 가 «법정 사유가 아니라 중도인출은 불가 · 해지는 퇴직소득세 전액 · 연금개시 후 한도 내 인출은 감면 구조» 세 갈래를 구조로 비교하고, 개시가 가져오는 부작용(추가입금·이전 불가)까지 함께 놓는 결정 지원 Case.

#### 2. Why This Case Exists
```text
Reference:   04_제도상품팩트 (중도인출 사유·연금수령한도·퇴직소득세 감면 3단) · 03_영업화법 (거절유형 Top3 — 부분 인출 대안)
Knowledge:   OK-015(6사유 한정·수령 중이면 해지만) · OK-013(퇴직급여 포함 시 55세만·한도 산식·개시 후 신규 IRP) · OK-009(70/60/50% — 3단) · OK-019 · TALK-012(해지 의사 거절유형 — «연금개시 후 필요액만 인출» 대안) · HT-047
Source:      SRC-003 · SRC-011 §2장 · SRC-085
Golden/Case: GC-12 는 퇴직금 3억·대출 1억(55세, 발화 시점) — 같은 구조. 차별점: 본 후보는 «법정 사유 아님» 을 명시하고 3자 비교의 **첫 갈래(중도인출 불가)** 를 세우며, 감면율은 3단(50% 포함)으로 정확히 — HTML 박정호 Audit P0-1 오류를 복제하지 않는다. [Gap 8.4 «3자 비교» 항목]
```

#### 3. Trigger
만 55세 도달(이번 달) + CRM «유학비 3,000만» + 앱 «중도인출 안내» 조회.

#### 4. Customer Context
```text
연금개시 가능 직후 · 55세 · 위험중립형 · 퇴직급여 포함 적립겸용 · 재직 중(소득 있음)
```

#### 5. Interesting Evidence Combination
```text
만 55세 도달
+ 퇴직급여 포함(5년 요건 불요)
+ 목돈 사유 «유학비»(법정 사유 아님)
+ 재직 중 소득 있음 → 개시 시 1,500만 경계·추가입금 불가 영향
+ 중도인출 안내 조회
```

#### 6. Potential Segment
`연금개시 가능` × `퇴직급여 보유` × `목돈 필요(비법정)` × `고객 결정 지원` × `재직 중`

#### 7. Potential Badges
```text
Primary:   연금개시 가능(이번 달)
Secondary: 목돈 인출 검토 · 중도인출 사유 미해당 가능
Signal:    중도인출 안내 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-015 · OK-013 · OK-009 · OK-019 · OK-021 (1,500만)
Product:            (없음)
Hot Tip:            HT-047 (T3) · HT-005
Talk:               TALK-012 · TALK-007
Screen:             SCR-007 [02-12-221] (퇴직소득세 시뮬레이션·한도) · SCR-038 [02-12-220] · SCR-080 [02-12-223]
Knowledge Gap / Conflict: 감면율 3단 vs HT 2단 표기 병존(Audit P0-1) · 한도·세액 계산은 HD-1 밖
```

#### 9. Expected Agent Discovery
«빼고 싶다» 의 실행 경로가 세 개이고, 첫 번째(중도인출)는 사유 때문에 **닫혀 있다**는 것. 나머지 둘은 세금 구조가 다르고, 개시는 되돌리기 어려운 부작용(추가입금·이전 불가)이 있어 재직 중 고객에게 특히 중요하다.

#### 10. Required Confirmation
```text
Employee Check: [02-12-221] 한도·퇴직소득세 시뮬레이션 · 계좌 구성(퇴직급여/부담금 비율)
Customer Check: 필요 금액·시점 · 재취업/근속 계획(개시 후 추가입금 불가) · 다른 재원 유무
```

#### 11. Potential Management Direction
```text
If 필요 확정:
→ 해지 vs 개시 후 한도 내 인출 — 구조 비교(감면 3단·한도)와 부작용 고지, 결정은 고객
If 다른 재원 가능:
→ 현 상태 유지 + 개시 시점은 별도 논의
```

#### 12. Forbidden Shortcut
```text
«유학비도 중도인출 돼요» · «개시하면 30% 감면» 2단 단정(3단) · 세액 계산값 · «무조건 IRP 에 두세요» (HD-7) · 개시 부작용 미고지
```

#### 13. Expected Brief Fit
- **S1**: 55세·퇴직급여·사유·조회.
- **S2** — Main: 세 갈래 구조. Why now: 이번 달 요건 충족. Customer check: 금액·근속.
- **S3**: 구조 비교 + 화면 연결 — 고객 결정.
- **S4**: Opening «이번 달부터 연금으로 받으실 수 있게 돼서, 유학비 말씀하신 것과 같이 보면 선택지가 셋이에요». 사전고지: 개시 후 추가입금·이전 불가.
- **S5**: [02-12-221] · [02-12-220] · TALK-012 · 후속: 결정 후 절차.

#### 14. Potential Chat Questions
```text
유학비로 중도인출 돼?
연금 개시하고 한꺼번에 빼면 세금 어떻게 돼?
개시하면 회사 다니면서 더 못 넣어?
```

#### 15. Demo Wow
«세 갈래 중 하나가 닫혀 있다» 를 먼저 말하는 정직한 Agent — 감면 3단을 정확히 쓰는 것으로 Seed 의 오류를 넘어선다.

#### 16. Grounding Status
```text
STRONG (OK-013·015·009 T2)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 4 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 3 |
| Brief Fit | 4 |
| **총점** | **32** |

---

### DC-023 — 연금개시 후 재취업 · 추가납입 불가 · 신규 IRP 개설 순서

#### 1. Case Concept
이미 연금을 받기 시작한 고객이 재취업해 회사 DC/부담금 납입이 필요해졌을 때, Agent 가 «개시 계좌는 추가입금 불가([02-12-223]) → 개시 등록된 기존 IRP 를 둔 채 신규 IRP 당일 개설 가능(OK-019) → 적립용 서류·세액공제 지속» 을 순서로 세우는 실행 순서 Case.

#### 2. Why This Case Exists
```text
Reference:   05_업무처리절차 (추가 개설 흐름도) · 03_영업화법 (퇴직금 마케팅 화법)
Knowledge:   OK-019(개시 요건 충족 시 기존 IRP 연금 개시 등록 후 신규 IRP 추가 개설 가능 — 당일) · OK-013 · OK-008(세액공제 지속) · HT-048([02-12-223] 개시 시 추가입금 불가) · HT-001(3단 구성 — bank_objective 태그)
Source:      SRC-003 L306~320 · SRC-086 · SRC-053
Golden/Case: GC-12 Critical «개시 후 추가입금 가능 안내» 로만 등장 — 실제 발화 Case 없음 [Gap-11]. Seed 박정호 챗 q2(재취업 3단)의 «사후 버전».
```

#### 3. Trigger
CRM «재취업했는데 회사에서 IRP 계좌 달라고 한다» + 기존 IRP 연금개시 중.

#### 4. Customer Context
```text
연금수령기 + 재취업 · 58세 · 안정추구형 · 기존 IRP 금액지정 수령 중
```

#### 5. Interesting Evidence Combination
```text
연금개시 중(금액지정 2년차)
+ 재취업 발화 + 회사 DC 가입 예정
+ 기존 IRP 추가입금 불가 상태
+ 세액공제 대상 소득 재발생
+ 개시 계좌와 적립 계좌를 나눠야 하는 구조
```

#### 6. Potential Segment
`연금수령기` × `재취업` × `계좌 추가 개설` × `절세 재개` × `실행 순서`

#### 7. Potential Badges
```text
Primary:   재취업 · 추가 개설 필요
Secondary: 개시 계좌 추가입금 불가
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-019 · OK-013 · OK-008 · OK-016 (신규 계좌 수수료 — 청년 할인은 해당 없음)
Product:            (없음)
Hot Tip:            HT-048 · HT-001 (원문 3단 구성 — 추천사유로 «유치 실적» 사용 불가)
Talk:               TALK-023 (직장인 신규 제안 — 취지만)
Screen:             SCR-080 [02-12-223] · SCR-031 [00-12-210] · SCR-005 [06-12-151] · SCR-055 [04-12-651]
Knowledge Gap / Conflict: 1인 1계좌 원칙과 «추가 개설» 규칙의 관계는 OK-019 흐름도 서술 — 개별 판정은 신규 화면
```

#### 9. Expected Agent Discovery
«기존 계좌에 넣으면 되지» 가 통하지 않는다는 것, 그리고 신규 개설은 **개시 등록이 되어 있어야** 가능하며 당일 처리된다는 것. 세액공제도 새 계좌로 이어진다.

#### 10. Required Confirmation
```text
Employee Check: 기존 계좌 개시 등록 상태([02-12-223]) · 신규 개설 서류(재직 증빙)
Customer Check: 회사 제도(DC/기업형IRP) · 개인 납입 의향·규모
```

#### 11. Potential Management Direction
```text
순번: ① 개시 상태 확인 → ② 신규 적립용 IRP 개설(당일) → ③ 회사 통보·자동이체 → ④ 세액공제 한도 확인
```

#### 12. Forbidden Shortcut
```text
기존 개시 계좌에 입금 안내 · 개시 취소 권유 · 3단 구성을 «유치 실적» 사유로 · 한도 계산값
```

#### 13. Expected Brief Fit
- **S1**: 개시 중·재취업·회사 요청.
- **S2** — Main: 계좌 분리 필요. Why now: 회사 납입 개시. Customer check: 제도·납입.
- **S3**: 순번 절차.
- **S4**: Opening «지금 받으시는 계좌엔 더 못 넣어서, 회사용은 새로 하나 만들면 돼요 — 당일 됩니다». 
- **S5**: [02-12-223] · [00-12-210] · [06-12-151] · HT-048.

#### 14. Potential Chat Questions
```text
연금 받는 계좌에 회사 돈 넣을 수 있어?
IRP 두 개 가져도 돼?
새 계좌도 세액공제 돼?
```

#### 15. Demo Wow
박정호 챗의 «3단 구성» 이 실제로 필요한 순간을 보여주는 후속편.

#### 16. Grounding Status
```text
STRONG (OK-019·013 T2)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 3 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 3 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **29** |

---

### DC-024 — 대출 금리 때문에 «대출이랑 퇴직연금 같이 옮기겠다» · VIP · 전출 접수

#### 1. Case Concept
대출 기한연장 시점에 타행 금리 조건을 이유로 대출과 IRP 를 함께 옮기려는 VIP 고객의 전출 접수에 대해, Agent 가 «대출과 퇴직연금은 판단 기준이 다르다(TALK-014)» 는 화법 재료와 «전출 사전체크 4단계·현금이전 손실 고지·의사확인 절차(OK-002·031)» 를 결합해, 손실을 알린 뒤 고객이 결정하게 하는 이탈 대응 Case.

#### 2. Why This Case Exists
```text
Reference:   03_영업화법 (대출 동반이전·VIP 이탈) · 01_고객세그먼트 «VIP»
Knowledge:   OK-002(사전체크 4단계·리스크 고지·경청) · OK-031(의사확인·자동취소) · OK-003(현금이전 손실 확인·부분이전 미확인 KG-002) · TALK-014(대출·연금 판단 기준 분리 — T3) · TALK-001(VIP 접점 화법 — T2) · HT-034(대출 기한연장 고객 발굴 — bank_objective)
Source:      SRC-015 · SRC-014 · SRC-003 §03-2 · SRC-071
Golden/Case: golden §7 «수수료 단독·대출 동반 이전 Case 없음(P2 후보 — 미해소)» [Gap-7]. GC-16(ETF·수수료)·GC-23(금리 단일)과 사유가 다름. TALK-001·014 미사용.
```

#### 3. Trigger
[06-AD-080] 전출 접수(현금이전, 타행) + 대출 기한연장 D-30 + VIP 등급.

#### 4. Customer Context
```text
재직기 · 40대 · 위험중립형 · VIP · 정기예금 6,000만(만기 8개월 잔여) + TDF 4,000만 · 당행 주택담보대출 보유
```

#### 5. Interesting Evidence Combination
```text
전출 접수 D+0(현금이전)
+ 대출 기한연장 D-30 · 타행 금리 제안 발화
+ 정기예금 중도해지 손실(만기 8개월 잔여) — [04-12-642] 예상조회
+ TDF 환매 공백(T+3)
+ 의사확인 알림톡 당일 18시 · 미확인 시 자동취소(OK-031)
```

#### 6. Potential Segment
`재직기` × `VIP` × `이전/이탈(대출 동반)` × `현금이전 손실` × `고객 결정`

#### 7. Potential Badges
```text
Primary:   전출 접수 D+0
Secondary: 대출 기한연장 D-30 · 중도해지 손실 확인
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-002 · OK-031 · OK-003 · OK-011 (중도해지 이율) · OK-016 (수수료 — 비교 시 as_of)
Product:            (없음 — 이전 방어용 상품 제안은 G4 위반)
Hot Tip:            HT-034 (bank_objective — 발굴 재료로만) · HT-012 (관리 소홀 불만 대응)
Talk:               TALK-014 · TALK-001 · TALK-032 (Step 01~06)
Screen:             SCR-003 [06-AD-080] · SCR-087 [72-01-801] · SCR-001 (중도해지 예상조회) · SCR-044 [04-12-613]
Knowledge Gap / Conflict: KG-002 부분이전 미확인 · TALK-014 는 T3 STT
```

#### 9. Expected Agent Discovery
대출 조건과 연금 관리는 **판단 축이 다르다**는 것 — 그러나 그것을 «옮기지 마세요» 로 쓰지 않고, 현금이전 시 정기예금 중도해지 손실과 TDF 공백을 **숫자 구조**로 먼저 알려 고객이 결정하게 한다. 의사확인 절차(당일 18시 알림톡·미확인 시 자동취소)도 고객 이익 관점에서 안내한다.

#### 10. Required Confirmation
```text
Employee Check: 사전체크 4단계([72-01-801]·[06-AD-080]·[04-12-642]) · 중도해지 예상손실
Customer Check: 이전 사유(대출 조건이 전부인지) · 예금 만기까지 유지 후 이전 의향(부분 경로는 미확인 — Epistemic) · 의사확인 절차 인지
```

#### 11. Potential Management Direction
```text
If 대출 조건이 핵심:
→ 대출 상담 분리 연계 + IRP 는 손실 고지 후 고객 결정(만기 후 이전 선택지 포함)
If 이전 확정:
→ 절차 안내(의사확인 링크·자동취소 기한) — 지연·방해 금지
```

#### 12. Forbidden Shortcut
```text
«이탈 방지» 사유(G4) · 절차 지연 · 부분이전 가능/불가 단정(KG-002) · 타행 금리 조건 비교 단정 · 대출 금리 우대를 IRP 잔류 조건으로 제시(원천 없음)
```

#### 13. Expected Brief Fit
- **S1**: 전출 접수·대출 연장·보유.
- **S2** — Main: 손실 고지 + 사유 분리. Why now: 의사확인 당일. Customer check: 사유·유지 의향.
- **S3**: 고객 결정 지원(손실 구조·선택지).
- **S4**: Opening(TALK-001 취지) «불편하셨던 점 먼저 듣고 싶어요 — 그리고 옮기실 때 예금 하나가 중도해지되는 부분만 확인드릴게요». 
- **S5**: [06-AD-080] · [72-01-801] 녹취 · [04-12-642] 예상조회 · [04-12-613].

#### 14. Potential Chat Questions
```text
지금 옮기면 정기예금은 어떻게 돼?
예금 만기까지 두고 나머지만 옮길 수 있어?
의사확인 문자 안 누르면 어떻게 돼?
```

#### 15. Demo Wow
«떠나는 고객에게도 정확히» — 자동취소 기한을 고객 편에서 알려주는 Agent.

#### 16. Grounding Status
```text
MEDIUM (절차 T2 · 화법 T3 · 부분이전 KG-002)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **31** |

---

### DC-025 — 수수료 단독 이탈 사유 · 퇴직금 5천만 이상 · 대면 개설 계좌 → 비대면 전환만으로 해소 가능성

#### 1. Case Concept
«증권사는 수수료가 없다더라» 며 이전을 검토하는 고객이 퇴직금 5천만 이상을 대면 개설 계좌에 두고 있을 때, Agent 가 «비대면 계좌 전환 시 퇴직금 수수료 면제(조건 결합 여부는 원천 불명확) · 연금수령 시 면제 · 장기할인은 이전 시 소멸» 을 결합해, 이전 없이 해소되는지 **조건 확인**부터 하는 정보 안내 Case.

#### 2. Why This Case Exists
```text
Reference:   [01:1135] 대면 개설 & 퇴직금 5천만↑ 비대면 전환 0원 · [05:2135] 면제 3층 중첩 · [03:196] 수수료 불만 3분기·장기할인 소멸 · C21
Knowledge:   OK-016(면제·할인 조건 — 5천만 면제의 «입금 기준 vs 비대면 전환 결합» 원천 상이, 수수료율 표 판독불확실 · [04-12-613] 예상조회) · HT-036(비대면 전환 절차·적용 시점 — T3) · TALK-015(수수료 무료 이탈 화법 — T3, 수수료율 STT 수치 인용 금지)
Source:      SRC-003 L349~353·L928 · SRC-011 L141 · SRC-074 · SRC-017
Golden/Case: golden §7 «수수료 단독 이탈 Case 없음 — GC-23 결과 후 재상정 없음» [Gap-7]. GC-16 은 ETF+수수료 복합. SCR-044·HT-036 미사용. HTML 이상철 Theme(«수수료 우대 0.25% vs 0.35%» — 수치 근거 없음)을 복제하지 않는다.
```

#### 3. Trigger
콜센터 «수수료 때문에 옮길까 한다» 문의 + 대면 개설 계좌 + 퇴직급여 5천만 이상 포함.

#### 4. Customer Context
```text
은퇴준비기 · 55세 · 안정추구형 · 퇴직급여 8,000만 포함 대면 개설 IRP · 원리금 중심 · 가입 4년(장기할인 구간)
```

#### 5. Interesting Evidence Combination
```text
«수수료» 단독 이전 사유 발화
+ 대면 개설 계좌 (비대면 전환 가능, 2025.10~)
+ 퇴직급여 5천만 이상 포함
+ 가입 4년 → 장기할인 적용 중(이전 시 소멸 — T3)
+ 개시 요건 충족 임박(연금수령 시 면제)
```

#### 6. Potential Segment
`은퇴준비기` × `이탈(수수료)` × `대면 계좌` × `퇴직금 보유` × `조건 확인`

#### 7. Potential Badges
```text
Primary:   수수료 사유 이전 검토
Secondary: 비대면 전환 가능 · 퇴직금 5천만↑
Signal:    콜센터 문의
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-016 (구조·면제·전환 경로·[04-12-613]) · OK-002 (경청 원칙) · OK-013 (개시 요건)
Product:            (없음)
Hot Tip:            HT-036 (전환 절차·적용 시점·«5천만 이상은 개시 전이라도 0원» — T3) · HT-012 (수수료 불만 대응)
Talk:               TALK-015 (T3 — 수익모델 설명, 수치 금지) · TALK-012 (사실 인정 후 설명 구조)
Screen:             SCR-044 [04-12-613] 수수료관리 예상조회 · 스타뱅킹 비대면계좌로 간편전환 경로(OK-016)
Knowledge Gap / Conflict: 5천만 면제 조건 결합 여부(OK-016 Limitation) · 수수료율 수치 판독불확실 — 인용 금지 · 장기할인 소멸은 [03:1662] 참고자료 수준
```

#### 9. Expected Agent Discovery
수수료가 사유라면 **이전이 아니라 계좌 전환**이 답일 수 있다는 것 — 단, 면제 조건이 원천 간 표현이 달라 «전환하면 0원» 을 단정하지 말고 [04-12-613] 예상조회로 확인한 뒤 말해야 한다는 것.

#### 10. Required Confirmation
```text
Employee Check: [04-12-613] 현재 수수료·전환 후 예상 · 5천만 면제 조건 공식 확인 · 장기할인 적용 여부
Customer Check: 이전 사유가 수수료뿐인지(이탈 5유형 [01:1023]) · 앱 사용 가능 여부(전환 경로)
```

#### 11. Potential Management Direction
```text
If 사유 = 수수료 + 조건 충족 확인:
→ 비대면 전환 안내(정보) + 예상조회 결과 공유 — 이전 여부는 고객 결정
If 다른 사유 동반:
→ 사유별 분리(ETF·서비스 등), 절차 지연 금지
```

#### 12. Forbidden Shortcut
```text
«전환하면 0원» 확정(조건 불명확) · 수수료율 «0.21~0.45%» 류 수치 인용 · 증권사 수수료 «무료 아님» 단정(타사 조건 확인) · 이탈 방지 사유(G4)
```

#### 13. Expected Brief Fit
- **S1**: 문의·계좌 유형·퇴직금·가입연수.
- **S2** — Main: 조건 확인 후 안내. Why now: 이전 검토 발화. Customer check: 사유·앱.
- **S3**: 정보 안내(전환 경로·면제 구조) — 조건부.
- **S4**: Opening «수수료 말씀이시면 옮기기 전에 확인할 게 하나 있어요 — 계좌를 비대면으로만 바꿔도 달라질 수 있어서요». 사전고지: 조건 확인 후.
- **S5**: [04-12-613] · 전환 경로 · HT-036(주의) · 후속: 예상조회 결과 통화.

#### 14. Potential Chat Questions
```text
비대면 계좌로 바꾸면 수수료 진짜 0원이야?
옮기면 지금 받는 할인은 어떻게 돼?
연금 받기 시작하면 수수료는?
```

#### 15. Demo Wow
«옮기지 않고 해결» — 고객 이익과 은행 이익이 겹치는 자리를 Agent 가 조건부로 짚는다.

#### 16. Grounding Status
```text
MEDIUM (OK-016 T2 이나 조건 결합 불명확·수치 판독불확실 · 절차 T3)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 3 |
| **총점** | **30** |

---

### DC-026 — 전출 접수 · 의사확인 알림톡·콜봇 무응답 · 자동취소 기한 → 고객 의사대로 진행되게 안내

#### 1. Case Concept
타행 이전을 신청한 고객이 당일 알림톡(18시 이후)과 익일 AI콜봇(10시·14시)에 응답하지 않아 **기한 내 의사 미확인 시 계좌이체가 자동 취소**될 상황에서, Agent 가 «이전이 고객의 진짜 의사라면 확인 절차를 마쳐야 한다» 는 사실을 고객 편에서 알리고, 방어가 아니라 **절차 안내**를 관리 포인트로 세우는 Case.

#### 2. Why This Case Exists
```text
Reference:   [03:1086] 클로징 후 알림톡→AI콜봇→자동취소 · [05:1401] «바쁘다» 고객이 응답 안 하면 자동취소로 잔류하지만 의사 확인 없음 · C23
Knowledge:   OK-031(1차 당일 18시 이후 알림톡 · 2차 익일 10·14시 AI콜봇 · 기한 내 미확인 시 자동 취소 · 직원 취소 3단계) · OK-002(고객 결정 수용 원칙 · 지연 금지 문구는 원천 없음) · HD-7/G4
Source:      SRC-003 L972~991
Golden/Case: GC-16·19·23 은 «접수 직후 대응». 의사확인 단계의 «무응답 → 자동취소» 는 없음. OK-031 미사용. HD-7(은행 목적 배제)의 극단 검증 — 자동취소를 «방어 성공» 으로 읽는 실패를 방지.
```

#### 3. Trigger
[06-AD-080] 전출 접수 D+1 + 알림톡 미응답 + AI콜봇 1차 미응답 로그.

#### 4. Customer Context
```text
재직기 · 40대 · 적극투자형 · ETF 중심 · 이전 사유 «실시간 매매»(CRM) · 통화 어려운 직장인
```

#### 5. Interesting Evidence Combination
```text
전출 접수 D+1(실물이전)
+ 알림톡 미응답 · 콜봇 10시 미응답
+ 의사확인 기한 임박(자동취소)
+ CRM «실시간 매매 때문에 옮긴다» 명시 의사
+ [06-AD-020] 실물이전 가능 상품 결과 조회됨
```

#### 6. Potential Segment
`재직기` × `이전(실물이전)` × `의사확인 진행 중` × `명시 의사 있음` × `절차 안내`

#### 7. Potential Badges
```text
Primary:   전출 의사확인 대기 (자동취소 기한)
Secondary: 실물이전 결과 조회 완료
Signal:    알림톡·콜봇 무응답
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-031 · OK-002 (사전체크·리스크 고지) · OK-003 (불가 상품 현금화) · OK-022
Product:            (없음)
Hot Tip:            HT-032 (전출 기관 의사확인 미응답만으로 거절 처리된 경험담 — [06-AD-080] 수시 조회, T3)
Talk:               TALK-011 (신청 → 확인 → 고객 최종 결정) · TALK-032 (Step — 실패 케이스 «감사 인사 + 의사확인 절차 안내»)
Screen:             SCR-003 [06-AD-080] · SCR-013 [06-AD-020] · SCR-087 [72-01-801]
Knowledge Gap / Conflict: 의사확인 시각·채널은 2026-03 운영 방식(변동 가능) · «절차 지연 금지» 명문 원천 없음(OK-002 Limitation)
```

#### 9. Expected Agent Discovery
무응답이 «마음이 바뀐 것» 이 아니라 **바쁜 것**일 수 있고, 그대로 두면 고객이 원한 이전이 자동취소된다는 것. Agent 의 역할은 리스크(불가 상품 현금화)를 한 번 더 알리되, 확인 절차를 마치도록 돕는 것이다.

#### 10. Required Confirmation
```text
Employee Check: [06-AD-080] 진행 단계·기한 · [06-AD-020] 불가 상품·현금화 손실
Customer Check: 이전 의사 유지 여부(재확인) · 불가 상품 현금화 수용 여부 · 확인 링크 응답 가능 시간
```

#### 11. Potential Management Direction
```text
If 의사 유지:
→ 확인 절차 완료 안내(링크/콜봇 시각) + 현금화 손실 고지 — 정보
If 의사 변경:
→ 취소 3단계(녹취·전출취소·CRM) 처리
```

#### 12. Forbidden Shortcut
```text
무응답을 «잔류» 로 기록 · 자동취소를 방어 성과로 프레이밍(G4) · 절차 지연·불응답 유도 · 손실 미고지 · 부분이전 가능/불가 단정(KG-002)
```

#### 13. Expected Brief Fit
- **S1**: 접수·무응답·명시 의사·결과 조회.
- **S2** — Main: 기한 내 의사확인 + 손실 고지. Why now: 자동취소 기한. Customer check: 의사·수용.
- **S3**: 절차 안내(정보) / 취소 절차 — 고객 결정.
- **S4**: Opening «이전 신청하신 건 확인했고, 오늘 안에 확인 응답이 없으면 자동으로 취소돼서 알려드려요». 사전고지: 불가 상품은 현금화.
- **S5**: [06-AD-080] · [06-AD-020] · [72-01-801] · HT-032(주의).

#### 14. Potential Chat Questions
```text
확인 문자에 답 안 하면 어떻게 돼?
실물이전 안 되는 상품은 어떻게 돼?
취소하고 싶으면 어떻게 해?
```

#### 15. Demo Wow
«떠나는 고객의 이익» 을 지키는 Agent — HD-7 을 가장 선명하게 보여주는 장면.

#### 16. Grounding Status
```text
STRONG (OK-031·002 T2)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 5 |
| Demo Wow | 5 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **35** |

---

### DC-027 — 타사 IRP 를 당행으로 «합치고 싶다» · 마이데이터 · 타사 DO 상품 선해지 · 실물이전 가능 상품 확인

#### 1. Case Concept
마이데이터로 타사 IRP 보유가 확인되고 고객이 «한 곳으로 합치고 싶다» 고 말할 때, Agent 가 «타사 DO 상품은 실물이전 비대상이라 선해지·현금화 필요 · [04-12-333] 당행 라인업 확인 · 신청 후 [06-AD-020] 결과를 보고 고객이 최종 결정 · 전입 후 현금 상태로 두면 재이탈 구간» 을 조건부 3단계로 세우는 Case.

#### 2. Why This Case Exists
```text
Reference:   [05:1350] 타행 DO 선해지 · [02:1042] [04-10-099] 3갈래 집약 · [03:1573] 현금화·재이전 손실 고지 · [01:700] 전입 후 재이탈 82.5% · C36
Knowledge:   OK-022(실물이전 요건·불가 상품 현금화·[04-12-333]) · OK-003(전액현금대체·중도해지 손실 확인) · TALK-011(3단계 확인 선행) · TALK-026(«신청만 먼저 해보시고 최종 결정») · HT-026(비대면 실물이전 — 타행 DO 해지, 확실성_주의) · HT-032(실물이전 유치 3단계·거절통보 대응) · HT-025(하나은행 비밀번호 사전등록) · HT-030(접수취소 4대 사유)
Source:      SRC-087 L85 · SRC-010 · SRC-061 · SRC-067 · SRC-060 · SRC-065 · SRC-071([04-0E-004])
Golden/Case: golden §7 «타행→당행 전입(유치)은 Scope 밖» — 재검토 여지(golden digest §8.2). 기존 Case 는 전부 «전출». Wider Context(마이데이터 [04-0E-004] SCR-084) 미사용.
```

#### 3. Trigger
[04-0E-004] MyData 대면상담에서 타사 IRP 확인 + 발화 «합치고 싶다».

#### 4. Customer Context
```text
재직기 · 45세 · 위험중립형 · 당행 IRP 소액 · 타사 IRP(DO 상품 + ETF + 정기예금) 보유
```

#### 5. Interesting Evidence Combination
```text
타사 IRP 보유(마이데이터)
+ 타사 계좌에 DO 상품(실물이전 비대상) + 정기예금(만기 8개월 잔여)
+ 발화 «합치고 싶다»(이유 미확인)
+ 당행 라인업에 타사 ETF 존재 여부 미확인([04-12-333])
+ 전입 후 현금 상태 방치 → 재이탈 구간(참고자료)
```

#### 6. Potential Segment
`재직기` × `외부 IRP` × `전입(집약)` × `실물이전 조건` × `확인 선행`

#### 7. Potential Badges
```text
Primary:   타사 IRP 통합 검토
Secondary: 실물이전 가능 여부 미확인 · 타사 DO 선해지 필요
Signal:    마이데이터 조회
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-022 · OK-003 · OK-020 (가입일 승계 — 0원 계좌) · OK-011 (타사 예금 중도해지 손실은 타사 기준)
Product:            (당행 라인업 확인 — [04-12-333])
Hot Tip:            HT-026 · HT-032 · HT-025 · HT-030 · HT-010 (마이데이터 발굴 — bank_objective)
Talk:               TALK-011 · TALK-026 (bank_objective 포함 — 확인 구조만)
Screen:             SCR-084 [04-0E-004] · SCR-079 [04-12-333] · SCR-013 [06-AD-020] · SCR-003 [06-AD-080] · SCR-015 [04-10-099]
Knowledge Gap / Conflict: KG-002 부분이전 · 재이탈 82.5% 는 references 수치(Grounding 아님) · 상대 기관별 예외(하나은행) T3
```

#### 9. Expected Agent Discovery
«합치기» 는 실물이전이 가능한 상품과 아닌 상품이 갈리고, 타사 DO 는 먼저 해지해야 하며, 정기예금은 중도해지 손실이 생긴다는 것. 그래서 **신청 → 결과 확인 → 고객 결정**의 순서를 지키고, 전입 뒤 현금 상태로 두지 않도록 운용지시까지 계획한다.

#### 10. Required Confirmation
```text
Employee Check: [04-12-333] 이관 가능 여부 · 타사 DO·예금 현금화 손실(타사 확인) · 상대 기관 전입 절차 예외
Customer Check: 합치려는 이유 · 예금 만기까지 기다릴지 · 현금화 손실 수용 · 전입 후 운용 계획
```

#### 11. Potential Management Direction
```text
If 손실 수용 + 즉시:
→ 타사 DO 해지 → 실물이전 신청 → 결과 확인 → 결정(TALK-011) → 전입 후 운용지시 예약
If 손실 큼:
→ 예금 만기 후 이전(후속예약) 또는 유지
```

#### 12. Forbidden Shortcut
```text
«전부 그대로 옮겨진다» · 현금화 손실 미고지 · 부분이전 가능 단정 · 유치 실적을 사유로(G4) · 전입 후 운용 계획 없이 종료(재이탈 구간)
```

#### 13. Expected Brief Fit
- **S1**: 타사 IRP 구성·발화·당행 소액.
- **S2** — Main: 실물이전 조건 3가지. Why now: 고객 요청. Customer check: 이유·손실 수용.
- **S3**: 조건부 절차(순번) / 만기 후 이전.
- **S4**: Opening «합치는 건 되는데, 옮겨지는 것과 안 옮겨지는 게 갈려서 신청 먼저 하고 결과 보고 결정하시면 돼요». 
- **S5**: [04-12-333] · [06-AD-020] · HT-026·032 · 후속: 결과 조회 후 통화.

#### 14. Potential Chat Questions
```text
다른 데 IRP 를 그대로 옮길 수 있어?
타사 DO 상품은 왜 먼저 해지해야 해?
옮기고 나면 바로 굴려야 해?
```

#### 15. Demo Wow
마이데이터(Wider Context)에서 시작해 실물이전 조건까지 이어지는 «전입» 시나리오 — 기존 Portfolio 에 없던 방향.

#### 16. Grounding Status
```text
MEDIUM (구조 OK-022·003 T2 · 실무 T3 다수 · Scope 재검토 필요)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 3 |
| **총점** | **31** |

---

### DC-028 — 투자성향 «하향» 재분석 · 기존 보유 2등급 ETF · 앱 조회 급증 → 보유는 위반 아님, 신규 매수만 제한

#### 1. Case Concept
재분석에서 위험중립형으로 낮아진 고객이 2등급 ETF 를 보유한 채 «팔아야 하냐» 며 수익률을 반복 조회할 때, Agent 가 «기존 보유의 등급 초과는 위반이 아니고 기준은 신규 매수·교체 권유에만 적용된다(OK-006)» 를 근거로 **유지 가능**을 말하고, 앞으로의 신규 매수 범위(4~6등급)만 안내하는 Case.

#### 2. Why This Case Exists
```text
Reference:   [03:2220] 성향분석일·WMTI 재진단 · [01:1549] 5단계 상한표 · [05:1252] 부적합 확인서 흐름
Knowledge:   OK-006(«이미 보유 중인 상품의 등급이 현재 성향의 허용 범위를 넘는 것 자체는 위반이 아니다. 기준은 신규 매수·교체 권유에 적용된다» — T1 Human-confirmed) · KG-006(재분석·변경 안내 원문 부재) · C2
Source:      SRC-096 · SRC-041 L81
Golden/Case: GC-09·20 은 성향 «상향». 하향 + 기존 보유 유지 판단은 없음 — golden digest §8.4 «성향 초과 보유 유지 판단 없음». HTML 윤소라·박은영 Theme 의 «불일치 → 재지정» 프레임을 반대로 검증.
```

#### 3. Trigger
투자성향 재분석 결과 하향(적극 → 위험중립) 등록 + 앱 수익률 조회 5회/주 + 콜센터 «팔아야 하나» 문의.

#### 4. Customer Context
```text
재직기 · 48세 · 위험중립형(1주 전 하향) · 미국 지수 ETF 2등급 40% + TDF + 예금 · DO 뿔려드림(C3 상 위험중립 이상 가능)
```

#### 5. Interesting Evidence Combination
```text
성향 하향(1주 전)
+ 기존 보유 2등급 ETF 40% (성향 범위 4~6 초과 — 보유 자체는 위반 아님)
+ 앱 수익률 조회 급증 + «팔아야 하나» 발화
+ DO 뿔려드림(위험중립 이상 가능 — C3 유지)
+ 최근 손실 없음(수익 +9%)
```

#### 6. Potential Segment
`재직기` × `실적배당 중심` × `성향 하향` × `보유 초과(관찰)` × `현 상태 유지`

#### 7. Potential Badges
```text
Primary:   투자성향 변경(하향)
Secondary: 보유 상품 등급 초과(관찰) — 관리 Badge 아님
Signal:    수익률 조회 급증
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-006 · OK-024 (5단계 정의 — 예시일 뿐) · OK-026 (DO C3)
Product:            (신규 매수 후보는 4~6등급 유형만 — 특정 상품 없음)
Hot Tip:            (없음)
Talk:               TALK-003 (변동성·타임 호라이즌) · TALK-018 (처분효과)
Screen:             SCR-004 [04-12-17A] (성향별 조회) · SCR-001
Knowledge Gap / Conflict: KG-006 재분석 후 안내 절차 원문 없음 · 부적합 확인 절차는 OK-006 범위 밖 · 하향 사유(고객 심경 변화?)는 확인 사항
```

#### 9. Expected Agent Discovery
«성향이 낮아졌으니 팔아야 한다» 는 규정에 없다는 것. 규정은 앞으로 무엇을 **새로** 살 수 있는지를 제한할 뿐이며, 지금 팔지는 고객의 손실 감내와 자금 계획의 문제다. 하향 재분석 자체가 «불안» 의 신호일 수 있어 그 이유를 묻는다.

#### 10. Required Confirmation
```text
Employee Check: 재분석 등록일·현재 성향 · 보유 상품 등급 · DO C3 적합
Customer Check: 재분석한 이유(불안·자금 계획 변화) · 보유 유지 의사 · 향후 매수 의향
```

#### 11. Potential Management Direction
```text
If 불안이 이유:
→ 유지 가능 사실 + 변동성 설명 재료(TALK-003) + 원하면 일부 축소(고객 결정)
If 자금 계획 변화:
→ 자금 시점에 맞춘 재구성 논의 — 신규는 4~6등급 범위
```

#### 12. Forbidden Shortcut
```text
«성향에 안 맞으니 매도» 단정 · 2등급 ETF 추가 매수 권유(C2 위반) · 성향 재상향 유도 · 조회 급증을 이탈 징후로 승격(SG-3)
```

#### 13. Expected Brief Fit
- **S1**: 하향·보유·조회·발화.
- **S2** — Main: 보유는 위반 아님 + 이유 확인. Why now: 하향 직후 문의. Customer check: 이유·의사.
- **S3**: 유지 가능 / 일부 축소 — 고객 결정.
- **S4**: Opening «성향 결과가 바뀌었다고 지금 가진 걸 꼭 팔아야 하는 건 아니에요 — 새로 살 때 기준이 달라지는 거예요». 
- **S5**: OK-006 · [04-12-17A] · 후속: 없음.

#### 14. Potential Chat Questions
```text
성향이 낮아졌는데 가진 ETF 팔아야 해?
앞으로 뭘 살 수 있어?
DO 는 그대로 둬도 돼?
```

#### 15. Demo Wow
«규정을 고객 편에서 읽는» 두 번째 장면 — 불일치 Badge 의 과잉 반응을 막는다.

#### 16. Grounding Status
```text
STRONG (OK-006 T1) — 재분석 후속 안내는 KG-006
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 3 |
| 직원 실용성 | 4 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **32** |

---

### DC-029 — 지난 상담 «만기 때 연락 달라» 약속 · 만기 D-14 · 담당 직원 변경(미승계)

#### 1. Case Concept
6개월 전 상담에서 «만기 때 다시 연락 달라, 그때 일부 실적배당 생각해 보겠다» 고 한 고객의 만기가 2주 남았는데 담당 직원이 전보돼 승계가 안 된 상태를 Agent 가 결합해, **약속 이행**을 관리 포인트로 세우고 새 담당자에게 지난 대화(상담 기억)를 넘겨주는 Case.

#### 2. Why This Case Exists
```text
Reference:   [01:1493] 현장 4유형 — 담당자 교체 후 방치·만기 무안내 · [02:1837] 권유직원 퇴직·전보 후 미승계 계좌 · [03:2140] 작년 교체매매 이력 고객 재접촉 · 더미 이준호 «만기 시 일부 실적배당 전환 관심»
Knowledge:   OK-004(만기 1개월 전 안내 원칙·예약변경) · OK-006(전환 시 성향 범위) · HT-003(재접점 화법) · TALK-030 유형2(펀드 경험 有 분산투자)
Source:      SRC-003 L790 · SRC-002 · SRC-068
Golden/Case: GC-20 은 «오래된 CRM vs 최근 신호» 충돌. 본 후보는 CRM 이 **약속**이라 충돌이 아니라 이행 — 다회차 서사·담당 변경(golden digest §8.3 «다회차 상담·직원 변경 서사 없음»). Seed 박정호 챗 q1(상담 기억)의 브리핑 버전. SCR-067·068 미사용.
```

#### 3. Trigger
정기예금 만기 D-14 + CRM(6개월 전) «만기 때 연락, 일부 실적배당 검토» + 권유직원 전보(미승계).

#### 4. Customer Context
```text
재직기 · 45세 · 위험중립형 · 정기예금 70% + TDF 30% · 과거 펀드 경험 있음
```

#### 5. Interesting Evidence Combination
```text
만기 D-14
+ CRM 약속 «만기 때 연락 — 일부 실적배당 검토»
+ 담당 직원 전보 · 승계 미처리([06-12-625] 권유직원 공란)
+ 예약변경 미등록
+ 펀드 경험 有(TALK-030 유형2)
```

#### 6. Potential Segment
`재직기` × `재운용 시점` × `약속 이행` × `담당 미승계` × `일부 전환 검토`

#### 7. Potential Badges
```text
Primary:   정기예금 만기 D-14
Secondary: 상담 약속 이행 필요 · 담당 미승계
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-004 · OK-006 · OK-029 (유선 특정 펀드 금지 — 상품군까지)
Product:            (위험중립 4~6등급 유형 — 특정 상품 없음)
Hot Tip:            HT-003 (재접점 멘트 — 동일 상담 내 재도전 원천; 시차 재접근은 KG-003 참고)
Talk:               TALK-030 유형2 · TALK-010 (일부만)
Screen:             SCR-068 [06-12-625] 권유직원 변경 · SCR-067 [06-12-624] 관리점 변경 · SCR-017 [06-12-611] · SCR-009
Knowledge Gap / Conflict: KG-003 시차 재접근 화법 원문 부재 · CRM «약속» 의 현재 유효성 재확인(GC-20 취지)
```

#### 9. Expected Agent Discovery
만기 자체보다 **고객이 기다리는 연락**이 관리 포인트라는 것. 담당이 바뀌어 아무도 그 약속을 모르는 상태를 Agent 가 메운다. 다만 6개월 전 «검토» 는 의사가 아니라 재확인 대상이다.

#### 10. Required Confirmation
```text
Employee Check: 승계 처리([06-12-625]) · 예약변경 상태
Customer Check: 지금도 일부 실적배당 검토 의향인지 · 만기 자금 사용계획
```

#### 11. Potential Management Direction
```text
If 의향 유지:
→ 성향 범위 내 유형 수준 논의(비대면은 상품군까지) + 예약변경
If 변경:
→ 원리금보장 내 예약변경으로 종료
```

#### 12. Forbidden Shortcut
```text
6개월 전 «검토» 를 현재 의사로 승격(SG-1) · 유선 특정 펀드 권유(OK-029) · 약속 미이행 상태로 만기 경과
```

#### 13. Expected Brief Fit
- **S1**: 만기·약속·담당 변경.
- **S2** — Main: 약속 이행 + 의향 재확인. Why now: D-14 + 1개월 전 안내 원칙. Customer check: 의향·사용계획.
- **S3**: 예약변경 + (의향 시) 일부 실적배당 유형 — 조건부.
- **S4**: Opening «3월에 만기 때 연락 달라고 하셨던 거 기억하고 연락드렸어요 — 담당이 저로 바뀌었고요». 
- **S5**: [06-12-625] · [06-12-611] · TALK-030 · 후속: 결정 후 앱 안내.

#### 14. Potential Chat Questions
```text
지난번에 이 고객이 뭐라고 했지?
담당이 바뀌면 고객한테 어떻게 말해?
비대면으로 펀드 얘기 어디까지 해도 돼?
```

#### 15. Demo Wow
«Agent 가 약속을 기억한다» — 담당이 바뀌어도 관계가 이어지는 장면.

#### 16. Grounding Status
```text
MEDIUM (제도 T2 · 약속·승계 서사는 CRM 구조에 의존, 재접근 화법은 KG-003)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 3 |
| 직원 실용성 | 4 |
| Agent 판단성 | 3 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **30** |

---

### DC-030 — 20대 비대면 신규 · 첫 입금 D+3 · DO 2주 창 · 입금예정상품 미등록 · 청년 수수료 할인

#### 1. Case Concept
비대면으로 IRP 를 만들고 첫 부담금을 넣은 20대 고객(권유직원 공란)에게, Agent 가 «입금 후 2주 무지시면 DO 로 자동 운용(등록했다면) / 미등록이면 현금 대기 · 입금예정상품을 등록하면 다음 입금부터 자동 매수 · 만 39세 미만 운용관리수수료 20% 할인» 을 시한과 함께 정보 안내하는 Lifecycle 초기 Case.

#### 2. Why This Case Exists
```text
Reference:   [01:926] 비대면 신규 후 1개월 내 운용 중단 · [01:444] 권유직원 코드 없음 · [03:532] «55세까지 멀었다» 젊은 고객 · C35 · 더미 김현수(29세, 고유대 75%)
Knowledge:   OK-005(최초 입금 2주·입금예정상품과의 구분) · OK-026(DO 지정 의무) · OK-016(청년 39세 미만 20% 할인 — 1년 내 해지 시 미적용) · HT-009(스타뱅킹 이용 Q&A) · HT-014(신입행원 가이드 — 3층 연금)
Source:      SRC-089 · SRC-098 L143~150 · SRC-003 L349~353 · SRC-041 · SRC-047
Golden/Case: CASE_001 은 29세이나 «10개월 경과형». «첫 입금 2주 창 + 비대면 + 청년 할인» 은 없음 — golden digest §8.2. SCR-047 미사용.
```

#### 3. Trigger
비대면 신규 D+10 · 첫 입금 D+3 · 운용지시 없음 · 권유직원 공란.

#### 4. Customer Context
```text
재직 초기 · 27세 · 적극투자형 · 첫 입금 100만 · DO 미등록 · 앱 능숙
```

#### 5. Interesting Evidence Combination
```text
첫 입금 D+3(2주 창 D-11)
+ DO 미등록(→ 2주 후에도 현금 대기)
+ 입금예정상품 미등록(자동이체 예정)
+ 권유직원 공란(관리 주체 없음)
+ 만 39세 미만(수수료 할인 조건)
```

#### 6. Potential Segment
`재직 초기` × `비대면 신규` × `현금성 100%(초기)` × `DO 미등록` × `청년`

#### 7. Potential Badges
```text
Primary:   첫 입금 D+3 · DO 미등록
Secondary: 입금예정상품 미등록 · 담당 미지정
Signal:    앱 신규
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-005 · OK-026 · OK-016 · OK-006 (적극투자형 3~6등급)
Product:            PRD-021 DO (C3: 적극투자형 → 알파·뿔려드림 가능, 모두드림 불가) · PRD-033 적극투자형 월간 포트폴리오(원문 표기 불일치 — 인용 금지)
Hot Tip:            HT-009 · HT-014 · HT-035 (앱 운용지시)
Talk:               TALK-023 (직장인 신규) · TALK-021 (투자 4단계)
Screen:             SCR-047 [06-12-610] 입금예정상품 · SCR-068 [06-12-625] 권유직원 · SCR-011 스타뱅킹 운용상품 찾기 · SCR-091 [75-08-850]
Knowledge Gap / Conflict: 청년 할인의 세부 조건은 수수료 표 판독불확실(OK-016) · 2주 기산 원문 없음
```

#### 9. Expected Agent Discovery
«소액이라 신경 안 써도 되는 계좌» 가 실은 **2주 안에 첫 운용 방식이 정해지는** 계좌라는 것, 그리고 청년 할인·입금예정상품처럼 지금 한 번 설정하면 계속 가는 것들이 있다는 것.

#### 10. Required Confirmation
```text
Employee Check: DO 등록 여부·입금예정상품·권유직원 지정
Customer Check: 매월 납입 계획 · 자동운용(DO) vs 직접 · 손실 감내(적극투자형)
```

#### 11. Potential Management Direction
```text
정보 안내(앱 메시지/LMS): DO 등록 · 입금예정상품 · 청년 할인 — 통화보다 [75-08-850] 모바일브랜치 LMS 가 적합
```

#### 12. Forbidden Shortcut
```text
현금 100% → «방치» 라벨 · 특정 펀드 확정 · 모두드림 권유(C3) · 할인율 확정 수치
```

#### 13. Expected Brief Fit
- **S1**: 신규·입금·미등록 3종·연령.
- **S2** — Main: 2주 창 안에 설정 3가지. Why now: 2주 규칙. Customer check: 납입 계획·방식.
- **S3**: 정보 안내(설정) — 상품 없음.
- **S4**: 메시지 초안 «첫 입금 감사해요 — 2주 안에 자동운용 설정 하나만 해두면 편해요».
- **S5**: [06-12-610] · [75-08-850] · HT-009.

#### 14. Potential Chat Questions
```text
2주 안에 안 하면 어떻게 돼?
입금예정상품이 뭐야?
39세 미만이면 수수료가 싸?
```

#### 15. Demo Wow
가장 작은 계좌에서 «시한» 을 보여주는 장면 — 발표에서 «이런 고객까지?» 를 만든다.

#### 16. Grounding Status
```text
STRONG (OK-005·016·026) — 할인 세부는 판독불확실
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 3 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **29** |

---

### DC-031 — «지난달 4.6% 예금 있다던데» · 월말 만기 · 월 단위 라인업·금리 변동 → 시점 판단

#### 1. Case Concept
8/31 만기 고객이 지난달 특별제공 저축은행 4.6% 를 기억하고 «그걸로 해달라» 고 할 때, Agent 가 «원리금보장 금리는 월 단위로 바뀌고 [04-12-17A] 에는 지금 가입 가능한 상품만 보인다» 는 사실로 **as-of** 를 바로잡고, 월말 만기라면 «며칠 뒤 다음 달 라인업» 을 기다리는 선택지도 있음을 정보 안내하는 Freshness Case.

#### 2. Why This Case Exists
```text
Reference:   [02:1434] 월 단위 금리·7/31 확정 · [03:2140] 특별제공 재예치 · N08 «며칠 대기가 이득» · C01
Knowledge:   OK-017(원리금보장 라인업·금리 월 단위 변동 · [04-12-17A] 가입 가능 상품만) · OK-010(금리 as-of 없이 인용 금지) · PRD-018(as_of 2026-07·08) · PRD-019/KG-007(저축은행 개별 상품 부재) · HT-048(예금금리 월단위 확정)
Source:      SRC-097 · SRC-001 L233~239 · SRC-086
Golden/Case: P3-7 «Freshness 미달 수치» 미검증(design KNOWLEDGE_ARCHITECTURE_STUDY §⑦). GC-01·08 특별제공 금리는 as-of 명시형. HTML 김형준·최지현 Theme(«금통위 전 예치») 의 시황 요소를 빼고 «월 단위 금리 확정» 사실만으로 재구성.
```

#### 3. Trigger
정기예금 만기 8/31(D-4) + 발화 «지난달 4.6% 상품».

#### 4. Customer Context
```text
은퇴준비기 · 56세 · 안정추구형 · 정기예금 100% · DO 지켜드림
```

#### 5. Interesting Evidence Combination
```text
만기 8/31(월말)
+ 발화 «지난달 특별제공 4.6%»
+ 이달 [04-12-17A] 라인업에 해당 상품 미조회(한도 소진 또는 종료)
+ 다음 달 라인업 확정 시점(월말)
+ 예약변경은 만기 1개월 전부터(이미 창구 안)
```

#### 6. Potential Segment
`은퇴준비기` × `원리금 100%` × `재운용 시점(월말)` × `시점 의존 수치` × `정보안내`

#### 7. Potential Badges
```text
Primary:   정기예금 만기 D-4
Secondary: 금리 as-of 확인 필요
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-017 · OK-010 · OK-004 (예약변경·현금성 상환)
Product:            PRD-018 · PRD-019 (개별 상품 없음)
Hot Tip:            HT-048 · HT-044
Talk:               TALK-009 (금리 변동성 대응 행)
Screen:             SCR-004 [04-12-17A] · SCR-018 [04-12-179] · SCR-017 [06-12-611]
Knowledge Gap / Conflict: KG-007 · 「월말 금리 확정 시점」 은 참고자료(references) 서술 — 공식 확인 · 시황·금리 전망 발언 금지(F59 참고)
```

#### 9. Expected Agent Discovery
고객이 말하는 금리는 **지난달 값**이고 지금은 없을 수 있다는 것. 월말 만기라면 «지금 예약변경» 과 «다음 달 라인업 확인 후 지시(그 사이 며칠은 현금성)» 두 시점 선택지가 있고, 어느 쪽이 나은지는 금리 전망이 아니라 고객의 편의·현금 대기 수용으로 정한다.

#### 10. Required Confirmation
```text
Employee Check: 이달 라인업·금리·한도([04-12-17A]·[04-12-179]) · 다음 달 라인업 게시 시점
Customer Check: 며칠 현금 대기 수용 여부 · 기간 선호
```

#### 11. Potential Management Direction
```text
If 대기 수용:
→ 만기 후 다음 달 라인업 확인 후 운용지시(DO 등록 계좌라 6주 규칙 안전망 — 확인)
If 즉시:
→ 이달 가능 상품으로 예약변경 — as-of 명시
```

#### 12. Forbidden Shortcut
```text
지난달 금리 인용 · «다음 달 금리 오른다/내린다» 전망(F59) · 특정 저축은행 상품명 생성(KG-007) · «금통위 전에» 류 시황 명분
```

#### 13. Expected Brief Fit
- **S1**: 만기·발화·라인업 미조회.
- **S2** — Main: as-of 정정 + 시점 선택. Why now: D-4. Customer check: 대기 수용.
- **S3**: 두 시점 선택지(정보).
- **S4**: Opening «지난달 그 상품은 이달엔 안 보여서요 — 대신 방법이 두 가지예요». 사전고지: 금리는 이달 기준.
- **S5**: [04-12-17A] · [04-12-179] · [06-12-611].

#### 14. Potential Chat Questions
```text
지난달 4.6% 상품 아직 있어?
만기 지나고 며칠 두면 손해야?
다음 달 금리는 언제 나와?
```

#### 15. Demo Wow
«숫자에 날짜를 붙이는» Agent — 시점 의존 지식을 다루는 방식을 보여준다.

#### 16. Grounding Status
```text
MEDIUM (OK-017 T2 · 월말 확정 시점은 참고자료 · KG-007)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 3 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 3 |
| **총점** | **28** |

---

### DC-032 — 전화 채널 · «그 펀드로 바꿔주세요» 요청 · 금소법 경계 · 컨설팅센터는 예금→예금만

#### 1. Case Concept
내점이 어려운 고객이 전화로 특정 펀드 교체를 요청할 때, Agent 가 «비대면 펀드 권유는 금소법 위반 소지(OK-029) · 퇴직연금 자산관리 컨설팅센터 단말은 정기예금→정기예금만(OK-030) · 펀드·ETF 는 앱 본인 실행 또는 내점» 을 결합해 **채널 제약을 상황으로** 세우고 실행 경로를 안내하는 Case.

#### 2. Why This Case Exists
```text
Reference:   [02:464] 컨설팅센터 예금→예금만 · [02:1463] 3경로 제약표 · C39 고령·앱 미사용 · [05:2274] [04-12-660] 원리금보장만 등록
Knowledge:   OK-029(비대면 펀드 권유 금소법 경계) · OK-030(컨설팅센터 범위·[04-12-660]·1833-3700 / 골든라이프센터) · HT-033(운용변경 채널 3종 — 1599-0099 전화센터는 정기예금·고유대 한정) · HT-035(앱 운용지시 지원)
Source:      SRC-002 L293·L297~318 · SRC-069 · SRC-073
Golden/Case: GC-08 이 컨설팅센터(예금→예금)를 언급. «채널 기인 실행 불가» 중심 Case 는 없음 — golden digest §8.4 [Gap-5]. OK-029·030·SCR-076 미사용.
```

#### 3. Trigger
콜센터/전화 «TDF 를 ○○펀드로 바꿔달라» 요청 + 고객 내점 불가(원거리) + 앱 미사용.

#### 4. Customer Context
```text
은퇴준비기 · 62세 · 위험중립형 · TDF + 정기예금 · 앱 미사용 · 내점 어려움
```

#### 5. Interesting Evidence Combination
```text
전화 요청(특정 펀드 교체)
+ 앱 미사용 · 내점 불가
+ 컨설팅센터 단말 범위 = 예금→예금만
+ 비대면 펀드 권유 경계(OK-029)
+ 요청 상품 등급이 성향 범위 내인지 미확인
```

#### 6. Potential Segment
`은퇴준비기` × `실적배당 보유` × `채널 제약` × `실행 불가(현 채널)` × `앱 미사용`

#### 7. Potential Badges
```text
Primary:   채널 제약 — 전화 펀드 변경 불가
Secondary: 앱 미사용 · 내점 불가
Signal:    전화 요청
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-029 · OK-030 · OK-006 (등급 확인) · OK-017 (판매 가능 여부)
Product:            (요청 상품 — 확정 아님)
Hot Tip:            HT-033 · HT-035 · HT-009
Talk:               (없음 — 채널 안내)
Screen:             SCR-076 [04-12-660] 상담연계등록 · SCR-010 스타뱅킹 보유상품변경 · SCR-004
Knowledge Gap / Conflict: 컨설팅센터 범위는 SRC-002 시점 기준(변동 가능) · 모바일브랜치 처리 범위 문서 모순([05:1233] 참고) · 가족 대리 요청은 본인 확인 원칙([05:1310] 참고)
```

#### 9. Expected Agent Discovery
«할 수 있냐» 의 답이 상품이 아니라 **채널**에 달려 있다는 것. 전화로는 예금 간 변경까지만이고, 펀드 교체는 앱 본인 실행 또는 내점(가족 동반 가능 여부 확인)으로 경로를 바꿔야 한다. 그 전에 요청 펀드가 성향 범위·판매 가능인지 확인한다.

#### 10. Required Confirmation
```text
Employee Check: 요청 펀드 등급·판매 여부([04-12-17A]) · 컨설팅센터 현재 업무 범위
Customer Check: 앱 설치·이용 가능성 · 내점 가능 일정(동반자) · 교체 이유
```

#### 11. Potential Management Direction
```text
If 앱 가능:
→ 앱 운용지시 안내(HT-035) — 상품 확정은 고객
If 앱 불가·내점 불가:
→ 내점 예약 또는 예금→예금 범위만 전화 처리 — 실행 제약 안내
```

#### 12. Forbidden Shortcut
```text
전화로 특정 펀드 권유·확정(OK-029) · 컨설팅센터에서 펀드 변경 접수 · 가족 대리 처리 · 등급 미확인 교체
```

#### 13. Expected Brief Fit
- **S1**: 요청·채널·내점 불가.
- **S2** — Main: 채널별 가능 범위. Why now: 요청 직후. Customer check: 앱·내점.
- **S3**: 경로 안내(실행 제약).
- **S4**: Opening «전화로는 예금 바꾸는 것까지만 되고, 펀드는 고객님이 앱에서 직접 하시거나 오셔야 해요 — 방법 같이 볼게요». 
- **S5**: [04-12-660] · 앱 보유상품변경 · HT-033.

#### 14. Potential Chat Questions
```text
전화로 펀드 바꿀 수 있어?
컨설팅센터는 뭘 해줘?
앱이 없으면 어떻게 해?
```

#### 15. Demo Wow
«채널이 곧 상황» 이라는 새로운 축 — 실행 가능성을 판단에 넣는 Agent.

#### 16. Grounding Status
```text
STRONG (OK-029·030 T2)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 4 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **32** |

---

### DC-033 — «ETF 샀는데 체결이 안 돼요» · 15:15 이후 주문 · 만기자금 아직 현금성 미착

#### 1. Case Concept
정기예금 만기일 오후 늦게 앱에서 ETF 를 주문한 고객이 «체결이 안 된다» 며 문의할 때, Agent 가 «은행 ETF 는 실시간이 아니라 09:05~15:15 사이 3분마다 분할 체결·금액주문 · 15:15 이후 주문은 익영업일 · 만기자금이 현금성으로 상환된 뒤에야 주문 가능» 을 결합해 오류가 아님을 정보 안내하는 Digital Execution Case.

#### 2. Why This Case Exists
```text
Reference:   [05:1030] ETF 2단계(현금성 확보 → 주문)·15:15 · [02:1308] 15:15 이전 당일 기준가 · [03:343] 3분 체결 · [03:1817] 팻핑거
Knowledge:   OK-023(실시간 불가·09:05~15:15·3분마다 30분할·금액주문·5분 이내 체결·24시간 신청) · OK-004(만기 시 현금성 상환) · HT-043(체결 소요 — 15:15 전 당일 체결·결제 +2영업일 / 이후 익영업일, TDF T+3 — T3) · HT-035(ETF 는 현금성 전환 후 매수)
Source:      SRC-004 L81~91 · SRC-003 L943 · SRC-081 · SRC-073
Golden/Case: GC-16 Critical 에 «실시간 가능 허위» 만 등장. «앱 실행 실패 신호» 는 golden digest §8.3 공백. OK-023·SCR-010 미사용.
```

#### 3. Trigger
콜센터 «ETF 주문했는데 안 사져요» + 앱 주문 로그 16:40 + 정기예금 당일 만기.

#### 4. Customer Context
```text
재직기 · 39세 · 적극투자형 · ETF·TDF 중심 · 앱 능숙
```

#### 5. Interesting Evidence Combination
```text
ETF 주문 16:40(15:15 이후)
+ 정기예금 당일 만기 → 현금성 상환 처리 시점
+ 주문 금액 > 당시 현금성 잔액
+ 3분 분할·금액주문 구조(실시간 아님)
+ 위험자산 한도 여유 있음(별개 확인)
```

#### 6. Potential Segment
`재직기` × `실적배당 중심` × `ETF 관심` × `앱 실행 실패` × `정보안내`

#### 7. Potential Badges
```text
Primary:   ETF 주문 미체결 문의
Secondary: 만기 당일 · 15:15 이후 주문
Signal:    앱 주문 로그
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-023 · OK-004 · OK-012 (한도 별개 확인)
Product:            (해당 ETF — 확정 아님)
Hot Tip:            HT-043 (체결 시각·결제 — T3, bank_objective 포함) · HT-035
Talk:               TALK-013 (실시간 매매 차이 인정 화법) · TALK-016
Screen:             SCR-010 스타뱅킹 보유상품변경(ETF 매매) · SCR-001 · SCR-002 [04-12-640] 운용내역
Knowledge Gap / Conflict: 당일매매·일회성 운용지시 프로세스 도식 판독불확실(OK-023) · 결제 +2영업일 등 세부는 T3
```

#### 9. Expected Agent Discovery
«안 사졌다» 는 오류가 아니라 **시각과 잔액**의 문제라는 것 — 주문 시각(15:15 이후)과 만기자금 상환 시점 두 가지가 겹쳤다. 익영업일 체결 안내와 «실시간 아님» 을 사실대로 말한다.

#### 10. Required Confirmation
```text
Employee Check: [04-12-640] 주문 상태 · 현금성 잔액 반영 시점 · 한도 여유
Customer Check: 주문 유지 여부 · 금액 조정 필요 여부
```

#### 11. Potential Management Direction
```text
정보 안내: 익영업일 체결 · 3분 분할 구조 · 필요 시 주문 정정 — 실행은 고객 본인 앱
```

#### 12. Forbidden Shortcut
```text
«실시간 체결 된다» · 직원 대행 매수 · 체결 가격 전망 · 결제일 확정 수치(T3)
```

#### 13. Expected Brief Fit
- **S1**: 주문 시각·만기·잔액.
- **S2** — Main: 미체결 원인 2가지. Why now: 문의 직후. Customer check: 유지 여부.
- **S3**: 정보 안내.
- **S4**: Opening «오류가 아니라 시간 때문이에요 — 은행 ETF 는 3시 15분 전까지 넣은 주문만 당일 처리돼요». 
- **S5**: 앱 보유상품변경 · [04-12-640] · HT-035.

#### 14. Potential Chat Questions
```text
왜 바로 안 사져?
몇 시까지 주문해야 오늘 돼?
만기된 돈은 언제부터 쓸 수 있어?
```

#### 15. Demo Wow
콜센터 문의를 Agent 가 «제도 + 시각» 으로 즉답하는 장면 — 챗 답변(제도 안내)에 어울린다.

#### 16. Grounding Status
```text
STRONG (OK-023 T2) — 결제 세부는 T3
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 3 |
| Demo Wow | 3 |
| 기존 Case 대비 차별성 | 5 |
| Brief Fit | 4 |
| **총점** | **30** |

---

### DC-034 — 현금성 7,500만 이상 · 사용계획 «6개월 뒤 자녀 결혼» 확정 · 단기 운용 조건부

#### 1. Case Concept
TM 스크립트 §25 기준(현금성 7,500만 이상)에 걸린 고객이 «6개월 뒤 자녀 결혼에 쓴다» 고 이미 밝힌 상황에서, Agent 가 «사용계획 있는 현금성은 권유 제외(OK-028)» 를 우선하되, 6개월이라는 확정 시점이 있으면 «만기 6개월 이내 원리금보장 상품(있다면)·현금 유지» 두 선택지를 조건부로 제시하고 인출 절차(중도인출 사유 해당 여부)를 먼저 확인하는 Case.

#### 2. Why This Case Exists
```text
Reference:   [01:229] 현금성 임계값 7,500만/100만/50% 상충 · [01:935] 사용예정액 컬럼 · [01:819] 사용계획 판정식 · C03 · N01
Knowledge:   OK-028(사용계획 있는 자금 권유 제외 · 판별 요건) · OK-015(자녀 결혼은 법정 사유 아님 → 인출 경로 = 해지/개시 후 인출) · OK-013(개시 요건) · OK-010(원리금보장 기간 — 단기 상품 실재 여부는 [04-12-17A]) · TALK-028 §25 · TALK-030 현금성(사용계획 확인 선행)
Source:      SRC-007 §25 · SRC-002 L50·L172~211 · SRC-003
Golden/Case: CASE_001·GC-03·12·18·22 는 사용계획 «미확인». 사용계획이 **확정된** 현금성 + 인출 경로 문제 조합은 없음. 임계값 상충([01:229])은 «직원확인우선» 재료.
```

#### 3. Trigger
현금성 8,000만(비중 60%) + TM §25 리스트 + CRM «내년 3월 자녀 결혼 자금».

#### 4. Customer Context
```text
은퇴준비기 · 59세 · 안정추구형 · 정기예금 40% + 현금성 60%(6월 만기 상환분) · 개시 요건 충족(미개시)
```

#### 5. Interesting Evidence Combination
```text
현금성 8,000만 · 2개월 무변동
+ CRM «6개월 뒤 결혼 자금» (사용계획 확정)
+ 개시 요건 충족(→ 개시 후 한도 내 인출 경로 존재)
+ 법정 중도인출 사유 아님
+ TM §25 임계값 7,500만 — 다른 문서는 100만/50% (상충)
```

#### 6. Potential Segment
`은퇴준비기` × `현금성 비중 높음` × `사용계획 확정` × `인출 경로 확인` × `조건부 단기 운용`

#### 7. Potential Badges
```text
Primary:   사용계획 있는 현금성 (권유 제외)
Secondary: 인출 경로 확인 필요 · 연금개시 가능
Signal:    (없음)
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-028 · OK-015 · OK-013 · OK-009 (인출 과세 구조) · OK-010
Product:            (6개월 이내 만기 원리금보장 상품 — 실재 여부 [04-12-17A] 확인, 생성 금지)
Hot Tip:            HT-005 (연금수령한도 내 일시금·자유인출) · HT-006 (PROVISIONAL)
Talk:               TALK-028 §25 (개인정보 언급 금지 유의) · TALK-030 · TALK-007
Screen:             SCR-001 · SCR-008 [04-12-644] · SCR-007 [02-12-221] · SCR-004
Knowledge Gap / Conflict: 현금성 임계값 상충([01:229] — Registry 에 SC 미등록) · 단기 상품 라인업 미확인
```

#### 9. Expected Agent Discovery
이 현금은 «운용 대상» 이 아니라 **인출 예정 자금**이라는 것, 그리고 정작 문제는 «어떻게 뺄 것인가» (결혼은 법정 사유가 아니므로 해지 vs 개시 후 한도 내 인출)라는 것. 운용 제안은 6개월 이내 만기·손실 없는 상품이 실재할 때만 조건부다.

#### 10. Required Confirmation
```text
Employee Check: [04-12-644] 입금사유 · 6개월 이내 만기 원리금보장 상품 실재 · [02-12-221] 한도
Customer Check: 사용 시점·금액 확정 여부 · 인출 방식 선호(해지/개시) · 나머지 자금 계획
```

#### 11. Potential Management Direction
```text
If 6개월 확정 + 개시 수용:
→ 개시 후 한도 내 인출 구조 안내(계산은 화면) + 잔여 자금 운용은 별도
If 해지 선호:
→ 과세 구조 고지 — 결정 지원
운용: 단기 상품 실재 시에만 조건부, 아니면 현금 유지가 합리
```

#### 12. Forbidden Shortcut
```text
7,500만 넘었다고 리밸런싱 권유(SG-2·OK-028 위반) · «결혼 자금 중도인출 가능» · 세액 계산값 · 임계값 하나를 행내 기준으로 단정
```

#### 13. Expected Brief Fit
- **S1**: 현금성·사용계획·개시 요건.
- **S2** — Main: 인출 경로 확인이 먼저. Why now: 6개월 시한. Customer check: 시점·방식.
- **S3**: 유지 / 조건부 단기 + 인출 구조 정보.
- **S4**: Opening «결혼 자금으로 쓰신다고 하셔서, 운용보다 빼는 방법을 먼저 정리해 드리려고요». 
- **S5**: [02-12-221] · [04-12-644] · HT-005.

#### 14. Potential Chat Questions
```text
결혼 자금으로 IRP 돈 뺄 수 있어?
6개월만 굴릴 상품 있어?
현금으로 두면 이자는?
```

#### 15. Demo Wow
«현금성 편중» Badge 를 «인출 설계» 로 바꾸는 Agent — Seed 이수민의 반대 결말.

#### 16. Grounding Status
```text
STRONG (OK-028·015·013 T2) — 단기 상품 실재는 확인
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 4 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 4 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **33** |

---

### DC-035 — 손실 구간 · «전부 예금으로 바꿔달라» · 위험중립형 · 변경도 유지도 정답

#### 1. Case Concept
실적배당 손실 중인 위험중립형 고객이 «다 팔고 예금으로» 요청할 때, Agent 가 «성향은 상한이라 예금 100% 도 허용(OK-006) · 전량 매도는 실행 가능 · 다만 처분효과·타임 호라이즌 설명 재료와 «일부만·되돌릴 수 있음» 완충 화법이 있다» 를 결합해, **결정권을 고객에게 두고** 시황 전망 없이 정보를 주는 결정 지원 Case.

#### 2. Why This Case Exists
```text
Reference:   [03:871] 감정 인정→사과→원인→리밸런싱, 즉시 매도 권유 금지 · [03:3049] 처분효과 · [02:508] 일부·가역 · C30 · [HTML-Theme] 박은영·강도윤(«다 팔고 예금으로»)
Knowledge:   OK-006(예금 100% 허용) · TALK-002 유형2 · TALK-003(타임 호라이즌) · TALK-005(하락장 자세) · TALK-018(처분효과) · TALK-010(일부만 변경·번복 가능) · HT-003(과거 손실 고객 재도전 화법) · OK-029(유선 특정 펀드 금지)
Source:      SRC-016 · SRC-018 · SRC-019 · SRC-021 · SRC-007 · SRC-068
Golden/Case: GC-06(판매중단·비교 요청)·GC-21(수익률 지표 Gap) 과 다른 축 — 고객이 **전량 매도를 요청**하는 상황에서 «변경도 유지도 정답(HD-6)» 을 검증. HTML 박은영 Case 의 하우스뷰(«수급 요인» 시황)는 Scope 미결이라 제외.
```

#### 3. Trigger
CRM/콜센터 «다 팔고 예금으로» + 1년 수익률 −6% + 앱 수익률 조회 급증.

#### 4. Customer Context
```text
재직기 · 46세 · 위험중립형 · 해외주식형 펀드(4등급) 60% + 예금 · 매수 후 14개월 · 은퇴까지 15년
```

#### 5. Interesting Evidence Combination
```text
«전부 예금으로» 요청
+ 손실 −6%(계좌 1년) · 보유 펀드 4등급(성향 범위 내)
+ 조회 급증(불안 신호 — 의사 아님)
+ 투자 기간 15년(타임 호라이즌 재료)
+ 과거 손실 후 매도 이력 1회(처분효과 재료)
```

#### 6. Potential Segment
`재직기` × `실적배당 중심` × `손실 구간` × `전량 매도 요청` × `고객 결정 지원`

#### 7. Potential Badges
```text
Primary:   손실 구간 · 매도 요청
Secondary: (없음)
Signal:    수익률 조회 급증
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-006 · OK-029 · OK-017 (매도 후 재매수 가능 여부는 판매 상태)
Product:            (예금 유형 — OK-010; 특정 상품 없음)
Hot Tip:            HT-003
Talk:               TALK-002 · TALK-003 · TALK-005 · TALK-018 · TALK-010
Screen:             SCR-010 스타뱅킹 보유상품변경 · SCR-001 · SCR-004
Knowledge Gap / Conflict: 시황·전망 발언 금지(F59 참고) — 하우스뷰 사용 여부는 Scope 미결 · KG-001 수익률 지표 정의
```

#### 9. Expected Agent Discovery
«팔지 말라» 도 «팔라» 도 Agent 의 답이 아니라는 것. 예금 100% 는 성향상 허용되므로 실행 가능하고, 다만 고객이 결정하기 전에 알아야 할 재료(기간·처분효과·일부 매도 선택지)가 있다. 조회 급증은 불안의 신호이지 매도 의사의 확정이 아니다.

#### 10. Required Confirmation
```text
Employee Check: 보유 펀드 판매 상태·환매 소요 · 성향 범위
Customer Check: 매도 이유(손실 확정 두려움/자금 필요) · 일부 매도 수용 · 자금 사용 시점
```

#### 11. Potential Management Direction
```text
If 자금 필요/불안 극심:
→ 전량 매도·예금 전환 실행 지원(고객 결정 존중)
If 장기 자금:
→ 일부 매도·되돌릴 수 있음 선택지 + 설명 재료 — 결정은 고객
```

#### 12. Forbidden Shortcut
```text
«지금 팔면 손해 확정» 만류 압박 · 회복 시점·시황 전망 · 유선 특정 펀드 교체 권유(OK-029) · 조회 급증을 이탈 의사로 승격
```

#### 13. Expected Brief Fit
- **S1**: 요청·손실·조회·기간.
- **S2** — Main: 결정 전 확인 3가지. Why now: 요청 직후. Customer check: 이유·수용.
- **S3**: 전량/일부/유지 — 복수 방향, 고객 결정.
- **S4**: Opening(TALK-002) «마음 불편하셨죠 — 예금으로 다 바꾸는 것도 가능해요. 그 전에 딱 두 가지만 같이 볼까요». 
- **S5**: 앱 보유상품변경 · TALK-003·018 재료 · HT-003.

#### 14. Potential Chat Questions
```text
다 팔면 손해가 확정되는 거야?
일부만 파는 것도 돼?
예금으로 바꾸면 다시 못 사?
```

#### 15. Demo Wow
«Agent 가 말리지 않는다» — HD-6 의 방향 중립을 발표에서 보여줄 유일한 장면.

#### 16. Grounding Status
```text
STRONG (OK-006 T1 · 화법 T2/T3)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 3 |
| 데이터 결합성 | 4 |
| Knowledge 활용성 | 4 |
| 직원 실용성 | 5 |
| Agent 판단성 | 5 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **33** |

---

### DC-036 — 고객은 «TDF 뭐 살까» 를 묻는데 시스템에는 만기 D-5 · 미신청분 · 한도 초과가 동시에 있다

#### 1. Case Concept
고객 발화 주제(TDF 선택)와 시스템 시한(정기예금 만기 D-5 · 직전 연도 세액공제 미신청분 미등록 · 위험자산 한도 초과 상태)이 서로 다른 고객에서, Agent 가 «시한 임박도 → 고객 이익 영향 → 접점 자연스러움» 순으로 우선순위를 세워 **만기 예약변경을 먼저, TDF 는 한도 해소와 함께** 논의하도록 상담 순서를 재구성하는 Case.

#### 2. Why This Case Exists
```text
Reference:   C06(순서 트랩) · [05:394] 명단 vs 조회 · [01:1370] 미신청금액 등록 유도 · [01:1605] 위반일수
Knowledge:   OK-004(D-5 — 예약변경 창구 안) · OK-009(미신청분 [06-12-622]) · OK-012(한도 초과·TDF 는 100% 예외 → TDF 매수는 한도와 무관하게 가능) · OK-025(TDF 선택 기준) · OK-006(등급) · INTERPRETATION_DESIGN 축7 우선순위
Source:      SRC-007 · SRC-003 · SRC-077 · SRC-090
Golden/Case: GC-22(복수 시한, PASS)는 시한끼리의 충돌. «고객 질문 주제 vs 시스템 시한» 충돌은 없음 — golden digest §8.4. TDF 가 한도 예외라는 사실이 반전 요소.
```

#### 3. Trigger
내점 «TDF 하나 고르고 싶다» + 시스템: 만기 D-5 · 미신청분 표시 · [04-12-354] 위반 상태.

#### 4. Customer Context
```text
재직기 · 43세 · 적극투자형 · 주식형 ETF 72% + 정기예금(만기 D-5) · DO 뿔려드림 · 직전 연도 미신청분 있음
```

#### 5. Interesting Evidence Combination
```text
발화 «TDF 뭐 살까»
+ 정기예금 만기 D-5(예약변경 미등록)
+ 위험자산 72% 초과 상태
+ 직전 연도 미신청분 미등록
+ TDF 는 100% 예외 상품(한도 무관 매수 가능)
```

#### 6. Potential Segment
`재직기` × `실적배당 중심` × `복수 시한` × `TDF 관심` × `우선순위 판단`

#### 7. Potential Badges
```text
Primary:   정기예금 만기 D-5
Secondary: 위험자산 한도 초과 · 미신청분 미등록
Signal:    TDF 문의
```

#### 8. Required Knowledge
```text
Official Knowledge: OK-004 · OK-009 · OK-012 · OK-025 · OK-006 (적극투자형 3~6등급 — TDF 시리즈 «다소높은» 3등급 가능)
Product:            PRD-001~004 (등급·as_of) · PRD-034 (참고)
Hot Tip:            HT-039 (100% 가능 상품) · HT-017/049 (미신청금액 계산기)
Talk:               TALK-019 · TALK-021
Screen:             SCR-017 [06-12-611] · SCR-006 [06-12-622] · SCR-020 [04-12-354] · SCR-004 [04-12-17A]
Knowledge Gap / Conflict: 70% 예외 상품 범위 T3 나열(OK-012) · 미신청분 등록 시점(7/1) T3 · 산정 기준 표현 상이
```

#### 9. Expected Agent Discovery
고객이 꺼낸 주제가 오늘 가장 급한 일이 아니라는 것 — D-5 만기가 먼저다. 그런데 TDF 가 **한도 예외**라 «한도 초과라서 TDF 못 산다» 는 오답이고, 만기자금을 TDF 로 돌리면 만기·한도·관심을 한 번에 다룰 수 있다는 연결이 보인다. 미신청분은 급하지 않지만 해지·개시 전 등록 사항으로 남긴다.

#### 10. Required Confirmation
```text
Employee Check: [06-12-611] 예약 상태 · [04-12-354] 초과액 · [06-12-622] 미신청분 · TDF 후보 등급([04-12-17A])
Customer Check: 은퇴 시점(빈티지) · 만기자금 사용계획 · 위탁 vs 직접
```

#### 11. Potential Management Direction
```text
순서: ① 만기 D-5 예약변경(만기자금 성격 확인) → ② TDF 선택 기준 안내(빈티지·등급, 한도 예외) → ③ 한도 초과 해소 경로(비위험/추가입금) → ④ 미신청분 등록은 후속
If 만기자금이 장기: 예약변경 대상으로 TDF 유형 가능(성향 범위) — 상품 확정은 고객
```

#### 12. Forbidden Shortcut
```text
질문 순서대로 TDF 만 답하고 만기 놓침 · «한도 초과라 TDF 불가» 오답 · 특정 TDF 확정(G1) · 미신청분 7/1 확정 인용
```

#### 13. Expected Brief Fit
- **S1**: 발화·D-5·초과·미신청분.
- **S2** — Main: 우선순위(만기 → TDF/한도 → 미신청분). Why now: D-5. Customer check: 은퇴 시점·사용계획.
- **S3**: 순서 + TDF 기준(조건부).
- **S4**: Opening «TDF 얘기 드리기 전에 닷새 뒤 만기 예금부터 정하면, 그 돈으로 TDF 를 볼 수도 있어요». 
- **S5**: [06-12-611] · [04-12-354] · [06-12-622] · [04-12-17A] · HT-039.

#### 14. Potential Chat Questions
```text
한도 넘었는데 TDF 는 살 수 있어?
만기 예금을 TDF 로 바로 넣을 수 있어?
미신청분은 언제까지 등록해야 해?
```

#### 15. Demo Wow
«고객이 묻지 않은 것을 먼저 챙기는» Agent — 우선순위 판단이 화면에서 보인다.

#### 16. Grounding Status
```text
STRONG (OK-004·009·012·025 T2/Public)
```

#### 17. Demo Score

| 평가축 | 점수 |
|---|---:|
| 발견성 | 5 |
| 데이터 결합성 | 5 |
| Knowledge 활용성 | 5 |
| 직원 실용성 | 4 |
| Agent 판단성 | 4 |
| Demo Wow | 4 |
| 기존 Case 대비 차별성 | 4 |
| Brief Fit | 4 |
| **총점** | **35** |

---

## 8. Seed Case 3종 재평가

평가 기준은 §4 의 8축과 §1 의 목적(결합 밀도 · Negative/Preservation 포함)이다. **Seed 파일은 수정하지 않는다** — 여기 적는 것은 다음 단계의 결정 재료다. 근거는 `demo/seed_cases/DEMO-0x_*.md` §12(내부 정합)·§13(Repo 정합)·§14(Open Questions)와 `demo/HTML_EXTRACTION_AUDIT.md` §6·§8 이며, 새 사실을 더하지 않았다.

| Verdict | 뜻 |
|---|---|
| KEEP | 주제·판단 구조 유지. P0/P1 지식 충돌만 정리 |
| IMPROVE | 주제는 유지하되 판단 구조(확인 우선·조건부·근거 등급)를 보강 |
| REPLACE | 주제 교체 — 이번 재평가에서 해당 없음 |

### 8.1 DEMO-01 김서연 — 타행 ISA 만기 × 세액공제 × ETF 조회

**Current Strength**
- 계좌 밖 정보(타행 ISA 8,000만 · 만기 D-3)를 당행 IRP 와 한 카드에 묶는 «Wider Context» 의 교본이다. 60일 창구(OK-001)라는 시한이 «왜 지금» 을 만든다.
- 세제 Opportunity(잔여 한도 + 전환 10%/300만)와 Digital Signal(ETF 조회 → S3 조건부 타일)이 한 고객에 들어 있어 Capability 5종을 한 화면에서 보여준다.
- HTML 이 스스로 «9.9%·3.3~5.5% 는 현장 팁 출처» 라고 근거 등급을 노출한다 — Authority 표시의 원형.

**Current Weakness**
- P0 지식 충돌 2건: 환급액 49.5만/39.6만(HT-004, 300만 기준) vs OK-001(198만/158.4만, 1,200만 기준) · 세율 9.9%/3.3~5.5% 의 유일 근거 HT-045 가 T3-only 인데 S4 반응 1 에서 확정 화법으로 쓰인다.
- 상품 근거 공백: ETF 후보 2종(KODEX 장기채권PLUS · RISE 200)이 Registry 에 없고, TDF «2030» 빈티지 특정도 PRD-004(시리즈 단위)에 없다. IRP 내 «KB저축은행 정기예금 +4.3%» 는 PRD-019 유형만 있다.
- 판단 구조: 사용계획 확인 → 전환 규모 결정의 Gate(G1 조건성)가 S2 에 명시돼 있지 않다. «위험중립형인데 현금성 67%» 를 불일치로 지적하지만 사용계획 확인 없이 세미나 매칭으로 넘어간다.
- 데이터 정합: 부점 브리핑 «ISA 만기 3명» 과 실제 1명(C-01) · D-3 의 60일 기산 방식 미정(OK-001 Limitation) · 이벤트 종료 10/30 과 60일 종료 11/6 의 순서 미언급(ISSUE-06).

**Verdict: IMPROVE**

**Suggested Improvement** (Seed 파일 수정 아님 — 다음 단계 제안)
1. 세제 수치는 OK-001 한 갈래로 두고, HT-004·HT-045 는 «현장 팁 · 공식 확인 전» 라벨로 Chat 근거 칸에만 둔다 (P0 · Human Decision §15-5).
2. ETF·TDF 는 «채권형 ETF 유형 · TDF 시리즈» 수준으로 낮추거나 Registry 등록을 별도 결정한다 (임의 교체 금지).
3. S2 첫 항목을 «ISA 만기자금의 사용계획 확인» 으로 세워 전환 규모를 조건부로 만든다 — DC-005 의 If 장기/단기 분기와 같은 구조.
4. GC-13/GC-18 계보 결정 후 D-day 규칙(기산 방식)을 명시한다.

**관련 Candidate**: DC-005(ISA 만기 × 종합과세 — 변주) · DC-003(세액공제 × 결정세액 — 세제 축 보강) · DC-009 / DC-033(ETF 조회가 이어지는 다음 장면).

### 8.2 DEMO-02 이수민 — 정기예금 만기 × 현금성 대기 × DO 미등록

**Current Strength**
- 만기 + 방치 + 미등록 세 신호를 «운용 공백» 한 주제로 묶고, 예약변경 가능 구간(만기 1개월 전, OK-004)을 «왜 지금» 으로 쓴다.
- «DO 등록만으로 기존 1,000만은 안 움직인다» 를 S3 foot 과 챗 q3 에서 이중으로 짚는다(OK-005) — 등록·자금 분리 원칙을 Demo 가 정확히 말한다.
- 실적배당형 제안을 «위험중립형 범위 내» 로 한정하고(OK-006), 화법 답변에 «본부 확정 지침이 아닙니다» 가드를 붙였다. 업무화면 2종(SCR-001·SCR-016)이 실제 처리와 맞는다.

**Current Weakness**
- P1 지식 충돌: DO 구성 설명(뿔려드림 «TDF·자산배분형 중심» · 모두드림 «TDF 100%»)이 PRD-021/SC-004 «종수·구성 확정 인용 금지» 와 충돌. «주요 시중은행 1위» 범위 미확정 · 국민연금 6.21%/퇴직연금 2.35% 는 2023 공시 수치인데 as-of 없음(TALK-017 규범) · 가드 원칙의 출처 귀속 오류(SRC-001 vs SRC-002).
- 판단 구조: «현금성 장기대기» 라벨을 붙이면서 OK-028 의 미운용 판별 2요건(① 1개월 이상 금액 변동 없음 ② [04-12-644] 입금사유가 교체매매·연금지급 아님)을 확인하지 않는다 — DC-013 이 보여주는 오탐 구조가 Seed 안에 그대로 있다.
- 데이터: 51세 고객의 세액공제 정보가 비어 있음(의도 여부 미정) · «약 10주» 는 달력상 11주 · HT-006 은 PROVISIONAL·구자료(DO 시행 직후) 플래그.

**Verdict: KEEP**

**Suggested Improvement**
1. S1 에 OK-028 2요건 확인 결과를 한 줄로 넣는다(«입금사유 교체매매 아님 · 77일 무변동») — 라벨의 근거가 생긴다.
2. DO 구성 문장은 «위험도 4단계 · 구성은 상품설명서 확인» 으로 낮추거나 SC-004 해소 후 복원한다 (P1).
3. 수치 인용 3건(1위 범위 · 2023 공시 · 72의 법칙 예시)에 as-of 를 붙이거나 Chat 근거 칸으로 내린다.
4. 세액공제 정보 공란은 «조회 이력 없음 → 확인 우선» 으로 살리면 확인 우선 판단이 하나 더 생긴다.

**관련 Candidate**: DC-008(만기 후 4주 + DO 등록 — 이수민의 반대 상태) · DC-013(현금성 대기 판별의 Negative) · DC-014(만기 임박 + 예약 완료 Negative) · DC-019(재운용 상품 선택의 다음 장면) · DC-031(월 단위 금리 시점).

### 8.3 DEMO-03 박정호 — 퇴직급여 일반통장 수령 × 60일 과세이연 × 상담이력

**Current Strength**
- IRP 원장 밖(당행 입출금계좌 입금)을 트리거로 쓰고, 콜센터 발화 → 메뉴 조회 순서로 «관심 확인» 을 만든다. 기존 GC 는 전부 IRP 입금 완료 상태라 이 구조는 Demo 만의 것이다.
- 상품보다 처리 순서(등록 후 입금)를 먼저 세우고 업무화면에 순번을 붙였다(OK-014·SCR-021·014·023·008). 상담 기억·요약·쪽지를 한 고객에서 다 보여준다.
- Opening 이 «사용계획 확인» 으로 시작한다(TALK-006·007 취지). 재취업 3단 구성은 ⚠ «본부 확정 지침 아님» 으로 등급을 가른다.

**Current Weakness**
- P0 지식 충돌: 챗 q2 «10년 이하 30% / 초과 40%» 2단 vs OK-009 «70/60/50%» 3단(20년 초과 50%). SC 미등록.
- 절차 누락: OK-014 Step4(과세이연정보 수정 요청)가 빠졌다. 수익률 +2.9%(리스트) vs +3.2%(상세·챗) 충돌(C-05).
- 축 불일치: 브리핑은 과세이연 단일 주제인데 챗 요약의 관리 사유는 «원리금 편중 · 개시 미개시 · 세액공제 · 추가입금 여력» (C-09). Case 계보 없음(P0) · 쪽지·상담기억 기능의 Registry·화면 근거 없음.
- 판단 구조: 사용계획 확인이 화법에는 있지만 S3 운용안(GIC 중심 + 단기채)이 그 확인 결과와 조건부로 묶여 있지 않다 — «잔금 발화» 하나로 방향이 뒤집히는 DC-002 구조가 Seed 에는 없다.

**Verdict: IMPROVE**

**Suggested Improvement**
1. 감면율은 OK-009 3단으로 정리하고 HTML 2단 표기는 SC 등록 여부를 Human 이 정한다 (P0 · §15-4).
2. 처리 순서에 Step4 를 넣고, 수익률은 한 값으로 고른다(HTML 값 보존 원칙상 선택은 Human).
3. S2 «확인할 점» 을 «60일 시한 내 사용계획» 하나로 세우고 S3 운용안을 «사용계획 없음 확인 시» 조건부로 묶는다 (G1).
4. 챗 요약의 관리 사유 4개 중 브리핑에 없는 축(개시 미개시 · 편중)은 «후속 관리 사유» 로 분리 표기하거나 삭제한다.
5. «통장 수령 → 60일 재입금» 구조를 신규 Case 계보로 세울지 결정한다 — DC-001(전 단계)·DC-002(다음 장면)와 3부작이 된다.

**관련 Candidate**: DC-001(퇴직 예정 — 전 단계) · DC-002(IRP 입금 후 DO 2주 창 — 다음 장면) · DC-020(개시 실행 순서) · DC-023(재취업 3단 구성의 공식판 · OK-019/020).

### 8.4 Seed 3종 종합

Candidate 와 같은 8축으로 채점했다(휴리스틱 · Freeze 근거 아님).

| Seed | 발견성 | 결합성 | Knowledge | 실용성 | 판단성 | Wow | 차별성 | Brief Fit | 총점 | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 김서연 | 4 | 5 | 5 | 4 | 2 | 4 | 3 | 5 | **32** | IMPROVE |
| 이수민 | 3 | 4 | 5 | 5 | 3 | 3 | 4 | 5 | **32** | KEEP |
| 박정호 | 5 | 5 | 4 | 5 | 3 | 5 | 5 | 4 | **36** | IMPROVE |

관찰: 세 Seed 모두 **«개입 필요(적극관리)» 결과**이고, «확인 우선 · 현 상태 유지 · 실행 제약» 결과가 하나도 없다. 판단성 축이 2~3점에 머무는 이유가 그것이다. Candidate 36 은 이 빈자리를 채우도록 설계했다(§12).

---

## 9. Candidate Ranking

정렬: 총점 내림차순 → 동점이면 ① Grounding(STRONG 우선) ② Portfolio 희소성(유지·실행 제약·확인 우선 결과, 연금수령기·퇴직 전후 Lifecycle) ③ «기존 Case 대비 차별성» 축 점수. 점수는 §4 의 상대 휴리스틱이며 최종 15 의 근거가 아니다.

| Rank | ID | Case Theme (요약) | Grounding | Score | Portfolio 역할 | Shortlist |
|---:|---|---|---|---:|---|---|
| 1 | DC-002 | 퇴직급여 입금 D+5 · DO 2주 창 · «잔금» 발화 → 현금 유지 | STRONG | 37 | 고객확인 우선 · 퇴직 직후 | ✓ |
| 2 | DC-020 | «개시하겠다» 결정 고객의 실행 순서 | STRONG | 36 | 적극관리(절차) · 연금개시 | ✓ |
| 3 | DC-026 | 전출 의사확인 무응답 · 자동취소 기한 | STRONG | 35 | 정보안내 · 이탈(절차 존중) | ✓ |
| 4 | DC-036 | 복수 시한 충돌 · 고객은 TDF 를 묻는다 | STRONG | 35 | 적극관리(우선순위) | ✓ |
| 5 | DC-008 | 만기 후 4주 · DO D-14 · «다른 상품으로» | STRONG | 35 | 적극관리 · 조건부 | ✓ |
| 6 | DC-003 | 연말 D-70 · 상여 · 결정세액 | STRONG | 34 | 조건부 · 세제 | ✓ |
| 7 | DC-004 | 다운사이징 차액 6개월 예외 납입 | STRONG | 34 | 직원확인 우선 · 세제 | ✓ |
| 8 | DC-017 | ELB 만기 · 연금개시 예정 · 지급 가능 여부 | STRONG | 34 | 직원확인 우선 · 상품 | ✓ |
| 9 | DC-018 | «예금 깨야 하나» 특별중도해지 오해 | STRONG | 34 | 정보안내 · 고객 결정 | ✓ |
| 10 | DC-019 | «GIC 전부» · 단리환산 · 매수한도 · 예보 충돌 | STRONG | 34 | 조건부 · Source Conflict 노출 | ✓ |
| 11 | DC-001 | 퇴직 예정 · DC 예금 만기 vs 퇴직일 | MEDIUM | 34 | 고객확인 우선 · 퇴직 직전 | ✓ (보강 조건) |
| 12 | DC-021 | 자유인출 · 사적연금 1,500만 경계 | MEDIUM | 34 | 고객 결정 지원 · 연금수령기 | ✓ (보강 조건) |
| 13 | DC-013 | 현금성 증가 · 입금사유 교체매매 · LMS 예정 → 접촉 불필요 | STRONG | 33 | 현 상태 유지(오탐 방지) | ✓ |
| 14 | DC-010 | 안정형 × TDF 요청 × 앱 차단 × 재분석 문의 | STRONG | 33 | 실행 제약 · 정보안내 | ✓ |
| 15 | DC-034 | 현금성 7,500만↑ · 사용계획 확정 · 조건부 단기 운용 | STRONG | 33 | 조건부 · 유지 | ✓ |
| 16 | DC-035 | 손실 · «전부 예금으로» · 변경도 유지도 정답 | STRONG | 33 | 고객 결정 지원 | ✓ |
| 17 | DC-009 | 위험자산 한도 초과 · «ETF 100%» 오해 | STRONG | 33 | 조건부 · Digital | alt-1 |
| 18 | DC-015 | AI일임 운용 중 · 이전/인출 요청 | MEDIUM | 33 | 실행 제약 · 순서 | ✓ (보강 조건) |
| 19 | DC-014 | 예약변경 완료 · TM 리스트 → 아무것도 하지 말 것 | STRONG | 32 | 현 상태 유지(리스트 오탐) | ✓ |
| 20 | DC-028 | 성향 하향 · 기존 2등급 보유 유지 | STRONG | 32 | 현 상태 유지 · Digital | ✓ |
| 21 | DC-006 | 연금저축보험 · 55세+5년 «충족 도래» | STRONG | 32 | 직원확인 우선 · GC-15 Pair | alt-2 |
| 22 | DC-022 | 55세 도달 · 법정 사유 없는 목돈 → 3자 비교 | STRONG | 32 | 고객 결정 지원 | alt-3 |
| 23 | DC-032 | 전화 채널 펀드 변경 · 금소법 · 컨설팅센터 | STRONG | 32 | 실행 제약(채널) | alt-4 |
| 24 | DC-011 | 공격투자형 · 예금 100% · 2년 내 주택 → 유지 | STRONG | 31 | 현 상태 유지(성향-운용) | ✓ |
| 25 | DC-024 | 대출 동반 이전 · VIP · 전출 접수 | MEDIUM | 31 | 고객 결정 지원 · 이탈 | alt-5 |
| 26 | DC-027 | 타사 IRP 전입 · 마이데이터 · DO 선해지 | MEDIUM | 31 | 직원확인 우선 · 전입 | – |
| 27 | DC-016 | TDF 빈티지 · 은퇴 변경 | STRONG | 30 | 고객확인 우선 · 상품 | – |
| 28 | DC-033 | ETF 체결 지연 문의 | STRONG | 30 | 정보안내 · Digital | – |
| 29 | DC-007 | 개시된 연저 0원 이전 | MEDIUM | 30 | 고객 결정 지원 · 연금수령기 | – |
| 30 | DC-025 | 수수료 단독 이탈 · 비대면 전환 | MEDIUM | 30 | 정보안내 · 이탈 | – |
| 31 | DC-029 | «만기 때 연락» 약속 · 담당 변경 | MEDIUM | 30 | 적극관리(약속 이행) | – |
| 32 | DC-023 | 개시 후 재취업 · 신규 IRP | STRONG | 29 | 적극관리(절차) | – |
| 33 | DC-030 | 20대 첫 입금 · 2주 · 청년 할인 | STRONG | 29 | 정보안내(LMS) | – |
| 34 | DC-005 | ISA 만기 × 종합과세 대상 | MEDIUM | 29 | 고객확인 우선 · 세제 | – |
| 35 | DC-012 | 판매중단 펀드 추가 매수 요청 | MEDIUM | 29 | 실행 불가 · 시점 의존 | – |
| 36 | DC-031 | «지난달 4.6%» · 월 단위 금리 | MEDIUM | 28 | 정보안내 · 시점 판단 | – |

Rank 17 DC-009 가 Shortlist 에 빠지고 Rank 18·24 가 들어간 이유: DC-009 의 판단축(한도 초과 → 비위험 매수)은 DC-036 과 겹치고, DC-015 (AI일임 실행 제약) · DC-011 (성향-운용 불일치의 유지 판단)은 Portfolio 에 대체가 없다. Digital 축이 더 필요하면 DC-009 를 첫 교체 후보로 쓴다(§11).

---

## 10. Recommended Shortlist 20

Freeze 아님. 최종 15 는 Human Review 가 정한다. 각 항목의 «보강 조건» 은 Case 를 쓰기 전에 지식 쪽에서 닫아야 하는 일이다.

| # | ID | Case Theme | 선정 이유 | 보강 조건 |
|---:|---|---|---|---|
| 1 | DC-002 | 퇴직급여 입금 D+5 · DO 2주 창 · «잔금» 발화 → 현금 유지 | 박정호의 다음 장면. 발화 하나로 방향이 뒤집히는 확인 우선의 대표 | – |
| 2 | DC-020 | 연금개시 실행 순서(미신청분 → 자동이체 → 지급설계) | 절차형 S3·S5 의 교본. 화면 6종이 순번으로 붙는다 | SC-002 화면번호 · KG-004 7/1 발급 시점(T3) |
| 3 | DC-026 | 전출 의사확인 무응답 · 자동취소 기한 | «이탈을 막지 않고 고객 의사대로 되게 한다» — HD-7/G4 를 화면으로 증명 | – |
| 4 | DC-036 | 복수 시한 충돌 · 고객은 TDF 를 묻는다 | Chat 질문과 시스템 시한의 우선순위를 Agent 가 정리한다 | – |
| 5 | DC-008 | 만기 후 4주 · DO D-14 · «다른 상품으로» | 이수민의 반대 상태(DO 등록). 옵트인/변경 2단계 분기 | SC-004 DO 구성 인용 금지 유지 |
| 6 | DC-001 | 퇴직 예정 · DC 예금 만기 vs 퇴직일 | 박정호의 전 단계. 퇴직 전 Scope 가 열리면 3부작이 된다 | 퇴직 시 DC 예금 현금화 규칙 공식 확인 · Scope 결정(§15-9) |
| 7 | DC-003 | 연말 D-70 · 상여 · 결정세액 | 세제 축을 «한도» 가 아니라 «결정세액» 으로 한 단계 깊게 | KG-005 결정세액 Public-only |
| 8 | DC-004 | 다운사이징 차액 6개월 예외 납입 | 1,800만 «한도 밖» 납입 — 직원도 잘 모르는 요건 | 요건 판정은 공식 절차(정보 수준 유지) |
| 9 | DC-017 | ELB 만기 · 연금개시 예정 · 지급 가능 여부 | 상품별 연금지급 가능 여부(OK-011)를 직원이 먼저 확인하는 구조 | ELB 신규 축 포함 여부(§15-8) |
| 10 | DC-018 | «예금 깨야 하나» 특별중도해지 오해 | 오해 정정만으로 개시를 앞당길 수 있는 정보안내 Case | – |
| 11 | DC-019 | «GIC 전부» · 단리환산 · 매수한도 · 예보 충돌 | Source Conflict(SC-001) 를 숨기지 않고 «미확정» 으로 노출 | SC-001 노출 방식(§15-6) |
| 12 | DC-021 | 자유인출 · 1,500만 경계 | 연금수령기 Case 의 유일한 세제 축 | 타 연금계좌 합산 데이터 경로 · 골든라이프센터 연계 근거 |
| 13 | DC-013 | 현금성 증가 · 교체매매 · LMS 예정 → 접촉 불필요 | 이수민 라벨의 오탐 방지. OK-028 2요건 + 자동 LMS 를 읽는다 | – |
| 14 | DC-010 | 안정형 × TDF 요청 × 앱 차단 × 재분석 문의 | 실행 제약 + «재분석은 안내만» 의 경계(OK-006·029) | KG-006 재분석 절차 |
| 15 | DC-015 | AI일임 운용 중 · 이전/인출 요청 | 일임 계약이 있는 계좌의 실행 순서 제약 | OK-027 절차 상세 · AI일임 축 포함 여부(§15-8) |
| 16 | DC-034 | 현금성 7,500만↑ · 사용계획 확정 · 조건부 단기 운용 | 현금 유지가 합리인 큰 금액 — 권유 제외 Badge | 단기 상품 실재 여부(PRD 월간) |
| 17 | DC-035 | 손실 · «전부 예금으로» · 변경도 유지도 정답 | 고객 결정 지원의 대표. Agent 가 정답을 주지 않는다 | TALK-021 은 T3 설명 재료로만 |
| 18 | DC-011 | 공격투자형 · 예금 100% · 2년 내 주택 → 유지 | 성향-운용 불일치가 «관리 사유가 아님» 을 보여주는 유지 Case | – |
| 19 | DC-014 | 예약변경 완료 · TM 리스트 → 아무것도 하지 말 것 | 리스트 오탐 · 접촉 과잉 방지. 통화 배정 취소가 정답 | – |
| 20 | DC-028 | 성향 하향 · 기존 2등급 보유 유지 | OK-006 «기존 보유는 위반 아님» 의 유일한 Demo | KG-006 |

**교체 후보(alternates)** — 축 균형을 위해 바꿔 넣을 때의 짝:

| Alt | ID | 들어가면 강해지는 축 | 바꿀 만한 자리 |
|---|---|---|---|
| alt-1 | DC-009 위험자산 한도 초과 · «ETF 100%» | Digital ◎ · 상품 | DC-036 과 한도 축 중복 → DC-015 대신 (AI일임 축을 안 쓰기로 하면) |
| alt-2 | DC-006 연금저축보험 55세+5년 | Wider Context · 확인 우선 · GC-15 Pair | DC-004 대신 (세제 축이 과하면) |
| alt-3 | DC-022 55세 · 목돈 · 3자 비교 | 고객 결정 지원 · Retirement | DC-018 대신 (개시 오해와 개시 선택 중 하나만) |
| alt-4 | DC-032 전화 채널 펀드 변경 · 금소법 | 실행 제약(채널) · 업무화면 | DC-010 대신 (실행 제약을 성향이 아니라 채널로 보여주려면) |
| alt-5 | DC-024 대출 동반 이전 · VIP | 이탈 ◎ · Wider Context | DC-011 대신 (이탈 Case 를 늘리기로 하면) |

**최종 15 구성 시 권고 하한**(Rule 아님): 현 상태 유지 ≥ 3 · 확인 우선(고객/직원) ≥ 3 · 실행 제약 ≥ 1 · 고객 결정 지원 ≥ 2 · 연금개시/수령기 ≥ 3 · 퇴직 전후 ≥ 2 · 이탈 ≥ 1 · Source Conflict 노출 ≥ 1. Seed 3명을 15 안에 넣을지는 §15-4 의 결정에 따른다.

---

## 11. Capability Coverage Matrix

◎ 핵심 · ○ 보조 · - 없음. Shortlist 20 + 교체 후보 5 + Seed 3(비교용). «이탈» 은 이탈 방어가 아니라 **이탈·이전 상황의 해석**(방해 금지 포함)이다.

| Case | 상황해석 | Event | Wider Context | Digital | 세제 | 상품 | Retirement | 이탈 | 확인우선 | 유지판단 | 업무화면 | Chat |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| DC-002 퇴직급여 D+5 · DO 2주 · 잔금 | ◎ | ◎ | ○ | - | ○ | - | ◎ | - | ◎ | ○ | ○ | ◎ |
| DC-020 연금개시 실행 순서 | ○ | ○ | ○ | - | ◎ | - | ◎ | - | ○ | - | ◎ | ○ |
| DC-026 전출 의사확인 무응답 | ◎ | ◎ | ○ | ○ | - | - | - | ◎ | ◎ | - | ◎ | ○ |
| DC-036 복수 시한 · TDF 질문 | ◎ | ◎ | - | ○ | ○ | ◎ | - | - | ○ | - | ○ | ◎ |
| DC-008 만기 후 4주 · DO D-14 | ○ | ◎ | - | ○ | - | ◎ | - | ○ | ○ | - | ◎ | ○ |
| DC-001 퇴직 예정 · DC 예금 만기 | ◎ | ◎ | ◎ | - | ◎ | ○ | ◎ | - | ◎ | ○ | ○ | ○ |
| DC-003 연말 D-70 · 결정세액 | ○ | ◎ | ◎ | - | ◎ | ○ | - | - | ◎ | - | ○ | ◎ |
| DC-004 다운사이징 6개월 예외 | ○ | ◎ | ◎ | - | ◎ | - | ○ | - | ◎ | - | ○ | ○ |
| DC-017 ELB 만기 · 개시 예정 | ○ | ◎ | - | - | - | ◎ | ◎ | - | ◎ | - | ○ | ○ |
| DC-018 «예금 깨야 하나» 오해 | ◎ | ○ | ○ | - | ○ | ○ | ◎ | - | ○ | ○ | ○ | ◎ |
| DC-019 GIC 전부 · 단리 · 예보 | ○ | ○ | - | - | - | ◎ | - | - | ◎ | - | ○ | ◎ |
| DC-021 자유인출 · 1,500만 | ○ | ○ | ◎ | - | ◎ | - | ◎ | - | ○ | - | ○ | ◎ |
| DC-013 교체매매 · 접촉 불필요 | ◎ | - | - | ○ | - | - | - | - | ○ | ◎ | ◎ | ○ |
| DC-010 안정형 × TDF · 앱 차단 | ○ | - | - | ◎ | - | ◎ | - | ○ | ○ | ○ | ○ | ◎ |
| DC-015 AI일임 중 인출/이전 | ◎ | ○ | ○ | - | ○ | ○ | - | ○ | ○ | - | ◎ | ○ |
| DC-034 현금성 7,500만 · 사용계획 확정 | ◎ | ○ | ○ | - | ○ | ○ | ○ | - | ◎ | ◎ | ○ | ○ |
| DC-035 손실 · 전부 예금으로 | ○ | - | - | ○ | - | ○ | - | ○ | ○ | ○ | ○ | ◎ |
| DC-011 공격형 · 예금 100% · 주택 | ◎ | - | ◎ | - | ○ | - | - | - | ○ | ◎ | - | ○ |
| DC-014 예약변경 완료 · TM 리스트 | ◎ | ◎ | - | ○ | - | - | - | - | - | ◎ | ◎ | ○ |
| DC-028 성향 하향 · 보유 유지 | ◎ | ○ | - | ◎ | - | ◎ | - | ○ | ○ | ◎ | ○ | ◎ |
| **◎ 합계 (Shortlist 20)** | **11** | **9** | **5** | **2** | **5** | **6** | **6** | **1** | **8** | **5** | **6** | **9** |
| alt-1 DC-009 한도 초과 · ETF 100% | ○ | - | - | ◎ | - | ◎ | - | - | ○ | - | ○ | ◎ |
| alt-2 DC-006 연저보험 55세+5년 | ○ | ◎ | ◎ | - | ○ | ○ | ○ | - | ◎ | ○ | ○ | ○ |
| alt-3 DC-022 55세 · 목돈 · 3자 비교 | ○ | ◎ | ○ | - | ◎ | - | ◎ | ○ | ○ | ○ | ○ | ◎ |
| alt-4 DC-032 전화 채널 펀드 변경 | ○ | - | - | ○ | - | ○ | - | - | - | - | ◎ | ○ |
| alt-5 DC-024 대출 동반 이전 · VIP | ◎ | ◎ | ◎ | - | - | ○ | - | ◎ | ○ | - | ○ | ○ |
| Seed 김서연 | ○ | ◎ | ◎ | ◎ | ◎ | ◎ | - | - | ○ | - | ◎ | ◎ |
| Seed 이수민 | ◎ | ◎ | - | ○ | - | ◎ | - | ○ | ○ | - | ◎ | ◎ |
| Seed 박정호 | ◎ | ◎ | ◎ | ◎ | ◎ | ○ | ◎ | - | ○ | - | ◎ | ◎ |

관찰
- **얇은 축**: Digital ◎ 2(DC-010·028) · 이탈 ◎ 1(DC-026). Seed 김서연·박정호가 Digital 을, 골든 GC 군이 이탈을 이미 많이 갖고 있어 의도적으로 낮췄지만, Demo 15 를 Seed 없이 짜면 alt-1(DC-009)·alt-5(DC-024)를 넣어야 한다.
- **두꺼운 축**: 상황해석 11 · Event 9 · Chat 9 — «단일 Rule 이 아니라 결합» 이라는 §1 목적과 일치한다. 확인우선 8 · 유지판단 5 는 Seed 에 없던 축이다.
- 업무화면 ◎ 6 은 절차형(DC-020·026·008·013·015·014)에 몰려 있다. 나머지는 ○ — 화면번호는 S5 에서만 쓴다는 G3 규범과 맞다.

---

## 12. Judgment Coverage

각 Candidate 의 **주(Primary) 판단 결과** 하나로 집계했다(§7 «Potential Management Direction» 의 첫 분기 기준). 골든 6유형과의 대응: 개입 필요 = 적극관리 + 조건부 Solution · 추가 확인 우선 = 고객확인 + 직원확인 · 현 상태 유지 · 정보 안내 · 고객 결정 지원 · 실행 불가 = 실행 제약·불가.

| 판단 결과 | Candidate 36 | Shortlist 20 | Seed 3 | 해당 ID (Shortlist 굵게) |
|---|---:|---:|---:|---|
| 적극관리 | 5 | 3 | 3 | **DC-020 · 036 · 008** · 023 · 029 |
| 고객확인 우선 | 4 | 2 | 0 | **DC-002 · 001** · 005 · 016 |
| 직원확인 우선 | 4 | 2 | 0 | **DC-004 · 017** · 006 · 027 |
| 조건부 Solution | 4 | 3 | 0 | **DC-003 · 019 · 034** · 009 |
| 현 상태 유지 | 4 | 4 | 0 | **DC-013 · 011 · 014 · 028** |
| 정보안내 | 6 | 2 | 0 | **DC-026 · 018** · 025 · 030 · 031 · 033 |
| 고객 결정 지원 | 5 | 2 | 0 | **DC-021 · 035** · 007 · 022 · 024 |
| 실행 제약·불가 | 4 | 2 | 0 | **DC-010 · 015** · 012 · 032 |
| 합계 | 36 | 20 | 3 | |

관찰
- Shortlist 20 의 **Negative/Preservation 비중**(현 상태 유지 4 + 실행 제약 2 + 고객확인 우선 2) = 8/20. Seed 3 은 전부 적극관리라 «상품을 바꾸세요» 로 수렴한다 — Candidate 가 그 균형을 되돌린다.
- 부(Secondary) 결과까지 보면 DC-002(실행 제약: 자동적용 전 인출 경로) · DC-026(실행 제약: 자동취소) · DC-019(직원확인: SC-001) · DC-018(고객 결정 지원) · DC-034(고객 결정 지원)이 두 유형에 걸친다 — Demo 에서 «판단이 하나로 끝나지 않는다» 를 보여줄 자리.
- 최종 15 에서 적극관리를 Seed 3 으로 채우면 Candidate 쪽 적극관리 3(DC-020·036·008)은 절차형(순서·시한)이라 Seed 의 «권유형» 과 겹치지 않는다.

---

## 13. Knowledge Coverage

§7 각 Candidate 의 «Required Knowledge» 에 적힌 Registry ID 를 집계했다(36 후보 기준 · 한 후보 안의 중복 제거).

| Knowledge 유형 | 참조 건수 | 사용된 ID 종수 / Registry 전체 | 참조한 후보 수 | 최다 참조 ID (후보 수) |
|---|---:|---|---:|---|
| Official Knowledge (OK) | 132 | 30 / 31 | 36 | OK-006 (12) · OK-013 (11) · OK-009 (10) · OK-016 (9) · OK-011 (6) · OK-017 (6) |
| Product (PRD) | 22 | 11 / 34 | 11 | PRD-021 (4) · PRD-033 (3) · PRD-018 (3) |
| Hot Tip (HT) | 71 | 41 / 49 | 33 | HT-048 (6) · HT-005 (5) · HT-035 (4) · HT-006 (3) |
| Talk (TALK) | 60 | 29 / 32 | 31 | TALK-007 (5) · TALK-021 (4) · TALK-031 (3) |
| Screen (SCR) | 121 | 45 / 91 | 36 | SCR-004 [04-12-17A] (12) · SCR-001 [04-12-642] (9) · SCR-010 스타뱅킹 보유상품변경 (7) · SCR-015 [04-10-099] (6) · SCR-007 [02-12-221] (6) |
| Knowledge Gap (KG) | 12 | 8 / 8 | 12 | KG-006 (2) · KG-002 (2) · KG-001 (2) · KG-007 (2) |
| Source Conflict (SC) | 4 | 4 / 5 | 4 | SC-001 (DC-019) · SC-002 (DC-020) · SC-003 (DC-003) · SC-004 (DC-008) |

**과의존 · 주의 플래그**

1. **OK-006 «성향 = 권유 가능 상한»** — 36 중 12 후보. Shortlist 20 에서도 DC-036·008·010·019·034·035·011·028 등에 걸린다. 최종 15 에서 성향 상한이 **핵심 판단**인 Case 는 2~3개(DC-010·028 + 택1)로 제한하고, 나머지는 배경 규칙으로만 쓰기를 권고한다. 한 규칙이 Demo 의 «단일 트릭» 으로 보이면 안 된다.
2. **OK-009 (중도해지·미신청분 등록)** — 10 후보. authority 가 T2 + Public + **T3(등록 실무·발급 시점)** 혼합이고 KG-004(7/1 발급)가 걸려 있다. 미신청분 등록·발급 시점은 공식 확인 전에는 «정보» 수준으로만 쓴다(DC-020·036·022 해당).
3. **SCR-004 [04-12-17A]** — 12 후보. 판매가능·성향별 조회 화면이라 자연스럽지만, S5 가 매번 같은 화면으로 끝나면 단조롭다. 절차형 Case(DC-020·026·013)의 화면 순번이 이를 상쇄한다.
4. **bank_objective_포함 Hot Tip** — HT-048(6) · HT-035(4) · HT-006(3) 은 태그상 은행 목표(유치·득점)가 섞인 글이다. HD-7/G4 에 따라 **접촉 순서·화면 절차** 재료로만 쓰고 추천 사유로 쓰지 않는다. 특히 DC-026·024·025 의 이탈 계열에서 유의.
5. **T3-only 핵심 지식** — 15 후보의 Required Knowledge 에 T3 표기가 있다. 그중 핵심 판단이 T3 에 기대는 자리: DC-005(HT-045 세율 비교 — Seed 김서연 P0 와 동일 이슈) · DC-020(SC-002 화면번호 · KG-004 7/1 발급) · DC-036·009(OK-012 예외 상품 범위의 T3 나열) · DC-001(HT-001 3단 구성 · TALK-027 caution) · DC-024(TALK-014 STT) · DC-016(HT-043 환매 T+3) · DC-035(TALK-021 — Registry authority 가 T3 STT 정제본). Seed 의 HT-045 문제와 같은 종류이므로 §15-5 정책이 여기에도 적용된다.
6. **PRD 참조가 적은 것은 의도**다 — 제안은 «유형 수준» 이고 상품 확정은 고객·직원 몫(G1 · OK-017 Execution Eligibility). 상품 자체가 판단 대상인 DC-016(PRD 5)·DC-019(PRD 3)·DC-036(PRD 2)만 예외. Seed 3 의 «개별 상품 지정»(KODEX·RISE·OK저축은행 등 Registry 미등록)과 대비된다.
7. **Registry 미사용 영역** — OK 31 중 1종, SCR 91 중 46종, PRD 34 중 23종이 어떤 후보에도 안 쓰였다. 시황(SRC-092·093 · PRD-033/034 월간)과 ELB 청약(DC-017 만 사용)은 Scope 결정(§15-7·8)에 달렸다.

---

## 14. 중복 / 제거 후보

Round 5 에서 병합·제거한 Situation Idea 와, Candidate 36 안에서 판단축이 가까워 최종 15 에서 **둘 다 넣지 말 것**을 권하는 짝.

### 14.1 Candidate 에 올리지 않은 아이디어

| 아이디어 | 처리 | 이유 |
|---|---|---|
| 희망퇴직 특별퇴직금 · 퇴직 예정 리스트 | DC-001 에 흡수(note) | 근거가 T3 Hot Tip 뿐. 퇴직 전 Scope 자체가 §15-9 |
| 재만기 T+1 규칙(만기 상품 재만기 시 익일 반영) | DC-008 note | 단독으로는 «정보 한 줄» — Case 가 안 된다 |
| 실물이전 접수취소 · 전입 후 재이탈 비중(조사) | DC-027 note | 비중 수치는 이탈 조사 «비중»(등급 C)이라 개인 임계값이 아니다 |
| 자영업자 납입 중단 · 소득 불규칙 | 제거(WEAK) | 지식베이스에 근거 없음 |
| 중도인출 — 주택구입 사유 | 제거 | GC-14 와 동일 판단축 |
| 수익률 지표 차이(누적 vs 연환산) 문의 | 제거 | GC-21 과 동일 |
| CRM 권유사절 · 접촉 금지 | 제거 | GC-20 과 동일. 접촉 과잉 방지는 DC-013·014 가 다른 형태로 다룬다 |
| ETF 실시간 매매 불가로 인한 증권사 이탈 | 제거 | GC-16 과 동일 |
| 월분배 ETF 보유 · 개시 전 전량 매도 | 제거 | GC-11 / DIAG-02 와 거의 같다 |
| 상속 · 대리인 인출 | 제거 | 절차 원천 없음 · Demo 정서에 맞지 않음 |
| 배우자 IRP 명의 분산 납입 | DC-003 If 분기에 흡수 | 단독 Case 로는 «권유형» 으로 기운다 |
| 시황 자료 활용(금리 인하 전망 × 만기) | 보류 | golden P2 보류 항목과 같음 · Scope 미결(§15-7) |
| 법인대표 · 기업 IRP | 제거 | 개인형 IRP Demo 범위 밖 |
| ISA 60일 «동일 취급» 미확정 표기 | Seed 김서연 Open Question 으로만 | references 충돌 색인 항목 — Source Conflict 임의 해결 금지 |

### 14.2 Candidate 36 안의 근접 짝 (최종 15 에서 택1 권고)

| 짝 | 공통 판단축 | 권고 |
|---|---|---|
| DC-009 ↔ DC-036 | 위험자산 한도 초과 해소 경로 | DC-036 (복수 시한이 더 많은 능력을 보여줌) · DC-009 는 Digital 보강용 alt |
| DC-018 ↔ DC-022 | 만 55세 · 개시 여부 결정 | DC-018 (오해 정정형) 우선 · 결정 지원형이 더 필요하면 DC-022 |
| DC-010 ↔ DC-028 | OK-006 성향 상한 | 둘 다 가능하나 방향이 반대(상향 요청 vs 하향 보유) — 함께 넣을 때는 «상한 규칙» 이 Demo 의 반복 트릭이 되지 않게 배치 |
| DC-010 ↔ DC-032 | 실행 제약 | 성향 제약(DC-010) vs 채널 제약(DC-032) — 택1 |
| DC-013 ↔ DC-014 | 접촉 불필요(리스트 오탐) | 둘 다 유지 권고 — 오탐 원인이 다르다(입금사유 vs 예약 완료). 15 가 빠듯하면 DC-013 |
| DC-024 ↔ DC-025 ↔ DC-026 | 이탈·이전 | DC-026 우선(절차 존중). 이탈 사유형은 DC-024(대출) 또는 DC-025(수수료) 택1 |
| DC-006 ↔ DC-007 | 타사 연금저축 이전 | 개시 전(DC-006) vs 개시 후 0원 이전(DC-007) — 택1 |
| DC-001 ↔ DC-002 ↔ 박정호 | 퇴직 전후 | 3부작으로 함께 쓸 수 있으나 Scope(§15-9) 결정 전에는 DC-002 만 확정 |
| DC-031 ↔ DC-019 | 정기예금 만기 재운용 | DC-019 (판단이 더 많다) · DC-031 은 시점 의존 표시의 예시로 Chat 에 흡수 가능 |
| DC-030 ↔ DC-002 | DO 2주 창 | DC-002 (발화 결합) · DC-030 은 LMS 안내형이라 Demo 화면 밀도가 낮다 |

---

## 15. 최종 15개 선정 시 Human Decision 이 필요한 사항

1. **Negative / Preservation Case 수** — Shortlist 20 에 현 상태 유지 4 · 실행 제약 2 · 확인 우선 4 가 있다. 최종 15 에서 «아무것도 하지 않는 게 정답» 인 Case 를 몇 개까지 발표에 올릴지(권고 ≥ 3).
2. **이탈 Case 수** — 골든 GC 군이 이탈을 이미 다루고 있어 Shortlist 는 DC-026 하나만 이탈 ◎ 이다. Demo 15 에 이탈 사유형(DC-024 대출 / DC-025 수수료)을 추가할지.
3. **연금수령기 Case 포함** — DC-021(자유인출 · 1,500만) · DC-007(개시 후 0원 이전)은 수령 중 고객이다. 사후관리 Demo 의 범위를 «수령 중» 까지 넓힐지.
4. **Seed 3 의 처리** — 김서연 IMPROVE · 이수민 KEEP · 박정호 IMPROVE. 15 안에 Seed 를 넣을지, 넣는다면 P0 충돌(환급액 · T3 세율 · 감면율 2단/3단)을 «HTML 값 보존» 과 «Registry 기준» 중 어느 쪽으로 고칠지. Seed 파일 수정은 이번 작업에서 하지 않았다.
5. **T3-only 지식의 화면 노출 정책** — HT-045(세율) · HT-001(3단 구성) · TALK-021(72의 법칙) · OK-009 의 T3 부분처럼 공식 근거가 없는 지식을 S3/S4 에 «확인 전» 라벨로 올릴지, Chat 근거 칸으로만 내릴지. DC-001·020·035 와 Seed 김서연·박정호가 영향을 받는다.
6. **Source Conflict 의 노출 방식** — DC-019 는 SC-001(예금자보호 5천만 vs 1억)을 «미확정 · 확인 후 안내» 로 화면에 드러낸다. 발표에서 미해결 충돌을 보여주는 것이 신뢰 표시인지 약점인지.
7. **HTML Dashboard-only Theme 의 재사용 범위** — 15명의 Theme(예: TDF 빈티지 불일치 · 초저위험 사전지정 · 성과저조)을 Candidate 로 옮길 때 8월 11일 기준 dormant 수치와 내부 충돌(C-11·C-12)은 버렸다. 그 Theme 을 Demo 에 다시 세울지, 세우면 어느 데이터 기준일로 할지. 시황 활용(금리 인하 전망 × 만기)은 골든 P2 보류와 같이 보류했다.
8. **신규 축의 포함** — AI투자일임(DC-015 · OK-027) · ELB 청약/만기(DC-017 · OK-011) 는 기존 GC 에 없는 축이다. Demo 가 다루는 상품 범위에 넣을지.
9. **퇴직 전 단계 Scope** — DC-001(퇴직 예정 · DC 예금 만기)은 골든 작업에서 «마케팅 성격» 으로 제외됐던 영역이다. 사후관리 Demo 에 «퇴직 전 준비» 를 넣을지. 넣으면 박정호·DC-002 와 3부작이 된다.
10. **골든 GC Pair 의 활용** — DC-006 ↔ GC-15 · DC-002 ↔ GC-03 · DC-011 ↔ GC-04 · DC-018 ↔ GC-10 은 기존 Case 의 «변주» 다. Demo 에서 GC 와 짝으로 보여줄지(«같은 규칙, 다른 판단»), 독립 Case 로만 쓸지. 짝으로 쓰면 golden/ 의 canonical 구조를 demo/ 가 참조하게 된다.

---

> 다음 단계(별도 작업): Human Review → 최종 15 선정 → 고객 상세 설계(이름 · 금액 · 날짜) → S1~S5 · Chat 완성 → Seed 3 의 P0/P1 정리. 이 문서는 그 입력이며, `demo/` 의 다른 파일과 `knowledge/`·`sources/`·`golden/`·`cases/`·`design/`·`prototype/`·`references/` 는 변경하지 않았다.
