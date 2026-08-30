# EVAL_001 — GC-01

## 1. Evaluation Metadata

- Case: GC-01 / Run: RUN_001 (`cases/GC-01/runs/RUN_001.md`)
- Evaluated At: 2026-08-31 / Evaluator: Claude (Evaluator role, separate context from Builder Gemma 4)
- Case Baseline: cases/GC-01/case.md (FROZEN 2026-08-31, commit 601aa1b) / Knowledge Pack: 601aa1b / Runtime: 601aa1bad52879a8ea2c0d46f9aa03aa0ec05660
- Evaluation Basis: case.md §5 (Must Consider / Must Not Assume / Required Confirmation / Acceptable Direction / Forbidden Behavior / Practical Usefulness); Verdict 정의 AGENTS.md §20.6

## 2. Verdict

**PARTIAL**

핵심 판단방향(만기 후 자동 재예치 없음 → 원리금보장 범위 안에서 재운용 안내, 연금 수령 계획 확인 선행, C1·C3 준수)은 Acceptable Direction 안에 있고 Critical Mistake·Hard Constraint 위반이 없다. 그러나 (1) 등록된 지켜드림 자동 적용을 "그대로 수용" 하는 현상유지 경로가 후보에 없고 오히려 열등한 경로로 프레이밍했으며, (2) Context에 전달된 K-002(지켜드림 = 3년제)·K-004(만기별 금리·월 한도·[04-12-17A]·계산기)·K-006(예보 한도 충돌)을 전혀 사용하지 않아 원리금보장 비교 축과 직원 확인 화면이 빠졌고, (3) 만기 1개월 전 예약변경 시점·채널(스타뱅킹 이용 중)·고유계정대 200만원 처리가 Brief에 없다.

## 3. Expected Judgment Check

| Must Consider | Result | Evidence |
|---|---|---|
| 시한과 만기 후 경로 3가지 | PARTIAL | reason: "자동 재예치되지 않으므로 … 현금성자산으로 상환된 후 대기 기간을 거쳐 디폴트옵션 적용" (경로 b·c 인식). 예약변경(경로 a)과 "만기 한 달 전부터 가능"(K-003)·6주 시계·지켜드림 3년제 잠김(K-002)은 미언급 |
| 원리금보장 범위 내 비교(만기·예보·한도·비대면) | PARTIAL | Cand.1 "저축은행 정기예금 등 고금리" 한 축만. GIC·특별제공·만기별 금리·잔여한도(K-004) 미사용 |
| 연금개시 요건 충족 ↔ 만기 길이 | MET | Cand.3, Brief "우선 연금 수령 계획을 확인하여 투자 기간 설정"(K-005 인용) |
| 고유계정대 200만원 운용지시 대상 | PARTIAL | situation·Unknown#2에 언급되나 방향·행동 없음 |
| 특별제공 금리·한도 = 직원 확인 항목 | MISSED | 화면·확인 행동 부재 |

| Must Not Assume | Result | Evidence |
|---|---|---|
| 자동 재예치 / 등록 DO 무시 | COMPLIANT | K-001 정확 인용 |
| 실적배당 필요 / 아무것도 불필요 | COMPLIANT | 후보 모두 원리금보장·DO 저위험 범위, 조건부 |
| 중도해지 갈아타기 | COMPLIANT | 언급 없음 |
| 예보 한도 단정 | COMPLIANT | 수치 언급 없음 (K-006 미사용이지만 위반도 없음) |
| 고객 무지/기결정 단정 | COMPLIANT | — |

| Required Confirmation | Result |
|---|---|
| 사용 계획·연금 수령 시작 시점 | IDENTIFIED (Unknown#1) |
| 선호 만기 길이(1년/3년) | MISSED |
| 원리금보장 유지 의사 | IDENTIFIED (Unknown#2) |
| DO 자동 적용 경로 수용 여부 | PARTIAL (Unknown#3은 알파드림 변경 의향만) |
| 비대면 가능 여부 / 내점 | MISSED (입력 "스타뱅킹 이용 중" 미사용) |
| (직원) 특별제공 금리·한도·발송이력 확인 | MISSED |

- Acceptable Direction: WITHIN — 원리금보장 내 재예치(Cand.1), 성향 범위 내 DO 변경(Cand.2), 수령 계획 확인 선행(Cand.3). **Gap**: "지켜드림 자동 적용 수용(현 상태 유지)" 경로 부재; reason이 "디폴트옵션에 맡기기보다 … 안내할 필요"로 배제 프레이밍.
- Forbidden Behavior: NO. 수치·상품명 생성 없음("저축은행 정기예금 등"은 유형). "2주 뒤 만기"(18일)는 경미한 부정확.

## 4. Critical Mistake Check

없음. 제도 Fact(자동 재예치 없음·DO 적용)는 정확, C1/C3 위반 없음, 실적배당 기본 방향 아님, 중도해지 권유 없음, 수치 생성 없음.

## 5. Constraint Check

- C1: PASS (Runtime validator PASS×3; Cand.1 안정형·Cand.2 안정추구형 라벨과 내용 정합; Brief에 상한 명시)
- C3: PASS (validator findings 0; Cand.2가 "알파드림 가입 가능"을 C3로 정확히 인용)
- C2: 해당 없음 (펀드 등급 언급 없음)

## 6. Grounding Check

- Grounded: 자동 재예치 없음·DO 적용(K-001), 안전자산 선호 판단 근거(K-003), 투자기간 재산정(K-005), C1/C3(K-008). 인용 K-ID는 전달 집합의 부분집합, 허위 인용 없음.
- Weak: Brief "전형적인 안전자산 선호 고객" — situation의 "분류될 가능성이 높습니다"가 Brief에서 확정으로 승격(경미). "빠른 안내가 필요" — K-003의 예약변경 시점 근거는 있으나 인용하지 않음.
- Under-used: K-002(3년제), K-004(비교 축·화면·계산기), K-006(예보 충돌), K-007(채널 안내 순서), K-009. 
- Source Traceability: PASS.

## 7. Observed Failures → Failure Map

| # | 관찰 | Severity | Failure Map |
|---|---|---|---|
| 1 | 현상유지(지켜드림 자동 적용 수용) 경로 부재 + 열등 프레이밍 | P1 | **F-005** (재현: CASE_001→GC-01) |
| 2 | 전달된 Knowledge 미사용(K-002/004/006) → 상품 비교 축·화면·만기 잠김 누락 | P2 | **F-006 (신규) Provided Knowledge Under-use** |
| 3 | 입력 Fact 미사용: 입금예정상품 미등록, LMS 발송, 스타뱅킹 이용 중 | P2 | **F-003** (재현) |
| 4 | Confirmation 축 누락: 만기 길이 선호, 채널 | P2 | **F-004** (재현) |
| 5 | 직원 다음 행동(화면·채널·시점) 부재 | P2 | **F-007 (신규) Employee Next Action Absent** |
| 6 | "가능성 높음" → "전형적인" 확정 (Brief) | P3 | **F-001** (재현, 경미) |

## 8. Candidate Failure Layer

- F-005: LLM Reasoning + Prompt/Schema(solution_candidates에 비변경 결과 자리 없음) — CASE_001과 동일 구조.
- F-006: Prompt/Grounding(Knowledge가 관련도 단서 없이 9건 평면 나열; Limitation/Relevance 미전달 설계) + LLM Reasoning.
- F-007: Prompt/Schema(employee_brief 지시에 화면·채널·시점 항목 없음) + Concept(D12가 Output에 없음).
- F-003/F-004/F-001: CASE_001과 동일 후보.

## 9. Evidence

RUN_001 §3(situation·unknowns), §6(reason), §7(Cand.1~3 condition), §9(brief); case.md §2 입력 "스타뱅킹 이용 여부: 이용 중", "입금예정상품 등록 여부: 미등록"; knowledge_pack K-002/K-004/K-006.

## 10. Suggested Direction (자동 수정 지시 아님)

Cross-case Evidence 축적 후 검토: (a) 비변경 결과 자리(F-005, 2/2 재현), (b) Knowledge 관련도 단서 또는 항목 수 축소(F-006), (c) employee_brief에 "직원 확인 화면/채널/시점" 구조(F-007). Human Gate 필요 여부: 없음 (Stop Condition 해당 없음).

> 이 Artifact는 생성 후 수정하지 않는다.
