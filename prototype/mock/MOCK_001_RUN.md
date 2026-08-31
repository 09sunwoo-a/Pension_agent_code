# MOCK_001 — Minimal End-to-End Mock v0 RUN

- 실행: 2026-08-31T19:01:31 / model gemma-4-31b-it / git 41d8010ed / status **SUCCESS**
- LLM Call: decision-level 3 + selection prune 2 = 총 5

## 1. Raw Input → Canonical Evidence
- Raw: `prototype/mock/MOCK_001_raw.json` (합성 고객 — 의미 라벨 없음)
- Canonical: E-item 18건 / Derived 6건 (기존 canonical.py 검증 통과)
  - [D001] 입금 경과일: 2026-08-08 30,000,000원 (사유: 타 금융기관 IRP 계약이전 입금) → 기준일까지 20일 경과
  - [D002] 최근 30일 현금성자산 증감: +30,000,000원 (0원 → 30,000,000원)
  - [D003] 최근 30일 전체 평가금액 증감: +30,000,000원 (28,000,000원 → 58,000,000원)
  - [D004] 현재 현금성자산 30,000,000원은 2026-08-08 '타 금융기관 IRP 계약이전 입금' 입금액과 금액이 일치한다 (산술 대조)
  - [D005] 만기 시한: KB퇴직연금 정기예금 (2년제) 20,000,000원 만기 2027-04-10 → D-225
  - [D006] 연금개시요건 충족 여부: 미충족 (만 47세, 가입 7.5년, 퇴직급여 포함 N) | rule_source=만55세 이상 + 가입 5년 이상(퇴직급여 포함 시 55세만) — 행내 공식 기준 | rule_as_of=2026-08-28 | rule_id=PENSION-OPEN-01
- Hard Constraint: 투자성향 위험중립형 → 허용 ['안정형', '안정추구형', '위험중립형'] / 금지 ['적극투자형', '공격투자형']

## 2. CALL 1 — LLM Knowledge Need Generation
- KN-M01 [rule_confirmation] 타 금융기관 IRP 계약이전 입금액에 대한 디폴트옵션 적용 시한 및 운용 규칙 확인 (keywords: 계약이전, 디폴트옵션, 현금성자산, 운용규칙)
- KN-M02 [procedure_confirmation] IRP 계좌 내 현금성자산을 이용한 상품 매수 및 교체 매매의 디지털 실행 경로 확인 (keywords: IRP, 상품매수, TDF, 펀드, 실행경로)

## 3. Hybrid Knowledge Selection
- deterministic 후보: ['OK-002', 'OK-003', 'OK-004', 'OK-005', 'KG-002', 'OK-012']
- LLM prune: keep ['OK-003', 'OK-004', 'OK-005', 'KG-002', 'OK-012'] / removed ['OK-002'] / fallback None
- 최종 K-001 [OK] OK-003 (need KN-M01)
- 최종 K-002 [OK] OK-004 (need KN-M01)
- 최종 K-003 [OK] OK-005 (need KN-M01)
- 최종 K-004 [KG] KG-002 (need KN-M01)
- 최종 K-005 [OK] OK-012 (need KN-M02)

## 4. CALL 2 — Management Judgment / Direction / Product Need
- judgment: **개입 필요 / 정보 안내 중심**
- reasoning: 타사 이전 입금액 3,000만원이 디폴트옵션 미등록(E009)으로 인해 현금성자산으로 대기 중이며(D004, K-003), 최근 상품 조회 행동(E014~E016)이 관찰되어 적절한 운용 방향 안내 및 제도적 보완(DO 등록)이 필요함.
- required_confirmation: ['현금성자산 30,000,000원에 대한 구체적인 운용 의사 및 상품 선호도 확인', '디폴트옵션 사전지정운용제도 등록 의사 확인']
- direction: [고객이 직접 상품을 선택하여 운용하고자 하는 경우] → 투자성향(위험중립형) 및 펀드 위험등급 제한(4~6등급) 범위 내에서 적절한 상품 매수 안내
- direction: [운용 상품 결정에 어려움을 느끼거나 자동 운용을 원하는 경우] → 디폴트옵션 제도를 안내하고, 가입 가능 포트폴리오(지켜드림, 알파드림, 뿔려드림) 중 선택 및 등록 지원
- product_need: {"needed": true, "solution_types": [{"solution_type": "직접 운용 지원", "characteristics": ["TDF", "채권형 펀드", "정기예금", "GIC"], "maturity": ""}, {"solution_type": "디폴트옵션 적용", "characteristics": ["초저위험(지켜드림)", "저위험(알파드림)", "중위험(뿔려드림)"], "maturity": ""}]}

## 5. Hybrid Product Candidate Selection
- deterministic pool: ['P01 KB 온국민 TDF 시리즈', 'P02 신한 마음편한 TDF 시리즈', 'P03 한화 LIFEPLUS TDF 시리즈', 'P04 마이다스 기본 TDF 시리즈', 'P05 DB손해보험 무배당 스마트 퇴직연금 이율보증형…', 'P06 KB손해보험 퇴직연금 이율보증형보험(DC/IRP,3년…', 'P07 무배당 메리츠화재 이율보증형보험3(개인형IRP,3년)', 'P08 무배당 메리츠화재 이율보증형보험3(개인형IRP,5년)', 'P09 무배당 한화생명 신탁계공용 이율보증형 3년 퇴직적…', 'P10 KB손해보험 퇴직연금 이율보증형보험(DC/IRP,2년…', 'P11 무배당 교보생명 신탁계공용 이율보증형보험(DC/IR…)']
- LLM prune keep: ['P01', 'P04', 'P05', 'P08', 'P10'] / removed ['P02', 'P03', 'P06', 'P07', 'P09', 'P11'] / fallback None
- 최종 Pool: ['P01 KB 온국민 TDF 시리즈', 'P04 마이다스 기본 TDF 시리즈', 'P05 DB손해보험 무배당 스마트 퇴직연금 이율보증형…', 'P08 무배당 메리츠화재 이율보증형보험3(개인형IRP,5년)', 'P10 KB손해보험 퇴직연금 이율보증형보험(DC/IRP,2년…']

## 6. CALL 3 — Final Employee Brief (S1~S5)
### S1
2026년 8월 8일 타사 IRP 계약이전으로 3,000만원이 입금되었으나, 현재 디폴트옵션이 미등록된 상태여서 해당 금액이 운용지시 없이 현금성자산으로 보유 중입니다. 최근 고객님께서 스타뱅킹을 통해 수익률과 펀드, 특히 TDF 상품 상세 화면을 조회하신 이력이 확인되어 자산 운용에 관심이 높으신 상황으로 보입니다.
### S2
이전 입금된 3,000만원이 현금성 상태로 대기 중인 상황에서 고객의 상품 탐색 행동이 포착되었으므로, 직접 운용 또는 디폴트옵션 등록 등 적절한 운용 방향을 안내하는 것이 핵심입니다.
- 상담 전 확인: ['단말에서 현금성자산의 정확한 잔액과 현재 수익률 현황 확인']
- 고객과 확인: ['입금된 3,000만원에 대한 구체적인 운용 계획 및 디폴트옵션 등록 의사 확인']
### S3
- [고객이 직접 상품을 선택하여 운용하고자 하는 경우] 위험중립형 성향에 적합한 상품 매수 안내 / TDF 및 펀드 매수 (risk: 위험중립형)
- [운용 상품 결정에 어려움을 느끼거나 자동 운용을 원하는 경우] 디폴트옵션 등록 지원 / 디폴트옵션 포트폴리오 지정 (risk: 해당없음)
- 후보 P04: 고객의 TDF 상품 조회 행동이 확인되었으며, 위험등급 4등급(보통)으로 고객의 투자성향(위험중립형) 범위 내에서 운용 가능함; 은퇴 시점에 맞춘 글로벌 자산배분 특성이 IRP 장기 운용 목적에 적합함
- 후보 P10: 원리금 보장 상품을 선호할 경우, 2년 계약기간의 이율보증형보험으로 안정적인 운용 가능
### S4
> 고객님, 지난 8월 8일에 타사에서 IRP 3,000만원을 이전해 오셨는데, 현재 이 자금이 별도의 운용지시 없이 현금성자산으로 보유되어 있어 안내차 연락드렸습니다.
> 최근 앱에서 TDF 상품 등을 살펴보신 것으로 보이는데, 혹시 이번에 이전하신 자금에 대해 생각하고 계신 운용 방향이나 특별히 선호하시는 상품군이 있으실까요?
> [if 직접 운용을 희망하는 경우] 고객님의 위험중립형 투자성향에 적합하면서도, 은퇴 시점에 맞춰 자동으로 자산비중을 조절해 주는 TDF 상품(P04 등)을 검토해 보시는 것을 추천드립니다.
> [if 상품 선택이 어렵거나 자동 운용을 원하는 경우] 어떤 상품을 고를지 고민되신다면, 미리 정해진 포트폴리오로 자동 운용되는 '디폴트옵션' 제도를 활용해 보시는 것이 좋습니다. 고객님은 '지켜드림', '알파드림', '뿔려드림' 세 가지 포트폴리오 중 하나를 선택해 등록하실 수 있습니다.
### S5
- tips: [] / screens: [{'screen_id': 'S01', 'purpose_here': '고객의 현재 현금성자산 규모 및 전체 운용 현황을 정확히 점검하기 위함'}, {'screen_id': 'S02', 'purpose_here': '고객이 직접 상품을 선택할 경우 매수 실행을 지원하기 위함'}]

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
