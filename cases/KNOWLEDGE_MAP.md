# Knowledge Map — IRP Knowledge Requirements (Failure Discovery Phase)

Case-local Knowledge가 실제 Runtime에서 어떻게 쓰였는지 축적한다. 공통 Domain Knowledge로의 의미적 승격은 Human 승인 없이 하지 않는다.

Reusable Knowledge Candidate 기준: 둘 이상의 Case에서 필요하고 의미가 안정된 것. 현재 Case가 1개이므로 모두 `candidate (pending)`.

## Knowledge Items Used

| K-ID (Case) | Knowledge (요지) | Basis | Runtime 전달 | 모델 인용 (RUN_001) | Eval 관찰 | Reusable Candidate |
|---|---|---|---|---|---|---|
| CASE_001 K-001 | 고유계정대 = 현금성자산 = 운용지시 안 된 자산; 과다 보유 시 수익률 저하 "가능성" | Source-derived (SRC-002, SRC-001) | Knowledge + Authority | 인용 | F-002: 집단 가능성 → 개인 확정 | pending — 정의 부분만 |
| CASE_001 K-002 | 현금성자산 존재 ≠ 미운용; 입금 사유(교체매매·연금지급) 확인 | Source-derived (SRC-002 L178) | 〃 | 인용 | 구조화 출력에서는 작동, Brief에서 반대 사용 (F-001) | pending — 핵심 Reasoning Cue |
| CASE_001 K-003 | 상태 인지 → 사용계획 확인 → 필요 시 운용 검토; 이해 가능한 표현 | Source-derived (SRC-002) | 〃 | 인용 | 확인 우선 구조로 작동 | pending — 확인 순서 원칙 |
| CASE_001 K-004 | 자금 성격 → 투자기간·투자성향 두 축 | Source-derived (SRC-024) | 〃 | 인용 | F-002: 연령 → "실익 큼" 확장 | pending — Limitation 없이는 확장 위험 |
| CASE_001 K-005 | 디폴트옵션 정의; 자동운용 설정 여부 Context | Source-derived (SRC-089, SRC-088) | 〃 | 인용 | 조건부 후보로만 사용 (적절) | pending |
| CASE_001 K-007 | 원리금보장형 / 실적배당형 / 자동운용 어휘 | Source-derived (SRC-088) | 〃 | 인용 | 유형 수준 표현에 사용 | pending — 범용 어휘 |
| CASE_001 K-008 | C1 투자성향 5단계, 동등/하위만 허용 | Human-approved (Source Gap) | 〃 | 인용 | 준수 | → Constraint Map C1 |
| CASE_001 K-009 | 영업·마케팅 목적 Source와 관리 판단 분리 | Case-local Interpretation | 〃 | 미인용 | 위반 없음 (효과 여부 미확인) | pending |

## Knowledge Gaps (Traceability)

| Gap | 상태 | 영향 |
|---|---|---|
| 투자성향별 허용 위험등급의 공식 적합성 기준 Source | 미확보 (Corpus에 없음) | 판단 영향 없음; C1은 Human-approved로 적용, Traceability 기록만 |

## Knowledge Issue Classification (EVAL_001 기준)

| 관찰 | 분류 |
|---|---|
| K-001 일반 가능성의 개인 확정화, K-004 연령 확장 | **Knowledge Usage Boundary** (Content·Authority 아님). Runtime이 Limitation 필드를 의도적으로 미전달한 설계와 연관 — Gate D 후보 |
| K-002 Brief에서 반대 방향 사용 | Prompt / Grounding 또는 Gemma Reasoning (Knowledge 자체는 정확) |

## Source Concerns 누적

- SRC-002 (As-of Unknown, 관련문서 2021): "1개월" 등 기준 — Threshold 미사용 유지.
- SRC-001 / SRC-037: 영업·이탈방어 목적 자료 — 판단 기준만 발췌, 목적은 배제 (K-009).
- SRC-088 / SRC-089: KB Think 정리본(원문 비복제) — 제도 사실 근거로 사용, 공식 원문 아님.
