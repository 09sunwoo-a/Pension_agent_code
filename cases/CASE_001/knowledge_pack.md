# CASE_001 Knowledge Pack

```text
Case: CASE_001
Frozen Baseline: f986a94559dc13e5847650d0cd12094bba7c7ff5
Status: FROZEN
Frozen At: 2026-08-28
Approved By: Human
```

이 문서는 Frozen CASE_001을 실행하기 위해 Gemma 4에 공급하는 **Case-local Knowledge**다. 전체 IRP Knowledge Base가 아니며, CASE_001의 판단에 실제로 필요한 최소 지식만 담는다.

Basis Type 구분:

- **Source-derived** — Corpus 원문에서 직접 확인되는 Fact / 판단기준 / 설명. Location은 `sources/corpus/` 기준 파일과 줄 번호.
- **Human-approved** — Frozen `case.md`에서 Human이 확정한 Constraint / Case 의미. Source에서 확인한 것처럼 쓰지 않는다.
- **Case-local Interpretation** — Source Fact를 CASE_001에서 쓸 수 있도록 Agent가 정리한 해석. Source 원문이 아님을 항상 드러낸다.

이 Pack에는 CASE_001의 정답, 사전 판정, Customer → Action Rule, 상품 추천, 투자비중, Target Threshold를 포함하지 않는다. Frozen `case.md`의 Expected Behavior는 여기에 복사하지 않으며, 판단 경계는 `case.md`가 기준이다.

---

## Knowledge Questions (CASE_001 기준)

이 Pack이 지원해야 하는 질문이다. 고정 Schema가 아니다.

| # | 질문 | 대응 Item |
|---|---|---|
| Q1 | 현금성자산 상태를 어떻게 과도하게 해석하지 않을 것인가 | K-001, K-002 |
| Q2 | 무엇을 추가 확인해야 하는가 | K-002, K-003 |
| Q3 | 현재 정보에서 Management Need를 어디까지 판단할 수 있는가 | K-003, K-004, K-005 |
| Q4 | 투자성향 Hard Constraint가 어떻게 Solution Space를 제한하는가 | K-008 |
| Q5 | Solution을 어떤 유형 수준으로 표현할 수 있는가 | K-007 |
| Q6 | 마케팅·영업 목적 Source와 고객관리 판단을 어떻게 분리할 것인가 | K-009 |

---

## Knowledge Items

K-ID는 Traceability를 위해 초안 번호를 유지한다. K-006, K-010은 Human Review로 삭제·통합되어 결번이다.

### K-001. 현금성자산(고유계정대)이 무엇인지

- **Knowledge (Source-derived)**: 개인형IRP 계좌의 "고유계정대"는 상담 시 "현금성자산" 또는 "운용지시가 되지 않는 자산"으로 표현되는 자산이다. 행내 가이드는 고유계정대 과다 보유를 "수익률이 낮아질 가능성이 높은" 상태로 설명한다.
- **Source / Location**:
  - SRC-002 `…/연금고객_수익률KPI_고객관리_시나리오.md` L185 (용어 설명), L193 ("운용지시가 안된 현금성자산")
  - SRC-001 `…/개인형IRP_고객관리_가이드_Series1.md` L110 ("고유계정대 과다 보유로 인해 수익률이 낮아질 가능성이 높은 고객")
- **Authority / Status**: Internal / REVIEW_REQUIRED (SRC-001 As-of 2026-05, SRC-002 As-of Unknown)
- **Case Relevance**: CASE_001 Known의 "현금성자산(고유계정대) 75%"가 업무적으로 어떤 자산인지 정의한다. 관찰 상태를 해석하는 출발점.
- **Limitation**: SRC-001의 "수익률 저하 가능성"은 영업전략 자료의 일반 서술이며, 이 고객에게 실제 손실·불이익이 발생했다는 Fact가 아니다. 금리·수익률 수치 비교는 Frozen Out of Scope다.

### K-002. 현금성자산 존재만으로 미운용 상태를 확정하지 않는다

- **Knowledge (Source-derived)**: 행내 시나리오는 고유계정대에 현금성자산이 있더라도 곧바로 "미운용"으로 안내하지 않고, **거래내역 조회로 현금성자산 입금 사유(운용상품 매도 사유)를 확인**하여 "교체매매"나 "연금지급"처럼 정상적인 거래 과정에서 생긴 자금인지 먼저 구분하도록 한다. 즉 현금성자산이 존재한다는 사실과 그 자금이 미운용 상태라는 판단은 별개다.
- **Source / Location**: SRC-002 L178
- **Authority / Status**: Internal / As-of Unknown (문서 말미 관련문서 일자 2021.06.01, L318) / REVIEW_REQUIRED
- **Case Relevance**: CASE_001의 핵심 Reasoning Cue. 현금성자산 75%와 운용지시 부재라는 관찰 상태에서 "방치 / 미운용"으로 단정하지 않고, 거래 사유·자금 성격 등 추가 Context를 확인해야 한다는 판단 방향을 Source에 근거해 제공한다.
- **Case-local Interpretation**: CASE_001 Input에는 현금성자산 입금 사유·거래내역이 제공되지 않는다. 따라서 이 Source 기준으로도 "미운용"을 확정할 수 없으며, 입금 사유 확인은 추가 확인 사항이다.
- **Limitation (사용 범위 한정)**: 같은 문장은 "일정기간(1개월 이상) 금액변동 없이 유지"라는 조건도 함께 적는다. `1개월`은 과거 시나리오 문서에 존재하는 **참고 정보**일 뿐이며, CASE_001에서 Hard Constraint, 분류 Threshold, Runtime IF-THEN Rule, Management Need 확정기준 중 어느 것으로도 사용하지 않는다. 기준의 현재 유효성·공식 여부는 확인되지 않았다.

### K-003. 사용계획을 먼저 확인한 뒤 필요 시 운용 검토

- **Knowledge (Source-derived)**: 고유계정대 현금성자산 보유 고객에 대한 행내 상담 시나리오의 제목 원칙은 "**사용계획이 있는지 거래내역 등을 확인한 후 필요시 상품운용지시 권유하기**"다. 즉 운용 검토는 사용계획 확인 이후의 조건부 단계다. 같은 시나리오의 대화는 "운용지시가 안된 현금성자산이 000만원 있는데 **알고 계신가요?**"로 시작하며(고객의 상태 인지 여부 확인), "고유계정대"라는 용어는 고객에게 생소할 수 있으므로 "현금성자산" 등 이해하기 쉬운 표현을 쓰도록 한다.
- **Source / Location**: SRC-002 L174, L176 (확인 순서), L193 (인지 확인), L185 (용어)
- **Authority / Status**: Internal / As-of Unknown / REVIEW_REQUIRED
- **Case Relevance**: CASE_001의 Management Need 판단에서 "관리 필요 / 추가 확인 후 판단 / 현 상태 유지 가능"을 나누는 데 직접 필요한 Reasoning Knowledge. 확인 순서(상태 인지 → 사용계획 → 필요 시 운용 검토)와 Employee Brief의 표현 참고를 Source가 제시한다.
- **Case-local Interpretation**: CASE_001에서 자금 사용계획이 Unknown인 상태만으로 상품 변경 필요성을 확정해서는 안 된다. 사용계획이 확인되면(예: 단기 인출 예정) 현 상태 유지가 유효한 방향일 수 있다는 점을 Source 원칙이 열어둔다. 고객의 상태 인지 여부는 Unknown이며 확인 대상이다.
- **Limitation**: 같은 문서의 대화 예시(L186 이하)는 확인 직후 "금리가 높은 상품으로 운용하시면 좋을 거 같아요"라는 권유 화법으로 이어진다. 화법 부분은 영업 목적이 섞여 있으므로(K-009) Knowledge로 가져오지 않고, 확인 순서·인지 확인·표현 참고만 사용한다.

### K-004. 자금의 성격 → 투자기간 · 투자성향이 판단의 두 축

- **Knowledge (Source-derived)**: 직원교육 자료는 개인투자자(DC·IRP 가입자)의 운용 판단에서 "자금의 성격을 먼저 규정하고, 그에 따라 목표 수익률과 투자 기간을 확인하는 것"을 가장 중요한 출발점으로 두며, 상품 선택의 두 축으로 **연령(=투자기간)** 과 **투자성향(=원금 손실 감내 수준)** 을 제시한다.
- **Source / Location**: SRC-024 `…/02_투자교육/퇴직연금_투자가능상품_5종.md` L21 (대전제), L33–44 (축1 연령=투자기간), L46–51 (축2 투자성향)
- **Authority / Status**: Internal (스타런 직원교육 STT 전사) / As-of Unknown / REVIEW_REQUIRED
- **Case Relevance**: CASE_001의 Relevant Context(만 29세, 적립용, 연금 미개시)와 C1(위험중립형)이 판단에서 각각 어떤 역할(투자기간 / 손실 감내 경계)을 하는지 구분해 준다. 자금 사용계획이 Unknown이면 "자금의 성격" 자체가 미확정이라는 점도 여기서 나온다.
- **Limitation**: 같은 Source는 30세 예시에서 "변동성을 감내하고 수익률을 끌어올리는 것이 필요한 시기"(L39)라고 서술한다. 이는 교육 강사의 일반론이며, CASE_001에서는 Frozen 경계(연령을 이유로 공격적 운용 가정 금지)가 우선한다. 이 Pack에서는 "투자기간이 판단 요소"라는 점까지만 사용하고, 연령별 전략 권고는 사용하지 않는다.

### K-005. 디폴트옵션의 제한적 Context 의미

- **Knowledge (Source-derived)**: 디폴트옵션(사전지정운용제도)은 가입자가 운용 상품을 결정하지 않을 경우 **사전에 지정해 둔 상품**으로 일정 조건에서 자동 운용되는 제도이며, IRP 가입자는 원하는 디폴트옵션 상품을 직접 지정할 수 있다. 직접 운용이 어려운 경우의 대안으로 안내된다.
- **Source / Location**: SRC-089 `04_KBthink_연금/03_디폴트옵션_제도.md` L15 (뜻), L68 (IRP 가입자 지정); SRC-088 `04_KBthink_연금/02_퇴직연금_운용방법.md` L69 ("직접 운용이 어렵다면 디폴트옵션 활용")
- **Authority / Status**: Public (KB Think 페이지 정리본, 콘텐츠 작성 기준일 2026-07-07) / REVIEW_REQUIRED. 원문 문장을 그대로 옮기지 않은 정리본임(문서 L5).
- **Case Relevance**: CASE_001 Known "디폴트옵션 미등록"은 **자동운용 방식의 설정 여부를 이해하기 위한 Customer Context**다. 이 Item은 그 Context를 읽는 데 필요한 제도의 정의까지만 제공한다.
- **Case-local Interpretation**: 디폴트옵션 등록은 "운용 상품을 고민하지 않아도 되는" 자동운용 방식이라는 점에서 Solution **유형** 후보 중 하나가 될 수 있다. 그 이상 — 현재 현금성자산이 발생한 원인, 앞으로 현금성자산이 유지될 것이라는 예측, 미등록이 문제상태라는 판정, 등록이 정답 Solution이라는 판정 — 은 이 Item에서 도출되지 않는다.
- **Limitation**: 적용 조건·대기기간 등 제도 세부의 정확성은 Frozen Out of Scope이며 판단에 사용하지 않는다. 미등록 IRP에서 개인부담금 입금 자금이 어떻게 처리되는지는 Corpus에서 공식적으로 확인되지 않았으므로 이를 근거로 어떤 추정도 하지 않는다.

### K-007. 운용 방식 유형의 어휘 — 원리금보장형 / 실적배당형 / 자동운용

- **Knowledge (Source-derived)**: 퇴직연금 운용 상품은 크게 **원리금보장형**(원금과 이율 확정; 정기예금, 원리금보장형 ELB/DLB, 이율보증형 보험, 발행어음 등)과 **실적배당형**(운용 실적에 따라 변동, 원금 손실 가능; ETF, 공모펀드(TDF 등), 사모펀드 등)으로 구분되며, 직접 운용이 어려운 경우의 대안으로 디폴트옵션(자동운용)이 안내된다.
- **Source / Location**: SRC-088 L13–35 (상품 유형·비교표), L37–45 (상품 종류), L69 (디폴트옵션 활용)
- **Authority / Status**: Public / 콘텐츠 작성 기준일 2026-07-07 / REVIEW_REQUIRED
- **Case Relevance**: CASE_001에서 Solution을 **유형 수준**으로만 표현하기 위한 어휘를 제공한다(예: "원리금보장형 내 운용", "투자성향 범위 내 실적배당형 일부 검토", "자동운용 방식 검토").
- **Limitation**: 상품 예시 명칭은 유형 설명용이며, CASE_001에서 개별 상품명·비중을 제시하는 것은 Frozen Forbidden/Out of Scope다. 비교표의 "추천 대상" 열은 일반 설명이지 이 고객에 대한 판정이 아니다.

### K-008. C1 — 투자성향 Hard Constraint

- **Knowledge (Human-approved)**: 투자성향은 `안정형 < 안정추구형 < 위험중립형 < 적극투자형 < 공격투자형`의 5단계이며, Agent가 제안하는 Solution은 고객의 현재 투자성향과 **같거나 더 낮은 위험 수준**으로 제한한다. CASE_001 고객은 `위험중립형`(Known, 분석일 2026-07-05)이므로 적극투자형·공격투자형 수준의 방향은 Reasoning 이전에 제외하고, 최종 Validation에서 다시 확인한다.
- **Source / Location**: `cases/CASE_001/case.md` §4 C1 (Frozen, Human-approved)
- **Authority / Status**: **Human-approved Constraint**. **Source Gap: 공식 적합성 기준 Source 미확보** (case.md의 Source Gap Note를 그대로 보존한다).
- **참고 Fact (Source-derived, Constraint의 근거가 아님)**:
  - 투자성향 5단계 정의 — 위험중립형: "예적금보다 높은 수익을 위해 일정 수준의 손실 위험 감수" (SRC-088 L49–54)
  - KB국민은행 디폴트옵션 포트폴리오의 "가입 가능 투자성향" 표에서 위험중립형은 초저위험·저위험·중위험 포트폴리오에 가입 가능하고 고위험은 공격투자형만 가능 (SRC-089 L39–54). 이는 디폴트옵션 포트폴리오에 한정된 사실이며 일반 적합성 규칙이 아니다.
- **Case Relevance**: Pre-Reasoning Candidate Space 제한과 Post-Reasoning Validation의 기준.
- **Limitation**: 위 참고 Fact들로 C1이 Source-grounded된 것처럼 표현하지 않는다. 투자성향을 특정 위험자산 비중으로 변환하지 않는다(SRC-088 L56–62의 자산구성 표는 "예시"다). 개별 상품의 위험등급 판정은 Out of Scope.

### K-009. Source의 영업·마케팅 목적과 Customer Management 판단의 분리

- **Knowledge (Case-local Interpretation — Source Note에 근거)**: CASE_001과 관련된 행내 Source는 대부분 영업·이탈방어·KPI 목적으로 작성되었다. 이 문서들의 **대상 선정 기준, 이탈 통계, KPI 가중치, 권유 화법**은 Customer Management Need의 근거가 아니다. 반면 같은 문서 안의 **확인 순서·구분 기준**(K-002, K-003)은 관리 판단 지식으로 사용할 수 있다.
- **근거가 되는 Source 사실 (Source-derived)**:
  - SRC-001 L3: "본 자료는 당행의 영업전략과 관련된 내용이 수록" (문서 성격); L36: 고유계정대 50% 이상 보유 고객의 이탈위험도 1.3배(’25.11~’26.4 분석); L22·L116: 해당 고객 이탈 시 KPI 가중치 △1.65; L61–63: Target 리스트 기준(고유계정대 50% 이상 / 정기예금 100%, 총 적립금 1천만원 이상)
  - SRC-002 L1: 문서 제목이 "수익률 KPI 평가대상 고객관리 시나리오"
  - SRC-037 L21: 카드뉴스 제목 "현금성 대기자산이 많은 고객님은 떠나기가 쉬워요" (이탈방지 관점)
- **Authority / Status**: Internal / Experiential, 모두 REVIEW_REQUIRED
- **Case Relevance**: Frozen case.md §4 "Marketing Target 기준과 Management Need 판단 기준은 동일하지 않다"를 실행 시 적용하기 위한 구분 지식. Gemma 4가 "고유계정대 50% 이상 → 리밸런싱 대상"이라는 Source 구조를 그대로 옮기지 않도록 한다.
- **Limitation**: 이탈 통계(1.3배)는 집단 통계이며 이 고객의 이탈 가능성이나 관리 필요성을 말하지 않는다. Target 리스트 기준(1천만원 등)은 판단에 사용하지 않는다.

---

## Knowledge Gaps

현재 Frozen CASE_001 실행을 차단하거나 판단을 불가능하게 하는
Case-local Knowledge Gap은 확인되지 않았다.

단, C1의 공식 Source Traceability Gap은 K-008에 별도로 기록되어 있다.

---

## Source Notes

| Source ID | 사용한 Section | Authority / As-of / Status | 사용 방식 | 주의 |
|---|---|---|---|---|
| SRC-001 | L3, L22, L36, L61–63, L110, L116 | Internal / 2026-05 / REVIEW_REQUIRED | 고유계정대 정의 보조(K-001), 문서 성격·KPI·Target 기준의 존재 확인(K-009) | 영업전략 자료. 리밸런싱 권유·Target 기준·이탈 통계를 관리 필요성 근거로 쓰지 않음 |
| SRC-002 | L1, L174–178, L185, L193, L318 | Internal / Unknown (관련문서 2021) / REVIEW_REQUIRED | 미운용 미확정 Cue(K-002), 확인 순서·인지 확인·용어(K-003) | KPI 평가대상 시나리오. `1개월` 조건은 참고 정보이며 Rule/Threshold로 쓰지 않음. 대화 예시의 권유 화법은 사용하지 않음 |
| SRC-024 | L21, L33–51 | Internal (STT 전사) / Unknown / REVIEW_REQUIRED | 자금 성격·투자기간·투자성향 두 축(K-004) | 연령별 전략 권고(L39)는 Frozen 경계와 충돌 가능 → 사용하지 않음 |
| SRC-037 | L21 | Experiential / 2023-09-25 / REVIEW_REQUIRED | 문서 성격 확인(K-009) | 화법 자료. 노하우 ①~⑩의 내용은 사용하지 않음 |
| SRC-088 | L5, L13–45, L49–62, L69 | Public / 2026-07-07 / REVIEW_REQUIRED | 운용 방식 유형 어휘(K-007), 투자성향 정의 참고(K-008), 디폴트옵션 활용(K-005) | 정리본(원문 비복제). 자산구성 표는 예시 |
| SRC-089 | L5, L15, L39–54, L68 | Public / 2026-07-07 / REVIEW_REQUIRED | 디폴트옵션 정의·지정(K-005), 가입 가능 투자성향 참고(K-008) | 정리본. 적용 조건·대기기간·의무 여부 등 제도 세부는 사용하지 않음 |

검토했으나 사용하지 않은 Source: SRC-077 (위험자산 70% 한도 — Frozen Out of Scope), SRC-094/095 (현재 포트폴리오·추천펀드 — 상품 추천 Out of Scope), 기타 03 Hot Tip 게시글(화법·KPI 중심).

`references/planning/` XLSX는 Grounding Source가 아니므로 이 Pack의 Evidence로 인용하지 않았다.
