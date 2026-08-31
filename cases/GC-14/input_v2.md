# GC-14 — Customer Evidence Pack (input_v2, REV-002)

변환 노트 (모델 미전달): 원본 case.md §2를 REV-002 8-섹션으로 재조직. 원본 불변.
제외(승인 스키마 적용): 최근 운용지시일(원본 부재), 연도별 납입 이력(2023~2025)·세액공제 신청/미신청 이력 필드(세제 축소 — 관련 세제 구조는 Knowledge K-001·K-005가 공급), 상품 판매상태("판매중"), "주택 보유 여부: 시스템 미확인" 별도 필드(고객 진술은 CRM 메모 원문에 보존). 당해년도 IRP 납입액은 Av `?` 유지 필드로 보존. 새 사실 추가 없음.
관련 평가 축 처리: 연도별 납입·공제 이력에 직접 의존하는 세부 축이 있으면 `N/A — Input removed by approved REV-002 schema`.

```json
{
  "base_date": "2026-08-28",
  "age": 44,
  "join_date": "2023-01-10",
  "retirement_benefit_included": false,
  "deposits": [{"date": "2026-08-05", "amount": 8000000, "reason": "개인부담금"}],
  "maturities": [{"date": "2027-02-10", "amount": 15000000, "product": "시중은행 퇴직연금 정기예금 1년"}],
  "do_registered": true,
  "do_trigger": {"type": "최초입금", "date": "2026-08-05"}
}
```

## 1. Customer / Pension Profile
- 기준일: 2026-08-28
- 계좌 유형: 개인형IRP (적립용)
- IRP 가입일: 2023-01-10
- 고객 연령: 만 44세
- 투자성향: 위험중립형 (분석일 2026-02-03)
- 퇴직급여 포함 여부: 없음
- 연금수령 중: 아님
- 스타뱅킹 이용 여부: 이용 중

## 2. IRP Current Snapshot
- 전체 평가금액: 38,000,000원
- 시중은행 퇴직연금 정기예금 1년: 15,000,000원 (39.5%) — 약정 2026-02-10 ~ 만기 2027-02-10, 적용금리 2.9%
- KB온국민TDF2040: 15,000,000원 (39.5%) — 고객보유수익률 +11%
- 현금성자산(고유계정대): 8,000,000원 (21.0%)
- 디폴트옵션 등록 여부: 등록 — 「알파드림2」
- 당해년도 IRP 납입액: 3,000,000원

## 3. IRP Event Timeline
- 2026-08-05 입금 8,000,000원 — 입금사유 "개인부담금"

## 4. Whole-Asset Context

## 5. Investment Activity

## 6. Upcoming Events
- 시중은행 정기예금 15,000,000원 만기 2027-02-10

## 7. Digital / Behavioral Signals

## 8. Customer Interaction / CRM Memo
- [CRM] 2026-08-27 (전화): "전세 계약했어요(계약일 8월 20일). 잔금이 10월 15일인데 3,000만원 정도 IRP에서 뺄 수 있나요? 무주택이에요." — source: 직원 작성 상담메모
