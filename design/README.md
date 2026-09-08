# design/ — 무엇이 살아있고 무엇이 끝났나

이 폴더는 단계(REV-002 → Pre-P2 → P2 → P3)를 지나며 쌓인 설계 문서·Spec·인수인계·실험 보고가
한 곳에 있다. 파일은 옮기지 않았다 — `golden/HUMAN_DECISIONS.md`·`prototype/REVISIONS.md`·Case 문서가
지금 경로로 인용하기 때문이다. 대신 이 표가 어느 문서를 지금 기준으로 읽어야 하는지 정한다.

## 지금도 규범인 문서 (새 Case·Runtime 작업이 따른다)

| 파일 | 역할 |
|---|---|
| `CANONICAL_CONTRACTS.md` | `canonical.json` 9-Block 입력·supply 계약 — Loader·Renderer·Brief v3·Case 작성의 공통 계약 |
| `EVIDENCE_PACK_SPEC.md` | Customer Evidence Pack 규범 (v2). v1 본문은 REV-002 종료 시점 기록으로 같은 파일 하단에 보존 |
| `EMPLOYEE_BRIEF_SPEC.md` | 직원용 Brief S1~S5 규범 (v2). v1 본문은 같은 파일 하단에 보존 |
| `INTERPRETATION_DESIGN.md` | 9-Block 입력 → Judgment 6유형 연결 — SYSTEM_ROLE v3·Evaluator 해석 기준의 원천 |
| `EVAL_TEMPLATE_P2.md` | v3 경로 Case (GC-18~25 이후) 의 Evaluation 형식 |
| `PRE_P2_REFINEMENT_PROPOSAL.md` | Human 승인된 입력 아키텍처 방향 (HD-PRE-P2-INPUT) |
| `PARALLEL_WORKPLAN_A_B.md` | Session A(Validation) × Session B(Knowledge Build) 운영 계약 — `knowledge/**` 소유권의 근거 |
| `KNOWLEDGE_REQUESTS.md` | K-REQ 대장. 두 세션이 함께 편집하는 유일한 파일 |

## Human Gate 대기 (닫히지 않았고 진행도 안 됨)

| 파일 | 상태 |
|---|---|
| `KNOWLEDGE_ARCHITECTURE_STUDY.md` | Design Study — 구현 없음. P3 결과(`P3_RUN_COMPARISON.md`) 가 Freeze 상정을 제안 |
| `P2_BATCH3_CANDIDATES.md` | 헤더는 «Gate ② 대기» 이지만 GC-18~25 는 이미 RUN/EVAL 까지 끝나고 `golden/P2_BATCH3_SUMMARY.md` 로 종료됐다. 헤더가 트리보다 뒤처져 있다 |

## 종료된 기록 (역사 — 읽되 따르지 않는다)

| 파일 | 무엇의 기록인가 |
|---|---|
| `INPUT_BRIEF_WORK_PLAN.md` | REV-002 작업 계획 Step 1~6 — COMPLETE |
| `HANDOFF_INPUT_BRIEF_PLAN.md` | 위 계획의 세션 투입 프롬프트 |
| `TARGET_CONCEPT.md` | REV-002 대상 개념 (Human 확정) — REV-002 는 CLOSED |
| `HANDOFF_P3_INTEGRATION.md` | P2 종료 시점 상태 인수인계 — 다음 단계(P3) 는 이미 실행됨 |
| `HANDOFF_B3_FULL_EXPANSION.md` | Knowledge B-3 전수 확장 프롬프트 — 2026-09-01 완료 |
| `P3A_KNOWLEDGE_NEEDS.md` · `P3B_PRODUCT_NEEDS.md` | P3 실험의 Human-defined 입력 |
| `P3A_SELECTION_REPORT.md` · `P3B_SELECTION_REPORT.md` · `P3_RUN_COMPARISON.md` · `P3_HYBRID_INTEGRATION_REPORT.md` | P3 Selection 실험 보고 (2026-08-31). Run record 는 `prototype/p3_runs/` |
| `evidence/` (5건) | REV-002 Step 1 원자료 — Case 역추적·Excel 필드·화면/Hot Tip 조사·Brief 감사. `SCREENS_HOTTIPS_INVENTORY.md` 의 화면 14건은 전부 `knowledge/SCREEN_REGISTRY.md` 에 흡수됐다 |

`evidence/P0_CUSTOMER_CONTEXT_INVENTORY.md` 가 인용하는 `design/CUSTOMER_CONTEXT_INVENTORY_DRAFT.md` 는
미승인 초안으로 main 에서 제거됐다(커밋 937235c). 원문은 `git show 1de4ea8:design/CUSTOMER_CONTEXT_INVENTORY_DRAFT.md`.
`P3_HYBRID_INTEGRATION_REPORT.md` 가 언급하는 `P3C_LLM_SELECTION_REPORT.md` 는 애초에 작성된 적이 없다(문서 자체가 그렇게 적고 있다).
