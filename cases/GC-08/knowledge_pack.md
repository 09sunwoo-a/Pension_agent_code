# GC-08 Knowledge Pack

```text
Case: GC-08 / Status: FROZEN / Frozen At: 2026-09-01 / Approved By: Agent (HD-5)
```

---

## Knowledge Items

### K-001. 지금 변경 vs 만기 보유 — 중도해지 계산기로 비교 후 결정
- **Knowledge (Source-derived)**: 행내 가이드는 시중은행 정기예금 보유 고객에게 "[1] 만기가 얼마 남지 않은 고객: 만기 시점에 맞춰 다른 상품 운용 안내, [2] 운용 중인 상품 수익률이 낮은 고객: 고금리 원리금보장상품으로 변경 안내"를 제시하되, "지금 바로 상품을 변경하는 게 좋을지? 만기까지 보유하는 게 좋을지 고민될 때 '정기예금 중도해지 & 리밸런싱 계산기'를 활용"하라고 한다. 계산기는 [04-12-642] 연계메뉴에서 상품별 원리금·만기전이율·중도해지이율·만기가치 vs 중도해지평가액·리밸런싱 예상가치를 비교해 준다. 이탈방어 사전체크도 원리금보장형 상품의 "만기일, 중도해지 시 예상 손실금액"을 계산기로 확인하라고 한다.
- **Source / Location**: SRC-001 `…/개인형IRP_고객관리_가이드_Series1.md` L135–142; SRC-082 `…/2026-07-10_207088_WM고객수익률 관리 득점방법….md` L38–50 (계산기 화면 설명); SRC-003 L877–884
- **Authority / Status**: Internal Guide (2026-05) / Operational — 계산은 화면 확인
- **Case Relevance**: 8,000만 정기예금(2.4%, 잔여 8개월)을 이번 달 특별제공(3.3~3.6%)으로 바꿀지의 판단 절차. 손실이 크면 유지 + 만기 예약이 합리적.
- **Limitation**: SRC-082는 "정기예금 1천만원 매도 후 저축은행 변경"을 KPI 득점 목적으로 소개 — 근거로 쓰지 않는다. 손실액 수치는 생성하지 않는다.

### K-002. 원리금보장상품 특징 — GIC/ELB/저축은행, 월별 특별제공 한도·만기별 금리
- **Knowledge (Source-derived)**: GIC — 보험사, 예금자보호 대상, 비대면 가능, 최소금액 제한 없음; ELB — 증권사, 예금자보호 비대상, 비대면 불가, 최소 5천만원(상품 협의 등록). 특별제공 원리금보장상품은 매월 금리·제공 한도가 바뀌고 같은 기관이라도 만기에 따라 금리가 다르므로 [04-12-17A]에서 만기별 금리·잔여한도 확인. 예금자보호 한도는 2026 자료 기준 1억(구자료 5천만 — Source 충돌, 최신·공식 우선).
- **Source / Location**: SRC-001 L233–264, L304; SRC-089 L88; SRC-024 L76 (구자료)
- **Authority / Status**: Internal Guide 2026-05 / Public — Product Fact
- **Case Relevance**: 입력의 특별제공 3종 중 ELB(3년 3.6%)는 대면·비보호·5천만 조건; GIC 3년·저축은행 1년의 만기 길이 차이.
- **Limitation**: 금리는 as-of 2026.08 입력값이며 다음 달 변동. "실물이전 불가 상품 유도"(L248)는 사용하지 않는다.

### K-003. 만기 관리 — 자동 재예치 없음, 6주 후 DO, 만기 1개월 전 예약변경
- **Knowledge (Source-derived)**: 정기예금은 자동 재예치되지 않으며 만기 후 6주(4+2주) 무지시 시 등록된 디폴트옵션이 적용된다(이 고객은 지켜드림, 3년 정기예금). 만기 예약변경은 만기 한 달 전부터 가능. 행내 가이드는 "만기 1개월 전 반드시 만기 안내"를 요구한다.
- **Source / Location**: SRC-089 L36, L45, L82–83; SRC-002 L116; SRC-003 L790
- **Authority / Status**: Public / Internal
- **Case Relevance**: 유지 결정 시 만기(2027-04-10) 1개월 전 예약변경; 고유계정대 500만(7/15 만기상환, 6주 경과)은 지켜드림 적용 여부 확인.
- **Limitation**: —

### K-004. 연금 수령 계획과 만기 길이 — 투자기간은 수령 종료 시점까지, 유동성 확인
- **Knowledge (Source-derived)**: 연금을 나눠 받는 방식이면 투자가능기간은 수령 종료 시점까지로 재산정하되, 개시 시점에 필요한 유동성(첫 수령분)은 만기가 맞아야 한다. 연금수령방식은 기간지정·금액지정·자유인출 3종. 개시 후에는 그 계좌로 이전·추가입금 불가.
- **Source / Location**: SRC-020 L58–73; SRC-003 L258–264, L308; SRC-049 L11
- **Authority / Status**: Training / Internal / Operational
- **Case Relevance**: 2년 후(64세) 개시 계획 고객에게 3년제 GIC(만기 2029)를 권하기 전 "개시 시 필요 유동성·방식"을 확인해야 하는 근거.
- **Limitation**: 수령 한도·세제는 Out of Scope.

### K-005. 채널 — 내점, 컨설팅센터(예금→예금만), 전화센터
- **Knowledge (Source-derived)**: 내점이 어렵거나 비대면이 힘든 고객 중 저축은행 정기예금으로 교체매매 니즈가 있으면 [04-12-660] 상담연계등록으로 퇴직연금 자산관리 컨설팅센터에 요청할 수 있으나 "단말 업무는 정기예금→정기예금 변경만 가능(펀드 불가)". 전화센터 1599-0099도 정기예금·고유대 한정.
- **Source / Location**: SRC-002 L299–316; SRC-069 L14
- **Authority / Status**: Internal / Operational
- **Case Relevance**: 스타뱅킹이 어려운 고객의 실행 채널.
- **Limitation**: —

### K-006. C1·C2·C3 — 안정추구형
- **Knowledge (Human-approved)**: C1 허용 안정형·안정추구형. C2: 5~6등급만. C3: 지켜드림·알파드림. 성향은 상한이지 의무가 아님.
- **Source / Location**: HD-2·2.1; SRC-096
- **Authority / Status**: Human-approved
- **Limitation**: —

### K-007. KPI 목적 중도해지·특정상품 유도의 분리
- **Knowledge (Case-local Interpretation)**: "정기예금 중도해지 후 저축은행/TDF 변경"(KPI 득점), "실물이전 불가 상품 유도", 이탈 시 가중치 등은 고객 판단 근거가 아니다.
- **근거 Source**: SRC-082 L14–36; SRC-001 L71, L248
- **Authority / Status**: Marketing Practice
- **Limitation**: —

---

## Knowledge Gaps
- 정기예금 중도해지이율 산식 — 계산기 화면 확인.

## Source Notes
| Source | Section | Authority | 사용 |
|---|---|---|---|
| SRC-001 | L71, L135–142, L233–264, L248, L304, L790 | Internal 2026-05 | K-001, K-002, K-007 |
| SRC-082 | L14–50 | Operational (KPI) | K-001 화면, K-007 |
| SRC-089 / SRC-002 / SRC-003 | L36–88 / L116, L299–316 / L258–308, L790, L877–884 | Public / Internal | K-001, K-003, K-004, K-005 |
| SRC-020 / SRC-049 / SRC-069 | — | Training / Operational | K-004, K-005 |
| HD-2·2.1 | — | Human-approved | K-006 |
