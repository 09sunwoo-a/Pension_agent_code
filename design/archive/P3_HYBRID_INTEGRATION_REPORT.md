# P3 Integration — Hybrid Selection + F-013(FC-1) Minimal Revision + Mock v0 (2026-08-31)

- 구조: **deterministic Recall → LLM Pruning → deterministic Safety Gate** (검색기술 Hybrid Search 아님). LLM은 Registry 검색·Trust 결정·내용 생성·최종 추천을 하지 않는다.
- 전제 기록: 지시문이 참조한 P3-C 산출물(`design/P3C_LLM_SELECTION_REPORT.md`, `prototype/llm_selector.py`)은 **이 저장소 어디에도 존재하지 않았다** (본 브랜치·main·전체 히스토리 확인). P3-C 수치(over-selection 5→0 / Recall 9/12 / miss OK-007·OK-011·OK-003, LLM 단독 Product의 C2 공백 위험)는 Human 지시문 기재값을 Evidence로 사용했고, LLM-only 경로 재현은 저장소 내 코드 부재로 불가함을 명시한다. 본 작업의 `llm_selector.py`는 Hybrid의 Pruner로 신규 작성한 것이다.
- P3-A precision rule(짧은 토큰 차단 등)·Product 유형당 상한·수익률 ranking: **추가하지 않음** (지시 §3·§4 준수). Frozen 무수정, 기존 Human/P3-A/P3-B 경로 전부 보존(dry-run 확인).

## 1. 구현 내용

| 파일 | 내용 |
|---|---|
| `prototype/llm_selector.py` (신규) | Knowledge/Product Pruning 프롬프트("명백히 불필요한 것만 제거·애매하면 KEEP·후보 밖 ID 금지") + keep/remove 해석. 언급되지 않은 후보 = KEEP. reason은 로그 전용(Decision Agent에 비전달) |
| `prototype/hybrid_selector.py` (신규, 얇은 orchestration) | `select_knowledge_hybrid` = selector.py 후보 → prune → selector.py 재조립(gate/flag 동일 적용) / `build_pool_hybrid` = product_selector.py pool → **기존 C2 매핑(runtime.PROFILE_MIN_FUND_GRADE) 재사용한 eligibility 표시**(판정 책임 이동 없음·복제 없음) → prune → pool. 로그 `prototype/out/hybrid_*.json` |
| `prototype/selector.py` (최소 수정) | needs 프로그램 주입 + `keep_registry_ids` 필터(프루닝 결과 반영 지점 — gate·조립은 기존 그대로). need의 후보가 전부 프루닝되면 합성 Gap 정상 생성 |
| `prototype/product_selector.py` (최소 수정) | needs 프로그램 주입 허용 |
| `prototype/runtime.py` | 옵트인 2곳: `P3_HYBRID_KNOWLEDGE_SELECTION=1` / `P3_HYBRID_PRODUCT_SELECTION=1` (기본 경로·기존 flag 불변) + 원칙 19 (d)(e) 보강 + OUTPUT_INSTRUCTION s5 tip_id 계약 문구 |
| `cases/FAILURE_MAP.md` | **F-013 정식 부여** (S4 Epistemic / Conditionality Inflation — 구 FC-1) + F-011 tip_id 변형 관찰 기록 |

**Fallback(§12)**: LLM timeout/HTTP/parse/후보 밖 ID/비정상 빈 keep → deterministic 후보 전체 사용 + 로그 기록. **실전 발동 1회 확인**: GC-18 hybrid RUN 1차에서 프루닝 호출이 RemoteDisconnected → 12개 deterministic pool로 자동 진행, RUN은 SUCCESS(Agent가 2개만 선별·C2 PASS) — LLM 실패 ≠ Retrieval 실패 실증.

## 2. Knowledge Hybrid 결과 (pack-level)

| Case | Deterministic Candidates | Hybrid Keep | Human Required | Miss | Extra |
|---|---|---|---|---|---|
| GC-21 | OK-007·KG-001·OK-006 (3) | 3 (제거 0) | OK-007·OK-006 | 0 | 0 |
| GC-23 | OK-002·OK-003·OK-009·OK-011·KG-002 (5) | 4 (OK-009 제거 ✓) | OK-002·OK-003·OK-011 | 0 | 0 |
| GC-24 | OK-008·KG-005·OK-009·OK-015·OK-011·OK-006 (6) | 5 (OK-011 제거 ✓) | OK-008·OK-009·OK-006 | 0 | OK-015 (KEEP-우선 허용) |
| GC-25 | OK-009·OK-008·OK-015·KG-004·OK-011·OK-003 (6) | 4 (OK-015·**OK-003** 제거) | OK-009·OK-011·OK-003 | **OK-003 1건** | OK-008 |

- **필수 Recall 11/12** (deterministic 12/12 대비 −1) / **KG 4/4 유지** / Authority·Status·flag 보존(gate가 프루닝 후 재적용).
- P3-C가 Miss했던 3건 중 **OK-007·OK-011 보존 ✓**, **GC-25 OK-003은 Hybrid도 Miss** — 항목 제목·topics가 계약이전 중심이라 프루너 요약 입력에서 해지 Case 관련성(중도해지 예상조회 경로)이 안 보임 → **Pruning Failure 1건 (경미 — 보조 경로 지식, OK-011이 이율 구조는 커버)**. 원인은 P-2(항목 내 혼합 claim)의 프루닝 버전.
- Over-selection: P3-A 5건 → **2건** (3건 제거·2건은 KEEP-우선 원칙상 잔존 허용).

## 3. Product Hybrid 결과 (pool-level)

| Case | Deterministic Pool | Hybrid Pool | Need Coverage | Constraint | 결과 |
|---|---|---|---|---|---|
| GC-18 (위험중립형) | 12 | **6** (TDF 4→2·GIC 5→1·채권형 3 유지) | 3 need 전부 | C2-유효 TDF(마이다스 4등급) 보존 — **공백 없음** | ✓ |
| GC-20 (적극투자형) | 7 | **5** (TDF 4→2·채권형 3 유지) | 2 need + **저위험/유지 분기 후보 보존** | 유지 | ✓ (나열 원인 축소) |
| GC-22 (위험중립형) | 10 | **4** (GIC 5→1·TDF 2·단기채 1) | 3 need 전부 | C2-유효 TDF 보존 | ✓ |
| GC-25 | 0 | 0 | 빈 Pool 정상 | — | ✓ |

유형 Recall 8/8 유지(Human 유효 후보 개별 항목 기준도 8/8). 수익률 정렬·유형 상한 없이 LLM 중복 제거만으로 감소.

## 4. 실 RUN 결과 (Hybrid 중심 5 RUN + GC-18 재시도)

| RUN | status | Judgment | 관찰 |
|---|---|---|---|
| GC-21 hybrid-K | SUCCESS (전 validator PASS) | 추가 확인 우선/정보 안내 중심 (불변) | S4: 두 수익률 제시 + 열린 질문 — **원인 설명 미생성** |
| GC-25 hybrid-K | SUCCESS | 고객 결정 지원/추가 확인 우선 (동등) | tip_id FAIL 소멸. S4: "추징될 가능성"·"유리하실 수 있습니다"+확인 연결 |
| GC-23 hybrid-K (Control) | SUCCESS | 개입 필요/고객 결정 지원 (직전 selector RUN과 동일) | S4 위축 없음 — 손익 고지·GIC 대안·전출 존중 분기 유지. tip_id FAIL 소멸 |
| GC-20 hybrid-P | SUCCESS | 동일 유형 | **TDF 2종+단기채 선택 — 4종 나열 해소 + 저위험 분기 후보 사용 복원** |
| GC-18 hybrid-P ①(fallback) | SUCCESS | 개입 필요/정보 안내 중심 | 12-pool에서도 2개 선별·C2 PASS |
| GC-18 hybrid-P ②(prune 성공) | VALIDATION_ERROR | 동일 | 6-pool에서 GIC+단기채+**4등급 TDF** 선택(C2 공백 없음·3등급 미선택). FAIL 원인은 reasoning의 "방치" — **F-001/FC-2 계열 baseline 재발**(Selection 무관, validator 차단 정상) |

## 5. F-013(FC-1) Regression

| Case | 직전 RUN (보강 전) | 이번 RUN (원칙 19 d·e 적용) | 판정 |
|---|---|---|---|
| GC-21 | selector RUN에서 "매수 시점이나 평가 기준에 따라 차이가 발생할 수 있는데" 원인 생성 | 두 수치 제시 + "궁금하시거나 느껴지는 점이 있으신지 먼저 여쭤보고" — 원인 미생성, 확인 선행 | **해소** |
| GC-25 | "7월 1일부터 발급 가능합니다 … 세금을 최대한 줄이는 방법입니다" (확정+최적) | "추징될 **가능성**이 있어 … 더 유리하실 **수 있습니다**. 이 부분 함께 확인해 드릴까요?" — 방향 확정 해소. 단 "7월 1일부터 발급 가능합니다" 시점 사실 단정은 **잔존** | **부분 해소** (방향 승격 해소 / T3 시점 사실 단정 1건 잔존) |
| GC-23 (Control) | — | 조건 분기·손익 고지·존중 화법 전부 유지, 화법 위축 없음 | **위축 없음** |

deterministic keyword blacklist는 추가하지 않음(지시 §15) — 잔존분은 Evaluator semantic gate 관찰 대상.

## 6. Failure Attribution

| 관찰 | 분류 |
|---|---|
| GC-25 OK-003 프루닝 손실 | **Pruning Failure (경미)** — 요약 기반 프루닝이 혼합 claim 항목의 부차 관련성을 못 봄 |
| GC-25 "7/1 발급" 시점 단정 잔존 | **S4 Semantic (F-013 부분 잔존)** — Pack 정확, 원칙 19(e) 부분 효과 |
| GC-18 ② "방치" reasoning | **Consumption (F-001/FC-2 계열 baseline)** — Selection 무관, hard-fail 차단 |
| GC-18 ① 프루닝 HTTP 실패 | **LLM 장애 → Fallback 정상 작동** (Failure 아님 — 설계 검증) |
| Retrieval / Gate(Authority·null·Constraint) Failure | **0건** |
| tip_id 슬롯 혼동 | 이번 5 RUN + Mock에서 **재발 0** (OUTPUT s5 문구 효과 — 표본 작음, 관찰 지속) |

## 7. Mock v0 (Minimal End-to-End) — 요약

`prototype/mock_pipeline.py` + `prototype/mock/MOCK_001_raw.json` → **status SUCCESS, 전 validator PASS, 전 단계 추적 가능** (`prototype/mock/MOCK_001_RUN.md`/`.json`).

- Flow: Raw JSON → adapter(build_canonical — 의미 라벨 금지) → **기존 canonical.py 검증·derive(D 6건: 경과일 20일·30d 증감·산술 대조 일치·만기 D-225·개시요건 미충족 R)** → C1/C2/C3 → **CALL1** Knowledge Need 생성(Human-defined Need 최초 제거 — 2 need 생성) → Hybrid Knowledge(OK-003/004/005·KG-002·OK-012 keep, OK-002 프루닝 제거 — 전출 절차로 정확 판별) → **CALL2** Judgment(개입 필요/정보 안내 중심)·조건 2분기 Direction·product_need 구조화 → Hybrid Product(TDF4+GIC7 → 5개: 4등급 TDF 포함·만기 차별화 GIC 3종) → **CALL3** 기존 SYSTEM_ROLE_V3/OUTPUT_INSTRUCTION_V3로 S1~S5 Brief + Fit reason → 기존 validator 전체.
- LLM Call: decision-level 3 + selection prune 2 = **총 5** (전부 run record 기재).
- 품질 관찰: S1 관찰 서술("운용지시 없이 현금성자산으로 보유 중" — 방치 류 없음), S4 의향 확인 선행, C3 정합(위험중립형에 지켜드림/알파드림/뿔려드림만 안내 — 모두드림 미등장), 미끼성 3등급 TDF는 pool에 있었으나 미선택.
- Mock에서 발견된 Failure: ① CALL2 생성 characteristic "채권형 펀드"가 registry type 토큰("채권형(단기채)")과 미매칭 → 채권형 후보 미회수 (**Retrieval 어휘 정렬 문제, 경미** — LLM 생성 need의 어휘가 registry 토큰과 다를 수 있음) ② DO 포트폴리오 characteristic은 PRD 검색 대상 밖(설계상 제외)이라 무回수 — direction의 DO 분기는 Knowledge(OK-005)로 커버됨.
- 판정: **최소 End-to-End Mock 성립** — Raw 하나로 Brief까지 연결, 이상 동작은 위 2건으로 분리 기록.

## 8. Knowledge Architecture v1 Freeze 판단

**Freeze 상정 가능 (권고)** — 보류 사유였던 실 RUN 검증이 Hybrid까지 완료되었고, Hybrid가 P3-A Recall(11/12)과 P3-C Precision(over-selection 5→2, pool 12→4~6)을 동시에 확보하며 Gate·Constraint·null 보존이 전 실험에서 유지됨. Freeze 문서에 명시할 것: ① 기본 경로는 여전히 Human pack(Hybrid는 옵트인) ② 수동 유지 영역(HT/TALK/SCR·운영형 Knowledge Need — Mock의 LLM Need 생성은 v0 실험) ③ 미해결 관찰(GC-25 OK-003 프루닝 손실, F-013 부분 잔존, LLM-need 어휘 정렬).

## 9. 다음 단계 (한 단계만)

**Hybrid 경로의 8 Case 전수 회귀 1회전** (P3-A 4 + P3-B 4 Case를 Hybrid 모드로 RUN + EVAL — 표본 1~2회의 위 관찰(F-013 잔존·프루닝 손실·tip_id 재발 0)이 안정적인지 확정한 뒤 v1 Freeze 문서를 작성·상정).
