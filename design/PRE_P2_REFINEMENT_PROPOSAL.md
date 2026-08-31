# Pre-P2 Input / Brief Refinement — Design Proposal

- Status: **INPUT ARCHITECTURE — HUMAN DIRECTION APPROVED (HD-PRE-P2-INPUT, 2026-08-31).** 9-Block 구조·3-Layer 방향 승인 + 수정사항 반영 완료(§7 결정 기록). **Employee Brief(§4) = Human Brief Design Direction 반영 완료(2026-08-31) — Target Design 확정, 구현은 별도 게이트.** Runtime/Parser/Canonical Schema 구현·P2 Case 작성·Freeze·RUN/EVAL은 여전히 금지(Brief Gate 확정 이후).
- 목적: REV-002의 검증된 Core Reasoning Architecture(판단층/전달층 분리·Judgment-first·Candidate Pool·Evidence Provenance)는 변경하지 않는다. **Customer Context를 더 풍부하고 안정적으로 재구성할 수 있도록 Input의 내용·표현 구조를 개선**하고, 그 변화가 Employee Brief에 어떻게 전달되어야 하는지 재설계한다.
- 불변 조건: 기존 Frozen Case·RUN/EVAL·REV-002 종료 기록 수정 없음.

---

## 1. 문제의식과 설계 원칙 (Human 지시 5항 + REV-002 실증)

| # | 원칙 | REV-002 실증 근거 |
|---|---|---|
| 1 | CRM 데이터 품질은 현재 높지 않음(향후 개선 예정) — **고객 맥락 파악을 CRM에 과의존하지 않게** 한다 | 8 Case 중 7개에서 CRM 메모가 사실상 유일한 의도 단서였고, GC-14에서 CRM 진술의 Brief 승격 발생(선택 Regression으로 표현은 교정했으나 **구조적 의존은 그대로**) |
| 2 | CRM 제거하지 않되 `Supplementary Human-authored Context`로 재위치 | 현행 ⑧이 "Customer Interaction"이라는 이름으로 사실상 Intent 섹션 역할 — 이름·위치·서술이 중심 Input처럼 읽힘 |
| 3 | CRM은 authoritative system fact 아님 — Freshness·작성주체·타 Evidence 정합성과 함께 해석 | 결정 2-8로 verbatim 비보장은 반영됐으나 작성주체 필드와 관련 Evidence 병렬 제공은 미구현 |
| 4 | System-observable Context 강화: 최근 변화·자금 흐름·실제 Event·행동 Sequence·Wider Context | 변화량은 "1개월 고유계정대 증감" 1개뿐; Digital은 횟수만(순서 없음); 자금 흐름과 현재 잔액의 연결은 GC-11 사유 분해가 유일 사례 |
| 5 | Input은 **What happened / What changed까지** — What it means는 Agent 판단 (판단 완료형 Label 금지) | REV-002 기존 원칙 유지·강화. "방치·미운용·대기자금" 등 의미 판단 전처리 금지 지속 |

## 2. Target Input 구조 — 9-Block 제안

현행 8-섹션 → 9-Block 재편. 핵심 변화: **③ Recent Changes & Money Flow 신설**(변화 축 승격), **⑥ Sequence 도입**, **⑨ CRM 재위치**(마지막 블록·보조 지위), 한도 합산 개념의 ⑦ 이동, DO Rule Clock의 ⑧ 이동.

### ① Customer & Retirement Lifecycle (현행 ① 재편)

| 항목 | 내용 |
|---|---|
| 목적 | 이 고객이 은퇴 생애주기 어디에 있는가 — 모든 판단의 기저 좌표 |
| 유지 (AS-IS) | 기준일·연령(생년월)·투자성향+분석일+유효·**직전 성향 이력**·IRP/제도 가입일·계좌유형·퇴직급여 포함(금액·입금연도)·연금개시 관련 일체(요건 R·개시·지급설계·지급정보)·재직/퇴직·스타뱅킹 이용 |
| 이동 | 없음 (기존 ①이 근간) |
| 추가 후보 | **퇴직일**(재직→퇴직 전환 시점 — 현행은 여부만), **퇴직급여 유입 여부/시점의 명시 필드**(현행은 계좌유형 속에 묻힘) |
| 삭제·통합 | 없음 |
| Type | F (개시요건만 R) |
| Av | 전부 O (HD-8·Step 3 확정 범위) / 퇴직일 상세 **?** |
| 판단 도움 | 생애주기 좌표가 있어야 만기 길이·수령 설계·TDF 빈티지 판단이 성립 (GC-15·17 실증) |
| 사전해석 금지 | 연령→성향 추정 금지("나이만으로 안정형 결정 금지"), 성향 변화→운용 변경 의사 추정 금지 |
| 확보 난이도 | 낮음. 퇴직일의 시스템 존재 여부만 미확정 |

### ② Current IRP Snapshot (현행 ② 슬림화)

| 항목 | 내용 |
|---|---|
| 목적 | 지금 계좌가 어떤 상태인가 — 정적 스냅샷만 담당 (변화는 ③으로) |
| 유지 | 전체 평가금액·자산유형별 금액/비중(A)·보유상품 배열(상품명·유형·발행기관·매입원금·평가금액·PF비중·약정/만기일·금리+as_of·**상품 수익률 vs 고객보유수익률 구분**·위험등급·실물이전 가능)·현금성 금액/비중·계좌 1년 수익률·DO 등록 정보+구성·입금예정상품·자동이체·`irp_personal_contribution_ytd` |
| 이동 (OUT) | `pension_account_contribution_limit_remaining`·`pension_tax_credit_limit_remaining` → **⑦** (합산 연금계좌 개념 — 계좌 밖 Context가 맞음) / DO 적용 예상 기준일(R) → **⑧** (Decision Horizon의 Rule Clock) / 1개월 증감 → **③** |
| 추가 후보 | 없음 (슬림화가 목적) |
| 삭제·통합 | 없음 (Step 3 삭제 완료 상태 유지) |
| Type | F + A(비중) |
| Av | 전부 O |
| 판단 도움 | 상태와 변화를 분리하면 "상태만 보고 원인 채우기"(P0 관찰 1의 기제)가 구조적으로 줄어듦 |
| 사전해석 금지 | 현금성 존재→미운용, 성향-구성 불일치→관리 필요 자동 판정 금지 (기존 유지) |
| 확보 난이도 | 낮음 |

### ③ Recent Changes & Money Flow (신설 — 이번 Refinement의 핵심)

| 항목 | 내용 |
|---|---|
| 목적 | **What changed** — 왜 지금 이 상태가 됐는지를 Agent가 재구성할 원재료. Why-now의 시스템 관찰 근거 |
| 유지 (이동 IN) | 최근 1개월 고유계정대 증감(현행 ⑤에서 이동) |
| 추가 후보 | **Window 기반 변화 구조**(Decision 2 반영 — 특정 기간에 Schema를 강결합하지 않음): 기본 `30d` 우선 활용, `90d`는 확보 가능 시 추가, 향후 다른 window 확장 가능. 대상: 평가금액 변화(전체·자산유형별 금액/비중, A)·현금성자산 증감 / **최근 자금 발생 원천 요약**(입금·만기상환·매도대금의 사유별 합계 — ④ Event의 집계 뷰) / **잔액-Flow의 산술적 reconciliation**(Decision 1-1 — 포함 확정): 허용 예 "현재 현금성 3,000만 / 8-10 만기상환 3,000만 / **금액 일치**"까지. 금지 예: "만기 후 **미운용된** 자금", "**대기성** 자금", "운용되지 않고 **남아 있는** 자금" |
| 삭제·통합 | — (신설) |
| Type | A (전부 산술 파생 — Canonical의 과거 스냅샷·Event에서 계산) |
| Av | 30d 변화 O 추정([9C] 실존) / **90d 변화·과거 시점 잔액 스냅샷 `?` 유지**(Decision 7 — 임의 확정 금지) / 잔액-Flow reconciliation은 파생이므로 — |
| 판단 도움 | GC-07("매수 후 평가 상승으로 초과" 추론)·GC-11(사유 분해)이 보여준 "변화를 알면 원인 추론이 정확해짐"의 일반화. Excel [9C]의 ±1.7억 급증 필드가 원형 |
| 사전해석 금지 | **"방치·미운용·대기자금" 등 의미 판단 전처리 금지** (명시 지시). 잔액-Flow 연결은 금액 일치라는 산술 사실까지만 — "이 현금은 지급 대기금이다" 단정 금지 |
| 확보 난이도 | **중** — 과거 시점 잔액 스냅샷(1M/3M 전) 보존 여부가 관건. 미확정 시 증감액 필드만으로 축소 운영 가능 |

### ④ Event Timeline (현행 ③ 유지)

| 항목 | 내용 |
|---|---|
| 목적 | What happened — 원천 시스템에 실존하는 사건의 시간순 기록 |
| 유지 | 입금 Event(일자·금액·**사유 코드**)·매수/매도 Transaction·계약이전 Event·투자성향 분석 Event |
| 이동 | 없음 |
| 추가 후보 | **연금개시/지급설계 등록 Event**(개시 이력이 있는 고객), **DO 등록/변경 Event**(등록일은 현행 ②에 있으나 Event로도 — 원천 실존 시) |
| 삭제·통합 | 없음. **현재 값으로 과거 상태를 추정해 Event화 금지** 원칙 유지(결정 2-3) |
| Type | F |
| Av | O (추가 후보 2건은 ?) |
| 판단 도움 | ③의 집계가 "얼마나"라면 ④는 "언제 무엇이" — 두 층이 있어야 시간맥락 오류가 줄어듦(REV-002 실증) |
| 사전해석 금지 | Event 나열에 해석 문구 부착 금지 (사유 코드는 원천 코드 그대로) |
| 확보 난이도 | 낮음 |

### ⑤ Investment Behavior (현행 ⑤ 재편)

| 항목 | 내용 |
|---|---|
| 목적 | 이 고객의 운용 행동 이력과 경험 — 성향 Label이 아닌 행동 사실 |
| 유지 | IRP 최근 매매일+내용·최근 1년 매매횟수·ETF/수익증권 현재보유+과거 이력(마지막 거래일 포함)·퇴직연금펀드/공모펀드 이력(폐기계좌 포함) |
| 이동 (OUT) | 1개월 증감 → ③ |
| 추가 후보 | **최근 활동 변화**(기간별 거래횟수 비교: 최근 3M vs 직전 3M — A), **기간별 거래횟수 세분화**(1M/3M/12M) |
| 삭제·통합 | 없음 (Cross-account 행동 제외는 Step 3 결정 유지) |
| Type | F + A(활동 변화) |
| Av | 기존 O / 기간별 세분화·비교 **?** (원천 거래내역에서 파생 가능하면 —) |
| 판단 도움 | "경험 있음" 단독은 해석 왜곡(GC-04 마지막 거래일의 교훈) — 활동의 시간 구조가 있어야 "과거 경험 vs 현재 행동 변화" 구분 가능 |
| 사전해석 금지 | **"적극투자 고객" 등 성향 Label 변환 금지** (명시 지시). 활동 증가→의사 변경 단정 금지 |
| 확보 난이도 | 낮음~중 (파생 계산 문제) |

### ⑥ Digital Behavior & Sequence (현행 ⑦ 확장)

| 항목 | 내용 |
|---|---|
| 목적 | 관심·탐색의 행동 신호 — 가능하면 **시간순 Sequence**로, 실행 여부까지 |
| 유지 | 화면 조회(자산현황/ETF/TDF/연금수령 등)·상품/시세 조회·이전 메뉴 진입·배너/세미나 |
| 이동 | 없음 |
| 추가 후보 | **운용지시 화면 진입**(조회와 실행 화면의 구분), **실제 실행 여부**(진입 후 미실행 — 강한 맥락 신호), **시간순 행동 Sequence**(가능한 경우: "mm-dd 수익률 조회 → mm-dd 타사 비교 → mm-dd 이전 메뉴 진입(미실행)") |
| 삭제·통합 | 없음 |
| Type | S (전부) — Sequence도 S |
| Av | 횟수형 O(HD-8) / **Sequence·실행 여부 ?** — 로그 타임스탬프·행동 구분 체계 필요 |
| 판단 도움 | 단발 횟수보다 Sequence가 훨씬 강한 재구성 재료 — "조회만 8회"와 "조회→비교→이전 메뉴→미실행"은 다른 상황. 단 해석은 Agent 몫 |
| 사전해석 금지 | **Digital Behavior는 Intent가 아니라 Signal** — Sequence가 강해도 승격 금지(Critical Boundary 유지). "이탈 준비 중" 류 전처리 라벨 금지 |
| 확보 난이도 | **중~높음, Av `?` 유지**(Decision 3·7) — P2 설계는 Sequence 제공 Case를 사용할 수 있게 하되, 실데이터에서 Sequence 확보 불가 시 **횟수/행동 Event 형태로 degraded 가능해야 함**(양 버전 설계 원칙 승인) |

### ⑦ Wider Financial Context (현행 ④ 확장)

| 항목 | 내용 |
|---|---|
| 목적 | 계좌 밖 재무 좌표 — IRP 단독 판단의 오류를 막는 맥락 |
| 유지 | 총 금융자산·구성·타사 연금저축(기관·가입일·적립금·납입액·공시이율·해지환급 관련·개시 여부)·ISA(기관·가입일·만기일·예상금액·의무기간)·총급여/소득구간 |
| 이동 (IN) | `pension_account_contribution_limit_remaining`(R)·`pension_tax_credit_limit_remaining`(R) ← 현행 ② (합산 연금계좌 개념 — HD-8 6-2 개념 분리 문구 유지) / **당해년도 연금 납입 Context**(IRP ytd는 ②에 두되, 연금저축 납입액과의 병렬 뷰를 여기에) |
| 추가 후보 | 없음 (Peer·식별 메타·주택·타기관 납입현황 제외는 기존 결정 유지) |
| 삭제·통합 | 없음 |
| Type | F + R(한도 2종) |
| Av | 전부 O |
| 판단 도움 | GC-13/15 실증 + P2 GC-18의 본검증 대상. 한도의 ⑦ 배치는 "이 IRP 하나의 한도가 아니다"라는 개념을 **위치로도** 표현 |
| 사전해석 금지 | 특정 자금의 목적 사전 해석 금지("ISA 만기자금은 IRP 전환 후보" 류 문구 금지 — GC-18 재검토 관점), 타 계좌 행동→IRP 의사 승격 금지 |
| 확보 난이도 | 낮음 |

### ⑧ Upcoming Decision Horizon (현행 ⑥ 확장)

| 항목 | 내용 |
|---|---|
| 목적 | 앞으로 결정이 필요해지는 시점들 — 시한 좌표 (F-003 대책 계승) |
| 유지 | 상품 만기 목록(부차 포함 전부·D-n)·ISA 만기(+60일 시한)·연금 지급 예정·자동이체 예정 |
| 이동 (IN) | **DO 적용 예상 기준일(Rule Clock, R)** ← 현행 ② — "예정된 제도 시계"는 Horizon이 제자리 |
| 추가 후보 | **기타 실제 예정 Event**(성향분석 유효기간 만료 예정, 세액공제 연말 시한 등 — 원천 실존·규칙 파생 가능한 것만). ~~시한별 "결정 성격 한 줄"~~ — **Decision 1-2로 제거**: Input에는 상품명·만기일·D-n·Rule Clock·실제 예정 Event 등 객관적 시점 정보까지만 제공하며, 해당 Event가 어떤 관리 Decision을 요구하는지는 Agent가 판단한다 |
| 삭제·통합 | 없음 |
| Type | F + A(D-n) + R(Rule Clock) |
| Av | O (기타 예정 Event 일부 ?) |
| 판단 도움 | GC-09 만기 누락 해소·GC-22 우선순위 Case의 기반. Rule Clock의 이동으로 "상태(②)"와 "다가오는 결정(⑧)"이 분리 |
| 사전해석 금지 | 시한→행동 필요 단정 금지("만기 도래=재예치 권유 대상" 라벨 금지). Rule Clock은 예상 기준일까지만(실제 적용 여부 미확인 유지 — 결정 2-4) |
| 확보 난이도 | 낮음 |

### ⑨ Supplementary Human-authored Context (현행 ⑧ 재위치·재정의)

| 항목 | 내용 |
|---|---|
| 목적 | 사람이 작성한 보조 맥락 — **중심 Input이 아니다.** 시스템 Evidence로 재구성한 상황에 대한 보조 참고 |
| 유지 | CRM 메모(작성일·채널·내용·source) |
| 이동 | 블록 위치를 마지막(⑨)으로 — 직렬화 순서 자체가 "보조" 지위를 표현 |
| 추가 후보 | **작성 경과일**(A — Freshness를 숫자로), **작성 주체**(창구 직원/상담센터/캠페인 후속 등 — 맥락 품질 단서), **관련 Evidence 병렬 제공**: 메모 주제와 관련된 시스템 Evidence의 E-ID를 함께 표기(예: "메모 주제 관련: E012 성향 분석 Event, E019 TDF 조회") — **corroboration/충돌의 기계 판정은 하지 않고** 재료만 병렬 |
| 삭제·통합 | 없음 (CRM 제거 금지 — 명시 지시) |
| Type | CRM (+A 경과일) |
| Av | 메모·작성일·채널 O / **작성 주체 ?** |
| 판단 도움 | GC-20(오래된 메모 vs 최근 신호)의 기반. 경과일 숫자화로 Freshness 판단이 산술 근거를 가짐 |
| 사전해석 금지 | 메모 내용→현재 의도 Ground Truth 승격 금지(유지). **정합성·충돌의 기계 판정 금지**(명시 지시) — 판정은 Agent 몫. 명시 의사/부수 언급 사전 분류 금지(유지) |
| 확보 난이도 | 낮음 (작성 주체만 ?) |

### 이동·신설 요약 (현행 8-섹션 → 9-Block)

```
현행 ① Profile            → ① Lifecycle (+퇴직일·퇴직급여 유입 명시)
현행 ② Snapshot           → ② Snapshot (슬림) — 한도 2종→⑦, DO Clock→⑧, 증감→③
현행 ③ Timeline           → ④ Event Timeline (+개시/DO 등록 Event 후보)
현행 ④ Whole-Asset        → ⑦ Wider Financial Context (+한도 2종 IN)
현행 ⑤ Activity           → ⑤ Investment Behavior (+활동 변화) — 증감→③
현행 ⑥ Upcoming           → ⑧ Upcoming Decision Horizon (+DO Rule Clock IN)
현행 ⑦ Digital Signals    → ⑥ Digital Behavior & Sequence (+Sequence·실행 여부)
현행 ⑧ CRM Memo           → ⑨ Supplementary Human-authored Context (지위 재정의)
(신설)                    → ③ Recent Changes & Money Flow
```

블록 순서의 의도: **시스템 관찰(①~⑧) 전체를 먼저, 사람 작성 맥락(⑨)을 마지막에** — CRM 과의존을 직렬화 순서 수준에서 구조적으로 낮춘다.

## 3. 표현 구조 — Canonical Evidence Object 3-Layer 설계 (구현 보류)

**AS-IS 문제**: `input_v2.md` = Markdown bullet(사람 작성) + machine JSON(파생 계산용 원천값 **중복 기입**). 같은 사실이 두 곳에 적혀 불일치 위험이 있고, Case 작성 비용이 이중이며, 렌더링 정책(순서·주석)이 Case 파일에 박제된다.

**TO-BE — 승인된 Target Architecture (Decision 4)**:

```
Raw / Source Data
  ↓ (향후 실데이터: Input Adapter만 교체)
Layer 1  Canonical Evidence Object  (Case당 단일 구조화 파일 — 유일한 사실 원천)
         item = { id(Stable), block(①~⑨), evidence_type, source_type,
                  field, value, as_of, unit? }
         사람(Case 작성자/향후 시스템)은 이것만 작성한다. 서술문 없음.
  ↓ deterministic
Layer 2  Deterministic Derived Context  (전처리 — Canonical만 입력)
         비중·D-n·경과일·window 변화(30d/90d/…)·Rule Clock·잔액-Flow reconciliation
         전부 rule_source/rule_as_of/적용 Rule ID 추적. 의미 판단 금지.
  ↓ deterministic
Layer 3  LLM-friendly 9-Block Rendering
         Stable E-ID 표기·블록 순서·경계 주석(⑥⑨)·NULL/0/해당없음·CRM 관련 Evidence 병렬 표기
  ↓
Agent Reasoning
```

**확정 사항 (Decision 4-1 ~ 4-4)**:
- **적용 시점**: P2 신규 Case부터. **기존 Frozen input_v2·RUN·EVAL은 절대 변환·수정하지 않는다.**
- **Evidence ID = Canonical Stable ID** — 렌더 시점 임시 부여가 아니라 Canonical Object의 고정 ID. 렌더링 순서가 바뀌어도 Evidence Provenance가 깨지지 않는다.
- **Canonical 파일 형식 = JSON 우선안** (Runtime 연동·Schema Validation·stdlib 구현·향후 Source Adapter 연결 용이). 현 단계 구현 금지.
- **Evidence Type과 Source Type 분리** — epistemic 성격과 출처 성격을 하나의 type에 혼합하지 않는다:
  - `evidence_type`: `fact` / `arithmetic_derived` / `rule_derived` / `signal`
  - `source_type`: `account_system` / `transaction` / `digital_behavior` / `crm` / `external_account` / `rule_engine` / …
  - 이에 따라 §2의 표기 중 "CRM"은 evidence_type이 아니라 **source_type=crm**이다. ⑨의 메모 항목은 evidence_type=`fact`(작성됐다는 사실·작성일) + source_type=`crm`으로 표현되며, 내용의 의미 해석은 Agent 몫. 목적: 향후 human-authored source가 늘어도(직원 메모 외) 축이 오염되지 않음.
- 효과: 단일 원천(이중 기입 제거) / deterministic 계산과 semantic reasoning 분리 / 실데이터 연동 시 Input Adapter만 교체.

## 4. Employee Brief Target Design — Human Design Direction 반영 (2026-08-31)

> **지위**: 이 절은 Human이 별도 Brief Design Prompt로 전달한 Direction을 정리한 **Target Brief Design**이다. 구 §4의 5개 후보 초안(S1 2단 구조·S2 why_now 노출·S3 alternatives_not_taken 중심·S4 질문형+설명형·S5 실행 단위)은 이 Direction으로 **대체**된다. REV-002의 5-Section 구조 자체는 유지하되 각 Section의 역할과 최종 Output 수준을 재정의한다. **Brief Schema/Prompt/Validator/Runtime/P2 Case는 아직 변경하지 않는다** — 구현은 별도 게이트. 구현 승인 시 `EMPLOYEE_BRIEF_SPEC.md`를 이 Target으로 개정한다.

### 4.0 Brief 전체 목적

Employee Brief는 모델의 판단·근거를 옮겨놓은 분석 리포트가 아니라, 직원이 **다시 조립할 필요 없이** 쓸 수 있는 **직원용 Decision & Action Brief**다. 직원이 Brief만 보고 — 무엇을 관리할지 / 어떤 방향을 제안할지 / 실제 어떤 상품을 보여줄지 / 고객에게 어떻게 말할지 / 이후 어디에서 실행할지 — 를 별도로 재구성하지 않아야 한다.

```
S1 고객 상황            → 지금 이 고객에게 어떤 상황과 변화가 있는가
S2 핵심 관리 포인트      → 이번 접점에서 무엇을 관리하고 무엇을 먼저 확인할 것인가
S3 제안 방향 및 추천 후보 → 어떤 관리 방향을 제안하고, 필요한 경우 실제 어떤 상품을 보여줄 것인가
S4 상담 Point           → 위 판단을 바탕으로 이 고객에게 실제로 어떻게 접근하고 말할 것인가
S5 관련 TIP & GUIDE     → 어떤 현장 노하우/공식 자료를 참고하고, 어디에서 실제 Action을 수행할 것인가
```

Section 간 역할 중복을 최소화한다.

### 4.1 S1 — 고객 상황

- **Target 역할**: 관찰 가능한 Fact를 직원이 빠르게 이해할 수 있는 고객 상황으로 압축. Management Judgment를 선행하지 않는다(판단은 S2).
- **AS-IS 대비 변화**: ① 구 후보의 "Current State / Recent Change 2단 Block 강제"는 **채택하지 않음** — 자연어 한 문단 요약 구조 유지. 대신 새 Input의 Recent Changes / Money Flow / Timeline / Upcoming Event를 활용해 **현재 상태 + 최근 중요 변화가 함께 보이는 요약**으로 개선. ② **실제 숫자·시점 보존 규칙 신설**: 이번 관리 판단에 중요한 정보(IRP 금액/자산구성·신규 입금액·만기금액과 시점·최근 구성 변화·퇴직급여 유입 등 Money Flow·성향 변화·가까운 중요 Event·필요한 미확인 상태)는 추상화하지 않는다.
  - Bad: "신규 입금분과 곧 만기되는 자금이 있습니다"
  - Target: "최근 개인부담금 1,000만원이 입금되었고, 11월에는 정기예금 1,500만원이 만기될 예정입니다"
- **절제된 해석 허용/금지 경계**: 허용 — "최근 3개월 IRP 수익률 조회 6회" → "최근 IRP 수익률에 대한 관심이 높아진 모습입니다". 금지(의미 승격) — 수익률 조회 증가→변경 의사 확정 / 현금 보유→방치·미운용 확정 / 이전 메뉴 진입→이탈 의사 확정 / CRM 진술→현재 의사·System Fact 확정.
- **Boundary**: 상황 압축까지가 S1. 관리 포인트·제안·화법은 각각 S2/S3/S4. CRM 사용 시 필요하면 Human-authored Context임이 드러나게 표현.
- **필요 Input**: 9-Block ①②③④⑧ (+⑨는 표기 규칙과 함께).

### 4.2 S2 — 핵심 관리 포인트

- **Target 역할**: 이번 상담에서 무엇을 관리할 것인가를 명확히 확정 + 업무 Flow 기준의 "먼저 확인" 배치.
- **AS-IS 대비 변화**: ① 구 후보의 `why_now`·`rationale` **필드 노출은 채택하지 않음** — Why-now는 내부적으로 반드시 판단하되 Final Brief에서는 관리포인트 문장 안에 자연스럽게 녹인다. ② **모델 방어문구 비노출**: "변경 의사로 단정할 수 없습니다" / "Digital Signal은 Intent가 아닙니다" / "CRM만으로 판단할 수 없습니다" 류는 내부 Reasoning/Evaluation에서 지키고 Brief에는 결과만 자연스럽게.
  - Bad: "수익률 조회가 변경 의사를 의미한다고 단정할 수 없으므로…"
  - Target: "최근 신규 입금된 1,000만원과 11월 만기 예정인 1,500만원의 향후 운용방향을 고객의 현재 운용 의사에 맞춰 점검하는 것이 이번 관리의 핵심입니다."
- **먼저 확인하세요 — 재설계**: 구 `[직원]/[고객]` Label 폐기. 업무 Flow 기준 두 영역을 **필요할 때만** 사용:
  - **상담 전 확인** (Operational Check — 시스템/단말/공식자료로 상담 전 확인 가능): 신규 입금분 DO 실제 적용 여부, 중도해지 예상 손실, 실물이전 가능 여부, 실제 수수료, 현재 연금 지급방식 등
  - **고객과 확인** (Decision Variable — System Evidence로 알 수 없는 것): 현재 운용 만족도, 운용 변경 의사, 자금 사용계획, 예상 은퇴시점, 직접/위임 선호, 이전 핵심 사유, 부분이전 의향 등
- **Boundary·규칙**: 빈 Section 강제 생성 금지. **이미 시스템이 아는 사실을 고객에게 재질문 금지**(구 후보 S4 규칙이 S2로 이동한 셈).
- **필요 Input**: 내부 Judgment 결과 + Evidence Trace(내부) + ③⑧(Why-now 재료).

### 4.3 S3 — 제안 방향 및 추천 후보 (핵심 변경 1)

- **Target 역할**: **Management Direction을 결정하고, 상품이 필요한 경우 실제 Product Candidate까지 연결하는 영역.** 구 "추천 운용 방향"의 리밸런싱 중심 프레임을 확장한다.
- **AS-IS 대비 변화**: ① **'비해당(not_applicable)' 구조 폐기** — 중도인출·연금수령·계약이전 Case가 비해당으로 처리되는 구조는 Target이 아니다. 다음 전부가 정상적인 S3 Output: 현재 운용 유지/모니터링 · 신규 입금자금 운용 · 만기자금 재운용 · 포트폴리오 조정/리밸런싱 · 직접↔위임 운용체계 변경 · 추가납입/세제 활용 · 연금개시/수령방식 관리 · **중도인출 지원** · **계약이전/부분이전 지원** · 고객 의사결정 지원 · 실행 불가 시 대안경로 안내. ② **실제 상품 후보까지 내려간다** — "위험중립형 범위 내 펀드 또는 디폴트옵션" 수준의 추상 표현으로 끝내지 않는다.
- **사고 순서** (상품부터 고르고 이유를 붙이는 구조 금지):
  ```
  Management Direction → Solution Type → Actual Product Candidate
  ```
- **추천 후보 Target Output** (승인된 Candidate Pool이 주어진 경우):
  ```
  추천 후보

  ① KB ○○ TDF 2045
  - 위험등급: 4등급
  - 최근 1년 수익률: +7.2% (2026.08.28 기준)
  - 특징: 목표 은퇴시점에 따라 위험자산 비중을 점진적으로 조정
  - 추천 사유:
    · 연금 수령까지 장기간이 남아 있음
    · 고객 투자성향 범위 내
    · 현재 IRP가 예금 중심으로 구성
    · 장기 운용자금으로 확인될 경우 활용 가능
  ```
  포함 수준: 상품명·상품유형·위험등급/위험수준·최근 수익률+측정기간+기준일·주요 운용특징·필요 시 보수/만기/자산구성 등 핵심 Metadata·**이 고객에게 이 상품을 후보로 보는 이유**.
- **추천사유의 기준**: "최근 수익률이 높다"는 그 자체로 추천 논리가 아니다 — 수익률은 Metadata·비교/설명 재료. 추천 논리는 운용기간·자금 목적·투자성향·현재 포트폴리오·운용 경험·직접/위임 선호·고객 의사와 상품 특성의 **Customer–Product Fit**으로 만든다.
- **유지 원칙**: 특정 상품은 반드시 승인 Candidate Pool 내부에서만(LLM 임의 생성 금지). **Branch Preservation, not Branch Creation** — 미확인 Decision Variable이 실제 Direction을 바꾸는 경우에만 조건별 방향, Evidence로 충분하면 단일 방향. `alternatives_not_taken`은 내부 검증/설명용 보조 구조로 검토 가능하나 이번 개편의 핵심 아님.
- **필요 Input/Knowledge**: **Metadata가 붙은 Candidate Pool**(현행 이름 목록 → 등급·수익률+기준일·특징·보수 등으로 확장 필요 — §4.6), 성향 Eligibility(C1/C2/C3), 고객 Evidence.

### 4.4 S4 — 상담 Point (핵심 변경 2)

- **Target 역할**: 가이드("이렇게 접근하세요")가 아니라 — **S1 상황 + S2 관리 포인트/확인사항 + S3 제안 방향/실제 추천상품 + Hot Tip·상담 화법 Knowledge를 결합해, 이 고객에게 실제로 사용할 수 있는 고객 맞춤 상담 화법을 생성하는 영역.** 직원이 읽고 나서 다시 고객에게 할 말을 생각해야 한다면 Target 미달.
- **AS-IS 대비 변화**: 구 "접근 순서 + 실제 화법 최소 1개"에서 → **실제 데이터가 들어간 완성형 화법**으로 수준 상향. 고객의 금액·시점·자산구성·운용기간·상품명·수익률·관리 방향이 화법 안에 반영되어야 한다.
  - Bad: "현재 자산구성과 수익률을 설명한 후 만기자금의 일부 변경을 제안하세요."
  - Target: "고객님, 현재 IRP 8,000만원 중 약 80%가 정기예금으로 운용되고 있고, 11월에는 1,500만원 정도가 만기될 예정인데요. 기존 상품을 모두 바꾸기보다는 이번에 만기되는 자금 일부부터 다른 방식으로 운용해보시는 방법도 있습니다."
- **설득 재료의 경계**: Peer/Performance/연령 등은 — 향후 Benchmark가 Input으로 제공되더라도 — "유사 고객 대비 낮으니 변경하세요" 같은 **Action Trigger로 사용 금지.** S2/S3에서 적절한 Direction이 이미 도출된 이후, S4에서 **고객이 이해하기 쉬운 설명 재료**로만 활용한다. 연령도 "20대이므로 공격 운용" 금지 — "연금수령까지 장기간이 남아 있고, 성향·자금 목적이 허용하는 경우 장기 분산운용을 설명"의 형태.
- **Hot Tip·화법 Knowledge 합성**:
  ```
  S1~S3 판단 + 관련 Hot Tip/상담 화법 Knowledge + 고객의 실제 데이터
      ↓
  Customer-specific Script
  ```
  예: Hot Tip "예금 위주 고객에게는 기존 상품 전체 변경보다 만기 도래자금부터 접근" + 이 고객의 실제 "11월 만기 1,500만원" → 맞춤 화법 생성. **Hot Tip은 무엇을 권유할지 정하는 Business Rule이 아니라, 이미 도출된 판단을 현장에서 어떻게 전달할지 돕는 Knowledge다.**
- **조건부 후속 화법**: 필요한 Case에서 고객 반응별(현재 유지 희망 시 / 일부 변경 관심 시 / 원금손실 우려 시) 후속화법을 조건적으로 제시 가능. 모든 Case에 Branch Script 강제 금지.
- **성공 기준**: S4만 읽어도 직원이 "그래서 고객에게 뭐라고 말하지?"를 다시 고민하지 않는다.
- **Boundary**: S4는 전달(어떻게 말할까) — 판단(S2)·후보 선정(S3)을 재수행하지 않음. 원문 인용은 S5의 몫.
- **필요 Input/Knowledge**: S1~S3 산출 + **상담 화법/반론 Knowledge**(용어 치환·설명 순서·이탈 골격 — `SCREENS_HOTTIPS_INVENTORY §3` 재료의 Case별 동봉).

### 4.5 S5 — 관련 TIP & GUIDE (핵심 변경 3: 두 역할)

**6-1. 실제 Hot Tip / Guide 원문 제공** — "가이드 참고" 식 지시로 끝내지 않고, 이번 Case에 실제 도움이 되는 행내 Hot Tip/Guide의 **관련 원문을 발췌 + Metadata와 함께** 보여준다:

```
💡 현장 Hot Tip

"기존 상품을 모두 변경하기 부담스러워하시는 고객에게는
만기 도래자금부터 일부 운용 변경을 제안하면
상담을 자연스럽게 이어갈 수 있습니다."

👍 좋아요 128 · 작성자: ○○지점 김○○ 대리 · 작성일: 2026.05.12 · 출처: 퇴직연금 Hot Tip
```

- Metadata 후보: Tip 제목·작성자·소속/지점·직급·작성일·좋아요 수·출처. **좋아요 수 = 현장 공감도/활용도 Signal이지 공식성·제도 정확성의 근거 아님.**
- **권위 구분 유지**: 공식 Guide vs Field Hot Tip. 제도/세제/실행 가능 여부는 **공식 Guide 우선**(HD-3).
- **S4와의 차이**: S4 = Hot Tip/화법을 고객 상황에 **적용한 실제 맞춤 상담멘트** / S5 = 그 Hot Tip/Guide의 **실제 원문과 출처**.

**6-2. 다음 Action의 실제 실행 화면** — S3에서 제안한 Action을 실제 업무로 잇는 연결:

```
🖥 직원 업무화면
[123456] IRP 운용상품 변경 — 보유상품 확인 및 운용지시 등록
[234567] 디폴트옵션 운용현황 — 신규 입금분의 실제 적용 여부 확인

📱 고객 StarBanking
퇴직연금 > 개인형IRP > 운용상품 변경 — 고객이 직접 운용상품 변경
퇴직연금 > 상품찾기 > TDF — 상담 중 제안한 상품 상세정보 확인
```

- 확보 가능한 경우 화면번호·정확한 화면명·메뉴 경로·이 Case에서의 사용 목적까지. **S3 Action과 관련 없는 화면의 일반 나열 금지.** Deep Link는 향후 확장 가능(이번 단계 미구현).
- **관계식**: `S3 = 무엇을 할 것인가 / S4 = 고객에게 어떻게 말할 것인가 / S5 = 어디에서 확인하고 실행할 것인가`
- **필요 Input/Knowledge**: Hot Tip **원문+Metadata**가 동봉된 Knowledge Pack(현행 발췌본에는 작성자·좋아요 등 Metadata 없음 — §4.6), 화면 마스터(SRC-027) + **StarBanking 메뉴 경로**(Availability 미확정).

### 4.6 유지되는 REV-002 Core 원칙 + 구현 전 확인 필요 사항

**유지** (이번 Refinement는 Core Reasoning Architecture 변경이 아님): Judgment-first / Business Objective의 관리 필요성 생성 금지(HD-7) / Hard Constraint(C1/C2/C3) / Execution Validation / 투자성향=허용 최대 위험경계 / Epistemic Preservation / Evidence Provenance / Candidate Pool / Branch Preservation / Performance Comparison 단독 Trigger 금지 / Digital Signal ≠ Intent / CRM ≠ authoritative current ground truth. — 단 **이 내부 안전원칙들을 Final Brief에 자기검열 문구로 노출하지 않는다.** Brief는 안전한 Reasoning의 결과를 실용적으로 전달한다.

**구현 게이트 전 확인 필요** (Human 확인/데이터 준비 대상):
1. **Candidate Pool 데이터 구조 확장** — 현행 이름 목록 → S3 상품 카드에 필요한 Metadata(유형·등급·최근 수익률+측정기간+기준일·특징·보수/만기 등) 포함 구조. Synthetic Case에서의 작성 책임과 형식.
2. **Hot Tip 원문·Metadata 동봉 방식** — Knowledge Pack에 발췌 원문+작성자/작성일/좋아요/출처를 어떻게 싣는가. Synthetic Metadata(작성자·좋아요 수) 생성 허용 여부(실자료가 아니므로 Human 확인 필요).
3. **StarBanking 메뉴 경로 Availability** — 화면번호 마스터(SRC-027)에는 직원 단말 중심; 고객 앱 메뉴 경로의 Source 확인 필요 (`?`).
4. **EMPLOYEE_BRIEF_SPEC.md 개정 범위** — 구현 승인 시 not_applicable 규칙 폐기·S3/S4/S5 Target 반영·구 §1 필수/금지 목록과의 정합 정리.
5. 유사 고객군/Benchmark Input(§4.4 언급)은 현재 Scope 밖(Peer 제외 유지) — 향후 제공 시의 사용 경계만 이 문서에 선기록됨.

## 5. 기존 P2 후보 GC-18~25 재분류 — **방향 승인 (Decision 6)**

> 재분류 방향은 원칙 승인됨. 단 **P2 Case의 실제 작성·Expected Output·Evaluation 설계는 시작하지 않는다** — Employee Brief Target이 별도 Gate에서 변경될 예정이므로, 새 Brief 구조 확정 이후에 Case를 작성한다. GC-18은 ISA-IRP 목적 연결의 사전 해석 금지(Fact만 제공, 관계 구성은 Agent), GC-19는 Sequence 우선 + degraded 버전 설계 가능 원칙이 함께 승인됨.

| 후보 | 분류 | 사유 |
|---|---|---|
| **GC-18** (Whole-Asset) | **Input 구조 수정 필요** | 지시 관점 반영: 초안의 "ISA 만기 전환 대기 가능성" 구도가 ⑦에 목적 해석을 심을 위험. 수정 방향 — ⑦에는 ISA 보유·잔액·가입일만(사실), 만기·D-n은 ⑧에 시한으로만, **"전환 대기" 유추 재료를 어디에도 사전 배치하지 않음**. 연결 자체를 Agent가 ③(현금 유입)과 ⑧(ISA 만기)에서 스스로 구성해야 통과하는 구조로 재설계 |
| **GC-19** (Digital Signal) | **Scenario 수정 필요** (+⑥ Sequence 의존) | 지시 관점 반영: 단일 신호(메뉴 진입 2회)가 아니라 **행동 Sequence**(수익률 조회 → 타사 비교 조회 → 이전 메뉴 진입 → **미실행**, 시간순)로 재설계. Sequence가 강할수록 Intent 승격 유혹이 커지므로 경계 검증이 더 정확해짐. ⑥ Sequence Availability 미확정 시 두 버전(횟수형/Sequence형) 설계 |
| **GC-20** (CRM 과신) | **그대로 유지 가능** (경미 조정) | 새 ⑨ 지위와 정확히 정합 — 오래된 메모(⑨, 경과일 ~3년) vs 최근 System Evidence(④ 성향 재분석 Event + ⑥ TDF 조회)의 충돌 구도가 새 구조에서 자연 성립. 조정: 관련 Evidence 병렬 표기(⑨ 추가 후보)를 이 Case에서 최초 적용 |
| **GC-21** (Performance) | **그대로 유지 가능** | 필요 필드(두 수익률 구분·보유기간) 전부 ② AS-IS. ③(변화)이 생기면 "최근 회복 추세" 재료가 보강되나 필수 아님 |
| **GC-22** (Multiple Events) | **Input 구조 수정 필요** (경미) | 시나리오 유효. 한도 2종의 ⑦ 이동·DO Clock의 ⑧ 이동을 반영해 Evidence 배치 재기술 — 오히려 ⑧ Decision Horizon의 본검증 Case로 적합성 상승 |
| **GC-23** (부분대안) | **그대로 유지 가능** | 구조 변화의 영향 없음. S3 `alternatives_not_taken`(§4)이 승인되면 F-010 검증 해상도가 올라감 |
| **GC-24** (결정세액) | **Input 구조 수정 필요** (경미) | 한도 3필드의 ②/⑦ 분리 배치를 반영해 재기술 — "잔여한도(⑦ 합산 개념)를 보고 IRP 납입(②)을 확정 권유"하는 유혹 구조가 더 선명해짐 |
| **GC-25** (미신청분 해지) | **그대로 유지 가능** (경미 조정) | 7/1 시한을 ⑧ "기타 예정 Event"로 표현하는 조정만 |

보류 필요: 없음 (8개 전부 새 방향과 양립 — 4개는 수정 후).

## 6. ~~Human 결정 필요 항목~~ → 결정 완료 (HD-PRE-P2-INPUT, 2026-08-31)

| 항목 | 결정 |
|---|---|
| 1. 9-Block 구조·이동안 | **승인** — Recent Changes 분리·Sequence 확장·CRM ⑨ 재위치·①~⑧ 선직렬화·한도 ⑦·DO Clock ⑧ 전부 승인. 수정 2건 반영: 잔액-Flow는 산술 reconciliation까지(1-1), ⑧ "결정 성격 한 줄" 제거(1-2) |
| 2. ③ Recent Changes 범위 | **Window 기반 구조** — 30d 우선, 90d는 확보 시, 특정 기간 강결합 금지. 90d Snapshot Av `?` 유지. 잔액-Flow reconciliation 포함(1-1 Boundary 적용) |
| 3. ⑥ Sequence | **방향 승인** — Sequence도 Signal(Intent 아님·Label 금지). Av `?` 유지, P2는 Sequence Case 사용 가능하되 횟수/Event 형태로 degraded 가능해야 함 |
| 4. 3-Layer 표현 구조 | **방향 승인** — P2 신규 Case부터, 기존 Frozen 불변. Stable E-ID·JSON 우선안·evidence_type/source_type 분리 확정. 구현은 금지 상태 유지 |
| 5. Brief Refinement 5건 | **미승인 — 별도 Human Brief Design Gate로 이동** (Reject 아님). Target Brief 확정 금지, Schema/Prompt/Validator 변경 금지 |
| 6. GC-18~25 재분류 | **원칙 승인** (유지 4 / Input 수정 3 / Scenario 수정 1 / 보류 0). 단 Case 작성·Expected Output·Evaluation 설계는 Brief 구조 확정 이후 |
| 7. Availability `?` 5건 | **전부 `?` 유지** (퇴직일 상세·90d Snapshot·거래횟수 세분화·Sequence/실행 여부·CRM 작성 주체) — 임의 O/X 확정 금지, 실제 Source 확인으로만 갱신 |

## 7. 현재 Gate 상태 (HD-PRE-P2-INPUT 이후)

```
REV-002                     → CLOSED 유지
Pre-P2 Input Architecture   → Human Direction Approved (수정사항 반영 완료)
Employee Brief Architecture → Target Design 확정 (Human Direction 반영, §4) — Schema/Prompt/Validator/Runtime 구현 게이트 PENDING
GC-18~25                    → Candidate / HOLD 유지 (재분류 방향만 승인, 작성·Freeze 금지)
Runtime / Schema / Parser   → 구현 금지
P2 RUN / EVAL               → 시작 금지
```
