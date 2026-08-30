# Architecture Revision #1 (REV-001) — P0 RUN_002 Regression Report

- Revision: `prototype/REVISIONS.md` REV-001 (Human-approved HD-6, 2026-09-01) / Before 601aa1b → After 8cf3787
- Regression: P0 8 Case × RUN_002 (Gemma 4, API default, 각 1회) / EVAL_002 (Claude). Case·Knowledge Pack 내용 변경 없음(Frozen); 전달 필드만 확장.
- Stop Condition: 없음. C1/C2/C3 deterministic validation: 8/8 PASS (REVIEW 0).

## A. Architecture Revision #1 구현 — Management Judgment / Action 구조

기존 `management_need{decision, reason} → solution_candidates[]` 는 "관리 필요 여부 → 해결책" 구조여서 decision 라벨이 "관리 필요"로 수렴하고 후보가 변경 방향으로만 채워졌다(F-005). REV-001은 다음으로 바꿨다.

```text
current_situation → known_facts / unknowns
→ management_judgment { judgment: 개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가 (복수 가능),
                        reasoning: 왜 이 상태인가·의도·사용계획·시한·관리 필요성의 실재,
                        must_confirm_before_action[] }
→ next_actions [ { action, kind: 변경/유지/확인/정보안내/절차/연계, condition, risk_level } ]
→ employee_brief (Diagnostic Output)
```

SYSTEM_ROLE에 원칙 8~10을 추가했다: 판단이 Action보다 먼저 / 어느 방향도 기본값이 아님(변경도 유지도 정답, "관리 필요 ≠ 변경 필요", 성향은 상한) / Knowledge의 Case Relevance·Usage Boundary까지 사용. Schema check는 judgment 유형 라벨 검출·kind·risk_level을 검사하고, C1/C3 validator는 `next_actions` 기준으로 동작한다. Judgment 유형 목록은 Ontology로 고정하지 않았다(자유 서술 안에서 검출).

## B. Knowledge Usage 변경

`KNOWLEDGE_FIELDS_SENT = (Knowledge, Case Relevance, Limitation→"Usage Boundary", Authority / Status→"Authority / As-of", Source / Location)`. Case-local Interpretation은 계속 미전달(정답 힌트). Knowledge 항목 수·내용은 늘리지 않았다(Pack Frozen). 이유: P0 8/8에서 관찰된 F-006은 "Knowledge 부재"가 아니라 "왜 지금·어디까지"가 전달되지 않은 문제라는 가설(HD-6). Prompt 크기는 GC-01 기준 7.4K → 11.7K chars.

## C. C2 Validator

- 매핑(HD-2.1, SRC-096 Human-confirmed Official): 안정형 6 / 안정추구형 5~6 / 위험중립형 4~6 / 적극투자형 3~6 / 공격투자형 1~6; 등급 1 매우높은위험 … 6 매우낮은위험. 투자성향 = 최대 허용 위험 제한.
- 구현: Constraint Section에 "권유 가능/불가 등급" 전달(Pre) + `validate_c2_fund_grade`(Post): action 텍스트에 불가 등급 라벨 → FAIL, condition/brief → REVIEW(부정문·기존 보유 가능), situation의 기존 보유는 검사 안 함. 라벨 매칭은 긴 라벨 우선("매우높은위험"이 "높은위험"으로 오검출되지 않음).
- Traceability: `sources/corpus/06_공식기준_Human확인/투자성향별_펀드위험등급_투자권유기준.md` + `source_registry.md` SRC-096 (Status HUMAN_CONFIRMED — 원문 확보 시 교체), `cases/CONSTRAINT_MAP.md` C2, `golden/HUMAN_DECISIONS.md` HD-2.1.
- RUN_002 관찰: GC-06에서 모델이 C2를 실제로 사용해 "'보통위험' 이하 대안 상품군"으로 범위를 좁힘. 위반 후보 0.

## D. RUN_001 vs RUN_002

| Case | RUN_001 | RUN_002 | F-005 변화 | F-006 변화 | Action 품질 Side Effect |
|---|---|---|---|---|---|
| GC-01 만기·안정추구 | PARTIAL | PARTIAL | 개선 — Judgment 선행, 열등 프레이밍 제거, DO 경로 중립; '지켜드림 수용' 선택지 미명시(경미) | 개선 — K-002 3년제·K-003 예약변경 절차 사용; K-004 한도·화면 잔존 | Action 유지. Action 3 조건 과협(F-010 경미) |
| GC-04 공격형·예금100 | PARTIAL | **PASS** | 해소 — "현 상태 유지 가능" 명시, kind=유지 | 해소 — K-005 2주 규칙 적용 | 없음 |
| GC-03 퇴직금 7일차 | PARTIAL | PARTIAL | 개선 — 확인 우선 유지, 조기 결론 없음 | 개선 — K-004 세금 구조 사용; K-005 환급 잔존 | 확인 후 조건부 운용 분기 탈락(F-010) |
| GC-06 판매중단펀드 | PARTIAL | PARTIAL | 개선 — 유지/분할/전량 선택지 명시, TM 근거 제거(F-009 해소) | 개선 — C2 사용; 원인 분석·재개 가능성 잔존 | 필요 Action 유지(비교 자료·내점·분할). 2026-01 매매 확인 탈락 |
| GC-10 개시요건·운용지속 | PARTIAL | PARTIAL | 개선 — DO 수용 경로 명시, 개입=만기 한정 | 개선 — K-003 자유인출 ETF 사용; K-004 TDF·수령 구조 잔존 | 세액미공제 확인 탈락(경미); F-001 잔존(63세) |
| GC-12 퇴직금 3억 | PARTIAL | PARTIAL | 개선 — 상충 관계 안내·고객 결정, "무조건 권유보다는" 명시 | 개선 — 한도 개념 Action 복원; [02-12-221] 잔존 | Action 유지. Brief 한도 조건 생략(F-008 경미) |
| GC-14 중도인출 | PARTIAL | **PASS** | 해당 없음(절차형) | 개선 — 시기·16.5%·매도 순서·잔금일 사용 | Action 구체성 향상 |
| GC-16 증권사 이전 | PARTIAL | PARTIAL | 해소 — 고객 결정 경로(전출 절차 지원) 명시 | 개선 — [04-12-613]; 절차 세부 잔존 | 분리 운용 부분 대안 탈락(F-010) |

Verdict: PARTIAL 8 → PARTIAL 6 · PASS 2. Critical Mistake 0 → 0. Hard Constraint 위반 0 → 0.

## E. Cross-case Failure 변화

| Pattern | 기존 (RUN_001, CASE_001 포함) | RUN_002 |
|---|---|---|
| **F-005** Action / Change Bias | 6 Case (강함 4, 경미 2) | **0 강함 / 1 경미** (GC-01 수용 선택지 미명시) |
| **F-006** Knowledge Under-use | 8/8 | **핵심 K 사용 8/8 개선; 경미 잔존 5/8** (세부·화면 수준) |
| F-002 Knowledge Over-application | CASE_001 3/3 (P0 개별 추적 없음) | 경미 1/8 (GC-01 K-003 분류 휴리스틱의 개인 확정) — 악화 없음 |
| F-001 Uncertainty Loss | 5 Case | **2/8** (GC-01 경미, GC-10 잔존·악화: 63세 확정이 situation으로) |
| F-008 Structured→Brief Condition Loss | 2 | **1/8 경미** (GC-12 Brief 한도 생략; Action에는 존재) |
| F-004 Confirmation Axis Gap | 5 | 5/8 — 변화 없음 (REV-001 대상 아님) |
| F-007 Employee Next Action Absent | 4/5 | **2/8** (부수 개선: 채널·절차·화면) |
| F-009 Marketing Basis | 1 | **0/8** |
| F-010 Downstream Option Narrowing (신규 후보) | — | 3/8 경미 |

## F. 새로운 Failure / Trade-off

- **Intervention Avoidance Bias는 관찰되지 않았다.** 실제 개입이 필요한 GC-01(만기 안내·예약변경 절차)·GC-06(비교 상담 준비·분할매도·내점)에서 필요한 Action이 유지됐고, GC-10은 만기 자금에 '개입 필요'를 명시했다. 현상유지가 맞는 GC-04는 유지로, 확인 우선인 GC-03은 확인으로, 고객 결정인 GC-16/12는 결정 지원으로 수렴했다.
- 대신 **F-010 Downstream Option Narrowing**(경미, 3/8)이 나타났다: Judgment에 맞는 Action만 생성하면서 RUN_001에 있던 조건부 하류 분기(GC-03 "확인 후 운용 방향")·부분 대안(GC-16 분리 운용)·과협 조건(GC-01)이 탈락. 필요 Action 약화가 아니라 선택지 폭의 축소이며, Batch 2에서 재관찰 후 판단.
- Judgment 유형 분포: 추가 확인 우선 6 / 정보 안내 중심 7 / 고객 결정 지원 5 / 현 상태 유지 가능 1 / 개입 필요 1 / 실행 불가 0. "정보 안내 중심"이 거의 모든 Case에 붙는 경향 — 방향 중립 위반은 아니지만 라벨의 변별력이 낮아질 수 있음(관찰).
- GC-10의 F-001이 situation 단계로 이동(악화)한 것은 REV-001과 무관한 Builder 추론 경향으로 보이나 1회 관찰.

## G. Revision #2 필요성 — Evidence만 제시 (자동 구현 없음)

| 질문 | 답 (Evidence) |
|---|---|
| Action / Change Bias는 실제로 감소했는가? | **예.** 강한 재현 4→0. Judgment 라벨이 Golden 결론과 일치(GC-04 유지, GC-03 확인, GC-16 결정 지원, GC-12 상충 안내). decision "관리 필요" 수렴 소멸. |
| 필요한 Action까지 약화되지는 않았는가? | **약화되지 않았다.** GC-01/06/10/14 Action 구체성 유지 또는 향상. 다만 하류 조건부 분기·부분 대안 축소(F-010, 3/8 경미). |
| Knowledge Under-use는 감소했는가? | **예.** RUN_001 미사용 핵심 K-item이 8/8에서 사용됨(3년제 잠김, 2주 규칙, 인출 세금, C2 등급, 자유인출 ETF, 한도 개념, 신청 시기·16.5%, [04-12-613]). 잔여는 항목 내부 세부·화면번호 수준(5/8 경미). |
| Usage Boundary 전달은 효과가 있었는가? | **있었다고 볼 근거가 있다.** F-009(TM 근거) 0/8, F-001 5→2, "방치"·"강력히" 소멸, C1 재진술 정확화(GC-03). 단 1회 실행이라 인과 확정은 아님. |
| F-001/F-008 전용 Validation이 필요한가? | **아직 판단 유보.** 잔존 F-001 2/8(그중 GC-10은 situation 단계 문제라 Brief Validator로 잡히지 않음), F-008 1/8 경미. Batch 2(P1 9 Case)에서 재현율을 본 뒤 결정하는 것이 §20.5에 부합. |
| Reusable Knowledge 설계를 시작할 만큼 Knowledge 표현이 안정됐는가? | **부분적.** 5개 필드 구조(Knowledge/Case Relevance/Usage Boundary/Authority·As-of/Source)는 8 Case에서 문제없이 동작했고 KNOWLEDGE_MAP의 Reusable 후보 8종(DO 시계, 현금성≠미운용, 성향=상한, 개시 요건, 개시 후 제약, 채널 규제, KPI 분리, 수령 구조)은 모델 인용률이 높다. 그러나 "Case Relevance"는 Case별로 다시 써야 하므로 공통 KB로 옮길 때 분리가 필요하다 — §20.8 결정 사항으로 남긴다. |

### Revision #2 후보 (Evidence 기반, 구현 보류)
1. F-004 Confirmation Axis Gap — REV-001에서 다루지 않았고 5/8 잔존. `must_confirm_before_action`이 생겼으나 Unknown 수는 늘지 않음.
2. 화면·시한 세부(F-006 잔여·F-007 잔존) — Knowledge 항목 내부의 "화면번호·시한"이 탈락하는 경향; Knowledge 표현(세부를 별도 필드로) 또는 Brief 구조 검토.
3. F-010 — Judgment-첫 구조에서 조건부 하류 분기의 자리.
4. F-001/F-008 — Batch 2 재현율 후.

## H. 다음 단계

```text
Human 검토 (이 보고서)
→ P1 Case Batch 2 (GC-02, 05, 07, 08, 09, 11, 13, 15, 17) — REV-001 Runtime으로 RUN_001
→ F-004 / F-010 / F-001·F-008 재현율 축적 → Revision #2 판단
```
