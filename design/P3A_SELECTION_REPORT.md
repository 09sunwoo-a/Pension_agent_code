# P3-A Minimal Knowledge Selection — 구현·비교 결과 (2026-08-31)

- 범위: `design/HANDOFF_P3_INTEGRATION.md` §6의 최소 침습 경로 — `load_knowledge_items(case_id)` 하나를 Minimal Selection Layer로 대체(옵트인). Canonical 3-Layer / SYSTEM_ROLE_V3 / OUTPUT_INSTRUCTION_V3 / Hard Constraint / Validator / RUN·EVAL 체계 **무변경**.
- 구현물: `prototype/selector.py` (Selection Layer) + `design/P3A_KNOWLEDGE_NEEDS.md` (Human-defined Need 전사) + `prototype/runtime.py`의 dispatch 1곳.
- Frozen 불변: 기존 knowledge_pack.md·RUN·EVAL·canonical.json 무수정. 환경변수 `P3A_KNOWLEDGE_SELECTION=1`일 때만 Selector 경로 — 기본 경로는 기존과 동일 동작 확인(GC-22 dry-run 비교).

## 1. 구현 내용

```
load_knowledge_items(case_id)
  ├─ (기본) Frozen knowledge_pack.md 파싱 — 기존 그대로 (_load_knowledge_items_manual)
  └─ (P3A_KNOWLEDGE_SELECTION=1) selector.load_knowledge_items_selected
       [1] Knowledge Need 로드 — design/P3A_KNOWLEDGE_NEEDS.md (수동/Human 정의 유지:
           기존 K-REQ·Frozen pack 구성에서 전사, Selector는 Need를 생성하지 않음)
       [2] 후보 탐색 — OFFICIAL_KNOWLEDGE(OK)·KNOWLEDGE_GAPS(KG)의 topics/
           applicability_tags/topic 토큰이 Need topic 구절에 포함되면 후보 (정규화 부분일치)
       [3] status gate — SUPERSEDED 제외(로그), PROVISIONAL/CONFLICT는 채택+기계 flag
       [4] authority gate — 제도·세제·Eligibility·실행가능성 purpose는 T1/T2만 판단 근거.
           T3/Public 단독이면 배제하지 않고 "확인 필요 상태"로 강등 전달
       [5] Gap — KG 매칭 시 consume_text가 K-item 본문(1급 명시). 매칭 0건이면 합성 Gap
           ("현재 확인한 Knowledge 범위에서 확인되지 않는다" — 불가/불존재 승격 금지 문면)
       [6] manual_keep — TALK/HT/PRD/SCR 계열 항목은 Frozen pack에서 원문 유지(자동화 범위 밖)
       → 기존과 동일한 K-item 5필드 구조 반환 → 이하 파이프라인 무변경
```

- Authority와 Relevance는 단일 점수로 합산하지 않음 — gate 순서 고정(status→authority), relevance는 match 토큰 수로 로그에만 기록.
- 관측성: Case별 selection log `prototype/out/p3a_selection_<CASE>.json` (need→후보→gate→채택/flag, Registry sha256).
- LLM/Vector/Embedding/Reranker/2-call 분리/Product 자동 Selection: 구현하지 않음 (지시 준수).

## 2. 기존 Runtime에서 유지한 부분

Canonical load/derive/render/supply · C1/C2/C3 constraint context · SYSTEM_ROLE_V3 원칙 1~19 · OUTPUT_INSTRUCTION_V3 · deterministic validator 7종 · RUN 기록·render 체계 — 전부 무변경. 비교 dry-run에서 4 Case 모두 knowledge_context 외 프롬프트 섹션(system/customer/constraint/output) 완전 동일 확인.

## 3. Case별 Selected Knowledge / Gap (B = Selector pack)

| Case | Selector 채택 (need별) | 명시 Gap | flag |
|---|---|---|---|
| GC-21 | KN-01: OK-007 / KN-02: OK-006 / manual: TALK 화법 | **KG-001** (수익률 정의 gap — consume_text 전문) | OK-007 PROVISIONAL "확정 Fact 아님·확인 필요" 기계 부착 |
| GC-23 | KN-01: OK-002 / KN-02: OK-003·OK-011·(OK-009†) / manual: GIC(PRD 연계) | **KG-002** (부분이전 실행경로 미확인 — 가능/불가 단정 금지) | — |
| GC-24 | KN-01: OK-008 / KN-02: OK-009·(OK-015†·OK-011†) / KN-03: OK-006 | **KG-005** (결정세액 조건의 행내 T1/T2 근거 gap) | — |
| GC-25 | KN-01: OK-009·(OK-008†·OK-015†) / KN-02: OK-011·OK-003 | **KG-004** (7/1 발급·추징의 공식 근거 gap — "특정 해지 시점이 유리하다는 확정 판단 근거 사용 금지") | — |

† = over-selection (Human pack에 없던 항목 — §5).

## 4. Human Pack 대비 결과

**Pack-level 비교 (실행 완료)**:

| 축 | 결과 |
|---|---|
| 올바른 Knowledge 선택 | **Recall 12/12** — 4 Case의 Human pack이 인용한 OK 원천(OK-002/003/006/007/008/009/011) 전부 회수. **Precision: over-selection 5건**(§5) |
| Authority/Status 유지 | **4/4 유지** — Registry authority·as_of·status 원문 전달 + PROVISIONAL 기계 flag(GC-21). GC-25의 T3 단독 서술은 OK-009 Limitation 원문("Hot Tip 1건 단독 — 확정 사실 사용 금지") + KG-004로 이중 전달 — Human pack보다 강화 |
| Gap 명시 | **4/4 명시** — Human pack은 Gap을 K-item Limitation 산문에 내장(GC-21에서 S4 위반이 발생했던 형태, Study P-1(a)); Selector pack은 KG consume_text를 독립 K-item으로 1급 전달(GC-23 PASS를 만든 형태의 구조화) |
| Pack 크기 | +22%~+64% (prompt 13.0→15.9k / 14.2→19.9k / 12.9→19.6k / 12.1→19.8k chars) — Registry Content verbatim 전달 + over-selection 영향. F-006/F-002 재발 조건(Study P-6)으로 RUN 관찰 필요 |
| Judgment 변화 / Hallucination / Consumption | **미검증 — RUN 불가** (본 세션 환경에 GEMINI_API_KEY 부재). dry-run으로 프롬프트 조립·validator 배선까지만 확인 |

**Human pack과의 질적 차이 2건 (RUN 관찰 대상)**:
1. Case Relevance가 기계 생성("Need XX 대응: <need_text>") — Human의 Case 맞춤 서술("이 고객의 화면에는 -8.0%와 +12.0%가 함께 표시된다")보다 약함. F-006(Under-use) 리스크.
2. OK Content verbatim에 supply 밖 화면번호 다수 포함([04-10-099] 등) — 모델이 인용하면 `validate_screen_refs` FAIL로 차단되나(안전망 정상), VALIDATION_ERROR율 상승 가능.

## 5. Failure 분류

| 관찰 | 분류 | 근거 |
|---|---|---|
| Over-selection 5건: OK-009→GC-23, OK-015·OK-011→GC-24, OK-008·OK-015→GC-25 | **Selection Failure** (정밀도) | Retrieval은 필요 항목을 전부 회수(Retrieval Failure 아님), Authority/Gap 처리도 정상. 원인은 짧은 일반 토큰("중도해지"·"세액공제"·"기타소득세")의 부분일치 단독 매칭 — 채택된 항목 자체는 유효 지식이라 유해성은 낮으나 pack 희석 |
| Retrieval / Authority / Gap Failure | **미발생** | Recall 12/12, 등급 유지 4/4, Gap 명시 4/4 |
| Consumption / S4 Semantic Failure | **판정 불가 (RUN 미실행)** | FC-1(S4 확실성 인플레이션)은 pack이 정확해도 발생 가능(P2 확인) — Selector 도입 여부와 독립 축이므로 RUN 비교 시 P2 FC-1과 혼동하지 않도록 EVAL에서 분리 판정 필요 |

## 6. 필요한 최소 Revision

1. **매칭 정밀도** (Selection Failure 대응): 4자 이하 일반 토큰의 단독 부분일치 억제, 또는 "정확 일치 ≥1 또는 매칭 토큰 ≥2" 규칙. Selection 규칙 변경 = Semantic Gate 대상이므로 Human 승인 후 적용.
2. **RUN 비교 실행**: GEMINI_API_KEY 확보 후 4 Case × (Human pack / Selector pack) RUN + EVAL — Judgment 불변·Hallucination·F-006 재발·screen_refs FAIL율 확인. 이것이 완료되어야 §4의 미검증 축이 닫힘.
3. (관찰 후 판단) Content verbatim 길이: matched-topic 불릿만 발췌하는 규칙은 의미 개입이므로 RUN에서 F-006 재발이 관찰될 때만 Human Gate 상정.

## 7. P3-A 종료 판정 (제안)

**조건부 종료 가능.** 목표였던 "사람이 넣던 Official Knowledge/Gap 부분의 최소 Selector 대체"는 구현·검증됨(인터페이스 무변경, Frozen 무영향, Recall 100%, Gap 1급 명시, Authority 보존). 잔여 2건 — ① over-selection 최소 revision의 Human 승인, ② API 키 확보 후 RUN-level A/B 비교 — 가 닫히기 전에는 Selector를 기본 경로로 전환하지 않는다(현재 옵트인 유지).
