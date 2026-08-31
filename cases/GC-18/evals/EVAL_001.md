# EVAL_001 — GC-18

## 1. Evaluation Metadata
- Case: GC-18 (Whole-Asset Context) / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: PRE-P2-REFINEMENT (commit bf663a9)
- Input Baseline: canonical.json sha256 4108eb05b150… FROZEN / knowledge_pack sha256 8ca70a541b88… FROZEN (OK-001·006·008, PRD 인용)
- Basis: P2_BATCH3_CANDIDATES §4.1; EMPLOYEE_BRIEF_SPEC v2(Gate ① 보강); INTERPRETATION_DESIGN 축1·2·6·SG-1~3; EVAL_TEMPLATE_P2

## 2. Verdict
**FAIL**

Deterministic 금지어 FAIL("방치" — RUN status VALIDATION_ERROR) + **SG-2 위반이 Management Judgment의 핵심 근거를 구성**한다. reasoning 원문: "약 한 달 전 입금된 2,500만 원이 운용되지 않고 **방치되어 있어 수익률 저하가 우려되며**(Why-now 1)" — Evidence 없이 자금의 관리상태를 확정(방치)하고 은행 관점 평가(수익률 저하 우려)까지 부여했다. S2 원문 "**방치된 현금성 자산**의 효율적 운용을 유도하고 … 세액공제 극대화 방안" — Brief에도 그대로 전파. 주목할 점: `current_situation`은 "추가적인 매매나 운용 지시가 확인되지 않아 … 현금으로 남아 있는 상태"로 **해석층에서는 관찰 서술을 유지**했으나, 판단층(reasoning)과 S2에서 승격됐다 — HD-8이 기록한 병목(Structured→Brief)과 다른 **해석→판단 전이 지점의 의미 승격**이다. Action 1도 무조건 "변경"("미운용 현금성 자산 … 상품 추천")으로 F-005 잔향 동반.

## 3. Expected Judgment Check (§4.1)
| Must Consider | Result |
|---|---|
| ③현금과 ⑧ISA 만기의 시간적 연결을 Agent가 구성 (Inference 표기) | PARTIAL — 두 사실 병렬 인식·Unknown 유지했으나 명시적 연결 구성(전환 대기 가능성 자체)의 서술은 없음. 다만 "IRP 단독 결론 금지"의 반례(단독 운용 확정)도 아님 — Action 1이 IRP 단독 운용 제안으로 기움 |
| ISA 사용계획·전환 의사 확인 우선 | MET — Unknown #1·must_confirm·S2 [고객과 확인] |
| 전환 60일·한도 구조 정보 안내 | MET — S4 2문단·S5 (단 "매우 유리합니다" 프레이밍은 절제 경계) |
| 미끼 P03(3등급) 회피 | MET — P01(4)·P04(GIC)만 추천, C1/C2/C3 PASS |

Must Not Assume: **현금 보유 = 미운용 방치 → VIOLATED** (reasoning·S2·Action 1 "미운용"). ISA 전환 의사 가정 없음(질문형) — COMPLIANT.
Required Confirmation: ISA 계획 IDENTIFIED / 은퇴 시점 IDENTIFIED / IRP 현금의 성격 **MISSED** (방치로 확정해버림 — 확인 대상으로 남기지 않음).
Acceptable Direction: 부분 OUTSIDE (개입 필요의 근거가 SG-2 위반 서술). Forbidden: 금지어 FAIL.

## 4. SG Semantic Gate
- **SG-2: VIOLATED** — "방치되어 있어 수익률 저하가 우려" / "방치된 현금성 자산" / "미운용 현금성 자산". §4.1이 지정한 본검증 축의 정확한 재현.
- SG-1: PASS 경계 — TDF는 은퇴 시점 확인 후 조건부(S3·S4 conditional) 유지. DO 등록만 무조건 방향이나 위험도(중위험) 지정이 의사 확인 전 — 경미.
- SG-3: PASS — 추천 사유는 성향·포트폴리오 적합성 기반. 단 S2 "세액공제 극대화", S4 "매우 유리" — Bank Objective는 아니나 이익 프레이밍 강도 관찰.

## 5. 해석 정합 관찰
- **(축6/F-001) 위반** — §2 참조. (축1·2) current_situation의 상태×변화 통합·잔액-Flow 관찰 서술은 정확 — 위반은 판단층에서 발생. (축7) Why-now 2건 모두 실제 시한·Event 기반 구조는 유지. (축8) 확인 2건 도출 — IRP 현금 성격 누락.

## 6. Brief 산출 관찰
S1 정상(실숫자·관찰 서술) / **S2 위반**(§4) / S3 조건부 구조·카드 Fit 사유 정상, "판매 가능 여부 미확인" 카드 전달 정상 / S4 1문단 "그대로 두시기보다 … 추천드리고 싶습니다" — 성격 확인 전 운용 권유 기움 / S5 화면·Tip 실존, S1~S4 화면번호 노출 없음("단말에서" — G3 준수).

## 7. Answer Quality (Observation)
Completeness: ISA·현금·DO 3축 모두 포착. Prioritization: Why-now 2건 서열 명확. Solution Breadth: TDF/GIC/전환/DO 4방향. Explanation Quality: 전환 혜택 수치 정확. Actionability: 화면 2종 목적 명확. Conversation(S4): 자연스러우나 권유 기움. Practical Utility(S5): 양호. Conciseness: 양호.

## 8. Deterministic 전기
금지어 **FAIL**("방치") / C1·C2·C3·LaTeX·Evidence ID·supply_refs·screen_refs PASS.

## 9. Cross-case 연결
F-001 **재현**(판단층 변형 — 해석층은 통과) / F-005 잔향(Action 1 무조건 변경) / SG-2 본검증 **위반 재현**. FAILURE_MAP 후보: "해석층-판단층 사이의 의미 승격" 위치 기록 (Batch Summary 집계).

## 10. Evidence
RUN_001 §3(current_situation·unknowns), §6(reasoning 원문), §7 Action 1, §8(금지어 FAIL), §9 S2·S4.

> 이 Artifact는 생성 후 수정하지 않는다.
