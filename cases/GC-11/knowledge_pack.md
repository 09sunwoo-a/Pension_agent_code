# GC-11 Knowledge Pack

```text
Case: GC-11 / Status: FROZEN / Frozen At: 2026-09-01 / Approved By: Agent (HD-5)
```

---

## Knowledge Items

### K-001. 현금성자산 입금사유별 해석 — "연금지급" 대기분은 정상
- **Knowledge (Source-derived)**: 고유계정대 현금성자산은 [04-12-644] 거래내역의 입금 사유가 "교체매매"나 "연금지급"이면 정상 거래 과정의 자금이며 미운용으로 안내하지 않는다. 미운용 판단은 1개월 이상 무변동 + 그 외 사유일 때.
- **Source / Location**: SRC-002 L178
- **Authority / Status**: Internal / Operational
- **Case Relevance**: 1,800만(연금지급)은 관리 대상이 아니고, 300만(만기상환)만 운용지시 대상.
- **Limitation**: —

### K-002. 연금수령 방식과 ETF — 자유인출방식만 수령기간 중 ETF 운용 가능
- **Knowledge (Source-derived)**: 연금수령방식은 기간지정·금액지정·자유인출 3종이며 방식 간 변경이 가능하다. 행내 가이드: "**자유인출방식만 연금 수령기간에 ETF를 운용할 수 있어요. 꼭 기억하세요!**" 현장 정리: 연금 금액/기간지급 시 ETF는 전량 매도가 필요(자유인출 예외). 연금수령 중인 경우 중도인출은 해지만 가능.
- **Source / Location**: SRC-003 `…/개인형IRP_마케팅_보물지도_Vol1.md` L258–264, L286, L231; SRC-084 `…/2026-07-20_207270_내노후는 <<배당 ETF로!>>.md` (Field — 지급방식별 ETF 매도)
- **Authority / Status**: Internal Guide 이론편 (2026-03) — 불가 원칙; SRC-084 Field — 매도 절차는 Operational Check Needed(HD-3)
- **Case Relevance**: 금액지정 수령 중 고객의 ETF 매수 요청은 현 방식에서 실행 불가; 자유인출로 변경하면 가능하나 변경 절차·지급 일정·연차 영향은 확인 대상.
- **Limitation**: 방식 변경의 세부 효과(지급일·한도·연차 기산)는 화면([02-12-221]) 확인.

### K-003. 인컴 니즈의 대안 유형 — 월분배형 ETF의 구조, 인컴 펀드·연금인컴 포트폴리오
- **Knowledge (Source-derived)**: 월분배형 ETF의 분배금은 연금계좌로 입금되어 재투자하거나 자유인출 방식으로 인출할 수 있다(ETF 자체는 자유인출 방식에서만). 행내 포트폴리오 자료에는 연금수령(예정) 전용 2종(연금든든테마: 국내채권 100%; 연금인컴테마: 국내채권 80/해외채권 20)이 있고, 디폴트옵션 구성 상품 중 TIF(Target Income Fund)는 안정적 수익·매달 일정 배당을 목표로 하는 글로벌 멀티에셋 펀드다.
- **Source / Location**: SRC-022 `…/월분배형_ETF_월배당상품.md` L7–9; SRC-094 L119–140; SRC-089 L63–65 (TIF)
- **Authority / Status**: Training / Product Data (2026.08) / Public
- **Case Relevance**: 현 방식(금액지정) 유지 시 "배당 ETF" 대신 위험중립 범위의 인컴형 펀드·연금인컴 포트폴리오 유형이 대안; 배당 니즈의 실체(현금 흐름 vs 성장) 확인.
- **Limitation**: 특정 상품명·비중 금지. 배당 ETF는 방식 변경 후에만.

### K-004. 연금 수령 중 운용 지속과 투자기간 — 수령 종료 시점까지
- **Knowledge (Source-derived)**: 연금을 나눠 받는 동안에도 계속 운용해야 하며 투자가능기간은 수령 종료 시점까지다. 다만 연금수령 중 고객에게 적립식 분산투자를 권유하는 것은 수령액 감소로 이어질 수 있어 부적합하다는 현장 정리가 있다.
- **Source / Location**: SRC-020 L58–73; SRC-041 (Field — 연금개시 중 적립식 분산투자 금지)
- **Authority / Status**: Training / Operational
- **Case Relevance**: 수령 중 운용은 정상; 300만·기존 포트폴리오 유지 판단.
- **Limitation**: —

### K-005. 연금 수령 중 제약 — AI투자일임 제외, 1,500만 기준은 세전·합산
- **Knowledge (Source-derived)**: AI투자일임은 연금 수령을 시작한(금액지정·기간지정) 고객을 제외한다. 사적연금 연간 수령액이 1,500만원을 초과하면 종합과세 또는 16.5% 분리과세 선택이며, 기준은 세전 금액이고 세액공제 받은 부담금·운용수익 분에 대해서만(퇴직급여분 제외) 여러 기관 합산으로 본다.
- **Source / Location**: SRC-091 L54; SRC-003 L300–304; SRC-036 (세무사 설명 — 1,500만 세전·합산)
- **Authority / Status**: Public / Internal / Public(웨비나)
- **Case Relevance**: 대안에서 AI일임을 제외; 연간 1,800만 수령 고객의 세제 상황은 "확인 필요"(HD-1: 계산 없음).
- **Limitation**: 세제 수치 단정 금지.

### K-006. C1·C2·C3 — 위험중립형
- **Knowledge (Human-approved)**: 허용 안정형~위험중립형; 4~6등급; 뿔려드림까지. 기존 보유(TDF2025 4등급)는 범위 내.
- **Source / Location**: HD-2·2.1
- **Authority / Status**: Human-approved
- **Limitation**: —

### K-007. 실행 불가 안내의 톤 — 정확히 말하고 대체 경로 제시
- **Knowledge (Source-derived)**: 고객 요청이 제도상 불가하면 명확히 알리고 가능한 대체 절차·확인 경로를 안내한다(웨비나: "53세 해지 외 방법 없음"처럼 실행 불가는 분명히). "알려준다는 마음"으로 상담.
- **Source / Location**: SRC-036 (실행 불가 사례); SRC-003 L759
- **Authority / Status**: Public / Internal
- **Limitation**: —

---

## Knowledge Gaps
- 지급방식 변경 절차·지급 일정 영향의 공식 원문; 금액지정 시 ETF 전량 매도 절차 — Operational Check.

## Source Notes
| Source | Section | Authority | 사용 |
|---|---|---|---|
| SRC-002 | L178 | Internal | K-001 |
| SRC-003 | L231, L258–304, L759 | Internal 이론편 | K-002, K-005, K-007 |
| SRC-084 / SRC-041 | — | Operational | K-002, K-004 |
| SRC-022 / SRC-094 / SRC-089 | L7–9 / L119–140 / L63–65 | Training / Product / Public | K-003 |
| SRC-020 / SRC-091 / SRC-036 | — | Training / Public | K-004, K-005, K-007 |
| HD-2·2.1 | — | Human-approved | K-006 |
