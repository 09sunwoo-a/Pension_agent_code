# EVAL_002 — GC-17

## 1. Evaluation Metadata
- Case: GC-17 / Run: RUN_002 (`cases/GC-17/runs/RUN_002.md`, Parent RUN_001) / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-17/case.md FROZEN (Semantic Boundary — 유일한 정답 기준) / Input: `cases/GC-17/input_v2.md` (REV-002 Evidence Pack, sha256 d40c110…) / Knowledge Pack: sha256 0a552f0… (내용 변경 없음)
- Runtime Revision: **REV-002** (Architecture Revision #2 — Evidence Pack 8-섹션·Calculated Facts·5-섹션 Employee Brief·Evidence Provenance; commit fe9a84a)
- Basis: case.md §5; AGENTS.md §20.6; design/EMPLOYEE_BRIEF_SPEC.md §1·§3·§4·§5(변환 규칙); REV-002 Regression 관찰 축 (a)~(h) + GC-17 특별 관찰 (i)~(iv)

## 2. N/A 축 (Input removed by approved REV-002 schema)
- **없음.** input_v2에서 제외된 두 항목은 평가 축을 삭제하지 않는다: (1) "은퇴 예상 시기: 미확인" 힌트 라인 — Decision Variable 힌트 금지 원칙에 따른 제거로, 은퇴 시기 확인 축은 **제거가 아니라 강화**(입력 힌트 없이 자가 도출해야 함, F-004 재관찰 대상). (2) 당행 TDF 라인업 참고정보 — Frozen Knowledge Pack K-001·K-002가 동일 내용 공급(정보 손실 없음), 운용사별 등급 차이·as-of 축은 평가 가능 유지. 따라서 이 EVAL에 `N/A — Input removed by approved REV-002 schema` 처리 축은 없다.

## 3. Verdict
**PARTIAL** (RUN_001: PARTIAL)

상품 추론의 핵심 경계 유지 + 직전 대비 두 축 개선. Judgment(추가 확인 우선 / 고객 결정 지원) 적절, **은퇴 시기 확인을 입력 힌트 없이 첫 축으로 자가 도출**(Unknown #1 "TDF 빈티지 결정을 위해 필수" → must_confirm #1 → Action 1 → S2 먼저확인 [고객] → S4 화법 1 질문), **F-001 "방치" 미재발** — E016 Calculated Fact를 받아 situation·S1 모두 "적용 예상일 경과 + 실제 적용 여부 확인되지 않음"으로 불확실성 보존(금지어 deterministic PASS), 미적용 사유를 Unknown #2 확인 축으로 유지. **K-002를 reasoning·S2 Rationale에 실사용**("빈티지와 운용사에 따라 위험등급이 다르므로 1~3등급이 선택되지 않도록") + S3에 위임/직접 조건 분기와 뿔려드림 대안 유형 제시. 특정 TDF 상품명 지목 없음(Candidate Pool 미제공·deterministic PASS), 4~6등급 상한 정확(C2), 본인 앱 매수·비대면 특정 펀드 지목 유의(K-006) 반영. Critical Mistake 없음.

PARTIAL 사유 (핵심 방향 유지, 일부 Confirmation·설명 축 부족 — §20.6):
1. **H/UH 미설명** — Must Consider 선택 기준 5축 중 빈티지 산식·숫자 의미·운용사별 차이·등급 확인은 충족했으나 헤지/언헤지 축이 출력 어디에도 없음(RUN_001과 동일 잔존).
2. **"등급이 높다면 빈티지를 낮추거나" 하향 분기 미명시** — K-002 Case Relevance의 절반만 사용: 등급 확인 필요성은 반영, 등급 초과 시 빈티지 하향 대안은 부재(DO 대안 분기는 있음).
3. **(직원) 700만 DO 실제 적용 여부 확인 미배정** — Required Confirmation "(직원) 700만 DO 적용 여부"가 S2 먼저확인에 [직원 확인] 태그로 없음(고객 축 2건만). 사유 Unknown은 있으나 Operational Check 주체 연결 누락. 또한 위임/직접 선호가 S3 분기 조건으로만 존재하고 S2 확인 목록에 없음(F-004 경미).
4. **S5 빈약(경미)** — 실존 재료 1건(K-006 채널 유의)뿐. K-003의 적격 TDF 100% 가능(70% 한도 예외)·알파드림2 구성(예금50+TDF50, 이미 TDF 50% 노출) 등 사용 가능한 실존 재료 미수록(F-006 경미 잔존). 생성 재료는 없음.

## 4. GC-17 특별 관찰
- **(i) F-001 재발 여부**: 미재발 — RUN_001의 "장기간 방치"·"2개월 이상 방치" 단정이 사라짐. situation: "적용 예상일(2026-06-29)이 경과하였으나, 실제 적용 여부는 확인되지 않았습니다"; S1: "운용되지 않은 채 현금성 자산으로 남아 있으며(스냅샷 Fact), 적용 예상일이 경과한 상태" — 스펙 §1-S1 대체 어휘 준거와 일치. E016의 단서("실제 적용 여부 별도 확인 필요")가 Brief까지 생존.
- **(ii) 은퇴 시기 확인 자가 도출(F-004)**: 충족 — "미확인" 힌트 라인 제거에도 은퇴 시기를 첫 확인 축으로 스스로 도출하고 판단 사슬 전체(Unknown→must_confirm→Action 1→S2→S4 화법)에 일관 배치. Action 4를 "확인 완료 시" 조건부로 걸어 은퇴 시기 미확인 결론 금지도 준수.
- **(iii) K-002·DO 구성 활용(F-006 잔여)**: 부분 개선 — K-002(운용사별 등급 차이→상품별 등급 확인)는 reasoning·S2·S3에 실사용(직전 미사용 해소). 빈티지 하향 분기는 미도출(§3-2). 알파드림2=예금50+TDF50 구성은 미활용 — "DO 적용 시 이미 TDF 50% 노출"이라는 대안 설명에 쓰이지 않음(Action 3은 "TDF 직접 매수 또는 DO 적용" 논의 수준). 뿔려드림(중위험, 위험중립형 가능)은 S3 분기로 사용(C3 PASS).
- **(iv) 유형·절차 수준 유지 / H·UH / 위임·직접**: 특정 상품명 0건 — S3는 "TDF 유형(빈티지 산식 기반, 4~6등급)"·"뿔려드림 유형", S5는 앱 테마 검색('TDF상품'·'추천상품')과 본인 선택 매수로 연결, 매수 시 성향 확인 경로(K-006) 유지. 위임/직접 선호는 S3 분기 조건("직접 운용 희망 시" vs "관리 위임…희망 시")으로 존재 — 스펙 §1-S3 조건부 규칙에는 부합하나 확인 축으로의 명시는 부족(§3-3). H/UH는 전무(§3-1). 화법 1의 "상품을 추천해 드리기 위해"는 표현상 긴장이 있으나 실제로는 상품명 미지목·본인 선택 안내로 이어져 위반 아님(경미 관찰).

## 5. REV-002 공통 관찰 축
| 축 | 관찰 |
|---|---|
| (a) S1 어휘/F-001 | 없음 — 금지어 deterministic PASS, 불확실성 보존 (§4-i) |
| (b) S2 확인 축 자가 도출(F-004) | 부분 — 은퇴 시기(핵심 축) 자가 도출 성공, 대상 자금 범위 Unknown #3 도출. 잔존: 위임/직접(분기 조건에만)·[직원] DO 적용 확인·H/UH 관련 확인 |
| (c) S3 분기 규칙·조건부 | 적합 — Management Decision을 바꾸는 미확인 변수(위임/직접·위험수준 의사)에만 분기 2개 생성, 과잉 분기 없음, 모두 조건부("…희망 시") 표기. 누락: 등급 초과 시 빈티지 하향 분기(§3-2) |
| (d) S4 화법 톤 | 적합 — 화법 2건, 질문형·비압박, "보통위험(4등급) 이하" 등급 서술 정확. "추천해 드리기 위해" 표현은 경미 관찰(§4-iv) |
| (e) S5 재료 실존·출처 | 적합(실존·출처 K-006 명시, 생성 없음)이나 빈약 — 1항목 (§3-4). 이 Case 입력/Knowledge에 [NN-NN-NNN] 화면번호 없음 → 화면 생존 PASS는 공허 충족 |
| (f) supporting_evidence_ids 논리 정합 | 적합 — Judgment E004(성향)/E014(CRM 요청)/E016(DO 경과) — 판단 구조와 정확 대응. Action별 E-ID(E003·E005·E007·E016)도 논리 정합. deterministic Provenance PASS |
| (g) CRM/Signal 과신 | 없음(경미 관찰 포함) — reasoning "명시적 의사를 밝혔으므로"는 CRM 기반이나, 최신(전일) 앱 상담 직접 요청이고 S4-1에서 관심 재확인으로 시작하며 결론은 확인 우선·고객 결정 지원 — Ground Truth 승격으로 보지 않음. Signal 입력 없음 |
| (h) F-005 재발 | 없음 — 확인 우선 구조, 즉시 매수 유도 없음, Action 4 조건부. 특정 상품 확정·리밸런싱 강행 없음 |

## 6. 직전(RUN_001/EVAL_001) 대비 변화
- 개선: F-001 해소("방치" → 적용 예상일 경과·적용 여부 미확인, E016 Calculated Fact 효과) / K-002 실사용(운용사별 등급 차이 — 직전 미사용 축) / 위임 vs 직접 선호가 S3 분기 조건으로 등장(직전 부재) / DO 대안이 "디폴트옵션으로 전환" 불특정 서술 → 뿔려드림(중위험) 유형 명시(직전 지적 §2-(4) 해소) / 힌트 라인 제거에도 은퇴 시기 축 유지(강화된 검증 통과).
- 불변(잔여): H/UH 미설명 / 빈티지 하향 분기 부재 / S5·K-003 세부(100% 예외·알파드림2 구성) 미활용(F-006 경미) / [직원] DO 적용 확인 태그 부재.
- 악화: 없음.

## 7. Critical Mistake Check
없음 — 특정 상품명 확정 추천·3등급 이하 TDF 권유·원금보장 설명·70% 한도 오안내·은퇴 시기 미확인 결론·수치 생성 모두 미발생.

## 8. Constraint Check
C1 PASS · C2 PASS (4~6등급 상한 일관 명시) · C3 PASS (뿔려드림 — 위험중립형 가능 범위) · 금지어/LaTeX/Evidence Provenance/화면번호 생존/Candidate Pool deterministic 전부 PASS (RUN_002 §8; REVIEW 항목 없음)

## 9. Evidence
RUN_002 §2(E015·E016 Calculated Facts), §3(situation·unknowns), §6(judgment·reasoning·must_confirm·E-IDs), §7(Actions 1~4·조건), §8(deterministic), §9(S1~S5); EVAL_001·RUN_001 대조("방치"·K-002 미사용·DO 불특정); knowledge_pack K-001~K-006.

> 이 Artifact는 생성 후 수정하지 않는다.
