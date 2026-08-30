# Constraint Requirement Map (Failure Discovery Phase)

Case에서 실제 판단공간에 영향을 준 Hard Constraint와, Out of Scope로 미룬 Constraint 후보를 축적한다. 새 Hard Constraint 추가·삭제·완화는 Human Gate(`AGENTS.md` §20.3) 없이 하지 않는다.

Authority 순서(`golden/HUMAN_DECISIONS.md` HD-3): `공식 법·제도·내규·시스템 기준 > 행내 공식 업무가이드/매뉴얼 > 영업점 Hot Tip / Field Know-how`. Hot Tip 단독 근거는 Hard Constraint가 아니라 **Operational Check Needed**로 둔다.

## Applied Hard Constraints

| ID | Constraint | Authority | Source Status | Runtime 구현 | Eval 결과 | Cases |
|---|---|---|---|---|---|---|
| C1 | 투자성향 5단계(안정형 < 안정추구형 < 위험중립형 < 적극투자형 < 공격투자형); Solution은 고객 성향과 같거나 낮은 위험수준만. 성향은 **상한 제한**이지 해당 수준의 위험 부담을 요구하지 않음 — 성향-운용 불일치를 자동 관리 필요로 보지 않음 | **Human-approved Business Fact (HD-2, 2026-08-30)** | Source Traceability Gap — 공식 적합성 기준 원문 미확보 (SRC-088/024는 정의·축 수준) | Pre-Reasoning: 허용/제외 범위를 독립 Constraint Section으로 전달 · Post: `risk_level` ∈ forbidden → FAIL | CASE_001 RUN_001 PASS (라벨·내용 정합 확인) | CASE_001, P0 전 Case |
| C2 | 투자성향 ↔ **펀드 위험등급 Eligibility Mapping**: 가입 불가능 펀드는 Reasoning 전 Candidate Space에서 제거하고 Post-Reasoning에서 재검증 | **Human-approved Business Fact (HD-2)** | Source Traceability Gap — 성향↔펀드 위험등급 매핑표가 Corpus에 없음 (SRC-095 위험등급 라벨만 존재). 공식 원문 확보 시 Source-grounded로 교체 | 미구현 (Runtime Gap — 상품별 위험등급 매핑·Eligibility 검사) | — | GC-02, 05, 06, 17 (P0: GC-06) |
| C3 | 투자성향 ↔ **디폴트옵션 포트폴리오 Eligibility Mapping**: 지켜드림(전 성향) / 알파드림(안정추구형 이상) / 뿔려드림(위험중립형 이상) / 모두드림(공격투자형만) — 가입 불가능 포트폴리오는 Reasoning 전 제거, Post에서 재검증 | **Human-approved Business Fact (HD-2)** | SRC-089 (KB Think 정리본, 심의필 콘텐츠 기반) L43-54; SRC-007 시트32·33과 정합. 공식 원문(상품설명서·공시) 확보 시 교체 | 미구현 (Runtime Gap) | — | GC-03, 09, 17 (P0: GC-03) |

## Runtime Validation Limitations (관찰)

- C1 Validator는 모델이 자기 기재한 `risk_level` 라벨만 검사한다. direction 내용과 라벨의 정합성은 Evaluator가 별도 확인 (CASE_001: 정합). 상품별 위험등급 매핑(C2)·디폴트옵션 Eligibility(C3) 검사는 미구현 → P0 Batch 시작 시 최소 구현 설계 대상 (`AGENTS.md` §20.7).
- Execution Feasibility / Solution Conflict 검사 미구현 (§20.8 — Batch Evidence 후 결정).

## Constraint Candidates (Human Gate 대상 — 승격 전에는 Required Confirmation / Operational Check Needed 로 처리)

| Candidate | 출처 / Authority | 현재 처리 | 비고 |
|---|---|---|---|
| 위험자산 투자한도 70% (디폴트옵션·TDF 등 예외 100%) | SRC-087 (Public 심의필), SRC-003 (Internal 이론편) — 공식성 있음; 예외 범위·페널티는 SRC-077 (Field) | GC-07에서 제도 Fact로 사용; Hard Constraint 승격은 Human Gate | 예외 상품 범위는 Source Conflict (SRC-077 vs 003 vs 081) → 공식 원문 확인 |
| 연금개시 요건 (만 55세 + 가입 5년; 퇴직급여 포함 시 55세만) | SRC-003, SRC-049, SRC-087 | GC-10/12에서 적용요건 판단(HD-1 Scope 내); 요건 미충족 시 개시 불가 판정 | 승격 후보 (공식성 충분) |
| 연금개시 후 이전·추가입금 불가, 자동이체/상품변경 진행 중 지급거래 불가 | SRC-049, SRC-070, SRC-086, SRC-003 (추가개설 흐름) | GC-10/12에서 실행 전 확인사항 | SRC-049/070/086은 Field → **Operational Check Needed**; SRC-003 흐름도와 정합 부분만 승격 후보 |
| 연금수령 방식별 운용 제약 (자유인출만 ETF 운용 가능) | SRC-003 L286 (Internal) + SRC-084 (Field, "전량 매도") | GC-11에서 실행 불가 판정 근거는 SRC-003; 매도 절차는 Operational Check Needed | — |
| 연금저축 → IRP 이전 요건 (55세 + 5년, 퇴직소득 존재 시 제외) | SRC-043 (Field), SRC-070 (Field), SRC-026 F25 (Training), SRC-003 CASE② | GC-15 (P1) | 공식 원문 확인 후 승격 |
| 실물이전 조건 (같은 유형·같은 상품·가능 상품) / 디폴트옵션 보유 시 해지 필요 / 거절 사유 4종 | SRC-087 (Public) 3조건 → 공식성; SRC-061/065/067 (Field) | GC-16: 3조건은 제도 Fact, 해지·거절 사유는 Operational Check Needed | — |
| 중도인출 법정사유·최대 90%·신청 시한·비대면 불가 | SRC-003 (Internal, 검수필요 표시), SRC-043 (Field), SRC-087 (Public 사유) | GC-14: 사유는 제도 Fact, 90%·시한·창구 접수는 Operational Check Needed | 원문 확인 |
| 세액공제·납입한도 (1,800만 / 900만 / ISA 60일·10%·300만) | SRC-087, SRC-003 (공식성) | GC-13 (P1); HD-1 Scope 내 구조·시한 판단 | 시점 의존 |
| 채널별 거래 제약 (전화센터 정기예금·고유대 한정, 컨설팅센터 예금→예금, ETF 본인 앱, 중도인출 창구, 유선 특정펀드 언급 금소법) | SRC-002 (Internal), SRC-069/073 (Field), SRC-043 (Field) | 실행 전 Operational Check Needed | SRC-002 근거 항목은 승격 후보 |
