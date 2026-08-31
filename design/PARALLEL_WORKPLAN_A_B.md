# 병렬 작업 계획 — Session A (P2 Agent Validation) × Session B (Knowledge Build)

- 작성: 2026-08-31. 전제: Phase G 완료(`design/P2_BATCH3_CANDIDATES.md` §4 — GC-18~25 상세 설계, **Gate ② 대기**), Gate ① 반영 완료(HD-PRE-P2-GATE1).
- 이 문서는 두 세션이 공통으로 읽는 **운영 계약**이다. 역할 정의·파일 소유권·인터페이스(K-REQ)·Sync Point를 정의한다.
- 공통 불변 규범 (두 세션 모두): Frozen Artifact(기존 case.md·input_v2·RUN·EVAL·종료된 Revision 기록) 수정 금지 / Human Gate 없이 Semantic 결정 금지 / HD 체계(`golden/HUMAN_DECISIONS.md`)와 HD-3 Authority 순서(공식 기준 > 행내 공식 가이드 > Hot Tip) 준수 / 세제·제도 Rule은 공식 Source 근거만(HD-8; R4 위험자산 한도는 공식 근거 확보 시 별도 HD 후 활성화).

---

## 1. 역할 정의

### Session A — P2 Agent Validation 전담
> 현재 확정된 Input(9-Block Canonical 3-Layer)/Brief(Decision & Action Brief v3)/Reasoning 구조를 기준으로 GC-18~25를 설계·검증한다. **Knowledge 원천의 대규모 정제는 하지 않고, 필요한 Knowledge 항목만 K-REQ로 명시한다.** Frozen Artifact는 수정하지 않는다.

- 산출: P2 Case(canonical.json + knowledge_pack.md), RUN/EVAL, FAILURE_MAP 갱신, Validator/Runtime 보수(HD-5.1 자율 범위 내), K-REQ 목록 관리.
- 하지 않는 것: `sources/` 원천 정제·구조화, `knowledge/` Registry 작성·수정, 신규 Semantic Rule 임의 도입.

### Session B — Knowledge Build 전담
> 퇴직연금 원천자료(`sources/corpus/`, SRC-001~)에서 **Official Knowledge / Product Knowledge / Hot Tip / 상담화법 / Screen·Procedure**를 구조화한다. Agent Judgment나 Golden Expected를 임의로 수정하지 않는다. **P2 Case에서 요청되는 Knowledge(K-REQ)를 우선 구축한다.**

- 산출: `knowledge/` Registry 5종(§3.2), `sources/source_registry.md`의 Status 갱신(REVIEW_REQUIRED 해소), K-REQ 납품.
- 하지 않는 것: `cases/`·`prototype/`·`golden/` 수정, Judgment 유형·Boundary·Expected Output 결정(발견한 판단 이슈는 **제안으로 Human에 보고**만), Hot Tip 내용의 재작성(원문 보존 + Metadata 구조화만).

---

## 2. 파일 소유권 매트릭스 (충돌 방지의 핵심)

| 경로 | 소유 | 상대 세션의 권한 |
|---|---|---|
| `cases/**` (신규 GC-18~25 포함) | **A** | B 읽기만 |
| `prototype/**` | **A** | B 읽기만 |
| `golden/**` (HD 기록 포함) | **A** (Human 결정 기록 대행) | B 읽기만 — B가 받은 Human 결정은 B가 `knowledge/DECISIONS_B.md`에 기록하고, 통합은 Human 지시 시 |
| `design/P2_BATCH3_CANDIDATES.md`, EVAL 관련 design 문서 | **A** | B 읽기만 |
| `design/KNOWLEDGE_REQUESTS.md` (K-REQ 대장) | **A가 항목 추가·상태 갱신(REQUESTED/CLARIFY)** | **B가 상태 갱신(DELIVERED)** — 유일한 공동 편집 파일. 행 단위 append/상태 갱신만, 서로의 행 삭제 금지 |
| `knowledge/**` (신설) | **B** | A 읽기·인용만 |
| `sources/**` (registry Status 갱신 포함) | **B** | A 읽기만 |
| `design/PARALLEL_WORKPLAN_A_B.md` (이 문서) | Human | 두 세션 모두 수정 금지, 변경은 Human 지시로만 |

- **브랜치**: 각 세션은 자기 지정 브랜치에서 작업·푸시. 병합(main 반영)은 Human이 결정. 소유권이 겹치지 않으므로 병합 충돌은 K-REQ 대장 1개 파일로 한정된다.
- 상대 소유 파일의 문제 발견 시: 직접 수정하지 않고 상대 세션 백로그로 전달(Human 경유 또는 K-REQ 대장의 메모 열).

## 3. 인터페이스 계약

### 3.1 K-REQ (A → B 요청)

`design/KNOWLEDGE_REQUESTS.md`에 표로 관리. 형식:

| 필드 | 내용 |
|---|---|
| REQ-ID | `REQ-001`부터 순번 |
| 요청 Case | GC-18 등 (공통이면 `COMMON`) |
| 유형 | official / product / hot_tip / talk / screen |
| 필요 내용 | 무엇이 필요한지 서술 (예: "ISA 만기자금의 연금계좌 전환 — 60일 시한·전환한도·세액공제 추가한도 구조, 공식 Source 근거") |
| 필요 시점 | Freeze 전 필수 / RUN 전 / 참고 |
| 상태 | REQUESTED → (B) DELIVERED(`knowledge/` 항목 ID 병기) / NOT_FOUND(원천에 없음 — 사유) / CLARIFY(질문) |

### 3.2 B 산출물 — `knowledge/` Registry 5종

전 항목 공통: **Stable ID + 원 SRC-ID 인용 + Authority + As-of + Status**. 원천에 없는 내용 생성 금지, Authority 불명 시 추정 금지(HD-3).

| 파일 | ID | 내용 |
|---|---|---|
| `knowledge/OFFICIAL_KNOWLEDGE.md` | `OK-xxx` | 제도·절차·과세·시한 등 공식 지식. Case-agnostic 서술(특정 고객 해석 금지) + Limitation(단정 금지 경계) 필수 |
| `knowledge/PRODUCT_REGISTRY.md` | `PRD-xxx` | 상품 카드 재료 — `design/CANONICAL_CONTRACTS.md` ProductCandidate 필드와 정합(상품명·유형·위험등급·수익률+측정기간+기준일·특징·sellable·채널). 수익률 등 시점 값은 as-of 필수 |
| `knowledge/HOTTIP_REGISTRY.md` | `HT-xxx` | Hot Tip **원문 보존** + Metadata(작성자·작성일·좋아요·출처). 원문 재작성 금지 — 검색을 위한 요약은 별도 열로 |
| `knowledge/TALK_REGISTRY.md` | `TALK-xxx` | 상담화법(연금왕찐천재·이탈대응 스크립트 등) — 원문 발췌 + 상황 태그. 화법의 채택 여부 판단은 A/Human 몫 |
| `knowledge/SCREEN_REGISTRY.md` | `SCR-xxx` | 화면번호·화면명·surface(staff/starbanking)·기능·메뉴 경로. **G3(화면 Reference S5 단일 위치·validate_screen_refs)의 원천 Master** — 화면번호 정확성이 deterministic FAIL과 직결 |

### 3.3 A의 인용 방식

- Case `knowledge_pack.md`의 K-item은 기존 5필드 형식 유지, Source 필드에 `knowledge/` ID + SRC-ID 병기 (예: `OK-003 (SRC-046/049)`).
- Case Relevance·Limitation의 **Case 맞춤 서술은 A가 작성** (B 항목은 Case-agnostic이므로).
- canonical.json의 supply(product_candidates/hot_tips/screens)는 B Registry 항목에서 구성 — 수치·원문·화면번호를 A가 임의 변형하지 않는다.

## 4. Session A 작업 계획

| 단계 | 내용 | Gate |
|---|---|---|
| A-0 | **K-REQ 초기 목록 작성**(§6을 `design/KNOWLEDGE_REQUESTS.md`로 옮겨 등록) — B가 즉시 착수할 수 있게 최우선 | — |
| A-1 | Gate ② 대기: §4 상세 설계에 대한 Human 승인. 대기 중 EVAL 템플릿 정비(SG-1~3 Semantic Gate + Answer Quality 8축 Observation 절 — HD-8·HD-PRE-P2-GATE1 기준) | **Gate ② (Human)** |
| A-2 | 승인 후 Case 작성: canonical.json + knowledge_pack.md (B 납품분 인용; §5 B-2 완료가 Freeze 전제) → dry-run(렌더·derived·validator) → **Freeze** | Freeze 전 K-REQ '필수' 항목 DELIVERED 확인 |
| A-3 | RUN_001 실호출 8건 → RUN 렌더 | — |
| A-4 | EVAL 8건(Boundary + SG-1~3 + AQ Observation) → FAILURE_MAP cross-case 갱신 | — |
| A-5 | P2 Batch 결과 보고(성공 기준·Gap·신규 Failure 후보·Revision 필요 여부) | **Human 보고 후 정지** |

- B 납품 지연 시: 해당 Case만 보류하고 나머지 진행(Case 간 독립). 임시로 A가 원천을 직접 정제하지 않는다 — 병목이면 Human에 보고.

## 5. Session B 작업 계획

| 단계 | 내용 | Gate |
|---|---|---|
| B-0 | 착수 준비: 이 문서 + `design/CANONICAL_CONTRACTS.md`(supply 필드) + `golden/HUMAN_DECISIONS.md`(HD-1·2·3·7·8) + `design/KNOWLEDGE_REQUESTS.md` 숙지. `knowledge/` 골격과 Registry 스키마 초안 작성 | **스키마 1회 Human 확인** (필드·ID 체계 — 이후 항목 추가는 자율) |
| B-1 | **P2 우선 구축**: K-REQ 순서대로 원천 확인 → Registry 항목화 → K-REQ 상태 DELIVERED 갱신. '필수' 항목 우선 | — |
| B-2 | K-REQ 전량 처리 보고 (DELIVERED/NOT_FOUND/CLARIFY 집계) → A의 Freeze 전제 해소 | Human/A에 통지 |
| B-3 | 확장 구축: K-REQ 밖 영역의 체계적 정제 — 우선순위: ① Screen Master 전수(G3 원천) ② 공식 제도·과세(01/04/06 폴더) ③ Hot Tip 전수(03) ④ 화법(연금왕찐천재·이탈대응) ⑤ 상품. `sources/source_registry.md` Status 갱신 병행 | — |
| B-4 | 품질 규칙 상시: Authority 충돌 발견 시 `Source Conflict`로 기록(임의 통합 금지) / 판단·Boundary에 영향 주는 발견(예: R4 위험자산 한도 공식 근거)은 **Human 보고 — Registry에 먼저 넣지 않는다** | 발견 시 Human |

## 6. K-REQ 초기 백로그 (A가 A-0에서 대장에 정식 등록)

§4 상세 설계에서 도출된 P2 필요 Knowledge. 유형·필요 시점 포함:

| Case | 필요 Knowledge | 유형 | 시점 |
|---|---|---|---|
| GC-18 | ISA 만기자금 → 연금계좌 전환: 60일 시한·전환한도·세액공제 추가한도 구조 (공식 근거) | official | Freeze 전 필수 |
| GC-18 | "전체 자산 흐름 먼저 묻기" 류 field tip 원문 | hot_tip | RUN 전 |
| GC-19 | 계약이전 처리 원칙(고객 결정 존중·절차 지연 금지) 공식 원문 (SRC-003 §03 확인) | official | Freeze 전 필수 |
| GC-19 | 이전 신호 고객 접점 화법(고객 관점 톤) | talk/hot_tip | RUN 전 |
| GC-20 | 투자성향 변경(상향) 고객 안내 원칙 — "상한 확대 ≠ 운용 요구" 공식 근거 | official | Freeze 전 필수 |
| GC-20 | 과거 '권유 사절' 고객 재접근 화법 | talk/hot_tip | RUN 전 |
| GC-21 | 고객보유수익률 vs 상품수익률 표시 기준·차이 설명 자료 | official | Freeze 전 필수 |
| GC-21 | 손실 구간 고객 상담 화법 | talk/hot_tip | RUN 전 |
| GC-22 | 정기예금 만기 처리·예약변경(만기 1개월 전~)·DO 미등록 시 만기 후 처리 경로 (SRC-001/002 확인) | official | Freeze 전 필수 |
| GC-22 | 퇴직급여 입금 직후 상담 순서 tip | hot_tip | RUN 전 |
| GC-23 | **부분 이전(일부 상품만 이전) 절차·현금이전 시 중도해지이율 구조** — F-010 재검증의 핵심 동봉물 | official | Freeze 전 필수 |
| GC-24 | 세액공제 구조: 총급여 구간별 공제율(16.5%/13.2%)·**결정세액 조건**·확인 경로(원천징수영수증/[06-12-151]) | official | Freeze 전 필수 |
| GC-25 | 중도해지 과세: 기타소득세 16.5%·미공제분 과세 제외·미신청분 등록([06-12-622])·증빙(연금납입확인서) 발급 개시 7/1 | official | Freeze 전 필수 |
| COMMON | Screen Master: §4 설계 등장 화면 전수 — [04-12-642]·[04-12-640]·[06-AD-080]·[04-12-17A]·[06-12-151]·[06-12-622]·[02-12-221]·[04-12-644] + StarBanking 경로(운용상품 변경·상품찾기·연금수령 정보) 실존·기능 확인 | screen | Freeze 전 필수 |
| COMMON | Product 카드 재료: TDF(빈티지별)·채권형(국공채/단기채)·인컴형·저축은행 특별제공 정기예금·GIC + 미끼용 2~3등급 상품 — 등급·수익률(as-of)·sellable·채널 | product | Freeze 전 필수 |
| COMMON | Hot Tip Metadata 원천(작성자·작성일·좋아요) 실존 확인 — HD-PRE-P2-BRIEF §4.6 확인사항의 실납품 | hot_tip | Freeze 전 필수 |

## 7. Sync Point & Human 개입 지점 요약

1. **Gate ②** (A-1): §4 상세 설계 승인 → A의 Case 작성 개시.
2. **B 스키마 확인** (B-0): Registry 필드·ID 체계 1회 승인 → 이후 B 자율.
3. **K-REQ 납품 완료** (B-2 → A-2): '필수' 항목 DELIVERED가 각 Case Freeze의 전제.
4. **병합**: 각 세션 브랜치 → main 반영은 Human 지시로만.
5. **수시**: Source Conflict / 판단 영향 발견(B-4) / 병목·CLARIFY 적체 시 Human 에스컬레이션.
6. **최종**: A-5 P2 Batch 보고 + B-3 확장 구축 현황 보고.
