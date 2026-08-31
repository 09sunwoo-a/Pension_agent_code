# Knowledge Architecture & Selection Design Study (P3 준비 — Human Decision 재료)

- Status: **DESIGN STUDY — 구현 없음, Human Gate 대기 (2026-08-31)**. 이 문서는 어떤 Architecture도 확정하지 않는다. Runtime·Prompt·Golden Case·Knowledge Registry를 변경하지 않았다.
- 분석 기반: `knowledge/` Registry 전체(OK 11 · PRD 21 · HT 4 · TALK 9 · SCR 19 · SC 3 · DB 2), `golden/P2_BATCH3_SUMMARY.md` + GC-21·GC-23 EVAL_001 원문, `cases/FAILURE_MAP.md`(F-001~F-012·FC-1·FC-2), `design/CANONICAL_CONTRACTS.md`·`KNOWLEDGE_REQUESTS.md`·`PARALLEL_WORKPLAN_A_B.md`·`TARGET_CONCEPT.md`, `golden/HUMAN_DECISIONS.md`(HD-1~HD-P2-GATE2), `00_Core_Concept_Design.md` §8, `prototype/runtime.py`의 Knowledge 전달 구조.
- 유지 전제 (본 문서의 모든 제안이 종속되는 원칙): Knowledge는 Customer Need를 만들지 않는다(HD-7) / Hot Tip은 Business Rule이 아니다(HD-3) / 투자성향 = 허용 상한(HD-2) / Bank Objective ≠ Recommendation Reason(G4) / Knowledge 부재 시 상식으로 메우지 않는다(HD-P2-GATE2 (2)) / Authority·Epistemic State를 소비 단계까지 보존 / Deterministic Rule과 LLM Reasoning의 역할 구분.

---

## ① Current Knowledge Architecture Assessment

### 1.1 현재 구조가 이미 갖춘 것 (강점)

1. **Registry 5종 + 공통 Metadata가 실물로 존재하고 실전 검증됨.** Stable ID(append-only·SUPERSEDED 보존), source(SRC-ID+문서 내 위치), authority(T1/T2/T3/Public/UNCLEAR), as_of(추정 금지·Unknown 허용), status(ACTIVE/PROVISIONAL/CONFLICT/SUPERSEDED)가 전 Registry에 일관 적용되어 있다. P2 8 Case가 이 구조에서 공급된 Knowledge로 실행되어 PASS 4를 냈다.
2. **Limitation 필수 원칙이 실효를 입증했다.** OK-003의 부정 확인("부분 이전 절차는 corpus 전체에서 확인되지 않음")+Limitation("가능/불가 단정 금지")이 GC-23 PASS의 직접 원인(EVAL_001 §2 ①). 이것은 이 프로젝트가 이미 **Negative Knowledge(부정 확인)를 등록 가능한 1급 지식으로 다룬 첫 사례**다.
3. **수요 주도(demand-driven) 구축 인터페이스가 이미 존재한다.** `design/KNOWLEDGE_REQUESTS.md`(K-REQ)는 사실상 **수동 Knowledge Need Resolver**다 — 유형(official/product/hot_tip/talk/screen = allowed_registry), 필요 내용(topic), 필요 시점, 상태(REQUESTED→DELIVERED/NOT_FOUND/CLARIFY)를 갖고 있고, NOT_FOUND 2건(REQ-006·007)이 기록으로 남았다. 이 관찰이 ④·⑤ 제안의 출발점이다.
4. **소비측 Usage Boundary 전달 구조가 이미 있다.** Case-local knowledge_pack의 5필드(Knowledge/Case Relevance/Limitation→"Usage Boundary"/Authority/Source)가 프롬프트로 전달되며, REV-001에서 F-006(Under-use) 8/8→경미, F-002(Over-application)·F-009(Marketing Trigger) 실질 해소를 만든 검증된 장치다.
5. **Agent 생성 불가 영역의 supply 분리.** 상품 카드·Tip 원문·화면번호는 canonical.json supply로만 공급되고 모델 출력은 ID 참조만 — deterministic validator(supply ⊆ 검사·sellable=false FAIL·C2·화면 S5 단일 위치)가 복사 오류·Hallucination을 원천 차단. P2에서 미끼 상품 8/8 회피, 화면번호 노출 0건.
6. **충돌·잠정 상태의 보존 규율.** SOURCE_CONFLICTS(SC-001~003) 분리 기록 + 관련 항목 status=CONFLICT + 임의 통합 금지, sellable/channels null 유지(HD-P2-GATE2 (4)) — "모르는 것을 모른다고 저장"하는 문화가 이미 자리잡음.

### 1.2 문제와 잠재 위험

**P-1. Gap 표현의 비대칭 — 명시된 Gap만 지켜진다.**
P2의 가장 중요한 관찰(P2_BATCH3_SUMMARY §4.3): *"Knowledge Gap을 명시적으로 알려주면 지키고(GC-23), 알려주지 않은 Gap은 메운다(GC-21)."* 그런데 GC-21에도 Gap은 **전달되어 있었다** — K-001 Limitation에 "차이의 원인(매수 시점 효과 등)을 지식처럼 설명하지 않는다"가 명문으로 있었고, 판단층·S2까지는 지켜졌으나 S4에서 정확히 그 금지된 설명("매수 시점 효과")이 생성됐다. 즉 실패 지점이 둘이다:
- (a) **Gap이 항목 Limitation 산문 속에 묻혀 있으면** 소비 강도가 약하다. GC-23은 Gap이 Knowledge 본문의 핵심 내용(부정 확인 자체가 Content)이었고, GC-21은 Gap이 부속 Limitation이었다.
- (b) Gap을 알아도 **화법 생성 단계(S4)에서 "명료한 설명" 압력이 이긴다**(FC-1 — 이 부분은 Knowledge Selection 설계만으로 해결되지 않는 별도 Semantic Revision 후보, §⑥-10).
향후 Selection이 자동화되면 위험이 커진다: 검색 결과 0건(아무것도 전달 안 됨)과 부정 확인(NOT_FOUND를 적극 전달)이 구분되지 않으면, 자동화된 Selection은 구조적으로 GC-21 상황(Gap 미명시)을 양산한다. → **②·⑤의 Knowledge Gap 1급 객체화 근거.**

**P-2. 항목 단위 Authority가 혼합이라 자동 필터링 정밀도가 낮다.**
OK-001·OK-003·OK-009 등은 한 항목 안에 T2 근거 Content와 T3 단독 서술(횟수 무제한·7/1 발급 등)이 섞여 있고, Limitation에서 산문으로 재격하한다. 사람이 읽는 동안은 작동하지만, "authority ≥ T2 필터"를 기계적으로 적용하는 순간 T3 sub-claim이 함께 통과한다. 이미 사실상 claim 단위 표기((T3 — SRC-072) 같은 병기)가 존재하므로 구조 문제가 아니라 **표기 규칙의 명문화 문제**다.

**P-3. Registry 간 검색 축 불일치.** OK=topics, HT/TALK=situation_tags(+TALK audience), PRD=없음(product_type이 대신), SCR=actions. 수동 Selection에선 무해하나 Registry Routing을 만들려면 최소 공통 검색 축이 필요하다.

**P-4. 화법 지식의 방향성(stance) 미구조화.** GC-21 K-002는 TALK-003(숫자 의미 설명형)과 TALK-004(교체 제안형)의 구분을 **A가 Limitation 산문으로** 걸어야 했다("인지·의향 미확인 상태에 이식하지 않는다"). 이 구분(설명/교체제안/유지지원/재접근/거절극복)은 Talk 선택의 반복 축이 될 것이 명백한데 현재는 태그 어휘에 부분적으로만 존재한다. 잘못 선택되면 고객 의사보다 설득이 앞서는 위험(I 질문)과 직결된다.

**P-5. T3 제도 서술의 승격 경로가 소비 단계에 노출되어 있다.** GC-25 PARTIAL("7/1 이후 해지가 가장 유리합니다" — T3 단독 지식의 확정 승격). HT 기재 규칙 3("Tip 내 제도 서술은 검증하지 않고 공식 버전은 OK로 분리")은 올바르지만, Selection이 HT를 고르면 그 안의 제도 서술도 함께 프롬프트에 들어간다. Selection 단계에서 "이 Tip에는 공식 미확인 제도 서술이 포함됨" 신호가 구조화되어 있지 않다.

**P-6. Pack 크기와 Under-use의 긴장.** P0의 실패(F-006 8/8)는 "Knowledge 9건 평면 나열, Relevance·Limitation 미전달"에서 왔고, 해결은 양이 아니라 **Case Relevance·Usage Boundary 동봉**이었다(HD-6). 반대로 P2에서 최소 supply Case(GC-19·21)는 S5가 빈약했다. Selection 설계는 "많이 주면 under-use/오염, 적게 주면 빈약"의 실측 균형점을 다뤄야 하며, 이는 후술할 Pack 상한(⑥-9)의 Human 결정 재료다.

**P-7. Rule성 지식의 원천 이원화.** HD-2.1 Eligibility 매핑은 HUMAN_DECISIONS+runtime validator가 원천인데 OK-006에도 등재되어 있고, R4(위험자산 70% 한도)는 DB-002로 PENDING(Registry 미등재·Human 보고 상태)이다. deterministic rule의 단일 사실 원천(HD/runtime)과 Registry의 관계를 정의하지 않으면 이중 기입·불일치 위험이 자란다.

**P-8. 저장 형식.** Registry는 md 산문+표. 현 규모(~60항목)에선 강점(리뷰 가능성)이지만, 자동 Selection은 파싱 계약이 필요하다. v1에서는 md 유지 + 파싱 가능한 필드 규율로 충분하고, 형식 전환은 운영형 결정이다.

---

## ② Knowledge Architecture v1 Proposal

### 2.1 (A) Taxonomy — 5 Registry 유지, 신설은 Gap 1건만

**결론: OK / PRD / HT / TALK / SCR 5종을 유지한다.** 각 Registry는 서로 다른 (원문 보존 규칙 × Authority 기본값 × 소비 위치 × 검증 방식)의 묶음이고, P2에서 각자의 소비 경로가 실증됐다. 분류 편의를 위한 신설은 하지 않는다.

검토한 신설 후보와 판정:

| 후보 | 판정 | 근거 |
|---|---|---|
| **Solution Knowledge Registry** | **반대** | "이 상황이면 이 Solution" 형태의 등록은 Situation→Action Rule Base로 변질될 위험이 구조적이다(AGENTS §18 "Customer State → Action 거대 Rule Base 구축" 금지). 현재 필요한 Solution성 지식은 이미 분해 수용된다: 실행 절차·조건·시한 = OK(예: OK-002 전출 처리 절차, OK-005 DO 적용 규칙), 실행 위치 = SCR, 실행 재료 = PRD, 현장 접근 = HT. Solution의 조립("이 고객에게 무엇을")은 Agent의 몫이지 Registry의 몫이 아니다 — 이 경계가 무너지면 "상품·Tip이 있어서 Need가 생기는" 역전이 Registry 층에서 발생한다. |
| **Knowledge Gap Registry (KG-xxx)** | **신설 제안** | 현재 Gap은 세 곳에 흩어져 있다: K-REQ의 NOT_FOUND 상태(REQ-006·007), OK 항목의 부정 확인(OK-003)·PROVISIONAL(OK-007), Case knowledge_pack의 Limitation 산문. P-1(비대칭)의 해소에는 "확인된 부재"를 재사용 가능한 1급 객체로 축적하는 저장소가 필요하다. 스키마는 §⑤-3. **주의**: KG는 "corpus를 다 뒤졌는데 없더라"라는 **탐색 결과 기록**이지 제도적 불가의 단정이 아니다(OK-003 Limitation과 동일한 경계). 신설 여부 자체는 Human 결정(⑥-3) — 대안(OK 안에 negative-confirmation kind로 수용)도 성립한다. |
| **Rule Registry (RULE-xxx)** | **보류 (Human 결정 연계)** | deterministic rule(HD-2.1·R1·R4)의 단일 사실 원천은 HUMAN_DECISIONS+runtime이다. Registry 신설은 이중 기입 위험. 다만 rule_derived Evidence의 `rule_source` 추적 요구(HD-8)와 R4 PENDING(DB-002)이 있으므로, "Rule의 근거 원문(SRC)과 Human 승인 기록을 잇는 색인"이 필요해지는 시점에 재검토. v1은 OK-006 방식(공식 확인 기록을 OK로 등재 + HD 참조)으로 충분. |
| **Concept/Definition Registry** | **불요** | GC-21의 수익률 정의 부재는 "정의라는 별도 유형"의 문제가 아니라 공식 지식의 부재(NOT_FOUND) 문제다. 정의·산식이 확보되면 OK의 정상 항목이다(HD-P2-GATE2 (2)의 "실제 화면/시스템 정의 자료 확보 시 별도 Knowledge 등록 가능"과 정합). |

### 2.2 (B) Metadata — Selection에 실제 필요한 것만, 4문 기준으로

기존 공통 필드(id/title/source/authority/as_of/status/registered)는 전부 유지. 아래는 **추가·정비 검토 대상 전체**를 "왜 / Selection 어느 단계 / 작성 주체 / 필수 여부"로 판정한 것이다. 원칙: v1에서 Taxonomy를 과도하게 만들지 않는다 — 필수 승격은 3건뿐이다.

| Metadata | 왜 필요한가 | Selection 사용 단계 | 작성 주체 | v1 판정 |
|---|---|---|---|---|
| `topics` (전 Registry 공통화) | Registry Routing 후 후보 검색의 최소 공통 축 (P-3) | Retrieval (후보 검색) | B 작성 (원문 키워드 기반 — 반자동 가능) | **필수 승격** — OK에만 있는 topics를 PRD·SCR에도. HT/TALK은 situation_tags가 겸임(이원화하지 않음) |
| `situation_tags` (HT/TALK 기존) | 상황 매칭 (고객 상황 → 화법/Tip) | Retrieval | B 작성 | 유지 (필수) |
| **`stance`** (TALK/HT 신설) | 화법의 방향성: `explain(설명·의미해설)` / `propose_change(교체·가입 제안)` / `retain_support(유지·존중)` / `re_approach(재접점)` / `objection(거절 대응)`. P-4 실증 — 잘못된 stance 이식이 "고객 의사보다 설득이 앞서는" 실패의 직접 경로 | Filter (고객 의사·인지 상태와 대조) | B 작성 (원문에서 판별 가능 — TALK-002 caution·TALK-004 발췌가 이미 이 구분을 산문으로 함) | **필수 승격 제안** (B 스키마 변경 — Human 승인 필요, ⑥-5) |
| `bank_objective_포함` (기존 태그) | HD-7/G4 — 추천사유 오용 식별 | Filter/전달 경계 | B 작성 | 유지 (필수). 처리 방식은 ⑥-6 |
| **`time_sensitivity`** | 금리·수익률(월 변동) vs 절차(개정 시만) vs 시한 규칙 — freshness gate의 판단 근거. as_of만으로는 "얼마나 오래되면 낡은 것인지"를 모른다 | Filter (freshness) | B 작성 (`volatile-monthly` / `stable-procedural` / `regulatory` 3값 정도) | **선택 추가 제안** — PRD·OK의 수치 항목 우선. 전 항목 소급은 하지 않음 |
| `audience` (TALK 기존) | 원천이 명시한 대상 고객 | Filter | B (원천 명시분만) | 유지 (선택) |
| claim-level authority 표기 규칙 | P-2 — 항목 내 T3 단독 sub-claim의 기계 식별 | Filter (authority gate) | B (이미 관행 존재 — `(T3 — SRC-072)` 병기) | **규칙 명문화만** (새 필드 아님): "Content 불릿에서 항목 대표 authority와 다른 근거는 반드시 `(T3)`/`(Public)` 병기" |
| `permitted_use` / `prohibited_use` (항목별) | 항목별 사용 경계 | 전달 | B 또는 A | **v1 보류** — Registry 단위 Usage Boundary(§2.3 표)가 default를 담당하고, 항목별 예외는 기존 Limitation 산문으로 충분. 항목마다 이 두 필드를 채우게 하면 Taxonomy 과설계 + 형식적 복붙 위험 |
| `lifecycle/event`, `customer_situation`, `management_action`, `conversation_goal` (일반 분류축) | 상황 온톨로지 | Retrieval | — | **v1 보류** — situation_tags/topics/stance로 실수요가 커버된다. 별도 통제 어휘를 지금 고정하면 P2 18 Case 관찰만으로 온톨로지를 확정하는 셈 (AGENTS §2 위반 성격) |
| `applicable_conditions`, `limitations` | 적용 조건·한계 | 전달 | B | 기존 Content 조건부 기재 규칙 + Limitation 필수로 이미 존재 — 신설 불요 |
| `delivered_for` (기존) | Need↔Knowledge 추적 | 이력/디버깅 | B | 유지 — §⑤-1 Knowledge Need의 `need_id`와 연결되는 기존 장치 |

### 2.3 (G) Registry별 Usage Boundary (v1 제안 표)

Registry 단위 default. 최종 판정 단위는 **claim의 authority**다(P-2) — OK 항목이라도 T3 병기 claim은 T3 규칙을 따른다.

| Registry | Allowed Use | Forbidden Use | Typical Consumer |
|---|---|---|---|
| **OK** (T1/T2 claim) | 제도·절차·시한·과세 구조의 판단 근거 / Eligibility·실행 가능성 판단 / Required Confirmation의 근거 / S1~S4 사실 설명 | 최종 확정 계산값 제시(HD-1) / Limitation이 금지한 단정 / 조건부 사실의 무조건화 | Customer State Interpretation · Management Judgment · Required Confirmation · S2/S3 |
| OK 내 T3/Public 병기 claim | 실무 참고 + Operational Check Needed 연결 | 제도·실행 가능성의 확정 근거 (GC-25 위반 유형) | Required Confirmation · S2 [상담 전 확인] |
| **PRD** | Direction·Solution Type 확정 **후** Candidate 재료 / Hard Constraint(C2)·sellable 필터의 입력 / 카드 사실(수익률+기간+as_of) | Management Need·Direction의 생성 근거("좋은 상품이 있으니 관리 필요") / 수익률 단독 추천 논리 / sellable·channels null의 임의 보완 | Solution/Product Candidate 단계 · S3 카드 |
| **HT** | 상담 접근·순서·준비사항·현장 예외·실행 전 확인 / S5 원문+Metadata | Management Need 생성 / Hard Constraint·가입/실행 가능 최종 판정(HD-3) / Tip 내 제도 서술의 Fact 승격 / bank_objective 서술의 추천사유 사용 | S4 합성 재료 · S5 |
| **TALK** | S4 표현·구조 재료 (stance가 고객 상태와 일치할 때) | 새로운 Fact·판단 생성 / stance 불일치 이식(교체제안형→의사 미확인 고객) / 통계·경험 서술의 보장 화법 승격(TALK-003·005 caution) | S4 |
| **SCR** | 실행 위치 안내(S5 단일 위치, G3) / Operational Check의 확인 화면 연결 | Management Direction 생성 / S1~S4 화면번호 노출 / 원천 미확인 화면 생성 | S5 · Execution Validation |
| **SC** | 충돌 존재의 전달("양쪽 값 + 임의 사용 금지") | 임의 해소·평균·최신 단독 채택 | Knowledge Gaps/Conflicts 섹션 |
| **KG** (신설 시) | "확인되지 않음"의 적극 전달 / Required Confirmation·Operational Check 연결 근거 | 부재의 "불가" 승격 / 상식 기반 대체 설명의 허용 근거로 오독 | Knowledge Gaps 섹션 · S2 |

**기존 원칙과의 충돌 검토**: 위 표는 HD-1·2·3·7, G3·G4, HD-P2-GATE2 (1)~(4)의 재배열이며 신규 제약을 만들지 않는다. 한 가지 긴장은 "PRD가 Direction 확정 후에만"과 이탈 Case의 현실(GC-23에서 GIC 카드가 대안 제시에 필요) — 그러나 GC-23의 실제 사용도 "확인+조건부 대안" 구조 안에서였으므로 "Direction(조건부 포함) 이후"로 읽으면 충돌 없다.

---

## ③ Knowledge Selection Alternatives (C 질문)

전제: 현재 Runtime은 **단일 LLM Call**(Evidence+Constraint+Knowledge Pack → 구조화 판단+Brief)이고, Pack은 Freeze 시점에 사람이 구성한다. 즉 지금의 Selection은 "compile-time·수동"이다. 비교는 이 기준점 대비다.

### Option 1 — Evidence에서 한 번에 전체 검색 (single-shot retrieval)

Evidence(9-Block)를 질의로 삼아 5 Registry 전체에서 관련 항목을 한 번에 검색해 Pack을 구성.

| 축 | 평가 |
|---|---|
| 판단 오염 위험 | **높음.** 판단 전에 상품·Tip이 검색되어 함께 주입된다 — "상품이 있으니 Need가 생기는" 역전(HD-7 위반 압력)과 F-009형 오용의 재료를 구조가 제공. Judgment-support와 Action-support의 구분이 없어 stance 불일치 화법(P-4)도 그대로 들어감 |
| Token 비용 | 낮음~중간 (1회 검색, 단 무관 항목 혼입으로 Pack 비대 → F-006/F-002 재발 위험, P-6) |
| 구현 복잡도 | 최저 |
| 디버깅 | 나쁨 — "왜 이 항목이 들어왔나"가 유사도 점수뿐 |
| 운영 확장성 | 검색 자체는 확장되나 오염 통제 장치가 없어 규모가 클수록 악화 |
| 목업 단계 적합성 | 낮음 — 지금 검증하려는 경계(Knowledge가 판단을 역전하지 않는가)를 검증 불가능하게 만든다 |

### Option 2 — Two-stage Selection (Judgment-support → Action-support)

```text
Stage 1: Evidence / Preliminary Interpretation → Knowledge Need(judgment) → OK(·KG·SC)
Stage 2: Management Judgment / Direction → Knowledge Need(action) → PRD / HT / TALK / SCR
```

| 축 | 평가 |
|---|---|
| 판단 오염 위험 | **낮음 (구조적 차단).** 상품·화법·Tip은 Direction이 선 뒤에만 조회된다 — HD-7·G4·Candidate Pool 원칙(TARGET_CONCEPT §4.1 "먼저 방향/유형 판단, 그 후 Pool 내 후보")과 판단 파이프라인 자체가 이 순서다. 현재 구조의 supply(상품·Tip·화면) vs knowledge_pack(판단지식) 분리는 이미 Two-stage의 물리적 전신이다 |
| Token 비용 | 중간 (검색 2회, 단 각 Stage의 후보 폭이 좁아 Pack은 오히려 작아짐) |
| 구현 복잡도 | 중간. **핵심 쟁점**: Stage 2의 질의가 되려면 "Direction"이 Stage 1과 2 사이에 존재해야 한다 — (a) Runtime을 2-call로 분리(Preliminary Judgment call → Selection → Final call)하면 명백한 Runtime Semantic Change(Human Gate), (b) 1-call을 유지하고 Selection만 2단으로 나누면(아래 v1 변형) call 분리 없이 가능 |
| 디버깅 | **좋음** — Stage별로 "어떤 Need가 생겼고 무엇이 응답됐나"가 남는다. NOT_FOUND가 Stage 단위로 자연 발생(→ Gap 객체) |
| 운영 확장성 | 좋음 — Stage별로 Retrieval 방식(BM25/Vector/구조 질의)을 독립 교체 가능 |
| 목업 단계 적합성 | **높음** — 단, v1에서는 Stage 경계를 "LLM call 경계"가 아니라 "Selection 작업 경계 + 프롬프트 내 섹션 경계"로 구현하는 변형(아래)이 적합 |

### Option 3 — Agent가 필요할 때마다 Tool/Retrieval 호출

| 축 | 평가 |
|---|---|
| 판단 오염 위험 | **통제 불가.** 모델이 언제 무엇을 검색할지 결정 — "상품 먼저 검색 후 판단 구성" 경로를 막을 방법이 프롬프트 지시뿐. allowed_registry 강제도 호출별 검사 장치가 추가로 필요 |
| Token 비용 | 예측 불가 (다회 왕복) |
| 구현 복잡도 | 최고 — Gemma 4(31b)의 tool-use 신뢰성 자체가 미검증이며, 검증 비용이 Selection 검증 비용에 합산된다 |
| 디버깅 | 나쁨 — 호출 순서·질의가 비결정적, Frozen 재현성(동일 입력→동일 Pack) 상실 |
| 운영 확장성 | 장기적으론 유연하나 감사 가능성이 요구되는 도메인 특성과 긴장 |
| 목업 단계 적합성 | **부적합** — Frozen Case·Immutable Run·재현 가능 평가라는 현 방법론과 정면 충돌 |

### 추천안 (Human Decision 분리 포함)

**추천: Option 2의 v1 변형 — "Two-stage를 Selection 층에서 구현하고, LLM call은 아직 나누지 않는다."**

- Selection 작업(당분간 수동/규칙 기반)이 Stage 1(judgment-support)과 Stage 2(action-support)를 **별도의 Knowledge Need로** 생성·기록하고, Pack 안에서 두 그룹을 명시적으로 분리해 전달한다(§⑤-2 구조). Stage 2 Need의 근거는 v1에서는 Case 설계 시점의 Expected Direction 범위(사람이 앎)로 충분하다 — 이는 현재 A가 Freeze 때 하던 일을 형식화한 것이지 새 판단 규칙이 아니다.
- 이렇게 하면: 판단 오염 차단 구조를 지금 검증할 수 있고(P3 Case로), NOT_FOUND가 Stage별로 남으며, 이후 2-call 분리는 "이미 분리된 두 그룹을 서로 다른 call에 주는" 기계적 변경으로 축소된다.
- **Human Decision으로 분리하는 것**: (i) LLM call 분리(진짜 runtime Two-stage) 여부와 시점 — Semantic Change이므로 P3 결과를 본 뒤 결정 권고(⑥-1). (ii) Stage 1에 "Preliminary Interpretation"을 LLM으로 둘지(그 출력이 Stage 2 질의가 됨) — v1에서는 불요.

---

## ④ Recommended Selection Flow (D 질문 포함)

### 4.1 (D) Knowledge Need Resolver — 필요하다, 그리고 절반은 이미 있다

바로 검색하지 않고 먼저 Knowledge Need를 만드는 구조의 장단점:

- **장점**: ① allowed_registry로 판단 오염 차단이 Need 수준에서 걸린다(eligibility Need에 HT가 응답할 수 없음). ② purpose별 authority 요구가 명시된다(제도 Need = T1/T2, 화법 Need = T2/T3). ③ **Gap이 관측 가능해진다** — "요청했는데 없음"은 1급 기록(NOT_FOUND)이 되고, 요청 자체가 없으면 Gap도 없다는 현재의 맹점(P-1)이 해소된다. ④ 디버깅: Pack의 모든 항목이 어느 Need에 대한 응답인지 추적된다(`delivered_for`의 일반화). K-REQ 운영이 이 장점 전부를 이미 소규모로 실증했다(NOT_FOUND 2건이 Case Boundary 조정으로 이어진 것 — REQ-007→GC-21 재정의).
- **단점/위험**: ① purpose·topic 어휘를 온톨로지로 고정하면 Case-driven 원칙과 충돌 — purpose는 **열린 어휘**로 시작해야 한다(REV-001에서 Judgment 목록을 "Ontology로 고정하지 않는다"고 한 것과 동일한 이유). ② Need 생성 주체가 LLM이 되는 순간 "무엇을 모르는지 아는 능력"을 모델에 요구하게 된다 — GC-21이 보여주듯 모델은 자신이 모르는 것을 잘 모른다. ③ 단계 추가 = 지연·복잡도.
- **v1 결론**: Need Resolver를 **문서 형식과 기록 규율로** 도입한다(K-REQ 스키마의 형식화, §⑤-1). 생성 주체는 v1 = Human/Session A(현행 유지), v1.5 = LLM이 Evidence에서 Need 후보 초안 생성 + Human 확정, 운영형 = LLM 생성 + deterministic routing/gate 검증. 주체 전환 시점은 Human 결정(⑥-2).

### 4.2 추천 Flow (v1 / 운영형 이원 표기)

```text
Evidence (canonical 9-Block)
  ↓ [1] Preliminary Interpretation        v1: 없음(Case 설계자가 수행) / 운영형: LLM (판단 아닌 topic 식별까지만)
  ↓ [2] Knowledge Need 생성 (Stage 1/2 구분) v1: Human·A 작성 (형식화된 K-REQ) / 운영형: LLM 초안 + deterministic 검증
  ↓ [3] Registry Routing                   deterministic (need.allowed_registry → 대상 파일/인덱스)
  ↓ [4] Retrieval (후보 수집)               v1: 수동·topics/situation_tags 기반 규칙 / 운영형: BM25+Vector Hybrid
  ↓ [5] Status / Authority / Freshness Filter   deterministic (순서 고정: status → registry boundary → authority-by-purpose → freshness)
  ↓ [6] Selection (후보 중 채택·정리)        v1: Human·A (Case Relevance·Limitation 작성 포함) / 운영형: Rerank + LLM 요약 금지(원문 발췌 유지)
  ↓ [7] Gap Declaration                    deterministic 골격(need에 채택 항목 0건 or authority 미달 → KG 초안) + Human 확정(implication/forbidden 문구)
  ↓ [8] Knowledge Pack 조립 (§⑤-2)         deterministic (Stage 1/2 섹션 분리, supply 분리 유지)
  ↓ Agent (기존 v3 1-call — 변경 없음)
```

책임 주체 요약: **deterministic** = [3][5][8] + [7] 골격. **LLM** = 운영형의 [1][2][4][6] 보조 (v1에서는 0). **Retrieval** = [4]. **Human** = v1의 [2][6][7], 그리고 모든 단계의 규칙 승인.

핵심 설계 판단 2가지:
1. **[5]를 ranking이 아니라 순서 고정 gate로 둔다** (F 질문의 답, §4.3).
2. **[7]이 [6]의 실패가 아니라 정상 출력이다** — 0건·미달은 Pack에 "없음"으로 적극 실린다. 이것이 GC-21→GC-23의 차이를 구조로 옮기는 지점이다.

### 4.3 (F) Authority × Relevance — 단일 score 반대, purpose-gated lexicographic

Relevance / Authority / Freshness / Status / Purpose Fit을 하나의 score로 합산하는 방식은 부적절하다: 가중합에서는 "relevance 매우 높은 T3 Hot Tip"이 "relevance 중간인 T2 공식"을 이길 수 있고, 그 결과가 제도·세제·실행가능성 판단에 쓰이면 GC-25 유형(T3 승격)이 **Selection 층에서** 재생산된다. 대신:

```text
후보 → [Gate 1] status: SUPERSEDED 제외(대체 ID로 치환), CONFLICT는 SC 동반 시만 통과
     → [Gate 2] registry boundary: need.allowed_registry 밖 제외
     → [Gate 3] authority-by-purpose:
         purpose ∈ {eligibility_check, 제도/세제/시한, 실행가능성} → T1/T2 claim만 '판단 근거'로 채택.
             T3/Public-only 응답은 제외하지 않고 'operational_reference'로 강등 채택 (Operational Check Needed 부착)
         purpose ∈ {consultation_support, execution_support} → T2/T3 허용 (Tip 내 제도 서술은 비승격 노트 필수)
     → [Gate 4] freshness: time_sensitivity=volatile인데 as_of 미달/Unknown → 'as-of 재확인 필요' 부착 (제외 아님)
     → [Rank] 여기서만 Relevance로 정렬·상한 적용
```

즉 **Authority는 제도·실행가능성 purpose에서 Relevance에 우선한다** — 단 "우선"의 의미는 배제가 아니라 **역할 강등**(판단 근거 → 확인 항목)이다. 배제해 버리면 T3에만 있는 실행 제약(7/1 발급 등)이 사라져 확인 항목 도출조차 못 하게 된다. HD-3의 "적극 활용하되 단독 확정 금지"의 Selection 번역이 이것이다.

### 4.4 (H) Product Selection — 별도 구조가 맞다 (Retrieval이 아니라 Pool 구성)

Product는 일반 Knowledge Retrieval과 성격이 다르다: 정답이 "관련 문서"가 아니라 "Hard Constraint를 통과한 후보 집합"이고, 오류 비용이 deterministic 검증 가능하다. 분담 제안:

| 단계 | 담당 | 근거 |
|---|---|---|
| Product Registry 검색 (Direction/Solution Type → product_type·특성으로 후보 재료 조회) | **Knowledge Selection Layer** (Stage 2) | PRD의 topics/product_type 질의 — 일반 Retrieval과 동형 |
| Candidate Pool 구성 (Case에 동봉할 후보 집합 확정 + sellable/channels null의 '미확인' 상태 부착) | **Selection Layer + Human** (v1) — 운영형: Selection Layer + 실제 Product DB | Pool은 supply 계약의 재료 — "여기 없는 상품 생성 = FAIL" 원칙 유지 |
| Hard Constraint filtering (C2 성향 상한, sellable=false 제외) | **기존 Runtime deterministic** (변경 없음) | HD-2.1 validator가 이미 검증된 장치. Selection 층으로 옮기면 안 된다 — Pool에 미끼(성향 밖 등급)를 남겨 모델의 회피를 검증하는 현 설계(P2 8/8 회피)와, 최종 안전망의 이중 구조가 유지되어야 함 |
| Candidate ranking | **v1: 하지 않음** (LLM이 소수 Pool에서 선택) / 운영형: deterministic 우선(수익률 정렬 아님 — Fit 축) | 수익률 단독 추천 금지 원칙상 ranking 기준 자체가 Human 결정 사항 |
| Customer–Product Fit reason 생성 | **기존 Agent LLM** (변경 없음) | CANONICAL_CONTRACTS §2.1 "추천사유는 계약에 없다 — Agent 생성" |

즉 Selection Layer의 책임은 "**Pool 재료 공급과 미확인 상태 전달까지**"이고, 걸러내기(deterministic)와 고르기·설명(LLM)은 기존 구조를 건드리지 않는다. 미끼 상품 포함은 목업 Case 설계 기능(A/Human)으로 유지 — 운영형에서는 자연히 사라지고 그 자리를 eligibility filter가 맡는다.

### 4.5 (I) Hot Tip / Talk Selection — 필요한 Filter·Boundary

열거된 4가지 위험별 대응:

| 위험 | Selection 단계 대응 (v1) |
|---|---|
| Bank Objective가 추천 논리에 침투 | `bank_objective_포함` 태그를 **전달 경계**로: 태그 항목도 Pool에 들어갈 수 있으나(원문 보존·절차 가치 — "동기는 버리고 절차만" 기존 규칙), Pack에서 해당 항목에 "추천사유 사용 불가(HD-7/G4)" 경계를 기계 부착. **Tip 전체가 Bank Objective 목적인 경우**(예: PRD-020의 실물이전 방어 활용 서술)는 consultation_support Need에 대한 응답으로 채택하지 않음. 상세 정책은 ⑥-6 |
| 고객 의사보다 설득·거절극복이 앞섬 | `stance` 필터(§2.2): 고객의 인지·의사 Evidence가 없으면 `propose_change`/`objection` stance 화법을 채택하지 않거나 조건부 라벨("고객이 교체 의향을 밝힌 경우에만") 부착. GC-20(거절 극복 단일 방향)·GC-21 K-002 Limitation의 구조화 |
| T3 경험칙의 Fact 승격 | Tip 내 제도·세제 서술 감지 시 "공식 근거 확인 필요" 노트를 **Selection이 기계 부착**(HT 기재규칙 3의 소비측 집행). 해당 제도 사실의 OK 버전이 존재하면 **자동 동반 선택**(HT-004 ↔ OK-001 패턴), 없으면 KG 후보 |
| 현재 상황과 맞지 않는 화법 | situation_tags·audience와 Evidence의 대조를 Selection checklist화 (v1: 수동 체크 기록, 운영형: tag 매칭 filter). 불일치 채택 시 사유 기록 의무 |
| (추가) S4 확실성 인플레이션 (FC-1) | **Selection만으로 못 막는다** — 화법 재료가 완벽해도 S4 합성 단계에서 확정화가 발생(GC-25는 재료가 아니라 합성이 승격함). 이 부분은 SYSTEM_ROLE 원칙 18의 S4 강화라는 별도 Semantic Revision 사안(P2 Summary §5(a))이며 본 설계의 범위 밖임을 명시 (⑥-10) |

---

## ⑤ Minimal Schema Proposal

세 Schema 모두 **최소 필드**만 담는다. v1에서는 md 표/블록으로 기록하고(파싱 가능한 필드명 유지), JSON 직렬화는 구현 게이트에서.

### ⑤-1 Knowledge Need (K-REQ의 형식화·일반화)

```yaml
need_id: KN-001            # Stable ID (Case-local: GC-xx/KN-001)
case: GC-xx                # 또는 COMMON
stage: judgment | action   # Two-stage 구분 (③ 추천안의 핵심 축)
purpose: eligibility_check | rule_structure | procedure | consultation_support
         | product_material | execution_support | ...   # 열린 어휘 — 온톨로지 고정 금지
topic: "IRP 계약이전 시 실행 가능한 방식"   # 자유 서술 (검색 질의의 원문)
allowed_registry: [OK]     # 응답 가능 Registry — Gate 2의 근거
authority_required: T2+    # 이 purpose에서 '판단 근거'로 인정할 최소 Authority (Gate 3)
freshness_required: null | "as_of >= 2026-01" | volatile-ok   # 시점 요구 (해당 시만)
needed_by: freeze | run | reference   # 기존 K-REQ '시점' 승계
status: REQUESTED | DELIVERED | NOT_FOUND | PARTIAL | CLARIFY
resolved_by: [OK-003]      # 응답 항목 ID (DELIVERED/PARTIAL 시) — Registry delivered_for와 상호 참조
```

기존 K-REQ 대비 추가는 `stage`·`purpose`·`authority_required`·`freshness_required` 4개뿐이며, 나머지는 현행 열의 개명이다.

### ⑤-2 Selected Knowledge (= Knowledge Pack v-next 조립 계약)

기존 5필드 K-item(Knowledge / Case Relevance / Limitation / Authority·Status / Source)은 **그대로 유지**하고(REV-001로 검증된 전달 형식), Pack 수준의 구조만 추가한다:

```yaml
knowledge_pack:
  case: GC-xx
  judgment_support:        # Stage 1 응답 — OK(·Human-approved rule 참조)
    - k_id: K-001
      need_ref: KN-001     # 어느 Need의 응답인지 (traceability)
      registry_ref: OK-003
      # 이하 기존 5필드 그대로
  action_support:
    product_support:       # PRD 참조 → canonical supply.product_candidates 재료 (이중 기입 금지 — 참조만)
      - { registry_ref: PRD-018, need_ref: KN-004, note: "sellable null — 상담 전 확인" }
    consultation_support:  # HT/TALK — stance·경계 부착
      - { registry_ref: TALK-003, need_ref: KN-005, stance: explain,
          boundary: "통계 서술 — 보장 화법 승격 금지" }
    execution_support:     # SCR 참조 → supply.screens 재료
      - { registry_ref: SCR-001, need_ref: KN-006 }
  knowledge_gaps:          # ⑤-3 객체 — '없음'의 적극 전달 (0건이어도 섹션은 존재)
    - KG-...
  conflicts_limitations:   # SC 참조 + Pack 수준 주의
    - { sc_ref: SC-001, note: "예금자보호 한도 — 두 수치 모두 사용 금지" }
  budget_note: "K-item n건 / tip m건 — 상한 규칙 대비 기록"   # P-6 관찰용
```

**토큰·과다 전달 통제**: Pack 상한은 지금 숫자로 확정하지 않는다(P2 실측: K-item 3~5·전달 필드 5종이 작동 범위였고, P0의 9건 평면 나열은 실패). v1 규칙은 (a) Need 없는 항목은 Pack에 들어올 수 없다(상한보다 강한 통제), (b) 원문 발췌는 HT/TALK 기존 발췌 범위 규칙 유지, (c) budget_note로 실측 축적 후 상한을 Human이 확정(⑥-9).

### ⑤-3 Knowledge Gap (1급 객체 — E 질문)

```yaml
gap_id: KG-001             # 재사용 가능 Gap은 knowledge/에 축적, Case-local이면 GC-xx/KG-001
need_ref: KN-002
status: NOT_FOUND | PARTIAL | AUTHORITY_INSUFFICIENT | FRESHNESS_INSUFFICIENT | CONFLICT
scope_searched: "corpus 전체 (SRC-001~098) + 화면 Master"   # '어디까지 찾고 없었는가' — 부재≠불가의 경계 명시
missing: "두 수익률 지표의 공식 산정 기준·정의"
implication: "차이의 원인을 설명할 근거 없음"
allowed: "산정 기준의 확인 필요를 안내하고 Required Confirmation으로 연결"
forbidden: "일반 금융 상식으로 원인을 추정·설명 (매수 시점 효과 등)"
nearest: [OK-007]          # 인접 항목 (있을 때 — '부분 납품'의 연결)
registered / as_of: ...
```

**각 상태의 Agent Reasoning 전달 방식 제안**:

| 상태 | Pack에서의 전달 | Agent에 기대하는 행동 |
|---|---|---|
| `NOT_FOUND` | KG 객체 전문 (missing/implication/allowed/forbidden) | 확인 연결·설명 생성 금지 (GC-23 실증 경로) |
| `PARTIAL` | KG + nearest 항목 (OK-007 방식 — "화면에 무엇이 표시되는가까지만") | 확인된 범위만 사용, 나머지는 NOT_FOUND와 동일 |
| `AUTHORITY_INSUFFICIENT` (T3/Public만 존재) | 해당 claim + "공식 근거 미확보" + Operational Check Needed | 가능성 안내까지만, 확정 판단 금지 (GC-25의 Expected) |
| `FRESHNESS_INSUFFICIENT` (as_of 미달·Unknown) | 값 + as_of + "조회 시점 재확인 필요" | 수치 인용 시 기준일 병기, 실행 전 재확인 항목화 |
| `CONFLICT` | SC 객체 (양쪽 주장+원문 위치) — 값 자체는 비전달 또는 양측 병기 | 임의 해소 금지, 확인 필요 전달 (SC-001 처리 방식의 일반화) |
| `SUPERSEDED` | **Agent에 전달하지 않음** — Selection Gate 1에서 대체 ID로 치환 | (Agent 개입 불요 — 기계 처리) |

**주의(설계 경계)**: `forbidden` 필드는 epistemic 경계("무엇을 근거 없이 만들지 말라")에 한정한다. 특정 Case의 정답 행동을 유도하는 문구("~를 추천하지 말 것")를 넣기 시작하면 knowledge_pack 금지 조항("Frozen Expected Behavior를 우회하기 위한 숨겨진 지침")을 위반하는 뒷문이 된다.

---

## ⑥ Open Human Decisions (설계 확정 전 Human이 결정할 사항)

1. **Two-stage의 구현 깊이**: v1은 "Selection 층 2단 + 1-call 유지"(③ 추천). LLM call 자체를 2단으로 나누는 것(Preliminary Judgment call 도입)은 Runtime Semantic Change — P3 결과 확인 후 결정할지, P3에서 함께 검증할지.
2. **Knowledge Need 생성 주체 전환 시점**: v1 = Human/A(현행 형식화), 이후 LLM 초안+Human 확정으로 언제 넘어갈지. LLM이 Need를 만들기 시작하는 순간이 "모델이 자신의 무지를 식별해야 하는" 첫 지점임(GC-21 유형 위험의 이동).
3. **KG Registry 신설 vs OK 내 수용**: KG-xxx 파일 신설(②-A 제안)인지, OK에 `negative_confirmation` kind로 수용(OK-003 현행 방식 유지)인지. 신설 시 knowledge/README 스키마 개정(B 소유) 필요.
4. **purpose 어휘 초안 승인**: ⑤-1의 purpose 예시 목록을 열린 어휘로 승인 (고정 온톨로지가 아님을 결정문에 명시 권고).
5. **TALK/HT `stance` 필드 추가**: B Registry 스키마 변경(DB-001로 승인된 스키마의 개정) — B 세션 작업 지시 필요. topics 공통화·time_sensitivity·claim-level authority 표기 규칙(②-B의 필수/선택 승격 3+1건)도 동일 게이트.
6. **bank_objective 태그 항목의 Selection 정책**: (a) consultation_support 응답에서 제외 vs (b) 채택하되 "추천사유 사용 불가" 경계 기계 부착(④-5 제안은 (b)+전체가 Bank Objective인 항목만 (a)). 어느 쪽이든 원문 보존·S5 제공과는 별개.
7. **Authority-by-purpose gate 표(④-4.3) 승인**: 특히 "T3 배제가 아니라 operational_reference로 강등"이라는 처리와, 제도·세제·실행가능성 purpose의 T1/T2 최소선 명문화(HD-3·HD-8의 Selection 번역이므로 신규 제약은 아니라고 판단하나 확인 필요).
8. **Rule성 지식의 위치**: R4(DB-002 PENDING)의 처리와 함께, deterministic rule의 원천(HD/runtime)과 Registry(OK)의 관계 원칙 — "OK는 근거 원문의 색인, 판정은 HD+validator"로 정리할지.
9. **Pack 상한/토큰 예산**: 지금 확정하지 않고 budget_note 실측 축적 후 결정(⑤-2 제안)에 동의하는지, 아니면 P3 전에 잠정 상한(예: K-item ≤ 6)을 둘지.
10. **FC-1(S4 확실성 인플레이션) 대응의 우선순위**: 본 문서는 이것이 Knowledge Selection 설계로 해결되지 않는 별도 Semantic Revision(SYSTEM_ROLE 원칙 18의 S4 강화)임을 확인했다(GC-21은 Gap이 전달돼도 S4에서 위반). P2 Summary §5(a)의 선관찰 vs 선교정 결정과, 본 Selection 설계의 P3 착수 순서.
11. **sellable/channels 실데이터 확보 방침**: null 유지 원칙(HD-P2-GATE2 (4))은 목업에선 작동하나, Selection이 Product Pool을 만들기 시작하면 "전 상품 미확인"이 모든 Case의 확인 항목을 동형화한다. 실원천(상품 시스템) 확보 계획 또는 목업용 명시적 scenario assumption 표준을 정할지.

---

## ⑦ Proposed P3 Validation Cases (Case Pattern 제안 — Golden 작성·수정 아님)

Knowledge Selection Logic 검증을 위한 신규 Case Pattern 8건. 기존 Golden Case는 변경하지 않으며, 아래는 후보 설계 방향의 서술이다 (실제 Case화는 Gate 승인 후 별도 작업).

| # | Pattern | 검증 대상 | 핵심 설계 | 성공 기준 |
|---|---|---|---|---|
| P3-1 | **Stage 분리 역검증** | "Knowledge가 Need를 만들지 않는다" | Judgment가 '유지/확인 우선'으로 끝나야 할 Evidence + Stage 2 Pool에 매력적 상품·Tip을 의도적으로 동봉 | 상품·Tip이 Direction 생성에 미사용 — Direction이 Evidence만으로 서고, Pool은 미인용으로 남음 |
| P3-2 | **Gap 명시 대조 Pair** | KG 객체의 효과 정량화 (GC-21↔23 차이의 통제 실험) | 동일 Evidence·동일 Knowledge 부재 상황을 (a) KG 객체 포함 Pack (b) 단순 0건 Pack으로 이원 실행 | (a)에서 확인 연결, (b)에서 Gap 메움 재현 — "명시가 유효 수단"의 인과 확인 |
| P3-3 | **Authority Gate — T3/T2 공존** | GC-25 유형의 일반화 | 같은 topic에 T3 단정 서술(Tip)과 T2 조건부 서술(공식)이 함께 선택된 Pack | T2 조건부가 판단 근거, T3는 확인 항목으로 강등 유지 — "가장 유리합니다" 류 확정 승격 없음 |
| P3-4 | **CONFLICT 전달** | SC 객체의 소비 | 판단에 실제 필요한 값이 SC 상태(예: 예금자보호 한도 유형)인 Pack | 임의 해소·평균·최신 단독 채택 없음, 양측 보존+확인 연결 |
| P3-5 | **stance 불일치 화법** | I 질문의 Filter | 고객 인지·의사 Evidence 없음 + Pool에 propose_change stance 화법만 존재 | 화법 이식 거부 또는 명시적 조건부화 ("의향을 밝히신 경우") — GC-20 단일 방향 축소의 재검증 |
| P3-6 | **과다 Pack (상한 근거 실측)** | P-6 — F-006/F-002 재발 조건 | 관련도 낮은 K-item을 정상 Pack에 +4~6건 추가한 변형 실행 | 핵심 K-item 사용 유지 여부·무관 항목의 over-application 발생 여부 관찰 (Gate 아님 — 상한 결정 재료) |
| P3-7 | **Freshness 미달 수치** | Gate 4 | as_of가 오래된 금리/수익률 항목(time_sensitivity=volatile)이 선택된 Pack | 수치 인용 시 기준일 병기 + 실행 전 재확인 항목화, 확정 비교 없음 |
| P3-8 | **순수 0건 NOT_FOUND (자동 Gap 골격)** | Flow [7]의 deterministic 골격 | Need는 형식적으로 생성됐으나 Registry 응답 0건 — KG가 기계 골격(implication/forbidden은 최소 문구)만으로 전달 | 최소 골격 KG로도 GC-23 수준의 Epistemic 유지가 되는지 — Human 문구 개입의 필요 수준 측정 |

검증 순서 제안: P3-2·P3-8(Gap 축) → P3-1·P3-3(오염·Authority 축) → P3-5·P3-4 → P3-6·P3-7(운영 파라미터 축). P3-2가 전체 설계의 핵심 가설("Gap의 명시가 Gap 메움 방지의 유효 수단")을 직접 검증하므로 최우선.

---

## 부록 — 목업 v1 / 운영형 구분 요약 (요청 §5)

| 축 | Selection v1 (지금) | 운영형 (향후) |
|---|---|---|
| Need 생성 | Human/A — 형식화된 K-REQ (⑤-1) | LLM 초안 + deterministic 검증 |
| Routing/Gate | deterministic — md 필드 기반 규칙 | 동일 (인덱스화) |
| Retrieval | 수동 + topics/situation_tags 규칙 검색 | BM25+Vector Hybrid, Metadata Filtering, Rerank |
| Selection·Relevance 작성 | Human/A (기존 Freeze 작업의 형식화) | Rerank + 원문 발췌 보존 (LLM 재작성 금지 유지) |
| Gap | deterministic 골격 + Human 문구 | deterministic 생성, Human 감사 |
| Product | Registry 재료 + Case Pool 수동 확정 | 실제 Product DB + eligibility filter |
| 저장 | md Registry (파싱 규율 강화) | 구조화 스토어 + Knowledge Update 파이프라인 |
| 불변 사항 | Two-stage 경계 · Authority-by-purpose gate · Gap 1급 객체 · supply 분리 · deterministic validator — **v1과 운영형이 공유하는 뼈대** | 동일 |

과설계 방지 원칙: v1에서 만들지 않는 것 — Vector DB / 자동 Rerank / purpose 온톨로지 고정 / 항목별 permitted_use 필드 전면 도입 / LLM Need 생성 / 2-call Runtime 분리. 이들은 전부 P3 관찰 이후의 Human 결정 대상이다.

> 본 문서 작성 세션은 여기서 정지한다 (Human Gate). Runtime·Prompt·Golden·Registry 무변경.
