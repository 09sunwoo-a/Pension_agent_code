# P2 Batch 3 Summary — GC-18~25 (RUN_001 / EVAL_001)

- 작성: 2026-08-31. 실행: HD-P2-GATE2 승인 범위 (Freeze bf663a9 → RUN_001 8건 실호출 gemma-4-31b-it → EVAL_001 8건 → 본 집계). Runtime: PRE-P2-REFINEMENT (v3 Canonical 3-Layer · Decision & Action Brief · SG Semantic Gate 최초 적용 Batch).
- Evaluator: Claude (separate context from Builder). 기준: `design/EVAL_TEMPLATE_P2.md` — 기존 Boundary + SG-1~3 + Answer Quality 8축 Observation.

## 1. Verdict Matrix

| Case | 검증 목적 | RUN status | Verdict | 핵심 근거 |
|---|---|---|---|---|
| GC-18 | Whole-Asset / SG-2 본검증 | VALIDATION_ERROR (금지어) | **FAIL** | "방치되어 있어 수익률 저하 우려"(reasoning)·"방치된 현금성 자산"(S2) — SG-2 위반이 판단 근거를 구성. F-001 재현 |
| GC-19 | Signal→Intent / SG-3 본검증 | SUCCESS | **PASS** | 승격 없음·접점 조건화·방어 rationale 없음 |
| GC-20 | CRM 과신 / SG-1 본검증 | SUCCESS | **PARTIAL** | 양방향 확정 회피는 통과 — S4에서 조건성 부분 소실(원금보전 분기 화법 부재·거절 극복 단일 방향·TDF 내장 질문) |
| GC-21 | Knowledge Gap / SG-1 본검증 | SUCCESS | **PARTIAL** | 판단·구조 우수 — S4에서 "매수 시점 … 차이가 발생한 것으로 보입니다" 원인 설명 생성(HD-P2-GATE2 (2) 위반) |
| GC-22 | 다중 시한 / SG-2 본검증 | SUCCESS | **PASS** | 1.2억 관찰 서술("대기 중, 5일 경과")·3/4 시한 보존·확인 선행 모범. 경미 F-003(세액공제 여력 탈락) |
| GC-23 | 확인되지 않은 실행경로 / F-010 일반화·SG-3 본검증 | SUCCESS | **PASS** | 부분이전 Epistemic 유지(가능/불가 비확정·운영 확인 연결)·실존 대안+존중 경로 Solution 연결·Bank Objective 사유 없음 |
| GC-24 | 결정세액 조건 / F-002 | SUCCESS | **PASS** | 잔여한도≠환급 전 층위 유지·장기 구속 고지·한도 혼용 없음 — 최소 결함 수행 |
| GC-25 | 7/1 경계 / T3 비승격·SG-3 본검증 | SUCCESS | **PARTIAL** | 존중·양분기 모범 — "7/1 이후 해지가 **가장 유리합니다**" T3 단독 지식의 확정 승격 + 공식 확인 연결 부재 |

**집계: PASS 4 / PARTIAL 3 / FAIL 1.** Deterministic hard-fail 1건(GC-18 금지어), C1/C2/C3·Evidence ID·supply refs·screen refs 8/8 PASS — 미끼 상품(2~3등급) 8 Case 전 건 회피, 화면번호 S1~S4 노출 0건(Pilot 3/3 REVIEW → 본 Batch 0건: **G3 프롬프트+validator 조합의 효과 확인**), sellable null → "판매 가능 여부 미확인" 전달을 모델이 [상담 전 확인] 항목으로 스스로 수용(GC-20·23).

## 2. Failure Cluster (cross-case)

### FC-1. 화법층의 확실성 인플레이션 (신규 Cluster 후보 — 3/8 Case)
해석층(current_situation)과 판단층은 상태·가능성을 보존하는데, **S4 고객 대면 화법에서 확정으로 굳는** 공통 위치:
- GC-21: S2 [상담 전 확인]에 "산정 기준·원인 확인"을 두고도 S4에서 원인("매수 시점 효과")을 설명 — Knowledge Gap 메움.
- GC-25: reasoning·S1은 "가능성"인데 conditional에서 "가장 유리합니다" — T3 단독 지식의 확정 승격.
- GC-20: S3의 양분기가 S4에서 단일 방향(재도전 유도)으로 축소.
- 성격: HD-8이 기록한 병목(Structured→Brief Semantic Preservation)의 **v3 잔존 형태** — 다만 위치가 좁혀짐: S1~S3는 대체로 보존되고 **S4 scripts/conditional_scripts가 취약 지점**. F-012류 명명은 재현 관찰 후 (선제 명명 금지 — 다음 Batch에서 재관찰 시 상정).

### FC-2. 해석층-판단층 사이의 의미 승격 (1/8 — GC-18)
current_situation은 관찰 서술("운용 지시가 확인되지 않아 남아 있는")을 유지했으나 management_judgment.reasoning에서 "방치·수익률 저하 우려"로 승격. GC-22가 동일 구조(거액 현금 대기)에서 관찰 서술을 유지한 것과 대비 — **차이 변수 후보: GC-18은 Whole-Asset 연결(ISA)로 판단 부하가 높은 상태에서 Why-now를 2개 구성해야 했음.** 단일 재현이라 명명 보류, F-001의 판단층 변형으로 기록.

### FC-3. 통과 확인 (미재현)
- Signal→Intent 승격 (GC-19) / CRM 과신·Conflicting Evidence (GC-20 판단층) / Performance 단독 Trigger (GC-21) / F-002 한도 과적용 (GC-24) / HD-7 위반·해지 만류 (GC-25) / **F-010 일반화 (GC-23 — GC-16 2연속 잔여의 해소**: 무근 재료 제거 + 확인·대안 구조로 재정의하자 통과. 원인 분리 판정: Case 재료 요인 우세) / Bank Objective 추천사유 (SG-3 3 Case 전부 통과 — Pilot DIAG-03 유형 재발 없음).
- F-003: 경미 1건(GC-22 세액공제 여력 — 4축 중 1축 탈락. REV-002 부 포인트 구조가 3/4까지 작동).

## 3. Answer Quality — Batch Observation (Gate 아님)

| 축 | Batch 관찰 |
|---|---|
| Completeness | 7/8 충분. GC-22만 부차 1축(세액공제 여력) 누락 |
| Prioritization | 전반 명확. GC-22의 주 포인트 선택(확인 우선 vs 시한 우선)은 Expected 문면과 다르나 방어 가능한 재구성 — 우선순위 규범의 서술 정밀화 여지 |
| Solution Breadth | 과잉 없음 — 상품 불요 Case(GC-25 빈 Pool)에서 방향만으로 정상 구성. 분기 수와 확인 수의 대응 일관 |
| Explanation Quality | 결정세액(GC-24)·현금이전 구조(GC-23)·자동 재예치 폐지(GC-22) 전달 우수. **GC-21의 '명료해 보이는 원인 설명'이 오히려 위반** — 설명 품질과 Grounding의 긴장 관찰 |
| Actionability | 우수 — [상담 전 확인]의 운영 확인 항목화(GC-23), 판매 가능 여부 확인 항목화(GC-20) 등 실행 지향 |
| Conversation Quality (S4) | 확인 질문 선행 모범 2건(GC-22·25) / 방향 내장 질문 1건(GC-20) / 원인 설명 1건(GC-21) — **S4가 품질·위반 모두의 집중 지점** |
| Practical Utility (S5) | supply 규모에 비례 — 최소 supply Case(GC-19·21)에서 빈약. Tip 활용은 원문 취지 준수(HT-001 bank_objective 태그의 왜곡 없음) |
| Conciseness | 전반 양호 |

## 4. 구조 효과 관찰 (Revision 판단 재료)

1. **G3(화면 S5 단일 위치)**: Pilot 3/3 노출 → 본 Batch 0/8 — 프롬프트 원칙 15+18 개정 효과.
2. **sellable null 전달**: 모델이 "미확인"을 확인 항목으로 승계 — null 유지 설계(HD-P2-GATE2 (4))가 실행 검증 축으로 작동.
3. **부정 확인 Knowledge(OK-003)**: "절차가 확인되지 않음"을 Limitation과 함께 주자 모델이 정확히 Epistemic 유지 — **Knowledge Gap을 명시적으로 알려주면 지키고(GC-23), 알려주지 않은 Gap은 메운다(GC-21)** — Knowledge 설계의 핵심 시사점: Gap의 명시가 Gap 메움 방지의 유효 수단.
4. SG Gate의 판별력: 8 Case에서 PASS/PARTIAL/FAIL이 검증 목적별로 분리 — Gate 기준이 변별력 있음.

## 5. 다음 단계 후보 (Human Gate 판단 대상 — 착수하지 않음)

- (a) FC-1(S4 확실성 인플레이션) 대응: SYSTEM_ROLE_V3 원칙 18의 S4 적용 강화 또는 별도 원칙 — **Semantic Revision 성격, Human Gate 필요.** 재현 1회차이므로 선(先)관찰(P2 재RUN 또는 P3) 후 결정도 가능.
- (b) GC-18 재RUN 여부: FAIL Case의 교정 Revision 없이 재RUN은 무의미 — (a)와 묶어 판단.
- (c) FAILURE_MAP 갱신: FC-1·FC-2를 후보로 기재(정식 F-번호 명명은 재현 후 — §2 원칙 유지).
- (d) B-3 확장 구축 재개 및 P3(Knowledge Selection) 상정: 본 Batch로 "Knowledge Gap 명시의 효과"가 확인되어 Registry 확장의 우선순위 근거 확보.

---

## 6. 선택 Regression (RUN_002 — Human 지시, 2026-08-31)

- 대상: Target GC-18·20·21·25 + Control GC-22·23. Input Baseline 전 건 불변. 적용 변경: SYSTEM_ROLE_V3 원칙 6 보강(FC-2)·원칙 19 신설(FC-1)·OUTPUT_INSTRUCTION s4 주석·SG-1/SG-2 판정 보강 (commit d6edbe4). Deterministic validator 추가 없음.

| Case | 확인 목표 | RUN_002 | 판정 (EVAL_002, 목적 한정) |
|---|---|---|---|
| GC-18 | 의미 승격 제거 | SUCCESS | **해소** — "방치·수익률 저하 우려" 소멸, reasoning 관찰 서술로 교체. 잔존: "미운용 현금" 라벨 (SG-2 REVIEW, 승격 아님) |
| GC-20 | S4 조건성 보존 | SUCCESS | **해소** — 유지 분기 화법 생성·열린 질문으로 교체 |
| GC-21 | Knowledge Gap 비보충 | SUCCESS | **해소** — 원인 설명 소멸, 열린 질문 + 유지 분기 생성 |
| GC-25 | T3 비승격 | SUCCESS | **해소** — "가장 유리합니다" → "더 유리할 수 있습니다"·"가능성", 즉시 해지 존중 유지 |
| GC-22 (Control) | 후퇴 없음 | VALIDATION_ERROR | **어휘 수준 후퇴 1건** — "자금이 방치되지 않도록 돕는 법적 의무"(DO 제도 목적의 부정형 일반론, 의미 승격 아님·Critical Semantic 아님). 의미 축(확인 선행·시한 보존·조건부)은 전부 유지 |
| GC-23 (Control) | 후퇴 없음 | SUCCESS | **후퇴 없음** — 부분이전 Epistemic·SG-3 유지 |

## 7. P2 Batch 3 종료 판정 (2026-08-31)

**종료 조건 충족 — P2 Batch 3 종료 처리.**
- ① 핵심 Failure 4건 전부 해소 확인 (§6) ② 신규 Critical Semantic Failure 없음 — GC-22 Control의 금지어 재발은 비승격적(제도 일반론) 어휘 사용으로 Critical Semantic이 아니며, 의미 축 후퇴도 없음.
- **Human 인지 필요 예외 1건**: GC-22 RUN_002 금지어 FAIL — F-001 대체 어휘 규범이 "제도 목적 설명" 문맥을 커버하지 못하는 관찰. 지시(Failure Evidence 기반 최소 수정·deterministic 과추가 금지)에 따라 추가 교정하지 않고 기록만 남김. 필요 시 후속 판단 대상.
- FC-1·FC-2는 Candidate Cluster로 `cases/FAILURE_MAP.md`에 기록 (정식 F-번호 미부여 — 이후 재현 시 부여 검토).
- 추가 Case 설계·새 P2 Batch·대규모 Architecture 개선 없이 종료. 다음 단계 인수인계: `design/HANDOFF_P3_INTEGRATION.md`.
