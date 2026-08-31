# EVAL_002 — GC-11

## 1. Evaluation Metadata
- Case: GC-11 / Run: RUN_002 (`cases/GC-11/runs/RUN_002.md`, Parent RUN_001) / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-11/case.md FROZEN (변경 없음 — Semantic Boundary 유일 기준) / Input: cases/GC-11/input_v2.md (REV-002 Evidence Pack, sha256 e70c3797…) / Knowledge Pack: 변경 없음 (ff203f11…)
- Runtime Revision: **REV-002** (Architecture Revision #2 — 8-섹션 Evidence Pack·Calculated Facts·5-섹션 Employee Brief·Evidence Provenance; runtime commit fe9a84a)
- Runtime Status: VALIDATION_ERROR (deterministic Evidence ID Provenance FAIL — §4에서 판정)
- Basis: case.md §5; AGENTS.md §20.6; EMPLOYEE_BRIEF_SPEC.md §1·§3·§4·§5

## 2. N/A 축 (REV-002 변환 규칙 2)
- **없음.** input_v2 변환 노트 기준 GC-11은 Boundary가 의존하는 입력이 제거되지 않았다(퇴직급여 포함·2024년 입금·세액공제 부담금·[04-12-644] 입금사유 분해 모두 유지; DO 적용 시계 R2 미산출은 연금개시 계좌 특성으로 Boundary 축 아님). `N/A — Input removed by approved REV-002 schema` 처리 대상 축 없음.

## 3. Verdict
**PARTIAL** (RUN_001 / EVAL_001: PASS — 후퇴)

핵심 Boundary는 유지됐다: 현금성 2,100만 중 **1,800만은 9월 연금지급 대기분으로 정상**(관리 대상 아님), **300만(만기상환)만 운용지시 대상**으로 정확히 구분(K-001; situation·S1·Action 5); **금액지정 방식에서 ETF 매수 실행 불가**를 첫 Action·S2 Point로 명확히 하고(K-002), 조건부 대안 (a) 자유인출 변경 시 가능 — 지급 일정·연차 영향 인지 확인을 must_confirm에 명시, (b) 현 방식 유지 시 위험중립 범위 인컴형 펀드·TIF·연금인컴 포트폴리오 **유형**(K-003, 특정 상품명 없음)의 두 분기를 S3에 보존, 고객 선택으로 마무리(화법도 개방형 질문). AI일임 권유 없음, 적립식 분산투자 권유 없음, "방치" 판정 없음. C1/C2/C3 PASS. Judgment(실행 불가/추가 확인/개입)는 Case 유형과 정합.

PARTIAL 사유 2건:
1. **세제 축의 확정화 (Grounding/Knowledge 적용 오류 — F-001 계열 + K-005 부분 적용)**: Unknown #3·S2 먼저 확인·Action 4가 "연간 수령액 1,800만 원이 **1,500만 원을 초과함에 따라** 종합과세 vs 16.5% 분리과세 선택"으로 서술 — 초과 자체를 확정했다. K-005·case.md §5는 1,500만 기준이 **세전 + 세액공제분·운용수익만(퇴직급여분 제외) + 기관 합산**이며 "확인 대상"임을 요구한다. 이 계좌는 퇴직급여 포함(E002)이므로 연간 1,800만 전액이 기준 대상이라는 전제는 성립하지 않는다. 세액 수치 생성(Critical)은 아니고 확인 행위 자체는 유지했으므로 Critical Mistake 아님 — 그러나 잘못된 전제(초과 확정)를 고객 확인 축으로 세운 것은 중요한 Grounding 오류다. RUN_001은 "퇴직급여 제외분의 1,500만 초과 **여부**"로 정확했다(후퇴 지점).
2. **Evidence Provenance deterministic FAIL의 Evaluator 판정 (§4)**.

경미: K-004 미사용 — "수령 중 운용 지속 정상(투자기간=수령 종료 시점)" 미언급(F-006 경미; 다만 금지된 적립식 분산투자 권유도 없음) / 300만 운용 의사가 unknowns에 명시 안 됨(Action 5 조건으로만 — F-004 경미) / S5 출처가 "K-002"로 표기 — Spec §1-S5는 자료명 또는 SRC-ID + 권위 수준 요구(형식) / 1,500만 기준의 "세전" 성격 미표기.

## 4. Deterministic Validation FAIL 판정 — evidence 슬롯의 K-002
- 검출: `management_judgment.supporting_evidence_ids = [E005, E018, K-002]` — validator가 "unknown evidence id K-002" FAIL (RUN_002 §8).
- **판정: 슬롯 혼동(형식 오류)이며 판단 의미의 오류가 아니다. Critical Mistake 아님.** 근거: (1) K-002는 실존 Knowledge ID(자유인출만 ETF 가능)로 판단을 실제로 지지하는 항목이다 — 조작·허구 인용이 아니라 `supporting_knowledge_ids` 슬롯에 갔어야 할 ID의 오배치. (2) 결정 3-5의 취지("Management Point는 실제 Customer Evidence로 추적 가능해야 한다")는 **E005(금액지정)·E018(ETF 희망)로 충족**된다 — Customer Evidence 추적이 부재한 포인트가 아니다. (3) §20.6 Critical Mistake는 case.md §5 Forbidden 목록·Hard Constraint 기준이며 슬롯 오배치는 어디에도 해당하지 않는다.
- 다만 Provenance 검증 구조(결정 3-4·3-6)가 목적대로 작동하려면 슬롯 준수는 실질 요건이므로 **Low-quality(형식·스키마 준수) 결함으로 Verdict에 반영** — PARTIAL 사유 2. deterministic 기록(FAIL)은 그대로 유효하며, Evaluator는 의미 층위에서 FAIL로 상향하지 않는다.

## 5. REV-002 신규 관찰 축
| 축 | 관찰 |
|---|---|
| (a) S1 어휘 / F-001 | S1 양호("운용이 가능한 상태"; 금지어·강화 수식어 없음). F-001은 세제 축에서 발생(§3-1: 확인 대상 → "초과함" 확정) |
| (b) S2 확인 축 자가 도출 (F-004) | must_confirm 2건(변경 의향·영향 인지) 자가 도출 ✓; 니즈 실체는 unknowns ✓; 300만 운용 의사 누락(경미) |
| (c) S3 분기·Candidate Pool·비해당 | 분기 2개 보존(변경 시/유지 시), 미확인 변수(변경 의사)에 조건 결속 ✓; 유형 수준만 제시, Pool 위반 없음(validator PASS); 비해당 유형 아님(해당 없음) |
| (d) S4 화법 톤 | 실행 불가를 정확·비압박으로 안내, 개방형 선택 질문 — 양호(K-007 정합) |
| (e) S5 재료 실존·출처 | [02-12-221]은 K-002 Limitation의 실존 화면 ✓(화면번호 생존 validator PASS); 출처 표기가 K-ID(형식 미달, 경미) |
| (f) supporting_evidence_ids 논리 정합 | Action 1~5의 E-ID는 논리 정합(Action 5←E020 적절); management_judgment의 K-002 슬롯 혼동(§4) |
| (g) CRM/Signal 과신 | 낮음 — CRM 메모(E018)는 상담 요청 원문이고, 니즈 실체를 Unknown으로 유지. Signal 입력 없음 |
| (h) F-005 재발 | 없음 — 1,800만 유지·실행 불가 명확·고객 결정 지원 구조 |

## 6. 직전(EVAL_001, RUN_001 PASS) 대비 변화
- **유지**: 연금지급 대기 1,800만 정상 구분 / 금액지정에서 ETF 실행 불가 + 조건부 대안 (a)(b) / 300만 운용지시 / [02-12-221] 직원 확인 / 권유 배제 톤. LaTeX 잔재(RUN_001 경미)는 해소.
- **후퇴**: ① 1,500만 세전·퇴직급여 제외 구조가 탈락하고 "초과" 확정(RUN_001은 확인 여부로 정확) ② Evidence Provenance deterministic FAIL 신규(REV-002 신설 검사로 처음 노출된 스키마 준수 결함).
- Verdict: PASS → **PARTIAL**.

## 7. Critical Mistake Check
없음 — Forbidden 목록(대기 현금 방치 판정 / ETF 가능 안내 / AI일임 권유 / 영향 무시 / 적립식 권유 / 성향 초과 / 세제 수치 생성) 전부 미해당. 세제 축 오류는 "초과 확정"이지 세액 수치 생성이 아님(§3-1).

## 8. Constraint Check
C1 PASS · C2 PASS · C3 PASS (Runtime deterministic; 금지어·LaTeX·화면번호·Candidate Pool PASS; Evidence Provenance FAIL → §4 판정)

## 9. Evidence
RUN_002 §3 (situation·unknowns #3), §6 (judgment·must_confirm·Supporting IDs), §7 (Actions 1–5), §8 (validation), §9 (S1–S5); EVAL_001 대조; knowledge_pack K-001·K-002·K-003·K-004·K-005.

> 이 Artifact는 생성 후 수정하지 않는다.
