# P3-B Minimal Product Candidate Retrieval — 구현·비교 결과 (2026-08-31)

- 범위: Human이 Case별로 구성하던 `supply.product_candidates`를, Human-defined Management Direction/Solution Type(`design/P3B_PRODUCT_NEEDS.md` — P2 Case 설계 §4에서 전사) 기준으로 PRD Registry에서 최소 자동 구성. **변화 변수는 Product Candidate Retrieval 하나** — P3-A(OK/KG)·HT/TALK/SCR·Judgment·Hard Constraint·Fit reason 생성 전부 무변경.
- 구현물: `prototype/product_selector.py` + `design/P3B_PRODUCT_NEEDS.md` + `prototype/runtime.py` run_case_v3의 옵트인 seam 1곳(`P3B_PRODUCT_SELECTION=1`일 때만 pool 교체·기본 경로 무변경).
- Frozen 불변: canonical.json·RUN·EVAL 무수정. Selection log: `prototype/out/p3b_pool_<CASE>.json`.

## 1. 구현 내용

```
(Human-defined) product_need: solution_type + intrinsic characteristics (+maturity)
  → PRD Registry 검색 — product_type 정규화 부분일치 (Customer Situation 태그 없음)
  → status gate (SUPERSEDED 제외 / PROVISIONAL flag)
  → 카드 완결성 gate — S3 카드 최소 필드(실명·등급(원리금보장형 면제)·수익률+기준일) 미달 시
    제외+사유 로그 (PRD-008/009 등급 미확인, PRD-019 유형만, PRD-020 수익률 미확보)
  → Candidate Pool (registry 값 verbatim — sellable/channels null 유지, product_id만 부여)
  → 기존 Runtime (render_supply · C2/sellable supply validator · Agent Fit reasoning 무변경)
```

- 순서 보존: Direction→Retrieval. needs는 Human Expected에서 전사되므로 **Product가 Management Need를 생성하는 역전은 구조적으로 불가능**. `### none` Case(GC-25)는 빈 Pool = 정상 결과.
- Ranking 없음(수익률 정렬 없음), Embedding/Vector/Reranker 없음. PRD-021(DO 포트폴리오)·PRD-022(판매중단 목록)는 카드 재료가 아니므로 검색 대상 제외.

## 2. 기존 구조에서 유지한 부분

Management Judgment(Agent) · C1/C2/C3 + supply validator(sellable=false·성향 밖 등급 FAIL — runtime 그대로) · 최종 후보 선택(Agent) · Customer–Product Fit reason(Agent 생성, Registry 무저장) · P3-A Selector·SYSTEM_ROLE_V3·FC-1 대응 프롬프트 · tips/screens supply. 4 Case dry-run에서 knowledge_context의 Candidate Pool 절 외 프롬프트 전 섹션 동일 확인.

## 3. Case별 결과 (A=Human pool / B=Selector pool)

| Case | Human Direction (Expected) | A | B | 누락 | 과다 |
|---|---|---|---|---|---|
| GC-18 신규 입금(ISA 전환 조건부) | 추가 확인 우선 — 확인 후 조건부 운용 | TDF④·TDF③(미끼)·단기채⑥·GIC3y | 12개: TDF 4종·채권형 3종·GIC(3y) 5종 | 0 | +8 (동일 유형 내) |
| GC-20 재분석·조건부 운용 | 추가 확인 우선 — 의향 확인 후에만 후보 | TDF③·단기채⑥·주식형②(미끼) | 7개: TDF 4종·채권형 3종 | 미끼만 (설계 장치) | +5 |
| GC-22 만기 재운용+퇴직급여 | 개입 필요 — D-10 만기 우선, 퇴직급여 조건부 | TDF④·단기채⑥·GIC3y·TDF③(미끼) | 10개: GIC(3y) 5종·TDF 4종·단기채 1종 | 0 | +6 |
| GC-25 해지 문의 (Product 불필요) | 정보 안내/고객 결정 지원 | (없음) | **빈 Pool (정상)** — 억지 생성 없음, 프롬프트 무변화 | — | 0 |

**최종 Agent 선택**(Frozen RUN_002 기준): GC-18 마이다스TDF+GIC+단기채 / GC-20 KB TDF / GC-22 마이다스TDF+단기채+GIC — **전부 B pool에 존재** → 동일 선택이 가능한 재료 공급. 실제 B pool로의 Agent 선택(Consumption)은 RUN 미실행(§6).

## 4. Recall / Precision

- **유효 후보 Recall 8/8 (100%)** — 미끼 제외한 Human pool 상품 전부 회수.
- **무관 유형 회수 0** — 과다분은 전부 요청 유형 내(TDF 시리즈 4종 전부·GIC 3년제 라인업 5종 전부·채권형 3종). Precision(유효 Human 후보 기준) 8/29 — pool 크기 A 3~4 → B 7~12, 프롬프트 +649~2,088 chars.
- maturity 필터 작동(GIC 2·5년제 제외). 카드 미달 4항목 제외 정상(로그 기록) — PRD-020 수협(bank_objective 성격 서술 포함 항목)도 카드 미달로 자연 제외.
- **상태 보존**: sellable=null → "판매 가능 여부 미확인 (상담 전 확인 필요)" 렌더, channels=[] → "채널 미확인", 위험등급·as_of verbatim — 임의 보완 0건.
- **미끼**: TDF 3등급 미끼(GC-18·22)는 유형 매칭으로 자연 회수되어 C2 회피 검증 축 유지. GC-20 주식형 2등급 미끼는 product_need에 없어 미회수 — Human 설계 장치의 부재이며 Retrieval Failure 아님(보고서 기록).

## 5. Product가 Management Need를 역전시킨 사례

**구조적으로 발생 불가** — Retrieval 입력이 Human 확정 Direction/Solution Type이고 GC-25에서 빈 Pool을 정상 반환(억지 후보 생성 없음). 단 "매력적 Pool이 Agent 판단을 흔드는가"(Study P3-1 축)는 RUN-level 검증 항목으로 잔여.

## 6. Failure 분류

| 관찰 | 분류 |
|---|---|
| 동일 유형 내 후보 확대 (TDF 전 브랜드·GIC 전 3년제 라인업) — pool 2~3배 | **Over-selection (경미~중간)** — 무관 상품은 아니며 "Candidate A/B/C 검토 재료" 역할은 유지되나, pool 희석·프롬프트 증가. F-006/F-002 재발 조건은 RUN으로 확인 필요 |
| Retrieval / Product Need / State Preservation / Constraint Failure | **미발생** (Recall 100%, GC-25 빈 Pool 정상, null 보존, Hard Constraint 무이동) |
| Consumption / Recommendation Reason Failure | **판정 불가** — GEMINI_API_KEY 부재로 실 RUN 불가. dry-run으로 프롬프트 조립·validator 배선까지 확인 |

## 7. 필요한 최소 Revision

1. **Pool 폭 규칙** (over-selection 대응): 유형당 후보 수 상한 또는 GIC 라인업 대표 선정 규칙 — 어떤 기준으로 줄일지(수익률 정렬 금지 원칙 하에서)는 **Human 결정 필요**. 증거(RUN에서 실제 F-006/희석 발생) 전에는 Metadata 추가 없이 보류 가능.
2. **RUN 비교**: API 키 확보 후 4 Case × (A/B) RUN + EVAL — Consumption·Fit reason·수익률 단독 추천·미끼 회피 확인.
3. 미끼 미회수(GC-20 유형): Selector pool로 RUN하는 경우 bait 검증 축이 약해짐 — 검증 목적 Case에서는 Human이 needs에 bait 유형을 명시적으로 추가하는 관행으로 해결 가능(코드 변경 불요).

## 8. P3-B 종료 판정 (제안)

**조건부 종료 가능** — 성공 정의(§16) 중 pack-level 3축(유사 검토 재료 공급 / Need 역생성 없음 / Hard Constraint·Fit 구조 유지)은 충족. RUN-level(Consumption·Fit reason) 검증과 pool 폭 규칙 Human 결정이 잔여. Selector는 옵트인 유지.

## 9. Knowledge Architecture v1 Freeze 판단

**Pack-level 구조는 Freeze 후보로 상정 가능, 전체 Freeze는 보류 권고.** 근거: (찬성) OK/KG(P3-A)·PRD(P3-B) 모두 기존 인터페이스(K-item·supply 계약) 무변경으로 자동화가 성립했고, Gap 1급 전달·Authority gate·Direction→Retrieval 순서·null 보존 등 경계 원칙이 두 실험에서 일관되게 유지됨. (보류 사유) ① 두 Selector 모두 실 RUN 미검증(공통 blocker: API 키) ② P3-A 매칭 정밀도·P3-B pool 폭의 최소 revision이 Human 미승인 ③ HT/TALK/SCR·Knowledge Need 생성은 여전히 수동 — v1 Freeze 범위 정의에 "수동 유지 영역"의 명시 필요. → RUN 검증 1회전 후 Freeze 상정이 안전한 경로.
