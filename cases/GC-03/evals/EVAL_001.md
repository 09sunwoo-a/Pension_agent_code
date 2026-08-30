# EVAL_001 — GC-03

## 1. Evaluation Metadata
- Case: GC-03 / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-03/case.md FROZEN (commit 59e69ba) / Knowledge Pack: 59e69ba / Runtime: 601aa1b
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PARTIAL**

핵심 판단방향이 Golden 경계에 정확히 들어온다: "단순 미운용으로 단정하기 전 자금 사용 계획 확인"(K-001 인용)을 첫 Candidate로 두고, 디폴트옵션 미등록의 의미("미등록 시 향후 자동 운용이 불가능")와 지정 의무를 제도안내로 다루며, 53세 개시 불가를 정확히 말하고, 운용 방향은 "사용 계획이 없으며 운용 의사가 확인된 경우"의 조건부·유형 수준에 그친다. Critical Mistake·Constraint 위반 없음.
PARTIAL 사유: (1) **55세 전 인출 = 해지·퇴직소득세 전액** 이라는 세금 구조(K-004)를 전혀 쓰지 않아 "왜 55세 전 사용 여부를 물어야 하는지"의 근거가 빠졌고, (2) 과세이연 환급 처리 상태 확인(K-005)·직접/위임 선호·디폴트옵션 인지 여부가 Confirmation에 없으며, (3) Brief가 C1을 "그 이하의 위험수준(안정형, 안정추구형) 내에서만"으로 **과도하게 축소 재진술** 하여 Candidate 3("안정형~위험중립형")과 모순되고, (4) "당분간 현 상태 유지 가능" 경로가 명시되지 않았다.

## 3. Expected Judgment Check
| Must Consider | Result | Evidence |
|---|---|---|
| 입금 7일차·입금사유 → 대기자금 가능성, 미운용 확정 불가 | MET | reason "입금 후 약 1주일 … 단순 미운용으로 단정하기 전 … 확인" |
| DO 미등록 → 자동 운용 없음, 지정 의무 = 제도안내 | MET | reason·Cand.2·brief |
| 55세 미만 → 개시 불가; 인출=해지·퇴직소득세 → 사용 시점 질문 | PARTIAL | 개시 불가는 정확(brief). 세금 구조(K-004) 미언급 — 질문의 근거 부재 |
| 사용 시점 확인 후 유형 선택 | MET | Cand.3 condition |
| "생각해 보겠다" 이력 → 강권 없이 | MET | brief "무리한 운용 권유에 앞서" |
| 직원 확인: 입금사유·환급 상태·DO 안내 경로 | PARTIAL | 입금사유는 known_facts에 사용; 환급 상태·경로 없음 |

| Must Not Assume | Result |
|---|---|
| 방치·미운용 규정 | COMPLIANT |
| 개시 가능 | COMPLIANT |
| 미등록인데 자동 운용 | COMPLIANT (정반대로 정확) |
| 재취업·인출 계획 특정 | COMPLIANT (Unknown으로) |
| C1/C3 초과 | COMPLIANT |
| 확인 없이 장기 상품 권유 | COMPLIANT |

| Required Confirmation | Result |
|---|---|
| 사용계획·시점·재취업 | IDENTIFIED (Unknown#1·#2) |
| 운용 의사·직접/위임 선호 | PARTIAL (Cand.3 condition "운용 의사 확인"; 방식 선호 없음) |
| DO 미등록 인지·지정 의사 | PARTIAL (Cand.2 condition은 상태 확인만) |
| 환급 처리 상태·입금사유 (직원) | MISSED / MET |
| 고객의 고민 내용 | MISSED |

- Acceptable Direction: WITHIN — 확인 우선 + 제도안내 + 조건부 유형. Gap: 현 상태 유지(당분간) 경로 미명시; 55세 전 인출 세금 구조 정보 없음.
- Forbidden: NO.

## 4. Critical Mistake Check
없음.

## 5. Constraint Check
- C1: PASS (validator; Cand.3 위험중립형 라벨 정합). **단 Brief의 재진술 오류**: "위험중립형을 상한으로 하여, 그 이하의 위험수준(안정형, 안정추구형) 내에서만" — 위험중립형 자체가 허용됨에도 제외한 것처럼 서술. 위반은 아니나 직원 오독 유발(§7 #4).
- C3: PASS (모두드림 미언급). C2: 해당 없음.

## 6. Grounding Check
- Grounded: K-001(확인 우선), K-002(DO 의무·미등록 의미), K-003(개시 요건), K-006(목표수익률·기간), K-007. 허위 인용 없음.
- Under-used: K-004(세금 구조), K-005(환급 전 제한), K-008(KPI 분리 — 위반 없음).
- Weak: "고액의 퇴직금 … 100% 현금성자산으로 유지되고 있으며 … 때문입니다"(reason 첫 문장)가 관리 필요 근거의 첫 자리에 옴 — 이어지는 문장이 단정을 막아 위반은 아님.
- Traceability: PASS.

## 7. Observed Failures → Failure Map
| # | 관찰 | Sev | Map |
|---|---|---|---|
| 1 | K-004(인출 세금 구조)·K-005(환급 확인) 미사용 → 질문 근거·직원 확인 누락 | P2 | **F-006** (3/3) |
| 2 | 확인 축 누락: 직접/위임 선호, DO 인지, 고민 내용 | P2 | **F-004** (재현) |
| 3 | "당분간 현 상태 유지" 경로 미명시 | P2 (이 Case는 확인 우선이 핵심이라 P1 아님) | **F-005** (4/4, 경미) |
| 4 | Brief에서 C1 범위를 축소 재진술 (위험중립형 제외) — Candidate와 모순 | P2 | **F-008 (신규) Constraint Restatement Drift** |
| 5 | 스타뱅킹 이용·입금예정상품 미등록 미사용 | P3 | **F-003** (재현) |
| 6 | 화면·경로 없음 (DO 등록 경로, 04-12-644, 환급) | P2 | **F-007** (재현) |

## 8. Candidate Failure Layer
- F-008: Presentation / LLM Reasoning — 구조화 출력(candidate risk_level)은 정확하나 Brief 서술에서 Constraint 의미가 변형됨. F-001(Uncertainty Loss)과 같은 "Structured → Brief 의미 변형" 계열.
- F-006: Prompt/Grounding (Knowledge 8건 평면 나열).

## 9. Evidence
RUN_001 §3, §6, §7 Cand.1~3, §9 brief 마지막 문장; knowledge_pack K-004/K-005.

## 10. Suggested Direction
Structured→Brief 의미 변형(F-001, F-008)이 2계열로 누적 — Brief 생성 단계의 Validation(candidate 라벨과 brief 진술 대조) 후보. Stop Condition 없음. Human Gate 불필요.

> 이 Artifact는 생성 후 수정하지 않는다.
