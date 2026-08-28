# Constraint Requirement Map (Failure Discovery Phase)

Case에서 실제 판단공간에 영향을 준 Hard Constraint와, Out of Scope로 미룬 Constraint 후보를 축적한다. 새 Hard Constraint는 Human Gate B 없이 추가하지 않는다.

## Applied Hard Constraints

| ID | Constraint | Authority | Source Status | Runtime 구현 | Eval 결과 | Cases |
|---|---|---|---|---|---|---|
| C1 | 투자성향 5단계; Solution은 고객 성향과 같거나 낮은 위험수준만 | Human-approved | 공식 적합성 기준 Source 미확보 (Gap) | Pre-Reasoning: 허용/제외 범위를 독립 Constraint Section으로 전달 · Post: `risk_level` ∈ forbidden → FAIL | CASE_001 RUN_001 PASS (라벨·내용 정합 확인) | CASE_001 |

## Runtime Validation Limitations (관찰)

- C1 Validator는 모델이 자기 기재한 `risk_level` 라벨만 검사한다. direction 내용과 라벨의 정합성은 Evaluator가 별도 확인 (CASE_001: 정합). 상품별 위험등급 매핑은 미구현(Out of Scope).
- Execution Feasibility / Solution Conflict 검사 미구현.

## Constraint Candidates (Out of Scope in CASE_001 — 향후 Case에서 Gate B 대상)

| Candidate | 출처 | CASE_001 처리 | 비고 |
|---|---|---|---|
| 위험자산 투자한도 70% (디폴트옵션·TDF·채권형 ETF 예외 100%) | SRC-077 (Experiential / REVIEW_REQUIRED) | Out of Scope | 공식 원문 미확보; 구체 비중을 다루는 Case에서만 의미 |
| 연금개시 요건 (만 55세 / 가입기간 / 퇴직용 예외) | SRC-049, SRC-087 | 해당 없음 (29세) | 연금개시·수령 Case에서 P0 후보 |
| 디폴트옵션 적용 조건 (등록 전제, 대기기간) | SRC-089 | Known Context로만 처리 | 제도 세부 정확성 Out of Scope |
| 계약이전·실물이전 제약 (디폴트옵션 보유·상품변경 진행 중 이전 불가 등) | SRC-061, SRC-065 | 해당 없음 | 계약이전 Case에서 후보 |
| 세액공제·납입한도 (연 1,800만원 / 900만원) | SRC-087, SRC-063 | Out of Scope | 추가납·ISA Case에서 후보; 시점 의존 |
