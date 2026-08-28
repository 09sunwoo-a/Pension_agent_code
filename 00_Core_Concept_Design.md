# 개인형IRP 사후관리 에이전트 — 개념 설계안 v0.4

> **목적**  
> 개인형IRP 사후관리에서 고객의 현재 상황을 이해하고, 반드시 지켜야 하는 제약 안에서 업무지식과 현장 노하우를 활용하여 적절한 관리판단과 실행 가능한 Solution을 구성하는 에이전트의 기본 구조를 정의한다.
>
> 본 문서는 최종 Knowledge Schema, Retrieval Architecture, LangGraph 구현구조 또는 완성된 업무 Ontology를 확정하기 위한 문서가 아니다.  
> 실제 Customer Case, Prototype, Knowledge Base 및 Runtime 실험을 시작하기 위한 **Core Design Baseline**이다.
>
> **상태:** v0.4 Core Design Baseline. 0~9장 정리 완료. Conceptual / Implementation Hypothesis는 실제 Case Test를 통해 검증 예정.

---

# 0. 문서의 역할과 설계 접근방식

현재 구조는 개인형IRP 업무 전체를 충분히 모델링하여 확정한 최종 설계가 아니다.

퇴직연금 관련 원천자료와 업무 특성을 바탕으로 구성한 **초기 의사결정 모델**이며, 실제 Customer Case와 Prototype을 통해 구조의 필요성과 경계를 검증·수정한다.

따라서 본 문서의 설계요소를 다음 세 수준으로 구분한다.

## Design Principle

현재 Agent를 발전시키더라도 가능한 한 유지해야 하는 기본 원칙이다.

예:

- 고객의 상황과 관리 필요성에서 출발하고 상품에서 출발하지 않는다.
- 법·제도·적합성 등 반드시 지켜야 하는 제약은 LLM의 자유로운 판단에 맡기지 않는다.
- 확인된 Fact와 시스템·LLM이 추론한 가능성을 구분한다.
- 특정 조건에 대한 고객별 정답을 Knowledge Base에 사전 정의하지 않는다.
- 최종 Solution은 실행가능성과 논리적 정합성을 검증한다.

## Conceptual Hypothesis

개인형IRP 사후관리의 판단과정을 설명하기 위해 현재 가설적으로 구분한 개념이다.

현재의 상위 구조는 다음과 같다.

```text
Customer Information
        ↓
Customer Context
        ↓
Management Decision
        ↓
Solution
```

각 영역 내부에는 다음과 같은 세부 개념이 필요할 수 있다고 가정한다.

```text
Customer Context
- Current Situation
- Relevant Context
- Known Intent / Preference
- Missing / Unconfirmed Information

Management Decision
- Management Issue
- Why Now / Priority
- Management Goal
- Management Strategy
- Required Confirmation
```

이러한 세부 개념은 고정된 순차 Workflow나 최종 Ontology가 아니다.

예를 들어 Situation과 Issue의 구분, Goal의 독립적 필요성, Strategy와 Solution의 경계, Customer Segment의 역할 등은 실제 Customer Case Test를 통해 유지·통합·제거할 수 있다.

## Implementation Hypothesis

현재 개념모델을 실제 시스템으로 구현하기 위한 기술적 선택은 아직 확정하지 않는다.

예:

```text
LLM Call 수와 Reasoner 분리 여부
Runtime Node / State 구조
Knowledge Representation
Knowledge Retrieval 방식
Structured Query 사용 여부
Prompt / Output Schema
Graph / Vector / DB 등 저장기술의 조합
```

이들은 Core Design을 충족하는 범위에서 실제 구현과 성능평가 과정 중 자유롭게 변경할 수 있다.

핵심 원칙은,

> **개념을 먼저 기술구조에 맞추지 않고, 실제 판단과정에서 필요한 구조를 검증한 뒤 구현방식을 선택하는 것**

이다.

## Target Base LLM

본 Agent의 Target Base LLM은 **Gemma 4**이다. Gemma 4는 비교 대상 후보 중 하나가 아니라 실제 Agent가 사용하는 Base LLM이다.

따라서 Case-driven iteration은 추상적인 범용 LLM을 가정하는 것이 아니라, Gemma 4의 실제 판단 특성 및 Failure Pattern을 관찰하면서 Context, Knowledge, Constraint, Reasoning, Validation 구조를 발전시키는 방식으로 수행한다.

단, 이는 위의 세 수준 구분을 바꾸지 않는다.

- Gemma 4를 사용한다고 해서 현재 Conceptual Flow를 곧바로 특정 Runtime Architecture로 확정하지 않는다.
- Gemma 4의 Failure가 관찰되었을 때 필요한 구조를 Case Evidence를 통해 발견한다.
- 모델 특성에 맞춘 최적화는 허용하지만 Case-specific Overfitting은 허용하지 않는다.
- Knowledge Graph, RAG, LangGraph, Multi-agent 등의 구현 선택을 Gemma 4라는 이유만으로 선결정하지 않는다.
- 어떤 구조가 필요한지는 실제 Case와 Failure Evidence를 통해 결정한다.

---

# 1. 문제 정의와 Agent Concept

개인형IRP 사후관리는 단순히 고객의 보유상품을 조회하고 더 높은 수익률의 상품을 추천하는 업무가 아니다.

동일한 계좌 상태라도 고객의 자금 성격, 투자기간, 투자성향, 연금수령 계획, 운용의사와 현재 발생한 상황에 따라 관리의 의미와 적절한 대응방향이 달라질 수 있다.

예를 들어 `현금성자산 비중이 높다`는 동일한 상태도 다음과 같이 다르게 해석될 수 있다.

```text
퇴직금이 최근 입금됨
→ 일시적 대기자금일 수 있음

장기간 운용지시 없음
→ 운용공백 가능성

교체매매가 진행 중
→ 정상적인 거래 과정일 수 있음

연금수령을 앞두고 있음
→ 계획된 유동성 확보일 수 있음
```

따라서 개인형IRP 사후관리에서 중요한 것은 관찰된 상태 자체가 아니라,

> **현재 고객에게 왜 이러한 상태가 나타났으며, 이 고객에게 지금 무엇을 관리해야 하고 어떤 방향으로 접근하는 것이 적절한지를 판단하는 것**

이다.

본 에이전트는 이를 지원하는 **개인형IRP 사후관리 의사결정 지원 에이전트**로 정의한다.

에이전트는 고객의 현재 상황과 맥락을 이해하고, 반드시 지켜야 하는 제약 안에서 관련 업무지식과 축적된 현장 노하우를 활용하여 다음을 판단한다.

- 지금 무엇을 관리해야 하는가?
- 어떤 방향과 우선순위로 접근하는 것이 적절한가?
- 실제 상담에서는 무엇을 먼저 확인하고 어떤 순서로 접근하는 것이 좋은가?

최종 목적은 특정 상품을 곧바로 추천하는 것이 아니라,

> **“이 고객에게 지금 무엇을 관리해야 하며, 어떤 방향과 순서로 접근하는 것이 적절한가?”**

에 대한 판단을 행원이 실제 고객관리에 활용할 수 있는 형태로 제공하는 것이다.

## 1.1 설계 방향

본 에이전트는 고객의 모든 상태 조합에 대해 정답을 사전에 정의하는 **Rule-only System**을 지향하지 않는다.

```text
Customer State
      ↓
Predefined Rule
      ↓
Action
```

반대로 고객정보와 관련 문서를 LLM에게 제공하고 모든 판단을 자유롭게 맡기는 **Pure LLM Agent**도 지향하지 않는다.

```text
Customer Data
      ↓
LLM
      ↓
Free-form Answer
```

본 설계는 그 중간에서 다음 원칙을 따른다.

> **업무지식과 현장 노하우는 고객을 판단할 때 무엇을 보고 어떻게 생각해야 하는지를 제공하고, Constraint는 판단이 넘어서는 안 되는 경계를 정의하며, LLM은 그 범위 안에서 고객별 상황에 적절한 관리방향을 구성한다.**

즉 본 에이전트가 지향하는 것은 **Knowledge-grounded, Constraint-controlled Decision Support Agent**다.

여기서 업무지식은 제도나 상품에 대한 Fact만을 의미하지 않는다.

개인형IRP를 관리하면서 현업에서 반복적으로 활용되는 다음과 같은 판단방법 역시 중요한 지식으로 본다.

```text
무엇을 먼저 확인하는가

어떤 요소를 함께 고려하는가

언제 개입하는 것이 적절한가

고객 반응에 따라 접근방향을 어떻게 조정하는가

어떤 순서로 설명하고 대안을 제시하는가
```

다만 이러한 현장 노하우 역시 고객별 정답을 사전에 지정하는 Rule로 사용하는 것이 아니라, **고객의 상황을 해석하고 실제 관리·상담 방향을 구성하기 위한 판단지식**으로 활용한다.

구체적인 판단과정과 내부 Decision Structure는 다음 장에서 **검증 가능한 초기 가설**로 정의한다.

---

# 2. Core Decision Model

본 에이전트는 고객 데이터에서 곧바로 관리방향이나 상품을 결정하지 않는다.

먼저 고객정보를 바탕으로 현재 상황과 판단에 필요한 맥락을 이해하고, 고객에게 반드시 적용되어야 하는 Hard Constraint를 Reasoning 전에 확인한다. 이후 허용 가능한 범위 안에서 현재 무엇을 관리해야 하며 어떤 방향으로 접근할지를 판단하고, 이를 실행 가능한 Solution으로 구체화한 뒤 다시 검증한다.

현재의 Core Decision Model은 다음과 같다.

```text
Customer Understanding
        ↓
Pre-Reasoning Control
        ↓
Management Reasoning
        ↓
Solution Resolution
        ↓
Post-Reasoning Validation
        ↓
Employee Brief
```

`Pre-Reasoning Control`과 `Post-Reasoning Validation`은 모두 **Decision Control**의 일부다.

즉 Decision Control은 한 번의 중간 단계가 아니라, Reasoning 전에 판단범위를 제한하고 Reasoning 이후 최종 결과를 다시 검증하는 통제구조다.

상위 흐름은 Agent가 수행해야 하는 기본 책임을 나타내며, 각 영역 내부의 세부 개념과 처리단계는 현재의 **Conceptual Hypothesis**다.

## 2.1 Customer Understanding

> **“현재 이 고객에게 무슨 일이 일어나고 있으며, 이를 판단하기 위해 어떤 맥락을 함께 봐야 하는가?”**

고객과 계좌에서 확인된 정보를 그대로 판단에 사용하는 것이 아니라, 다양한 고객정보를 종합해 현재 상황과 관련 맥락을 구성한다.

Customer Understanding의 구체적인 구조는 다음 장에서 정의한다.

## 2.2 Decision Control — Pre-Reasoning

> **“이 고객에게 애초에 허용되지 않는 판단이나 실행은 무엇인가?”**

투자성향, 법·제도, 계좌상태, 상품 가입조건 등 고객에게 반드시 적용되어야 하는 Hard Constraint를 Reasoning 전에 확인하여 판단 가능한 범위를 제한한다.

```text
Customer Context
       +
Hard Constraints
       ↓
Constraint Gate
       ↓
Constraint Result
       ↓
Management Reasoning
```

`Constraint Result`는 허용되는 범위, 금지되는 판단·실행, 추가로 충족해야 하는 조건 등을 표현할 수 있다.

이 결과로 제한된 Reasoning 범위를 개념적으로 `Allowed Decision Space`라고 볼 수 있으나, 이를 실제 별도 객체로 구현할지는 확정하지 않는다.

## 2.3 Management Reasoning

> **“허용 가능한 범위 안에서 이 고객에게 지금 무엇을 관리해야 하며 어떤 방향으로 접근해야 하는가?”**

Customer Context, Constraint Result 및 현재 판단에 필요한 업무지식과 현장 노하우를 종합하여 **Management Decision**을 구성한다.

```text
Customer Context
        +
Constraint Result
        +
Relevant Knowledge
        ↓
Management Reasoning
        ↓
Management Decision
```

현재 Management Decision에는 다음 요소가 필요할 수 있다고 가정한다.

```text
Management Issue
Why Now / Priority
Management Goal
Management Strategy
Required Confirmation
```

이 항목은 독립된 Runtime 단계나 순차적인 LLM Call을 의미하지 않는다.

Situation과 Issue의 구분, Goal의 독립적 필요성, Goal과 Strategy의 경계 등은 실제 Case Test를 통해 검증한다.

## 2.4 Solution Resolution

> **“판단된 관리방향을 실제로 어떤 수단을 통해 실행할 수 있는가?”**

Management Strategy가 결정되었다고 해서 특정 상품으로 곧바로 연결하지 않는다.

먼저 Strategy를 실행할 수 있는 Solution Candidate를 구성한 뒤, 필요한 경우 현재 이용 가능한 Product / Service를 연결한다.

```text
Management Strategy
        ↓
Solution Candidates
        ↓
Current Product / Service
```

상품과 서비스는 Reasoning의 출발점이 아니라 **판단된 관리방향을 실제로 실행하기 위한 수단**으로 위치시킨다.

## 2.5 Decision Control — Post-Reasoning Validation

> **“도출된 결과를 실제 고객에게 사용할 수 있는가?”**

Reasoning과 Solution Resolution을 통해 생성된 결과를 그대로 최종 결과로 사용하지 않는다.

최종적으로 다음 두 가지를 검증한다.

```text
① Execution Feasibility
   실제 실행 가능한가?

② Logical Consistency
   함께 제시된 대안들이 서로 충돌하지 않는가?
```

따라서 실행가능성과 Solution Set의 논리적 정합성을 확인한 후 유효한 결과만 Employee Brief에 전달한다.

## 2.6 Employee Brief

위 Decision Process의 결과는 단순 상품목록이 아니라 행원이 고객관리를 수행하기 위한 **의사결정 지원정보**로 제공한다.

최종적으로 다음과 같은 질문에 답할 수 있어야 한다.

```text
왜 이 고객을 지금 관리해야 하는가?

무엇을 관리해야 하는가?

어떤 방향으로 접근하는 것이 적절한가?

무엇을 추가로 확인해야 하는가?

어떤 대안을 검토할 수 있는가?

실제 상담에서는 어떤 순서로 접근하는 것이 좋은가?

어떤 제약과 유의사항이 있는가?
```

구체적인 Employee Brief Schema는 후속 Runtime Design에서 정의한다.

## 2.7 현재 Core Decision Model의 위치

본 장의 구조를 Runtime 관점에서 요약하면 다음과 같다.

```text
Understand
   ↓
Control
   ↓
Ground
   ↓
Reason
   ↓
Resolve
   ↓
Validate
   ↓
Present
```

여기서 `Ground`는 판단에 필요한 Relevant Knowledge를 공급하는 Runtime 책임이며, Knowledge Base의 저장·검색방식을 의미하지 않는다.

상위 책임은 초기 구현의 기준으로 사용하되, 그 내부의 세부 계층과 표현방식은 실제 고객 Case를 처리하면서 **판단 품질, 통제가능성, 설명가능성, 구현효율에 실질적인 가치를 제공하는지**를 기준으로 검증한다.

즉 현재 Core Decision Model은 완성된 업무 Ontology가 아니라,

> **개인형IRP 사후관리 판단과정을 실제로 구현하고 검증하기 위한 상위 구조와 초기 세부 가설**

로 사용한다.

---

# 3. Customer Understanding Model

Customer Understanding의 목적은 고객과 관련된 다양한 정보를 종합하여,

> **현재 고객에게 어떤 상황이 발생하고 있으며, 이후 판단에서 어떤 맥락을 중요하게 고려해야 하는지를 이해하는 것**

이다.

현재는 다음과 같은 단순한 구조를 기본으로 한다.

```text
Customer Information
        ↓
Context Interpretation
        ↓
Customer Context
```

Customer Understanding에서 가장 중요한 원칙은 **확인된 사실과 그 사실을 바탕으로 Agent가 추론한 가능성을 구분하는 것**이다.

```text
확인된 정보
현금성자산 비중 80%
최근 8개월간 운용지시 없음

        ↓ Context Interpretation

추론된 가능성
운용공백 가능성
```

추론된 가능성을 고객에게 확인된 사실처럼 취급하지 않는다.

## 3.1 Customer Information

Customer Information은 개인형IRP 계좌정보뿐 아니라 현재 고객의 상황을 이해하는 데 활용할 수 있는 관련 정보를 폭넓게 포함한다.

```text
Customer Information

├─ IRP Account
│   잔액, 보유상품, 비중, 수익률, 만기,
│   현금성자산, 최근 운용지시 등
│
├─ Customer Profile
│   연령, 투자성향, 투자경험,
│   연금수령 계획, 확인된 운용선호 등
│
├─ Financial / Investment Context
│   전체 투자상품 규모, 금융자산 구성,
│   타 투자계좌 및 상품 보유현황 등
│
├─ Behavior / Activity
│   ETF 매매, 비대면 거래,
│   상품매매 및 운용변경 행동 등
│
└─ Interaction History
    이전 상담기록, 고객 발화,
    과거 상담결과 및 확인된 의사 등
```

모든 Customer Information을 동일한 중요도로 사용하는 것은 아니다.

현재 판단과 관련 있는 정보를 선별하여 Context Interpretation에 활용한다.

또한 가능한 경우 정보의 **출처와 기준시점**, 그리고 해당 정보가 `Observed / Calculated / Customer-stated / Inferred` 중 어떤 성격인지 구분하여 관리한다.

## 3.2 Context Interpretation

Context Interpretation은 Customer Information을 종합하여,

> **현재 확인된 상태가 이 고객에게 어떤 의미를 가지는가**

를 해석하는 과정이다.

예를 들어 개인형IRP 계좌만 보면 원리금보장형 중심으로 장기간 운용변경이 없는 고객이라도,

```text
타 계좌에서 ETF를 지속적으로 매매하고 있음
+
비대면 투자거래에 익숙함
+
과거 상담에서 직접운용을 선호한다고 밝힘
```

이라는 정보가 함께 확인된다면,

```text
투자 자체에 소극적인 고객
```

이라고 단정하기보다,

```text
IRP 계좌가 상대적으로 관리되지 않고 있을 가능성
```

을 검토할 수 있다.

다만 행동이나 과거 이력을 고객의 현재 의사로 자동 변환하지 않는다.

```text
ETF 매매가 활발함
≠
IRP에서도 적극적으로 투자하고 싶음

전체 투자자산 규모가 큼
≠
IRP에서 높은 위험을 감수해도 됨

과거 직접운용 선호
≠
현재도 동일한 의사를 가지고 있음
```

이러한 정보는 고객의 의사나 적합성을 대신 결정하는 것이 아니라 **현재 상황을 더 정확하게 이해하기 위한 Contextual Evidence**로 활용한다.

## 3.3 Customer Context

Context Interpretation의 결과는 이후 Decision Control과 Management Reasoning에 필요한 **Customer Context**로 구성한다.

현재는 다음 정도의 구조를 가정한다.

```text
Customer Context

- Current Situation
- Relevant Context
- Known Intent / Preference
- Missing / Unconfirmed Information
```

### Current Situation

현재 고객에게 발생하고 있다고 판단되는 주요 상황이다.

예:

```text
장기 미관리
대기성 자금 존재 가능성
만기 도래 예정
퇴직자금 신규 유입
연금개시 준비
계약이전 고려
```

Situation은 직접 확인된 상태일 수도 있고 여러 정보를 바탕으로 추론한 가능성일 수도 있으므로 둘을 구분하여 관리한다.

### Relevant Context

현재 Situation의 의미와 이후 관리방향을 판단할 때 중요하게 고려해야 하는 정보다.

예:

```text
투자기간
자금 사용시점
투자성향
전체 투자경험
타 계좌 투자행동
직접운용 경험
과거 상담내용
```

기존 설계에서 `Decision Factor`라고 정의했던 개념은 별도의 계층으로 만들기보다, **현재 판단에서 중요하게 고려되는 Relevant Context**로 우선 다룬다.

### Known Intent / Preference

고객에게 직접 확인된 목적과 선호다.

행동정보 등을 통해 추정된 선호와 고객이 직접 밝힌 의사는 구분한다.

### Missing / Unconfirmed Information

판단에는 중요하지만 아직 확인되지 않은 정보다.

정보가 부족한 경우 임의로 추정하여 채우기보다 **추가 확인사항으로 남기는 것**을 기본 원칙으로 한다.

## 3.4 Customer Segment / Archetype

행내 가이드, 교육자료, 상담자료 등에는 반복적으로 특정한 고객군이 정의되어 있을 수 있다.

예:

```text
퇴직금 신규 입금 고객
현금성자산 과다 고객
장기 미운용 고객
만기 도래 고객
연금개시 예정 고객
계약이전 의향 고객
```

이러한 고객군은 Runtime에서 생성되는 Customer Context와 구분한다.

```text
Customer Context
= 현재 실제 고객의 정보를 종합하여
  Runtime에서 구성한 판단 맥락

Customer Segment / Archetype
= 기존 업무자료에서 정의되거나 반복적으로 발견되는
  대표적인 고객 상태·유형
```

Customer Segment / Archetype은 원천자료에서 발견할 경우 **보존할 가치가 있는 Knowledge Asset**으로 본다.

```text
Knowledge Assets
      │
      ├─ Customer Segment / Archetype
      ├─ Reasoning Knowledge
      └─ Field Know-how
              ↓
            GROUND
              ↓
      Relevant Knowledge
              ↓
     Management Reasoning
```

하나의 고객은 여러 Segment와 동시에 관련될 수 있으며, Agent가 고객을 특정 Segment 하나로 확정 분류할 필요는 없다.

또한 원천자료에 정의된 Segment의 조건을 그대로 고객별 정답이나 Action을 결정하는 Rule로 사용하지 않는다.

Segment는 현재 고객과 관련 있는 기존 업무지식과 현장 노하우를 찾는 **잠재적 Knowledge Anchor**로 활용할 수 있다.

다만 Segment가 실제 Grounding에 유용한지, 별도 구조로 관리할 필요가 있는지, Metadata나 자연어 Knowledge의 일부로 충분한지는 아직 확정하지 않는다.

구체적인 Schema, 저장방식, 판별기준 및 Retrieval 활용방식은 후속 Knowledge Design과 Case Test를 통해 결정한다.

## 3.5 핵심 원칙

Customer Understanding은 고객에 대해 가능한 한 많은 것을 추론하는 단계가 아니다.

핵심은,

> **다양한 고객정보를 활용하되 ‘확인된 사실’과 ‘그 사실로부터 추론한 가능성’을 구분하고, 현재 의사결정에 필요한 Customer Context를 구성하는 것**

이다.

따라서 다음 원칙을 따른다.

- IRP 계좌정보만으로 고객을 판단하지 않는다.
- 확인된 사실과 Agent의 추론을 구분한다.
- 행동과 과거 이력을 고객의 현재 의사로 단정하지 않는다.
- 현재 판단과 관련 있는 정보만 Context로 구성한다.
- 부족한 정보는 임의로 채우지 않고 확인사항으로 남긴다.
- 기존 자료의 Customer Segment는 정답 Rule이 아니라 관련 업무지식을 탐색하기 위한 Anchor로 활용한다.

---

# 4. Decision Control Model

Decision Control의 목적은 LLM의 판단을 사전과 사후에 통제하여,

> **고객에게 허용되지 않는 판단을 Reasoning 단계에서 배제하고, 최종적으로 도출된 결과가 실제로 실행 가능한지 다시 확인하는 것**

이다.

현재는 다음과 같은 구조를 기본으로 한다.

```text
                 Hard Constraints
                       │
              ┌────────┴────────┐
              ▼                 ▼
      Pre-Reasoning          Post-Reasoning
          Control              Validation
              │                 │
              ▼                 ▼
      판단범위 제한        최종 결과 검증
```

## 4.1 Hard Constraint

Hard Constraint는 고객에게 어떤 방향이 더 적절한지를 판단하기 위한 참고정보가 아니라,

> **어떤 판단이나 실행이 허용되지 않는지를 결정하는 경계**

다.

예:

```text
투자성향에 따른 허용범위
법·제도상 제한
계좌상태에 따른 거래제약
상품 가입조건
투자한도
연금개시 상태
현재 판매가능 여부
채널별 실행제약
```

하나의 고객정보가 Customer Context와 Constraint에 동시에 활용될 수 있다.

예를 들어 `투자성향`은

```text
투자성향 = 위험중립형
        │
        ├─ Customer Context
        │   → 어떤 운용방향이 더 적절한지 판단할 때 고려
        │
        └─ Hard Constraint
            → 허용되지 않는 위험수준의 상품·실행을 제한
```

처럼 서로 다른 역할을 가질 수 있다.

즉 Customer Context가 **무엇이 더 적절한가**를 판단하는 데 활용된다면, Hard Constraint는 **무엇이 가능한가 / 불가능한가**의 경계를 정의한다.

## 4.2 Pre-Reasoning Control

Hard Constraint는 Reasoning 결과를 마지막에 걸러내기 위한 사후 필터로만 사용하지 않는다.

Reasoning 전에 해당 고객에게 적용되는 Constraint를 먼저 확인하여 이후 판단에서 유효한 범위를 제한한다.

```text
Customer Context
      +
Hard Constraints
      ↓
Constraint Gate
      ↓
Constraint Result
      ↓
Management Reasoning
```

Constraint Result는 예를 들어 다음과 같은 정보를 포함할 수 있다.

```text
Allowed
- 검토 가능한 위험수준
- 허용 가능한 Solution 유형
- 현재 계좌에서 가능한 실행

Prohibited
- 투자성향을 초과하는 상품·운용방향
- 제도상 허용되지 않는 거래
- 현재 계좌상태에서 불가능한 실행

Required
- 실행 전에 추가로 충족하거나 확인해야 하는 조건
```

이러한 Constraint Result에 의해 제한된 이후의 Reasoning 범위를 개념적으로 **Allowed Decision Space**라고 볼 수 있다.

핵심 원칙은 다음과 같다.

> **허용되지 않는 판단을 LLM이 먼저 생성하도록 한 뒤 마지막에 제거하는 것이 아니라, 애초에 Reasoning에서 유효한 선택지로 취급하지 않도록 한다.**

이는 이후 Management Decision과 Solution이 고객에게 실제로 가능한 범위 안에서 일관되게 구성되도록 하기 위한 것이다.

## 4.3 Post-Reasoning Validation

Pre-Reasoning Control을 적용하더라도 Reasoning을 통해 생성된 결과를 그대로 최종 결과로 사용하지 않는다.

Strategy와 Solution이 구체화되는 과정에서 현재 상품조건, 실행방식, 복수 Solution의 조합 등으로 인해 추가적인 제약이나 충돌이 발생할 수 있기 때문이다.

따라서 최종 결과에 대해 다음 두 가지를 확인한다.

### Execution Feasibility

도출된 Solution이 실제로 실행 가능한지 확인한다.

예:

```text
투자성향상 가능한가?
법·제도상 가능한가?
현재 계좌상태에서 가능한가?
IRP에서 실행 가능한 방식인가?
현재 판매 가능한 상품·서비스인가?
해당 채널에서 실행 가능한가?
```

### Logical Consistency

개별 Solution이 각각 실행 가능하더라도 함께 제시했을 때 서로 모순되지 않는지 확인한다.

예를 들어,

```text
Solution A = 실행 가능
Solution B = 실행 가능

하지만

A와 B는 동시에 실행할 수 없음
또는
서로 다른 전제를 요구하는 상호배타적 대안
```

이라면 이를 하나의 실행방안처럼 동시에 제시하지 않는다.

필요한 경우 각각의 조건부 대안으로 구분하여 제시한다.

## 4.4 사전 통제와 사후 검증의 관계

Pre-Reasoning Control과 Post-Reasoning Validation은 서로 다른 목적을 가진다.

```text
Pre-Reasoning Control
→ 생각할 수 있는 범위를 제한

Post-Reasoning Validation
→ 생각한 결과가 실제로 사용할 수 있는지 확인
```

가능한 경우 두 단계에서 동일한 Constraint Knowledge를 재사용한다.

```text
               Constraint Knowledge
                    /        \
                   /          \
       Pre-Reasoning        Post-Reasoning
           Control            Validation
              ↓                   ↓
       판단범위 제한           결과 재검증
```

따라서 Constraint를 LLM Prompt 안의 주의사항으로만 제공하는 것이 아니라, **Runtime에서 명시적으로 적용되고 검증되는 통제장치**로 다루는 것을 기본 원칙으로 한다.

## 4.5 현재 구조의 위치

현재 Decision Control은 다음 두 단계의 구조를 기본 가설로 한다.

```text
Hard Constraints
       ↓
Pre-Reasoning Control
       ↓
Management Reasoning
       ↓
Solution Resolution
       ↓
Post-Reasoning Validation
```

다만 `Allowed Decision Space`, `Constraint Result` 등의 실제 데이터 구조와 각 Constraint의 적용방식은 후속 Runtime Design에서 구체화한다.

현재 단계에서 중요한 것은,

> **반드시 지켜야 하는 제약은 Reasoning 전에 판단범위를 제한하는 데 사용하고, Reasoning 이후에는 최종 결과의 실행가능성과 논리적 정합성을 다시 검증한다**

는 원칙이다.

---

# 5. Management Reasoning Model

Management Reasoning의 목적은 Customer Context와 Constraint를 바탕으로,

> **이 고객에게 지금 무엇을 관리해야 하며, 어떤 방향으로 접근하는 것이 적절한지를 판단하는 것**

이다.

Agent는 고객정보만으로 자유롭게 판단하지 않고, 현재 고객과 관련된 업무지식과 현장 노하우를 함께 활용한다.

```text
Customer Context
        +
Constraint Result
        +
Relevant Knowledge
        ↓
Management Reasoning
        ↓
Management Decision
```

여기서 `Management Reasoning`은 반드시 여러 단계의 LLM Call이나 독립된 Runtime Node를 의미하지 않는다.

현재는 고객관리 판단에 필요한 주요 요소를 하나의 **Management Decision**으로 구조화하고, 실제 테스트를 통해 필요한 세부 단계와 경계를 검증한다.

## 5.1 Management Decision

현재 Management Decision에는 다음과 같은 판단요소가 필요할 것으로 가정한다.

```text
Management Decision

- Management Issue
- Why Now / Priority
- Management Goal
- Management Strategy
- Required Confirmation
```

### Management Issue

> **현재 또는 가까운 미래에 무엇을 관리해야 하는가?**

예:

```text
운용공백
만기 후 재운용
운용구조 점검
연금수령 준비
인출구조 점검
고객 운용의사 재확인
```

Customer Situation 자체와 Management Issue가 실제로 별도의 개념으로 필요한지는 향후 Case Test를 통해 검증한다.

### Why Now / Priority

> **왜 지금 이 고객을 관리해야 하며, 여러 관리사항 중 무엇을 우선해야 하는가?**

예:

```text
상품 만기가 임박함
장기간 운용공백이 지속됨
퇴직금 신규 유입으로 운용결정이 필요함
연금개시 시점이 가까워짐
과거 상담 이후 고객상황이 변화함
```

단순히 관리할 사항을 나열하는 것이 아니라 실제 상담에서 우선순위를 판단할 수 있도록 한다.

### Management Goal

> **관리를 통해 어떤 상태로 만드는 것이 바람직한가?**

예:

```text
운용공백 해소
향후 운용방향 정립
만기 후 재운용 준비
운용구조 적정화
연금수령 준비
```

Management Goal이 독립적인 판단요소로 필요한지는 아직 확정하지 않는다.

실제 테스트에서 Goal이 Management Issue 또는 Strategy와 반복적으로 중복된다면 통합할 수 있다.

### Management Strategy

> **현재 고객에게 어떤 방식으로 접근하는 것이 적절한가?**

예:

```text
단기 필요자금을 우선 확보하고
잔여자금의 장기 운용방향을 검토

현재 안정성을 유지하면서
허용 가능한 범위 내에서 운용효율 개선

직접운용 부담을 고려하여
관리 편의성이 높은 운용방식 검토

전면적인 변경보다
단계적인 접근 우선 검토
```

Strategy는 특정 상품명을 지정하는 단계가 아니다.

실제 상품이나 서비스는 이후 `Solution Resolution` 단계에서 현재 실행 가능한 수단으로 연결한다.

### Required Confirmation

> **현재 판단을 확정하거나 다음 단계로 진행하기 전에 무엇을 추가로 확인해야 하는가?**

예:

```text
대기자금의 실제 사용계획
현재 운용의사
향후 투자기간
연금수령 계획
과거에 확인한 선호의 현재 유효성
```

Customer Understanding에서 발견된 Missing / Unconfirmed Information 가운데 현재 Management Decision에 중요한 내용을 연결한다.

정보가 부족한 경우 Agent가 임의로 가정하여 하나의 방향으로 확정하기보다, 필요한 확인사항을 명시하고 조건부 판단을 구성할 수 있어야 한다.

## 5.2 Reasoning Knowledge

Management Reasoning에는 개인형IRP 사후관리 과정에서 반복적으로 활용되는 **Reasoning Knowledge**를 사용한다.

Reasoning Knowledge는 특정 고객에게 적용할 정답을 저장하는 Rule이 아니라,

> **현재 고객을 판단할 때 무엇을 확인하고, 어떤 요소를 함께 고려하며, 어떤 원칙과 Trade-off를 적용해야 하는지를 제공하는 업무지식**

이다.

예를 들어 다음과 같은 Knowledge를 생각할 수 있다.

```text
[대기성 자금]

- 실제 미운용자금인지 확인한다.
- 일시적인 거래대기자금인지 확인한다.
- 향후 자금 사용계획을 확인한다.
- 현 상태 유지 시 발생할 수 있는 영향을 고려한다.
- 고객의 현재 운용의사를 확인한다.
```

이는 다음과 같은 정답 Rule과 구분한다.

```text
현금성자산 50% 이상
→ 상품변경 권유
```

Reasoning Knowledge는 고객별 결과를 미리 결정하는 것이 아니라 **LLM이 현재 고객을 판단하기 위한 사고의 재료와 방향을 제공한다.**

## 5.3 Field Know-how

Reasoning Knowledge에는 공식적인 업무 가이드뿐 아니라 실제 영업현장에서 반복적으로 축적된 판단 노하우도 포함할 수 있다.

예:

```text
무엇을 먼저 확인하는가
언제 고객에게 접근하는 것이 효과적인가
고객이 특정 대안에 부담을 느낄 때 어떤 다른 접근을 검토할 수 있는가
어떤 내용을 먼저 설명하고 어떤 순서로 대안을 제시하는가
고객 반응에 따라 상담방향을 어떻게 조정하는가
```

예를 들어 `전면적인 운용변경에 부담을 보이는 경우 → 부분 리밸런싱 제안`이라는 정답 Rule을 만드는 것이 아니라,

```text
고객의 실행부담이 높은 경우
현 상태 유지와 전면 변경만을 비교하지 않고
단계적이거나 가역적인 대안도 함께 고려한다.
```

와 같이 재사용 가능한 판단원칙으로 정제한다.

따라서 Field Know-how의 목적은 판매전략을 우선하여 고객을 설득하는 것이 아니라, 적절한 Management Decision을 실제 상담으로 연결하는 데 있다.

## 5.4 Customer Segment와 Reasoning Knowledge

기존 업무자료에서 추출한 Customer Segment / Archetype은 관련 Reasoning Knowledge를 찾는 하나의 Anchor로 활용할 수 있다.

```text
Customer Context
        ↓
Related Segment / Archetype
        ↓
Relevant Knowledge
        ↓
Management Reasoning
```

다만 Segment가 Management Decision을 직접 결정하지는 않는다.

동일한 Segment에 속하더라도 Customer Context와 Constraint가 다르면 서로 다른 판단이 나올 수 있다.

## 5.5 현재 구조에서 검증할 사항

현재 `Management Issue`, `Goal`, `Strategy` 등의 구분은 **Conceptual Hypothesis**다.

실제 고객 Case Test에서는 다음을 검증한다.

```text
Situation과 Management Issue를 별도로 구분할 필요가 있는가?
Management Goal이 독립적인 판단요소로 실질적인 역할을 하는가?
Goal과 Strategy가 반복적으로 같은 내용을 표현하지 않는가?
Why Now / Priority가 실제 고객관리 우선순위 결정에 도움이 되는가?
Required Confirmation을 명시하는 것이 과도한 추론을 줄이는 데 도움이 되는가?
Reasoning Knowledge가 판단의 일관성과 품질을 실제로 개선하는가?
Field Know-how가 관리방향 및 상담 접근방법을 개선하는가?
```

현재 단계에서는,

> **Management Reasoning을 `Issue → Goal → Strategy`라는 고정된 순차 Workflow로 확정하기보다, 고객에게 필요한 관리판단을 구조화하는 초기 Output Model로 사용한다.**

---

# 6. Solution Resolution

Solution Resolution의 목적은 Management Reasoning을 통해 도출된 관리방향을,

> **실제로 검토 가능한 실행수단으로 구체화하는 것**

이다.

본 설계에서는 Management Strategy에서 특정 상품으로 곧바로 이동하지 않고, 먼저 재사용 가능한 수준의 Solution을 구성한 뒤 현재 이용 가능한 Product / Service를 연결한다.

```text
Management Decision
        ↓
Management Strategy
        ↓
Solution Candidates
        ↓
Product / Service
        ↓
Post-Reasoning Validation
```

## 6.1 Solution의 역할

Management Strategy는 고객에게 어떤 방식으로 접근할 것인지를 표현하는 상위 수준의 판단이다.

반면 Solution은 해당 Strategy를 실제로 실행하기 위해 검토할 수 있는 수단이다.

```text
Strategy
= 어떤 방식으로 해결할 것인가

Solution
= 어떤 실행수단을 검토할 것인가
```

이 구분이 실제 판단 품질과 설명가능성에 도움이 되는지는 향후 Case Test를 통해 검증한다.

## 6.2 Solution Candidate

Solution Candidate는 현재 Management Strategy를 실행할 수 있는 복수의 대안이다.

예:

```text
현 상태 유지
재예치
원리금보장 내 개선
부분 리밸런싱
분산운용
자동운용 활용
직접운용
TDF 활용
ETF 활용
추가입금
연금개시
인출방식 조정
```

Solution은 항상 변경이나 판매를 의미하지 않는다.

고객의 상황에 따라 현 상태 유지, 만기까지 대기, 추가 정보 확인 후 판단 보류, 일부만 변경, 조건 충족 시 실행 등도 유효한 Solution이 될 수 있다.

## 6.3 Product / Service 연결

Solution이 결정되었다고 해서 임의의 상품을 연결하지 않는다.

실제 Product / Service는 현재 시점의 판매가능 여부, 상품조건, 계좌상태, 채널 등 실행조건을 반영하여 조회한다.

```text
Solution
   ↓
Current Product / Service
```

따라서 Product / Service 정보는 고객관리 판단의 출발점이라기보다,

> **판단된 Solution을 현재 시점에서 실제 실행 가능한 형태로 구체화하는 Dynamic Knowledge**

로 취급한다.

## 6.4 Solution과 Knowledge의 관계

Solution 역시 모든 고객조건에 대한 정답경로를 사전에 정의하는 Rule로 관리하지 않는다.

Knowledge에는 특정 Strategy를 실행할 수 있는 Solution 유형, Solution 검토조건, Solution 간 Trade-off, 실행 전 추가 확인사항 등을 축적할 수 있다.

## 6.5 Post-Reasoning Validation과의 관계

Solution Candidate가 생성된 뒤에는 4장에서 정의한 Post-Reasoning Validation을 적용한다.

```text
Solution Candidates
        ↓
Execution Feasibility
        +
Logical Consistency
        ↓
Validated Solutions
```

이를 통해 실제 실행할 수 없는 Solution, 고객 Constraint를 위반하는 Solution, 현재 상품·서비스 조건상 불가능한 Solution, 서로 충돌하는 Solution 조합을 제거하거나 조건부 대안으로 구분한다.

## 6.6 현재 구조에서 검증할 사항

실제 Case Test에서는 다음을 검증한다.

```text
Management Strategy와 Solution을 별도로 구분하는 것이 필요한가?
Solution의 추상화 수준은 적절한가?
현재 Product / Service 조회는 어느 시점에 수행하는 것이 적절한가?
복수 Solution Candidate를 생성하는 것이 판단 품질에 도움이 되는가?
현 상태 유지나 판단 보류 역시 Solution으로 명시할 필요가 있는가?
```

현재 단계에서는 Solution Taxonomy를 완전히 정의하지 않는다.

핵심 원칙은 다음과 같다.

> **관리방향에서 특정 상품으로 바로 이동하지 않고, 먼저 재사용 가능한 Solution 수준으로 실행방향을 구체화한 뒤 현재 이용 가능한 Product / Service를 연결한다.**

---

# 7. Runtime Architecture

Runtime Architecture의 목적은 앞에서 정의한 Customer Understanding, Decision Control, Management Reasoning, Solution Resolution을 실제 Agent 실행과정으로 연결하는 것이다.

다만 본 장에서는 LangGraph Node, LLM Call 수, Knowledge Graph, Vector DB 등 구체적인 구현방식을 확정하지 않는다.

> **Runtime에서는 Agent가 수행해야 하는 책임과 각 단계 사이의 Input / Output 관계를 정의하고, 구체적인 구현방식은 실제 Prototype과 Test를 통해 결정한다.**

현재는 다음과 같은 Runtime Flow를 기본 구조로 한다.

```text
Customer Information
        ↓
     UNDERSTAND
        ↓
Customer Context
        ↓
      CONTROL
        ↓
Constraint Result
        ↓
       GROUND
        ↓
Relevant Knowledge
        ↓
       REASON
        ↓
Management Decision
        ↓
      RESOLVE
        ↓
Solution Candidates
        ↓
      VALIDATE
        ↓
Validated Solutions
        ↓
      PRESENT
        ↓
Employee Brief
```

## 7.1 UNDERSTAND

> **고객정보를 현재 판단에 필요한 Customer Context로 구성한다.**

Input은 Customer Information, Output은 Customer Context다.

UNDERSTAND 단계에서는 특히 **확인된 정보와 해당 정보로부터 추론한 가능성을 구분한다.**

## 7.2 CONTROL

> **현재 고객에게 허용되지 않는 판단범위를 Reasoning 전에 제한한다.**

Customer Context와 Applicable Constraints를 입력받아 Constraint Result를 만든다.

법·제도, 투자성향, 계좌상태, 상품 및 거래조건 등 명확한 Constraint는 원칙적으로 LLM의 자유로운 판단보다 Deterministic / Structured Logic을 통해 적용한다.

## 7.3 GROUND

> **현재 고객을 판단하는 데 필요한 업무지식과 현장 노하우를 제공한다.**

Customer Context와 현재 판단 목적을 입력받아 Relevant Knowledge를 제공한다.

중요한 것은 **Runtime이 Knowledge Base의 물리적 구조를 전제하지 않는다는 점**이다.

Runtime에서는 `Relevant Knowledge`라는 Contract만 정의하며 Semantic Retrieval, Structured Query, Knowledge Graph, Metadata Lookup 또는 다른 Knowledge Representation 중 어떤 방식을 사용할지는 후속 설계에서 결정한다.

## 7.4 REASON

> **Customer Context, Constraint 및 Relevant Knowledge를 바탕으로 현재 고객에게 필요한 관리판단을 구성한다.**

Output은 Management Decision이다.

현재 Management Decision에는 Management Issue, Why Now / Priority, Management Goal, Management Strategy, Required Confirmation 등이 포함될 수 있다고 가정한다.

다만 이 항목들이 각각 별도의 Reasoning 단계 또는 LLM Call을 의미하는 것은 아니다.

## 7.5 RESOLVE

> **Management Decision을 실제 검토할 수 있는 Solution Candidate로 구체화한다.**

Management Strategy에서 특정 상품으로 곧바로 이동하지 않고 먼저 Solution 수준의 실행대안을 구성한다.

## 7.6 VALIDATE

> **생성된 Solution이 실제로 사용 가능한지 최종 검증한다.**

Execution Feasibility와 Logical Consistency를 확인하여 Validated Solutions를 만든다.

## 7.7 PRESENT

> **검증된 판단결과를 행원이 실제 고객관리에 활용할 수 있는 형태로 구성한다.**

Output은 Employee Brief다.

## 7.8 LLM과 Deterministic Logic의 역할

| Runtime Responsibility | 기본 처리방향 |
|---|---|
| UNDERSTAND | Structured Logic + 필요 시 LLM |
| CONTROL | Deterministic / Structured 중심 |
| GROUND | Knowledge Provider |
| REASON | LLM 중심 |
| RESOLVE | Knowledge / Structured Logic + 필요 시 LLM |
| VALIDATE | Deterministic / Structured 중심 |
| PRESENT | LLM 중심 |

정확한 계산, 상품 판매여부, 명확한 수치조건, 법·제도상 가능 여부, 투자성향에 따른 가입 가능범위 및 상품·채널 실행조건 등은 LLM이 직접 판단하지 않는 것을 원칙으로 한다.

반면 여러 고객정보의 의미 종합, Management Issue와 우선순위 판단, Relevant Knowledge의 맥락적 적용, Management Strategy 및 상담 접근순서 구성 등은 LLM을 활용할 수 있다.

## 7.9 Runtime State와 Trace

실제 Test와 설계개선을 위해 최소한 다음 정보는 Trace로 남길 수 있도록 한다.

```text
Input Customer Information
Generated Customer Context
Applied Constraints
Provided Knowledge
Management Decision
Solution Candidates
Validation Result
Employee Brief
```

Trace의 목적은 LLM의 내부 사고과정을 저장하는 것이 아니라,

> **최종 결과가 어떤 데이터, Constraint, Knowledge 및 중간 판단을 통해 만들어졌는지를 검증 가능한 수준으로 남기는 것**

이다.

## 7.10 구현 원칙

### Concept Model과 Runtime Node를 1:1로 연결하지 않는다

개념적으로 구분된 요소가 반드시 독립된 LLM Call이나 Node를 의미하지 않는다.

초기에는 가능한 한 단순한 Runtime으로 구현하고, Test에서 필요성이 확인된 경우에만 분리한다.

### Knowledge Base 구조를 Runtime에서 전제하지 않는다

Runtime이 요구하는 것은 **현재 고객을 판단하는 데 필요한 Relevant Knowledge**이며 특정 Graph, Vector DB 또는 Schema가 아니다.

따라서 Knowledge Base는 Runtime과 독립적으로 재설계할 수 있어야 한다.

### 최소 구조에서 시작한다

초기 Prototype에서는 전체 Knowledge Base와 Retrieval System을 먼저 구축하지 않아도 된다.

대표 Customer Case에 대해 필요한 Knowledge를 수작업으로 구성한 **Knowledge Pack**을 입력하여 Management Reasoning 자체를 먼저 검증할 수 있다.

```text
Customer Context
+
Constraint
+
Hand-curated Knowledge Pack
        ↓
Management Reasoning
```

## 7.11 현재 검증할 사항

Runtime의 세부 구현은 실제 Prototype을 통해 검증한다.

특히 UNDERSTAND에서 LLM이 필요한지, Customer Context의 명시적 생성이 유용한지, GROUND에 실제로 어떤 Knowledge가 필요한지, 하나의 Management Reasoner로 충분한지, Retrieval의 횟수와 시점, Validation 범위, Trace 범위를 확인한다.

따라서 본 Runtime Architecture는 완성된 구현설계가 아니라,

> **Customer Context와 Constraint, 필요한 Knowledge를 바탕으로 관리판단을 생성하고 검증한다는 Agent의 실행 Contract**

로 사용한다.

---

# 8. Knowledge Requirements

본 Agent가 안정적으로 Management Reasoning을 수행하기 위해서는 단순한 상품정보나 규정정보만으로는 충분하지 않다.

현재 고객의 상황을 해석하고, 반드시 지켜야 하는 경계를 적용하며, 적절한 관리방향과 실행수단을 구성하기 위해 서로 다른 성격의 Knowledge가 필요하다.

다만 본 장에서는 Knowledge Base의 Schema, 저장방식, Graph 구조 또는 Retrieval 방식을 확정하지 않는다.

> **현재 단계에서는 “Agent가 어떤 종류의 Knowledge를 필요로 하는가”를 정의하고, 이를 어떤 형태로 표현·저장·검색할지는 실제 Prototype과 Test를 통해 후속 설계한다.**

## 8.1 Knowledge의 역할

Runtime의 `GROUND` 단계에서는 현재 Customer Context와 판단 목적에 맞는 **Relevant Knowledge**를 제공해야 한다.

Relevant Knowledge의 역할은 고객별 정답을 미리 제공하는 것이 아니라, 무엇을 확인해야 하는지, 어떤 요소를 함께 고려해야 하는지, 어떤 판단원칙과 Trade-off가 있는지, 무엇이 허용·금지되는지, 어떤 실행수단과 현장 접근을 검토할 수 있는지를 제공하는 것이다.

## 8.2 Agent가 요구하는 Knowledge

### Reasoning Knowledge

고객상황을 해석하고 Management Decision을 구성할 때 필요한 판단지식이다.

Reasoning Knowledge는 `조건 → 정답`을 지정하기 위한 Rule이 아니라,

> **현재 고객을 판단할 때 무엇을 보고 어떻게 생각할지를 제공하는 지식**

으로 사용한다.

### Constraint Knowledge

Agent의 판단과 실행이 넘어설 수 없는 경계를 정의하는 Knowledge다.

투자성향, 법·제도, 계좌상태, 상품조건, 투자한도, 판매가능 여부, 채널별 실행조건 등이 포함될 수 있다.

### Solution / Execution Knowledge

Management Strategy를 실제 실행수단으로 구체화하기 위한 Knowledge다.

특정 Strategy를 어떤 Solution으로 실행할 수 있는지, Solution 적용조건과 Trade-off, 실제 업무절차와 채널 등이 포함될 수 있다.

### Dynamic Fact

시점에 따라 변하고 정확성이 중요한 정보다.

예:

```text
현재 판매상품
현재 금리
상품별 수익률
상품코드
상품 만기
가입가능 여부
판매가능 채널
현재 계좌상태
잔여한도
```

이러한 정보는 LLM의 기억이나 일반적인 문서지식에 의존하지 않고 가능한 경우 현재 시점의 Structured Data 또는 공식 Source를 통해 확인해야 한다.

### Field Know-how

실제 영업현장에서 반복적으로 활용되는 상담·판단 노하우다.

Field Know-how 역시 고객을 특정 방향으로 설득하기 위한 단순 Sales Rule이 아니라, 적절한 Management Decision을 실제 상담으로 연결하기 위한 판단지식으로 활용한다.

향후 실제 Corpus 분석 결과에 따라 Reasoning Knowledge의 일부로 통합할 수도 있으며, 현재 단계에서는 별도 Knowledge 영역으로 확정하지 않는다.

### Evidence / Provenance

모든 Knowledge가 동일한 권위와 신뢰도를 가지는 것은 아니다.

가능한 경우 Source, Source Type, As-of, Authority, Explicit / Integrated / Inferred, Validity 등의 정보를 함께 보존한다.

## 8.3 Customer Segment / Archetype

기존 업무자료에서 정의되거나 반복적으로 발견되는 고객군 역시 보존해야 할 Knowledge Asset으로 본다.

Customer Segment / Archetype은 고객을 하나의 유형으로 확정 분류하여 정답을 결정하기 위한 것이 아니라, 현재 Customer Context와 관련된 기존 업무지식과 현장 노하우를 찾는 Anchor로 활용한다.

원천자료에서 Segment를 발견한 경우 고객군의 이름이나 판별기준만 보존하는 것이 아니라, 왜 해당 고객군을 관리하는지, 어떤 정보를 함께 확인하는지, 어떤 판단원칙과 관리방향이 연결되는지 등 그 아래의 업무적 의미도 Knowledge Candidate로 추출한다.

구체적인 Segment Schema와 저장·검색방식은 후속 Knowledge Design에서 결정한다.

## 8.4 Knowledge의 기본 원칙

### 고객별 정답을 저장하지 않는다

고정된 `Customer Type → Goal → Solution` 경로를 대량으로 만드는 것을 Knowledge Base의 기본 구조로 삼지 않는다.

대신 고객을 판단하기 위해 반복적으로 사용되는 확인사항, 고려요소, 판단원칙, 관계, Trade-off, 현장 Know-how를 축적한다.

### Fact와 Judgment를 구분한다

제도상 가능/불가능 같은 Fact / Constraint와 경험적 판단이나 Know-how를 동일한 강도로 사용하지 않는다.

### 시점과 출처를 관리한다

상품, 금리, 제도, 내부 기준, 고객군 판별기준 등은 변경될 수 있으므로 가능한 경우 Source와 As-of를 함께 관리한다.

### Knowledge의 권위 수준을 구분한다

공식 규정과 현장경험이 충돌하는 경우 경험적 Know-how가 공식 Constraint를 우선할 수 없다.

## 8.5 Knowledge Design 접근방식

현재 단계에서는 Knowledge Schema를 먼저 완성한 뒤 전체 Corpus를 해당 구조에 맞추는 방식을 사용하지 않는다.

대신 실제 Management Reasoning에서 **어떤 Knowledge가 필요한지 먼저 관찰하고**, 반복적으로 필요한 구조를 기반으로 Knowledge Design을 구체화한다.

```text
Raw Documents
      ↓
Knowledge Candidate 추출
      ↓
Prototype Knowledge Pack 구성
      ↓
Customer Case Test
      ↓
실제 판단에 기여한 Knowledge 관찰
      ↓
반복 Pattern 발견
      ↓
Knowledge Model / Schema 정제
```

초기 Prototype에서는 완성된 Knowledge Base가 없어도 된다.

대표적인 Customer Case에 대해 필요한 Knowledge를 수작업으로 구성하여,

```text
Customer Context
+
Constraint
+
Hand-curated Knowledge Pack
        ↓
Management Reasoning
```

을 먼저 검증할 수 있다.

그 결과를 바탕으로 후속 Knowledge Design에서 구체적인 Schema, 저장방식 및 Retrieval Architecture를 결정한다.

## 8.6 현재 구조의 위치

본 장에서 정의한 Knowledge 영역은 최종 Knowledge Taxonomy가 아니다.

현재 단계에서는,

> **Agent가 Customer Context를 근거 있는 Management Decision으로 전환하기 위해 어떤 성격의 Knowledge가 필요한지를 나타내는 Requirement**

로 사용한다.

따라서 향후 실제 Corpus와 Prototype을 통해 Knowledge 영역을 통합하거나 추가할 수 있으며, Graph, RAG, Structured DB 등 물리적인 구현방식 역시 현재 구조에 종속되지 않는다.

핵심 원칙은 다음과 같다.

> **Knowledge Base를 먼저 완성한 뒤 Agent를 맞추는 것이 아니라, 실제 Agent Reasoning에서 반복적으로 요구되는 Knowledge의 형태를 관찰하면서 Knowledge Base를 설계한다.**

---

# 9. Implementation & Evaluation Loop

본 문서는 완성된 Agent Architecture를 그대로 구현하기 위한 최종 명세서가 아니다.

앞에서 정의한 Customer Understanding, Decision Control, Management Reasoning, Solution Resolution, Runtime 및 Knowledge Requirement는 현재 시점의 **Design Baseline**이며, 실제 Customer Case와 Prototype을 통해 검증하고 수정해야 한다.

따라서 본 Agent의 개발은 다음 반복과정을 기본 원칙으로 한다.

```text
Design Baseline
        ↓
Minimal Prototype
        ↓
Customer Case Test
        ↓
Failure Analysis
        ↓
Design / Knowledge / Runtime Revision
        ↓
Regression Test
        ↓
Next Iteration
```

핵심은 처음부터 완성된 구조를 설계하는 것이 아니라,

> **실제 Case에서 어떤 구조와 Knowledge가 필요한지를 관찰하면서 Agent를 발전시키는 것**

이다.

## 9.1 현재 설계의 해석 원칙

본 문서에는 성격이 다른 세 수준의 설계가 함께 존재한다.

### Design Principle

현재 Agent를 발전시키더라도 가능한 한 유지해야 하는 기본 원칙이다.

예:

```text
고객의 상황과 관리 필요성에서 출발한다.

상품에서 출발해 고객에게 이유를 맞추지 않는다.

확인된 사실과 추론된 가능성을 구분한다.

법·제도·투자성향 등 명확한 Hard Constraint는
LLM의 자유로운 추론에 맡기지 않는다.

Knowledge Base에 고객별 정답을 미리 저장하지 않는다.

최종 Solution은 실행가능성과 논리적 정합성을 검증한다.
```

이러한 원칙을 변경하려면 단순한 구현 편의가 아니라 명확한 업무적·실험적 근거가 필요하다.

### Conceptual Hypothesis

Agent가 고객을 판단하기 위해 현재 필요할 것으로 가정한 개념구조다.

예:

```text
Customer Context
Management Issue
Why Now / Priority
Management Goal
Management Strategy
Solution
Customer Segment / Archetype
```

이들은 현재 설계상 유용할 것으로 예상되지만 **확정된 Ontology가 아니다.**

실제 Case Test에서 역할이 중복되거나 판단 품질에 기여하지 않는다면 통합하거나 제거할 수 있다.

### Implementation Hypothesis

현재 구조를 구현할 때 선택할 수 있는 기술적 방법이다.

예:

```text
LLM Call 수
LangGraph Node 구성
Knowledge Representation / Retrieval 방식
Prompt 구조
Output Schema
Runtime State 구조
```

이러한 구현방식은 Core Design보다 자유롭게 변경할 수 있다.

## 9.2 개발 시작 방식

초기 개발에서는 개인형IRP 전체 업무범위를 한 번에 구현하지 않는다.

대표적인 하나의 **Vertical Slice**를 선택하여 End-to-End 흐름을 먼저 검증한다.

예를 들어 초기 Slice는 다음과 같이 구성할 수 있다.

```text
장기 미운용 / 대기성 자금 고객
```

해당 Case에 대해 최소한의 구조만 연결한다.

```text
Customer Information
        ↓
Customer Context
        ↓
Constraint
        ↓
Hand-curated Knowledge Pack
        ↓
Management Reasoning
        ↓
Solution Candidate
        ↓
Validation
        ↓
Employee Brief
```

초기 Prototype에서는 완성된 Knowledge Base나 Retrieval Engine을 전제하지 않는다.

필요한 Knowledge는 사람이 직접 구성하여 Reasoning 과정에 공급할 수 있다.

목적은 Knowledge Retrieval 기술을 먼저 검증하는 것이 아니라,

> **현재 정의한 Management Reasoning 구조 자체가 실제 고객판단에 유효한지 먼저 확인하는 것**

이다.

## 9.3 Test Case 확장 방식

하나의 Case가 잘 작동한다고 해서 현재 구조가 일반적으로 유효하다고 판단하지 않는다.

첫 Vertical Slice 이후에는 성격이 다른 Case를 순차적으로 추가한다.

예:

```text
운용공백
상품 만기
퇴직금 신규 유입
연금개시 예정
인출 필요
계약이전 검토
```

새로운 Case는 기존 Case와 가능한 한 다른 판단요소와 Constraint를 포함하도록 선정한다.

이를 통해 특정 Case에만 맞춰진 구조인지, 다양한 개인형IRP 사후관리 상황에서도 재사용 가능한 구조인지 검증한다.

## 9.4 평가 단위

Agent의 최종 답변만 평가하지 않는다.

Runtime의 각 단계가 맡은 책임을 제대로 수행했는지를 분리하여 평가한다.

### Customer Understanding

```text
필요한 고객정보를 빠뜨리지 않았는가?
확인된 Fact와 추론된 가능성을 구분했는가?
관련성이 낮은 정보를 과도하게 해석하지 않았는가?
Missing / Unconfirmed Information을 임의로 가정하지 않았는가?
```

### Decision Control

```text
필요한 Constraint가 적용되었는가?
허용되지 않는 판단이 Reasoning 후보에 포함되지 않았는가?
고객 Context와 Hard Constraint를 혼동하지 않았는가?
```

### Grounding

```text
현재 고객판단에 필요한 Knowledge가 공급되었는가?
불필요하거나 잘못된 Knowledge가 포함되지 않았는가?
Knowledge의 Source와 권위가 적절하게 사용되었는가?
```

### Management Reasoning

```text
실제 관리가 필요한 Issue를 포착했는가?
Why Now / Priority가 타당한가?
고객 Context와 Knowledge를 근거로 판단했는가?
과도한 가정을 하지 않았는가?
필요한 추가 확인사항을 명시했는가?
```

### Solution Resolution

```text
Management Strategy와 Solution이 자연스럽게 연결되는가?
실제 고객상황과 무관한 Solution을 생성하지 않았는가?
변경하지 않는 대안이나 판단 보류도 필요한 경우 고려했는가?
```

### Validation

```text
실행 불가능한 Solution을 제거했는가?
Constraint를 위반하는 결과가 남아 있지 않은가?
서로 논리적으로 충돌하는 Solution을 동시에 제시하지 않았는가?
```

### Presentation

```text
행원이 고객관리 판단을 이해할 수 있는가?
왜 관리해야 하는지 설명되는가?
무엇을 확인해야 하는지 알 수 있는가?
어떤 순서로 상담할지 실무적으로 활용할 수 있는가?
```

## 9.5 Failure Analysis

Test 결과가 기대와 다를 경우 곧바로 Prompt를 수정하거나 새로운 Rule을 추가하지 않는다.

먼저 **어느 단계에서 실패가 발생했는지 분류한다.**

현재는 다음 Failure Category를 기본 분류로 사용한다.

```text
Data Failure
Context Interpretation Failure
Constraint Failure
Knowledge Failure
Grounding / Retrieval Failure
Concept Model Failure
Prompt / Schema Failure
LLM Reasoning Failure
Solution Resolution Failure
Validation Failure
Presentation Failure
```

예를 들어 위험중립형 고객에게 허용되지 않는 고위험 상품이 제시된 경우 이를 단순히 `LLM Reasoning Failure`라고 판단하지 않는다.

다음 가능성을 먼저 구분한다.

```text
투자성향 Data가 입력되지 않았는가?
Constraint가 정의되지 않았는가?
Pre-Reasoning Control에서 적용되지 않았는가?
Solution / Product 후보 필터링이 누락되었는가?
Post-Reasoning Validation이 실패했는가?
```

이를 통해 오류의 실제 발생지점을 찾고 **필요한 부분만 수정한다.**

## 9.6 Conceptual Hypothesis 검증

현재 문서에서 정의한 Concept은 실제 Test를 통해 독립적인 필요성을 검증한다.

| 현재 가설 | 검증 질문 | 가능한 변경 |
|---|---|---|
| Situation과 Issue 구분 | 서로 다른 의미를 안정적으로 표현하는가? | 통합 |
| Management Goal | Strategy 도출이나 설명에 기여하는가? | 유지 / 통합 / 제거 |
| Strategy와 Solution 구분 | 재사용성과 설명가능성을 높이는가? | 유지 / 통합 |
| Why Now / Priority | 관리대상 우선순위 판단에 도움이 되는가? | 강화 / 제거 |
| Required Confirmation | 과도한 추론을 줄이는가? | 유지 / 구조변경 |
| Customer Segment | Knowledge Grounding에 실질적으로 도움이 되는가? | 유지 / 약화 / 제거 |
| Reasoning Knowledge | Knowledge 없이 판단할 때보다 품질이 개선되는가? | 구조 정제 |
| 단일 Reasoner | 복잡한 Case까지 안정적으로 처리하는가? | 유지 / 분리 |

Concept을 추가할 때도 동일한 원칙을 적용한다.

> **새로운 Concept은 “있으면 그럴듯하기 때문”이 아니라, 반복되는 Failure를 기존 구조로 설명하거나 해결하기 어렵다는 근거가 있을 때 추가한다.**

## 9.7 Knowledge Base 발전 방식

Knowledge Base 역시 초기 Schema를 확정하고 Corpus 전체를 맞추는 방식으로 개발하지 않는다.

초기에는 Case별 Hand-curated Knowledge Pack을 사용한다.

```text
Customer Case
      ↓
필요 Knowledge 수작업 구성
      ↓
Reasoning Test
      ↓
사용된 Knowledge 관찰
      ↓
Case 추가
      ↓
반복적으로 등장하는 Knowledge Pattern 발견
```

여러 Case에서 반복적으로 필요한 Knowledge가 발견되면 그때 구조화를 검토한다.

예를 들어 다음 질문을 기반으로 Knowledge Design을 발전시킨다.

```text
어떤 Knowledge가 반복적으로 필요한가?
어떤 Knowledge는 구조화된 Field가 필요한가?
어떤 Knowledge는 자연어 문맥이 더 중요한가?
어떤 관계는 명시적으로 연결해야 하는가?
어떤 정보는 최신성이 중요해 Dynamic Source로 분리해야 하는가?
Customer Segment가 실제 Grounding Anchor로 작동하는가?
Field Know-how를 어떤 수준으로 일반화해야 다른 Case에서도 재사용할 수 있는가?
```

그 결과에 따라 Graph, RAG, Structured DB 또는 다른 방식과 그 조합을 검토한다.

즉,

> **Knowledge Representation은 선행조건이 아니라 실제 Knowledge Usage Pattern에서 도출한다.**

## 9.8 설계 변경 원칙

Test에서 문제가 발견되었다고 해서 전체 설계를 즉시 변경하지 않는다.

설계 변경은 다음 순서로 수행한다.

```text
1. Failure를 재현한다.
2. Failure 발생 Layer를 특정한다.
3. Data / Knowledge / Runtime / Concept 중 실제 원인을 구분한다.
4. 가장 작은 수정안을 적용한다.
5. 해당 Case를 다시 Test한다.
6. 기존 Case를 Regression Test한다.
7. 반복적으로 개선효과가 확인되는 경우 Design Baseline에 반영한다.
```

다음과 같은 변경은 지양한다.

```text
한 개 Case 때문에 새로운 Concept을 추가하는 것
한 번의 좋은 결과만으로 Concept을 확정하는 것
Prompt 문제를 Concept Model 문제로 오인하는 것
Knowledge 부족을 LLM 성능 문제로 오인하는 것
특정 상품이나 업무사례에 맞추어 전체 Architecture를 과도하게 특화하는 것
구현 편의를 위해 Hard Constraint를 LLM Prompt에만 의존하도록 변경하는 것
```

## 9.9 Regression Test

설계를 수정한 경우 새로운 Case만 좋아졌는지를 보지 않는다.

기존에 정상적으로 처리하던 Case에도 동일한 변경을 적용하여 결과를 비교한다.

```text
New Case Failure
      ↓
Design Revision
      ↓
New Case Re-test
      +
Existing Case Regression Test
```

가능한 경우 각 Test Case에는 다음과 같은 Expected Behavior를 함께 관리한다.

```text
반드시 고려해야 하는 정보
적용되어야 하는 Constraint
피해야 하는 잘못된 판단
기대되는 관리방향의 범위
반드시 추가 확인해야 하는 사항
허용 가능한 Solution 범위
```

Expected Behavior는 하나의 정답문장을 지정하기보다 **허용 가능한 판단범위와 금지되는 오류를 정의하는 방식**으로 관리한다.

## 9.10 Design Change Log

설계가 변경될 때에는 결과만 수정하지 않고 변경 이유를 기록한다.

최소한 다음 내용을 남긴다.

```text
변경 대상
기존 설계
변경된 설계
변경을 유발한 Test Case
관찰된 Failure
변경 이유
Regression Test 결과
```

이를 통해 이후 작업자가 현재 구조를 단순한 최종 결과로 보지 않고,

> **어떤 문제를 해결하기 위해 현재 구조가 만들어졌는지**

추적할 수 있도록 한다.

## 9.11 다른 LLM / 다른 세션에서의 작업 원칙

본 문서를 기반으로 새로운 LLM, Agent 또는 작업 세션에서 개발을 이어갈 경우 다음 원칙을 우선 확인한다.

1. **현재 구조를 완성된 Architecture로 간주하지 않는다.**  
   기존 요소를 그대로 구현하기보다 왜 해당 요소가 존재하는지 먼저 이해한다.

2. **Design Principle과 Hypothesis를 구분한다.**  
   Hard Constraint 통제나 Fact / Inference 구분과 같은 기본원칙과 Goal·Segment·Strategy 같은 Conceptual Hypothesis를 동일한 수준으로 취급하지 않는다.

3. **새로운 구조를 추가하기 전에 실제 필요성을 확인한다.**

```text
어떤 실제 Failure를 해결하려는가?
기존 구조로는 왜 해결하기 어려운가?
추가된 구조가 다른 Case에도 반복적으로 필요한가?
```

4. **Knowledge Base의 구현형태를 Core Design에 역으로 강제하지 않는다.**  
   Graph를 사용한다고 모든 Concept을 Node로 만들지 않고, Vector DB를 사용한다고 모든 Knowledge를 자연어 Chunk로만 표현하지 않는다.

5. **결과가 이상하면 먼저 Failure Layer를 찾는다.**  
   LLM 결과가 좋지 않다는 이유만으로 Prompt부터 수정하지 않는다.

6. **설계 변경의 이유를 남긴다.**  
   어떤 Test와 Failure 때문에 변경했는지 기록한다.

7. **기존 Case를 다시 Test한다.**  
   특정 Case에만 최적화되지 않았는지 Regression Test를 수행한다.

## 9.12 권장 작업 Handoff 순서

새로운 작업자가 본 문서를 이어받는 경우 다음 순서로 시작하는 것을 권장한다.

```text
1. Agent Concept 확인

2. Design Principle /
   Conceptual Hypothesis /
   Implementation Hypothesis 구분

3. 현재 Test Case와 Change Log 확인

4. 하나의 Vertical Slice 선정

5. 필요한 Customer Information 정의

6. Constraint 정의

7. Hand-curated Knowledge Pack 작성

8. Minimal Runtime으로 End-to-End Test

9. Trace 기반 Failure Analysis

10. 최소 수정

11. Regression Test

12. 반복적으로 확인된 Pattern을
    Core / Knowledge / Runtime Design에 반영
```

전체 Knowledge Base나 전체 개인형IRP 업무를 먼저 구현하는 것을 기본 접근방식으로 삼지 않는다.

## 9.13 문서 간 역할 분리

향후 문서는 다음과 같이 역할을 분리한다.

```text
00_Core_Concept_Design.md
→ Agent가 무엇이며 어떤 원칙으로 판단하는가

01_Knowledge_Design.md
→ 검증을 통해 발견한 Knowledge를
  어떤 구조로 표현하고 관리하는가

02_Runtime_Design.md
→ 실제 Runtime을
  어떤 Component / Node / State로 구현하는가

03_Test_Evaluation.md
→ Test Case, Expected Behavior,
  평가기준과 Failure를 어떻게 관리하는가

04_Test_Cases/
→ 실제 Customer Case와 Regression Case

05_Knowledge/
→ 검증·정제된 Knowledge Asset
```

본 문서는 이 가운데 `Core Concept Design`의 기준 문서다.

따라서 구체적인 Graph Schema, Prompt 전문, LangGraph Code, DB Schema, Product Table 등은 본 문서에 과도하게 포함하지 않고 후속 문서로 분리한다.

## 9.14 Current Status

현재 v0.4 단계의 상태는 다음과 같다.

```text
Core Agent Concept
→ 초기 Baseline 정의

Customer Understanding Model
→ Conceptual Hypothesis

Decision Control
→ 기본 원칙 정의

Management Decision Model
→ Conceptual Hypothesis / 검증 전

Solution Resolution
→ Conceptual Hypothesis / 검증 전

Runtime Contract
→ 초기 Baseline 정의

Knowledge Requirements
→ Requirement 수준 정의

Knowledge Schema
→ 미확정

Knowledge Retrieval Architecture
→ 미확정

LangGraph / Runtime Implementation
→ 미확정

Initial Vertical Slice
→ 선정 및 구현 필요

Customer Case Test
→ 미실시

Conceptual Hypothesis Validation
→ 미실시
```

따라서 다음 단계의 목표는 전체 설계를 더 정교하게 만드는 것이 아니라,

> **대표적인 Customer Case 하나를 현재 설계로 실제 실행해보고, 어떤 부분이 유효하고 어떤 부분이 불필요하거나 부족한지를 관찰하는 것**

이다.

## 9.15 최종 개발 원칙

본 Agent의 발전방향을 한 문장으로 정리하면 다음과 같다.

> **설계를 먼저 완성한 뒤 구현하는 것이 아니라, 최소한의 설계를 실제 Customer Case에 적용하고 그 결과에서 얻은 증거를 바탕으로 Concept, Knowledge, Runtime을 반복적으로 발전시킨다.**

따라서 본 문서의 목적은 변화하지 않는 정답 Architecture를 남기는 것이 아니다.

본 문서는 향후 개발과정에서,

```text
무엇은 지켜야 하는 원칙인지
무엇은 아직 검증되지 않은 가설인지
무엇을 실제로 테스트해야 하는지
결과가 틀렸을 때 어디를 살펴봐야 하는지
어떤 근거가 있을 때 구조를 변경해야 하는지
```

를 지속적으로 판단할 수 있도록 하는 **Core Design Baseline이자 개발 Handoff 기준**으로 사용한다.
