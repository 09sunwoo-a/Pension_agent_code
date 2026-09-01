# DEMO-A — Minimal End-to-End Mock v0 RUN

- 실행: 2026-09-01T04:29:21 / model gemma-4-31b-it / git 9e8db6ce5 / status **SUCCESS**
- LLM Call: decision-level 3 + selection prune 2 = 총 5

## 1. Raw Input → Canonical Evidence
- Raw: `prototype/mock/DEMO-A_raw.json` (합성 고객 — 의미 라벨 없음)
- Canonical: E-item 20건 / Derived 4건 (기존 canonical.py 검증 통과)
  - [D001] 최근 30일 전체 평가금액 증감: +800,000원 (69,200,000원 → 70,000,000원)
  - [D002] 만기 시한: 시중은행 정기예금 (1년제) 20,000,000원 만기 2027-05-15 → D-256
  - [D003] 만기 시한: 타행 ISA 80,000,000원 만기 2026-09-26 → D-25
  - [D004] 연금개시요건 충족 여부: 미충족 (만 51세, 가입 8.4년, 퇴직급여 포함 N) | rule_source=만55세 이상 + 가입 5년 이상(퇴직급여 포함 시 55세만) — 행내 공식 기준 | rule_as_of=2026-09-01 | rule_id=PENSION-OPEN-01
- Hard Constraint: 투자성향 위험중립형 → 허용 ['안정형', '안정추구형', '위험중립형'] / 금지 ['적극투자형', '공격투자형']

## 2. CALL 1 — LLM Knowledge Need Generation
- KN-D01 [tax_confirmation] IRP 개인부담금 세액공제 한도 및 소득 수준별 공제율 기준 확인 (keywords: 세액공제, IRP한도, 납입한도, 소득기준)
- KN-D02 [procedure_confirmation] ISA 만기 자금의 IRP 전환 입금 절차 및 전환 시 추가 세액공제 혜택 확인 (keywords: ISA만기, IRP전환, 전환입금, 추가공제)

## 3. Hybrid Knowledge Selection
- deterministic 후보: ['OK-008', 'OK-001']
- LLM prune: keep ['OK-008', 'OK-001'] / removed [] / fallback None
- 최종 K-001 [OK] OK-008 (need KN-D01)
- 최종 K-002 [OK] OK-001 (need KN-D02)

## 4. CALL 2 — Management Judgment / Direction / Product Need
- judgment: **개입 필요 / 추가 확인 우선**
- reasoning: IRP 내 상당액의 현금성 자산(2,000만원)이 방치되어 있으며[E201], 단기간 내 타행 ISA 만기(D-25)라는 주요 자금 이벤트가 예정되어 있음[D003]. 또한 고객이 직접 세액공제 콘텐츠를 조회[E603]하는 등 명확한 관심 신호가 포착되었으므로, ISA 만기자금 전환을 통한 세액공제 혜택 안내 및 미운용 자산의 포트폴리오 재구성이 필요한 시점임.
- required_confirmation: ['원천징수영수증 상의 결정세액 확인 (세액공제 실효성 판단 근거, K-001)', '타행 ISA 만기자금의 IRP 전환 입금 의사 및 규모 확인 (K-002)']
- direction: [] → ISA 만기자금의 IRP 전환 입금을 통한 추가 세액공제 혜택(전환금액 10%, 최대 300만원) 안내 및 절차 지원 (K-002)
- direction: [] → IRP 내 현금성 자산(2,000만원)에 대해 고객의 투자성향(위험중립형) 및 허용 위험등급(4~6등급)에 부합하는 상품으로의 재운용 제안 (E104, C1, C2)
- direction: [결정세액이 공제 예상액보다 적을 경우] → 단순 납입보다는 실효 공제액을 고려한 최적 납입 금액 가이드 제공 (K-001)
- product_need: {"needed": true, "solution_types": [{"solution_type": "미운용 현금 및 ISA 전환자금 운용", "characteristics": ["TDF", "채권형", "정기예금", "GIC"], "maturity": ""}]}

## 5. Hybrid Product Candidate Selection
- deterministic pool: ['P01 KB 온국민 TDF 시리즈', 'P02 신한 마음편한 TDF 시리즈', 'P03 한화 LIFEPLUS TDF 시리즈', 'P04 마이다스 기본 TDF 시리즈', 'P05 키움 더드림 단기채', 'P06 한국투자 크레딧 포커스 ESG', 'P07 교보악사 Tomorrow 장기우량K-1호', 'P08 DB손해보험 무배당 스마트 퇴직연금 이율보증형…', 'P09 KB손해보험 퇴직연금 이율보증형보험(DC/IRP,3년…', 'P10 무배당 메리츠화재 이율보증형보험3(개인형IRP,3년)', 'P11 무배당 메리츠화재 이율보증형보험3(개인형IRP,5년)', 'P12 무배당 한화생명 신탁계공용 이율보증형 3년 퇴직적…', 'P13 KB손해보험 퇴직연금 이율보증형보험(DC/IRP,2년…', 'P14 무배당 교보생명 신탁계공용 이율보증형보험(DC/IR…)']
- LLM prune keep: ['P04', 'P05', 'P06', 'P07', 'P08', 'P11', 'P13'] / removed ['P01', 'P02', 'P03', 'P09', 'P10', 'P12', 'P14'] / fallback None
- 최종 Pool: ['P04 마이다스 기본 TDF 시리즈', 'P05 키움 더드림 단기채', 'P06 한국투자 크레딧 포커스 ESG', 'P07 교보악사 Tomorrow 장기우량K-1호', 'P08 DB손해보험 무배당 스마트 퇴직연금 이율보증형…', 'P11 무배당 메리츠화재 이율보증형보험3(개인형IRP,5년)', 'P13 KB손해보험 퇴직연금 이율보증형보험(DC/IRP,2년…']

## 6. CALL 3 — Final Employee Brief (S1~S5)
### S1
고객님은 현재 IRP에 7,000만원을 보유 중이며, 이 중 2,000만원은 입금 이후 추가 매매나 운용지시가 확인되지 않은 현금성 자산 상태입니다. 최근 스타뱅킹을 통해 IRP 수익률과 세액공제 관련 내용을 여러 차례 조회하셨으며, 특히 9월 26일에 타행 ISA 계좌의 만기(8,000만원)가 예정되어 있어 세제 혜택에 관심이 높으신 상황으로 보입니다. 지난 4월 상담 시에도 연말 여유자금 가능성을 언급하신 기록이 있습니다.
### S2
25일 후 도래하는 ISA 만기자금의 IRP 전환을 통한 세액공제 극대화와 IRP 내 미운용 자산 2,000만원의 효율적 운용을 지원하는 것이 핵심입니다.
- 상담 전 확인: ['단말에서 고객의 연금계좌 납입 가능 잔여한도 및 세액공제 잔여한도 확인', '현재 가입 가능한 퇴직연금 상품 라인업 및 판매 가능 여부 확인']
- 고객과 확인: ['원천징수영수증 상의 결정세액 확인 (실효 공제액 판단 목적)', '타행 ISA 만기자금을 IRP로 전환하여 입금하실 의사가 있는지 확인']
### S3
- [] ISA 만기자금의 IRP 전환 입금 안내 및 지원 / 세제 혜택 안내 및 입금 절차 지원 (risk: 해당없음)
- [] 현금성 자산의 포트폴리오 재구성을 통한 재운용 / 투자성향 부합 상품 제안 (risk: 위험중립형)
- [결정세액이 낮아 전액 공제가 어려운 경우] 실효 공제액을 고려한 납입 금액 조정 안내 / 납입 금액 최적화 가이드 (risk: 해당없음)
- 후보 P04: 고객의 투자성향(위험중립형)에 부합하는 보통위험(4등급) 상품이며, 이미 일부 보유 중인 TDF 상품으로 운용 경험이 있어 추가 비중 확대에 적합함
- 후보 P08: 원리금보장상품을 선호하거나 안정적인 수익을 추구하는 경우 적합하며, 위험중립형 성향 내에서 안정적인 자산 배분 수단으로 활용 가능
### S4
> 고객님, 최근에 앱으로 연금 세액공제 내용을 살펴보신 것 같아 도움을 드리고자 연락드렸습니다. 마침 9월 26일에 만기가 되시는 타행 ISA 자금 8,000만원이 있으신데, 이 자금을 만기 후 60일 이내에 IRP로 전환하시면 기존 한도 외에 추가로 최대 300만원까지 세액공제 혜택을 더 받으실 수 있습니다.
> 또한, 현재 IRP 계좌에 운용 지시가 되지 않은 현금성 자산 2,000만원이 있으신데요. 고객님의 위험중립형 성향에 맞춰, 기존에 보유하신 마이다스 기본 TDF(P04)의 비중을 높이시거나, 안정적인 이율보증형 보험(P08) 등으로 운용하여 효율을 높여보시는 것을 추천드립니다.
> 다만, 실제로 세액공제를 얼마나 환급받으실 수 있는지는 원천징수영수증상의 '결정세액'에 따라 달라질 수 있습니다. 정확한 혜택 금액을 확인해 드릴 수 있도록 영수증 내용을 함께 살펴봐도 될까요?
> [if 원금 손실에 대한 우려를 표하는 경우] 그렇다면 위험등급이 매우 낮은 채권형 펀드(P05)나 원리금보장형 상품인 GIC(P08) 위주로 구성하여 안정성을 높이는 방향으로 안내해 드리겠습니다.
> [if ISA 전환 입금 절차가 복잡하다고 느끼는 경우] 타행에서 해지하신 후 저희 은행 IRP로 입금만 하시면 전산으로 확인이 가능하여 별도의 증빙서류 없이 편리하게 처리하실 수 있도록 도와드리겠습니다.
### S5
- tips: [{'tip_id': 'T01', 'why_relevant': '타행 ISA 만기자금의 IRP 전환 입금 시 증빙서류 불필요 및 추가 세액공제 혜택에 대한 실무적 안내 근거로 활용'}] / screens: [{'screen_id': 'S01', 'purpose_here': '고객의 세금우대 관련 조회 및 ISA 전환 가능 금액 확인'}, {'screen_id': 'S02', 'purpose_here': 'ISA 만기자금 입금 처리 시 입금가능금액 자동조회 및 실행'}, {'screen_id': 'S03', 'purpose_here': '당해년도 개인부담금 납입 가능 한도 확인 및 변경'}, {'screen_id': 'S04', 'purpose_here': '재운용 제안 상품(P04, P08 등)의 현재 판매 가능 여부 최종 확인'}, {'screen_id': 'S05', 'purpose_here': '고객이 직접 비대면으로 ISA 만기자금을 입금할 수 있도록 경로 안내'}]

## 7. Validators
- schema_errors: PASS(없음)
- validation: PASS
- validation_c2: PASS
- validation_c3: PASS
- validation_forbidden_words: PASS
- validation_evidence_ids: PASS
- validation_supply_refs: PASS
- validation_screen_refs: PASS
- validation_latex: PASS
