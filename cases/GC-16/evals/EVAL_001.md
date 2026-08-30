# EVAL_001 — GC-16

## 1. Evaluation Metadata
- Case: GC-16 / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-16/case.md FROZEN (commit 47239e2) / Knowledge Pack: 47239e2 / Runtime: 601aa1b
- Basis: case.md §5; AGENTS.md §20.6; HD-3

## 2. Verdict
**PARTIAL** (PASS 경계)

이탈 대응의 핵심이 정확하다: 사전체크(불가 상품 2종·SBI 재확인·현금화 필요)를 situation에서 구성, 손실을 "숫자로 정확히 안내하여 고객의 의사를 재확인"(K-002), **실시간 거래는 은행 구조상 불가함을 인정**(허위 없음), 수수료는 비대면 전환(K-004)으로 조건부 대응, 분리 운용(K-005) 조건부 제안, ETF 라인업 수·순위 인용 없음, KPI·계열사·비방 없음, C1 정확. Critical Mistake 없음.
PARTIAL 사유: (1) **고객 결정권**("실시간이 핵심이면 이전이 합리적일 수 있음, 손실 고지 후 고객 결정, 이전 진행 시 절차 지원")이 명시되지 않고 Brief가 "은행에 남기는 분리 운용 검토"로 유지 방향에 기울어 있음, (2) 절차 항목(상대기관 확인전화 응답, 디폴트옵션 해지 후 재신청 가능성, 취소 절차) 미언급 — K-001 Operational 세부 미사용, (3) 핵심 사유·니즈 강도 확인이 Unknown에 없음(Candidate 조건에만 암시), (4) [04-12-613] 수수료 조회·계산기 등 화면 없음.

## 3. Expected Judgment Check
| Must Consider | Result | Evidence |
|---|---|---|
| 사전체크: 유형·불가 상품·손실·운용 공백·SBI 재확인 | MET | situation·Unknown#1·#2·Cand.1 |
| 사유를 사실 기반으로(실시간 불가·3분 분할·as-of / 수수료 절대금액·비대면 전환 / 타사 무료 조건) | MET (부분) | brief "은행 구조상 불가함을 인정"; Cand.3 "3분 분할매매 안내"; 수수료 실제 금액 확인(Unknown#3)·비대면 전환. 타사 조건 확인 미언급 |
| 이전 합리성 인정 + 손실 고지 후 고객 결정 | PARTIAL | 손실 고지·의사 재확인 MET; "이전이 합리적일 수 있음"·결정권 명시 없음 |
| 부분 대안 조건부 | MET | Cand.3 분리 운용(조건부) |
| 절차: 확인전화·해지 후 재신청·취소 | MISSED | — |
| 직원 확인 화면 | PARTIAL | 손실액 산출 언급, 화면번호 없음 |

| Must Not Assume | Result |
|---|---|
| 전부 가능 / 손실 없음 | COMPLIANT |
| "실시간 가능" 허위 | COMPLIANT (정반대로 인정) |
| 타사 무료 단정 | COMPLIANT (언급 없음) |
| 손실 인지·결정 확정 단정 | COMPLIANT (재확인) |
| 근거 없는 비교 | COMPLIANT |

| Required Confirmation | Result |
|---|---|
| 핵심 사유·니즈 강도 | PARTIAL (Cand. 조건) |
| 손실 인지·수용 | IDENTIFIED |
| 부분 이전 의향 | PARTIAL (Cand.3) |
| 확인전화 응답 계획 | MISSED |
| 직원: 실제 수수료·손실 계산 | IDENTIFIED (Unknown#2·#3) |

- Acceptable Direction: WITHIN — 사전체크→팩트→손실 고지→대안. Gap: 결정권·절차 지원 부재.
- Forbidden: NO.

## 4. Critical Mistake Check
없음.

## 5. Constraint Check
- C1: PASS (Cand.3 적극투자형 라벨 정합; brief 공격투자형 제외 명시). C3: PASS. C2: 해당 없음. HD-3: 불가 상품·현금화는 [06-AD-020] 결과(입력)로 확인된 사실로 사용 — 적절. 수치 생성 없음.

## 6. Grounding Check
- Grounded: K-001~K-005 정확. 허위 없음. 라인업 수 미인용(시점 의존 회피 — 적절).
- Weak: "은행의 제도적 한계와 대안 … 대응할 여지가 있어, 단순 전출 처리 전 상담이 필요"(reason) — 방어 프레임이 은은하나 팩트 기반이라 위반 아님.
- Under-used: K-001 Operational 세부(확인전화·재신청·취소), K-004 [04-12-613], K-007(위반 없음).
- Traceability: PASS.

## 7. Observed Failures → Failure Map
| # | 관찰 | Sev | Map |
|---|---|---|---|
| 1 | 절차 세부(확인전화·재신청·취소)·화면 미사용 | P2 | **F-006** (8/8) / **F-007** (경미) |
| 2 | 고객 결정권·"이전이 합리적일 수 있음" 미명시 → 유지 방향 기울기 | P2 | **F-005** 변형(이전 진행 = 비변경? — 여기서는 "고객 결정 경로" 부재) — Cross-case 6 |
| 3 | 핵심 사유·확인전화 응답 확인 누락 | P3 | **F-004** (경미) |
| — | 허위·비방·KPI 없음, 손실 고지·인정 톤 | — | F-009 미재현 |

## 8. Candidate Failure Layer
- F-005 변형: 이탈 Case에서 "고객의 이전 결정을 지원하는 경로"가 Solution 자리에 없음 — solution_candidates가 "은행 내 대안"으로만 채워지는 구조(Concept/Schema).

## 9. Evidence
RUN_001 §3, §6, §7 Cand.1~3, §9 brief; knowledge_pack K-001(절차), K-005(결정 존중).

## 10. Suggested Direction
Solution 후보에 "고객 결정 경로(이전 진행 지원 / 현상유지)"의 자리가 없다는 점이 F-005의 본질로 보임(6 Case). Stop Condition 없음.

> 이 Artifact는 생성 후 수정하지 않는다.
