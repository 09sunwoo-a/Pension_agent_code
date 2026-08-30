# P0 Golden Discovery Batch — Summary (BATCH_001)

- 실행일: 2026-08-31 / Builder: Gemma 4 (`gemma-4-31b-it`, API default) / Evaluator: Claude (별도 Context)
- Runtime: `601aa1b` (Execution-enabling 변경 포함, HD-5.1) / 각 Case 1회 실행 (§20.1)
- 정책: `AGENTS.md` §20, `golden/HUMAN_DECISIONS.md` HD-1~5. Case-specific Prompt Patch 없음. Stop Condition 발생 없음.

## 1. 결과

| Case | Title | Verdict | Critical | Hard Constraint | 핵심 관찰 |
|---|---|---|---|---|---|
| GC-01 | 정기예금 만기 · 안정추구형 | PARTIAL | 없음 | C1/C3 PASS | 제도 정확(재예치 없음·DO); 현상유지 경로 부재, 3년제 잠김·화면·예약 시점 누락 |
| GC-04 | 공격투자형 · 예금 100% (Negative) | PARTIAL | 없음 | PASS | KPI 분류 명시적 분리, 의사 존중; "현 상태 유지 합리" 미명시·라벨 "관리 필요" |
| GC-03 | 퇴직금 7일차 · DO 미등록 | PARTIAL | 없음 | PASS | 확인 우선·DO 의무·개시 불가 정확; 인출 세금 구조 미사용, Brief C1 축소 재진술(F-008) |
| GC-06 | 판매중단펀드 −38% | PARTIAL | 없음 | PASS (C3 REVIEW→PASS) | 톤·채널·분할매도 양호; **TM 리스트를 관리 근거로(F-009 P1)**, 유지 경로 부재 |
| GC-10 | 개시 요건 충족 · 운용 지속 | PARTIAL | 없음 | PASS | 개시 강요 없음·제약 정확; 수령 구조·ETF 조건·TDF 관점 미사용, 63세 추론 확정 |
| GC-12 | 퇴직금 3억 · 1억 사용 | PARTIAL | 없음 | PASS | 두 경로·추가입금 불가 정확; **Brief에서 한도 조건 소실(F-008 P1)**, [02-12-221] 연결 없음 |
| GC-14 | 중도인출 | PARTIAL (PASS 경계) | 없음 | PASS | 절차·세전 역산·권유 금지 정확; 신청 시기·역산 일정 누락 |
| GC-16 | 증권사 실물이전 | PARTIAL (PASS 경계) | 없음 | PASS | 사전체크·정직한 인정·비대면 전환·분리 운용; 고객 결정권·절차 세부 누락 |

**8/8 PARTIAL, 0 FAIL, 0 PASS.** 판단형 Case(01/04/10)보다 절차형 Case(14/16/06)의 Brief 품질이 높았다.

## 2. Cross-case Failure Evidence (FAILURE_MAP 요약)

| Pattern | Sev | Cases (CASE_001 포함) | 본질 |
|---|---|---|---|
| **F-006** Provided Knowledge Under-use | P2 | 8/8 | 전달된 K-item 중 상품·절차·제도 구조 항목이 인용되지 않거나 항목 내부 세부(시한·세율·화면)가 탈락 → 판단이 제도 Fact 수준에서 멈춤 |
| **F-005** Non-change / Customer-decision Path Absent | P1 | 6 (+CASE_001) | Solution 후보에 "현 상태 유지 / 고객 결정 경로"의 자리가 없어 후보가 변경·유지방어로만 구성되고 decision 라벨이 "관리 필요"로 수렴 |
| **F-004** Confirmation Axis Gap | P2 | 5 (+CASE_001) | 확인 항목이 2~3건으로 축소, 선호·채널·시기 축 누락 |
| **F-001** Uncertainty Loss (Structured→Brief) | P3 | 5 (+CASE_001) | situation의 추론·가능성 표기가 Brief에서 확정 표현으로 변환 ("방치", "전형적인", "63세 전까지") |
| **F-007** Employee Next Action Absent | P2 | 4/5 (GC-06 미재현) | 화면·채널·시점 없음 |
| **F-008** Constraint / Condition Drift (Structured→Brief) | P2 (GC-12 P1) | 2 | Candidate의 condition·Constraint 범위가 Brief에서 탈락·변형 (한도 조건 소실 → 오안내 위험) |
| **F-009** Marketing Trigger as Management Basis | P1 | 1/8 (비결정적) | TM 리스트 포함을 관리 필요 근거로 사용 (D10) |
| F-003 Provided Fact Omission | P2~3 | 4 | 입력 Fact(채널·입금예정상품·퇴직급여 포함) 미사용 |

## 3. Architecture Revision Proposal 후보 (Human Gate — 승인 전 구현하지 않음)

§20.5: 반복 Cross-case Evidence가 확보된 항목만 올린다. 구현 방식은 미확정이며 §20.8 미결정 목록과 충돌하지 않도록 "무엇을 검토할지"만 제시한다.

| 순위 | 대상 Pattern | Evidence | 검토 방향 (제안, Semantic Change → Gate) |
|---|---|---|---|
| **1** | F-005 (6 Case) + decision 라벨 수렴 | 모든 판단형 Case | Solution 후보/Decision Outcome에 "현 상태 유지 · 확인 후 판단 · 고객 결정 지원" 결과의 **명시적 자리**; `management_need.decision` 어휘를 "관리 필요/정보안내/현상유지" 등으로 구조화 — §20.8의 "Solution vs Decision Outcome 분리" 결정과 연결 |
| **1** | F-006 (8/8) | 전 Case | Knowledge 전달 방식: 관련도 단서(Case Relevance) 또는 Limitation 전달(Gate D 기존 후보), 항목 수 축소, 제도 구조 항목의 "필수 인용" 표시 — Prompt/Knowledge Semantic Change |
| **2** | F-001 + F-008 (Structured→Brief 변형, 7건) | GC-03/10/12 등 | Post-Reasoning Validation에 **Brief ↔ Candidate/Constraint 대조 검사**(조건 소실·범위 축소·확정화 검출) — §20.8 "Execution Validation 구체 구현"과 별개의 Presentation Validation |
| **3** | F-007 (4/5) | 판단형 Case | employee_brief 지시에 "확인 화면 · 채널 · 시점 · 직원/고객 역할" 항목 — Schema Semantic Change |
| **3** | F-009 (1/8) | GC-06 | Marketing 태그 Knowledge/입력 Fact의 전달 방식(경고를 Fact와 같은 자리에) — 재현성 낮아 Batch 2에서 재관찰 후 |

## 4. Human Gate 요청 항목 (Batch 종료 시점)

1. **C2 성향↔펀드 위험등급 Eligibility 매핑표 정의** — HD-2로 Constraint는 확정됐으나 구체 표가 어떤 Source에도 없어 Runtime은 DETECT_ONLY 로만 구현됨(`prototype/runtime.py` `detect_c2_fund_grades`). P0 Batch에서는 실제 위반 후보가 발생하지 않아 영향은 없었음. P1 Case(GC-02/05/17)에서 필요.
2. **§3 Revision Proposal 1순위 2건(F-005, F-006)의 검토 승인 여부** — 승인 시 변경 목적·허용 범위만 정해 주면 Builder가 구현하고 P0 8 Case Regression(RUN_002)을 수행.
3. (선택) F-001/F-008 Brief 대조 Validation을 같은 Revision에 포함할지, 별도 Revision으로 둘지.

이 3건은 모두 §20.3 Human Gate 정의(새 판단 규칙·Schema 의미 변경)에 해당하므로 Agent가 임의로 진행하지 않았다.

## 5. Batch 중 수행한 Execution-enabling Runtime Change (HD-5.1, 기록)

- `prototype/runtime.py` (601aa1b): C3 디폴트옵션 Eligibility validator(승인 매핑 그대로; direction에 불가 포트폴리오명 → FAIL, condition/brief → REVIEW) 및 Constraint Section에 C3 가입 가능/불가 전달; C2 detect-only; Customer Input에 `[Customer-stated]`/`[Event]` 태그가 있으면 provenance note를 그에 맞게 선택(serialization 정확성); C1 basis 문구를 HD-2로 갱신.
- `prototype/run_case.py`: C3/C2 결과 출력. `prototype/render_run.py`: run record → RUN_xxx.md 전사 헬퍼(판단 없음).
- 입력 스키마 확장은 필요 없었다 — case.md §2 bullet(중첩 허용)로 만기·DO 상세·PENSION·[Event]·고객 발화를 모두 표현 가능했다.
- C3 REVIEW 등급은 부정문 미구분 때문이며, GC-06에서 Evaluator가 PASS로 확정했다(정상 동작).

## 6. 재현성·해석 주의

- 각 Case 1회 실행이므로 Pattern의 재현율은 Case 간 반복(Cross-case)으로만 판단했다. F-009처럼 1/8인 항목은 Batch 2에서 재관찰이 필요하다.
- Evaluator(Claude)가 Case·Knowledge Pack 작성자와 동일 주체다. Semantic Boundary는 Golden Draft(Human-approved)에 고정되어 있어 평가 기준 자체는 독립적이나, Knowledge Pack 구성이 Builder 성능에 영향을 준다는 점은 F-006 해석 시 고려해야 한다.
- 모든 RUN/EVAL Artifact는 Immutable. Raw record는 `prototype/out/GC-xx_RUN_001.json`(git-ignored, 로컬).

## 7. 다음 단계

```text
Human Gate (§4 1~3)
→ 승인 시: Revision(변경 목적·범위) → P0 8 Case RUN_002 Regression → EVAL_002 → FAILURE_MAP 갱신
→ 이후 P1 Case (GC-02, 05, 07, 08, 09, 11, 13, 15, 17) Batch 2
```
