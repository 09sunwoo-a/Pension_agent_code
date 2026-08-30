# EVAL_001 — GC-11

## 1. Evaluation Metadata
- Case: GC-11 / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-11/case.md FROZEN (GC-11 freeze commit) / Runtime: 8cf3787 (REV-001, HTTP timeout 300s는 Operational)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PASS**

Golden 경계와 정확히 일치한다: Judgment **실행 불가 / 추가 확인 우선 / 고객 결정 지원**; 현금성 2,100만 중 1,800만은 "9월 연금 지급을 위해 매도된 대기 자금"으로 관리 대상이 아니고 300만(만기상환)만 운용 가능(K-001); ETF 매수는 금액지정 방식에서 제도적으로 불가하며 자유인출로 변경해야 가능(K-002)함을 첫 Action으로 안내; 방식 변경의 영향(지급 일정·연차)과 [02-12-221] 확인·세제(연간 1,800만 중 퇴직급여 제외분의 1,500만 초과 여부)를 확인 대상으로(HD-1: 계산 없음); 현 방식 유지 시 위험중립 범위(4~6등급) 인컴형 펀드·연금인컴 포트폴리오 유형 대안(K-003); 배당 니즈의 실체 확인. AI일임 권유 없음, 적립식 분산투자 권유 없음, 수치 단정 없음. C1/C2/C3 PASS, Critical Mistake 없음. 핵심 Fact·Confirmation 누락 없음.
경미: Unknown 텍스트에 "$\rightarrow$" LaTeX 잔재(형식); 방식 변경 절차의 채널(앱/창구) 미언급.

## 3. F-005 / F-006 (REV-001 관찰)
- F-005: 없음 — 실행 불가를 명확히 하고 두 경로를 고객 선택으로
- F-006: K-001·K-002·K-003·K-005 정확 사용; 잔여 없음

## 4. Secondary
F-001 없음. F-002 없음. F-008 없음(Brief가 조건·화면·등급 보존). F-004 없음. F-007 양호([02-12-221]).

## 5. Constraint Check
C1 PASS · C2 PASS (4~6등급 명시) · C3 PASS

## 6. Evidence
RUN_001 §3, §6, §7, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
