# Planning References

## Purpose

이 디렉터리는 과거 또는 현재 기획 과정에서 생성된 참고자료를 보관한다.

이 자료들은 공식 Source Corpus가 아니며, Agent 판단의 직접적인 Grounding 근거로 사용하지 않는다.

## Files

- `IRP_마케팅_타겟고객_텐션업기반_룰베이스.xlsx` — 기획 단계의 마케팅 타겟 고객 조건 → Target → Action 룰베이스
- `IRP_Agent_목업_더미고객_9Cases_v3.xlsx` — 기획 단계의 목업 더미고객 9 Cases

## Allowed Uses

다음 용도로 참고할 수 있다.

- Customer Case 아이디어 발굴
- Synthetic Customer Input 설계
- 현실적인 고객 데이터 필드 및 값 범위 참고
- 기존 기획에서 고려했던 관리상황 확인
- 테스트 케이스 다양성 검토

## Not Allowed

다음 용도로 사용하지 않는다.

- Hard Constraint의 근거
- 업무 Fact의 직접 근거
- Customer → Action Rule
- Expected Behavior의 정답
- 특정 Solution을 정당화하는 근거
- Agent Runtime Rule Base

특히 `IRP_마케팅_타겟고객_텐션업기반_룰베이스.xlsx`의 조건 → Target → Action 구조를 Runtime Rule로 가져오지 않는다.

`IRP_Agent_목업_더미고객_9Cases_v3.xlsx`를 Case 설계에 참고할 때는 Raw Customer Information만 참고하고, Badge / Target / 시연 포인트 / 추천 Action 등 기획자가 미리 만든 판단결과는 Agent Input으로 사용하지 않는다.

## Repository 운영상 의미

```text
sources/
→ Agent의 판단을 Grounding하기 위한 Source Corpus

references/
→ 설계 및 Case 작성에 참고할 수 있으나 Grounding 근거로 사용하지 않는 보조자료
```

두 영역의 역할을 섞지 않는다.

`references/planning/`의 파일은 `sources/source_registry.md`에 등록하지 않는다.
