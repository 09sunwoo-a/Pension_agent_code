# GC-03 Knowledge Pack

```text
Case: GC-03 / Status: FROZEN / Frozen At: 2026-08-31 / Approved By: Agent (HD-5)
```

Case-local Knowledge. 정답·Customer→Action Rule 없음. Runtime은 `Knowledge`·`Authority / Status`만 전달.

---

## Knowledge Items

### K-001. 현금성자산 존재 ≠ 미운용 — 입금 사유와 사용계획 확인이 먼저

- **Knowledge (Source-derived)**: 행내 시나리오는 고유계정대 현금성자산이 "일정기간(1개월 이상) 금액변동 없이 유지" 되고 거래내역([04-12-644])의 입금 사유가 "교체매매"나 "연금지급"이 아닌 경우에 한해 미운용 자산이 있다고 안내하도록 한다. 또한 "퇴직금 인출 등 사용계획이 있는 현금성자산"은 운용지시 권유 대상에서 제외하며, 원칙은 "사용계획이 있는지 거래내역 등을 확인한 후 필요시 상품운용지시 권유"다.
- **Source / Location**: SRC-002 `…/연금고객_수익률KPI_고객관리_시나리오.md` L50, L174, L178
- **Authority / Status**: Internal / As-of Unknown / REVIEW_REQUIRED (Operational 성격)
- **Case Relevance**: 입금 7일차·입금사유 "과세이연/계약이전입금"인 GC-03은 이 기준상 미운용으로 볼 수 없다. `1개월`은 참고 정보이지 Threshold가 아니다.
- **Limitation**: 시나리오의 권유 화법·KPI 목적은 사용하지 않는다.

### K-002. 디폴트옵션 — 지정 의무, 등록된 경우에만 최초 입금 후 2주 적용

- **Knowledge (Source-derived)**: 디폴트옵션(사전지정운용제도)은 가입자가 운용 상품을 결정하지 않을 경우 **사전에 지정해 둔** 상품으로 자동 운용되는 제도다. 적용 케이스: 적립금을 처음 입금한 경우 입금 후 2주간 운용지시가 없으면 **지정한** 디폴트옵션 상품으로 자동 운용; 기존 상품 만기 후 6주; 옵트인은 즉시. 디폴트옵션 지정은 법적 의무사항으로 DC·IRP 가입자는 지정해야 한다. IRP 가입자는 본인이 원하는 상품을 자유롭게 지정할 수 있다(스타뱅킹 경로 존재). 지정된 상품이 없으면 자동 운용될 상품도 없다는 것이 제도 정의에서 따라 나온다.
- **Source / Location**: SRC-089 `04_KBthink_연금/03_디폴트옵션_제도.md` L15 (정의), L35–37 (적용 케이스), L66–70 (지정 방법), L74 (의무)
- **Authority / Status**: Public Explanation (정리본, 2026-07-07) / REVIEW_REQUIRED. 마지막 문장은 정의로부터의 Case-local Interpretation.
- **Case Relevance**: 미등록 고객의 현금성자산은 2주가 지나도 자동 운용되지 않는다. 지정 의무 안내는 제도안내(HD-1 Scope)이며 특정 포트폴리오 권유가 아니다.
- **Limitation**: 미등록 상태에서의 시스템 처리 세부는 Corpus에 명시 없음 — 추정하지 않는다.

### K-003. 연금개시 요건 — 55세 미만은 개시 불가, 퇴직급여 포함이면 가입기간 요건 없음

- **Knowledge (Source-derived)**: 연금 수령 자격은 ① 만 55세 이상, ② 연금계좌 가입일로부터 5년 이상 경과 두 가지를 모두 충족해야 하며, 퇴직급여가 포함된 경우에는 5년이 경과되지 않아도 만 55세 조건만 충족되면 즉시 연금 수령이 가능하다(퇴직용 IRP는 가입기간 제한 없음). 행내 가이드는 "퇴직금을 받은 고객이 만 55세 미만이면 아직 연금개시 요건을 충족하지 못했기 때문에 연금수령 개시를 할 수는 없으며, 지금 당장 퇴직소득세 절세가 어렵더라도 먼저 고객님의 자금 계획을 확인"하라고 한다.
- **Source / Location**: SRC-003 `…/개인형IRP_마케팅_보물지도_Vol1.md` L248–256, L705; SRC-049 `03_스타런_영업점_Hottip/posts/2025-02-27_199404_irp 연금 지급 절차.md` L16
- **Authority / Status**: Internal Guide 이론편 (2026-03) / Operational (Hot Tip) / REVIEW_REQUIRED
- **Case Relevance**: 53세 → 개시 불가. 자금 계획 확인이 첫 행동이라는 근거.
- **Limitation**: 수령 한도·연차·세율 계산은 GC-03 Out of Scope.

### K-004. 55세 전 인출은 해지 — 일시금 수령의 세금 구조 (계산 아님)

- **Knowledge (Source-derived)**: IRP 계좌를 해지하고 한 번에 수령(일시금)하면 퇴직금에 퇴직소득세가 전액 부과되고 운용수익에는 기타소득세 16.5%가 부과된다. 반면 만 55세 이후 연금으로 받으면 퇴직소득세가 감면(30~50%)되고 운용수익에는 연금소득세 3.3~5.5%가 적용된다. IRP 안에서 발생한 이자·배당·평가차익은 과세이연되어 재투자된다. 중도인출은 법정 사유(무주택자 주택구입/전세금·임차보증금, 6개월 이상 요양, 파산·개인회생, 천재지변 등)에 한해 가능하다.
- **Source / Location**: SRC-087 `04_KBthink_연금/01_IRP_개인형퇴직연금.md` L46–65 (일시금 vs 연금), L68–71 (과세이연), L87–88 (중도인출); SRC-003 L215–240 (중도인출 6사유·16.5%)
- **Authority / Status**: Public Explanation (심의필 콘텐츠 정리본, 2026-06-08) / Internal Guide / REVIEW_REQUIRED. 감면율 조건 세부는 원문 확인.
- **Case Relevance**: "55세 전에 써야 하는 돈인가"를 묻는 이유. 세액 계산은 하지 않는다(HD-1).
- **Limitation**: "최대 50%" 등 조건 없는 인용 금지. 이 Item은 구조 설명용.

### K-005. 과세이연 입금 후 환급 처리 전 지급·연금설계 제한

- **Knowledge (Source-derived)**: 퇴직금 과세이연 입금 절차상 "개인형IRP에 퇴직소득세가 환급되기 전까지는 개인형IRP 지급 및 연금설계 등록이 제한"된다. 과세이연 정보 등록·입금·환급 신청·정보 수정·환급세 입금의 단계가 있으며 담당 화면([06-12-501], [01-12-213], [04-12-648], [04-12-644])이 있다.
- **Source / Location**: SRC-003 L713–750 (CASE③ Step1~5), L748 (제한)
- **Authority / Status**: Internal Guide (2026-03) / REVIEW_REQUIRED — 절차는 Operational Check
- **Case Relevance**: 직원이 지급·설계 관련 안내 전 환급 처리 상태를 확인해야 함. DC 이전(계약이전입금)인 경우 절차가 다를 수 있으므로 "확인 대상"으로만.
- **Limitation**: 이 고객이 환급 대상인지는 입력에 없음 — 추정하지 않는다.

### K-006. 자금 성격 → 목표수익률·투자기간 → 성향 — 판단 순서

- **Knowledge (Source-derived)**: 운용 판단은 자금의 성격을 먼저 규정하고 목표 수익률과 투자기간을 확인하는 데서 출발한다. 연령은 투자기간과 관련되며, 55세 사례에서는 "자금 규모는 크고 운용 기간은 짧으므로" 변동성을 낮추고 안전하게 지키는 운용이 언급된다. 반면 연금으로 나눠 받을 계획이면 투자가능기간은 수령 종료 시점까지로 재산정하며, 나이만으로 안정형을 결정하지 않는다. 직접 운용이 어려운 경우의 대안으로 디폴트옵션·TDF 같은 위임형 유형이 안내된다.
- **Source / Location**: SRC-024 `…/퇴직연금_투자가능상품_5종.md` L21, L33–51; SRC-020 L58–73; SRC-088 L69
- **Authority / Status**: Training (STT) / Public / REVIEW_REQUIRED
- **Case Relevance**: 사용 시점(55세 전 vs 이후·연금)이 확정되어야 유형을 고를 수 있다는 근거. 유형 어휘(원리금보장/실적배당/위임형).
- **Limitation**: 연령별 상품 권고는 사용하지 않는다.

### K-007. C1·C3 — 위험중립형의 허용 범위

- **Knowledge (Human-approved)**: 투자성향 5단계 상한 원칙(C1). 성향은 상한이지 의무가 아니다. 디폴트옵션 가입 범위(C3): 위험중립형은 지켜드림·알파드림·뿔려드림 가능, 모두드림 불가.
- **Source / Location**: `golden/HUMAN_DECISIONS.md` HD-2; `cases/CONSTRAINT_MAP.md` C1·C3
- **Authority / Status**: Human-approved Business Fact
- **Case Relevance**: Pre/Post 경계.
- **Limitation**: —

### K-008. 퇴직금 입금 고객 Target·리밸런싱 실적 목적과 관리 판단의 분리

- **Knowledge (Case-local Interpretation — Source Note 근거)**: 영업점 타깃 요청서는 "퇴직금 입금 후 운용지시 여부/금액"을 KPI 평가대상 조건으로 반복 요청하고, 행내 가이드·TM 스크립트의 현금성자산 관리 활동은 수익률 KPI·이탈방어 목적이다. 이 분류·통계·가중치·"빨리 운용하시라" 화법은 관리 필요성의 근거가 아니며, 같은 문서의 확인 순서(K-001)·제도 설명만 사용한다.
- **근거 Source**: SRC-012 (타깃 요청서 — 퇴직금 입금·운용지시 여부 조건); SRC-001 L3, L71; SRC-007 시트25 L516–523 (현금성자산 7,500만↑ TM, "연금수령액이 적어질 수 있습니다" 화법)
- **Authority / Status**: Internal / Marketing Practice / REVIEW_REQUIRED
- **Case Relevance**: Gemma 4가 "퇴직금 입금 후 미운용 → 리밸런싱 대상"으로 옮기지 않도록.
- **Limitation**: —

---

## Knowledge Gaps
- 디폴트옵션 미등록 계좌의 시스템 처리 세부 — Corpus 미명시.
- DC→IRP 계약이전입금 시 환급 절차 적용 여부 — 확인 대상.

## Source Notes
| Source | Section | Authority | 사용 |
|---|---|---|---|
| SRC-002 | L50, L174, L178 | Internal / Operational | K-001 |
| SRC-089 | L15, L35–37, L66–74 | Public 정리본 | K-002 |
| SRC-003 | L215–240, L248–256, L705, L713–750 | Internal 이론편 2026-03 | K-003, K-004, K-005 |
| SRC-049 | L16 | Operational | K-003 |
| SRC-087 | L46–71, L87–88 | Public 심의필 정리본 | K-004 |
| SRC-024 / 020 / 088 | L21–51 / L58–73 / L69 | Training / Public | K-006 |
| HD-2 | — | Human-approved | K-007 |
| SRC-012 / 001 / 007 | — / L3, L71 / L516–523 | Marketing | K-008 |
