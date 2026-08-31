# EVAL_002 — GC-22 (Regression Control: 기존 정상 동작 후퇴 확인)

- Run: RUN_002 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context) / 평가 범위: 목적 한정 (Control). Runtime commit d6edbe4. Input Baseline 불변 (sha e45a35cf…).

## Verdict (목적 한정)
**어휘 수준 후퇴 1건 (deterministic FAIL — Critical Semantic Failure 아님)**

- RUN status VALIDATION_ERROR — 금지어 "방치" 1건. 원문: "'디폴트옵션'이 아직 등록되지 않았습니다. 이는 운용 지시가 없을 때 **자금이 방치되지 않도록 돕는** 법적 의무 설정이므로 …" — **DO 제도의 목적을 설명하는 부정형 일반론**으로, 고객 상태를 방치로 확정한 RUN_001 GC-18 유형(의미 승격)과 성격이 다르다. 고객 자산 상태 서술은 RUN_001과 동일하게 관찰 서술 유지("운용 지시 없이 현금성 자산으로 대기").
- **의미 축 후퇴 없음**: 확인 질문 선행·3/4 시한 보존·조건부 추천·미끼 회피 등 RUN_001 PASS 축 유지 확인.
- 분류: FC-1/FC-2 재발 아님 — **금지어 어휘의 비승격적(제도 일반론) 사용**. RUN_001 GC-22에는 없던 표현이므로 어휘 수준 후퇴로 정직히 기록. F-001의 대체 어휘 규범("운용으로 연결되지 않은 상태" 등)이 제도 설명 문맥까지는 커버하지 못함을 보여주는 관찰 — 재교정·룰 추가는 하지 않음(Human 지시: Failure Evidence 기반 최소 수정, deterministic 과추가 금지). **Human 판단 대상으로 종료 기록에 명시.**

> 이 Artifact는 생성 후 수정하지 않는다.
