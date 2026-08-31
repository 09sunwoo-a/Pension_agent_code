# GC-05 — Customer Evidence Pack (input_v2, REV-002)

변환 노트 (모델 미전달): 원본 case.md §2를 REV-002 8-섹션으로 재조직. 원본 불변.
제외(승인 스키마 적용): 최근 운용지시일, 타 계좌 투자행동 마이데이터(Cross-account), 동연령대 비교(Peer), 행내 TM 대상 분류(Bank Signal). 새 사실 추가 없음.
관련 평가 축 처리: 마이데이터=Contextual Evidence 판정 축·TM 압박 금지 축·동연령 비교 미사용 축은 `N/A — Input removed by approved REV-002 schema`. Pair(GC-04↔05)의 핵심 판단 차이(명시 의사 존중 vs 의사 부재→확인 우선)는 CRM 메모 부재·Digital Signals(수익률 조회)로 성립 — EMPLOYEE_BRIEF_SPEC §5 변환 규칙 4.

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
- 투자성향: 위험중립형 (투자성향 분석일 2026-07-18, 유효)
- 퇴직급여 포함 여부: 포함 (80,000,000원, 2023년 입금) / 개인부담금 누적 160,000,000원
- 연금개시 여부: 미개시 / 연금지급설계: 미등록
- 스타뱅킹 이용 여부: 이용 중

## 2. IRP Current Snapshot
- 전체 평가금액: 240,000,000원
- 시중은행(신한은행) 퇴직연금 정기예금 1년: 158,000,000원 (65.8%) — 약정 2026-01-05 ~ 만기 2027-01-05, 적용금리 2.9% (as-of 약정일)
- 시중은행(하나은행) 퇴직연금 정기예금 1년: 79,000,000원 (32.9%) — 약정 2026-02-01 ~ 만기 2027-02-01, 적용금리 2.7% (as-of 약정일)
- 현금성자산(고유계정대): 3,000,000원 (1.3%)
- 최근 1년 IRP 수익률: +2.8%
- 디폴트옵션 등록 여부: 등록 — 「지켜드림」(초저위험)

## 3. IRP Event Timeline
- 2026-08-05 입금 3,000,000원 — 입금사유 "개인부담금"
- 2026-07-18 투자성향 분석 실시 (결과: 위험중립형)

## 4. Whole-Asset Context

## 5. Investment Activity
- IRP 내 ETF 보유·매매 이력: 없음

## 6. Upcoming Events
- 신한은행 정기예금 158,000,000원 만기 2027-01-05
- 하나은행 정기예금 79,000,000원 만기 2027-02-01

## 7. Digital / Behavioral Signals
- 스타뱅킹 최근 3개월 IRP 수익률 조회: 6회 (운용지시·상품변경 화면 진입: 없음)

## 8. Customer Interaction / CRM Memo
- CRM 상담메모: NULL (상담 이력 없음)
