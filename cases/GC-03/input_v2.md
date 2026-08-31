# GC-03 — Customer Evidence Pack (input_v2, REV-002)

변환 노트 (모델 미전달 — bullet 아님): 원본 case.md §2를 REV-002 8-섹션으로 재조직. 원본 case.md·RUN·EVAL 불변.
제외(승인 스키마 적용): 최근 운용지시일(없음), 이연퇴직소득세·과세이연 등록 상태 필드(입금사유 코드는 유지), "연금개시 요건 미충족" 파생 라인(R1 전처리로 대체). 새 사실 추가 없음.

```json
{
  "base_date": "2026-08-28",
  "age": 53,
  "join_date": "2026-08-19",
  "retirement_benefit_included": true,
  "deposits": [{"date": "2026-08-21", "amount": 180000000, "reason": "과세이연/계약이전입금"}],
  "do_registered": false,
  "one_month_cash_delta": 180000000
}
```

## 1. Customer / Pension Profile
- 기준일: 2026-08-28
- 계좌 유형: 개인형IRP (퇴직용 — 퇴직급여 수령 계좌, 2026-08-19 신규)
- IRP 가입일: 2026-08-19
- 고객 연령: 만 53세
- 투자성향: 위험중립형 (투자성향 분석일 2026-08-19, 계좌 개설 시 분석)
- 퇴직급여 포함 여부: 포함 (180,000,000원) / 개인부담금 누적: 0원
- 연금개시 여부: 미개시
- 재직/재취업 여부: NULL (시스템 미확인)
- 스타뱅킹 이용 여부: 이용 중

## 2. IRP Current Snapshot
- 전체 평가금액: 180,000,000원
- 현금성자산(고유계정대): 180,000,000원 (100%)
- 디폴트옵션 등록 여부: 미등록
- 입금예정상품 등록 여부: 미등록

## 3. IRP Event Timeline
- 2026-08-21 입금 180,000,000원 — 거래내역 입금사유 "과세이연/계약이전입금" (전 직장 DC에서 이전)
- 2026-08-19 계좌 신규 개설 · 투자성향 분석 실시 (결과: 위험중립형)

## 4. Whole-Asset Context

## 5. Investment Activity
- IRP 내 상품 매매 이력: 없음 (신규 계좌)

## 6. Upcoming Events

## 7. Digital / Behavioral Signals

## 8. Customer Interaction / CRM Memo
- [CRM] 2026-08-19 (창구, 계좌 개설 시): "운용은 당분간 생각해 보겠다." — source: 직원 작성 상담메모
