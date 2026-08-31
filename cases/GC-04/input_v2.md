# GC-04 — Customer Evidence Pack (input_v2, REV-002)

변환 노트 (모델 미전달): 원본 case.md §2를 REV-002 8-섹션으로 재조직. 원본 불변.
제외(승인 스키마 적용): 최근 운용지시일, 행내 TM 대상 분류(Bank Signal — Reasoning Input 제거), 타 계좌 투자행동 마이데이터 필드(Cross-account — 단 고객 발화 속 언급은 CRM 메모에 보존), "연금개시 요건 충족" 파생 라인(R1 대체). 새 사실 추가 없음.
관련 평가 축 처리: TM 분류 오용(F-009) 축은 입력 제거로 `N/A — Input removed by approved REV-002 schema`.

```json
{
  "base_date": "2026-08-28",
  "age": 56,
  "join_date": "2017-04-03",
  "retirement_benefit_included": true,
  "deposits": [{"date": "2026-08-05", "amount": 3000000, "reason": "개인부담금"}],
  "maturities": [
    {"date": "2027-01-05", "amount": 158000000, "product": "신한은행 퇴직연금 정기예금 1년"},
    {"date": "2027-02-01", "amount": 79000000, "product": "하나은행 퇴직연금 정기예금 1년"}
  ],
  "do_registered": true,
  "do_trigger": {"type": "최초입금", "date": "2026-08-05"},
  "one_month_cash_delta": 3000000
}
```

## 1. Customer / Pension Profile
- 기준일: 2026-08-28
- 계좌 유형: 개인형IRP (적립겸용 — 퇴직급여 포함)
- IRP 가입일: 2017-04-03
- 고객 연령: 만 56세
- 투자성향: 공격투자형 (투자성향 분석일 2026-07-18, 유효)
- 퇴직급여 포함 여부: 포함 (80,000,000원, 2023년 입금) / 개인부담금 누적 160,000,000원
- 연금개시 여부: 미개시 / 연금지급설계: 미등록

## 2. IRP Current Snapshot
- 전체 평가금액: 240,000,000원
- 시중은행(신한은행) 퇴직연금 정기예금 1년: 158,000,000원 (65.8%) — 약정 2026-01-05 ~ 만기 2027-01-05, 적용금리 2.9% (as-of 약정일)
- 시중은행(하나은행) 퇴직연금 정기예금 1년: 79,000,000원 (32.9%) — 약정 2026-02-01 ~ 만기 2027-02-01, 적용금리 2.7% (as-of 약정일)
- 현금성자산(고유계정대): 3,000,000원 (1.3%)
- 최근 1년 IRP 수익률: +2.8%
- 디폴트옵션 등록 여부: 등록 — 「지켜드림」(초저위험)

## 3. IRP Event Timeline
- 2026-08-05 입금 3,000,000원 — 입금사유 "개인부담금"
- 2026-07-18 투자성향 분석 실시 (결과: 공격투자형)

## 4. Whole-Asset Context

## 5. Investment Activity

## 6. Upcoming Events
- 신한은행 정기예금 158,000,000원 만기 2027-01-05
- 하나은행 정기예금 79,000,000원 만기 2027-02-01

## 7. Digital / Behavioral Signals

## 8. Customer Interaction / CRM Memo
- [CRM] 2026-02-20: "원금손실 우려가 커서 IRP는 예금 중심으로 유지하고 싶다. 타 계좌에서 ETF 투자경험은 있다." — source: 직원 작성 상담메모
