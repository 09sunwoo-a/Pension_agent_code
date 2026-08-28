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

## Runtime Flow

```text
cases/<CASE>/case.md §2 Customer Input (bullet lines, verbatim)
→ C1 Constraint Context (투자성향 → allowed / forbidden levels, deterministic)
→ cases/<CASE>/knowledge_pack.md K-items (Knowledge / Authority·Status 필드만 — Limitation·Case Relevance·Interpretation은 미전달)
→ Prompt (역할·원칙 / 고객정보 / Constraint / Knowledge / 출력형식)
→ gemma-4-31b-it REST call
→ JSON parse (code fence 제거·바깥 중괄호 슬라이스만 허용) + 최소 schema check
→ deterministic C1 validation (solution_candidates[].risk_level)
→ run record JSON
```

## Run Record (observable fields)

`customer_input`, `constraint_context`, `knowledge_ids_used`, `knowledge_fields_sent`, `prompt`(5 sections), `model_response`(status/http/finish/usage/error), `raw_model_output`, `json_normalizations`, `parsed_output`, `schema_errors`, `validation`, `employee_brief`, `status`, `error`, file sha256 of the frozen case / knowledge pack, git HEAD.

Status values: `CONFIG_ERROR`, `HTTP_ERROR`, `API_ERROR`, `EMPTY_RESPONSE`, `JSON_PARSE_ERROR`, `SCHEMA_ERROR`, `VALIDATION_ERROR`, `SUCCESS` (and `DRY_RUN`).

Hidden chain-of-thought는 요청하지도 저장하지도 않는다(thought-flagged part는 버림). Credential은 어떤 필드에도 저장하지 않는다.

## Supported Cases

- `CASE_001` (Frozen — `cases/CASE_001/case.md`, `cases/CASE_001/knowledge_pack.md`)

다른 Case는 §2 Customer Input에 `투자성향:` 항목이 있고 knowledge_pack.md가 있으면 같은 방식으로 실행되지만, 검증된 것은 CASE_001뿐이다.

## Not Implemented (intentionally)

```text
- Dynamic Retrieval / RAG / Vector DB / Embedding / Knowledge Graph
- LangGraph / LangChain / Multi-Agent / Planner-Executor / Tool Calling
- Product Recommendation / Product risk-grade mapping / Portfolio optimization
- Evaluator (EVAL) / RUN_001 artifact generation (run record is a smoke-test output, not a formal RUN artifact)
- Retry / backoff / streaming / async / production logging / monitoring
- Structured-output API mode (JSON is requested in the prompt and parsed with json.loads)
- UI / DB / customer memory
- Any deterministic rule beyond C1 (Expected Behavior stays with the Evaluator)
```
