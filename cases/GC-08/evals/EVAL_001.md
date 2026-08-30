# EVAL_001 — GC-08

## 1. Evaluation Metadata
- Case: GC-08 / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-08/case.md FROZEN / Knowledge Pack 동일 커밋 / Runtime: 8cf3787 (REV-001)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PARTIAL**

핵심 판단이 Golden 경계 안에 있다: 8,000만 정기예금은 "만기가 8개월 남았으므로 중도해지 실익 분석이 선행"(K-001, 계산기 [04-12-642])으로 계산 없는 갈아타기를 배제했고, 3년제 특별제공 상품이 2년 후 연금개시 계획과 "불일치하므로 유동성 확보 계획 확인 없이는 장기 상품 권유가 불가"(K-004)라고 정확히 짚었으며, 고유계정대 500만원의 만기상환 후 6주 경과 → DO 적용 시점 도달을 첫 확인 항목으로 두었고(K-003), 내점 선호·컨설팅센터 연계(K-005)까지 채널을 맞췄다. KPI 목적의 즉시 중도해지 권유 없음(D10). C1/C2/C3 PASS, Critical Mistake 없음.
PARTIAL 사유: (1) Golden Acceptable Direction의 핵심인 **"현 상태 유지 + 만기 1개월 전 예약변경"** 경로가 결과(Judgment 유형·Action)로 명시되지 않음 — 계산 결과 손실이 크면 무엇을 하는지가 비어 있고 Judgment는 '개입 필요 / 추가 확인 우선'으로만(F-005 경미·F-010), (2) ELB(대면·최소 5천만·예금자보호 비대상) 조건과 GIC/저축은행의 만기 길이 차이(K-002) 미언급, (3) 만기 예약변경 가능 시점(만기 1개월 전, K-003) 미언급, (4) 500만원의 원리금보장 내 운용지시 방향은 "운용 방향 안내"로만.

## 3. Expected Judgment Check
| Must Consider | Result |
|---|---|
| 중도해지 손실 계산 없이 변경 금지 → 계산기 | MET |
| 손실 크면 유지 + 만기 예약변경 | PARTIAL (유지 경로·예약 시점 미명시) |
| 500만 DO 적용 확인 → 운용지시 | MET (확인) / PARTIAL (방향) |
| 3년제 ↔ 2년 후 개시 정합 | MET |
| ELB 조건 | MISSED |
| 채널(내점·컨설팅센터 예금→예금) | MET |
| 금리 as-of | PARTIAL (입력 수치 그대로, as-of 미표기) |
Must Not Assume: 전부 COMPLIANT (즉시 중도해지·3년제 무조건·실적배당·ELB 오안내·예보 단정 없음). Required Confirmation: 계산기 IDENTIFIED / 500만 DO IDENTIFIED / 유동성·수령 방식 IDENTIFIED / 금리 비교 희망 여부 MISSED. Acceptable: WITHIN(부분). Forbidden: NO.

## 4. F-005 / F-006
- F-005: 경미 — 판단 선행·확인 우선은 정확하나 "현 상태 유지 가능"을 결과로 두지 않음; 계산 후 분기(유지 vs 교체)가 Action에 없음(F-010 계열).
- F-006: K-001·K-003(6주)·K-004·K-005 사용; K-002(ELB·만기 길이)·K-003(예약변경 시점) 세부 미사용 → 경미 잔존.

## 5. Secondary
F-001 없음. F-002 없음. F-008 없음 (Brief가 조건 보존). F-004 경미(금리 비교 희망). F-007 양호([04-12-642]·[04-12-660] 명시).

## 6. Constraint Check
C1 PASS (Action 2 안정추구형) · C2 PASS · C3 PASS.

## 7. Evidence
RUN_001 §3, §6, §7 Action 1~4, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
