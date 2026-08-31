# REV-002 Regression — 8 Case (input_v2 Evidence Pack, 2026-08-31)

- Builder: Gemma 4 (`gemma-4-31b-it`, API default) / Evaluator: Claude (별도 Context, Case별 독립 평가) / Runtime: REV-002 (`prototype/REVISIONS.md`)
- 대상: GC-03·04·05·09·11·14·16·17 — 각 1회 실행(모델 출력 기준, 전송 재시도 0). P0 4 Case는 RUN_003/EVAL_003, P1 4 Case는 RUN_002/EVAL_002.
- 변환: `input_v2.md` — 승인된 8-섹션 스키마 일관 적용(삭제 필드 미반입), 삭제 입력 의존 축은 EVAL에서 `N/A — Input removed by approved REV-002 schema`(PASS 아님). 기존 Frozen Case/RUN/EVAL 불변.
- Stop Condition 없음. Deterministic: C1/C2/C3 위반 0/8 · 금지어 0/8 · LaTeX 0/8 · Candidate Pool 위반 0/8 · evidence-id FAIL 1/8(GC-11, 슬롯 혼동) · 화면 생존 REVIEW 1/8(GC-05).

## 1. 결과

| Case | Run/Eval | Verdict | 직전 대비 | 핵심 관찰 |
|---|---|---|---|---|
| GC-03 | RUN_003/EVAL_003 | **PASS** | ↑ (PARTIAL→) | 확인 우선 정확; S3 조건부 분기+유지 경로 복원(F-010 해소); 환급 확인 축 힌트 없이 자가 도출 |
| GC-04 | RUN_003/EVAL_003 | **PASS** | 유지·강화 | Pair 핵심(명시 의사 존중→유지) 보존; DO 예상 기준일 경과를 확정 없이 확인 축 처리; CRM 재확인 Action 승격 |
| GC-05 | RUN_002/EVAL_002 | **PASS** | 유지 | 의사 부재→확인 우선; Signal→Intent 승격 없음; 분기 2개+Pool 준수. 경미: 화법 내 선제 단정, 자금 목적·기간 축 탈락 |
| GC-09 | RUN_002/EVAL_002 | **PASS** | ↑ (PARTIAL→) | 직전 사유 4건 전소 — "방치" 해소(R-Fact 효과), 1,500만 만기 사용(F-003 해소), 확인 축 5/5 자가 도출, 2단계 절차 정확 |
| GC-11 | RUN_002/EVAL_002 | PARTIAL | ↓ (PASS→) | 핵심(1,800만 대기 정상·ETF 불가·분기) 유지. 후퇴: 1,500만 "초과" 확정(직전엔 확인), K-ID의 evidence 슬롯 기재(형식) |
| GC-14 | RUN_003/EVAL_003 | PARTIAL | ↓ (PASS→) | S3 비해당 규칙·세제 구조 정확. 후퇴: S1에서 CRM "무주택" 진술을 사실 승격(F-001 변형; structured는 보존, 확인 축 존재로 Critical 아님) |
| GC-16 | RUN_003/EVAL_003 | PARTIAL | 유지(개선) | Boundary 전부 유지; [04-12-613] S5 생존(직전 미반영 해소); S4 화법 신규. 잔여: 부분 대안 부재 2연속(F-010) |
| GC-17 | RUN_002/EVAL_002 | PARTIAL | 유지(개선) | **F-001 "방치" 미재발**; 은퇴 시기 확인 축 힌트 없이 자가 도출; K-002 실사용. 잔여: H/UH·S5 빈약 |

**PASS 4 · PARTIAL 4 · FAIL 0** (개선 2 · 유지 4 · 후퇴 2). Pattern 상세: `cases/FAILURE_MAP.md` "REV-002 Regression" 절.

## 2. REV-002 효과 확인 (설계 목표 대비)

1. **F-001 "방치" 계열 소멸 (0/8)** — 목표 달성. DO "적용 예상 기준일 + 실제 적용 여부 별도 확인" R-Fact가 GC-09(35일)·GC-17(60일)에서 직전 발생분을 정확히 해소. 단 **F-001의 의미 층위는 자리만 옮겨 잔존**: CRM 진술 승격(GC-14)·세제 수치 확정화(GC-11)·화법 선단정(GC-05 경미) — 어휘 필터로 잡히지 않는 변형 3건.
2. **F-003·F-010 구조 효과 실증** — ⑥ Upcoming Events 분리로 GC-09 부차 만기 포착; 분기 규칙(Branch Preservation)으로 GC-03 유지 경로 복원. GC-16 부분 대안 부재는 잔존(입력 구조로 해결 안 되는 유형).
3. **확인 축 자가 도출 (F-004)** — Missing 힌트 14개 제거에도 핵심 축은 전 Case 도출(GC-09 5/5, GC-17 은퇴 시기 첫 축). 부차 축 1~2개 누락은 5/8 잔존 — REV-001 수준 유지, 악화 없음.
4. **F-005 재발 없음 (0/8)** — 기회 중심 Brief(관리 포인트 커밋) 구조에서 Counterfactual Pair가 정확히 갈림(GC-04 유지 / GC-05 확인 우선). 판단층/전달층 분리 설계 유효.
5. **S4 화법 8/8 생성, S5 재료 8/8 존재** — 감사 시점 0/18에서 스키마 강제로 전환 성공. 품질 이슈: S5 출처의 K-ID 표기 4/8(직원이 찾아갈 수 없는 내부 ID — F-012 후보), 재료 생성(hallucination) 0건.
6. **Evidence Provenance** — supporting_evidence_ids 8/8 기재, 무근거 관리 포인트 0. 슬롯 혼동 1건(GC-11, K-ID 혼입 — F-011 후보, deterministic 검출 성공).

## 3. 후퇴 2건의 성격

GC-11·GC-14 모두 **핵심 판단은 유지, S1/수치 서술의 확정화**로 후퇴 — REV-001 때 "방치"가 발생하던 것과 같은 산문 지점에서, 금지어가 아닌 형태로 나타났다. 공통 구조: **structured 출력은 불확실성을 보존하는데 Brief 산문에서 승격**(F-001/F-008의 의미 층위). 어휘 확장(금지어 목록 추가)은 두더지잡기이므로, Revision 후보는 (a) S1/S3 산문 생성 시 "CRM·수치 추정값은 조건 표현 유지" 프롬프트 보강(Operational), (b) Brief↔structured 대조의 의미 검증은 Evaluator 축 유지(§3.2 설계대로).

## 4. Revision 후보 (Evidence만 — 구현 보류, Human 결정 대상)

1. **F-012 S5 출처 형식** (4/8): S5 source에 K-ID 대신 자료명/SRC-ID/화면 마스터 표기 — 프롬프트 문구 수준(Operational 가능성).
2. **F-011 슬롯 혼동** (1/8): OUTPUT_INSTRUCTION에 "K-ID는 knowledge_ids_used에만" 1줄 — Operational.
3. **F-001 변형 (산문 확정화)** (2/8+경미 1): §3의 (a) — 프롬프트 보강. 재현율 관찰 후 판단 권장.
4. GC-16 부분 대안 부재 (2연속): Case 특이적일 수 있음 — P2 이탈 Case 추가 시 재관찰.

## 5. 다음 단계 (Step 6 — Human 결정)

(a) 후퇴 2건·Revision 후보에 대한 처리 방향(Operational 보강 즉시 적용 vs 관찰 유지), (b) REV-003(Knowledge Key Conditions) 여부 — F-006이 2/8 경미로 감소(전처리·Usage 개선 효과)하여 우선순위 재평가 필요, (c) P2 Batch 3 설계 착수(신규 섹션 Wider Context·Digital Signals 본검증 + Coverage Gap), (d) 잔여 Availability `?` 2건·R4 rule_source 확정.
