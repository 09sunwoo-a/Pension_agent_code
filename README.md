# Pension Agent

개인형IRP 사후관리 의사결정 Agent를 Customer Case 기반으로 개발·검증하기 위한 Repository이다.

## Start Here

새로운 Agent Session은 다음 순서로 시작한다.

1. `README.md`
2. `00_Core_Concept_Design.md`
3. `AGENTS.md` (Golden Batch 운영은 §20)
4. `golden/HUMAN_DECISIONS.md` → `golden/GOLDEN_SET_DRAFT.md`
5. Active Case가 존재한다면 해당 `cases/CASE_xxx/status.md`

## Repository

- `sources/`: 판단 근거 Source Corpus
- `templates/`: Case 개발·실행·평가 표준 Template
- `golden/`: Golden Set(Domain Map · Capability Map · Case Candidates)과 확정 Human Decision
- `cases/`: 실제 Case (CASE_001 = Baseline / GC-00; Golden P0 Case는 `cases/GC-xx/`)
- `prototype/`: Gemma 4 최소 Runtime

## Important Principle

Source Corpus는 Customer Condition → Correct Action 형태의 정답 Rule Base가 아니다.

Agent는 Case에서 필요한 판단지식을 먼저 식별한 뒤 관련 Source를 탐색하고, 실제 원문을 근거로 필요한 Knowledge를 구성한다.

전체 Source Corpus를 기본 Context로 읽지 않는다.
