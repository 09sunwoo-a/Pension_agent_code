# Prototype — Minimal Gemma 4 Runtime

## Purpose

Frozen Case 하나를 Target Base LLM으로 End-to-End 실행하고, **어느 단계에서 실패하는지 관찰**하기 위한 가장 작은 Runtime이다. 완성형 Agent Architecture가 아니며, `00_Core_Concept_Design.md`의 Conceptual Flow를 코드 Node로 옮기지 않는다.

## Target Model

```text
Model    : gemma-4-31b-it
API      : Google Generative Language API (REST, generateContent)
Endpoint : https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent
Auth     : GEMINI_API_KEY (environment variable)
```

`generationConfig`는 보내지 않는다(API 기본값). Model / Variant / Generation 설정 변경은 `AGENTS.md` §9·§17에 따라 Semantic Change다.

## Dependencies

- Python 3.9+
- **Standard library only**: `os`, `json`, `re`, `pathlib`, `urllib.request`, `urllib.error`, `datetime`, `dataclasses`, `typing`, `hashlib`, `subprocess`(git HEAD 기록용, 실패해도 무시)
- 외부 패키지 없음. Google SDK / requests / pydantic 등을 사용하지 않는다.

## GEMINI_API_KEY

```bash
export GEMINI_API_KEY="..."        # 셸 프로필(~/.zshrc 등)에 두는 것을 권장
```

Key 값은 Repository, 코드, `.env`, Run 출력 어디에도 기록하지 않는다. 미설정 시 `CONFIG_ERROR: GEMINI_API_KEY is not set`으로 종료한다.

## Run

```bash
# Repository root에서
python prototype/run_case.py CASE_001                # 실제 Gemma 4 호출
python prototype/run_case.py CASE_001 --dry-run      # Prompt만 구성 (API 호출 없음)
python prototype/run_case.py CASE_001 --show-prompt  # 실제 전달 Prompt 전문 출력
python prototype/run_case.py CASE_001 --out some.json
```

기본 출력: `prototype/out/<CASE>_<timestamp>.json` (Run record). `out/`은 git에서 제외된다.

## Runtime Flow (REV-001, prototype/REVISIONS.md)

```text
cases/<CASE>/case.md §2 Customer Input (bullet lines, verbatim; [Customer-stated]/[Event] 태그 인식)
→ Constraint Context (deterministic): C1 투자성향 상한 / C2 펀드 위험등급 Eligibility (HD-2.1) / C3 디폴트옵션 Eligibility
→ cases/<CASE>/knowledge_pack.md K-items — Knowledge / Case Relevance / Usage Boundary(Limitation) / Authority·As-of / Source 전달 (Case-local Interpretation 미전달)
→ Prompt (역할·원칙[판단 우선·방향 중립·Knowledge Usage] / 고객정보 / Constraint / Knowledge / 출력형식)
→ gemma-4-31b-it REST call
→ JSON parse + schema check: current_situation → known_facts → unknowns → management_judgment{judgment, reasoning, must_confirm_before_action} → next_actions[{action, kind, condition, risk_level}] → employee_brief
→ deterministic validation: C1 (next_actions[].risk_level) / C2 (불가 등급 라벨: action=FAIL, condition·brief=REVIEW) / C3 (불가 포트폴리오명: action=FAIL, condition·brief=REVIEW)
→ run record JSON  (python prototype/render_run.py <record> --run-id RUN_00n --out cases/<CASE>/runs/RUN_00n.md 로 전사)
```

Management Judgment 유형: `개입 필요 / 추가 확인 우선 / 현 상태 유지 가능 / 정보 안내 중심 / 고객 결정 지원 / 실행 불가` (복수 가능). 어느 것도 기본값이 아니며, `현 상태 유지 가능`도 Next Action(유지·재점검 조건)을 가진다. `employee_brief`는 최종 UI가 아니라 구조화 판단이 자연어로 옮겨질 때 의미가 보존되는지 보는 Diagnostic Output이다.

## Run Record (observable fields)

`runtime_revision`, `customer_input`, `constraint_context`, `knowledge_ids_used`, `knowledge_fields_sent`, `prompt`(5 sections), `model_response`(status/http/finish/usage/error), `raw_model_output`, `json_normalizations`, `parsed_output`, `schema_errors`, `validation`(C1), `validation_c2`, `validation_c3`, `judgment_types_detected`, `employee_brief`, `status`, `error`, file sha256 of the frozen case / knowledge pack, git HEAD.

Status values: `CONFIG_ERROR`, `HTTP_ERROR`, `API_ERROR`, `EMPTY_RESPONSE`, `JSON_PARSE_ERROR`, `SCHEMA_ERROR`, `VALIDATION_ERROR`, `SUCCESS` (and `DRY_RUN`).

Hidden chain-of-thought는 요청하지도 저장하지도 않는다(thought-flagged part는 버림). Credential은 어떤 필드에도 저장하지 않는다.

## Supported Cases

- `CASE_001` (Frozen Baseline / GC-00 — RUN_001은 pre-REV-001 스키마)
- Golden P0: `GC-01, GC-03, GC-04, GC-06, GC-10, GC-12, GC-14, GC-16` (RUN_001 = 601aa1b, RUN_002 = REV-001)

§2 Customer Input에 `투자성향:` 항목이 있고 knowledge_pack.md가 있으면 같은 방식으로 실행된다.

## Not Implemented (intentionally)

```text
- Dynamic Retrieval / RAG / Vector DB / Embedding / Knowledge Graph
- LangGraph / LangChain / Multi-Agent / Planner-Executor / Tool Calling
- Product Recommendation / Portfolio optimization (C2 grade eligibility validation은 구현됨)
- Evaluator (EVAL) / RUN_001 artifact generation (run record is a smoke-test output, not a formal RUN artifact)
- Retry / backoff / streaming / async / production logging / monitoring
- Structured-output API mode (JSON is requested in the prompt and parsed with json.loads)
- UI / DB / customer memory
- Any deterministic rule beyond C1/C2/C3 (Expected Behavior stays with the Evaluator)
- Brief↔Reasoning preservation validation (F-001/F-008 — REV-001에서 보류)
```
