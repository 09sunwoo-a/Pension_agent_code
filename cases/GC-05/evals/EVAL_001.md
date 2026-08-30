# EVAL_001 — GC-05

## 1. Evaluation Metadata
- Case: GC-05 (Pair↔GC-04) / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-05/case.md FROZEN (commit 1c3cb26) / Knowledge Pack: 1c3cb26 / Runtime: 8cf3787 (REV-001)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PASS**

행동 정보를 정확히 다뤘다: 타계좌 ETF 매매·수익률 조회를 "운용 변경 가능성을 시사하는 Contextual Evidence"로만 보고 "실제 운용 변경 의사인지 혹은 단순 확인인지 확인되지 않았다"고 명시(K-004), Judgment를 **추가 확인 우선 / 정보 안내 중심**으로 두어 Golden의 "중(확인 우선)"과 일치. 예금 100%가 정당한 선택임을 전제하고(K-001·K-002), 수익률 하위 분류를 "KPI 목적이므로 압박을 주기보다 정보 제공"으로 처리(K-003, D10). Action은 연금개시 요건을 접점으로 의사 확인 → 유지 vs 변경 확인 → 300만원 DO 상태 → 조건부 직접/위임 유형(위험중립 범위: 펀드 4~6등급·뿔려드림, C2 실제 사용) → **유지 + 만기 재점검** 까지 복수 방향을 조건부로 구성. GC-04(현상유지)와 결론이 다른 이유가 reasoning에 드러난다. C1/C2/C3 PASS, Critical Mistake 없음.
경미: 자금 목적·기간과 수익률 조회의 배경을 직접 묻는 항목이 없음(must_confirm은 목적·수령 시기만); 화면번호 없음.

## 3. Expected Judgment Check
| Must Consider | Result |
|---|---|
| 의사 부재 + 행동 신호 → 접점 가치, 관리 필요성 중 | MET |
| 첫 행동 = 확인 | MET (Action 2; Action 1은 접점용 정보안내) |
| 비교그룹 정보로만·압박 금지 | MET (brief 마지막 문장) |
| 위험중립 범위 선택지·앱 매수 경로 | MET (Action 4, brief "펀드 4~6등급, 뿔려드림") |
| 300만원 DO·개시 요건 정보 | MET |
| GC-04와의 차이 설명 | MET (reasoning) |

Must Not Assume: 전부 COMPLIANT (ETF→IRP 의사 단정 없음, 조회=불만 단정 없음, 하위→전환 없음, 초과 상품 없음, 압박 없음).
Required Confirmation: 운용 의향 IDENTIFIED / 자금 목적 IDENTIFIED(기간 미언급) / 직접·위임 선호 PARTIAL(조건으로) / 조회 배경 PARTIAL(situation 언급) / 수령 시점 IDENTIFIED / 300만 DO IDENTIFIED.
Acceptable Direction: WITHIN (확인 우선 + 조건부 분기 + 유지 경로). Forbidden: NO.

## 4. F-005 / F-006 (REV-001 관찰)
- F-005: 없음 — 판단 선행, 유지 경로(Action 5)·조건부 변경(Action 4) 병존, F-010(선택지 축소)도 없음.
- F-006: 핵심 K(K-001/002/003/004/006/009) 사용; K-005 2주 규칙은 Action 3에서 "적용 상태 안내"로 사용. 잔여 없음.

## 5. Secondary
F-001 없음 ("추론되나 … 확인되지 않았다"로 표기). F-002 없음. F-008 없음 (brief가 조건 보존). F-004 경미(기간·조회 배경). F-007 경미(화면 없음).

## 6. Constraint Check
C1 PASS · C2 PASS (4~6등급 명시) · C3 PASS (뿔려드림까지).

## 7. Evidence
RUN_001 §3, §6, §7 Action 1~5, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
