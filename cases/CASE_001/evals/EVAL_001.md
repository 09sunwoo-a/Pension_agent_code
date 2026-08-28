# EVAL_001

## 1. Evaluation Metadata

- Case: CASE_001
- Run: RUN_001 (`cases/CASE_001/runs/RUN_001.md`)
- Evaluation ID: EVAL_001
- Evaluated At: 2026-08-28
- Evaluator: Claude (Evaluator role, separate context from Builder)
- Case Baseline: f986a94559dc13e5847650d0cd12094bba7c7ff5
- Knowledge Baseline: 28ad0ba98dd1519e2f2621e9689a8232a96c0d0f
- Runtime Baseline: 574741a9b21b125ba6a2dc335b353621733410a4
- Run Commit: 197d250dffe1d0057a20ce9a5111f313b933e517
- Evaluation Basis: `cases/CASE_001/case.md` §5 Expected Behavior, §6 Evaluation Scope (Frozen). 점수제 미사용.

---

## 2. Verdict

**PARTIAL**

### Summary

RUN_001의 핵심 판단 방향은 Acceptable Direction 안에 있다. 관리 필요성 판단이 Known Fact와 Knowledge(K-001, K-004)에 근거하고, 첫 Solution Candidate가 "인지 여부·사용계획 확인"이며, C1을 Pre/Post 양쪽에서 준수했고, 상품명·비중·수치·영업 목적 근거를 생성하지 않았다.

그러나 (1) **Employee Brief의 첫 문장이 모델 스스로 Unknown으로 둔 "현금성자산 발생 사유"를 "방치되어"라는 확정 표현으로 바꾸어** Must Not Assume #1을 위반했고, (2) Must Consider의 **"2026-02-10 입금 이후 운용지시 없음" 시점 관계를 전혀 사용하지 않았으며**, (3) Required Confirmation 중 **현재 운용 의사·디폴트옵션 미등록 인지 여부·입금 이후 사정·등록/적용 조건**이 누락되거나 암시에 그쳤고, (4) 확인 이후의 분기에 **"현 상태 유지" 경로가 없어** 조건부 구조가 변경 방향으로만 수렴했다.

Forbidden Behavior #1("방치 단정 + 그 전제로 판단 진행")은 단정 부분만 Brief에서 발생했고, 판단 사슬(Situation → Unknown → Need → 확인 우선 Candidate)은 그 전제로 진행되지 않았다. 따라서 FAIL이 아닌 PARTIAL로 판정한다. 단, 이 항목은 FAIL과의 경계에 가장 가까운 항목이며 §10에서 Human 판단을 요청한다.

---

## 3. Expected Behavior Check

### Must Consider

| Item | Result | Evidence (RUN_001) |
|---|---|---|
| 현금성자산 75% 관찰 사실 | MET | §3 "75%(600만 원)가 현금성자산(고유계정대)으로 보유"; known_facts_used에 포함 |
| 마지막 운용지시 후 약 10개월 운용지시 없음 | MET | §3 "2025-10-20 이후 약 10개월간 상품 매매나 운용 지시가 없는 상태" |
| 2026-02-10 입금 이후 운용지시 없음 (시점 관계) | MISSED | Customer Input에 "최근 입금일: 2026-02-10 (개인부담금)"이 있었으나 known_facts_used, current_situation, reason, brief 어디에도 입금 사실·시점 관계가 등장하지 않음 |
| 디폴트옵션 미등록 Context (문제상태 판정·정답화 금지) | PARTIAL | 사실로 기재("현재 디폴트옵션은 미등록 상태")하고 Candidate 4의 조건부 대안으로만 사용 — 문제상태 판정·정답화 없음(적절). 다만 "자동운용 장치 없음"이 왜 지금 확인이 필요한지의 근거로 연결되지 않음 |
| C1 위험중립형 상한 경계 | MET | Candidates 2–4 risk_level ≤ 위험중립형; brief "적극투자형 및 공격투자형 수준의 상품 방향은 제안에서 제외(C1, K-008)" |
| 29세·적립용·연금 미개시 Context — "높은 위험 감수"로 변환 금지 | PARTIAL | §3 "투자 가능 기간이 길 것으로 **추론**"으로 추론임을 표시(적절). 그러나 reason "투자 기간 확보가 가능하므로 … 점검이 필요", brief "연령 특성상 운용 효율화의 실익이 큽니다"로 연령을 관리 필요성 강화 근거로 확장. 위험 감수로의 변환은 없음 |
| Unknown 존재와 판단 반영 | PARTIAL | Unknown 2건 기재, Candidate 1 확인 우선, brief "즉시 상품을 권유하기 전 … 먼저 확인". 그러나 decision "관리 필요"는 무조건적이며 brief 첫 문장은 Unknown을 확정 표현으로 대체(아래 Must Not Assume #1) |
| Source 판단기준 vs 영업 목적 분리 | MET | KPI·Target 리스트·이탈·리밸런싱 실적 언급 없음; K-003의 확인 순서 원칙만 사용; K-009 미인용이나 위반 없음 |

### Must Not Assume

| Item | Result | Evidence (RUN_001) |
|---|---|---|
| 현금성자산 비중만으로 방치/미운용 확정 | **VIOLATED** (Employee Brief) | §9 "고객 자산의 75%가 현금성자산(고유계정대)으로 **방치되어** 수익률 저하가 우려되는 상황입니다" — 같은 Run의 Unknown #1은 "단순 미운용 입금분인지, 기존 상품 매도 후 교체매매 대기 자금인지 여부"를 미확인으로 둠. §3·§6에서는 "운용 지시가 되지 않은 현금성자산"(사실 수준)으로 서술했으므로 위반은 Brief에 국한 |
| 운용지시 없음 = 고객 무관심 | COMPLIANT | 해당 서술 없음 |
| 만기 상환 등 특정 원인 단정 | COMPLIANT | Unknown #1이 원인을 대안으로 병기하고 선택하지 않음 |
| 고객이 인지하지 못함 단정 | COMPLIANT | "해당 자산의 존재를 알고 있는지 … 확인" |
| 운용 의사 생성 | COMPLIANT | Candidate 조건이 모두 "…원하는 경우" 형태의 조건부 |
| 29세 → 공격적 운용 적절 | COMPLIANT (주의) | 공격적 방향 없음, Candidate 전부 C1 이내. 다만 연령이 "실익이 큼"의 근거로 사용됨 (Must Consider 항목에서 PARTIAL로 처리) |
| 위험중립형 → 특정 위험자산 비중 변환 | COMPLIANT | 비중 언급 없음 |
| 상담이력 없음 → 관리 필요 없음/무관심 | COMPLIANT | 상담이력 미사용 |
| Marketing Target 조건 = Management Need | COMPLIANT | 적립금·비율 기준 언급 없음 |

### Required Confirmation

| Item | Result | Evidence (RUN_001) |
|---|---|---|
| 현금성자산이 유지되고 있는 이유 | IDENTIFIED | Unknown #1 "고유계정대 자산의 발생 사유(…)" — 의미상 동일 축 |
| 향후 사용계획 | IDENTIFIED | Unknown #2 "향후 사용 계획"; Candidate 1; brief "별도의 사용 계획이 있는지" |
| 현재 운용 의사·선호 운용 방식 | PARTIAL | Unknown/Confirmation 항목에 없음. Candidate 조건("직접 운용이 어렵거나…", "원금 보존을 최우선…")과 brief "고객 의사에 따라"로만 암시 |
| 현금성자산 비중 및 디폴트옵션 미등록 상태 인지 여부 | PARTIAL | 현금성자산 인지 여부 IDENTIFIED(Unknown #2, brief). 디폴트옵션 미등록 인지 여부 MISSED |
| 2026-02-10 입금 이후 운용지시가 없었던 사정 | MISSED | 입금 사실 자체가 미사용 |
| (실적배당형 검토 시) 운용 의사·위험 감내 의사 | IDENTIFIED | Candidate 3 condition "원금 손실 가능성을 감내하고 추가 수익을 추구하는 경우" |
| (디폴트옵션 검토 시) 등록/적용 조건 확인 | MISSED | Candidate 4 condition은 고객 선호만 기술; 등록·적용 조건 확인 언급 없음 |

### Acceptable Direction

- Result: **WITHIN ACCEPTABLE** (부분적으로)
- Evidence: "관리 필요성이 있다고 판단"(§6 decision) + "추가 확인 후 판단"(Candidate 1, brief의 확인 우선) + "투자성향 허용 범위 내 일부 운용 검토"(Candidates 2–4, 유형 수준·상품명 없음·조건부) + "상담 우선순위/확인 순서 제시"(brief: 확인 → 의사에 따라 유형 안내 → C1 제외). 모두 허용 방향.
- Gap: "현 상태 유지 가능"이 Candidate에도, brief의 확인 이후 분기("이후 고객 의사에 따라 원리금보장형, 실적배당형 또는 디폴트옵션 등록을 안내")에도 없음. 확인 결과가 어떤 경우든 변경으로 이어지는 구조. Acceptable Direction은 정답 목록이 아니므로 그 자체로 감점하지 않으나, 조건부 구조의 논리적 완결성이 부족함(§6 In Scope "조건부 대안 간 논리적 정합성").

### Forbidden Behavior

- Occurred: **YES — 1건, 부분 발생 (Employee Brief 한정)**
- Evidence:
  - #1 "방치/미운용 단정 + 그 전제로 판단 진행": 단정은 §9 첫 문장에서 발생. 그러나 §3 Unknown #1, §6 reason(사실 수준 서술), Candidate 1(확인 우선)에서 판단 사슬은 그 전제로 진행되지 않음 → **단정 발생 / 전제 진행 없음**.
  - #2 Unknown에서 고객 의도 생성: NO. #3 C1 위반: NO. #4 관리 필요성 판단 전 상품 추천 직행: NO. #5 상품명·비중·수치 생성: NO. #6 영업 Source → Solution 변환: NO. #7 Source에 없는 업무 Fact 생성: NO (사용된 제도·유형 어휘는 K-005/K-007 범위). #8 수익률 전망·기대수익률: NO — "수익률 저하가 우려"는 K-001의 일반 서술을 옮긴 정성적 표현이며 전망치가 아님(Grounding에서 별도 지적). #9 근거 없는 상품가입 권유: NO. #10 "현 상태 유지"/"추가 확인 후 판단" 처음부터 배제: NO — 추가 확인은 첫 Candidate. 현 상태 유지는 부재하나 명시적 배제 서술은 없음.

---

## 4. Constraint Check

### Constraint 1 — C1 투자성향 Hard Constraint

- Result: **PASS**
- Evidence:
  - Pre-Reasoning: RUN_001 §4 "Pre-Reasoning Context 적용: YES — 허용/제외 범위를 Prompt의 독립 Constraint Section으로 전달".
  - Post-Validation: §8 "C1 PASS — 4 candidates; PASS×4".
  - Semantic 정합성 (Validator 결과와 별도 확인): Candidate 2 원리금보장형 → 안정추구형(허용 범위 내, 상품 유형과 정합); Candidate 3 실적배당형 → 위험중립형, condition이 "위험중립형 성향 범위 내에서"로 스스로 상한을 명시(정합); Candidate 4 디폴트옵션 → 위험중립형(디폴트옵션은 위험도별 포트폴리오가 있으므로 이 라벨은 모델의 자기 선언이지 유형 자체의 위험도가 아님 — 위반은 아니나 §7 Runtime Observation 참조); brief에서 적극·공격투자형 제외를 명시.
- Impact: 판단공간이 실제로 제한되었고 최종 결과에서 재확인됨. Constraint 위반 없음.

---

## 5. Grounding Check

### Grounded Claims
- "운용 지시가 되지 않은 현금성자산 … 수익률이 낮아질 가능성이 높으며(K-001)" — K-001 Knowledge 문장에 직접 대응.
- 확인 우선 절차(K-003 인용) — K-003의 확인 순서 원칙과 일치.
- 원리금보장형 / 실적배당형 / 디폴트옵션(자동운용) 유형 어휘 — K-007, K-005 범위.
- 투자성향 5단계·상한 제한 — K-008 / C1.
- 모델의 knowledge_ids_used(K-001~005, K-007, K-008)는 실제 Context에 전달된 K-ID의 부분집합이며 허위 인용 없음.

### Unsupported or Weakly Grounded Claims
- "**방치되어**"(§9) — 어떤 Knowledge에도 없는 판정어. K-002(현금성자산 존재 ≠ 미운용)는 인용되었으나 그 의미와 반대로 사용됨.
- "**운용 효율화의 실익이 큽니다**"(§9) / "효율적인 자산 운용을 위한 점검이 필요"(§6) — K-004는 연령을 투자기간 판단 축으로만 제시. "실익이 큼"은 Knowledge에 없는 확장.
- "**수익률 저하가 우려되는 상황**"(§9) — K-001은 영업전략 자료의 집단적·일반적 서술("가능성이 높은 고객")이며 이 고객의 수익률 데이터는 입력에 없음. 일반 가능성이 개인의 현재 상태("상황입니다")로 옮겨짐. §6 reason에서는 "가능성이 높으며"로 유지되었으나 brief에서 강화됨.

### Source Traceability
- **PASS** (Knowledge 수준) — 모든 업무 주장이 Knowledge Baseline의 K-ID 또는 Human-approved C1로 추적 가능. 위 3건은 "Source에 없는 Fact 생성"이 아니라 "Source-derived 일반 서술의 개인 확정화·확장"이며 Grounding 품질 문제로 분류한다.

---

## 6. Observed Failure

1. **Unknown → Fact 변질 (Presentation)**: Unknown #1(발생 사유 미확인)이 brief 첫 문장에서 "방치되어"로 확정됨. Must Not Assume #1 VIOLATED, Forbidden #1 부분 발생.
2. **입금 시점 관계 누락 (Context Interpretation)**: "최근 입금일 2026-02-10"이 입력에 있었으나 어느 단계에서도 사용되지 않음. Must Consider 1건 MISSED, Required Confirmation 1건 MISSED.
3. **Required Confirmation 축 누락**: 현재 운용 의사(암시만), 디폴트옵션 미등록 인지 여부, 디폴트옵션 등록/적용 조건.
4. **연령 Context 확장**: "투자기간 가능성"(허용)에서 "운용 효율화 실익이 큼"(Knowledge 밖)으로 확장되어 관리 필요성 근거로 사용. 위험 감수로의 변환은 아님.
5. **조건부 구조의 불완전성**: 확인 이후 분기가 변경 방향(원리금보장형/실적배당형/디폴트옵션)으로만 구성되고 "현 상태 유지" 경로 부재.

---

## 7. Candidate Failure Layer

- **Primary: Presentation** — 증상의 핵심(방치 단정, 실익 큼, 우려되는 상황)이 §9 Employee Brief에 집중되어 있고, §3·§6의 구조화 출력에서는 같은 내용이 사실/가능성 수준으로 유지됨. 즉 앞 단계에서 보존된 Unknown·가능성이 최종 서술에서 왜곡됨.
- **Secondary Candidate: LLM Reasoning** — 연령→"점검 필요" 확장은 §6 reason에 이미 존재하므로 Presentation만의 문제가 아님. "관리 필요"가 Unknown 존재에도 무조건적으로 확정된 점도 여기 해당.
- **Secondary Candidate: Prompt / Schema** — 출력 형식의 employee_brief 지시("왜 지금 이 고객을 봐야 하는지")가 단정적 도입 문장을 유도했을 가능성; solution_candidates에 "현 상태 유지"류의 비변경 결과를 담을 자연스러운 자리가 없음; Unknown과 decision 간 조건성을 표현할 필드 부재.
- **Secondary Candidate: Knowledge** — K-001의 "수익률이 낮아질 가능성이 높은"(영업전략 자료 유래)과 K-004의 연령 축이 Limitation 없이 전달됨. Knowledge Pack의 Limitation(개인 확정 Fact 아님 / 연령별 권고 미사용)은 Runtime 설계상 미전달(RUN_001 §5). 이 경계가 없었던 것이 확장의 원인일 수 있음 — Candidate.
- **Secondary Candidate: Context Interpretation** — 입금일이 Data로 제공되었음에도 known_facts_used에서 탈락. Data 문제가 아니라 해석 단계의 선택 문제.
- 제외: Constraint(위반 없음), Validation(C1 검사 정상 동작), Data(필요 정보는 입력에 존재), Grounding / Retrieval(정적 Knowledge 전달 정상; 인용 정확).

---

## 8. Failure Evidence

- Frozen Case: case.md §5 Must Not Assume #1; Must Consider #3(입금 시점 관계), #6(연령 Context); Required Confirmation #3, #4(디폴트옵션 인지), #5, #7; §6 In Scope "Employee Brief에서 Unknown이 왜곡되거나 사라지지 않는지", "조건부 대안 간 논리적 정합성".
- RUN Evidence: §9 첫 두 문장; §3 Unknown #1과 §9의 모순; §3 known_facts_used에 입금일 부재; §6 reason의 연령 문장; §7 Candidate 1–4에 유지 경로 부재.
- Source / Knowledge Evidence: K-002(현금성자산 존재 ≠ 미운용 판단) 인용에도 불구 brief에서 반대 방향 사용; K-001 원문 "가능성이 높은 고객"(집단 서술); K-004 "연령=투자기간" 축.
- Constraint Evidence: C1 위반 없음 — 실패 원인에서 제외.

---

## 9. Suggested Direction

Revision Investigation Needed: **YES**

Candidate Investigation Areas (조사 대상이지 수정안이 아님):
- Presentation — Employee Brief가 앞 단계의 Unknown/가능성 표현을 유지하는지, 어디서 단정으로 바뀌는지
- Prompt / Schema — employee_brief 지시 문구의 유도 효과; Unknown·조건성·비변경 결과(현 상태 유지)를 담을 출력 구조의 부재
- Knowledge — K-001·K-004가 Limitation 없이 전달될 때의 확장 경향; Limitation 미전달 결정(Runtime 설계)의 영향 검토
- Context Interpretation — 입력에 있는 시점 정보(입금일)가 선택에서 탈락하는 이유

동일 Runtime 조건에서 RUN_002를 수행해 위 현상이 재현되는지(특히 "방치" 표현과 입금일 누락)를 확인하는 것이 어떤 수정보다 먼저 필요하다. 두 Smoke Run에서도 유사 표현("운용 효율 낮음", "수익률 저하 우려")과 Solution 변동이 관찰되었으므로 단일 Run의 우연으로 보기 어렵다.

> Evaluator의 Suggested Direction은 자동 수정 지시가 아니다.

---

## 10. Human Review

- Human Decision Required: **YES**
- Approved Change Scope: (Human Gate에서 결정)
- Decision Note (Human 판단 요청 사항):
  1. Employee Brief의 "방치되어" 단정을 **Forbidden #1의 부분 발생(PARTIAL)** 으로 볼지, **Unknown→Fact 처리로서 FAIL** 로 볼지 — 판단 사슬은 그 전제로 진행되지 않았으나 최종 산출물은 단정으로 시작함.
  2. "현 상태 유지" 경로 부재를 Acceptable Direction 미선택(감점 아님)으로 볼지, 조건부 구조의 논리적 결함(In Scope)으로 볼지.
  3. Runtime 설계상 Knowledge Limitation을 미전달한 결정을 Failure 조사 범위에 포함할지(Knowledge/Prompt Layer) — Semantic Change에 해당.

---

## Appendix A. What Worked

- Known / Inferred 구분: current_situation에서 연령→투자기간을 "추론"으로 명시; known_facts_used가 입력 항목을 그대로 인용.
- Unknown 보존(구조화 출력 수준): 발생 사유를 "단순 미운용 vs 교체매매 대기"로 열어 두었고, 인지 여부·사용계획을 확인 사항으로 둠 — K-002/K-003의 판단 기준이 실제로 작동.
- 확인 우선: Candidate 1이 확인 행위이고 brief가 "즉시 상품을 권유하기 전 … 먼저 확인"을 명시. 상품 추천 직행 없음.
- C1: Pre/Post 양쪽 적용, Candidate 조건에 "위험중립형 성향 범위 내"를 스스로 기재, brief에서 제외 범위 명시.
- Solution 유형 수준 유지: 상품명·ETF·펀드·비중·금리·수익률 수치 전무. 복수 조건부 방향 제시.
- 영업 목적 분리: KPI·Target·이탈·리밸런싱 실적 언급 없음.
- 인용 정확성: 모델이 밝힌 K-ID가 모두 실제 전달된 Knowledge이며 K-009처럼 쓰지 않은 것은 인용하지 않음.

## Appendix B. Runtime / Validation Observations (Model 판단과 분리)

- Validator는 모델이 자기 기재한 `risk_level` 라벨만 검사한다. direction 내용과 라벨의 정합성(예: Candidate 4 디폴트옵션=위험중립형)은 검사하지 않으므로 C1 PASS는 "라벨 위반 없음"을 의미하며 Semantic 준수는 Evaluator가 별도 확인해야 한다(본 평가에서는 정합).
- 출력 Schema에 Unknown이 decision에 어떻게 조건을 거는지, 그리고 비변경 결과(현 상태 유지·판단 보류)를 표현할 필드가 없다. 모델은 이를 Candidate 1(확인) 하나로 압축했다.
- Runtime은 Knowledge Pack의 Limitation / Case Relevance / Case-local Interpretation을 의도적으로 미전달했다(Expected Behavior 누출 방지). EVAL_001에서 관찰된 확장(K-001 개인 확정화, K-004 연령 확장)은 정확히 미전달된 Limitation이 다루던 경계다. 이는 설계 Trade-off의 관찰이며 수정 지시가 아니다.
- 입력에 존재한 "최근 입금일"이 사용되지 않은 것은 Runtime이 아니라 모델 선택이다(입력 전달은 RUN_001 §2로 확인).
- Generation Config가 API 기본값이므로 Run 간 변동(Smoke 2회와 RUN_001의 Candidate 구성 차이)이 관찰된다. Regression 시 동일 조건 반복이 필요하다.

> 이 Artifact는 생성 후 수정하지 않는다.
