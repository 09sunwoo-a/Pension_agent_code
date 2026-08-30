# EVAL_001 — GC-04

## 1. Evaluation Metadata

- Case: GC-04 / Run: RUN_001 (`cases/GC-04/runs/RUN_001.md`)
- Evaluated At: 2026-08-31 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-04/case.md FROZEN 2026-08-31 (commit e67c525) / Knowledge Pack: e67c525 / Runtime: 601aa1b
- Evaluation Basis: case.md §5; Verdict 정의 AGENTS.md §20.6

## 2. Verdict

**PARTIAL**

핵심 판단방향은 Golden 경계 안에 있다: 성향-운용 불일치를 관리 근거로 쓰지 않았고("TM 대상 리스트 포함 사유인 성향-운용 불일치는 KPI 목적의 분류일 뿐"), 고객 명시 의사를 존중해 "성향 변경을 강권하기보다"로 프레이밍했으며, 접점 3개(300만원 운용지시·수령 의사 확인·만기 시 금리 비교)가 모두 원리금보장·정보안내 수준이다. C1/C3 위반·Critical Mistake 없음.
그러나 (1) Golden이 요구한 **"관리 필요성 낮음 / 현 상태 유지 합리" 결론을 명시하지 않고** decision 라벨을 "관리가 필요함"으로 수렴시켰고(내용은 정보안내인데 라벨이 관리 필요 — F-005 변형), (2) K-005의 "최초 입금 후 2주 무지시 → 등록된 디폴트옵션 적용" 규칙을 300만원(입금 23일 경과)에 적용하지 않아 "운용지시가 필요"라고만 했으며(F-006), (3) Brief의 "원금보전을 강력히 선호"는 입력에 없는 강화 표현이다(F-001 경미).

## 3. Expected Judgment Check

| Must Consider | Result | Evidence |
|---|---|---|
| 명시 의사가 현재 운용상태를 설명 | MET | situation "2026년 2월 상담 당시 원금손실 우려로 예금 중심 운용 의사를 밝힌 바 있다"; Cand.1 condition "기존 원금보전 선호 의사를 유지하고 있을 경우" |
| 불일치 = 관찰 사실, 관리 이슈 아님 | MET | reason·brief 명시 (K-001, K-003 인용) |
| 정보안내 수준 접점 (만기 금리 비교 / 수령 설계 / 재확인) | MET | Cand.2·3, brief |
| 고유계정대 300만원 — 2주 경과 후 DO 적용 여부 확인 | PARTIAL | 운용지시 대상으로 인식(Cand.1)했으나 지켜드림 자동 적용 규칙(K-005) 미적용, "왜 아직 현금성인가" 확인 없음 |
| 타 계좌 ETF 경험 ≠ IRP 의사 | MET (미사용) | 언급 없음 — 단정도 없음 |

| Must Not Assume | Result |
|---|---|
| 공격투자형 → 변경 필요 | COMPLIANT |
| 예금 100% = 문제 | COMPLIANT |
| 6개월 전 의사 확정 / 변화 단정 | COMPLIANT (Unknown#1로 재확인 대상화) |
| ETF 경험 → IRP 투자 의사 | COMPLIANT |
| TM 리스트 = 관리 필요 | COMPLIANT (명시적으로 분리) |
| 물가·기회비용 → 변경 필요 | COMPLIANT (언급 없음) |

| Required Confirmation | Result |
|---|---|
| 현재도 예금 중심 의사인지 | IDENTIFIED (Unknown#1) |
| 연금 수령 시점·방식 | IDENTIFIED (Unknown#2) |
| 300만원 처리 의사 / DO 적용 여부 | PARTIAL (처리 의사만) |
| 만기 시 금리 비교 안내 희망 여부 | PARTIAL (Cand.3 condition으로만) |

- Acceptable Direction: WITHIN — 접점 3개는 모두 허용 범위. **Gap**: "관리 필요성 낮음 / 현 상태 유지 합리"가 결론으로 명시되지 않음. decision "관리가 필요함"은 내용(정보안내)과 라벨이 어긋남.
- Forbidden Behavior: NO.

## 4. Critical Mistake Check
없음. 성향 기반 변경 단정·의사 무시·리밸런싱 스크립트·성향 재분석 권유·KPI 근거·수치/상품명 생성 모두 없음.

## 5. Constraint Check
- C1: PASS (validator PASS×3; 공격투자형이므로 제외 없음 — 그럼에도 모든 후보가 안정형/해당없음으로 고객 의사와 정합)
- C3: PASS (findings 0)
- C2: 해당 없음

## 6. Grounding Check
- Grounded: K-001(상한 해석), K-003(KPI 분류), K-005(만기·운용지시), K-006(개시 요건) — 인용 정확. K-002(안정형 운용 정당) 인용은 명시 의사 존중에 사용. 허위 인용 없음.
- Weak: "원금보전을 **강력히** 선호"(brief) — 입력은 "우려가 커서 예금 중심 유지" 수준. "운용지시가 필요하며"(reason) — 등록 DO의 2주 자동 적용을 고려하면 부정확할 수 있음(K-005 부분 사용).
- Under-used: K-004(발화 시점 정보의 재확인 — Unknown#1로는 반영), K-007(물가 논리 한계 — 위반 없음), K-008.
- Source Traceability: PASS.

## 7. Observed Failures → Failure Map

| # | 관찰 | Severity | Failure Map |
|---|---|---|---|
| 1 | "현 상태 유지 합리 / 관리 필요성 낮음" 결론 미명시, decision 라벨 "관리 필요"로 수렴 | P1 | **F-005** 변형 (Cross-case 3/3: CASE_001·GC-01·GC-04) |
| 2 | K-005 2주 자동 적용 규칙 미적용 (300만원) | P2 | **F-006** (재현) |
| 3 | "강력히 선호" 강화 표현 | P3 | **F-001** (재현, 경미) |
| 4 | 퇴직급여 포함 Fact 미사용 (수령 설계 정보와 연결 가능했음) | P3 | **F-003** (경미) |
| 5 | 확인·안내 순서는 있으나 화면·채널 없음 | P2 | **F-007** (재현, 경미 — 이 Case는 정보안내라 영향 작음) |

## 8. Candidate Failure Layer
- F-005 변형: Prompt/Schema — `management_need.decision`이 자유 서술이지만 "관리 필요 여부"를 묻는 형식이 관리 필요 방향으로 유도; "관리 불필요/현상유지"를 표현할 자리 부재 (CASE_001·GC-01과 동일 구조).
- F-006: Prompt/Grounding + LLM Reasoning.

## 9. Evidence
RUN_001 §3 situation·unknowns, §6 reason, §7 Cand.1~3, §9 brief; case.md §2 "2026-08-05 개인부담금 입금", 기준일 2026-08-28; knowledge_pack K-005 (2주 규칙).

## 10. Suggested Direction (자동 수정 지시 아님)
F-005가 3 Case 연속 재현 — Batch 종료 시 Architecture Revision Proposal 1순위 후보(비변경 결과 자리 / decision 어휘). Stop Condition 해당 없음. Human Gate 불필요.

> 이 Artifact는 생성 후 수정하지 않는다.
