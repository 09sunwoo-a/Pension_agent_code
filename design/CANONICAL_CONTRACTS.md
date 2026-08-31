# Canonical Evidence Object & Supply Contracts (Pre-P2 Architecture Refinement)

- Status: **Phase A 산출물 (2026-08-31)** — HD-PRE-P2-INPUT(3-Layer·Stable ID·JSON·type 2축)과 HD-PRE-P2-BRIEF(공급계약 선확정)의 구현 계약서. 이 문서가 Loader(Phase C)·Renderer(Phase D)·Brief v3(Phase F 상당)·Case 작성(Phase H)의 공통 계약이다.
- 원칙: 단일 사실 원천(이중 기입 금지) / Stable ID / evidence_type·source_type 2축 분리 / 전처리는 What happened·What changed까지 / **Agent가 생성할 수 없는 것(상품·Tip 원문·화면)은 supply로만 공급**.

---

## 1. Canonical Evidence Object — 파일 계약

Case당 단일 파일 `cases/<CASE>/canonical.json` (P2 신규 Case·Diagnostic fixture 전용 — 기존 Frozen input_v2/case.md는 불변).

```json
{
  "case_id": "GC-XX",
  "base_date": "2026-08-28",
  "evidence": [ EvidenceItem, ... ],
  "supply": {
    "product_candidates": [ ProductCandidate, ... ],
    "hot_tips": [ HotTip, ... ],
    "screens": [ Screen, ... ]
  }
}
```

### 1.1 EvidenceItem

```json
{
  "id": "E101",                  // Stable ID — 파일 내 유일, 렌더 순서와 무관하게 불변. E+3자리
  "block": 1,                    // 1~9 (아래 Block 정의)
  "evidence_type": "fact",       // fact | arithmetic_derived | rule_derived | signal
  "source_type": "account_system", // account_system | transaction | digital_behavior | crm
                                  // | external_account | rule_engine
  "text": "고객 연령: 만 53세",     // 사람이 읽는 한 줄 (렌더 시 이 문자열이 그대로 bullet)
  "as_of": "2026-08-28",         // 값의 기준일/발생일 (모름이면 생략)
  "data": { "kind": "age", "years": 53 }   // 선택 — Derived Engine이 소비하는 구조값 (§1.3)
}
```

- **작성자는 evidence_type=fact/signal만 쓴다.** arithmetic_derived/rule_derived 항목은 Derived Engine이 생성해 부착한다(수기 작성 금지 — Layer 분리).
- text에는 판단 완료형 라벨·의미 부여("방치·미운용·대기성" 류) 금지. NULL/0/해당없음 구분 표기.
- source_type=crm 항목은 작성일·채널·작성주체(확보 시)를 text에 포함하고 block=9에만 둔다.

### 1.2 Block 정의 (HD-PRE-P2-INPUT 9-Block)

| # | Block | 주 source_type |
|---|---|---|
| 1 | Customer & Retirement Lifecycle | account_system |
| 2 | Current IRP Snapshot | account_system |
| 3 | Recent Changes & Money Flow | account_system·rule_engine(파생) |
| 4 | Event Timeline | transaction |
| 5 | Investment Behavior | transaction·account_system |
| 6 | Digital Behavior & Sequence | digital_behavior |
| 7 | Wider Financial Context | external_account·account_system |
| 8 | Upcoming Decision Horizon | account_system·rule_engine(파생) |
| 9 | Supplementary Human-authored Context | crm |

### 1.3 data.kind 어휘 (Derived Engine 소비 — 필요한 것만 부착)

| kind | 필드 | Engine 산출 (→ 대상 block) |
|---|---|---|
| `age` | years | R1 개시요건 (→1) |
| `join_date` | date | R1 |
| `retirement_benefit` | included(bool) | R1 |
| `deposit` | date, amount, reason | 입금 경과일 A (→3) |
| `maturity` | date, amount, product | D-n A (→8) |
| `balance_snapshot` | date, cash, total | window 변화 A (→3): base_date 대비 30d/90d — 스냅샷이 있는 window만 계산(강결합 금지) |
| `current_balance` | cash, total | window 변화·reconciliation의 현재값 |
| `do_registration` | registered(bool), trigger_type(최초입금/만기), trigger_date | Rule Clock R (→8) |
| `limit_value` | limit_kind(tax_credit/contribution), amount | R 수신값 표기 (→7) |
| `behavior_event` | date, action, executed(bool) | Sequence 정렬 표기 보조 (→6; 파생 계산 없음) |

**잔액-Flow reconciliation** (A, →3): current_balance.cash와 개별 deposit.amount의 **금액 일치만** 검사해 "금액 일치" 사실 서술 생성. 의미 부여 금지(HD-PRE-P2-INPUT 1-1).

### 1.4 Derived Item 규칙

- Engine이 생성하는 item: id는 `D` + 3자리, **생성 순서가 canonical evidence 순서의 결정적 함수**(같은 입력 → 같은 ID). evidence_type=arithmetic_derived 또는 rule_derived.
- rule_derived는 text 말미에 `| rule_source=... | rule_as_of=... | rule_id=...` 필수.
- Engine 출력 어휘 금지 목록: "방치", "미운용", "대기성", "남아 있는" — 단위 테스트로 강제.

## 2. Supply Contracts (S3/S4/S5 공급 데이터 — Agent 생성 불가 영역)

공통 원칙: **여기 없는 상품·Tip·화면을 모델이 만들면 validator FAIL.** 모델 출력은 아래의 `*_id` 참조 + Agent 생성분(추천사유·화법·용도 코멘트)만 담고, 카드·원문·경로의 실제 데이터는 record/Brief 렌더 시 supply에서 결정론적으로 복원한다(복사 오류·변조 원천 차단).

### 2.1 ProductCandidate

```json
{
  "product_id": "P01",
  "name": "KB온국민TDF2045",
  "product_type": "TDF",
  "risk_grade": 4,                      // 1~6 (C2 검증 대상)
  "risk_level_label": "보통위험",
  "return_recent": 0.072,
  "return_period": "1Y",
  "return_as_of": "2026-08-28",
  "features": "목표 은퇴시점에 따라 위험자산 비중을 점진 조정",
  "fee_note": "총보수 연 0.xx%",          // 선택
  "maturity_note": null,                 // 선택 (원리금보장형)
  "sellable": true,                      // 판매 가능 여부
  "channels": ["앱", "창구"]             // 채널 가능 여부
}
```

**추천사유는 이 계약에 없다** — Customer Evidence + Management Direction + 위 Metadata를 결합해 **Agent가 생성**한다(HD 지시). sellable=false·성향 밖 등급 상품을 넣어 유혹 구조를 만들 수 있다(모델이 걸러야 함 — C2/판매가능 validator).

### 2.2 HotTip / Guide

```json
{
  "tip_id": "T01",
  "kind": "field_hot_tip",              // field_hot_tip | official_guide
  "title": "만기 도래자금부터 접근하는 상담법",
  "body": "기존 상품을 모두 변경하기 부담스러워하시는 고객에게는 ...",   // 원문 발췌
  "author": "○○지점 김○○ 대리",          // 원천에 있을 때만 — 임의 생성 금지
  "author_org": "○○지점", "author_title": "대리",
  "written_at": "2026-05-12",
  "likes": 128,                          // 공감도 Signal — 공식성 근거 아님
  "source": "퇴직연금 Hot Tip (SRC-0xx)"
}
```

- 원천에 없는 author/likes 등은 **필드 생략**(임의 생성 금지 — Human 확인: 원천에 실존하므로 실자료 기반 Case에서는 채울 수 있음).
- kind=official_guide가 제도·세제·실행 가능 여부의 우선 권위(HD-3). Brief 렌더 시 kind에 따라 표기 구분.

### 2.3 Screen

```json
{
  "screen_id": "S01",
  "surface": "staff",                    // staff | starbanking
  "screen_no": "[04-12-642]",            // staff만; 미확인이면 생략
  "screen_name": "적립금및수익률조회",
  "menu_path": null,                     // starbanking: "퇴직연금 > 개인형IRP > 운용상품 변경"
  "actions": "보유상품 확인 및 운용지시 등록"   // 이 화면에서 가능한 Action
}
```

- Availability 미확인 화면은 Case에 넣지 않는다(`?` 유지·임의 생성 금지).

## 3. 모델 출력에서의 참조 계약 (Brief v3에서 소비 — Phase F 설계의 전제)

- S3 상품: `{"product_id": "P01", "reasons": ["..."]}` — reasons만 Agent 생성, 카드는 supply에서 복원.
- S5 Tip: `{"tip_id": "T01", "why_relevant": "..."}` — 원문은 supply에서 복원(모델이 body를 재작성하지 않음).
- S5 화면: `{"screen_id": "S01", "purpose_here": "..."}` — 번호·경로는 supply에서 복원. **S3 Action과 직접 연결된 것만 선택.**
- Validator(deterministic): 출력의 모든 product_id/tip_id/screen_id ⊆ supply의 id 집합; sellable=false 상품의 추천 후보 등재 FAIL; 성향 밖 risk_grade FAIL(C2 확장).

## 4. Frozen 보호·Dispatch

`canonical.json` 존재 → v3 경로 / `input_v2.md` → REV-002 / 그 외 → REV-001. 기존 Frozen Artifact(case.md·input_v2·RUN·EVAL)는 읽기 전용 — v3 경로는 신규 Case·fixture에만 적용.
