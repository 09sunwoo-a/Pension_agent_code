# Input·Brief 개편 작업 계획 (Customer Evidence Pack + Employee Brief Target Concept)

- Status: **PLAN CONFIRMED — 전체 계획 확정 · 착수 대기** (2026-08-31 Human 확정; 착수는 별도 지시로 시작)
- 승계 세션용 자족 요약본: `design/HANDOFF_INPUT_BRIEF_PLAN.md` (저장소 없이 읽어도 이해되도록 쓴 인수인계 문서)
- 착수 조건: **Human의 명시적 착수 지시가 있을 때까지 어떤 Step도 시작하지 않는다.** 이 문서 작성 자체는 Human 지시로 수행되었다.
- 이 문서의 목적: 다른 Agent Session이 이 계획을 이어받아 수행할 수 있도록 (1) 합의된 Target Concept, (2) 이번 대화에서 이미 내려진 설계 판단, (3) 작업 순서와 Human Gate, (4) 후속 로드맵을 기록한다.
- Target Concept 은 **Working Hypothesis** 다 — 확정 스펙이 아니며, Step 1~2 의 증거 작업과 Step 3 Human Gate 에서 다듬는다.
- 선행 문서: `README.md` → `00_Core_Concept_Design.md` → `AGENTS.md`(§20) → `golden/HUMAN_DECISIONS.md` → `golden/P1_BATCH2_SUMMARY.md` → 본 문서.

---

## 0. 출발점 — 저장소 현재 상태 (2026-08-31, main 기준)

- Golden 17 Case (P0 8 + P1 9) 전부 1차 사이클(Freeze → Run → Eval) 완료. FAIL 0 · Stop Condition 0.
- REV-001 (Judgment-first 출력, Knowledge Usage Context, C2 validator) 구현·검증 완료: Action/Change Bias 강한 재현 0/17.
- 잔여 실패는 "표현·세부 수준"으로 수렴: F-006 잔여(Knowledge 항목 내부 세부 조건 탈락) 5/9, F-004(확인 축 누락) 4/9, F-001 "방치" 어휘 2/9. `cases/FAILURE_MAP.md` 참조.
- Human이 정한 다음 방향: **INPUT 구체화 / Brief 구체화 → 그 방향의 탐색 → Agent 로직 고도화.** 이 계획은 그 실행안이다.
- 참고: 과거 병렬 세션의 `design/CUSTOMER_CONTEXT_INVENTORY_DRAFT.md` 는 미승인 상태로 main 에서 제거되었다(커밋 937235c). 내용(P0 9개 Case 역추적)은 원자료로 유효하며 `git show 1de4ea8:design/CUSTOMER_CONTEXT_INVENTORY_DRAFT.md` 로 회수한다.

---

## 1. Target Concept (Working Hypothesis)

### 1.1 중심 원칙 (Human 기획)

> Agent에게 "고객을 설명한 데이터(판단 완료형 라벨)"를 주지 말고, "고객을 스스로 재구성할 수 있는 Evidence"를 시간·맥락·확실성 정보와 함께 준다. **계산은 시스템이 하고, 해석과 판단은 Agent가 한다.**

### 1.2 Input — Customer Evidence Pack

핵심 4덩어리: **Snapshot + Event Timeline + Wider Context + Evidence Metadata.**

설계 원칙 8개 (Human 기획 원문 기준):

1. **Snapshot**: 현재 상태를 한눈에. 금액·비중·기간 등 객관 계산값은 미리 계산해 제공하되 **의미 판단은 하지 않는다** ("현금성 비중 100%" ✅ / "미운용 방치고객 = Y" ❌).
2. **Event Timeline**: Snapshot 보다 중요. "왜 지금 이런 상태가 됐는가"를 재구성할 수 있도록 최근 주요 Event(입금·사유, 매매, 운용지시, 만기, 이전, 성향분석)를 시간순으로 제공.
3. **Wider Customer Context**: IRP 밖 정보(전체 금융자산, 타계좌 투자행동, 연금저축·ISA·만기예정)는 별도 맥락으로 분리 제공. Cross-context 해석은 허용하되 의사 승격("타계좌 투자 활발 → IRP도 공격 투자 원함")은 금지.
4. **Digital / Behavioral Signals**: 조회·클릭·메뉴 진입은 관심/행동의 Evidence이며 **고객 의사를 직접 의미하지 않음**을 개념적으로 명시 ("ETF 5회 조회 → 관심 가능성"까지만).
5. **모든 데이터에 as_of**: `value + as_of/date` 가 기본. 발화는 라벨이 아니라 일자 + 원문("2026-02-20 상담 시: 'IRP는 예금 중심으로 하고 싶다'").
6. **Fact / Calculated / Signal 3분류**: 최소한의 Evidence Metadata. 복잡한 Provenance Framework는 만들지 않는다. "ETF 니즈 고객·이탈위험 고객·리밸런싱 필요 고객" 같은 판단 완료형 라벨은 Input에서 제거.
7. **변화량**: 잔액·비중·투자행동·현금성 등 변화가 의미 있는 항목에는 현재/1개월 전/3개월 전/증감 제공.
8. **Missing 명시**: "단기 자금사용계획: 데이터 없음"처럼 없는 것도 명시적으로 — Agent가 "확인해야 한다"를 도출할 수 있도록. 단, **모든 고객에게 동일한 고정 슬롯(스키마)** 으로 제공한다 (Case별 선택 제공은 확인 축 힌트가 되므로 금지).

Evidence Pack 9개 섹션 (의미 구조, JSON Schema 아님):

```
1. Customer / Pension Profile   연령, 투자성향(+분석일), 가입일, 연금단계
2. IRP Current Snapshot         잔액 / 상품 / 비중 / 수익률 / 현금성 / 만기
3. IRP Event Timeline           입금(사유) / 퇴직급여 / 만기 / 매수 / 매도 / 운용지시 / 이전
4. Whole-Asset Context          전체 금융자산 / 투자자산 / 타 연금 / 유동성
5. Investment Activity          IRP 및 타계좌 최근 투자행동
6. Upcoming Events              IRP 만기 / ISA 만기 / 주요 예정 Event
7. Digital Signals              조회 / 검색 / 비교 / 메뉴 진입
8. Known Customer Intent        있을 때만 — 과거 상담/확인된 의사 (일자 + 원문)
9. Existing Bank Signals        캠페인 / Badge / Target — 고객 상태 판단 근거와 분리(Trigger Provenance)
```

### 1.3 판단 파이프라인

```
Customer Evidence Pack
  ↓
① Customer State Interpretation   "어떤 상황이고 왜 이렇게 됐나" — Fact/추론 구분 명시
  ↓
② Management Judgment (방향 중립)  "지금 무엇이 필요한가" — REV-001 단계 재사용
  ↓                                (개입 필요/확인 우선/현상유지 가능/정보안내/고객결정 지원/실행 불가)
③ 핵심 관리 포인트 + 관리전략       판정된 기회를 전략으로 (조건부 분기 포함)
  ↓
④ Required Confirmation           직원이 고객에게 물어야 할 것
  ↓
⑤ Employee Brief (5-섹션 출력)
```

### 1.4 Output — Employee Brief 5-섹션

Brief 는 "판단 요약"이 아니라 **직원의 업무 흐름을 미러링한 Recommendation Brief** 다. 직원용 도구이며 고객 직접 제공 문서가 아니다.

| # | 섹션 | 직원의 질문 | 내용 |
|---|---|---|---|
| 1 | 고객 상황 | "무슨 상황이야?" | 핵심만 간결하게. 절제된 해석 허용("운용 여부를 결정하지 않은 상태") — 단정 어휘("방치") 금지. 관리 포인트와 연결되는 사실만 선택 |
| 2 | 핵심 관리 포인트 | "오늘 왜 이 고객을 만나? 뭘 먼저 물어?" | "지금 무엇을 관리하는 것이 중요한가"에 커밋. **Required Confirmation 은 독립 섹션이 아니라 이 아래에 '먼저 확인하세요'로 종속** — 확인은 관리 포인트 실행의 첫 행동 |
| 3 | 추천 운용 방향 | "뭘 제안해?" | 연령·자금성격·예상기간·성향·자산구성·의사 고려. 필요 시 원리금보장/TDF/펀드/디폴트옵션/추천상품 등 **상품 수준까지 연결** — 단, 확인 미완 사항은 조건부("장기운용 의사가 확인되면 →"). HD-1(최종 계산값 제외)·HD-2(성향→등급 Hard Constraint) 작동 지점 |
| 4 | 상담 Point | "어떤 순서로, 뭐라고 말해?" | 이 고객 전용으로 **생성**: 접근 논리·설명 순서·실제 화법. D9(용어 치환·단정 회피) 영역 |
| 5 | 관련 TIP & GUIDE | "실무적으로 뭘 챙겨?" | 행내 자료에서 **연결(retrieval)**: Hot Tip·확인 순서·반론 대응·관련 화면·업무 절차·후속관리·제도 유의사항. HD-3(Hot Tip=Operational Knowledge)·D12 영역. 출처·권위 수준 명시 필수 |

성격 요약: 입장을 가진 문서("~가 필요합니다"라고 커밋)이되, 불확실성은 조건 분기로 유지(커밋 ≠ 조기 수렴, F-010 주의). 내부 판단 구조(Judgment 6유형 라벨 등)는 문서에 노출하지 않는다.

### 1.5 Business 관점 원칙 (Human 기획 — Step 3에서 HD로 명문화 예정)

> **은행의 Business Objective 가 고객의 관리 필요성을 만들어내서는 안 된다. 하지만 고객에게 유효한 관리기회가 존재한다면, 허용 가능한 범위 안에서 그 기회를 은행의 관리행동(운용 활성화·장기 운용 연결·만기 재운용·추가납입·리밸런싱·이탈방어·연금관계 지속·후속관리)으로 적극 연결해야 한다.**

평가 가능한 경계 = **근거 출처 테스트**: 관리 포인트의 근거가 Customer Fact/Event에서 출발하면 유효한 기회, KPI·캠페인·타겟 리스트에서 출발하면 필요성 창출(F-009, Critical Mistake 유지). D10 원칙은 유지·정밀화되는 것이지 폐기가 아니다.

---

## 2. 이번 대화에서 이미 내려진 설계 판단

다른 세션은 아래를 재논의하지 않는다 (변경은 Human 승인 필요).

1. **F-005 재발 방지 = 판단층/전달층 분리.** 내부 판단은 REV-001 Management Judgment(방향 중립, "관리할 것 없음·유지·확인우선·불가"가 동등한 정답)를 그대로 재사용. "관리기회" 언어는 판단이 끝난 뒤의 **전달층(Brief)** 에서만 사용. "핵심 관리 포인트"는 넓게 정의: 확인 우선·유지+다음 관리 시점 예약·불가 안내+대안도 관리 포인트다.
2. **Required Confirmation 의 위치**: 파이프라인상 독립 단계지만, Brief 출력에서는 섹션 2에 종속("먼저 확인하세요"). 확인과 개입은 양자택일이 아니라 한 관리 포인트 안의 순서다.
3. **Missing 은 고정 슬롯**: Case별 선택 제공 금지 (확인 축 힌트 방지, C3 평가 보전).
4. **Calculated Fact 의 경계**: 비중·경과일·만기 D-n·DO 자동적용 예정일·개시요건 충족 여부 등 "계산"만 전처리. "미운용 상태로 추정" 같은 "판단"은 전처리 금지.
5. **Regression 방식**: 기존 Freeze case.md 불변(append-only). 대표 6~8개 Case에 `input_v2` 변환본(정보량 동일, 조직 형태만 변경)을 부록 추가해 재실행. **Counterfactual Pair(최소 GC-04↔05) 필수 포함** — 기회 중심 Brief가 Action Bias를 재도입했는지의 감지선. Wider Context·Signals 등 신규 섹션 검증은 신규 P2 Case 담당.
6. **REV-002 와 Knowledge Key Conditions(REV-003 후보)는 분리**: 변수 2개 동시 변경 시 Regression 귀속 불가. REV-002 결과를 본 뒤 REV-003 범위 결정 (전처리가 F-006 일부를 흡수했을 수 있음).
7. **Excel 활용 범위**: `references/planning/` 두 파일은 README Allowed Uses(필드·값 범위 참고, Synthetic Input 설계)로만. Badge/Target/Action 은 Input·정답 근거 금지 — 단 형태는 섹션 9(Bank Signals) 설계 참고 가능.
8. 이 개편은 **REV-002** 로 기존 사이클(`Failure Evidence → Human Gate → Revision → Regression → FAILURE_MAP`)에 편입한다. Runtime 변경은 Semantic Change 이므로 HD-5.1에 따라 Step 3 Human Gate 통과 전 구현 금지.

---

## 3. 작업 순서

### Step 1. 증거 수집 + 역추적 — Agent 자율, 문서만 산출

- 구 Inventory Draft 회수(`git show 1de4ea8:design/CUSTOMER_CONTEXT_INVENTORY_DRAFT.md`) → P1 9 Case(GC-02,05,07,08,09,11,13,15,17)의 case.md·RUN·EVAL 역추적을 더해 **17 Case 전수**로 확장: 판단에 실제 쓰인 Fact / Unknown→확인 필요 / 있었는데 미사용(F-003) / 오추론(F-001·002·009)
- 두 Excel에서 실제 필드명·값 범위 추출
- 기존 17개 RUN 의 Brief 를 5-섹션 관점에서 재독해: 섹션별 유·무, F-001/F-008 소실의 섹션 귀속
- Source Corpus 의 업무 화면·Hot Tip 목록 정리 (Brief 섹션 5의 공급 가능 재료 확인)

### Step 2. Spec 초안 3건 — Agent 자율, Draft 상태

1. `design/TARGET_CONCEPT.md` — §1 전체(파이프라인·관리기회 정의·Business 경계)를 증거와 함께 정식화. Draft
2. `design/EVIDENCE_PACK_SPEC.md` — 9개 섹션별 필드 후보 표: `필드 | 섹션 | Fact/Calculated/Signal | as_of | 변화량 | 근거 Case | Availability(?)` + Calculated Fact 산식 목록 + Missing 고정 슬롯 목록. **Availability 는 Human 답변 없이 확정 금지 — `?` 유지**
3. `design/EMPLOYEE_BRIEF_SPEC.md` — 5개 섹션별 필수/금지 요소, Judgment 결과별 변형(유지·확인우선·불가 Case 의 Brief 형태), 섹션별 평가 축·실패 모드

### Step 3. Human Gate — Human 결정 (유일한 확정 지점)

- Availability `?` 확정 (은행 데이터 현실)
- 필드·섹션 취사선택, Target Concept 수정·승인
- HD-6 갱신 여부 (Brief: Diagnostic → 직원용 Output 승격) · HD-7 신설 (Business 관점 원칙 §1.5) · 관리기회 정의 승인
- REV-002 구현 범위 승인

### Step 4. REV-002 구현 — Agent 자율 (Step 3 승인 범위 내)

- `prototype/runtime.py`: Evidence Pack 입력 구조 + 전처리(Calculated Fact) + Brief 5-섹션 출력 구조
- `prototype/REVISIONS.md` 에 REV-002 기록. C2 validator 등 기존 deterministic 검사 유지

### Step 5. Regression + 평가 — Agent 자율

- 대표 6~8 Case (Judgment 유형별 커버 + Counterfactual Pair 필수) `input_v2` 재실행 → 기존 RUN 과 비교 평가 (Builder=Gemma 4, Evaluator=Claude, §20 절차 그대로)
- 신규 실패 관찰(예: Wider Context→성향 재추정, Signal→의사 승격, Calculated Fact 무시 재계산) 시 F-011~ 등록, `cases/FAILURE_MAP.md` 갱신
- Batch Summary 작성 (`golden/REV002_REGRESSION.md` 등) → Human 보고

### Step 6. 결과 보고 후 다음 결정 — Human

- REV-003 (Knowledge Key Conditions) 여부·범위 / P2 Batch 3 설계 / Reusable Knowledge 착수 여부

---

## 4. 후속 로드맵 (이번 사이클 완료 이후)

각 단계는 앞 단계의 Failure Evidence 로 정당화될 때만 착수한다 (§20.8 원칙 유지).

1. **REV-003: Knowledge Key Conditions 구조화** — 증거 확보됨(F-006 잔여 5/9 + P0 RUN_002 5/8). 단 REV-002 Regression 결과를 먼저 보고 범위 결정.
2. **P2 Batch 3** — 신규 섹션(Wider Context·Signals·Upcoming Events) 검증용 Case + Coverage Gap(`GOLDEN_SET_DRAFT.md` §7: 시황 활용, ELB 청약, 결정세액 부족, 세액공제 미신청분 해지, 수수료 단독 이탈, GC-10 변형 순수 Pair). 신규 Case 는 처음부터 Evidence Pack 형식으로 작성.
3. **Reusable Knowledge → Retrieval** (§20.8 해금) — Brief 섹션 5(TIP & GUIDE)가 실수요처. 20개+ Case 의 K-item 사용 실적을 근거로 승격 정책 결정 후 Retrieval 구조 검토.
4. **실전화 준비** — Availability 확정된 Evidence Pack = 은행 시스템 인터페이스 명세의 전신; deterministic 레이어 확장(Signal→의사 승격 검출, 시한 계산 검증, Brief Hard Constraint 소실 검사); Case 30~40개 규모에서 자동 Evaluator·통계 평가 검토; 승격된 Brief 의 실제 직원/전문가 검증.

권장 순서: Regression 결과 확인 → REV-003 여부 즉시 결정 → P2 Batch 3. (Runtime 안정화 후 Case 확장이어야 신규 실패의 귀속이 깨끗함.)

---

## 5. 제약·주의 (승계 세션 필독)

- **착수 금지**: Human 의 명시적 지시 전에는 Step 1 도 시작하지 않는다.
- 기존 Freeze 된 Case·RUN·EVAL 은 소급 수정하지 않는다 (append-only).
- §20.8 보류 항목(Retrieval, Multi-Agent, 자동 Evaluator, 통계 평가 등)을 이 작업 중에 무단 도입하지 않는다.
- Runtime Semantic Change(새 Output Schema·입력 의미 변경)는 HD-5.1 에 따라 Human Gate 대상 — Step 3 이전에 runtime 코드를 변경하지 않는다.
- 확정된 Human Decision(`golden/HUMAN_DECISIONS.md` HD-1~6)은 재질문하지 않는다.
- Builder=Gemma 4 / Evaluator=Claude 역할 분리(§17, §20) 유지.
