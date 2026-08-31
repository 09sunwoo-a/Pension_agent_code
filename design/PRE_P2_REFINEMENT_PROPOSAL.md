# Pre-P2 Input / Brief Refinement — Design Proposal

- Status: **PROPOSAL — Human Design Gate 검토 대기 (2026-08-31).** 승인 전 P2 Case 작성·Freeze·RUN/EVAL·Runtime 변경 금지. 이 문서는 설계 제안이며 어떤 구현도 포함하지 않는다.
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
| 추가 후보 | **1M/3M 평가금액 변화**(전체·자산유형별 금액/비중, A) / **현금성자산 증감(1M/3M)** / **최근 자금 발생 원천 요약**(최근 N건 입금·만기상환·매도대금의 사유별 합계 — ④ Event의 집계 뷰) / **잔액-Flow의 객관 연결**(가능한 경우: "현재 현금성 X원 중 Y원은 mm-dd '만기상환' 입금분과 금액 일치" 수준의 **산술 대조**만 — 기계적 등식, 원인 단정 아님) |
| 삭제·통합 | — (신설) |
| Type | A (전부 산술 파생 — Canonical의 과거 스냅샷·Event에서 계산) |
| Av | 1M 변화 O 추정([9C] 실존) / **3M 변화·과거 시점 잔액 스냅샷 ?** / 잔액-Flow 연결은 파생이므로 — |
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
| 확보 난이도 | **중~높음** — 확보 불가 시 횟수형으로 축소 운영(P2 Case는 두 수준 모두 설계 가능하게) |

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
| 추가 후보 | **기타 실제 예정 Event**(성향분석 유효기간 만료 예정, 세액공제 연말 시한 등 — 원천 실존·규칙 파생 가능한 것만), 시한별 **결정 성격 한 줄**(예: "만기 → 재예치/변경 결정 필요") — 단 이것이 사전해석이 되지 않도록 "결정이 필요한 시점"이라는 사실 서술까지만 |
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

**TO-BE 3-Layer**:

```
Layer 1  Canonical Evidence Object  (Case당 단일 구조화 파일 — 유일한 사실 원천)
         item = { id, block(①~⑨), type(F/A/R/S/CRM), field, value, as_of, unit?, source? }
         사람(Case 작성자/향후 시스템)은 이것만 작성한다. 서술문 없음.
  ↓ deterministic
Layer 2  Derived Context Engine  (전처리 — Canonical만 입력으로 A/R Fact 생성)
         비중·D-n·경과일·1M/3M 변화·Rule Clock·잔액-Flow 산술 대조
         전부 rule_source/rule_as_of/적용 Rule ID 추적. 의미 판단 금지.
  ↓ deterministic
Layer 3  LLM-friendly Rendering  (렌더러 — Canonical+Derived → 9-Block 한국어 Markdown)
         E-ID 부여·블록 순서·경계 주석(⑥⑨)·NULL/0/해당없음 표기·CRM 관련 Evidence 병렬 표기
         렌더링 정책 변경이 Case 파일과 완전히 분리됨
```

- 효과: 단일 원천(불일치 제거) / Case 작성은 Canonical만(작성 비용 절반) / 실데이터 연동 시 Layer 1만 시스템 인터페이스로 교체하면 됨(Availability 확정 필드 = Canonical 필드 정의와 일치) / 렌더링·주석 개선이 re-Freeze 없이 가능.
- 마이그레이션: P2 신규 Case부터 Canonical 작성 + 렌더러로 Markdown 생성. **기존 input_v2 8건은 불변**(재변환하지 않음). Parser/Schema/runtime 수정은 이 Proposal 승인 후 별도 구현 단계에서.
- 미결(승인 시 결정): Canonical 파일 형식(JSON vs YAML — 가독·주석 필요성으로 YAML 우세하나 stdlib 제약상 JSON 우세), E-ID를 Canonical id로 고정할지(렌더 순서 무관 안정 ID — **권장**) vs 렌더 시 부여(현행).

## 4. Employee Brief Refinement 후보 (구현 보류)

| 섹션 | 후보 | 근거 |
|---|---|---|
| **S1** | **Current State + Recent Change 2단 구조**: 상태 한 문장 + "최근 변화" 한 문장(③에서 — "3주 전 퇴직급여 1.8억 유입 후 매매 없음"). 변화 서술에는 근거 E-ID 연결 | What changed가 S1에 명시돼야 S2 Why-now가 서술이 아닌 사실에 얹힘 |
| **S2** | **`why_now` 필드 분리**: {point, why_now(어떤 Event/변화/시한 때문에 지금인가 — ③④⑧의 E-ID 필수 연결), rationale, confirm_first}. Why-now 없는 관리 포인트는 검증 대상(HD-7 연장) | 현행은 point/rationale에 Why-now가 섞여 선명도 낮음. Evidence Trace의 자연 확장 |
| **S3** | **`alternatives_not_taken` 선택 필드**: 채택 방향 외에 "검토했으나 이번에 제시하지 않은 대안 + 한 줄 사유"(유지/부분대안/시점조정 포함) — F-010의 정보 손실을 구조로 보존. 분기 규칙(Branch Preservation)은 불변 | GC-16 부분대안 2연속 부재 — 대안이 '없던 것'인지 '기각된 것'인지 구분 불가했음 |
| **S4** | **Decision Variable 전용 규칙**: 확인 질문은 Evidence Pack에 **없는** Decision Variable만. 시스템 기지 사실의 재질문 금지(deterministic 후보: 질문 항목이 Evidence 필드명과 충돌하면 REVIEW). scripts는 [확인 질문형 1 + 설명형 1] 권장 구조 | 결정 2-11의 출력측 완성 — 아는 것을 물으면 직원 신뢰 하락 |
| **S5** | **실행 단위 구조화**: {할 일(동사형), 화면/채널([번호] 화면명), 출처, as_of?, 후속관리 시점?} — "지식 나열"이 아니라 "직원의 다음 동작" 중심. 빈약 영역의 "자료 없음—확인처" 규칙 유지 | Answer Quality의 Actionability·Practical Utility 축과 정합 |

공통: 전부 **표현·구조 후보**이며 판단 의미(Judgment 6유형·Constraint·분기 규칙)는 불변. 구현 시 스키마 변경이므로 승인 후 진행.

## 5. 기존 P2 후보 GC-18~25 재분류 (새 Input 방향 대입)

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

## 6. Human 결정 필요 항목 (이 Proposal의 승인 범위)

1. 9-Block 구조·이동안(§2) 승인 여부 — 특히 한도 2종의 ⑦ 이동, DO Clock의 ⑧ 이동, CRM의 ⑨ 재위치.
2. ③ Recent Changes의 범위 — 1M만 vs 1M/3M, 잔액-Flow 산술 대조 포함 여부.
3. ⑥ Sequence·실행 여부 필드 — Availability 미확정 상태에서 P2 Case 설계에 포함할지(두 버전 설계 권장).
4. Canonical Evidence Object 3-Layer(§3) — 설계 방향 승인 여부와 적용 시점(P2 신규 Case부터 vs 보류).
5. Brief Refinement 5건(§4) — 각각 채택/보류 (특히 S2 why_now·S3 alternatives_not_taken은 스키마 변경).
6. GC-18~25 재분류(§5) 승인 — 수정 4건의 재설계 방향 포함.
7. 신규 Availability `?` 5건: 퇴직일 상세 / 3M 변화·과거 스냅샷 / 거래횟수 기간 세분화 / ⑥ Sequence·실행 여부 / ⑨ 작성 주체.
