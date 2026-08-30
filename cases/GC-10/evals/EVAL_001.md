# EVAL_001 — GC-10

## 1. Evaluation Metadata
- Case: GC-10 / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-10/case.md FROZEN (commit 88f7f17) / Knowledge Pack: 88f7f17 / Runtime: 601aa1b
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PARTIAL**

제도 정확성이 높다: 개시를 관리 목표로 두지 않고(개시 강요 없음), 만기 후 6주 알파드림1 적용 경로·자동 재예치 없음(K-005), 자동이체 진행 중 지급거래 제약·개시 후 추가입금 불가→신규 계좌(K-002), 세액 미공제 등록 확인(Unknown#2), 골든라이프센터 연계(K-008)를 모두 정확히 짚었고, situation에 [사실]/[추론] 표기를 스스로 붙였다. C1/C3 위반·Critical Mistake 없음.
PARTIAL 사유: (1) Brief에서 "국민연금 수령(63세) 전까지 운용을 희망하시므로"로 **고객이 말하지 않은 시점을 의사로 확정**(입력은 "당분간 운용 지속" + 국민연금 63세 언급) — F-001, (2) 수령방식 3종·한도/연차·인출순서의 **구조 정보(K-003)와 "자유인출만 ETF 운용 가능"** 을 전혀 다루지 않고 센터 연계로만 처리 — 이 고객은 채권혼합 ETF를 보유하므로 수령방식 선택에 직접 영향, (3) 투자가능기간=수령 종료 시점·TDF2030 유지 관점(K-004) 미사용, (4) 재취업·추가 납입 계획 확인 누락, 화면([02-12-221]/[06-12-622]) 미제시.

## 3. Expected Judgment Check
| Must Consider | Result | Evidence |
|---|---|---|
| 의사 존중 → 개시는 목표 아님; 관리 = 만기 + 정보 준비 | MET | reason 3항, Cand.2 조건부("희망 시") |
| 만기 경로 3가지 / 알파드림1 | MET | brief "6주 후 디폴트옵션(알파드림1)" |
| 수령 시작 시점 ↔ 만기 길이·유동성 | PARTIAL | Unknown#3(개시 희망 시점); 만기 길이 연결 없음 |
| 개시 전 정보: 자동이체·추가입금·이전·세액미공제·수령방식·한도/연차·자유인출 ETF | PARTIAL | 자동이체·추가입금·세액미공제 MET; 이전 불가·수령방식 3종·한도/연차·ETF 조건 MISSED |
| 투자가능기간 = 수령 종료; TDF2030 유지 | MISSED | K-004 미인용 |
| 연금수령 포트폴리오 유형 | MISSED | — |
| 직원 화면·연계 | PARTIAL | 골든라이프센터 MET; 화면번호 없음 |

| Must Not Assume | Result |
|---|---|
| 즉시 개시 단정 | COMPLIANT |
| 개시 후 추가입금·이전 가능 | COMPLIANT (정반대로 정확) |
| 61세 → 안전자산 100% | COMPLIANT (실적배당 매도 언급 없음) |
| 국민연금 63세 → IRP 63세 개시 확정 | **VIOLATED (Brief, 경미)** — "63세 전까지 운용 희망" 확정 표현; Cand.2 조건은 "희망 시"로 유지 |
| 한도·세액 수치 생성 | COMPLIANT |

| Required Confirmation | Result |
|---|---|
| 수령 시작 시점·방식·기간 | PARTIAL (시점만) |
| 만기 자금 만기 길이·사용 계획 | PARTIAL (방향만) |
| 재취업·추가 납입 계획 | MISSED |
| 세액공제 미신청분 | IDENTIFIED |
| TDF2030 유지 의사 | MISSED |

- Acceptable Direction: WITHIN. Gap: 수령 구조 정보 부재(HD-1 Scope 내 항목을 센터로만 위임), ETF·수령방식 연결 없음.
- Forbidden: NO.

## 4. Critical Mistake Check
없음. 자동이체 상태를 반영한 안내(무시하지 않음), 요건 정확.

## 5. Constraint Check
- C1: PASS (Cand.1 안정추구형). C3: PASS. C2: 해당 없음.

## 6. Grounding Check
- Grounded: K-002(제약), K-005(만기·DO), K-006, K-008. 정확.
- Weak: "63세 전까지 운용 희망"(brief) — 입력 초과 추론의 확정화. situation의 [추론] 표기는 좋은 관행이나 Brief에서 사라짐(F-001 전형).
- Under-used: K-001(요건≠의무 — 결과적으로 준수), **K-003**(수령 구조·자유인출 ETF), **K-004**(수령기간·TDF), K-007(수령 중 AI일임 제외), K-009.
- Traceability: PASS.

## 7. Observed Failures → Failure Map
| # | 관찰 | Sev | Map |
|---|---|---|---|
| 1 | 63세 추론을 Brief에서 의사로 확정 | P3 | **F-001** (4 cases) |
| 2 | K-003/K-004 미사용 → 수령방식·한도/연차·ETF 조건·TDF 유지 관점 누락 | P2 | **F-006** (5/5) |
| 3 | 재취업·추가 납입·TDF 유지 의사 미확인 | P2 | **F-004** (5 cases) |
| 4 | decision "적극적인 관리 필요" 라벨 vs 정보안내 성격 | P3 | **F-005** 변형(라벨) — 경미 |
| 5 | 화면번호 없음(연계처는 있음) | P3 | **F-007** (경미) |

## 8. Candidate Failure Layer
- F-006: 9건 Knowledge 중 제도 구조(K-003)처럼 긴 항목이 전혀 인용되지 않음 — Prompt/Grounding(관련도 단서 없음) + LLM Reasoning(센터 연계로 대체하는 경향).
- F-001: Presentation.

## 9. Evidence
RUN_001 §3 situation [추론] 표기, §6 reason, §7 Cand.1~3, §9 brief 2문장; case.md §2 상담이력; knowledge_pack K-003/K-004.

## 10. Suggested Direction
HD-1 Scope 내 "구조 정보"가 센터 연계로 대체되는 경향 → Batch 종료 시 Employee Brief 구조(정보안내 항목 자리) 검토 후보. Stop Condition 없음.

> 이 Artifact는 생성 후 수정하지 않는다.
