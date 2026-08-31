# 인수인계 문서 — IRP 사후관리 Agent: Input·Brief 개편 계획 (확정본)

이 문서는 이 프로젝트를 처음 보는 LLM/Agent가 저장소를 뒤지기 전에 읽는 자족적 설명문이다. 계획은 2026-08-31 Human이 확정했다. **단, 착수는 Human의 명시적 지시가 있어야 시작한다 — 이 문서를 읽었다는 것만으로 작업을 시작하지 않는다.**

---

## 1. 이 프로젝트가 무엇인지

KB 개인형IRP(퇴직연금) **사후관리 의사결정 Agent**를 만드는 프로젝트다. Agent의 사용자는 고객이 아니라 **은행 직원**이다. Agent는 고객 데이터를 받아 "이 고객이 지금 어떤 상황이고, 무엇을 관리해야 하며, 무엇을 확인해야 하는가"를 판단해 직원용 Brief를 만든다.

개발 방법론이 특징적이다:
- **Golden Case 기반**: 숙련 직원이 "이걸 못 하면 업무를 모르는 것"이라 볼 상황 17개를 Case로 동결(Freeze)하고, 각 Case에 정답 문장이 아닌 **판단의 경계(Semantic Boundary)** — 반드시 고려할 것 / 단정하면 안 되는 것 / 확인해야 할 것 / Critical Mistake — 를 정의한다.
- **역할 분리**: 판단 생성(Builder)은 Gemma 4 모델, 평가(Evaluator)는 Claude가 별도 Context에서 수행한다.
- **증거 기반 개정**: Case 실행에서 실패 패턴(F-001~F-010)을 수집하고, 여러 Case에 걸친(cross-case) 증거가 모였을 때만 아키텍처를 개정(REV-001, REV-002, …)한다. 개정 후에는 반드시 Regression으로 검증한다.
- **Human Gate**: 업무 의미(Semantic)를 바꾸는 결정 — 새 출력 구조, 새 제약, 평가 기준 변경 — 은 Human만 내린다. Agent는 승인된 경계 안에서만 자율 작업한다. 확정된 결정은 HD-1~HD-6으로 기록돼 있고 재질문하지 않는다.

핵심 도메인 원칙 몇 가지 (이미 확정, HD 문서 참조):
- **투자성향은 Hard Constraint** (HD-2): 안정형<안정추구형<위험중립형<적극투자형<공격투자형. 성향은 가입 가능한 위험수준의 **상한**이지 그만큼 위험을 지라는 요구가 아니다. 성향↔펀드등급 매핑은 코드로 검증한다(C2 validator).
- **최종 계산값은 Scope 밖** (HD-1): 세액·수령액의 확정 계산은 하지 않고 업무 화면/계산기로 연결한다.
- **영업점 Hot Tip은 Operational Knowledge** (HD-3): 확인 순서·화면·절차엔 적극 활용하되, 단독으로 제도적 사실이나 실행 가능 여부를 확정하지 않는다.
- **마케팅/KPI 동기를 판단 근거로 재생산하지 않는다**: TM 타겟 리스트 포함 여부는 관리 필요의 근거가 아니다(이를 어기면 F-009).

## 2. 현재 상태 (2026-08-31, main 기준)

- 17개 Golden Case 전부 1차 사이클 완료: **PASS 7 · PARTIAL 10 · FAIL 0**, Stop Condition 없음.
- **REV-001** (첫 아키텍처 개정) 완료·검증: 출력을 "Judgment-first" 구조로 바꿈 — 고객 상황 → **Management Judgment**(개입 필요 / 추가 확인 우선 / 현상유지 가능 / 정보안내 중심 / 고객결정 지원 / 실행 불가) → Next Action. 이로써 최대 실패였던 F-005(판단 전에 변경/개입 방향으로 조기 수렴하는 Action Bias)가 17 Case에서 강한 재현 0으로 소멸.
- 잔여 실패는 표현·세부 수준으로 수렴: Knowledge 항목 내부의 세부 조건 탈락(F-006), 확인 축 1~2개 누락(F-004), "방치" 같은 단정 어휘(F-001).
- 다음 큰 작업으로 Human이 정한 방향이 바로 이 문서의 주제: **Input과 Output(Employee Brief)의 전면 개편 = REV-002.**

## 3. 확정된 Target Concept

### 3.1 중심 원칙

> Agent에게 "고객을 설명한 결론(판단 완료 라벨)"을 주지 말고, "고객을 스스로 재구성할 수 있는 Evidence"를 시간·맥락·확실성 정보와 함께 준다. **계산은 시스템이 하고, 해석과 판단은 Agent가 한다.**

지금까지의 실패 대부분이 이 경계가 입력에 없어서 생겼다는 것이 17개 Case의 실증이다. 예: 입금 사유·경과일 없이 "현금성 100%"만 주면 모델은 "방치"라고 확정한다. "7일 전 퇴직급여 1.8억 입금 + 이후 매매 없음"을 주면 "신규 퇴직자금이 아직 운용으로 연결되지 않은 상태"라는 올바른 해석이 나온다.

### 3.2 Input — Customer Evidence Pack

4덩어리: **Snapshot(현재 상태) + Event Timeline(왜 이렇게 됐나) + Wider Context(IRP 밖 맥락) + Evidence Metadata(확실성 정보)**. 9개 섹션:

1. Customer/Pension Profile — 연령, 투자성향(+분석일), 가입일, 연금단계
2. IRP Current Snapshot — 잔액/상품/**비중(미리 계산)**/수익률/현금성/만기
3. IRP Event Timeline — 입금(사유 포함)/퇴직급여/만기/매수/매도/운용지시/이전, 시간순
4. Whole-Asset Context — 전체 금융자산, 타 연금(연금저축·ISA), 유동성
5. Investment Activity — IRP·타계좌 최근 투자행동
6. Upcoming Events — 만기·ISA 만기 등 예정 이벤트
7. Digital Signals — 조회/검색/메뉴 진입 (관심의 Evidence일 뿐 의사가 아님을 명시)
8. Known Customer Intent — 있을 때만, **일자+발화 원문** ("2026-02-20 상담 시: 'IRP는 예금 중심으로 하고 싶다'")
9. Existing Bank Signals — 캠페인/타겟 분류. 고객 상태 판단 근거와 **분리**(왜 이 고객이 화면에 떴는가의 출처일 뿐)

규칙: 모든 데이터에 `as_of`(시점) / Fact·Calculated·Signal 3분류 / 변화가 의미 있는 항목엔 변화량(현재·1개월 전·증감) / 없는 데이터는 빼지 말고 "데이터 없음"으로 명시(단, 모든 고객 공통의 고정 슬롯으로 — Case별 선택 제공은 힌트가 되므로 금지) / "이탈위험 고객·ETF 니즈 고객" 같은 판단 완료 라벨 금지.

### 3.3 판단 파이프라인

```
Evidence Pack → ① 고객 상태 해석(Fact/추론 구분) → ② Management Judgment(방향 중립, REV-001 재사용)
→ ③ 핵심 관리 포인트 + 전략(조건부 분기) → ④ Required Confirmation → ⑤ Employee Brief
```

### 3.4 Output — Employee Brief 5-섹션

"판단 요약"이 아니라 **직원의 업무 흐름을 미러링한 Recommendation Brief**. 직원용 도구이며 고객 직접 제공 문서가 아니다.

1. **고객 상황** — 핵심만 간결히. 절제된 해석 허용("운용 여부를 결정하지 않은 상태") / 단정 어휘("방치") 금지
2. **핵심 관리 포인트** — "지금 무엇을 관리하는 것이 중요한가"에 커밋. **확인 사항은 독립 섹션이 아니라 이 아래 '먼저 확인하세요'로 종속** — 확인은 관리 포인트 실행의 첫 행동이다
3. **추천 운용 방향** — 연령·자금성격·기간·성향·의사를 고려해 필요 시 상품 수준(원리금보장/TDF/펀드/디폴트옵션)까지 연결. 확인 미완 사항은 조건부("장기운용 의사가 확인되면 →"). 성향 Hard Constraint 작동 지점
4. **상담 Point** — 이 고객 전용으로 생성: 접근 논리, 설명 순서, 실제 화법
5. **관련 TIP & GUIDE** — 행내 자료에서 연결(retrieval): Hot Tip, 관련 화면번호, 절차, 반론 대응, 제도 유의사항. 출처·권위 수준 명시

### 3.5 Business 관점 원칙 (Step 3에서 HD로 명문화 예정)

> 은행의 Business Objective가 고객의 관리 필요성을 **만들어내서는 안 된다.** 하지만 고객에게 유효한 관리기회가 존재한다면, 허용 범위 안에서 그 기회를 은행의 관리행동(운용 활성화, 만기 재운용, 추가납입, 이탈방어, 후속관리 등)으로 **적극 연결해야 한다.**

판별 기준 = **근거 출처 테스트**: 관리 포인트의 근거가 고객의 Fact/Event에서 출발하면 유효, KPI·캠페인·타겟 리스트에서 출발하면 위반.

## 4. 이미 내려진 설계 판단 (재논의 금지)

1. **F-005 재발 방지 = 판단층/전달층 분리.** 내부 판단은 방향 중립 Management Judgment 유지("관리할 것 없음·유지·불가"도 동등한 정답). "관리기회" 언어는 판단 후의 Brief에서만. "핵심 관리 포인트"는 넓게 정의 — 확인 우선, 유지+다음 관리 시점 예약, 불가 안내+대안도 모두 관리 포인트다.
2. **Calculated Fact 경계**: 비중·경과일·만기 D-n·디폴트옵션 자동적용 예정일·개시요건 충족 여부 등 "계산"만 전처리로 제공. "미운용 상태로 추정" 같은 "판단"은 전처리 금지.
3. **Regression 방식**: 동결된 기존 Case 문서는 불변. 대표 6~8개 Case에 `input_v2`(정보량 동일, 조직 형태만 새 구조) 부록을 만들어 재실행·비교. **Counterfactual Pair(GC-04↔05: 같은 조건에서 고객 의사만 달라 정답이 갈리는 쌍) 필수 포함** — 기회 중심 구조가 Action Bias를 재도입했는지의 감지선.
4. **Knowledge 세부 조건 구조화(REV-003 후보)는 이번에 섞지 않는다** — 변수 2개 동시 변경 시 효과 귀속 불가. REV-002 결과를 보고 범위 결정.
5. Wider Context·Digital Signals 등 **신규 섹션의 검증은 기존 Case가 아니라 신규(P2) Case가 담당**한다.

## 5. 작업 순서 (확정)

| Step | 내용 | 수행 주체 | 산출물 |
|---|---|---|---|
| 1 | 증거 수집: 17 Case 역추적(쓰인 Fact/Unknown/미사용/오추론) + 참고 Excel 필드 추출 + 기존 Brief를 5-섹션 관점으로 재독해 + Source의 화면·Hot Tip 재료 조사 | Agent 자율 | 증거 목록 |
| 2 | Spec 초안 3건: `TARGET_CONCEPT.md`(컨셉+증거), `EVIDENCE_PACK_SPEC.md`(필드 표: 유형/as_of/변화량/근거 Case/**Availability=`?`**), `EMPLOYEE_BRIEF_SPEC.md`(섹션별 필수·금지 요소, Judgment 결과별 변형, 평가 축) | Agent 자율 | Draft 3건 |
| 3 | **Human Gate**: Availability `?` 확정(은행 데이터 현실은 Human만 앎), 필드·컨셉 승인, HD-6 갱신(Brief를 진단용→직원용 Output으로 승격)·HD-7 신설(§3.5 원칙), REV-002 범위 승인 | **Human** | 확정 Spec + HD |
| 4 | REV-002 구현: runtime에 Evidence Pack 입력 구조 + 전처리(Calculated Fact) + Brief 5-섹션 출력. 기존 deterministic 검사 유지 | Agent 자율 | runtime 개정 + REVISIONS 기록 |
| 5 | Regression: 대표 6~8 Case `input_v2` 재실행(Builder=Gemma 4, Evaluator=Claude), 신규 실패는 F-011~로 등록, Batch Summary 보고 | Agent 자율 | Regression 결과 |
| 6 | 결과 보고 후 결정: REV-003 여부 / P2 Batch 3 설계 / Reusable Knowledge 착수 | **Human** | 다음 방향 |

Human 개입 지점은 Step 3과 Step 6 두 곳뿐이다. Step 3 승인 전에는 runtime 코드를 절대 변경하지 않는다.

## 6. 이후 로드맵 (참고)

REV-002 완료 후: ① REV-003(Knowledge 세부 조건 구조화 — Regression 결과가 범위 결정) → ② P2 Batch 3(신규 섹션 검증 + 커버리지 공백: 시황 활용, ELB 청약, 결정세액 부족 등) → ③ Reusable Knowledge/Retrieval(Brief 섹션 5가 실수요처, 20+ Case 사용 실적 근거로) → ④ 실전화(Availability 확정 필드 = 시스템 연동 명세의 전신, deterministic 검사 확장, 자동 평가, 직원 검증).

## 7. 승계 세션 행동 규칙

- **Human의 착수 지시 전에는 Step 1도 시작하지 않는다.**
- 동결된 Case·RUN·EVAL 소급 수정 금지 (append-only).
- 보류 항목(Retrieval, Multi-Agent, 자동 Evaluator 등)을 이 작업 중 무단 도입 금지.
- 확정된 Human Decision(HD-1~6) 재질문 금지.
- 상세 근거·파일 경로는 저장소의 `design/INPUT_BRIEF_WORK_PLAN.md`(본 계획의 상세판), `AGENTS.md` §20(운영 규칙), `golden/HUMAN_DECISIONS.md`, `cases/FAILURE_MAP.md`, `golden/P1_BATCH2_SUMMARY.md`를 본다.
