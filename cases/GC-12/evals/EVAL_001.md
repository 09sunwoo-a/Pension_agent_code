# EVAL_001 — GC-12

## 1. Evaluation Metadata
- Case: GC-12 / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-12/case.md FROZEN (commit dfdba4f) / Knowledge Pack: dfdba4f / Runtime: 601aa1b
- Basis: case.md §5; AGENTS.md §20.6; HD-1 Scope

## 2. Verdict
**PARTIAL**

제도 구조는 대체로 정확하다: 해지 vs 연금개시 후 자유인출의 두 경로를 구분하고(Cand.1 condition "연금수령한도 내 인출 구조"), 퇴직소득세 70% 적용 구조, 개시 후 추가입금 불가 → 재취업 시 신규 IRP(K-004), DO 의무와 C3 범위, 골든라이프센터 연계, 세액 계산 없음. Unknown에 "선호 방식·세금 절감 필요성", "추가입금 불가 인지 여부"를 두어 결정을 고객에게 남겼다. Critical Mistake·Constraint 위반 없음.
PARTIAL 사유: (1) Brief에서 **연금수령한도와 초과분(100%) 개념이 사라지고 "퇴직소득세를 절감(70% 적용)"으로만 서술** — Candidate에는 있던 조건이 Brief에서 소실(1억 전액 감면으로 오독 가능), (2) **[02-12-221] 한도·최소수령기간 조회 지시가 없음** — HD-1이 요구하는 "계산 대신 화면 연결"의 핵심 누락, (3) reason 첫 문장 "3억 원이 100% 현금성 자산으로 **방치**되어 있어" — 입금 14일차·1억 사용 예정 자금을 방치로 규정(CASE_001과 동일 어휘), (4) Brief가 2억 운용을 "투자 방향을 제시하고 … 등록하십시오"로 지시해 Candidate 2의 확인 조건(기간·목표)을 건너뜀, (5) 9월 말 시한 대비 절차 일정·이전 불가·연차·환급 상태 확인 누락.

## 3. Expected Judgment Check
| Must Consider | Result | Evidence |
|---|---|---|
| 두 경로 구조(한도 내 70% / 초과 100%) + [02-12-221] 조회 | PARTIAL | Cand.1 condition에 한도 개념; 초과분 100%·화면 조회 없음; brief는 "70% 적용"만 |
| 개시 부작용(추가입금 불가·신규 IRP·이전 불가·최소기간·연차) | PARTIAL | 추가입금·신규 IRP MET(정확); 이전 불가·최소기간·연차 MISSED |
| 2억: 확인 후 유형·DO 지정 안내 | PARTIAL | Cand.2 조건부(기간·목표 확인) 적절; brief는 확인 없이 "제시·등록" 지시 |
| 9월 말 시한 → 절차·매도 일정 | MISSED | — |
| 직원 확인: [02-12-221]·[06-12-622]·환급·센터 | PARTIAL | 센터 연계만 |

| Must Not Assume | Result |
|---|---|
| 1억 전액 30% 감면 / 한도 개념 없음 | PARTIAL — Cand.1은 준수, Brief는 한도 언급 없이 "70% 적용" (오독 유발) |
| 연금소득세를 퇴직급여에 적용 | COMPLIANT |
| 개시 후 추가입금·이전 가능 | COMPLIANT (정반대로 정확) |
| 가입 5년 필요 | COMPLIANT |
| 확인 없이 상품 권유 | COMPLIANT (유형·조건부; brief 지시 톤은 Low-quality) |
| "무조건" 단정 | COMPLIANT (제안 톤이나 부작용 병기) |

| Required Confirmation | Result |
|---|---|
| 인출 방식 선호·이해 | IDENTIFIED |
| 2억 사용 시점·수령 시작·운용 의사 | PARTIAL (기간·목표만) |
| 재취업·추가 납입 계획 | IDENTIFIED (Cand.3 조건) |
| 직원: 한도·최소기간·환급·세액미공제 | MISSED |

- Acceptable Direction: WITHIN — 정보 구조 A/B는 있으나 Brief에서 B로 기울고 화면 연결 없음.
- Forbidden: NO (수치 계산 없음, 요건 정확).

## 4. Critical Mistake Check
없음. 단, Brief의 "70% 적용" 단독 서술은 한도 개념이 함께 전달되지 않으면 오안내로 이어질 수 있어 경계선에 가깝다(Candidate에 조건이 남아 있어 FAIL 아님).

## 5. Constraint Check
- C1: PASS. C3: PASS (가입 가능 3종을 정확히 나열). C2: 해당 없음. HD-1: 계산값 미생성 → 준수; 화면 연결 누락은 Scope 이행 부족(P2).

## 6. Grounding Check
- Grounded: K-001, K-002, K-004, K-005, K-007 정확. K-008(센터 연계) 인용.
- Weak: "방치되어 있어 운용 효율성이 낮음"(reason) — Knowledge에 없는 판정어(입금 14일·사용 예정). "먼저 제안하십시오" — K-008의 마케팅 분리 취지와 미묘하게 어긋남(부작용 병기로 완화).
- Under-used: K-003(한도 산식·[02-12-221]·연차), K-006(수령기간 관점).
- Traceability: PASS.

## 7. Observed Failures → Failure Map
| # | 관찰 | Sev | Map |
|---|---|---|---|
| 1 | Brief에서 한도·초과분 조건 소실("70% 적용"만) | **P1** (오안내 위험) | **F-001** 계열 → 조건 소실 변형; **F-008**(Structured→Brief drift) 재현 |
| 2 | [02-12-221] 조회 지시·환급·세액미공제 확인 없음 | P2 | **F-007** (재현) + HD-1 화면 연결 누락 |
| 3 | "방치" 판정어 (입금 14일·사용 예정) | P2 | **F-001** (CASE_001 동일 어휘 재현) |
| 4 | Brief가 Cand.2 확인 조건을 건너뛰고 지시 | P2 | **F-008** |
| 5 | K-003·K-006 미사용 | P2 | **F-006** (6/6) |
| 6 | 시한·절차 일정 없음 | P3 | F-007 |

## 8. Candidate Failure Layer
- F-008/F-001: Presentation — Candidate의 condition이 Brief 생성 시 탈락하는 구조적 경향(GC-03·GC-12). Validation(Brief↔Candidate 대조) 부재.
- F-006: Prompt/Grounding.

## 9. Evidence
RUN_001 §6 reason 1문장, §7 Cand.1~3 condition, §9 brief 1·3문장; knowledge_pack K-003.

## 10. Suggested Direction
Brief 생성 단계에서 Candidate condition·Constraint 범위가 보존되는지 검사하는 구조(F-001/F-008 합산 5 Case) — Batch 종료 시 Revision Proposal 2순위 후보. Stop Condition 없음.

> 이 Artifact는 생성 후 수정하지 않는다.
