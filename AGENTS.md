# AGENTS.md

## 1. Purpose

이 Repository는 **개인형IRP 사후관리 의사결정 Agent**를 Customer Case 기반으로 개발·검증하기 위한 작업공간이다.

이 문서는 IRP 업무지식을 정의하지 않는다. 이 문서의 목적은 Repository에서 작업하는 Coding Agent에게 다음을 규정하는 것이다.

- 무엇을 먼저 읽어야 하는가
- Case를 어떻게 정의하고 Freeze하는가
- Builder와 Evaluator가 어떻게 행동하는가
- 어떤 변경에 Human 승인이 필요한가
- Source와 Knowledge를 어떻게 다루는가
- Run과 Evaluation을 어떻게 기록하는가
- 어떤 Base LLM을 기준으로 개발·평가·개선하는가

업무지식, 상품 규칙, 고객별 판단 기준은 이 문서에 추가하지 않는다.

> Repository 운영방식은 현재 `AGENTS.md`를 기준으로 한다. `00_Core_Concept_Design.md`에 포함된 과거의 후속 문서구조나 Vertical Slice 예시는 설계 당시의 예시이며, 현재 Repository 구조나 CASE_001을 자동으로 확정하지 않는다.

---

## 2. Project Principle

Agent 개발은 Architecture를 먼저 완성하는 방식이 아니라 **Customer Case를 하나씩 해결하면서 필요한 구조를 발견하는 방식**으로 진행한다.

기본 개발 Loop:

```text
Case Draft
→ Human Framing
→ Case Freeze
→ Builder Run
→ Evaluation
→ Failure Analysis
→ Human-approved Revision
→ New Run
→ Regression
```

한 Case에서 발견된 문제를 곧바로 전역 Rule이나 Architecture로 일반화하지 않는다. 반복되는 Cross-case Evidence가 확인될 때만 공통 설계 변경을 검토한다.

---

## 3. Read Order

새로운 작업 세션은 Repository 전체를 재귀적으로 읽지 않는다.

```text
README.md
↓
00_Core_Concept_Design.md
↓
AGENTS.md
↓
Active Case가 있다면 cases/CASE_xxx/status.md
↓
cases/CASE_xxx/case.md
↓
필요한 최신 Run / Evaluation
```

Source Corpus는 작업 시작 시 전체를 읽지 않는다. Case에서 필요한 Knowledge가 확인된 이후에만 `sources/source_registry.md`에서 후보를 좁히고 필요한 Source / Section만 탐색한다.

---

## 4. Agent Autonomy

Agent는 다음을 자율적으로 수행할 수 있다.

- Repository 읽기 및 분석
- Case 후보 제안
- Case 초안 작성
- Expected Behavior 초안 작성
- 관련 Source 탐색
- Knowledge 후보 정리
- 승인된 Scope 내 구현
- Run 실행
- Artifact 및 Trace 기록
- Operational Fix
- 개선안 제안

단, Agent는 스스로 Case를 확정하거나 의미가 바뀌는 변경을 승인할 수 없다.

Active Case가 없다면 Agent는 다음 Case 후보를 제안할 수 있으나 Human 승인 없이 Case를 Freeze하거나 구현을 시작하지 않는다.

---

## 5. Human Question Rule

Agent는 모든 애매한 사항을 Human에게 질문하지 않는다.

답에 따라 다음 중 하나가 달라지는 경우에만 질문한다.

- Case의 의미
- Expected Behavior
- Source Authority
- Constraint
- Evaluation 기준
- 허용 가능한 Solution 범위
- Semantic Change 범위

파일명, 함수명, 코드 정리 방식, 동일 의미의 표현 선택 등 구현 세부사항은 가능한 한 Agent가 스스로 결정한다.

Human-approved Golden Batch 안에서는 Case Freeze · Knowledge Pack · Run · Evaluation · 다음 Case 진행 같은 **Step 별 확인을 요청하지 않는다** (§20). 이미 확정된 Human Decision(`golden/HUMAN_DECISIONS.md`)을 다시 질문하지 않는다.

---

## 6. Case Lifecycle

### 6.1 Before Freeze

Freeze 전에는 Case의 의미를 함께 정의한다.

Agent는 Customer Situation 초안 해석, Known / Unknown 구분, 필요한 Constraint 및 Source 후보 제안, Expected Behavior 초안 작성, 중요한 모호성 질문, Case 범위 축소 또는 확장 제안을 할 수 있다.

Freeze 전에는 Case 의미가 합의되지 않은 상태에서 Runtime 구현을 서두르지 않는다.

### 6.2 Case Freeze

Human이 다음을 승인하면 Case를 Frozen 상태로 본다.

- Case Meaning
- Customer Input
- Known / Unknown
- Applicable Constraints
- Expected Behavior
- Evaluation Scope

Expected Behavior는 정답 Solution이 아니라 **판단의 경계**를 정의한다.

- `Must Consider`
- `Must Not Assume`
- `Required Confirmation`
- `Acceptable Direction`
- `Forbidden Behavior`

### 6.3 After Freeze

Freeze 이후 Builder는 Frozen Case의 의미를 임의로 변경하지 않는다.

- Expected Behavior 변경 금지
- 새로운 고객 가정 추가 금지
- Unknown을 임의의 Fact로 변환 금지
- Constraint 임의 추가 또는 삭제 금지
- Case Scope 재해석 금지

Missing Information이 있어도 Frozen Semantics를 유지한 채 실행할 수 있다면 `Unknown` 또는 `Required Confirmation`으로 처리하고 계속 진행한다.

Frozen Semantics를 변경하지 않고는 실행 자체가 불가능한 경우에만 Human에게 질문한다.

---

## 7. Builder Responsibility

Builder의 역할은 Frozen Case를 가능한 최소 구현으로 실행하는 것이다.

```text
Customer Input
→ Context Interpretation
→ Constraint Application
→ Knowledge Grounding
→ Reasoning
→ Solution Resolution
→ Validation
→ Final Output
```

이 단계들은 Conceptual Flow이며 각각을 반드시 독립된 Agent, LLM Call 또는 LangGraph Node로 구현해야 한다는 의미가 아니다.

Builder는 현재 Case를 실행하는 데 필요한 최소 구조를 우선한다.

---

## 8. Evaluator Responsibility

Evaluator는 Builder와 역할을 분리한다. Golden Discovery Batch에서는 **Builder = Gemma 4, Evaluator = Claude** 이며 별도 Context에서 평가한다 (§17, §20).

Evaluator의 질문은 "더 좋은 Solution은 무엇인가"가 아니라 **"Golden Case가 요구하는 Semantic Boundary를 Builder가 준수했는가"** 다.

Evaluator는 Frozen Case, Expected Behavior, Applied Constraints, Used Knowledge / Source, Run Artifact를 비교한다.

### PASS
- Expected Behavior 충족
- Hard Constraint 위반 없음
- 핵심 판단이 Grounding되어 있음
- 중요한 Unknown을 임의로 Fact 처리하지 않음

### PARTIAL
- 핵심 판단 방향은 Acceptable Direction 안에 있음
- 일부 Must Consider, Required Confirmation 또는 Grounding이 누락됨

### FAIL
- Forbidden Behavior
- Hard Constraint 위반
- 근거 없는 핵심 판단
- 중요한 Unknown을 Fact로 처리
- 허용 범위를 벗어난 Solution
- 핵심 전제 또는 Context Interpretation 오류

점수제는 사용하지 않는다. **Low-quality Behavior만으로 FAIL을 주지 않는다.**

Evaluator는 직접 코드, Prompt, Knowledge 또는 Constraint를 수정하지 않는다. 수정이 필요하다고 판단되면 Failure Layer와 Suggested Direction만 기록한다.

Evaluation Artifact는 불필요하게 장문화하지 않는다. 최소한 `Verdict / Expected Judgment Check / Critical Mistake Check / Constraint Check / Grounding Check / Observed Failures / Failure Map Mapping / Evidence` 가 추적 가능하면 된다.

---

## 9. Change Authority

변경은 `Operational Change`와 `Semantic Change`로 구분한다.

### Operational Change

동일한 Frozen Case와 동일한 Input에서 판단 의미가 달라지지 않는 변경이다.

예: Syntax / Import / Path / Serialization 오류 수정, Typo, Formatting, Dead Code 제거, Behavior-preserving Refactoring.

Builder가 자율적으로 수정할 수 있다.

### Semantic Change

다음 질문에 `YES`라면 Semantic Change다.

> 동일한 Frozen Case와 동일한 Input에서 Agent의 판단, Grounding, 허용 Solution 또는 Final Output의 의미가 달라질 수 있는가?

대표 예:
- Prompt 의미 또는 Few-shot 변경
- Knowledge 추가 / 삭제 / 의미 변경
- Source Authority 변경
- Constraint 변경
- Retrieval 방식 또는 검색 범위 변경
- Customer Context 의미 변경
- Runtime 단계 책임 변경
- Validation 기준 변경
- Semantic Output Schema 변경
- Model 또는 Generation 설정 변경 (Gemma 4 Variant / Runtime Parameter 변경 포함)

Semantic Change는 Human 승인 없이 실행하지 않는다. 초기에는 애매하면 Human Gate를 거친다.

---

## 10. Revision Rule

```text
Evaluation
↓
Failure Analysis
↓
Human Review
↓
Approved Change Objective / Scope
↓
Builder Revision
↓
New Run
```

Human은 모든 코드 Line을 승인하는 것이 아니라 **변경 목적과 허용 범위**를 승인한다.

Builder는 승인된 Scope 안에서 구현 세부사항을 결정한다. 가능한 한 한 Revision에서는 하나의 coherent semantic concern만 변경한다.

---

## 11. Anti Prompt-Patching

Case 실패를 발견했다고 해서 즉시 Case-specific Prompt Rule을 추가하지 않는다.

Prompt 변경 전 다음을 검토한다.

1. 실제 Prompt Failure인가?
2. Data / Knowledge / Constraint / Runtime / Concept 문제를 Prompt로 숨기는 것은 아닌가?
3. 현재 Case 밖에서도 일반화 가능한 행동 원칙인가?
4. Knowledge, Constraint, Schema 또는 Runtime에 두는 편이 더 적절하지 않은가?

Prompt에는 가능한 한 일반적인 Reasoning Behavior만 둔다.

---

## 12. Source Usage

`sources/`는 Agent가 판단 근거를 찾기 위한 Source Corpus다. Source Corpus 자체는 정답 Rule Base가 아니다.

```text
Case
↓
필요한 Knowledge 식별
↓
source_registry.md 확인
↓
관련 Source 후보 선정
↓
필요한 원문 구간 탐색
↓
Case-local Knowledge 구성
```

원칙:
- Source Corpus 전체를 기본 Context로 로드하지 않는다.
- Source와 Agent의 해석을 구분한다.
- Source에 없는 업무 Fact를 임의로 생성하지 않는다.
- Source 간 충돌을 임의로 해소하지 않는다.
- Source의 Authority와 As-of를 고려한다.
- Source Authority 순서: `공식 법·제도·내규·시스템 기준 > 행내 공식 업무가이드/매뉴얼 > 영업점 Hot Tip / Field Know-how`.
- Hot Tip / Field Know-how는 **Operational Knowledge**(확인 순서·화면·채널·준비사항·현장 예외·커뮤니케이션)로 적극 활용하되, 단독으로 Hard Constraint · 법·제도 Constraint · 가입/실행 가능 여부를 확정하지 않는다. Hot Tip에만 있는 실행 제약은 `Operational Check Needed / Required Confirmation`으로 처리하고, 공식 Source 또는 시스템 기준에서 확인되면 Execution Constraint로 승격한다 (`golden/HUMAN_DECISIONS.md` HD-3).
- Source 충돌은 임의로 평균·통합하지 않고 공식성·최신성·적용범위로 판단하며 필요 시 `Source Conflict`로 기록한다.
- 실제 사용한 Knowledge는 원 Source까지 Trace 가능해야 한다.

Knowledge Schema, Knowledge Graph, Vector DB 등의 구조는 사전에 확정하지 않는다.

---

## 13. Knowledge Pack

Case에 필요한 Knowledge는 우선 Case-local `knowledge_pack.md`에 둔다.

포함 가능:
- 판단에 필요한 Fact
- Hard Constraint
- Reasoning Knowledge
- Field Know-how
- Source / Location
- Authority / As-of

포함 금지:
- Case-specific 정답 Solution
- 근거 없는 Customer → Action Rule
- Frozen Expected Behavior를 우회하기 위한 숨겨진 지침

공통 Knowledge 구조는 여러 Case에서 반복 사용되는 Pattern이 확인된 이후 검토한다.

---

## 14. Run Artifact

모든 Run은 Immutable Artifact로 저장한다. 기존 Run을 덮어쓰지 않는다.

Run은 private chain-of-thought를 저장하지 않는다. 대신 다음과 같은 관찰 가능한 구조화 결과를 저장한다.

1. Run Metadata
2. Customer Input
3. Interpreted Context
4. Applied Constraints
5. Used Knowledge + Source
6. Decision Output
7. Solution Candidates
8. Validation
9. Final Output

필요한 경우 `Parent Run`을 기록한다.

---

## 15. Evaluation Artifact

Evaluation 역시 Immutable하게 저장한다. 각 Evaluation은 특정 Run을 명시적으로 참조해야 한다.

최소 기록:
- Evaluation ID
- Case ID
- Run ID
- Verdict: PASS / PARTIAL / FAIL
- Expected Behavior Check
- Constraint Check
- Grounding Check
- Observed Failure
- Candidate Failure Layer
- Evidence
- Suggested Direction

Evaluator의 Suggested Direction은 제안일 뿐 자동 수정 지시가 아니다.

---

## 16. Core Design Authority

`00_Core_Concept_Design.md`는 현재 프로젝트의 Design Baseline이다. 단, 모든 내용이 확정 Architecture라는 의미는 아니다.

- `Design Principles`: 상대적으로 안정적인 원칙
- `Conceptual Hypotheses`: 검증이 필요한 개념적 가설
- `Implementation Hypotheses`: 구현 가설

Conceptual Hypothesis가 문서에 있다는 이유만으로 Runtime Node, Agent, DB Table, Rule 또는 Graph Node로 자동 구현하지 않는다.

Agent는 Core Design을 비판하거나 변경안을 제안할 수 있지만 Human 승인 없이 수정하지 않는다. 한 Case의 결과만으로 Core Design을 변경하지 않는다.

반복적인 Cross-case Evidence가 확인되면 Design Finding 후보로 제안한다. `DESIGN_FINDINGS.md` 같은 공통 Artifact는 실제 반복 Finding이 처음 발생할 때 생성한다.

---

## 17. Base LLM

### Target Model

본 Agent의 Base LLM은 **Gemma 4**이다.

- Gemma 4는 여러 LLM 후보 중 하나가 아니라 실제 Agent가 사용하는 **Target Runtime Model**이다.
- Coding Agent는 범용 LLM 최적화를 목표로 하지 않는다. 구현과 개선은 Gemma 4에서의 실제 동작을 기준으로 수행한다.
- 개발의 목적은 Gemma 4가 개인형IRP 사후관리 판단을 안정적이고 일관되게 수행할 수 있도록 Agent의 Context, Knowledge, Constraint, Prompt, Reasoning Flow, Validation, Runtime 구조를 Case 기반으로 발전시키는 것이다.

### Case-driven Improvement

Case 실행 결과 Gemma 4가 판단에 실패하더라도 다른 모델로 교체하여 문제를 회피하지 않는다.

먼저 기존 Failure Analysis 원칙에 따라 Candidate Failure Layer(Data, Context Interpretation, Constraint, Knowledge, Grounding / Retrieval, Concept Model, Prompt / Schema, LLM Reasoning, Solution Resolution, Validation, Presentation)를 점검한다. 그 다음 Gemma 4가 동일 유형의 판단을 더 안정적으로 수행할 수 있도록 **가장 작은 구조적 개선**을 검토한다.

### Model-aware Development

Gemma 4의 실제 수행 특성에 맞춰 다음을 조정하는 것은 허용한다.

- Context 표현
- Knowledge 표현
- Constraint 전달 방식
- Prompt 구조
- Output Schema
- Reasoning 단계
- Runtime 책임 분리
- Validation 구조

단, 특정 Case 하나의 정답을 맞히기 위한 Case-specific Prompt Patch나 예외 Rule은 추가하지 않는다 (11. Anti Prompt-Patching). 개선은 현재 Case 밖의 유사한 판단에서도 재사용 가능한 방향이어야 한다.

이러한 조정은 대부분 Semantic Change에 해당하므로 9. Change Authority의 Human Gate를 따른다.

### Builder / Evaluator

Golden Discovery Batch부터 **Builder = Gemma 4 (Target Runtime Model), Evaluator = Claude** 로 확정한다. Evaluator는 Builder와 별도 Context에서 Semantic Boundary 준수 여부만 평가한다 (8. Evaluator Responsibility). 기계적으로 검증 가능한 Hard Constraint(투자성향 ↔ 펀드 위험등급 / 디폴트옵션 Eligibility 등)는 Runtime에서 deterministic하게 검사한다 (§20.7).

### Regression

Semantic Change 이후에는 가능한 한 동일한 Gemma 4 Runtime 조건에서 다시 실행한다. 모델 자체가 바뀌어서 결과가 좋아진 것인지 Agent 구조 개선으로 좋아진 것인지 섞이지 않도록 한다.

Gemma 4의 Variant 또는 Runtime Parameter를 변경하는 경우 기존 Semantic Change 규칙을 적용하며, Human 승인 없이 실행하지 않는다.

---

## 18. Do Not

- Repository 전체 Source를 무조건 읽기
- 처음부터 Knowledge Base 전체 구축
- 처음부터 Knowledge Graph 설계
- Concept 하나당 Agent / Node 생성
- Customer State → Action 거대 Rule Base 구축
- Source 없는 Fact 생성
- Case-specific Prompt Patch
- Unknown을 임의로 Fact 처리
- Evaluator의 직접 코드 수정
- 기존 Run / Evaluation 덮어쓰기
- 한 Case의 결과를 전역 Rule로 일반화
- Human 승인 없는 Semantic Change
- Human 승인 없는 Core Design 변경
- Gemma 4의 판단 실패를 다른 모델로 교체하여 회피
- Human 승인 없는 Gemma 4 Variant / Runtime Parameter 변경
- Hot Tip / Field Know-how 단독으로 Hard Constraint · 실행 가능 여부 확정
- 확정된 Human Decision을 다시 `Human Review Needed`로 되돌리기
- Golden Batch 안에서 Step 별 승인을 Human에게 반복 요청

---

## 19. Default Working Principle

> **가장 작은 Case, 가장 작은 Knowledge, 가장 작은 구현으로 먼저 검증한다.**

> **Human은 업무의 경계와 중요한 변경을 결정한다. Agent는 승인된 경계 안에서 Case 개발·실행·평가를 자율적으로 반복한다.**

> **(Golden Discovery 단계) 한 Case의 실패를 바로 고치지 말고, 여러 Case에서 반복되는 Failure Evidence를 먼저 수집한다.**

Architecture는 Case를 설명하기 위해 존재한다. Case를 Architecture에 맞추지 않는다.

---

## 20. Golden Discovery Batch 운영

Golden Set(`golden/GOLDEN_SET_DRAFT.md`)의 Human-approved Case를 대상으로 하는 Batch 운영 규칙이다. 확정된 업무 Decision(연금·세제 Scope, 투자성향 Hard Constraint, Hot Tip Authority, Batch 범위)은 `golden/HUMAN_DECISIONS.md`에 있으며 여기서 반복하지 않는다.

### 20.1 범위

- 첫 Batch: **P0 8 Case** (GC-01, 03, 04, 06, 10, 12, 14, 16). CASE_001은 GC-00 Baseline으로 유지하며 재실행·재작성하지 않는다.
- 각 Case **1회 실행**. 재현성 검증·Regression은 Batch 종료 후 별도 수행한다.

### 20.2 Agent 자율 범위

Golden Draft에 정의되고 Human이 승인한 Case 의미 안에서 Agent는 다음을 Human 확인 없이 연속 수행한다.

```text
Golden Case Candidate → Case 구체화 → Known / Unknown → Expected Behavior 형식화
→ Source 후보 탐색 → 원문 확인 → Case-local Knowledge Pack → Case Freeze
→ Runtime Run → Evaluation → Failure Analysis
→ FAILURE_MAP / KNOWLEDGE_MAP / CONSTRAINT_MAP 갱신 → 다음 Case
```

### 20.3 Human Gate (이 경우에만 Human Review 요청)

- Golden Case의 핵심 Situation 변경 · Expected Good Judgment 방향 변경 · Critical Mistake 의미 변경
- 새로운 Hard Constraint 추가, 기존 Hard Constraint 삭제·완화
- Agent 업무 Scope 변경 · Case를 다른 업무문제로 재해석
- Core Design Semantic Change · Runtime Architecture의 의미 있는 Semantic Change

### 20.4 Stop Condition (즉시 중단 → Evidence 정리 → Human Review)

1. Hard Constraint 위반
2. 중대한 법·제도·업무 실행가능성 오류
3. 고객에게 중대한 불이익을 줄 가능성이 있는 Solution
4. Golden Case 자체의 Semantic Boundary가 잘못되었다는 Evidence
5. 현재 Source만으로 해결할 수 없는 중대한 Source Conflict

다음은 중단 사유가 아니다 — `Failure 기록 → Failure Map 연결 → 다음 Case`: 중요 Fact 일부 누락, Required Confirmation 누락, Grounding 부족, Employee Brief 표현 문제, Uncertainty Loss, Knowledge Over-application, 현상유지 경로 누락, Candidate 품질 부족, 실무성 낮음. `FAIL` 자체는 중단 사유가 아니다.

### 20.5 Failure Discovery 정책

Batch의 목표는 Case별 정답이 아니라 **Gemma 4의 반복 Failure Pattern 발견**이다. Case-specific Prompt Patch 금지(§11). 기본 흐름은 `Run → Evaluation → Failure Pattern 기록 → 다음 Case`. 둘 이상의 Case에서 같은 Pattern이 반복될 때만 `Cross-case Failure → Root Cause 후보 → Architecture Revision Proposal → Human Gate`로 올린다.

### 20.6 Golden Evaluation

Evaluation Source는 Golden Case의 `Expected Good Judgment / Critical Mistakes / Low-quality Behaviors`이며, Case 작성 시 `Must Consider / Must Not Assume / Required Confirmation / Acceptable Direction / Critical Mistake Check / Constraint Check / Grounding Check / Practical Usefulness`로 형식화한다.

- **PASS**: 핵심 판단방향 충족 · Critical Mistake 없음 · Hard Constraint 위반 없음 · 중요한 Fact / Confirmation 누락 없음
- **PARTIAL**: 핵심 방향 적절 · 일부 Confirmation / Grounding / Fact / 실무성 부족 · Low-quality Behavior 있으나 핵심 판단 유지
- **FAIL**: Critical Mistake · Hard Constraint 위반 · 핵심 판단방향 오류 · Case Semantic Boundary 밖의 판단

### 20.7 Deterministic Validation

기계적으로 검증 가능한 Hard Constraint(투자성향 ↔ 펀드 위험등급 Eligibility, 투자성향 ↔ 디폴트옵션 Eligibility 등)는 Runtime에서 deterministic하게 검사한다: `Gemma 4 Builder → Runtime deterministic validation → Claude Evaluator → Verdict`. 현재 구현으로 불가능한 부분은 Runtime Gap으로 기록하고, Batch 시작 시 필요한 최소 구현만 설계한다.

### 20.8 이번 Batch 전에 확정하지 않는 것

Output Schema 변경, Solution / Decision Outcome 분리, Execution Validation 구체 구현, Solution Conflict Validation 구조, 공통 Knowledge Base 구조, Reusable Knowledge 승격 정책, Dynamic Retrieval / RAG / Vector DB / Knowledge Graph, LangGraph / Multi-Agent, 자동 Evaluator Pipeline, 반복 실행·통계 평가 체계. 이들은 **P0 Batch의 Failure Evidence를 본 뒤** 결정한다. 문서에 Conceptual Hypothesis로 존재하는 것은 유지하되 확정 구현으로 승격하지 않는다.
