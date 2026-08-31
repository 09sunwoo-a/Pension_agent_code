# GC-17 — Customer Evidence Pack (input_v2, REV-002)

변환 노트 (모델 미전달): 원본 case.md §2를 REV-002 8-섹션으로 재조직. 원본 불변.
제외(승인 스키마 적용): "은퇴 예상 시기: 미확인" 명시 라인(Decision Variable — 입력 힌트 금지, 확인 축 도출은 Agent 몫), 당행 TDF 라인업 참고정보(Reference Data → Frozen Knowledge Pack K-001·K-002가 동일 내용 공급 — 정보 손실 없음). 새 사실 추가 없음.
관련 평가 축 처리: 은퇴 시기 확인 도출 축은 유지(입력 힌트 없이 도출해야 하므로 오히려 강화된 검증).

```json
{
  "base_date": "2026-08-28",
  "age": 34,
  "deposits": [{"date": "2026-06-15", "amount": 7000000, "reason": "개인부담금"}],
  "do_registered": true,
  "do_trigger": {"type": "최초입금", "date": "2026-06-15"}
}
```

## 1. Customer / Pension Profile
- 기준일: 2026-08-28
- 계좌 유형: 개인형IRP (적립용)
- 고객 연령: 만 34세 (1992년생)
- 투자성향: 위험중립형 (분석일 2026-06-01)
- 스타뱅킹 이용 여부: 이용 중

## 2. IRP Current Snapshot
- 전체 평가금액: 24,000,000원
- 현금성자산(고유계정대): 7,000,000원 (29.2%)
- 시중은행 정기예금: 9,000,000원 (37.5%) — 만기 2027-06
- 키움더드림단기채(채권형): 8,000,000원 (33.3%) — 매우낮은위험(6등급)
- 디폴트옵션 등록 여부: 등록 — 「알파드림2」(저위험: 정기예금 50 + TDF 50)

## 3. IRP Event Timeline
- 2026-06-15 입금 7,000,000원 — 입금사유 "개인부담금" (이후 무변동)
- 2026-06-01 투자성향 분석 실시 (결과: 위험중립형)

## 4. Whole-Asset Context

## 5. Investment Activity

## 6. Upcoming Events
- 시중은행 정기예금 9,000,000원 만기 2027-06

## 7. Digital / Behavioral Signals

## 8. Customer Interaction / CRM Memo
- [CRM] 2026-08-27 (앱 상담 요청): "TDF로 굴리고 싶은데 어떤 걸 골라야 하나요?" — source: 직원 작성 상담메모
