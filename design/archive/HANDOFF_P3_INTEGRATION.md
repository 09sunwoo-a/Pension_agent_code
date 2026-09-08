# Handoff — P2 종료 시점의 Agent 상태 (통합 세션용)

- 작성: 2026-08-31, Session A (P2 Batch 3 종료 시점). 대상 독자: Knowledge Selection 등 다음 단계를 설계·구현할 **새 통합 세션**.
- 이 문서는 짧은 진입점이다 — 각 절의 원문 문서가 규범이며, 충돌 시 원문(HD > Spec > 이 문서)이 우선한다.

## 1. 현재 Agent Reasoning Pipeline (v3 — PRE-P2-REFINEMENT)

```
cases/<CASE>/canonical.json  (Layer 1: Canonical Evidence Object — 9-Block, Stable E-ID,
                              evidence_type×source_type 2축, supply 계약 포함)
  → prototype/canonical.py load_canonical()   [검증: E-ID·block·type·crm 위치·supply id]
  → derive()                 (Layer 2: 결정론 파생 D-id — 경과일·Window 증감·잔액-Flow 산술 대조·
                              만기 D-n·DO Rule Clock·연금개시요건. 금지 어휘 assert)
  → render_blocks()          (Layer 3: 9-Block 렌더 — ①~⑧ 시스템, ⑨ CRM 마지막, 경계 주석)
  + knowledge_pack.md        (K-item 5필드 — knowledge/ Registry 인용) + render_supply() (카드/원문/화면)
  + build_constraint_context (C1/C2/C3 — HD-2.1 deterministic 사전 전달)
  → SYSTEM_ROLE_V3 (원칙 1~19) + OUTPUT_INSTRUCTION_V3 (v3 Brief JSON Schema)
  → 단일 LLM 호출 (gemma-4-31b-it, API default)
  → parse → check_schema_v3 → deterministic validators
     (C1·C2·C3 / 금지어 / LaTeX / Evidence ID Provenance / supply_refs(Pool 밖·sellable=false·등급 초과)
      / screen_refs(미제공 FAIL·S1~S4 노출 REVIEW))
  → record(prototype/out/*.json) → render_run.py → cases/<CASE>/runs/RUN_00X.md (카드·원문·경로는 supply에서 복원)
```
- Dispatch: canonical.json 존재→v3 / input_v2.md→REV-002 / else→REV-001 (`runtime.py run_case`). 구 경로는 Frozen 기록 재현용 — 삭제 금지.
- Output: `management_judgment`(judgment/reasoning/must_confirm/E·K-ID 분리) + `next_actions` + `employee_brief`(S1~S5 — Decision & Action Brief).

## 2. P2에서 검증된 Boundary (보존 필수 — 위반 시 EVAL FAIL 근거였던 것들)

| Boundary | 검증 Case | 규범 위치 |
|---|---|---|
| Judgment-first·방향 중립 (6유형, Action 전 판단) | 전 Case | HD-6/REV-001 |
| Signal ≠ Intent (Sequence 강해도 관심 관찰까지) | GC-19 PASS | 축4, 원칙 4 |
| CRM ≠ ground truth·충돌 시 재확인이 유일 결론 | GC-20(판단층 PASS) | 축5, 원칙 5 |
| 관찰 상태의 의미 비승격 (방치/미운용/대기성 금지) | GC-18 FAIL→교정, GC-22 PASS | 원칙 6, SG-2, FC-2 |
| 확인되지 않은 실행경로의 Epistemic 유지 (가능/불가 비확정→확인 연결) | GC-23 PASS | HD-P2-GATE2 (1) |
| Knowledge Gap 비보충 (없는 원인·정의 생성 금지) | GC-21 PARTIAL→교정 | HD-P2-GATE2 (2), 원칙 19(a) |
| T3/PROVISIONAL/CONFLICT 지식 비승격 (HD-3의 화법층 적용) | GC-25 PARTIAL→교정 | HD-3, 원칙 19(c) |
| S2↔S3↔S4 조건성 보존 (SG-1) + S4 확실성 비인플레이션 | GC-20·21·25→교정 | 원칙 18·19, FC-1 |
| Bank Objective는 관리 필요성·추천사유 불가 | GC-19·23·25 PASS | HD-7, SG-3, G4 |
| 결정세액·한도 3필드 분리, 최종 계산값 금지 | GC-24 PASS | HD-1, HD-8 6 |
| Hard Constraint C1/C2/C3 + 미끼 회피 | 8/8 PASS | HD-2.1, deterministic |
| 화면 Reference = S5 단일 위치·supply id 참조만 | 8/8 (Pilot 3/3→0/8) | G3, screen_refs |

## 3. Failure Cluster 현황

- **F-001~F-012**: `cases/FAILURE_MAP.md` — REV-001/002에서 정의·대응된 기존 패턴.
- **FC-1 (Candidate)**: S4 화법층의 확실성 인플레이션 — P2 3/8 재현, 원칙 19+SG 보강으로 대응, 선택 Regression으로 해소 확인(§5의 P2_BATCH3_SUMMARY 종료 절 참조). **정식 F-번호 미부여** — 이후 Batch에서 재현 시 부여 검토.
- **FC-2 (Candidate)**: Interpretation→Judgment 의미 승격 (F-001의 판단층 변형) — GC-18 1회, 원칙 6 보강으로 대응.
- 관찰만 기록(규범 미정): 행동 신호의 고객 대면 화법 노출(GC-19·20), 주/부 포인트 우선순위 서술 정밀화(GC-22).

## 4. Knowledge 사용에서 관찰된 문제 (Selection 설계의 입력)

1. **Gap의 명시가 Gap 메움을 막는다 (P2의 핵심 발견)**: 부정 확인을 Limitation과 함께 명시한 GC-23은 Epistemic을 지켰고, "정의 자료 부재"만 적힌 GC-21은 원인을 생성했다(교정 전). → Selection이 K-item을 고를 때 **"무엇이 없는지"를 함께 공급하는 능력**이 품질 변수다.
2. **Authority 등급이 화법 확실성을 결정해야 한다**: T3 단독 지식(7/1 발급)이 화법에서 확정으로 승격됨(GC-25) → Selection은 K-item의 authority/status(T1~T3·PROVISIONAL·CONFLICT)를 메타데이터로 반드시 전달해야 한다.
3. **Limitation(Usage Boundary)은 본문만큼 중요**: REV-001 F-006 이래 일관 — K-item은 Knowledge/Case Relevance/Limitation/Authority/Source 5필드 전체가 전달 단위다. 요약·본문만 잘라 공급하면 과적용(F-002)이 돌아온다.
4. **bank_objective 태그의 유효성**: 태그된 Tip(HT-001)을 공급해도 모델이 취지만 활용(GC-22) — 원문 보존+태그 방식이 작동함. Selection도 태그를 유지·전달할 것.
5. **수동 동봉 상태의 활용률**: P2에서 공급된 K-item은 대체로 실사용됨(reasoning·S4 인용) — Selection 도입 시 비교 기준선.

## 5. Knowledge Selection Logic이 반드시 보존해야 할 원칙

1. **Frozen 불변**: 기존 canonical/knowledge_pack/RUN/EVAL은 Selection의 Golden Expected(회귀 기준)다 — 25 Case의 수동 pack이 selection 출력의 비교 대상. 수정 금지.
2. **K-item 5필드 온전 공급** (§4-3) + **Authority/Status 메타데이터** (§4-2) + **Gap 명시 능력** (§4-1).
3. **HD-3 Authority 순서**: 공식 > 행내 가이드 > Hot Tip. 충돌은 SC-xxx로 — Selection이 임의 통합·해소하지 않는다.
4. **세제·제도 Rule은 공식 Source만** (HD-8): rule_source/as_of/rule_id 추적. R4(위험자산 한도)는 공식 근거 확보 전 비활성 유지.
5. **Supply 계약 유지**: 모델은 id로만 참조, 카드/원문/경로는 렌더 복원. sellable/channels null은 사실로 보완 금지(HD-P2-GATE2 (4)). SC-001(예금자보호 한도) OPEN — 수치 비노출.
6. **Selection 자체는 Semantic Gate 대상**: 무엇을 고르는가가 판단을 바꾼다 — 도입은 Human Gate + 25 Case 회귀(수동 pack RUN vs selection pack RUN 비교)로.

## 6. 기존 Runtime의 재사용 가능 부분

| 재사용 | 위치 | 비고 |
|---|---|---|
| Canonical 3-Layer 전체 (load/derive/render/supply) | `prototype/canonical.py` | Selection과 독립 — 그대로 사용 |
| Deterministic validator 7종 + hard-fail 배선 | `prototype/runtime.py` §10 | Selection 도입과 무관하게 유지 |
| SYSTEM_ROLE_V3 원칙 1~19 / OUTPUT_INSTRUCTION_V3 | 〃 | Knowledge 공급 방식이 바뀌어도 판단·Brief 원칙은 불변 |
| C1/C2/C3 constraint context | 〃 | 〃 |
| RUN 렌더·기록 체계 (재현성 메타데이터 포함) | `prototype/render_run.py` | 〃 |
| EVAL 템플릿 (SG Gate + AQ 8축) | `design/EVAL_TEMPLATE_P2.md` | Selection 평가에도 §8(deterministic 전기)·SG 그대로 |
| knowledge/ Registry 5종 + K-REQ 인터페이스 | `knowledge/`, `design/KNOWLEDGE_REQUESTS.md` | Selection의 검색 대상 원천 — B-3 확장이 전제 조건 |
| **교체 대상**: `load_knowledge_items(case_id)` — Case별 수동 pack 파일 로드 | `prototype/runtime.py` | Selection Layer가 이 함수 하나를 대체하는 구조가 최소 침습 경로. 인터페이스(K-item 리스트 반환) 유지 시 하위 전부 무변경 |

## 7. 문서 지도 (통합 세션 필독 순서)

1. `golden/HUMAN_DECISIONS.md` — HD 전체 (특히 HD-1·2.1·3·7·8, HD-PRE-P2-INPUT/BRIEF, HD-PRE-P2-GATE1, HD-P2-GATE2)
2. `design/CANONICAL_CONTRACTS.md` / `design/INTERPRETATION_DESIGN.md` (축 1~8 + SG-1~3) / `design/EMPLOYEE_BRIEF_SPEC.md` v2 배너
3. `golden/P2_BATCH3_SUMMARY.md` (Batch 결과·Regression·종료 판정) / `cases/FAILURE_MAP.md`
4. `design/PARALLEL_WORKPLAN_A_B.md` (A/B 분업·소유권 — 통합 세션이 승계할 계약)
5. Pipeline 코드: `prototype/canonical.py` → `runtime.py` §10 → `render_run.py`
