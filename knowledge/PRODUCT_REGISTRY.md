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

## 항목

(승인 후 B-1에서 등록)
