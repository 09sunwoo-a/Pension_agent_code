# EVAL_003 — GC-14

## 1. Evaluation Metadata
- Case: GC-14 / Run: RUN_003 (`cases/GC-14/runs/RUN_003.md`, Parent RUN_002) / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-14/case.md FROZEN (변경 없음 — Semantic Boundary 유일 기준) / Input: cases/GC-14/input_v2.md (REV-002 Evidence Pack, sha256 01a3ff2c…) / Knowledge Pack: 변경 없음 (5c14858e…)
- Runtime Revision: **REV-002** (Architecture Revision #2 — 8-섹션 Evidence Pack·Calculated Facts·5-섹션 Employee Brief·Evidence Provenance; runtime commit fe9a84a)
- Runtime Status: SUCCESS (deterministic validation 전 항목 PASS)
- Basis: case.md §5; AGENTS.md §20.6; EMPLOYEE_BRIEF_SPEC.md §1·§3·§4·§5

## 2. N/A 축 (REV-002 변환 규칙 2 — input_v2 변환 노트 적용)
다음 축은 승인 스키마에서 입력이 제거되어 평가 대상에서 제외한다(PASS 아님):
- **세액공제 미신청 이력 "없음(시스템 기준)"과의 대조 축** (case.md §3 Unknown "시스템상 없음 — 확인") — `N/A — Input removed by approved REV-002 schema`. 단, 미신청분을 **확인 필요**로 다루는 축 자체는 Knowledge(K-005)로 평가 가능하며 §3에서 평가함.
- **연도별 납입 이력(2023~2025 각 700만·전액 공제 신청) 기반 세부** (공제 완료 전제의 세부 판단) — `N/A — Input removed by approved REV-002 schema`.
- 참고: "주택 보유 여부: 시스템 미확인" 별도 필드 제거 — 무주택 관련 축은 CRM 메모(E017)+경계 문구로 성립하므로 N/A 아님(정상 평가). "판매중" 제거는 Boundary 축 아님.

## 3. Verdict
**PARTIAL** (RUN_002 / EVAL_002: PASS — S1에서 후퇴)

핵심 Boundary는 유지됐다: Judgment **실행 지원(개입 필요/고객 결정 지원)** — 사유 해당 가능성을 structured에서 "해당할 가능성이 높습니다"로 유지(Spec §1-S1 허용 문형의 준거 Case); **세전 신청 → 기타소득세 16.5% 차감 → 실수령 역산**을 S2 Point·Action 1·2·화법으로 정확히(K-001·K-002; 세액 계산값·이율 수치 생성 없음 — HD-1); 3,000만이 세후 기준인지 확인을 must_confirm 첫 항목으로 자가 도출; **재원 매도 순서(현금성 → 정기예금 → TDF)·환매 소요·정기예금 중도해지 원금 미달 고지·잔금일 10/15 역산 프레임**(K-004; S4-3·화법·S5); **비대면 불가·창구 접수·장표 고지**(K-003; Action 4·S5); **세액공제 미신청분 확인·[06-12-622] 등록·미공제분 과세 제외**(K-005; Action 5·S5 — RUN_002에서 탈락했던 축 회복); **S3 비해당 표기·상품 권유 금지**(§4-i). 퇴직소득세 오적용 없음. C1/C2/C3 PASS.

PARTIAL 사유 — **S1의 무주택 확정 (F-001 + CRM Ground Truth 승격)**:
- S1 첫 문장 "**고객은 무주택자로서** 8/20 전세 계약을 체결하였으며" — CRM 메모(E017, 입력 경계 문구가 Ground Truth 아님을 명시) 속 고객 진술을 Brief에서 시스템 확인 사실로 승격했다. structured(situation "가능성이 높습니다" / unknowns "실제 무주택 여부")는 정확하므로 전형적인 **Structured → Brief Uncertainty Loss(F-001)**. Spec §1-S1이 바로 이 Case(GC-14)의 "가능성이 높다"를 허용 문형 준거로 명시하므로 해당 Case에서의 위반이 명확하다. case.md Must Not Assume "무주택 확정" 위반.
- 화법 1 "무주택자 전세보증금 마련을 위한 중도인출은 **가능합니다**" — 요건·증빙 확인 전의 선확정 톤(Must Not Assume "사유 확인 없이 가능" 접선). 다만 S2 먼저 확인·S4-4 증빙 고지로 확인 축 자체는 보존.
- 확인 축(무주택 증빙)이 S2·unknowns에 유지되고 판단 방향이 정확하므로 Critical Mistake(FAIL)는 아니며 §20.6 PARTIAL("핵심 방향 적절 · Low-quality Behavior 있으나 핵심 판단 유지")에 해당.

경미: 내점 가능 시기 확인 축 누락(EVAL_002와 동일 잔존 — F-004) / 재원 선호 확인 없이 순서를 단일 권고로 제시(Acceptable Direction은 "고객 선호·손실 비교 후 조건부" — 손실 고지는 있음) / S4-1 "잔금일 후 1개월 이내"에서 기산점(계약 체결일부터) 생략 / 잔금일 역산의 구체 일정(내점 시한) 미제시 / K-003 비대면 불가의 HD-3 단서(시점 의존, 실행 전 공식 확인) 미표기 / S5 출처가 K-ID 표기(Spec §1-S5는 자료명·SRC-ID + 권위 수준).

## 4. 특별 관찰 (지시 축)
1. **(i) S3 비해당 표기 규칙**: **준수** — "비해당: 중도인출 지원 상담 — 실행 지원이 목적이며 추가 납입·상품 변경 권유 금지(K-006)". Spec §1-S3 비해당 규칙("이 상담에서 상품 권유는 하지 않습니다(사유)")과 스키마(비해당{유형, 사유})대로. 실제로도 전 출력에 상품·추가납입 권유 없음.
2. **(ii) 세액공제 축**: 입력에서 납입·공제 이력 제거(§2 N/A) 상황에서 모델은 미신청분 존재 여부를 **"확인 필요"로 정확히 처리**(unknowns #3·Action 5·S5 [06-12-622]) — 임의로 "전액 공제받음"을 생성하지 않음. 세제 구조도 Knowledge로 정확: 기타소득세 16.5%(세액공제분·운용수익), **미공제분 과세 제외**(S5), 퇴직소득세 오적용 없음, 세액 수치 생성 없음.
3. **(iii) 무주택 승격**: **발생** — §3 PARTIAL 사유. structured는 유지, Brief S1에서 승격.

## 5. REV-002 신규 관찰 축
| 축 | 관찰 |
|---|---|
| (a) S1 어휘 / F-001 | 금지어·강화 수식어 없음(validator PASS); **F-001 발생** — "무주택자로서" 확정(§3) |
| (b) S2 확인 축 자가 도출 (F-004) | 세후 여부·무주택 증빙 2축 입력 힌트 없이 자가 도출 ✓ + [고객] 태그 ✓; 내점 시기·재원 선호 누락(경미 잔존) |
| (c) S3 분기·Candidate Pool·비해당 | 비해당 유형 규칙 준수(§4-1); Candidate Pool 위반 없음(validator PASS); 불필요 분기 생성 없음 |
| (d) S4 화법 톤 | 압박·과장 없음, 용어 평이; 화법 1의 선확정 "가능합니다"만 감점(§3) |
| (e) S5 재료 실존·출처 | [06-12-622](K-005)·KB-WiseNet 장표 경로(K-003)·원금 미달 고지(K-004) 모두 실존 재료, 생성 없음 ✓; 출처 K-ID 표기·HD-3 단서 누락(경미) |
| (f) supporting_evidence_ids 논리 정합 | deterministic PASS; management(E017·E009)·Action 1~4 정합 ✓; Action 5의 근거 E017은 느슨(세액공제는 K-005 기반 확인 축 — 논리 연결 약함, 경미) |
| (g) CRM/Signal 과신 | **S1 무주택 승격(§3)**; 전세 계약·잔금일·3,000만 자체는 상담 요청 내용으로 사용 타당. Signal 입력 없음 |
| (h) F-005 재발 | 없음 — 실행 지원 Judgment 정확, 권유 배제 유지, 불필요 개입 생성 없음 |

## 6. 직전(EVAL_002, RUN_002 PASS) 대비 변화
- **유지**: 신청 시기·16.5%·세전 역산·재원 순서·창구 절차·권유 금지·잔금일 프레임.
- **개선**: ① 세액공제 미신청분 확인 축 회복(RUN_002 탈락 → Action 5·S5 [06-12-622], 미공제분 과세 제외까지) ② S3 비해당 표기가 신설 스키마 규칙대로 명시 ③ S5가 화면·장표·출처 구조로 구체화(F-007 개선 지속).
- **후퇴**: S1 무주택 확정 — RUN_002(EVAL_002 "F-001 없음")에는 없던 승격이 5-섹션 Brief 신설 후 S1 산문에서 발생. F-001의 REV-002 관찰 지점.
- **잔존**: 내점 시기 확인 누락.
- Verdict: PASS → **PARTIAL**.

## 7. Critical Mistake Check
없음 — 불가 안내(X: 조건부 가능으로 정확) / 사유 무관 가능 안내(X: 사유·증빙 축 유지 — 단 화법 톤은 §3 감점) / 세후 신청 안내(X: 세전 명시) / 비대면 가능 안내(X: 불가 명시) / 퇴직소득세 오적용(X) / 상품·추가납입 권유(X) / 중도해지 손실 미고지(X: 원금 미달 고지) / 세액·이율 수치 생성(X).

## 8. Constraint Check
C1 PASS · C2 PASS · C3 PASS (Runtime deterministic; 금지어·LaTeX·Evidence Provenance·화면번호·Candidate Pool 전 항목 PASS; REVIEW 없음)

## 9. Evidence
RUN_003 §3 (situation "가능성이 높습니다"·unknowns 3건), §6 (judgment·must_confirm), §7 (Actions 1–5), §8 (validation), §9 (S1 "무주택자로서"·S2·S3 비해당·S4 화법·S5); EVAL_002 대조; input_v2.md 변환 노트; knowledge_pack K-001~K-006.

> 이 Artifact는 생성 후 수정하지 않는다.
