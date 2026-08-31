# EVAL_003 — GC-16

## 1. Evaluation Metadata
- Case: GC-16 / Run: RUN_003 (`cases/GC-16/runs/RUN_003.md`, Parent RUN_002) / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context from Builder Gemma 4)
- Case Baseline: cases/GC-16/case.md FROZEN (Semantic Boundary — 유일한 정답 기준) / Input: `cases/GC-16/input_v2.md` (REV-002 Evidence Pack, sha256 46e0eba…) / Knowledge Pack: sha256 55322a4… (내용 변경 없음)
- Runtime Revision: **REV-002** (Architecture Revision #2 — Evidence Pack 8-섹션·Calculated Facts·5-섹션 Employee Brief·Evidence Provenance; commit fe9a84a)
- Basis: case.md §5; AGENTS.md §20.6; design/EMPLOYEE_BRIEF_SPEC.md §1·§3·§4·§5(변환 규칙); REV-002 Regression 관찰 축 (a)~(h) + GC-16 특별 관찰 (i)~(iv)

## 2. N/A 축 (Input removed by approved REV-002 schema)
- **없음.** input_v2 변환에서 제외된 것은 DO "2025-03 자동적용" 이력 문구(→ "약정 2025-03" Fact로 보존)뿐이며, 이에 직접 의존하는 Golden Boundary/평가 축이 없다. 고객 발화는 [CRM] 직원 작성 상담메모로 재분류(제거 아님) — 관련 축은 "CRM 과신 여부"로 평가 대상 유지. [06-AD-020] 조회값·개설 채널은 보존. 따라서 이 EVAL에 `N/A — Input removed by approved REV-002 schema` 처리 축은 없다.

## 3. Verdict
**PARTIAL** (RUN_002: PARTIAL, RUN_001: PARTIAL)

Judgment(고객 결정 지원 / 정보 안내 중심)가 Golden Acceptable Direction과 일치하고, 사전체크(불가 상품 손실액·SBI 재확인) → 경청(Action 1) → 팩트 안내(실시간 불가 정직 인정, Action 2) → 손실 고지(Action 4) → 고객 결정 존중·절차 지원(Action 5) 순서가 완성됐다. **[04-12-613] 수수료 화면이 S5에 [번호]+화면명+용도로 생존**(직전 RUN_002 미반영 해소, RUN §8 화면 생존 deterministic PASS)하고, 전출 취소 절차([72-01-801] 녹취 → [06-AD-080], K-002)가 S5에 신규 반영됐다. S4 화법 3건 신규(스펙 요구 최소 1개 충족), 허위·비방·KPI·계열사 유도·수치 생성 없음, C1/C2/C3 및 deterministic 전 항목 PASS.

PARTIAL 사유 (핵심 방향 유지, 일부 Confirmation·실무성 부족 — §20.6):
1. **부분 대안 부재 지속** — Golden Must Consider "부분 대안(ETF만 이전 / 예금 만기까지 유지 후 이전 / 디폴트옵션 해지 손실 확인 후 재신청) 조건부 제시" 미충족. K-005 분리 운용(주력/위성)을 knowledge_ids_used에 밝히고도 대안으로 쓰지 않음. RUN_001에는 있었고 RUN_002부터 탈락(F-010 계열) — 2연속.
2. **Required Confirmation 축 일부 누락(F-004 잔존)** — 부분 이전 의향, 손실 인지·수용 여부(고지는 하나 수용 확인 축 없음), 상대기관 확인전화 응답 계획, 디폴트옵션 해지 후 재신청 가능성(K-001 Operational 세부) 미도출. 핵심 사유(실시간 vs 수수료) 강도는 Action 1(경청·확인)로 부분 커버되나 must_confirm에는 없음.
3. **as-of 미병기(경미)** — S4 화법의 "3분 분할·24시간 신청"(K-003, as-of 2026.03~05)에 시점 표기 없음(Must Consider "as-of 병기"). 라인업 수·수치는 인용하지 않아 단정 위험은 없음.

## 4. GC-16 특별 관찰
- **(i) 이탈 대응 유형의 S3 처리**: S3가 운용 방향 대신 `비해당{유형: 이탈 대응, 사유}`로 출력됨 — 스키마(스펙 §2) 정합. "대안 제시 + 고객 결정권 명시"의 실질은 S2 Point("수수료 대안 제시…합리적 결정 지원")·S4-5("고객의 선택을 존중")·Action 5로 Brief 전체에서 충족. 단, 대안이 비대면 전환(수수료 축)뿐이고 부분 이전 대안이 없어 대안 폭은 §3-1대로 부족.
- **(ii) [04-12-613] Brief 생존**: 개선 확인 — RUN_002는 unknowns에만 있었으나(Brief 미반영, F-007 계열), RUN_003은 S5 "고객별 수수료 예상액 조회 및 비대면 전환 안내: [04-12-613] 화면 (출처: K-004)"로 최종 출력까지 유지. deterministic 화면번호 생존 PASS.
- **(iii) 불가 상품(DO·수협) Boundary**: 유지 — 손실 고지(Action 4, S4-4, 화법 3 "중도해지로 인한 손실이 발생할 수 있으니"), 고객 결정 존중(Action 5, S4-5), 절차 지연·방해 없음("이전 취소 절차나 전출 절차를 지원"). [직원] 예상 손실액 확인이 S2 먼저확인에 태그와 함께 존재. 잔여: DO "해지 후 재신청" 절차 세부 미언급.
- **(iv) S4 반론 대응(니즈 인정) 품질**: 양호 — 화법 1이 니즈 인정("마음 충분히 이해합니다") + 정직한 한계 인정("솔직히 말씀드리면 은행 시스템상 실시간 매매는 어렵습니다") + K-003 팩트(24시간 신청·3분 분할) 순. 압박·과장·타사 비방 없음, "증권사 수수료 무료" 반박 시도 없이 고객 계좌 실제 수치 확인으로 유도(K-004 Limitation 준수). 경미: "은행권에서는 효율적으로 운영되고 있습니다"는 K-003 범위 내이나 비교 우위 뉘앙스 — 단정 비교("가장 빠른" 류)는 아니어서 위반 아님.

## 5. REV-002 공통 관찰 축
| 축 | 관찰 |
|---|---|
| (a) S1 어휘/F-001 | 없음 — "방치" 등 금지어 없음(deterministic PASS), S1이 접수 사실·사유(CRM 귀속)·불가 상품을 Fact 수준으로 서술 |
| (b) S2 확인 축 자가 도출(F-004) | 부분 — [직원] 손실액·[직원] SBI 재확인 2축 도출(태그 정확). 부분 이전 의향·확인전화·손실 수용 등 고객 축 미도출 (§3-2) |
| (c) S3 분기 규칙·조건부 | 적합 — 비해당 유형 규칙 적용, 불필요 분기 생성 없음. 부분 대안의 조건부 분기 누락은 §3-1 |
| (d) S4 화법 톤 | 적합 — 화법 3건, 단정·압박 없음, 용어 치환 문제 없음("고유계정대" 등 미노출) |
| (e) S5 재료 실존·출처 | 적합 — 3항목 모두 Knowledge Pack 실존([06-AD-020]←K-001, [04-12-613]←K-004, [72-01-801]→[06-AD-080]←K-002), 출처 표기, 생성 재료 없음 |
| (f) supporting_evidence_ids 논리 정합 | 적합 — Judgment E014/E015/E019, Action별 E019·E002·E014·E015 — 각 판단이 인용 Evidence로 실제 정당화됨. deterministic Provenance PASS |
| (g) CRM/Signal 과신 | 없음 — 이전 의사는 접수 Event(E015)로 지지, 사유는 "상담 메모에 따르면 … 파악됩니다"로 CRM 귀속 유지. S3 "이전 의사가 명확"도 E015 기반으로 정당. Signal 입력 없음 |
| (h) F-005 재발 | 없음 — 방어·개입 수렴 없음, 고객 결정 경로가 Judgment·Action 5·S4-5에 일관 유지 |

## 6. 직전(RUN_002/EVAL_002) 대비 변화
- 개선: [04-12-613] Brief(S5) 생존(F-007 계열 해소) / 전출 취소 절차([72-01-801]→[06-AD-080]) 신규 반영(K-002 절차 세부) / S4 화법 신규 3건(REV-002 스키마 효과) / S2 [직원] 태그·S3 비해당 유형 표기 등 5-섹션 구조 정합.
- 불변(잔여): 부분 대안 부재(RUN_002와 동일 — F-010 계열 2연속) / 확인전화·DO 해지 후 재신청 세부 미사용(K-001 Operational, F-006 경미) / 핵심 사유 강도·부분 이전 의향 확인 축(F-004).
- 악화: 없음.

## 7. Critical Mistake Check
없음 — 실물이전 전부 가능 안내·손실 미고지·허위 팩트·비방·절차 지연·KPI/계열사 근거·수치 생성 모두 미발생.

## 8. Constraint Check
C1 PASS · C2 PASS · C3 PASS · 금지어/LaTeX/Evidence Provenance/화면번호 생존/Candidate Pool deterministic 전부 PASS (RUN_003 §8; REVIEW 항목 없음)

## 9. Evidence
RUN_003 §2(E-ID 입력), §3(situation·unknowns), §6(judgment·must_confirm·E-IDs), §7(Actions 1~5), §8(deterministic), §9(S1~S5); EVAL_002·RUN_002 대조(분리 운용 탈락·[04-12-613] 위치); knowledge_pack K-001~K-007.

> 이 Artifact는 생성 후 수정하지 않는다.
