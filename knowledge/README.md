# knowledge/ — Knowledge Registry (Session B 소유)

- Status: **B-0 스키마 초안 (2026-08-31) — Human 승인 대기.** 승인 전 대량 항목 작성 금지.
- 소유권: `design/PARALLEL_WORKPLAN_A_B.md` §2 — `knowledge/**`는 Session B 소유, Session A는 읽기·인용만.
- 근거 계약: PARALLEL_WORKPLAN_A_B.md §3.2 (Registry 5종·공통 필드) / `design/CANONICAL_CONTRACTS.md` §2 (supply 계약) / `golden/HUMAN_DECISIONS.md` HD-1·2·3·7·8.

## 1. 파일 구성

| 파일 | ID Prefix | 내용 |
|---|---|---|
| `OFFICIAL_KNOWLEDGE.md` | `OK-xxx` | 제도·절차·과세·시한 등 공식 지식 (Case-agnostic + Limitation 필수) |
| `PRODUCT_REGISTRY.md` | `PRD-xxx` | 상품 카드 재료 (CANONICAL_CONTRACTS ProductCandidate 정합) |
| `HOTTIP_REGISTRY.md` | `HT-xxx` | Hot Tip 원문 보존 + Metadata 구조화 |
| `TALK_REGISTRY.md` | `TALK-xxx` | 상담화법 원문 발췌 + 상황 태그 |
| `SCREEN_REGISTRY.md` | `SCR-xxx` | 화면번호·화면명·surface·기능·메뉴 경로 (G3 원천 Master) |
| `SOURCE_CONFLICTS.md` | `SC-xxx` | Source 충돌 기록 (임의 통합 금지 — HD-3) |
| `DECISIONS_B.md` | `DB-xxx` | B가 받은 Human 결정 기록 (golden/ 통합은 Human 지시 시) |

## 2. ID 체계

- 형식: `<PREFIX>-` + 3자리 순번 (`OK-001`, `PRD-001`, `HT-001`, `TALK-001`, `SCR-001`, `SC-001`).
- **Append-only**: 번호는 등록 순서대로 부여하며 재사용·재부여·재정렬하지 않는다. 렌더·파일 내 위치와 무관하게 불변(Stable ID).
- 항목 폐기 시 삭제하지 않고 `Status: SUPERSEDED`(+대체 ID 병기)로 남긴다 — A가 이미 인용한 ID가 깨지지 않게 한다.
- 한 원천 문서(SRC)에서 여러 항목이 나올 수 있고, 한 항목이 여러 SRC를 인용할 수 있다 (N:M).

## 3. 공통 필드 (전 Registry 필수)

| 필드 | 정의 |
|---|---|
| `id` | Stable ID (§2) |
| `title` | 항목 한 줄 제목 |
| `source` | 원 SRC-ID(+복수 가능) 및 **문서 내 위치**(섹션·페이지·표 등) — 원문 Trace 가능해야 함 |
| `authority` | HD-3 Authority 표기 (§4) |
| `as_of` | 내용의 기준 시점 — 원천에 명시된 값만. 불명이면 `Unknown` (추정 금지) |
| `status` | 항목 상태 (§5) |
| `delivered_for` | 납품 대상 K-REQ ID (해당 시. 예: `REQ-001`) — B-3 확장 구축분은 생략 |
| `registered` | Registry 등록일 |

## 4. Authority 기재 규칙 (HD-3)

Authority 순서: `공식 법·제도·내규·시스템 기준 > 행내 공식 업무가이드/매뉴얼 > 영업점 Hot Tip / Field Know-how`.

| 표기 | 의미 | 해당 원천 예 |
|---|---|---|
| `T1-Official` | 공식 법·제도·내규·시스템 기준 | 법령·내규 원문, Human-confirmed 공식 기준(SRC-096류 — 확인 기록 병기) |
| `T2-InternalGuide` | 행내 공식 업무가이드·매뉴얼·부서 공문·공식 참조자료 | SRC-001~007, SRC-025~027 등 |
| `T3-FieldTip` | 영업점 Hot Tip / Field Know-how / 경험 공유 | SRC-037~086 (03 폴더) |
| `Public` | 공개 콘텐츠 (KB Think·웨비나 등) — HD-3 3단계 밖, 참고용 | SRC-028~036, SRC-087~091 |
| `UNCLEAR` | 매핑 불명 — **추정하지 않고 그대로 기록**, source_registry의 Authority 값 병기 | |

- 세제·제도 Rule은 T1/T2 근거 없이는 확정 기술하지 않는다(HD-8). T3/Public에만 있는 제도 서술은 Limitation에 "공식 근거 미확보"를 명기한다.
- Hot Tip에만 있는 실행 제약은 `Operational Check Needed`로 기재한다 — Hard Constraint로 승격하지 않는다(HD-3).

## 5. Status 어휘

| 값 | 의미 |
|---|---|
| `ACTIVE` | 원문 확인 완료, 인용 가능 |
| `PROVISIONAL` | 기록은 했으나 확인 미완(Authority 불명·원문 일부 미확인 등 — 사유 병기) |
| `CONFLICT` | Source 충돌 — `SOURCE_CONFLICTS.md`의 SC-ID 병기, 임의 통합 금지 |
| `SUPERSEDED` | 대체됨 — 대체 항목 ID 병기, 행 삭제 금지 |

## 6. 기재 규칙 (전 Registry 공통 불변)

1. **원천에 없는 내용을 생성하지 않는다.** 원천에 없는 필드는 비우거나 생략한다(빈 값을 임의로 채우지 않는다).
2. **원문 보존**: HT/TALK의 원문은 재작성 금지, 발췌 시 발췌 범위를 명시한다. 검색용 요약은 별도 필드에만 두고 원문과 구분한다.
3. **Case-agnostic**: 특정 고객 해석·판단 서술 금지. Case 맞춤 Relevance/Limitation은 A가 작성한다(§3.3).
4. **시점 값**: 수익률·금리·한도 등 시점 의존 값은 as-of 필수. as-of 불명 값은 PROVISIONAL.
5. **Source 충돌**: 발견 즉시 `SOURCE_CONFLICTS.md`에 SC-xxx로 기록하고 관련 항목 status=CONFLICT. 공식성·최신성·적용범위 판단이 필요한 통합은 Human 몫.
6. **판단 영향 발견**(예: R4 위험자산 한도의 공식 근거, Judgment/Boundary에 영향 주는 사실): **Registry에 넣지 않고 Human에 먼저 보고**한다(B-4). 보고 후 Human 결정은 `DECISIONS_B.md`에 기록.
7. K-REQ 납품 시 `design/KNOWLEDGE_REQUESTS.md`에서 **상태·납품 ID·메모 열만** 갱신한다. A가 쓴 행의 다른 내용은 수정하지 않는다.
8. `cases/`·`prototype/`·`golden/`·Frozen Artifact는 읽기 전용.

## 7. A의 인용 방식 (참고 — PARALLEL_WORKPLAN §3.3)

- knowledge_pack.md K-item Source 필드: `OK-003 (SRC-046/049)` 형식.
- canonical.json supply(product_candidates/hot_tips/screens)는 PRD/HT/SCR 항목에서 구성 — 수치·원문·화면번호를 A가 변형하지 않는다.
