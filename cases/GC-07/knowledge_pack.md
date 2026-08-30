# GC-07 Knowledge Pack

```text
Case: GC-07 / Status: FROZEN / Frozen At: 2026-09-01 / Approved By: Agent (HD-5)
```

---

## Knowledge Items

### K-001. 위험자산 투자한도 70% — 대상과 예외 (공식)
- **Knowledge (Source-derived)**: 개인형IRP는 정기예금·ELB/DLB·펀드·ETF·TDF 등을 원하는 비중으로 운용할 수 있으나, "주식형·주식혼합형 펀드 등 위험자산은 평가금액의 70% 이내에서만 운용 가능"하다. 행내 가이드: "근로자퇴직급여 보장법 시행령에 따라 주식형 및 주식혼합형 펀드의 경우 위험자산으로 분류되어 전체 적립금의 70% 범위 내에서만 운용", "금감원장이 정한 기준을 충족한 TDF(적격 TDF), 디폴트옵션 상품은 적립금의 100%까지 운용 가능 — 당행 퇴직연금에서 운용 가능한 TDF는 전부 적격 TDF". 같은 가이드는 "주식형 펀드 70% + TDF 30%로 운영하면 주식비중 94% 효과"처럼 실질 주식비중이 높아질 수 있음을 설명한다.
- **Source / Location**: SRC-087 `04_KBthink_연금/01_IRP_개인형퇴직연금.md` L68; SRC-003 `…/개인형IRP_마케팅_보물지도_Vol1.md` L179–191, L368–369(팩트체크 6·7)
- **Authority / Status**: Public 심의필 정리본 (2026-06) / Internal Guide 이론편 (2026-03) — Official 성격
- **Case Relevance**: 73.8%가 ETF 2종 합산이며 TDF(적격)는 산정 제외라는 판단의 근거.
- **Limitation**: 규정 원문(시행령·감독규정)은 Corpus에 없음 — 세부 예외 범위는 확인 대상.

### K-002. 초과 시 조치·예외 확대·페널티 — 현장 정리 (Operational Check)
- **Knowledge (Source-derived)**: 영업점 Hot Tip 정리: 위험자산(주식형·주식혼합형 펀드 및 ETF 포함) 투자한도는 적립금의 최대 70%; 디폴트옵션·TDF·**채권형·채권혼합형 ETF**는 예외적으로 최대 100%까지 투자 가능; 한도 초과 시 조치는 "초과 금액을 정기예금 등 안전자산으로 교체매매 또는 추가입금 후 안전자산으로 운용지시"; "투자한도 초과에 따른 별도 페널티 없음"; 초과 내역은 [04-12-354] 컴플라이언스 위반점검 현황조회(고객명·위반기준일·위반일수·한도초과상품·초과금액·보유가능금액)에서 확인. 다른 Hot Tip은 "주식형 70% + 채권형/채권혼합형 30% = ETF 100%" 구성을 소개하나 이는 실질 주식비중을 높이는 우회 사례다.
- **Source / Location**: SRC-077 `…/2026-04-27_205618_* 퇴직연금 100% 투자 가능 상품 정리 *.md` L18–44; SRC-081 `…/2026-06-29_206430_ETF 100%운용지시로….md` L26–38 (⚠ negative)
- **Authority / Status**: **Operational (Field Know-how, 직원 정리)** — 조치 방법·"페널티 없음"·채권형 ETF 예외는 공식 기준 확인 전까지 `Operational Check Needed`(HD-3)
- **Case Relevance**: 고객의 "팔기 싫다"에 맞는 조치 경로(추가입금 후 안전자산 운용지시)의 근거; 페널티는 단정 금지.
- **Limitation**: SRC-081의 ETF 100% 구성은 사용하지 않는다. "페널티 없음"을 확정 사실로 말하지 않는다.

### K-003. 납입한도와 추가입금 — 조치 경로의 전제
- **Knowledge (Source-derived)**: 개인형IRP 연간 납입한도는 1,800만원(전 금융기관 IRP·DC 개인부담금·연금저축 합산). 추가입금 후에는 운용지시(또는 등록된 디폴트옵션 2주 후 적용)가 필요하다.
- **Source / Location**: SRC-087 L75–80; SRC-089 L35
- **Authority / Status**: Public 심의필 정리본
- **Case Relevance**: 추가입금 경로는 잔여 납입한도(입력 1,300만) 안에서만 가능하고, 입금 후 비위험자산으로 운용지시해야 비중이 내려간다(뿔려드림1 자동 적용도 TDF 70%라 비위험 효과는 제한적일 수 있음 — 확인).
- **Limitation**: 세액공제 한도는 별개 주제.

### K-004. 현금성자산은 위험자산이 아니다 — 비중 계산의 이해
- **Knowledge (Case-local Interpretation — K-001/K-002 근거)**: 위험자산 비중은 위험자산 평가액 ÷ 전체 평가금액이다. 고유계정대(현금성자산)와 TDF·정기예금·채권형은 분모에만 들어가므로, 현금성자산 400만원을 정기예금 등 비위험 상품으로 바꿔도 비중은 변하지 않는다. 비중을 낮추려면 (a) 위험자산을 줄이거나 (b) 분모를 늘리는 추가입금(비위험 운용)이 필요하다.
- **Source / Location**: 산식 해석 — SRC-087 L68 "평가금액의 70% 이내", SRC-077 L32
- **Authority / Status**: Case-local Interpretation (산술)
- **Case Relevance**: "고유계정대를 운용지시하면 해결된다"는 오답을 막는다.
- **Limitation**: 시스템의 정확한 산정 기준(평가일·분모 정의)은 확인 대상.

### K-005. ETF 실행 채널 — 고객 본인 앱 매수/매도, 3분 분할
- **Knowledge (Source-derived)**: ETF 매매는 현금성자산 상태에서 고객 본인이 스타뱅킹에서 직접 한다(전화센터는 정기예금·고유대만). 은행 ETF는 장중 3분 분할매매, 신청 24시간.
- **Source / Location**: SRC-069 L14–16; SRC-004 L83–85
- **Authority / Status**: Operational / Internal
- **Case Relevance**: 조치의 실행 주체·채널.
- **Limitation**: —

### K-006. C1·C2·C3 — 적극투자형
- **Knowledge (Human-approved)**: C1 허용 안정형~적극투자형(공격투자형 제외). C2(HD-2.1): 적극투자형은 3~6등급 권유 가능, 1~2등급(매우높은·높은위험) 불가 — 기존 보유 1등급 ETF는 위반 아님, **추가 매수 권유는 불가**. C3: 모두드림 불가. 성향은 상한.
- **Source / Location**: HD-2·HD-2.1; SRC-096; CONSTRAINT_MAP
- **Authority / Status**: Human-approved
- **Case Relevance**: 조치 대안에서 1등급 ETF 추가 매수를 제안하지 않는다.
- **Limitation**: —

---

## Knowledge Gaps
- 위험자산 한도 규정 원문(시행령·감독규정), 예외 상품 범위, 초과 시 제한·페널티 — Corpus에 공식 원문 없음 → Operational Check.

## Source Notes
| Source | Section | Authority | 사용 |
|---|---|---|---|
| SRC-087 / SRC-003 | L68, L75–80 / L179–191, L368 | Public / Internal | K-001, K-003 |
| SRC-077 / SRC-081 | L18–44 / L26–38 | Operational (negative 포함) | K-002 |
| SRC-089 | L35 | Public | K-003 |
| SRC-069 / SRC-004 | L14–16 / L83–85 | Operational / Internal | K-005 |
| HD-2·2.1 / SRC-096 | — | Human-approved | K-006 |
