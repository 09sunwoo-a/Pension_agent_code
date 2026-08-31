# Target Concept — Customer Evidence Pack · 판단 파이프라인 · Employee Brief (REV-002 대상)

- Status: **HUMAN CONFIRMED — Step 3 Human Gate 결정 반영 (2026-08-31)**. 기본 방향 승인(결정 1-1), Evidence Pack 8-섹션 확정(1-2), 실증 표현 정교화(1-3), 화면 조회값 3계층(1-4), Candidate Pool 원칙(1-5) 반영. 결정 전문은 Step 3 지시 기록, 요약은 §6.
- 근거: `design/evidence/` 5건. 상세 명세: `design/EVIDENCE_PACK_SPEC.md` · `design/EMPLOYEE_BRIEF_SPEC.md`. 계획: `design/INPUT_BRIEF_WORK_PLAN.md`.

---

## 1. 중심 원칙

> Agent에게 "고객을 설명한 결론(판단 완료형 라벨)"을 주지 말고, "고객을 스스로 재구성할 수 있는 Evidence"를 시간·맥락·확실성 정보와 함께 준다. **계산은 시스템이 하고, 해석과 판단은 Agent가 한다.**

### 1.1 실증의 범위 (결정 1-3 — 과대 표현 금지)

기존 Golden Case(18개)가 실증한 것은 Target Concept의 **핵심 구조 필요성**이다:

| 실증된 핵심 구조 | 근거 |
|---|---|
| 결론 라벨 금지·Evidence 제공 (Snapshot+사유) | 입금사유·경과일 부재 → "방치" 확정(CASE_001·GC-12); 사유 분해 제공 → 정확한 구분(GC-11 PASS) |
| Timeline·경과 계산의 시스템 담당 | GC-04 2주 자동적용 도과 미검출; 계산 성공 ≠ 해석 성공(GC-09·17) |
| Intent의 Freshness (일자 동반) | GC-04(6개월 전 발화)·GC-06(8개월 전) — 일자가 있어야 재확인 판단 가능 |
| Judgment Boundary (방향 중립·확인 우선·유지 정답) | REV-001 17 Case: Action Bias 강한 재현 0 |

**Whole-Asset Context와 Digital Signals는 신규·확장 영역이다.** 기존 Case의 부분 관찰(GC-13/15의 타사 계약, GC-05의 행동 신호)이 방향을 지지하지만, 본격 검증은 **P2 Case가 담당**한다. 따라서 이 문서는 "현재까지의 Evidence를 기반으로 Human이 승인한 설계 방향"이며, 신규 영역까지 검증 완료된 설계가 아니다.

## 2. 판단 파이프라인 (판단층 / 전달층 분리)

```
Customer Evidence Pack (8-섹션 입력)
  ↓
① Customer State Interpretation   "어떤 상황이고 왜 이렇게 됐나" — Fact/추론 구분 명시
  ↓
② Management Judgment (방향 중립)  REV-001 재사용: 개입 필요 / 추가 확인 우선 / 현 상태 유지 가능
  ↓                               / 정보 안내 중심 / 고객 결정 지원 / 실행 불가
③ 핵심 관리 포인트 + 관리전략       ②의 결과를 기회 언어로 조직 (필요한 분기만 유지)
  ↓
④ Required Confirmation           고객 확인 vs 직원 Operational Check 구분 — Agent가 도출 (입력 힌트 아님)
  ↓
⑤ Employee Brief (5-섹션 출력)
```

- **F-005 재발 방지**: "관리기회" 언어는 ③ 이후에만. ②는 방향 중립 유지 — "관리할 것 없음·유지·불가"도 동등한 정답.
- **핵심 관리 포인트의 넓은 정의**: 확인 우선·유지(+다음 관리 시점 예약)·실행 불가(사유+대안)도 관리 포인트다.
- **Required Confirmation은 Agent의 산출물**(결정 2-11): 자금 사용계획·위임 선호·손실 감내 같은 Decision Variable은 입력 슬롯으로 제공하지 않는다. Agent가 Evidence와 판단 결과로부터 "무엇을 물어야 하는가"를 도출한다.
- **Evidence Trace**(결정 3-4): Management Point와 Recommended Direction에는 내부적으로 `supporting_evidence_ids` / `supporting_knowledge_ids`를 남긴다 — Chain-of-Thought 저장이 아니라 판단의 Evidence Provenance 검증 구조다.

## 3. Input — Customer Evidence Pack (8-섹션 확정; 상세는 EVIDENCE_PACK_SPEC.md)

| # | 섹션 | 비고 |
|---|---|---|
| 1 | Customer / Pension Profile | 성향 변경 이력 포함(GC-09 실증). Availability 확정(결정 2-1) |
| 2 | IRP Current Snapshot | 비중 등은 전처리 계산. 판매중단·과세이연 상태·한도위반 표시값은 미제공(결정 2-2) |
| 3 | IRP Event Timeline | 입금(+사유 코드)·매매·계약이전 등 **실확보 가능 Event만**. 과거 상태를 현재 정보에서 추정해 Timeline Fact화 금지(결정 2-3) |
| 4 | Whole-Asset Context | 타사 연금저축·ISA·소득구간 확보 가능. **본격 검증은 P2**(결정 2-5) |
| 5 | Investment Activity | IRP 내 행동만. 타계좌/마이데이터 Cross-account 행동은 미제공(결정 2-6) |
| 6 | Upcoming Events | 시한·할 일 성격 명시 구조 — 부차 만기 탈락(F-003) 대책 |
| 7 | Digital / Behavioral Signals | 고객 단위 행동 로그 활용 가능. **Signal→Intent 직접 승격 금지 = Critical Boundary, P2 검증**(결정 2-7) |
| 8 | Customer Interaction / CRM Memo | 상담메모(작성일·채널·내용·source=직원 작성). verbatim 보장 없음·현재 의사의 Ground Truth 아님·명시/부수 사전 분류 없음 — 해석은 Agent 몫(결정 2-8) |

- **Existing Bank Signals 섹션은 삭제**(결정 1-2·2-9): TM Target·Campaign·Badge·LMS/SMS 등은 REV-002 Customer Reasoning Input에 제공하지 않는다.
- 횡단 규칙: `value + as_of` / F·C·S 라벨 / NULL·0·해당없음 3분 / 판단 완료형 라벨 금지 / **Evidence Missing만 스키마 NULL로 명시**(Decision Variable은 입력이 아님 — 결정 2-11).
- **Calculated Fact 2분류**(결정 2-12): Arithmetic Derived(비중·D-n·경과일·증감)와 Rule-derived Fact(개시요건·DO 적용 예상 기준일·세액공제 한도·위험자산 한도 판정 — `rule_source`·`rule_as_of` 필수).

### 3.1 데이터 확보 시점 3계층 (결정 1-4)

화면에 존재한다는 이유만으로 입력으로 간주하지 않는다:

| 계층 | 정의 | 취급 |
|---|---|---|
| **Base Customer Evidence** | 정기적으로 확보되는 고객/계좌/거래 데이터 | Evidence Pack 본체 |
| **Pre-Judgment Enrichment** | 판단 직전 별도 조회로 확보 가능하고 Management Judgment 자체에 필요한 값 | 확보된 경우 Evidence Pack에 동봉 가능(조회 출처 표기) |
| **Execution-time Check** | 실행 직전 직원이 화면/계산기에서 확인할 값 (수령한도 [02-12-221], 중도해지 계산기, 실제 수수료율 등) | 입력 아님 — Next Action/S5의 산출물 |

## 4. Output — Employee Brief 5-섹션 (요약; 상세는 EMPLOYEE_BRIEF_SPEC.md)

S1 고객 상황 / S2 핵심 관리 포인트+먼저 확인하세요 / S3 추천 운용 방향 / S4 상담 Point / S5 관련 TIP & GUIDE — 구조 승인(결정 3-1).

- S1: 단정 어휘 금지(F-001 5건 전부 S1 발생 — 감사 실증).
- S3 분기 규칙(결정 3-2): **Branch Preservation, not Branch Creation** — Management Decision을 실제로 바꾸는 미확인 변수가 있을 때만 분기. Evidence만으로 방향이 결정되면 단일 Recommended Direction 허용.
- S3 상품 연결(결정 1-5·3-3): §4.1 Candidate Pool 원칙.
- S4 화법·S5 출처 연결은 신규 제작(감사: 0/18). S5는 Case별 Knowledge Pack 수동 동봉 — Retrieval·자동 색인 보류(결정 3-7).
- 검증 경계(결정 3-6): 문자열/구조로 확정 판정 가능한 것만 deterministic validator, 의미 판정은 Evaluator 몫.

### 4.1 상품 수준 연결 — Candidate Pool 원칙 (결정 1-5, SYSTEM_ROLE 원칙 5 대체)

1. LLM이 임의로 상품을 생성하거나 자유롭게 선정하지 않는다.
2. 먼저 고객 상황에 따른 **운용 방향/상품 유형**을 판단한다.
3. 특정 상품 수준 연결이 필요한 경우, **현재 판매 가능하고 투자성향(C1/C2/C3)·채널·상품 제약을 통과한 승인된 Candidate Pool 안에서만** 후보를 제시한다. (REV-002에서 Pool은 Case별 Reference Data로 동봉 — GC-17 TDF 라인업 방식)
4. 고객 의사 또는 실행조건이 미확인이면 반드시 조건부로 제시한다.
5. 고객의 최종 선택을 전제로 한다.
6. 기존 deterministic Hard Constraint(C1/C2/C3)는 유지한다.

## 5. Business 관점 원칙 (HD-7로 명문화 — 결정 4)

> **고객의 관리 필요성은 Customer Evidence에서 출발해야 한다. 은행의 Business Objective가 관리 필요성을 만들어내서는 안 된다. 독립적으로 유효한 고객 관리기회가 존재하는 경우에만, 허용된 범위 안에서 은행의 관리행동(운용 활성화·장기 운용 연결·만기 재운용·추가납입·리밸런싱·이탈방어·연금관계 지속·후속관리)으로 적극 연결할 수 있다.**

- D10·F-009와 정합: 기존 원칙의 폐기가 아니라 명문화·정밀화다.
- REV-002에서는 TM·캠페인 신호가 **입력에서 제거**되므로 F-009형 오용은 구조적으로 차단된다. 대신 검증 축은 Evidence Trace로 이동: Management Point가 실제 Customer Evidence(`supporting_evidence_ids`)로 추적 가능해야 하며, 근거 없는 포인트는 REVIEW/FAIL(결정 3-5).
- Hot Tip (f)군(KPI 동기성)은 S5 재료 편집 시 "동기는 버리고 절차만" 규칙 유지.

## 6. Step 3 Human Gate — 결정 기록 (2026-08-31 확정)

| 항목 | 결정 |
|---|---|
| Target Concept 기본 방향 | **승인** (1-1) |
| Evidence Pack 구조 | **8-섹션 확정** — Existing Bank Signals 삭제, §8은 Customer Interaction / CRM Memo로 (1-2·2-8·2-9) |
| Availability | 결정 2-1~2-8대로 확정 — 상세는 EVIDENCE_PACK_SPEC 각 표 |
| HD-6 갱신 | **승인** — Brief를 직원용 Target Output으로 승격 (운영 검증 완료 의미 아님; REV-002/P2 Regression·직원 검증 대상) |
| HD-7 신설 | **승인** — §5 원칙 명문화 |
| SYSTEM_ROLE 원칙 5 | **Candidate Pool 원칙으로 변경 승인** (§4.1) |
| 보류 필드 3건 (피어 통계·식별 메타·TOP3) | **전부 REV-002 제외** (2-10) |
| Missing 슬롯 | Evidence Missing / Required Confirmation 분리 — 14개 목록은 입력에서 제거, 평가 기준으로 이동 검토 (2-11) |
| S5 공급 방식 | Knowledge Pack 수동 동봉 — Retrieval·색인 보류 (3-7) |
| Regression | **8 Case**: GC-03·04·05·09·11·14·16·**17** (Pair 필수 유지; GC-17은 DO 적용 예상시점 해석·F-001 재발을 GC-09와 함께 검증) (5) |

## 7. REV-002 구현 범위 (Step 4)

- `prototype/runtime.py`:
  1. case.md §2를 **8-섹션 Evidence Pack**으로 파싱·직렬화 (F/C/S 라벨·as_of·NULL/0/해당없음 3분 포함)
  2. 전처리 레이어 — Arithmetic Derived + Rule-derived Fact(rule_source·rule_as_of 필드 포함; EVIDENCE_PACK_SPEC §4)
  3. 출력 스키마: 5-섹션 Brief 분해 + `supporting_evidence_ids`/`supporting_knowledge_ids` (구조화 판단부는 REV-001 유지)
  4. deterministic validator 갱신: 기존 C1/C2/C3 유지 + 금지어·형식·구조 필드·Evidence ID 존재 검사 (의미 판정은 Evaluator — EMPLOYEE_BRIEF_SPEC §3)
  5. SYSTEM_ROLE 개정: 원칙 5 → Candidate Pool 원칙(§4.1), Brief 산출 지시(5-섹션)
- Regression: 8 Case `input_v2` (기존 정보량 유지·조직 구조만 변환·새 사실 추가 금지 — 새 스키마에서 제외된 필드의 처리는 보고 §6 항목 참조)
- 보류(§20.8 준수): Retrieval/색인 자동화, Reusable KB, Multi-Agent, 자동 Evaluator.
