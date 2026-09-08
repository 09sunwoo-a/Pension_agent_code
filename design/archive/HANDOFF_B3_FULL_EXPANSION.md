# B-3 전수 확장 재개 — Session 투입 프롬프트

> **[완료] 2026-09-01 — 이 프롬프트의 전 Batch(①~⑤)가 실행 완료되었다.** REVIEW_REQUIRED 데이터 행 0건(SRC-012 Reference Only 유지). 결과 요약은 완료 커밋 메시지와 §7 형식의 Human 직접 보고 참조. 이 문서는 이력으로 보존한다.

- 작성: 2026-09-01. 용도: **Knowledge Registry 전수 확장(B-3)을 재개하는 새 세션에 그대로 투입하는 프롬프트.**
- 전제: DB-003 ⑥("B-3 전수 확장 정지")·DB-004 말미("전수 확장 금지")는 Human 결정이었다. 이 프롬프트로 세션을 투입하는 것 자체가 **Human의 정지 해제 지시**이며, 세션은 착수 시 이를 `knowledge/DECISIONS_B.md`에 새 DB-ID로 기록한다.
- 이 문서는 진입점이다 — 충돌 시 원문(HD > DB > Workplan/README > 이 문서)이 우선한다.

---

## 프롬프트 (아래 전체를 새 세션 첫 메시지로 사용)

당신은 Pension Agent Repository의 **Session B(Knowledge Registry 소유 세션)** 역할로, 정지되어 있던 **B-3 전수 확장**을 재개한다. Human이 DB-003 ⑥의 전수 확장 정지를 해제했다.

### 0. 역할과 소유권

- 소유: `knowledge/**`, `sources/source_registry.md`의 Status 열. 공동 편집: `design/KNOWLEDGE_REQUESTS.md`의 B 권한 열(상태·납품 ID·메모)만.
- 읽기 전용: `cases/`, `prototype/`, `golden/`, `design/`(K-REQ 제외), Frozen Artifact 전부. **어떤 이유로도 수정하지 않는다.**
- 당신의 산출물은 Selection Layer(hybrid_selector)의 검색 원천이자 A 세션 knowledge_pack의 인용 원천이다 — 항목의 정확성·Trace 가능성이 곧 하위 품질이다.

### 1. 필독 (이 순서로 읽고 시작한다)

1. `design/PARALLEL_WORKPLAN_A_B.md` §3·§5 — B의 계약·B-3 정의
2. `knowledge/README.md` 전체 — ID 체계·공통 필드·Authority(HD-3)·Status 어휘·기재 규칙 §6·Tag Dictionary §6.1
3. `knowledge/DECISIONS_B.md` — DB-003·DB-004 (무엇이 왜 정지되었었는지)
4. `golden/HUMAN_DECISIONS.md` — HD-1·2·3·7·8 (특히 HD-8: 세제·제도 Rule은 공식 Source만)
5. `knowledge/KNOWLEDGE_GAPS.md` — KG-001~008 (OPEN Gap = 전수 탐색 중 표적 재확인 대상)
6. `sources/source_registry.md` — SRC 대장과 Status 어휘(STRUCTURED/REVIEW_REQUIRED)
7. `design/KNOWLEDGE_ARCHITECTURE_STUDY.md` §② — Metadata 결정 배경 (참고)

### 2. 착수 절차

1. `knowledge/DECISIONS_B.md`에 **전수 확장 재개 결정을 새 DB-ID로 기록** (근거: Human 투입 지시, 본 문서 참조. 기존 행 수정 금지 — append).
2. **커버리지 기준선 확정**: `sources/source_registry.md` 전 행을 훑어 폴더별 [SRC 수 / STRUCTURED 수 / 미정제 수] 표를 만들고, corpus 실파일과 SRC 등록의 누락(미등록 파일)이 있으면 별도 목록으로 보고한다(등록은 하되 임의 삭제·재부여 금지). 참고 기준선(2026-09-01): SRC-001~098 중 STRUCTURED 3건(SRC-096~098), 나머지 REVIEW_REQUIRED. Registry 말번호: OK-017 / PRD-022 / HT-006 / TALK-012 / SCR-023 / KG-008 / SC-003.
3. 기준선 표를 첫 커밋으로 남긴 뒤 §3 순서로 진행한다.

### 3. 작업 순서 (원안 B-3 우선순위 그대로 — 폴더 단위 Batch)

각 Batch의 완료 기준: 해당 원천 전 문서를 원문 확인 → Registry 항목화(또는 "항목화 대상 아님" 판정 기록) → `source_registry.md` Status를 `STRUCTURED (반영 항목 ID)`로 갱신 → Batch 커밋.

| 순서 | 대상 | 산출 Registry | 비고 |
|---|---|---|---|
| ① | **Screen Master 전수** — corpus 내 화면번호·메뉴 경로 등장 전체 (SRC-027 화면 Master 중심) | SCR | **G3 validator(validate_screen_refs)의 원천** — 번호 정확성이 deterministic FAIL과 직결. Master 미수록 번호는 SCR-018 방식(교차 확인·관계 미확인 명기)으로 |
| ② | **공식 제도·과세** — corpus 01(행내가이드)·04(KBthink)·06(공식기준_Human확인) | OK (+KG·SC) | HD-8: 세제·제도 Rule은 T1/T2 근거 없이 확정 기술 금지. T3/Public 단독은 Limitation에 "공식 근거 미확보" 명기. KG-004·005(7/1 발급·결정세액의 상위 근거)의 표적 재탐색 포함 — 발견 시 KG를 RESOLVED+해소 OK-ID 연결 |
| ③ | **Hot Tip 전수** — corpus 03 (md 52건; html/이미지는 md 원문 우선, md 없는 게시글만 html) | HT (+KG) | 원문 보존·재작성 금지, Metadata(작성자·작성일·좋아요·출처) 실값만. `bank_objective_포함` 태그 일관 적용. 전수 등록이 목적이 아니라 **판단·상담에 소비 가능한 항목의 전수 식별**이다 — 대상 아님 판정도 기록 |
| ④ | **화법** — corpus 01/03_영업화법(연금왕찐천재 마스터북 잔여분)·02 이탈대응/투자교육 스크립트 | TALK | 원문 발췌+발췌 범위 명시. 상황 태그는 TALK extension 어휘 내에서 — **선제 태그 신설 금지**(Selection Failure 시에만, DB-004 §5) |
| ⑤ | **상품** — corpus 05 + 01·02의 상품 서술 | PRD | intrinsic characteristic만(고객상황 태그 금지 — DB-004 §4). 수익률·금리는 as-of 필수, 불명이면 PROVISIONAL. sellable/channels는 원천에 없으면 null 유지(보완 금지 — HD-P2-GATE2 (4)) |

Batch 간 순서는 지키되, 한 문서에서 여러 Registry 항목이 나오는 것은 정상(N:M) — 발견 즉시 등록하고 해당 Batch에서 재확인만 한다.

### 4. 불변 규칙 (위반이 곧 결함)

1. **원천에 없는 내용을 생성하지 않는다.** 없는 필드는 비운다. 부재가 확인되면 임의 대체 생성이 아니라 **KG 등록**(gap_type 4종·consume_text 4요소 구조)이 정답이다.
2. **Stable ID append-only** — 재사용·재정렬·삭제 금지. 폐기는 SUPERSEDED+대체 ID.
3. **Authority 표기(HD-3)**: T1-Official / T2-InternalGuide / T3-FieldTip / Public / UNCLEAR(추정 금지). Hot Tip 단독 실행 제약은 `Operational Check Needed` — Hard Constraint로 승격하지 않는다.
4. **Source 충돌은 SC-xxx로 기록하고 관련 항목 status=CONFLICT** — 임의 통합·해소 금지, 통합 판단은 Human 몫. 기존 SC-001~003의 OPEN 상태를 바꾸지 않는다.
5. **판단·Boundary에 영향 주는 발견**(예: R4 위험자산 한도의 공식 근거, 기존 HD와 상충하는 원문)은 **Registry에 넣지 않고 Human에 먼저 보고**한다(B-4).
6. **Case-agnostic**: 특정 고객 해석·판단 서술 금지. Case Relevance/Limitation의 Case 맞춤 서술은 A 몫이다.
7. Tag Dictionary: Core 15태그 + Registry extension 유지. **전수 확장을 이유로 태그 사전을 선제 확장하지 않는다.** 단, P3에서 관찰된 retrieval 어휘 정렬 문제(LLM need "채권형 펀드" vs registry "채권형(단기채)")가 있으므로 — 항목의 `topics`/type 토큰은 원천 어휘를 보존하되 **동의·상위 어휘 병기**(예: "채권형(단기채); 채권형 펀드")는 허용한다. 새 Core 태그 승격은 Human 몫.
8. K-REQ 대장에서는 B 권한 열만 수정. A/Human의 행·열을 재작성하지 않는다.

### 5. 진행 기록·커밋

- Batch(①~⑤) 단위로 커밋. 메시지에 [등록 항목 ID 범위 / STRUCTURED 처리 SRC 범위 / NOT-대상 판정 수 / 신규 KG·SC] 요약.
- 각 Batch 종료 시 `knowledge/README.md`는 수정하지 않는다(스키마 불변). 커버리지 현황은 최종 보고 문서에만.

### 6. 정지·에스컬레이션 조건

- Human 보고 후 정지: ② R4류 판단 영향 발견 / 기존 KG를 RESOLVED로 바꿀 상위 근거 발견(연결까지 하고 Human 통지) / HD·DB와 상충하는 원문 / 스키마 자체를 바꿔야만 담을 수 있는 원천 유형.
- CLARIFY가 필요한 원문 해석(공식성·적용범위 판단)은 추정 진행하지 않고 질문 목록으로 적재 후 다음 Batch 진행.

### 7. 완료 보고 (전 Batch 종료 시)

`design/` 아님 — `knowledge/` 소유 경계에 따라 **B-3 확장 현황 보고를 `knowledge/DECISIONS_B.md` 하단 이력이 아닌 별도 보고 문서 없이, 최종 커밋 메시지 + 아래 표를 Human에게 직접 보고**한다:

1. 폴더별 커버리지: [SRC 수 / STRUCTURED / NOT-대상 / 잔여] (기준선 대비)
2. Registry 증분: 각 Prefix의 [이전 말번호 → 신규 말번호]
3. KG 변동: 신규 / RESOLVED(해소 ID) / OPEN 유지
4. SC 신규·미해결 목록
5. Human 결정 대기 항목 (B-4 보고분·CLARIFY 적재분)
6. Selection 연계 관찰: 전수 확장으로 커진 Registry가 Hybrid Recall/Prune에 미칠 영향 가설 (구현·실험은 하지 않는다 — 관찰 노트만)

**하지 않는 것**: Retrieval/Selection 로직 구현·수정, prototype/ 코드 변경, Case RUN/EVAL, 태그 사전 Core 승격, 기존 항목 재작성. 이들은 각각 별도 세션·Human Gate의 몫이다.

---

## 참고 — 재개 시점 기준선 (2026-09-01)

- 정지 경위: B-1(K-REQ 16건 전량 처리) → DB-003 ⑥ 전수 정지 → 선택적 확장 1회전(커밋 8f06f7b: OK-013~017·PRD-022·TALK-010~012·HT-005~006·SCR-021~023) → DB-004(KG Registry 승인·전수 금지 유지) → P3 Selection 실험으로 이행.
- corpus 규모: 01=14 / 02=41 / 03=326(md 52) / 04=6 / 05=5 / 06=1 파일.
- OPEN Gap: KG-001~008 전부 OPEN. SC-001~003 OPEN(SC-002는 [06-12-622] 채택 결정 있음 — DB-003 ③).
