# EVAL_001 — GC-02

## 1. Evaluation Metadata
- Case: GC-02 (Pair↔GC-01) / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-02/case.md FROZEN (commit 9f826a6) / Knowledge Pack: 3dd289f / Runtime: 8cf3787 (REV-001)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PASS**

Pair 축이 정확히 반영됐다: TDF 보유·과거 공모펀드 이력으로 "분산투자 가능고객으로 분류될 수 있다"(K-003/K-010)고 보되, Judgment는 **추가 확인 우선 / 고객 결정 지원**으로 두고 "원리금보장 유지와 실적배당 전환이라는 두 가지 선택지를 모두 고려할 수 있는 상태"로 복수 방향을 열었다. Action 3(원리금보장 선호 시: 만기별 금리·발행주체 기반 대안)과 Action 4(분산투자 희망 시: **4~6등급** 채권 비중 높은 TDF/채권형 **일부** 운용)가 조건부로 병렬이며, 어느 쪽도 기본값이 아니다. C2를 실제로 사용해 위험중립형의 등급 범위를 명시했고, "일부 금액만"으로 전액 전환을 배제했다. 만기 후 6주·3년제 DO 경로(K-001/K-002), 스타뱅킹 예약변경(K-003)까지 제시. GC-01 RUN_002(원리금보장 내 비교만)와 결론이 달라진 이유가 reasoning에 드러난다. C1/C2/C3 PASS, Critical Mistake 없음.
경미: 기존 TDF2035 보유(3등급)의 "추가 매수 불가·보유 유지 가능" 언급 없음; 만기 길이(1년/3년) 선호·특별제공 잔여한도 확인 없음; 고유계정대 200만원 미처리; Brief에 "$ightarrow$" 렌더링 잔재(형식).

## 3. Expected Judgment Check
| Must Consider | Result |
|---|---|
| 분산투자 가능 접근 + 원리금보장 동등 제시 (복수 방향) | MET |
| 경험 ≠ 실적배당 의향 확정 | MET (확인 선행, 조건부) |
| 기존 TDF2035 위반 아님·추가 매수 불가 | PARTIAL (미언급, 위반도 없음) |
| 만기 경로·시한 | MET |
| 연금개시 요건 ↔ 투자기간 | MET (K-005) |
| 비대면 특정펀드 금지 | MET (유형 수준만) |
Must Not Assume: 전부 COMPLIANT. Required Confirmation: 유지 vs 일부 실적배당 IDENTIFIED / 비중 PARTIAL("일부") / 만기 길이 MISSED / 사용계획 IDENTIFIED. Acceptable: WITHIN. Forbidden: NO.

## 4. F-005 / F-006
- F-005: 없음 — 판단 선행, 두 방향 병렬, F-010(선택지 축소)도 없음(오히려 GC-01 RUN_002보다 분기가 풍부).
- F-006: 핵심 K 사용(K-001/002/003/005/008/010). 잔여 경미: K-004 한도·화면, 고유계정대 200만.

## 5. Secondary
F-001 없음 ("분류될 수 있다"). F-002 없음. F-008 없음 (Brief가 조건·등급 보존). F-004 경미(만기 길이). F-007 개선(스타뱅킹 예약변경). 형식: Brief 화살표 LaTeX 잔재.

## 6. Constraint Check
C1 PASS (Action 3 안정형·Action 4 위험중립형) · C2 PASS (4등급 이하 명시) · C3 PASS.

## 7. Evidence
RUN_001 §3, §6, §7 Action 1~5, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
