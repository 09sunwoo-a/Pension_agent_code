# EVAL_002 — GC-14

## 1. Evaluation Metadata
- Case: GC-14 / Run: RUN_002 (`cases/GC-14/runs/RUN_002.md`, Parent RUN_001) / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-14/case.md FROZEN (commit 9e0cb60, 변경 없음) / Knowledge Pack: 9e0cb60 (내용 변경 없음; 전달 필드만 REV-001로 확장) / Runtime: 8cf3787 (REV-001, `prototype/REVISIONS.md`)
- Basis: case.md §5; AGENTS.md §20.6; HD-6 (EVAL_002 Primary = F-005 Action/Change Bias, F-006 Knowledge Under-use; Secondary = F-001, F-002, F-008; Trade-off = 필요 Action 약화 여부)

## 2. Verdict
**PASS** (RUN_001: PARTIAL)

RUN_001의 PARTIAL 사유가 모두 해소됐다: 신청 가능 시기(계약 체결일부터 잔금 지급일 후 1개월 이내)를 situation·reasoning에서 명시, 기타소득세 16.5%와 세전 신청금액 설정을 Action 2에서 명시, 잔금일(10/15)에 맞춘 재원 계획과 자산별 매도 순서(고유계정대 > 정기예금 > 펀드)·정기예금 중도해지 원금 미달을 Action 4에서 안내(F-006 개선). 무주택 요건·서류 확인 선행, 창구 접수·후선 절차, 상품 권유 금지(K-006) 유지. Judgment(추가 확인 우선 / 정보 안내 중심 / 고객 결정 지원)가 실행 지원 Case에 맞다.
잔여(경미): 내점 시기 확인, 세액공제 미신청분 확인(RUN_001에 있었음) 탈락, 펀드 환매 소요일 수치 없음. 핵심 판단·Fact·Confirmation 누락이 없어 PASS.

## 3. Primary — F-005 Action / Change Bias
- Management Judgment가 Next Action보다 먼저 형성되었는가: YES (`management_judgment` → `next_actions`; reasoning이 Context 근거를 제시)
- 변화: 해당 없음(절차형) — 판단 우선 구조 유지
- 필요 Action 약화 / 불필요 변경 수렴 (Trade-off): Action 구체성 향상(4개 Action, 순서·조건)

## 4. Primary — F-006 Knowledge Under-use
- 변화: 개선 — K-001 시기·16.5%, K-004 매도 순서·잔금일 사용

## 5. Secondary Observation
| Pattern | RUN_001 | RUN_002 |
|---|---|---|
| F-001 Uncertainty Loss | EVAL_001 참조 | 없음 |
| F-002 Knowledge Over-application | — | 없음 |
| F-008 Structured→Brief Condition Loss | EVAL_001 참조 | 없음 |
| F-004 Confirmation Axis Gap | EVAL_001 참조 | 경미 — 내점 시기; 미신청분 확인 탈락 |
| F-007 Employee Next Action | EVAL_001 참조 | 개선 — 창구 절차·매도 순서 |

## 6. Critical Mistake Check
없음

## 7. Constraint Check
C1 PASS · C2 PASS · C3 PASS (Runtime deterministic validation; REVIEW 항목 없음)

## 8. Employee Brief (Diagnostic — 의미 보존)
Unknown→Fact 변환 / 조건부→무조건 / Hard Constraint 소실 / Judgment 왜곡 / 고객 의사 왜곡 여부는 §2·§5에 기재. 문장 길이·형식은 평가 대상 아님.

## 9. Evidence
RUN_002 §3 (situation·unknowns), §6 (judgment·reasoning·must_confirm), §7 (Actions), §9 (brief); EVAL_001 대조.

> 이 Artifact는 생성 후 수정하지 않는다.
