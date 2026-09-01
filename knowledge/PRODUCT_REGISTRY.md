# Product Registry (PRD-xxx)

- 내용: 상품 카드 재료 — `design/CANONICAL_CONTRACTS.md` §2.1 ProductCandidate 필드와 정합.
- 공통 규칙: `knowledge/README.md` §2~§6. 수익률 등 시점 값은 **as-of 필수**.

## 항목 스키마

```markdown
### PRD-xxx. <상품명>

| 필드 | 값 | 비고 |
|---|---|---|
| source | SRC-xxx §<위치> | |
| authority | (README §4) | |
| as_of | 수익률 기준일 등 | |
| status | ACTIVE / PROVISIONAL / ... | |
| delivered_for | REQ-xxx (해당 시) | |
| registered | YYYY-MM-DD | |

**ProductCandidate 재료** (canonical.json supply 구성용 — 필드명은 계약과 동일. `product_id`는 Case-local이므로 A가 부여):

​```json
{
  "name": "",                  // 원천 표기 그대로
  "product_type": "",          // TDF | 채권형 | 인컴형 | 정기예금 | GIC | ETF | ...
  "risk_grade": 0,             // 1~6 — 원천에 명시된 값만 (C2 검증 대상)
  "risk_level_label": "",
  "return_recent": 0.0,        // 소수 표기 (7.2% → 0.072)
  "return_period": "",         // 1Y / 3M / 3Y 등 — 원천의 측정기간
  "return_as_of": "",          // 수익률 기준일 — 원천에 명시된 값만
  "features": "",              // 원천 서술 기반 — 창작 금지
  "fee_note": "",              // 원천에 있을 때만
  "maturity_note": null,       // 원리금보장형 등 해당 시
  "sellable": null,            // 원천에서 판매 가능 여부 확인된 경우만 true/false. 미확인 = null + 아래 Unconfirmed에 기재
  "channels": []               // 원천에서 확인된 채널만
}
​```

**Unconfirmed** (원천에서 확인하지 못한 필드와 사유 — A/Human이 별도 확인해야 사용 가능):
- 예: sellable — SRC-xxx에 판매중단 여부 표기 없음
```

### 기재 규칙 (PRD 전용)

1. **원천에 없는 필드 값을 만들지 않는다** — risk_grade·수익률·보수는 원천 명시 값만, 없으면 Unconfirmed로 남긴다.
2. 수익률은 측정기간(return_period)·기준일(return_as_of) 없이 단독 기재하지 않는다. 기준일 불명이면 status=PROVISIONAL.
3. 추천사유는 이 Registry에 없다 — Agent(A)가 Case에서 생성한다(CANONICAL_CONTRACTS §2.1).
4. "미끼용" 여부 등 Case 설계상 역할 지정은 A 몫 — B는 실제 상품 사실만 기재한다.
5. 같은 상품의 수익률이 자료마다 다르면(기준일 차이) 최신만 남기지 말고 각 as-of를 병기하거나 별도 항목·SC 기록으로 보존한다.

---

## 일괄 기재 규칙 (2026-08-31 등록분)

- **risk_grade 숫자**: 원천(SRC-095)은 라벨(매우낮은/낮은/보통/다소높은/높은)로 표기 — 숫자는 HD-2.1 공식 등급 어휘(1 매우높은위험 · 2 높은위험 · 3 다소높은위험 · 4 보통위험 · 5 낮은위험 · 6 매우낮은위험)로 결정적 변환. 라벨은 risk_level_label에 원문 그대로 보존.
- **return_recent**: 원문 %값을 소수로 변환(12.58% → 0.1258). 음수 가능. SRC-095 수익률의 return_as_of = 2026-07-30, TDF 시리즈는 2030 빈티지 수익률 기준.
- **sellable·channels**: 전 항목 원천 미확인(null·[]) — SRC-095는 '추천펀드' 자료로 판매중 상품으로 추정 가능하나 판매상태 필드가 원천에 없어 기재하지 않음. A/Human이 확인 후 supply에 채울 것.
- **Product Fit ≠ Execution Eligibility (DB-003 §5, Human Decision)**: sellable/channels가 null인 상품은 **판매·채널 실행가능성을 확정하지 않는다.** 이 Registry의 상품 정보는 Customer–Product Fit 판단 재료까지만이며, 실제 가입·매수 실행 가능 여부(판매중·채널·한도소진 등)는 별도 확인 사항이다 — 실행 가능을 전제로 한 서술·추천 금지.
- **Metadata는 Source-backed intrinsic characteristic만 (DB-004 §4, Human Decision)**: PRD에는 Customer Situation 기반 태그(예: "손실구간 대안"·"만기고객 추천"·"연금수령 고객용")를 **추가하지 않는다** — 고객 상황→상품 연결을 암시하는 Metadata는 숨은 Recommendation Rule이 된다. 허용되는 것은 상품 자체의 사실·특성(topics, product_type, asset_class, 위험등급, 만기/유동성 특성, 분배(income/distribution) 특성 등 원천이 뒷받침하는 값)뿐이다. Customer Evidence와 상품의 적합성 연결은 Agent의 Management Direction / Product Fit reasoning에서 수행한다.
- fee_note(합성총보수/총보수)는 SRC-094(2026-08 포트폴리오 자료)에서 상품명 일치 시 결합 — 교차 원천 결합임을 각 항목에 명기.

## 항목

### PRD-001. KB 온국민 TDF 시리즈

| source | SRC-095 (TDF 표) + SRC-094 (빈티지별 위험자산 비중) | authority | T2 | as_of | 2026-07-30(수익률) | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "KB 온국민 TDF 시리즈", "product_type": "TDF", "risk_grade": 3, "risk_level_label": "다소높은",
  "return_recent": 0.1258, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "은퇴에 맞춘 글로벌자산배분", "sellable": null, "channels": [] }
```
- 보조 수치(SRC-095): 3M -1.47% / 3Y 36.83% / 표준편차(1Y) 10.25. 수익률·등급은 2030 빈티지 기준.
- 빈티지별 위험자산 비중(SRC-094, 2026-08, 열 정렬 ⟨판독불확실⟩): 2020 36.6% / 2025 38.2% / 2030 54.1% / 2035 59.5% / 2040 68.2% / 2045 72.8% / 2050 74.5% / 2055 74.1%.
- DO 편입용 적격 TDF 등급(SRC-095): KB온국민적격TDF2035(H) 다소높은(3) / KB온국민적격TDF2055(UH) 다소높은(3).
- **Unconfirmed**: sellable·channels·보수·빈티지별 개별 위험등급(적격형 외).

### PRD-002. 신한 마음편한 TDF 시리즈

| source | SRC-095 + SRC-094 | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "신한 마음편한 TDF 시리즈", "product_type": "TDF", "risk_grade": 3, "risk_level_label": "다소높은",
  "return_recent": 0.1392, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "생애주기에 따라 포트폴리오 조정, 환노출 포트폴리오 운용", "sellable": null, "channels": [] }
```
- 보조: 3M +0.25% / 3Y 38.23% / 표준편차 8.21. 빈티지 비중(SRC-094): 2025 33.4% ~ 2055 77.9%.
- **Unconfirmed**: sellable·channels·보수.

### PRD-003. 한화 LIFEPLUS TDF 시리즈

| source | SRC-095 + SRC-094 + SRC-098 | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "한화 LIFEPLUS TDF 시리즈", "product_type": "TDF", "risk_grade": 3, "risk_level_label": "다소높은",
  "return_recent": 0.1275, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "하이브리드운용전략과 목표연도의 노하우로 중장기성과 추구", "sellable": null, "channels": [] }
```
- 보조: 3M -2.35% / 3Y 37.94% / 표준편차 7.44. 빈티지 비중(SRC-094): 2020 27.0% ~ 2050 71.9%.
- **빈티지·적격형 등급 차이 실례**: 시리즈 대표(2030 기준) 다소높은(3) vs DO 편입 한화Lifeplus적격TDF2040·2045 = **높은(2)**(SRC-095) — 같은 브랜드라도 빈티지·적격 여부에 따라 위험등급이 다름. C2 검증 시 개별 빈티지 등급 확인 필수.
- **Unconfirmed**: sellable·channels·보수.

### PRD-004. 마이다스 기본 TDF 시리즈

| source | SRC-095 + SRC-094 | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "마이다스 기본 TDF 시리즈", "product_type": "TDF", "risk_grade": 4, "risk_level_label": "보통",
  "return_recent": 0.1850, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "마이다스에셋의 대표적인 국내외펀드를 편입하는 TDF", "sellable": null, "channels": [] }
```
- 보조: 3M -1.28% / 3Y 공란(원문 ⟨판독불확실⟩) / 표준편차 8.88.
- **Unconfirmed**: sellable·channels·보수·3Y.

### PRD-005. 키움 더드림 단기채

| source | SRC-095 (국내채권) + SRC-094 (안정추구형 포트 편입, 보수) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "키움 더드림 단기채", "product_type": "채권형(단기채)", "risk_grade": 6, "risk_level_label": "매우낮은",
  "return_recent": 0.0229, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "금리변동 위험 최소화, 매매차익 및 이자수익 추구",
  "fee_note": "합성총보수 연0.2990% (SRC-094, 교차 원천 결합)", "sellable": null, "channels": [] }
```
- 보조: 3M +0.63% / 3Y 11.48% / 표준편차 0.31.
- **Unconfirmed**: sellable·channels.

### PRD-006. 한국투자 크레딧 포커스 ESG

| source | SRC-095 | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "한국투자 크레딧 포커스 ESG", "product_type": "채권형", "risk_grade": 5, "risk_level_label": "낮은",
  "return_recent": 0.0087, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "ESG등급이 우수한 중단기 우량채권에 투자, 지속가능한 초과수익 추구", "sellable": null, "channels": [] }
```
- 보조: 3Y 14.07% / 표준편차 1.46. **Unconfirmed**: sellable·channels·보수.

### PRD-007. 교보악사 Tomorrow 장기우량K-1호

| source | SRC-095 + SRC-094 (공격투자형 포트 편입, 보수) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "교보악사 Tomorrow 장기우량K-1호", "product_type": "채권형(장기 국공채·우량채)", "risk_grade": 5, "risk_level_label": "낮은",
  "return_recent": -0.0579, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "안정성이 높은 채권을 주된 투자대상자산으로 안정적인 이자수익 추구",
  "fee_note": "총보수 연0.3300% (SRC-094, 교차 원천 결합)", "sellable": null, "channels": [] }
```
- 보조: 3M -2.06% / 3Y 6.96% / 표준편차 3.63. **1Y 음수 수익률 상품** — 손실 구간 Case 재료 가능.
- **Unconfirmed**: sellable·channels.

### PRD-008. 한화 내일받는 단기국공채

| source | SRC-094 (안정형·연금수령 포트 편입) | authority | T2 | as_of | 2026-08 (포트폴리오 자료) | status | PROVISIONAL (위험등급·수익률 원천 부재) | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "한화 내일받는 단기국공채", "product_type": "채권형(단기 국공채)", "risk_grade": null, "risk_level_label": null,
  "return_recent": null, "return_period": null, "return_as_of": null,
  "features": "무위험 채권 및 특수채, 우량채에 투자하며, 채권잔존만기를 6개월 수준으로 유지하여 채권가격 변동위험 최소화",
  "fee_note": "합성총보수 연0.1977%", "sellable": null, "channels": [] }
```
- **Unconfirmed**: risk_grade·수익률·sellable·channels — SRC-094에 미기재.

### PRD-009. KB 스타 단기국공채

| source | SRC-094 (안정형 포트 편입) | authority | T2 | as_of | 2026-08 | status | PROVISIONAL | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "KB 스타 단기국공채", "product_type": "채권형(단기 국공채)", "risk_grade": null, "risk_level_label": null,
  "return_recent": null, "return_period": null, "return_as_of": null,
  "features": "단기 국채, 지방채, 특수채 및 우량 회사채에 투자하여 안정적인 수익 추구",
  "fee_note": "총보수 연0.2430%", "sellable": null, "channels": [] }
```
- **Unconfirmed**: risk_grade·수익률·sellable·channels.

### PRD-010. 삼성 EMP 리얼리턴 (UH)

| source | SRC-095 (해외혼합) + SRC-094 (위험중립형 포트 편입, 보수) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "삼성 EMP 리얼리턴 (UH)", "product_type": "혼합형(EMP, 주식혼합-재간접)", "risk_grade": 4, "risk_level_label": "보통",
  "return_recent": 0.1858, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "국내외주식, 채권, 대체자산 등 다양한 자산관련 ETF에 투자",
  "fee_note": "합성총보수 연1.1215% (SRC-094, 교차 원천 결합)", "sellable": null, "channels": [] }
```
- 보조: 3Y 51.45% / 표준편차 8.11. **Unconfirmed**: sellable·channels.

### PRD-011. KB 드림스타 자산배분 안정형

| source | SRC-095 (해외혼합; DO 뿔려드림III 편입) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "KB 드림스타 자산배분 안정형", "product_type": "혼합형(혼합-재간접)", "risk_grade": 4, "risk_level_label": "보통",
  "return_recent": 0.1233, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "전세계 주식, 채권 및 대체투자 관련 국내외 ETF 등에 분산투자", "sellable": null, "channels": [] }
```
- 보조: 3Y 공란(⟨판독불확실⟩) / 표준편차 6.07. **Unconfirmed**: sellable·channels·보수·3Y.

### PRD-012. 우리 미국단기채 공모주 (H)

| source | SRC-095 (해외혼합, 채권혼합) + SRC-094 (보수) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "우리 미국단기채 공모주 (H)", "product_type": "혼합형(채권혼합)", "risk_grade": 4, "risk_level_label": "보통",
  "return_recent": 0.0492, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "미국 공모주와 채권에 주로 투자하며 글로벌 공모주에 선별하여 투자",
  "fee_note": "합성총보수 연1.2171% (SRC-094, 교차 원천 결합)", "sellable": null, "channels": [] }
```
- 보조: 표준편차 1.70. **Unconfirmed**: sellable·channels·3Y.

### PRD-013. KB 퇴직연금 배당

| source | SRC-095 (국내주식) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 (2등급 후보) | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "KB 퇴직연금 배당", "product_type": "주식형(배당)", "risk_grade": 2, "risk_level_label": "높은",
  "return_recent": 0.8142, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "배당주와 성장주에 투자하여 장기수익률 극대화 추구", "sellable": null, "channels": [] }
```
- 보조: 1M -33.39% / 3M -16.06% / 3Y 134.86% / 표준편차 38.20 — **1Y 고수익·최근 1M 급락** 조합(수익률 단독 추천 유혹 구조 재료).
- **Unconfirmed**: sellable·channels·보수.

### PRD-014. 에셋플러스 글로벌 리치투게더

| source | SRC-095 (해외주식) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 (3등급 후보) | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "에셋플러스 글로벌 리치투게더", "product_type": "주식형(해외)", "risk_grade": 3, "risk_level_label": "다소높은",
  "return_recent": 0.2608, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "글로벌 혁신기업 및 고부가소비재 기업의 주식에 투자", "sellable": null, "channels": [] }
```
- 보조: 3Y 76.14% / 표준편차 23.06. **Unconfirmed**: sellable·channels·보수.

### PRD-015. 마이다스 아시아 리더스 성장주 (H)

| source | SRC-095 (해외주식) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 (2등급 후보) | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "마이다스 아시아 리더스 성장주 (H)", "product_type": "주식형(해외)", "risk_grade": 2, "risk_level_label": "높은",
  "return_recent": 0.4719, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "성장잠재력 높은 아시아지역(일본, 중국, 인도, 대만 등) 주식에 투자", "sellable": null, "channels": [] }
```
- 보조: 1M -22.82% / 3Y 107.35% / 표준편차 26.34. **Unconfirmed**: sellable·channels·보수.

### PRD-016. 피델리티 글로벌 테크놀로지

| source | SRC-095 (해외주식) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 (2등급 후보) | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "피델리티 글로벌 테크놀로지", "product_type": "주식형(해외, 재간접)", "risk_grade": 2, "risk_level_label": "높은",
  "return_recent": 0.1724, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "전세계 테크기업의 주식형증권 투자", "sellable": null, "channels": [] }
```
- 보조: 3Y 63.68% / 표준편차 16.99. **Unconfirmed**: sellable·channels·보수.

### PRD-017. KB RISE 미국ETF 모아드림

| source | SRC-095 (해외주식) | authority | T2 | as_of | 2026-07-30 | status | ACTIVE | delivered_for | REQ-015 (2등급 후보) | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "KB RISE 미국ETF 모아드림", "product_type": "주식형(해외, 재간접)", "risk_grade": 2, "risk_level_label": "높은",
  "return_recent": 0.2670, "return_period": "1Y", "return_as_of": "2026-07-30",
  "features": "미국 대표지수 및 미국 성장테마 관련 ETF에 투자", "sellable": null, "channels": [] }
```
- 보조: 3Y 공란(⟨판독불확실⟩) / 표준편차 16.30. **Unconfirmed**: sellable·channels·보수·3Y.

### PRD-018. GIC(이율보증형보험) 라인업 — 개인형IRP 가입 가능 상품 (2026-07 조회 기준)

| source | SRC-097 (L215~225 [04-12-17A] 조회 캡처, 금리 기준월 2026-07 / L280~294 8월 특별제공상품 표) | authority | T2 | as_of | 2026-07(조회 캡처)·2026-08(특별제공) | status | ACTIVE | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

개별 카드 구성용 원천 표 — supply 구성 시 아래 행에서 개별 상품 선택 (전 상품 예금자보호 **대상**, IRP 연금지급 **가능**, 최소금액 제한 없음, 별도 신청 없이 거래 가능 — 운용지시서 상품종류 '보험'):

| 상품명(원문) | 신용등급 | 계약기간 | 금리(연, 공시이율) | 잔여한도(억원) |
|---|---|---|---|---|
| DB손해보험 무배당 스마트 퇴직연금 이율보증형… | AAA | 3년 | 4.41 | 699 |
| KB손해보험 퇴직연금 이율보증형보험(DC/IRP,3년…) | AA+ | 3년 | 4.38 | 406 |
| 무배당 메리츠화재 이율보증형보험3(개인형IRP,3년) | AA+ | 3년 | 4.36 | 845 |
| 무배당 메리츠화재 이율보증형보험3(개인형IRP,5년) | AA+ | 5년 | 4.36 | 845 |
| DB손해보험 무배당 스마트 퇴직연금 이율보증형… | AAA | 5년 | 4.31 | 699 |
| 무배당 한화생명 신탁계공용 이율보증형 3년 퇴직적… | AA+ | 3년 | 4.25 | 477 |
| KB손해보험 퇴직연금 이율보증형보험(DC/IRP,2년…) | AA+ | 2년 | 4.20 | 406 |
| 무배당 교보생명 신탁계공용 이율보증형보험(DC/IR…) | AAA | 3년 | 4.20 | 473 |

- 8월 특별제공(2026-08 기준, SRC-097 L285 — GIC 9개사·기간별 금리 상이): 예 — DB손해보험2(AAA) 3년제 4.55%/5년제 4.45%, 삼성생명(AAA) 3년제 4.61%, 한화생명(AAA) 3년제 4.48%, KB손해보험(AA+) 3년제 4.38% 등. 원문 표 전체는 SRC-097 참조.
- 금리 표시는 **공시이율(연복리)** — 타 상품과 비교 시 단리 환산 필수(OK-010).
- 특성: 보험사 발행, 예금자보호 1억원 대상, 비대면 거래 가능(SRC-001 특징표). KB라이프/KB손해보험 등 KB계열사 GIC 존재.
- **Unconfirmed**: channels 상세(비대면 가능은 GIC 일반 특성으로만 확인). 상품명 일부 원문에서 말줄임(…) — 전체 정식명칭 미확보. 금리·잔여한도는 월단위 변동.

### PRD-019. 저축은행 정기예금 (상품 유형 — 개별 상품 데이터 corpus 부재)

| source | SRC-097 (L59~67·L149~153) / SRC-002 (L43~46·L93~96·L112) / SRC-001 (L114·L304) | authority | T2 | as_of | 2026-08(금리 범위) | status | PROVISIONAL (개별 상품명·금리 부재) | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "(개별 상품 미확보 — 유형 정보만)", "product_type": "저축은행 정기예금", "risk_grade": null,
  "risk_level_label": null, "return_recent": null, "return_period": null, "return_as_of": null,
  "features": "시중은행보다 높은 금리 제공(2026-08 기준 연 4.00~4.70%, 월복리 표시). 신용등급 A~BBB-. 만기 원리금이 예금자보호 한도 이내가 되도록 매수한도 존재(1년제만 보유 시 저축은행별 9,500만원, 2·3년제 보유 시 9,000만원 이내)",
  "sellable": null, "channels": [] }
```
- 개별 저축은행 상품명·금리는 corpus에 없음 — 확인 경로만 존재: KB-WiseNet > 연금(퇴직연금) > [자산관리]원리금보장상품 > 상품한도 내 저축은행 관련자료(SRC-002 L95), 월별 특별제공상품 안내(SRC-001).
- 일반은행 대비 금리 +0.7~0.8%p 서술(SRC-002 L112, As-of Unknown — 시점 주의). **예금자보호 한도는 SC-001 미해소**(구자료 5천만원 vs 2026년 자료 1억원).
- **Unconfirmed**: 개별 상품 전부.

### PRD-020. 수협은행 정기예금 (당행 단독 제공 — 실물이전 방어 특성)

| source | SRC-097 (L57 꿀팁) / SRC-001 (L248~251) / SRC-095 (주석 — 수협은행 노후보장 정기예금 디폴트옵션용(3년) 금리 3.27, 2026-08) | authority | T2 | as_of | 2026-08 | status | PROVISIONAL (일반 판매용 금리 미확인) | delivered_for | REQ-015 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

```json
{ "name": "Sh 수협은행 정기예금", "product_type": "시중은행(특수은행) 정기예금", "risk_grade": null, "risk_level_label": null,
  "return_recent": null, "return_period": null, "return_as_of": null,
  "features": "KB국민은행에서 단독 제공하는 상품 — 타사로 실물이전 불가(이전 시 현금화 필요). DO 편입용 '수협은행 노후보장 정기예금 디폴트옵션용(3년)' 금리 3.27%(2026-08)",
  "sellable": null, "channels": [] }
```
- 실물이전 방어 활용 서술(SRC-097 "타사로 이전을 고려중인 고객님께 실물이전 방어용" / SRC-001 "금리가 비슷하다면, 타사로 실물이전이 불가한 상품으로 매수 유도")은 **Bank Objective 성격 포함** — 추천사유로 직접 사용 불가(HD-7/G4), '실물이전 불가 상품' 사실 고지는 고객 리스크 안내로 사용 가능(OK-002 Step4).
- **Unconfirmed**: 일반 판매용(비DO) 금리·기간 라인업.

### PRD-021. KB 디폴트옵션 포트폴리오 (위험도 4단계 9종 + BF 1종)

| source | SRC-095 (편입상품·비중·금리·수익률 2026-07-30/금리 2026-08) / SRC-098 (L81~94 구성·수익률 2026-08-20) / SRC-089 (L43~54 위험도·가입 가능 투자성향) | authority | T2 + Public | as_of | 2026-08 | status | CONFLICT(종수 — SC-004: SRC-089는 2026-07 기준 10종 표기, 본 표는 T2 2건의 9종. 종수·전체 구성 확정 인용 금지, 개별 행은 T2 교차분) | delivered_for | REQ-015·REQ-009 연계 | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

| 위험도 | 명칭 | 구성(SRC-098) | 1Y 수익률(2026-08-20, SRC-098) | 가입 가능 투자성향(SRC-089) |
|---|---|---|---|---|
| 초저위험 | 지켜드림 | 신한은행 정기예금(3년) 35 / 기업은행 35 / 하나은행 30 | +2.55% | 모든 투자성향 |
| 저위험 | 알파드림1 | 수협은행 정기예금(3년) 70 / 키움 키워드림 TDF2030 20 / 삼성 글로벌EMP TDF2035 10 | +5.23% | 공격·적극·위험중립·안정추구형 |
| 저위험 | 알파드림2 | 기업은행 정기예금(3년) 50 / KB다이나믹 TDF2030 40 / NH 하나로 TDF2035 10 | +10.33% | 〃 |
| 저위험 | 알파드림3 | 농협은행 정기예금(3년) 35 / DB손해보험 GIC(3년) 35 / KB온국민 TDF2035(H) 30 | +7.05% | 〃 |
| 중위험 | 뿔려드림1 | 하나은행 정기예금(3년) 30 / KB다이나믹 TDF2040 50 / 한화LifePlus TDF2040 20 | +16.60% | 공격·적극·위험중립형 |
| 중위험 | 뿔려드림2 | 미래에셋 평생소득 TIF 70 / 키움불리오 EMP(UH) 20 / IBK플레인바닐라 EMP 10 | +16.08% | 〃 |
| 중위험 | 뿔려드림3 | KB라이프 GIC(3년) 20 / KB드림스타 자산배분안정형 80 | +11.04% | 〃 |
| 고위험 | 모두드림1 | KB온국민 TDF2055(UH) 60 / 한국투자 알아서 TDF2050(UH) 20 / 한화LifePlus TDF2045 20 | +22.93% | 공격투자형 |
| 고위험 | 모두드림2 | KB다이나믹 TDF2050 50 / 한국투자 알아서 TDF2055(UH) 40 / 미래에셋 전략배분 TDF2050 10 | +23.04% | 〃 |
| 고위험 | 모두드림3 | 미래에셋드림스타 자산배분성장형 100 (BF) | +17.52% | 〃 |

- DO 편입 정기예금 금리(2026-08, SRC-095): 신한 3.40 / 기업 3.25 / 하나 3.32 / 농협 3.40 / 수협 3.27. GIC: DB손보 4.41 / KB라이프 4.25.
- 저위험 알파드림1: 고용노동부 상품변경승인(26.5.26)에 따라 '26.7.6 하나은행 정기예금 → 수협은행 노후보장 정기예금 교체(SRC-095 주석).
- 편입상품 표기는 SRC-095(정식명)·SRC-098(축약형) 간 표기 차이 있으나 구성·비중 일치 교차 확인됨. 수익률은 두 원천의 기준일이 다름(2026-07-30 vs 2026-08-20) — 인용 시 기준일 명시.
- DO 상품은 실물이전 비대상(OK-003·OK-005 참조). **Unconfirmed**: sellable·channels(DO 등록은 StarBanking·단말 경로 존재 — SCR 참조).

### PRD-022. 성과부진(판매중단) 펀드 21종 — sellable=false 원천 목록

| source | SRC-002 (L18~35 [성과부진(판매중단)펀드 21종] 표, L215~245 관리 유형 C) | authority | T2 | as_of | **Unknown** (문서 내 "'21년 1년 수익률" 언급 — 구자료 가능성) | status | PROVISIONAL (As-of 불명 — 현재 판매 상태로 사용 금지) | delivered_for | (B-3 선택 확장 — Execution Eligibility 원천) | registered | 2026-08-31 |
|---|---|---|---|---|---|---|---|---|---|---|---|

corpus 내 유일한 **sellable=false 명시 원천**. 원문 표 그대로(가나다순 21종):

| No | 펀드명 | No | 펀드명 |
|---|---|---|---|
| 1 | KB퇴직연금이머징국공채인컴증권자투자신탁(채권) | 12 | 유리트리플알파증권자투자신탁(주식혼합) |
| 2 | KTB퇴직연금40증권자투자신탁(채권혼합) | 13 | 이스트스프링글로벌이머징증권자투자신탁제2호(주식-재간접) |
| 3 | 미래에셋퇴직연금솔로몬40증권자투자신탁1호(채권혼합) | 14 | 이스트스프링퇴직연금업종일등증권자투자신탁(주식) |
| 4 | 미래에셋퇴직연금솔로몬증권자투자신탁1호(주식혼합) | 15 | 파인만스타공모주증권투자신탁(채권혼합) |
| 5 | 미래에셋퇴직플랜목돈분할투자3/10증권자투자신탁2호(채권혼합) | 16 | 파인만코리아국가대표증권자투자신탁1호(주식) |
| 6 | 삼성퇴직연금CHINA본토포커스40증권자투자신탁제1호(채권혼합) | 17 | 파인만퇴직연금우량채증권자투자신탁1호(채권) |
| 7 | 삼성퇴직연금액티브증권자투자신탁제1호(주식) | 18 | 파인만퇴직연금코어셀렉트안정40증권자투자신탁1호(채권혼합) |
| 8 | 삼성퇴직연금코리아대표40증권자투자신탁제1호(채권혼합) | 19 | 파인만퇴직연금코어셀렉트증권자투자신탁1호(주식혼합) |
| 9 | 우리G퇴직연금글로벌이머징40증권자투자신탁(채권혼합) | 20 | 한국밸류10년투자퇴직연금증권투자신탁1호(채권혼합) |
| 10 | 우리연금재팬증권자투자신탁(주식)P클래스 | 21 | 한국투자코스피솔루션증권투자신탁(채권혼합) |
| 11 | 우리템플턴퇴직연금글로벌40증권자투자신탁(채권혼합) | | |

- 의미: 문서 시점 기준 **신규 판매 중단**(성과부진 사유) — 기존 보유 고객은 유지 중일 수 있으며, 판매 재개 가능성 언급 존재(L245). 위험등급·수익률은 이 원천에 없음.
- Case 활용: sellable=false 상품 카드(미끼/보유상품 시나리오)의 실명 재료. 단 **As-of 불명이므로 "현재 판매중단"으로 단정 금지** — Case에서는 scenario 시점 명시(mock assumption provenance, HD-P2-GATE2 (4)) 또는 [04-12-17A] 조회 확인 경로와 함께 사용.
- **Unconfirmed**: 각 펀드의 현재 판매 상태·위험등급·수익률 전부.
