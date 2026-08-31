# P3-C LLM Selector Baseline Experiment — 결과 보고 (2026-08-31)

- 목적: P3-A/B의 deterministic Selector와 **동일한 입력(Human-defined Need)·출력(K-item/ProductCandidate) 경계**를 유지한 채, 관련성 판단만 LLM(gemma-4-31b-it, Decision Agent와 동일 모델·별도 Selector 프롬프트)에 위임했을 때의 Selection Precision 비교. 기존 Selector 폐기·대체 아님 — Mock Baseline Experiment.
- 대상: Knowledge GC-21·23·24·25 / Product GC-18·20·22·25 (기존 Case 재사용, 신규 Case 없음). Frozen·기존 구현 무수정.
- 금지사항 준수: Vector/Embedding/Reranker/Need 생성/Ontology/stance·situation tag/Registry 개편/HT·TALK·SCR retrieval — 전부 미구현.

## 1. 구현 내용

- **변경 파일**: `prototype/llm_selector.py` (신규 — Knowledge/Product 두 함수, 과도한 Framework 없음) / `prototype/runtime.py` seam 2곳 (`P3A_LLM_SELECTION=1`·`P3B_LLM_SELECTION=1` 옵트인 분기 — 기본값·P3-A/B 경로 완전 보존, GC-22 기본 dry-run 동일 동작 확인).
- **LLM Input**: Human-defined Need 원문(P3A_KNOWLEDGE_NEEDS / P3B_PRODUCT_NEEDS 그대로 — Need 생성 없음) + Compact Registry Index. Index는 **Registry 필드 verbatim만** (OK: id/title/topics/applicability_tags/authority/status ≈4.4k chars; KG: id/title/topic/gap_type/what_is_missing/status ≈1.8k; PRD: 27항목 id/name/type/grade/maturity/return/특성/status/sellable/channels/as_of ≈8.8k — GIC 라인업 행은 `PRD-018|<상품명>` 조합 식별). short description 창작 없음.
- **LLM Output**: `{selected_ok_ids, selected_gap_ids, selection_reason}` / `{selected_product_ids, selection_reason}` JSON만. selection_reason은 로그 전용 — **K-item Case Relevance에 넣지 않음**(기계 문구 사용), Decision Agent에 미전달.
- **LLM 이후 deterministic Gate 유지**: ID 실존 검증 → SUPERSEDED 제외 → PROVISIONAL/CONFLICT flag → authority gate(T1/T2 미달 시 "확인 필요 상태" 강등 — P3-A와 동일) → 카드 완결성 gate(P3-B `_card_complete` 재사용) → **Registry 원문 deterministic load** → 기존 K-item 5필드/ProductCandidate 계약. null/status/as_of 무변형. GC-25 Product는 needs=none이므로 LLM 호출 없이 빈 Pool(정상).
- Call 구조: Case당 Selector 1 call (Knowledge 4 + Product 3 = 7 live calls). 무료 티어 rate limit(429)은 transport 재시도로 처리. 로그: `prototype/out/p3c_knowledge_<CASE>.json` / `p3c_pool_<CASE>.json` (Registry sha 포함).

## 2. Knowledge Selection 비교 (OK 기준; KG 별도 행)

Human = Frozen pack 인용 OK / Deterministic = P3-A 재현 실행(보고서와 일치 확인) / LLM = 본 실험.

| Case | Human | Deterministic | LLM | Miss (vs Human) | Extra (vs Human) |
|---|---|---|---|---|---|
| GC-21 | OK-007·006 | OK-007·006 (+KG-001) | OK-006 (+KG-001) | **OK-007** | 0 |
| GC-23 | OK-002·003·011 | OK-002·003·011 **+OK-009†** (+KG-002) | OK-002·003 (+KG-002) | **OK-011** | 0 |
| GC-24 | OK-008·009·006 | OK-008·009·006 **+OK-015†·011†** (+KG-005) | OK-008·009·006 (+KG-005) | 0 | 0 |
| GC-25 | OK-009·011·003 | OK-009·011·003 **+OK-008†·015†** (+KG-004) | OK-009·011 (+KG-004) | **OK-003** | 0 |

- **Recall**: Human 필수 OK 12개 기준 — Deterministic 12/12 / **LLM 9/12 (75%)**. Miss 3건은 전부 **각 Need의 1차 대상이 아닌 인접·보조 항목** (OK-007=Gap의 what_exists_instead가 가리키는 화면 사실, OK-011@GC-23=중도해지 이율 구조 보조, OK-003@GC-25=예상조회 경로 보조). 각 Need의 핵심 항목은 4/4 Case 전부 회수.
- **Over-selection**: Deterministic 5건 → **LLM 0건**. P3-A의 핵심 질문("일반 토큰 부분일치 over-selection을 LLM이 줄이는가")에 대한 답: **전부 제거**.
- **Gap Recall: 4/4** — 4 Case 모두 정확한 KG를 선택 (KG-001·002·004·005; 무관 KG 선택 0).
- Pack 크기: Deterministic 대비 K-item 6→4(GC-24)·6→3(GC-25) 수준 축소 — P3-A의 +22~64% prompt 증가 요인 중 over-selection 분이 제거됨.

## 3. Product Selection 비교

Human = Frozen supply 유효 후보(미끼 제외) / Deterministic = P3-B 재현(12/7/10/0).

| Case | Human | Deterministic | LLM | Miss (유형 기준) | Extra |
|---|---|---|---|---|---|
| GC-18 | TDF·단기채·GIC(3y) = 3 | 12 (TDF 4·채권 3·GIC 5) | **3** (TDF 1·채권형 1·GIC 1) | 0 | 0 (+PRD-020 시도 → gate 차단) |
| GC-20 | TDF·단기채 = 2 | 7 (TDF 4·채권 3) | **2** (TDF 1·채권형 1) | 0 | 0 |
| GC-22 | TDF·단기채·GIC(3y) = 3 | 10 (GIC 5·TDF 4·단기채 1) | **3** (GIC 1·TDF 1·단기채 1) | 0 | 0 (+PRD-020 시도 → gate 차단) |
| GC-25 | 0 (none) | 0 | **0** (LLM 미호출 — needs none) | — | 0 |

- **Recall**: Need 유형 기준 8/8 — 모든 characteristics(TDF/채권형/GIC+3년 maturity)가 후보로 충족. **Pool Size: 7~12 → 2~3** (Human 2~3과 동급) — P3-B 핵심 질문에 대한 답: **필요 소수로 축소됨**.
- **무관 유형 후보: 0.** maturity 판단도 LLM이 정확(GIC 3년제만 선택 — 2·5년제 미선택).
- **개별 상품 대표 선정 차이 4건**: 같은 유형 안에서 Human과 다른 대표를 고름 — TDF: Human 마이다스(PRD-004, 위험중립 4등급 고려) vs LLM KB(PRD-001, 3등급) / 채권형: Human 키움 단기채(PRD-005) vs LLM 크레딧포커스(PRD-006) (GC-22 단기채는 PRD-005 일치 — need가 "채권형(단기채)"로 구체적이었음). **Retrieval Miss가 아니라 유형 내 대표 선정 재량의 차이**로 분류 — 단 C1/C2 관점 함의 있음(§4). GC-20 미끼(주식형 2등급)는 P3-B와 동일하게 need에 없어 미회수(설계 차이, Failure 아님).
- null/status/as_of: Registry verbatim 보존(gate 구조상 LLM이 건드릴 수 없음) — sellable=null 보완 0건.

## 4. Safety Boundary 점검

| 축 | 결과 |
|---|---|
| Authority | 승격 0건 — LLM은 ID만 선택, T1/T2 gate·PROVISIONAL/CONFLICT flag는 코드가 부착 (GC-21 OK-007 미선택으로 해당 flag 케이스는 미발생) |
| Status | SUPERSEDED 후보 없음(현 Registry) — gate 경로는 PRD-020 차단으로 작동 실증 |
| KG | Epistemic Boundary 보존 — consume_text 원문 그대로 K-item 본문, LLM 재작성 없음(구조상 불가) |
| null | sellable/channels/as_of 변형 0 — 카드 조립이 deterministic |
| Hard Constraint | C1/C2/C3·supply validator 무이동. **관찰**: LLM이 GC-18(위험중립 4~6)에 3등급 TDF(PRD-001)를 후보로 선정 — Selector는 성향을 모르므로(§P3-B 원칙: 성향 필터는 Selector 책임 아님) 정상이나, Human은 4등급 마이다스를 골랐었음. 하위 C2 validator가 추천 시 차단하므로 안전하지만, **pool에 유효 등급 대안이 함께 없으면 Agent가 쓸 재료가 없어지는 구조** — Hybrid 설계 시 고려 사항 |
| Role Leakage | **0건** — selection_reason 전수 검사: 전부 "유형/특성 부합"·"Need의 무엇을 다룸" 서술. "좋다/최적/수익률 높음/추천" 0건. 고객 판단 0건 |

## 5. Failure 분석 (지시 §19 분류)

| 분류 | 건수 | 상세 |
|---|---|---|
| Retrieval Miss | **3 (Knowledge)** | OK-007·OK-011@GC-23·OK-003@GC-25 — 전부 보조·인접 항목, 핵심 항목 Miss 0. 공통 패턴: **Need의 1차 대상을 만족시키는 항목을 찾으면 보조 맥락 항목을 "최소 선택" 원칙에 따라 잘라냄** — 원칙 4(최소 항목)의 부작용 |
| Over-selection | **0 (Knowledge) / 2 (Product, gate 차단)** | PRD-020(수협 — index에 '수익률 미확인' 명시)을 2 Case에서 선택 → 카드 완결성 gate가 차단. LLM+deterministic gate 조합의 방어 실증 |
| Gap Miss | 0 (KG 4/4) |
| Role Leakage | 0 |
| Authority Misuse | 0 |
| State Mutation | 0 (구조상 불가) |
| Product Need Inversion | 0 (Need가 Human-defined — 구조상 불가) |
| Consumption Failure | **판정 불가** — Decision Agent RUN은 본 실험 범위 밖(Pack-level 비교까지). 참고 함의: GC-18/22의 Frozen RUN에서 Agent가 선택했던 마이다스 TDF(4등급)가 LLM pool에 없음 → 동일 재현 불가, 대체 TDF(3등급)는 C2에 걸림 — RUN 시 TDF 방향 후보 공백 가능 |

한계(정직 기록): 표본 4+3 Case × 1회 호출 — 반복 안정성(동일 입력 재호출 시 선택 변동) 미측정. Selector도 LLM call이므로 rate limit·비용이 Case당 +1 call.

## 6. 결론 — **Deterministic Retrieval + LLM Selection Hybrid 유력 (결과 B)**

- LLM은 **Precision에서 압도적** (Knowledge over-selection 5→0, Product pool 12/7/10→3/2/3, 무관 후보 0, Role Leakage 0, KG 4/4) — P3-A/B의 핵심 Failure(Selection Precision)를 정확히 해결한다.
- 그러나 **Recall이 완전하지 않다** (Human 필수 OK 9/12) — 보조·인접 항목을 "최소 선택" 원칙 하에 잘라내며, 이는 원칙 강화로 고칠수록 over-selection이 되돌아오는 trade-off 구조다. Recall 보장은 LLM에게 맡길 수 없는 성질(P3-A deterministic은 12/12)이므로 **결과 A(LLM 단독 유력)는 기각**한다.
- Deterministic 유지(결과 C)도 기각하지 않을 이유가 없음 — over-selection 5건·pool 3배는 실측 Failure이고 LLM이 이를 0으로 만들었다.
- 따라서: **Deterministic Retrieval(재현율 보장, 현 selector의 후보 생성) → LLM Selection(후보 집합 내 정밀 선택) + 기존 deterministic Safety Gate** 구조가 두 실측 강점을 결합하는 유력안이다. Miss 위험이 "Registry 전체에서 못 찾음"이 아니라 "deterministic 후보 안에서 잘라냄"으로 한정되고, gate는 이미 작동이 실증됐다.

## 7. 다음 최소 실험 (새 Architecture 설계 아님 — 한 단계만)

**Hybrid Pruning 실험**: 동일 4+3 Case에서, P3-A/B deterministic Selector의 **출력 후보 목록**(over-selection 포함)을 그대로 LLM에게 주고 "이 후보 중 Need에 불필요한 항목만 제거"를 시킨다 — Registry 전체 index 대신 후보 목록이 입력이라는 점만 다르고 나머지(Need·gate·계약) 동일. 확인 질문 하나: **후보 집합이 좁혀진 조건에서 LLM이 over-selection 5건은 제거하면서 Human 필수 9+3건을 보존하는가** (이번 실험의 Miss 3건이 "전체 index에서의 최소 선택" 부작용인지, "보조 항목 경시" 성향인지 분리 판정). 결과가 좋으면 Hybrid를 Human Gate에 정식 상정, 나쁘면 결과 C(deterministic 유지 + 매칭 최소 개선)로 회귀.

---
보고 후 Human Gate 정지. (브랜치 참고: P3-A/B 커밋은 main 미병합 상태였으므로 P3-C도 세션 브랜치 `claude/current-progress-check-fl8osq`에만 push — main 병합은 Human 결정.)
