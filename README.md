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
- `golden/`: Golden Set(Domain Map · Capability Map · Case Candidates), 확정 Human Decision, Batch Summary (`P0_BATCH_SUMMARY.md`, `REVISION_001_REGRESSION.md`, `P1_BATCH2_SUMMARY.md`)
- `cases/`: 실제 Case (CASE_001 = Baseline / GC-00; Golden P0 Case는 `cases/GC-xx/`)
- `prototype/`: Gemma 4 최소 Runtime

## Windows 사용 안내 (인코딩 깨짐 방지)

이 저장소의 모든 텍스트 파일(`.md` / `.py` / `.json` / `.html`)은 **UTF-8(BOM 없음) · LF**로 저장되어 있으며, `.gitattributes`와 `.editorconfig`가 이를 강제한다. Windows에서 받아서 쓸 때는 다음을 따른다.

1. **ZIP 다운로드보다 `git clone`을 권장한다.** clone/checkout 과정에서 파일 인코딩은 절대 변환되지 않는다.
2. **ZIP으로 받는 경우**: 압축 해제 후 한글 파일명이 깨지면 압축 프로그램 문제다. Windows 10/11 기본 탐색기 압축 풀기 또는 반디집(인코딩 자동 감지)을 사용한다. 구형 알집 등 일부 프로그램은 UTF-8 파일명을 깨뜨릴 수 있다.
3. **파일 내용이 깨져 보이는 경우**: 에디터가 CP949(EUC-KR)로 잘못 연 것이다. VS Code라면 우측 하단 인코딩 표시를 눌러 `UTF-8`로 다시 열고, 기본값도 `"files.encoding": "utf8"`로 설정한다.
4. **Python 실행**: CLI 스크립트(`run_case.py` / `mock_pipeline.py` / `render_run.py`)가 stdout/stderr를 UTF-8로 자체 강제하므로 콘솔·리다이렉트 출력이 깨지지 않는다. 전역으로 확실히 하려면 `set PYTHONUTF8=1`(PowerShell: `$env:PYTHONUTF8=1`)을 권장한다.
5. **git에서 한글 파일명이 `\354...`처럼 표시되는 경우**: 깨진 것이 아니라 표시 설정 문제다. `git config core.quotepath false`로 해결한다.

## Important Principle

Source Corpus는 Customer Condition → Correct Action 형태의 정답 Rule Base가 아니다.

Agent는 Case에서 필요한 판단지식을 먼저 식별한 뒤 관련 Source를 탐색하고, 실제 원문을 근거로 필요한 Knowledge를 구성한다.

전체 Source Corpus를 기본 Context로 읽지 않는다.
