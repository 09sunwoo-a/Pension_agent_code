# EVAL_001 — GC-13

## 1. Evaluation Metadata
- Case: GC-13 / Run: RUN_001 / Evaluated At: 2026-09-01 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-13/case.md FROZEN / Runtime: 8cf3787 (REV-001)
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PASS**

규칙이 정확하고 시한 중심 정보안내 구조다: ISA 만기자금은 1,800만 납입한도와 별개로 전액 입금 가능·전환금 10%(최대 300만) 추가 공제(K-001), 총급여 6,200만 → 13.2% 구간이라 중도해지 시 16.5% 추징으로 손해 가능 → "장기 유지 가능한 금액만"(K-002), 60일 기한·이월전환 절차(K-003), 입금 후 경로(입금예정상품 또는 2주 후 뿔려드림1)(K-004). 운용은 양호하므로 변경 권유 없음(Golden 핵심). Judgment(추가 확인 우선 / 고객 결정 지원)와 must_confirm(전환 금액·장기 유지 가능 여부)이 적절. C1/C2/C3 PASS, Critical Mistake 없음.
경미: 결정세액이 공제액보다 적으면 환급이 제한된다는 조건(K-002) 미언급; 연금저축 vs IRP 배분 선호·[06-12-151] 절세여력 확인 없음.

## 3. F-005 / F-006 (REV-001 관찰)
- F-005: 없음
- F-006: K-001~K-004 사용; 결정세액 조건(K-002 일부) 미사용(경미)

## 4. Secondary
F-001 없음. F-002 없음. F-008 없음. F-004 경미(배분 선호). F-007 경미(화면). ISA 의무기간 5년 오기 재생산 없음(C11).

## 5. Constraint Check
C1 PASS · C2 PASS · C3 PASS

## 6. Evidence
RUN_001 §3, §6, §7, §9.

> 이 Artifact는 생성 후 수정하지 않는다.
