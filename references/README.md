# references/ — 참고자료 (Grounding 근거 아님)

`sources/` 가 Agent 판단을 Grounding 하는 Source Corpus 라면, `references/` 는 설계·Case 작성에
참고할 수는 있으나 판단 근거로 인용하지 않는 보조자료다. `sources/source_registry.md` 에 등록하지 않는다.

| 폴더 | 내용 | 규칙 |
|---|---|---|
| `planning/` | 기획 단계 xlsx 2건 (타겟 룰베이스 · 목업 더미고객 9 Cases) | `planning/README.md` — Customer → Action Rule 로 가져오지 않는다 |
| `06_주제별_추출지식/` | 2026-08-17 에 corpus 01~04 전체를 주제 5축(고객세그먼트 · IRP관리방법론 · 영업화법 · 제도상품팩트 · 업무처리절차)으로 추출·재구성한 **검토 자료**. 문서 스스로 «팀 논의·취사선택용, 에이전트 구현 스키마 아님» 이라 밝힌다 | 원문이 아니라 파생물이다. 판단 근거가 필요하면 각 문서가 가리키는 corpus 원문으로 돌아간다 |

`06_주제별_추출지식/` 은 `09sunwoo-a/pension_agent` 저장소의 같은 이름 폴더를 옮겨온 것이며 폴더명을
그대로 두었다. 이 저장소의 `sources/corpus/06_공식기준_Human확인/` 과는 무관하다.
