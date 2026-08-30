# P1 Golden Batch 2 — Summary (BATCH_002, REV-001 Runtime)

- 실행일: 2026-09-01 / Builder: Gemma 4 (`gemma-4-31b-it`, API default) / Evaluator: Claude / Runtime: REV-001 (8cf3787; HTTP read timeout 300s는 Operational 변경)
- 대상: P1 9 Case (GC-02, 05, 07, 08, 09, 11, 13, 15, 17) 각 RUN_001·EVAL_001 (모델 출력 기준 1회; GC-02·GC-07은 1차 API read timeout으로 무출력 후 재실행)
- Stop Condition: 없음. C1/C2/C3 deterministic validation 9/9 PASS.

## 1. 결과

| Case | Title | Verdict | 핵심 관찰 |
|---|---|---|---|
| GC-02 | [Pair↔01] 만기·위험중립·펀드 경험 | **PASS** | 분산투자 가능 접근 + 원리금보장 동등 병렬, 4~6등급·"일부"·6주 DO·예약변경; 만기 길이·고유대 200만 미처리(경미) |
| GC-05 | [Pair↔04] 행동 신호·의사 없음 | **PASS** | 행동=Contextual Evidence, 확인 우선, 비교그룹 압박 금지, 조건부 직접/위임 + 유지 경로 |
| GC-07 | 70% 한도 초과 | PARTIAL | 현금성 운용≠비중 하락(K-004) 정확, 추가입금 경로, 페널티 Operational Check; TDF 예외 설명·교체매매 경로·추가 매수 의향 누락 |
| GC-08 | 중도해지 vs 만기보유 | PARTIAL | 계산기 선행·3년제↔개시 정합·500만 DO 6주·컨설팅센터; "유지+예약변경" 경로·ELB 조건 미명시 |
| GC-09 | DO 초저위험·성향 상향 | PARTIAL | 등록 변경≠적립금 이동(2단계)·계산기·확인 선행·단계적; 11월 만기 1,500만 누락, "방치" 표현 |
| GC-11 | 연금수령 중 ETF 희망 | **PASS** | 실행 불가 정확, 지급 대기 1,800만 정상·300만만 운용, 방식 변경 영향·[02-12-221]·인컴 대안·1,500만 세전 확인 |
| GC-13 | ISA 만기·세액공제 | **PASS** | 60일·10%/300만·1,800만 별개·13.2%·추징→장기 자금만·이월전환·2주 DO; 결정세액 조건 미언급(경미) |
| GC-15 | 연금저축→IRP 불가 | **PASS** | 55세·5년 미충족 정확, 충족 시점, 해지 위험 고지, 연저 간 이전은 확인 후, IRP 별도 점검 |
| GC-17 | TDF 선택 | PARTIAL | 은퇴 시기 확인·빈티지 산식·4~6등급·특정 상품 금지·앱 절차; 운용사별 등급 차이·DO 유형 분기·H/UH 없음, "방치" |

**PASS 5 · PARTIAL 4 · FAIL 0.** Counterfactual Pair 2쌍(GC-01↔02, GC-04↔05) 모두에서 판단 차이가 정확히 갈렸다.

## 2. Failure Pattern (Batch 2)
F-005 0/9 · F-010 2/9(경미) · F-006 5/9(경미, 세부 수준) · F-001 2/9(경미) · F-003 2/9 · F-004 4/9(경미) · F-007 0/9 · F-008 0/9 · F-009 0/9. 상세 `cases/FAILURE_MAP.md` "P1 Batch 2" 절.

## 3. REV-001 효과의 재확인 (Batch 1 RUN_002 + Batch 2, 17 Case)
- Action/Change Bias: 강한 재현 0/17. Judgment 유형이 Case 성격과 일치(실행 불가 2, 현상유지 1, 확인 우선 다수). Intervention Avoidance 없음 — 개입이 필요한 GC-09는 '개입 필요' 명시.
- Knowledge Usage: 핵심 K-item 인용률 높음; 잔여는 "항목 내부 세부"(운용사별 등급, ELB 조건, 예약 시점, 결정세액 조건) 수준으로 수렴 — Knowledge 표현에서 세부 조건을 별도 필드로 분리할 필요(Revision #2 후보 근거).
- C2 validator: 위반 0; 6 Case에서 모델이 "4~6등급" 등 범위를 스스로 인용 → Pre-Reasoning 전달 효과.
- F-001/F-008: Batch 2에서 F-008 0/9, F-001 경미 2/9("방치"). 전용 Validator 필요성은 낮아짐(보류 유지 타당).
- 형식: LaTeX 화살표 잔재 2/9 — Presentation 후처리(Operational) 후보.

## 4. Revision #2 후보 (Evidence만, 구현 보류)
1. **Knowledge 세부 조건의 탈락** (F-006 잔여 5/9 + P0 RUN_002 5/8): 시한·화면·조건·등급 예외를 K-item 본문에 묻지 말고 구조화(예: `Key Conditions` 필드) — Prompt/Knowledge Semantic Change.
2. **F-010 하류 선택지 축소** (P0 3/8 → Batch 2 2/9): Judgment-첫 구조에서 "계산/확인 결과에 따른 분기"를 Action에 두도록 하는 지시 — 재현율 낮아 Batch 3 이후.
3. **F-004 확인 축** (4/9 경미): `must_confirm_before_action`이 1~2건으로 짧은 경향.
4. F-001 "방치" 어휘(2/9) — Usage Boundary에 "DO 미적용 사유 확인 전 방치 단정 금지"가 있는 Case에서만 관찰 → Knowledge 문구 문제일 수 있음(GC-09·17 Pack에는 그 Boundary가 없었음).

## 5. 다음 단계
Human 검토 → (a) Revision #2 여부 결정, (b) Golden P2·추가 Case(§7 Coverage Gap: 시황 활용, ELB 청약, 결정세액 부족, 세액공제 미신청 해지, 수수료 단독 이탈 등) 설계, (c) Reusable Knowledge 설계 착수 여부(§20.8).
