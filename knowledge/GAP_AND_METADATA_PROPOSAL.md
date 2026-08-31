# Knowledge Gap 명시 구조 · Selection Metadata 검토 — 설계 제안 (구현 전)

- Status: **DECIDED (2026-08-31, DB-004)** — 본 문서는 제안 기록으로 보존. 결정 요지: §1 KG Registry **승인·구현됨**(`knowledge/KNOWLEDGE_GAPS.md`, KG = Knowledge Coverage State/Negative Evidence로 정의, consume_text는 4요소 구조적 문면으로 제한) / §2.2-1 OK 태그 **승인하되 명칭 `applicability_tags`**(제도적 Context 표현) / §2.2-2 PRD situation_tags **불채택**(intrinsic characteristic만 허용) / §2.2-3 태그 사전 **Core+Extension 방식**(단일 사전 전면 승격 불채택, README §6.1) / §2.2-4 purpose 필드 불추가 **승인**(향후 Knowledge Need 속성으로) / §2.2-5 포맷 전면 통일 **보류**(향후 Registry→parser→Selection Index 구조 검토 시). Session B 작성.
- 배경 근거: `golden/P2_BATCH3_SUMMARY.md` §4-3 — "Knowledge Gap을 명시적으로 알려주면 지키고(GC-23), 알려주지 않은 Gap은 메운다(GC-21)". Gap의 명시가 Gap 메움(임의 생성) 방지의 유효 수단으로 확인됨.

---

## 1. Knowledge Gap Registry 설계안 (`knowledge/KNOWLEDGE_GAPS.md`, KG-xxx)

### 1.1 목적

지금까지 Gap은 세 곳에 흩어져 있다: K-REQ의 NOT_FOUND 행 / OK 항목의 Limitation 문장 / SC 기록. 이 중 **Agent가 소비할 수 있는 형태**(supply나 knowledge_pack에 실릴 수 있는 단위)는 OK-003처럼 "부정 확인을 본문으로 승격한 항목"뿐이었다. GC-23은 그 형태 덕분에 통과했고, GC-21은 그 형태가 없어서 실패했다. KG Registry는 이 형태를 **일반 계약**으로 만든다.

### 1.2 항목 스키마 (초안)

```markdown
### KG-xxx. <무엇이 없는가 한 줄>

| 필드 | 값 |
|---|---|
| gap_type | source_not_found / definition_not_available / official_source_not_found / execution_path_unconfirmed |
| topic | 검색용 키워드 |
| what_is_missing | 부재한 지식의 정확한 범위 (무엇을 물어도 이 Registry가 답할 수 없는가) |
| what_exists_instead | 인접·부분 지식의 ID (OK/HT/TALK/SCR/PRD) — "이것으로 대체하지 말 것" 경계 포함 |
| verified_by | 탐색 범위·방법·일자 (corpus 전수 grep / 표적 재탐색 등 — 부재 주장의 근거) |
| consume_text | **Agent 전달용 문면** — knowledge_pack K-item으로 그대로 실을 수 있는 1~3문장: ① 무엇이 확인되지 않았는가 ② 그래서 무엇을 단정하면 안 되는가 ③ 확인이 필요하면 어디서(화면/절차/공식 기준) |
| related | REQ-ID / Case / SC-ID / HD·DB-ID |
| status | OPEN → RESOLVED(원천 확보 시 — 해소한 OK-xxx 병기, 행 삭제 금지) |
| registered / as_of | 등록일 / 부재 확인 기준 시점 (corpus 스냅샷 기준) |
```

### 1.3 gap_type 정의

| 값 | 의미 | 대표 사례 |
|---|---|---|
| `source_not_found` | 요청 주제의 원천 자체가 corpus에 없음 | 재접근 화법(REQ-006) |
| `definition_not_available` | 용어·지표는 실존하나 **정의·산식**이 없음 | 계좌수익률 vs 상품수익률 표시 기준(REQ-007) |
| `official_source_not_found` | 지식은 있으나 **상위 Authority(T1/T2) 근거가 없음** — T3/Public 단독 | 7/1 증빙 발급(SRC-043 단독), 결정세액 조건(Public 단독) |
| `execution_path_unconfirmed` | 실행 경로(절차·화면·메뉴)의 실존이 확인되지 않음 | 부분이전 절차(OK-003) |

### 1.4 소비 계약 (A와의 인터페이스 — 제안)

- A는 knowledge_pack K-item으로 `KG-xxx`를 기존 5필드 형식 그대로 인용할 수 있다 (Source 필드: `KG-002 (부재 확인: corpus 전수, 2026-08-31)`). **consume_text가 K-item 본문이 된다.**
- Evaluator 관점: KG 인용 Case에서 Agent가 consume_text의 경계를 넘는 서술(원인 설명 생성·가능/불가 단정)을 하면 SG 위반 판정의 명시 근거가 된다 — GC-21 유형의 재발 검증이 deterministic해짐.
- **경계**: KG는 "모른다"를 전달하는 장치이지 Boundary·Expected를 정하는 장치가 아니다. 어떤 Case에 어떤 KG를 동봉할지는 A/Human 몫.

### 1.5 초기 이관 후보 (승인 시 등록 — 현재 미등록)

| 후보 | gap_type | 현재 위치 | 비고 |
|---|---|---|---|
| KG-001 수익률 지표(계좌/상품별) 정의·산식 | definition_not_available | REQ-007 NOT_FOUND + OK-007 Limitation | GC-21 재검증의 직접 재료 — **최우선** |
| KG-002 부분이전 실행경로 | execution_path_unconfirmed | OK-003 본문 | 이미 사실상 KG 형태 — 형식 통일만 |
| KG-003 과거 권유 사절 고객 재접근 화법 | source_not_found | REQ-006 NOT_FOUND + HT-003 노트 | |
| KG-004 소득세액공제확인서 7/1 발급의 공식 근거 | official_source_not_found | OK-009 Limitation | GC-25 PARTIAL(T3 승격)의 직접 재료 |
| KG-005 결정세액 조건의 행내(T1/T2) 근거 | official_source_not_found | OK-008 Limitation | |
| KG-006 투자성향 재분석·상향 안내의 행내 원문 | official_source_not_found | OK-006 Limitation | |
| KG-007 저축은행 정기예금 개별 상품명·금리 | source_not_found | PRD-019 | |
| KG-008 개별 펀드 sellable/channels 현재값 | source_not_found | PRD 전 항목 Unconfirmed | 확인 경로는 OK-017 |

---

## 2. Selection Metadata 검토 (§4 질의축 대응 현황)

### 2.1 현황 매트릭스 (8개 질의축 × Registry 5종)

| 질의축 | OK | PRD | HT | TALK | SCR | 판정 |
|---|---|---|---|---|---|---|
| topic | ○ topics | △ 없음(항목명·product_type으로 부분 대체) | △ search_summary·tags로 대체 | △ tags로 대체 | △ actions 서술 | **PRD만 실질 공백** |
| purpose | △ 없음 | △ 없음 | △ kind | △ 없음 | △ 없음 | 별도 필드 불필요 판단 — §2.2 |
| authority | ○ | ○ | ○ | ○ | ○ | 충족 |
| status | ○ | ○ | ○ | ○ | ○ | 충족 |
| as_of | ○ | ○ | ○ | ○ | ○ | 충족 (SCR 일부 Unknown — 원천 한계) |
| situation_tags | × 없음 | × 없음 | ○ | ○ | × 없음 | **OK가 실질 공백** |
| product_type | 해당 없음 | ○ | 해당 없음 | 해당 없음 | 해당 없음 | 충족 |
| surface | 해당 없음 | 해당 없음 | 해당 없음 | 해당 없음 | ○ | 충족 |

### 2.2 최소 보강안 (승인 시 1회 정비 — 현재 미반영)

1. **OK에 `situation_tags` 추가** — Selection이 "상황→지식"으로 갈 때 OK가 topics(주제어)만으로는 상황 매칭이 약함. TALK의 태그 어휘를 공통 사전으로 승격해 사용.
2. **PRD에 `situation_tags`(또는 topics) 추가** — "만기 재운용", "연금수령 재원", "손실 구간 대안" 등 상황 태그를 상품 카드에 부여.
3. **태그 어휘 사전의 단일화** — 현재 TALK_REGISTRY §태그 어휘가 사실상의 사전. `knowledge/README.md`로 이동해 HT/TALK/OK/PRD 공용화, append-only 관리.
4. **purpose는 별도 필드 불필요** — Registry 종류(OK=판단 근거/PRD=상품 카드/HT·TALK=화법·팁/SCR=실행 위치/KG=부재 고지)가 purpose를 결정적으로 유도. 필드 추가는 중복.
5. **파싱 일관성 정비** — 현재 필드 표기가 블록형(OK/HT/TALK)·1행 표(PRD 일부)·표형(SCR)으로 혼재. Selection Logic이 기계 파싱한다면 "필드명 | 값" 표 형식으로 통일하는 정비 1회 필요(내용 불변·형식만). 구현 세션 요구 확인 후 진행 권장.

### 2.3 하지 않는 것

Retrieval Engine·임베딩·검색 인덱스·Agent Selection Logic 구현은 Session B 범위 밖(본 문서는 Registry 측 준비 상태 점검·제안까지).
