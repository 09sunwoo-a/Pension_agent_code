# EVAL_002 — GC-01

## 1. Evaluation Metadata
- Case: GC-01 / Run: RUN_002 (`cases/GC-01/runs/RUN_002.md`, Parent RUN_001) / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-01/case.md FROZEN (commit 601aa1b, 변경 없음) / Knowledge Pack: 601aa1b (내용 변경 없음; 전달 필드만 REV-001로 확장) / Runtime: 8cf3787 (REV-001, `prototype/REVISIONS.md`)
- Basis: case.md §5; AGENTS.md §20.6; HD-6 (EVAL_002 Primary = F-005 Action/Change Bias, F-006 Knowledge Under-use; Secondary = F-001, F-002, F-008; Trade-off = 필요 Action 약화 여부)

## 2. Verdict
**PARTIAL** (RUN_001: PARTIAL)

Judgment(추가 확인 우선 / 정보 안내 중심)가 먼저 형성되고, reasoning이 왜 그 판단인지(만기 후 경로·지켜드림 3년제·연금 계획이 만기 길이를 결정·안전자산 선호)를 근거로 말한다. RUN_001에서 미사용이던 K-002(3년제 잠김)가 reasoning에 들어왔고, K-003의 스타뱅킹 예약변경 절차가 Action 3에 반영됐다(F-006·F-007 개선). "디폴트옵션에 맡기기보다"류의 열등 프레이밍이 사라지고 자동 적용 경로가 중립적으로 서술된다(F-005 개선).
잔여: (1) 특별제공 금리·잔여한도·[04-12-17A]·만기 1개월 전 예약 가능 시점(K-004/K-003 세부) 여전히 없음, (2) 고유계정대 200만원 미처리, (3) 만기 길이(1년/3년) 선호 확인 없음(Unknown 2건으로 축소), (4) Action 3 조건이 "연금 수령 계획이 없으며 계속 운용 희망"으로 좁아, 수령 계획이 있어도 필요한 만기 자금 재운용 안내가 조건 밖으로 밀림(Trade-off 관찰 — 필요한 Action 자체는 유지됨).

## 3. Primary — F-005 Action / Change Bias
- Management Judgment가 Next Action보다 먼저 형성되었는가: YES (`management_judgment` → `next_actions`; reasoning이 Context 근거를 제시)
- 변화: 개선 — Judgment 선행, 열등 프레이밍 제거, DO 자동 적용 경로 중립 서술. '지켜드림 수용'을 명시적 선택지로는 두지 않음(경미)
- 필요 Action 약화 / 불필요 변경 수렴 (Trade-off): Action 구체성 유지(원리금보장 내 금리 비교·예약변경 절차). Action 3 조건 과협(수령 계획 있는 경우 분기 없음) — 경미

## 4. Primary — F-006 Knowledge Under-use
- 변화: 개선 — K-002·K-003(예약변경 절차) 사용; K-004 세부(한도·화면·계산기) 여전히 미사용

## 5. Secondary Observation
| Pattern | RUN_001 | RUN_002 |
|---|---|---|
| F-001 Uncertainty Loss | EVAL_001 참조 | 경미 — situation "안전자산 선호 성향으로 분류되며"(K-003 휴리스틱을 사실처럼) |
| F-002 Knowledge Over-application | — | 경미 — 위와 동일(K-003 분류 휴리스틱의 개인 확정) |
| F-008 Structured→Brief Condition Loss | EVAL_001 참조 | 없음 |
| F-004 Confirmation Axis Gap | EVAL_001 참조 | 잔존 — 만기 길이 선호·비대면 가능 여부 미확인 |
| F-007 Employee Next Action | EVAL_001 참조 | 개선 — 스타뱅킹 예약변경 절차; 화면번호 없음 |

## 6. Critical Mistake Check
없음

## 7. Constraint Check
C1 PASS (Action 3 안정형) · C2 PASS · C3 PASS (Runtime deterministic validation; REVIEW 항목 없음)

## 8. Employee Brief (Diagnostic — 의미 보존)
Unknown→Fact 변환 / 조건부→무조건 / Hard Constraint 소실 / Judgment 왜곡 / 고객 의사 왜곡 여부는 §2·§5에 기재. 문장 길이·형식은 평가 대상 아님.

## 9. Evidence
RUN_002 §3 (situation·unknowns), §6 (judgment·reasoning·must_confirm), §7 (Actions), §9 (brief); EVAL_001 대조.

> 이 Artifact는 생성 후 수정하지 않는다.
