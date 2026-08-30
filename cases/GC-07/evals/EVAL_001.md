# EVAL_001 — GC-07

## 1. Evaluation Metadata
- Case: GC-07 / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-07/case.md FROZEN (GC-07 freeze commit; RUN_001 1차 시도 HTTP read timeout → 모델 출력 없음, 동일 Frozen 상태로 재실행) / Runtime: 8cf3787 (REV-001, HTTP timeout 300s는 Operational)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PARTIAL**

제도·산술 이해가 정확하다: 초과 원인을 "매수 당시 66% → 평가액 상승"으로 추론(사실 표기), **현금성 400만원을 안전자산으로 운용지시해도 분모가 변하지 않아 비중이 유지된다**(K-004)는 핵심 논리를 정확히 적용하고, 고객 의사(매도 회피)에 맞춰 "추가 입금(잔여 납입한도 1,300만) 후 안전자산 운용지시" 경로를 제시했다. 페널티는 "공식 기준 확인" 으로 Operational Check 처리(K-002, HD-3), 1~2등급 상품 권유 불가(C2) 명시. Judgment(정보 안내 중심 / 고객 결정 지원)가 고객 결정 구조에 맞다. C1/C2/C3 PASS, Critical Mistake 없음.
PARTIAL 사유: (1) 70% 규정의 대상·예외(적격 TDF·디폴트옵션 100%)를 명시적으로 설명하지 않음 — TDF를 위험자산에 합산하지는 않았으나 "왜 TDF는 제외되는가"의 정보가 빠짐(K-001), (2) 두 조치 경로(초과분 교체매매 vs 추가입금) 비교 없이 추가입금만 제시 — 고객 의사 반영으로 정당하나 Golden은 "두 경로 비교 → 고객 선택"을 요구, (3) 향후 위험자산 추가 매수 의향·제한 가능성 확인 없음, (4) 실행 주체(고객 본인 앱 운용지시, 직원 [04-12-354] 확인) 미언급; Action 2의 kind "고객 결정 지원"은 kind 목록 밖(형식), risk_level '적극투자형'은 안전자산 운용 경로 라벨로 부정확(허용 범위 내).

## 3. F-005 / F-006 (REV-001 관찰)
- F-005: 없음 — 판단 선행, 고객 의사 반영, 강제 매도 없음. 교체매매 경로 미제시는 F-010(선택지 축소) 경미
- F-006: K-002·K-003·K-004 사용 정확; K-001 예외 설명·K-005 채널 미사용 → 경미

## 4. Secondary
F-001 없음('추론됩니다'). F-002 없음. F-008 없음. F-004 경미(추가 매수 의향). F-007 경미(앱·화면).

## 5. Constraint Check
C1 PASS · C2 PASS (1~2등급 불가 명시) · C3 PASS

## 6. Evidence
RUN_001 §3, §6, §7, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
