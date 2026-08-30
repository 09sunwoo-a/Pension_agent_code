# EVAL_001 — GC-09

## 1. Evaluation Metadata
- Case: GC-09 / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-09/case.md FROZEN (GC-09 freeze commit) / Runtime: 8cf3787 (REV-001, HTTP timeout 300s는 Operational)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PARTIAL**

절차 정확성과 우선순위가 좋다: "DO 등록 변경만으로는 기존 예금 4,000만원이 이동하지 않음"(K-001 2단계)을 Action 3에서 명시, 지켜드림 4,000만은 리밸런싱 계산기로 중도해지 유불리 분석(K-003), 성향 상향 + 명시 의사 → '개입 필요'로 보되 은퇴 시기·직접/위임·손실 감내 확인을 선행('추가 확인 우선'), 최종 변경은 "단계적 전환 방향으로 합의 시"(공격투자형 상한 내). 1,000만원이 입금 7주 경과에도 DO 미적용인 사유를 Unknown·Action 1로 정확히 짚었다. C1/C2/C3 PASS, Critical Mistake 없음.
PARTIAL 사유: (1) 우선순위 (2) **11월 만기 1,500만원 예약변경**이 전혀 언급되지 않음(입력 Fact 미사용, F-003), (2) 등록 변경 시 공격투자형 가입 가능 범위(모두드림 포함)와 "가능 ≠ 권유 근거"가 명시되지 않음(K-002 부분), (3) Brief의 "방치된 현금성 자산" — 7주 미적용은 확인 대상이지 방치 확정이 아님(경미 F-001), (4) 직원/고객 역할(앱 등록 변경·보유상품 변경 거래) 구분 없음.

## 3. F-005 / F-006 (REV-001 관찰)
- F-005: 없음 — 확인 선행 + 단계적 개입, 즉시 전액 전환 없음
- F-006: K-001·K-003·K-004 사용; K-002 범위·K-006 미사용(경미)

## 4. Secondary
F-001 경미('방치된'). F-002 없음. F-008 없음. F-004 없음(4 항목). F-003 재현(11월 만기 1,500만 미사용). F-007 경미.

## 5. Constraint Check
C1 PASS · C2 PASS · C3 PASS (공격투자형 — 제외 없음)

## 6. Evidence
RUN_001 §3, §6, §7, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
