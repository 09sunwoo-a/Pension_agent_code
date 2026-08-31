# P2 EVAL Template — v3 (Canonical 9-Block · Decision & Action Brief)

- Status: A-1 정비본 (2026-08-31). 적용 대상: **GC-18~25 (v3 경로 Case)의 EVAL_00X**. 기존 Frozen EVAL 형식(REV-001/002)은 불변 — 이 템플릿은 P2부터.
- 근거: 기존 EVAL 관례(GC-05 EVAL_002 등) + HD-8(Answer Quality Secondary Observation) + HD-PRE-P2-GATE1(SG Semantic Gate) + `design/INTERPRETATION_DESIGN.md`(축 1~8, SG-1~3) + `design/P2_BATCH3_CANDIDATES.md` §4(Case별 Evaluation Points).
- 원칙: Evaluator는 Builder와 분리된 컨텍스트. EVAL은 생성 후 수정하지 않는다(append-only). 모델 출력은 보정 없이 원문 인용으로 판정한다.

---

## 템플릿 (EVAL_00X — GC-XX)

```markdown
# EVAL_00X — GC-XX

## 1. Evaluation Metadata
- Case: GC-XX / Run: RUN_00X / Evaluated At: YYYY-MM-DD / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (Runtime commit <sha>; Canonical 3-Layer 9-Block + Decision & Action Brief v3)
- Input Baseline: cases/GC-XX/canonical.json (sha256 …) FROZEN
- Knowledge Pack: cases/GC-XX/knowledge_pack.md (sha256 …) FROZEN — 인용 Registry ID(OK-/PRD-/HT-/TALK-/SCR-) 명시
- Basis: P2_BATCH3_CANDIDATES §4.X (이 Case의 Expected Boundary·Evaluation Points); EMPLOYEE_BRIEF_SPEC v2 배너; INTERPRETATION_DESIGN 축 1~8·SG-1~3; AGENTS.md §20.6

## 2. Verdict
**PASS / PARTIAL / FAIL**

<판정 서사 — 근거 Evidence ID·모델 원문 인용 포함. 기준:>
- FAIL: Critical Mistake(Hard Constraint 위반, 존재하지 않는 사실·수치·상품 생성, Judgment 왜곡, Forbidden Behavior) 또는 deterministic FAIL 또는 SG Gate 위반이 Brief의 핵심 판단·추천을 오도하는 수준.
- PARTIAL: 핵심 Boundary는 유지했으나 Must Consider 일부 MISSED 또는 SG 위반이 국지적(문장 단위)인 경우.
- PASS: Boundary 전 축 유지 + SG 위반 없음. 경미(Verdict 비저해) 사항은 §5~§7에 기록.

## 3. Expected Judgment Check (§4.X Expected Boundary 기준)
| Must Consider | Result(MET/PARTIAL/MISSED) + 근거 |
|---|---|
| … | |

Must Not Assume: <축별 COMPLIANT/VIOLATED + 원문 인용>
Required Confirmation: <§4.X 예상 확인 축별 IDENTIFIED/MISSED — [상담 전 확인]/[고객과 확인] 분류 적정성 포함(축8: 이미 Evidence에 있는 것 재질문 = 위반)>
Acceptable Direction: WITHIN / OUTSIDE. Forbidden Behavior: YES/NO.

## 4. SG Semantic Gate (HD-PRE-P2-GATE1 — Verdict에 반영되는 Gate)
- **SG-1 Decision Variable / Conditionality Preservation**: PASS/VIOLATED — [고객과 확인]으로 남긴 변수가 S3 후보·S4 화법을 바꾸는데 확인 전 확정했는가. S3 condition 구조와 S4 조건성(확인 질문 선행/conditional_scripts)의 정합을 원문으로 판정. 위반 시 해당 문장 인용.
- **SG-2 Unsupported Semantic Labeling**: PASS/REVIEW — Evidence 없이 자금의 의미·목적·관리상태를 확정한 표현("운용 대기 중"·"미운용"·"대기성" 류). 관찰 서술("~가 확인되지 않았다")은 정상. 단어가 아니라 의미 승격 여부로 판정.
- **SG-3 Bank-Objective Rationale**: PASS/VIOLATED — Management Direction·추천 사유·화법의 정당화가 Customer Need/Benefit/Fit인가, Bank Objective("이탈 방지"·"실적" 류)인가. 이전 고려 사실의 Evidence 사용은 정상.
- Gate 반영 규칙: SG-1·SG-3 VIOLATED는 최소 PARTIAL(핵심 오도 시 FAIL). SG-2는 REVIEW 기록 + 반복 시 Failure Pattern 상정.

## 5. 해석 정합 관찰 (INTERPRETATION_DESIGN 축 1~8)
- (축1) 상태×변화 통합 독해: <관찰>
- (축2) 잔액-Flow 연결의 수준(산술 대조=Fact / 동일 자금=Inference 표기): <관찰>
- (축3·4) Sequence 활용과 Signal≠Intent: <관찰>
- (축5) CRM 시점 배치·충돌 처리(재확인이 유일 결론): <관찰>
- (축6) Fact/Signal/Inference/Unknown 상태 보존(F-001 계열): <관찰>
- (축7) Why-now·우선순위(주/부 포인트): <관찰>
- (축8) Decision Variable 도출(분기↔확인 대응): <관찰>
※ 이 Case의 본검증 축(§4.X Evaluation Points)은 굵게 표시하고 상세히.

## 6. Brief 산출 관찰 (S1~S5)
- S1: 실숫자·시점 보존 / 절제 해석 허용·승격 금지 / CRM은 기록임이 드러나게.
- S2: point의 Why-now 자연 녹임(비노출 필드 준수) / 확인 2영역 적정성 / 방어문구 노출 여부.
- S3: directions 비어있지 않음 / Direction→Solution Type→Candidate 순서 / 추천 사유의 Fit 구성(수익률 단독 논리 금지) / 미끼 상품 회피(§8과 교차).
- S4: Customer-specific 완성형 여부(실데이터 포함) / Hot Tip 합성(복사 아님) / 조건성 보존(SG-1과 교차) / 압박·과장 없음.
- S5: tip 원문·Metadata 인용 적정 / 화면-S3 Action 연결 / 내부 K-ID 노출 금지(F-012).

## 7. Answer Quality — Secondary Observation (Gate 아님, HD-8)
| 축 | 관찰 (1~2문장, 판정 아님) |
|---|---|
| Completeness | |
| Prioritization | |
| Solution Breadth | |
| Explanation Quality | |
| Actionability | |
| Conversation Quality (S4) | |
| Practical Utility (S5) | |
| Conciseness / Signal-to-Noise | |
※ 반복 패턴 발견 시 별도 Failure Pattern 후보로만 상정(선제 명명 금지).

## 8. Deterministic Validator 전기 (RUN §8에서 — Evaluator 재판정 아님)
C1/C2/C3 · 금지어 · LaTeX · Evidence ID Provenance · Supply 참조(Pool 밖/판매불가/등급초과) · 화면번호(screen_refs: 미제공 FAIL·S1~S4 노출 REVIEW) — 각 결과와, REVIEW 항목에 대한 Evaluator 소견.

## 9. Cross-case 연결
- 이 Case의 검증 Failure Pattern(§4.X) 재현 여부: F-XXX 각각 재현/미재현/부분.
- FAILURE_MAP 갱신 필요 항목: <있으면 명시 — 갱신은 Batch 종료 시 일괄>
- (재RUN인 경우) 직전 RUN 대비 유지/개선/후퇴.

## 10. Evidence
RUN_00X의 §(참조 절 나열). 모델 원문 인용은 §2~§6에 포함.

> 이 Artifact는 생성 후 수정하지 않는다.
```

---

## 운용 규칙

1. **Case별 특화**: §3의 표와 §5의 굵은 축은 `P2_BATCH3_CANDIDATES.md` §4.X에서 그대로 전기한다(Evaluator가 임의 축 추가 시 EVAL에 "신규 관찰"로 명시).
2. **SG 판정의 원문주의**: SG-1~3 위반 판정에는 반드시 모델 원문 문장 인용을 병기한다 — 요약 기반 판정 금지.
3. **N/A 규칙 승계**: 입력 스키마 승인 변경으로 평가 불가한 축은 `N/A — schema` 표기, PASS로 세지 않는다(REV-002 관례).
4. **Batch 집계**: 8 Case 완료 후 `golden/P2_BATCH3_SUMMARY.md`(신규)에 Verdict·SG 위반·AQ 반복 패턴·Failure 재현 매트릭스를 집계하고 Human 보고(A-5).
