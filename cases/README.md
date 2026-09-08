# cases/ — Case Artifact

Case 하나가 폴더 하나다. Frozen 된 입력·Run·Evaluation 은 **덮어쓰지 않는다** (`AGENTS.md` §14·§15).

## 폴더 모양이 셋인 이유

입력 형식이 Runtime Revision 마다 달라졌고, `prototype/runtime.py::run_case` 가 폴더 안의 파일로
경로를 고른다. 옛 형식을 새 형식으로 고쳐 쓰지 않는다 — 기존 Run 과의 비교 가능성을 지키기 위해서다.

| 입력 파일 | Runtime 경로 | 해당 Case |
|---|---|---|
| `case.md` (§2 Customer Input) | REV-001 (Judgment-first) | CASE_001, GC-01~17 |
| `case.md` + `input_v2.md` (8-섹션 Evidence Pack) | REV-002 | GC-03·04·05·09·11·14·16·17 (REV-002 Regression 8건) |
| `canonical.json` (9-Block, `design/CANONICAL_CONTRACTS.md`) | v3 | GC-18~25, DIAG-01~03 |

공통: `knowledge_pack.md`(Case-local Knowledge) · `runs/RUN_00n.md` · `evals/EVAL_00n.md` · `status.md`(현재 상태만).

- `CASE_001` 은 GC-00 Baseline 이다. 폴더명은 바꾸지 않았다 — 7개 문서가 `CASE_001` 로 인용한다.
- `DIAG-01~03` 은 Golden Case 가 아니라 **파이프라인 진단용 fixture** 다. Freeze·Evaluation 없이
  `canonical.json` + `knowledge_pack.md` + `runs/` 만 있다 (`golden/HUMAN_DECISIONS.md` HD-P2-GATE2 · `design/P2_BATCH3_CANDIDATES.md` §4 GC-23 항목의 DIAG-03 비교).
- `runs/RUN_00n.md` 는 `prototype/render_run.py` 로 전사한 정리본이다. 원본 JSON record 는
  `prototype/out/`(git 제외) 에만 있다.

## Cross-case Map

| 파일 | 내용 |
|---|---|
| `FAILURE_MAP.md` | 반복 Failure Pattern (F-xxx) 과 Revision Status |
| `KNOWLEDGE_MAP.md` | Case 별 Knowledge 사용·미인용 관찰, Reusable Knowledge 후보 |
| `CONSTRAINT_MAP.md` | Hard Constraint (C1~C3) 와 Case 별 적용 관찰 |
