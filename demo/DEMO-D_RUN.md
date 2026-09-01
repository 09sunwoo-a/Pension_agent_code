# DEMO-D — Minimal End-to-End Mock v0 RUN

- 실행: 2026-09-01T04:45:43 / model gemma-4-31b-it / git 42872dedf / status **SUCCESS**
- LLM Call: decision-level 3 + selection prune 2 = 총 5

## 1. Raw Input → Canonical Evidence
- Raw: `prototype/mock/DEMO-D_raw.json` (합성 고객 — 의미 라벨 없음)
- Canonical: E-item 17건 / Derived 5건 (기존 canonical.py 검증 통과)
  - [D001] 입금 경과일: 2026-07-28 60,000,000원 (사유: 정기예금 만기상환 — 현금성자산 대체) → 기준일까지 35일 경과
  - [D002] 최근 30일 전체 평가금액 증감: +700,000원 (91,300,000원 → 92,000,000원)
  - [D003] 현재 현금성자산 60,000,000원은 2026-07-28 '정기예금 만기상환 — 현금성자산 대체' 입금액과 금액이 일치한다 (산술 대조)
  - [D004] 디폴트옵션 적용 예상 기준일: 2026-09-08 (만기 2026-07-28 + 6주), 도래까지 7일 | rule_source=최초입금 2주 / 만기 4+2주 — 행내 기준 | rule_as_of=2026-09-01 | rule_id=DO-CLOCK-01
  - [D005] 연금개시요건 충족 여부: 미충족 (만 49세, 가입 9.0년, 퇴직급여 포함 N) | rule_source=만55세 이상 + 가입 5년 이상(퇴직급여 포함 시 55세만) — 행내 공식 기준 | rule_as_of=2026-09-01 | rule_id=PENSION-OPEN-01
- Hard Constraint: 투자성향 위험중립형 → 허용 ['안정형', '안정추구형', '위험중립형'] / 금지 ['적극투자형', '공격투자형']

## 2. CALL 1 — LLM Knowledge Need Generation
- KN-D01 [rule_confirmation] 디폴트옵션(사전지정운용제도)의 적용 시점 및 실행 전 운용지시 변경 가능 기한 확인 (keywords: 디폴트옵션, 사전지정운용, 적용시점, 운용지시, 실행기한)
- KN-D02 [execution_path_confirmation] IRP 계좌 내 현금성 자산의 상품 매수 및 운용지시 변경을 위한 스타뱅킹 내 실행 경로 확인 (keywords: IRP, 상품매수, 운용지시, 스타뱅킹, 실행경로)
- KN-D03 [rule_confirmation] IRP 계좌 내 TDF 등 실적배당형 상품의 투자 한도 및 위험자산 편입 제한 비율 확인 (keywords: IRP, TDF, 위험자산한도, 투자제한, 실적배당형)

## 3. Hybrid Knowledge Selection
- deterministic 후보: ['OK-005', 'OK-004', 'OK-012']
- LLM prune: keep ['OK-005', 'OK-012'] / removed ['OK-004'] / fallback None
- 최종 K-001 [OK] OK-005 (need KN-D01)
- 최종 K-002 [SYNTH_GAP] GAP(KN-D02) (need KN-D02)
- 최종 K-003 [OK] OK-012 (need KN-D03)

## 4. CALL 2 — Management Judgment / Direction / Product Need
- judgment: **개입 필요 / 추가 확인 우선**
- reasoning: 고액의 현금성 자산(6,000만 원)이 디폴트옵션 자동 실행 예정일(2026-09-08)을 7일 앞두고 있으며[E801, D004], 최근 TDF 상품 조회 등의 행동 신호[E603]가 관찰되어, 고객의 실제 운용 의사를 확인하고 적절한 상품 선택을 지원할 필요가 있음.
- required_confirmation: ['디폴트옵션(초저위험) 자동 매수 전, TDF 또는 다른 위험수준의 상품으로 운용 변경을 원하는지 여부']
- direction: [고객이 자발적인 운용 변경 의사를 밝힌 경우] → 투자성향(위험중립형) 내에서 허용되는 TDF 또는 상위 등급 디폴트옵션 포트폴리오 등으로의 교체매매 및 운용지시 지원
- direction: [특별한 운용 의사가 없거나 안내만 원하는 경우] → 현재 설정된 디폴트옵션의 실행 예정 내용 및 일정 안내
- product_need: {"needed": true, "solution_types": [{"solution_type": "자발적 운용 변경 및 포트폴리오 다변화", "characteristics": ["TDF", "채권형 펀드"], "maturity": ""}, {"solution_type": "사전지정운용제도 변경을 통한 자동매수 상품 조정", "characteristics": ["알파드림", "뿔려드림"], "maturity": ""}]}

## 5. Hybrid Product Candidate Selection
- deterministic pool: ['P01 KB 온국민 TDF 시리즈', 'P02 신한 마음편한 TDF 시리즈', 'P03 한화 LIFEPLUS TDF 시리즈', 'P04 마이다스 기본 TDF 시리즈']
- LLM prune keep: ['P01', 'P04'] / removed ['P02', 'P03'] / fallback None
- 최종 Pool: ['P01 KB 온국민 TDF 시리즈', 'P04 마이다스 기본 TDF 시리즈']

## 6. CALL 3 — Final Employee Brief (S1~S5)
### S1
지난 7월 28일 정기예금 만기로 발생한 6,000만 원이 현재 운용지시 없이 현금성 자산으로 대기 중입니다. 이 자금은 사전 지정하신 'KB 디폴트옵션 초저위험 지켜드림' 상품으로 9월 8일에 자동 매수될 예정이며, 최근 고객님께서 스타뱅킹을 통해 TDF 상품 상세 화면 등을 조회하신 이력이 확인됩니다.
### S2
9월 8일 디폴트옵션 자동 실행 전, 고객님의 실제 운용 의사를 확인하여 초저위험 상품 자동 매수 전 투자성향에 맞는 최적의 운용 방향을 지원하는 것이 핵심입니다.
- 상담 전 확인: ['단말에서 디폴트옵션 실제 실행예정내역 및 대상 자금 재확인', 'TDF 후보 상품의 현재 판매 가능 여부 확인']
- 고객과 확인: ['초저위험 디폴트옵션 자동 매수 전, TDF 또는 다른 위험수준의 상품으로 운용 변경을 원하시는지 여부']
### S3
- [고객이 운용 변경 의사를 밝힌 경우] 재운용 / TDF 또는 상위 등급 디폴트옵션 포트폴리오 교체매매 (risk: 위험중립형)
- [특별한 운용 의사가 없는 경우] 유지 / 현재 디폴트옵션 실행 일정 안내 (risk: 해당없음)
- 후보 P04: 고객의 투자성향(위험중립형) 내 허용되는 위험등급(4등급) 상품이며, 최근 고객이 TDF 상품을 직접 조회한 관심 신호가 관찰되어 적합함
### S4
> 고객님, 지난 7월 28일에 만기 되신 정기예금 6,000만 원이 현재 운용지시 없이 대기 중입니다. 이 자금은 사전 지정하신 '초저위험 지켜드림' 상품으로 9월 8일에 자동 매수될 예정인데요. 최근에 TDF 상품 등을 살펴보신 것으로 보여, 자동 매수 전에 혹시 다른 상품으로 운용 방향을 변경하고 싶으신지 여쭤보고자 연락드렸습니다.
> [if 운용 변경을 원하는 경우] 고객님의 위험중립형 투자성향과 최근 TDF에 관심을 가지신 점을 고려했을 때, 은퇴 시점에 맞춰 자산 비중을 조절해주는 TDF 상품들이 좋은 대안이 될 수 있습니다. 구체적인 상품 내용을 함께 살펴보시겠습니까?
> [if 현재 상태 유지 또는 안내만 원하는 경우] 네, 알겠습니다. 그럼 별도의 운용지시가 없으시면 예정대로 9월 8일에 '초저위험 지켜드림' 상품으로 운용이 시작될 예정입니다.
### S5
- tips: [{'tip_id': 'T01', 'why_relevant': '디폴트옵션의 신뢰도를 높이고 고객이 직접 투자성향에 맞는 상품을 선택하도록 주도권을 부여하는 화법으로 활용 가능'}, {'tip_id': 'T03', 'why_relevant': 'TDF 권유 시 고객의 투자성향과 은퇴년도를 고려하여 제안하는 노하우 적용'}] / screens: [{'screen_id': 'S01', 'purpose_here': '디폴트옵션 실행예정내역 및 대상 금액 최종 확인'}, {'screen_id': 'S04', 'purpose_here': '제안할 TDF 상품의 실시간 판매 가능 여부 확인'}, {'screen_id': 'S02', 'purpose_here': '고객이 직접 운용을 결정할 경우 자동 매수 전 대기자금 처리'}]

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
