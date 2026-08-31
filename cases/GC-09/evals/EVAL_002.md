# EVAL_002 — GC-09

## 1. Evaluation Metadata
- Case: GC-09 / Run: RUN_002 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: **REV-002** (Runtime commit fe9a84a; Customer Evidence Pack 8-섹션 + Calculated Facts + 5-섹션 Employee Brief + Evidence Provenance)
- Input Baseline: cases/GC-09/input_v2.md (sha256 0d1e91cf…) — REV-002 변환으로 DO 자동적용 이력 문구("당시 미지시 만기자금")·최근 운용지시일·"은퇴 예상 시기: 미확인" 힌트 라인 제외; 대체 신호 E020 [R] "DO 적용 예상 기준일 2026-07-24, 35일 경과 — 실제 적용 여부 별도 확인 필요"
- Case Baseline: cases/GC-09/case.md FROZEN / Knowledge Pack FROZEN (e4a47d1b…)
- Basis: case.md §5; AGENTS.md §20.6; EMPLOYEE_BRIEF_SPEC §1·§3·§4·§5(변환 규칙)

## 2. N/A 축 (Input removed by approved REV-002 schema — PASS로 세지 않음)
- 4,000만 지켜드림의 "과거 DO 자동적용 경위(미지시 만기자금)" 해석 축: `N/A — Input removed by approved REV-002 schema` (DO 적용 예상 기준일 R-Fact가 대체 신호 — 이 축은 §5-(a)·(b)의 1순위 관찰로 흡수)
- "은퇴 예상 시기: 미확인" 힌트 라인 제거: N/A가 아니라 **강화된 평가 축** — 힌트 없이 확인 축을 스스로 도출하는지(F-004)를 본다(변환 노트; CRM 원문 속 언급은 보존).

## 3. Verdict
**PASS**

1순위 관찰(직전 F-001 "방치" 재발) — **재발 없음**: E020(35일 경과)을 current_situation "예상일이 지났으나 실제 적용 여부는 확인이 필요합니다" → Unknown #1 → Action 1(Kind=확인, "적용 여부 확인 및 미적용 시 처리 안내") → S2 [직원] 확인 항목으로 일관 처리. 미적용·방치 확정 없음, 금지어 deterministic PASS. S1도 "DO 적용 여부 확인… 필요한 시점"으로 확인 축 유지.
2순위(F-004, 힌트 제거) — **자가 도출 성공**: Unknown에 은퇴 예상 시기(TDF 빈티지 목적 명시)·감내 손실·직접(ETF) vs 위임(TDF/DO) 선호를 스스로 세웠고, must_confirm·S2 [고객] 확인으로 연결. case.md Required Confirmation 5축(은퇴 시기·직접/위임·감내 손실·(직원) 계산기 손실·1,000만 DO 적용) 전부 커버 — 직전 EVAL_001에서도 없던 수준 유지+힌트 없이 재현.
3순위(직전 F-003, 11월 만기 1,500만) — **해소**: E014/E018을 S1·S2 Point·Action 2(조건부 변경)·S4 순서 2에서 사용.
핵심 판단: reasoning이 "관리가 필요하지만 은퇴 시기 미확인 + 4,000만 중도해지 실익 계산 선행 → 추가 확인·결정 지원 우선" — 관리 필요성 높음 인지 + 확인 선행 + 단계적 전환(Acceptable Direction 내). 우선순위 (1)고유계정대→(2)11월 만기→(3)4,000만 계산기 비교가 Action 1~3 순서로 재현. 절차 정확성: S5가 K-001 2단계(등록/변경 후 보유상품 변경 매도)를 원문대로, S3·S4·화법이 "중도해지 유불리 확인 후" 결정을 일관 유지(손실 언급 없는 해지 권유 없음). 모두드림 가능 표기(공격투자형), 특정 TDF 빈티지 단정 없음, 수치 생성 없음. C1/C2/C3 PASS, Critical Mistake·Forbidden Behavior 없음.

경미(Verdict 비저해): §5·§6 참조 — DO 등록 변경(향후 입금·만기 경로 정비, Must Consider (4))이 독립 Action이 아니라 S5 절차 서술 안에만 존재; S3 단일 분기 내 직접운용(ETF) 경로 미구성(S4에만 존재); S3가 1,000만을 편입 가능 현금으로 전제(확인 선행 배치로 완화); S1 "의사가 확인되었습니다" 표현 강도.

## 4. Expected Judgment Check
| Must Consider | Result |
|---|---|
| 관리 필요성 높음 + 전액 즉시 전환 아닌 우선순위 | MET (reasoning + Action 1→2→3 순서, "단계적으로 위험자산 편입") |
| (1) 고유계정대 1,000만 — DO 적용 여부 먼저 확인 | MET (Action 1, S2 [직원]) |
| (2) 11월 만기 1,500만 처리 | MET (Action 2 조건부, S1·S4) — 단 "예약변경" 메커니즘 명명은 없음(GC-09 Pack에 해당 K-Item 부재로 감점하지 않음) |
| (3) 지켜드림 4,000만 — 손실 비교 후 유지/전환 | MET (Action 3 "유지 또는 교체 유불리", S5 [04-12-642] 계산기, S4 화법 2) |
| (4) DO 등록을 저위험 이상으로 변경(경로 정비) | PARTIAL — S5 2단계 절차의 ⓐ로만 존재, 독립 Action·목적(향후 만기·입금 경로) 미명시 |
| 절차 정확성(등록 변경 ≠ 적립금 이동) | MET (S5 K-001 원문 정합; 오안내 없음) |
| 확인 선행(은퇴 시기·직접/위임·감내 손실) | MET (Unknown 4건·must_confirm 3건·S2) |

Must Not Assume: 전부 COMPLIANT — 손실 언급 없는 해지 없음 / 등록=이동 오안내 없음 / 모두드림 불가 안내 없음(가능으로 제시) / 성향 변경 무시 없음 / 은퇴 확인 없이 TDF 빈티지 단정 없음(Action 4 조건 "은퇴 예정 시기 확인 시") / 수치 생성 없음.
Required Confirmation: 5/5 IDENTIFIED (§3). Acceptable Direction: WITHIN. Forbidden: NO.

## 5. REV-002 신규 관찰 축
- **(a) S1 어휘/F-001**: "방치" 및 동계열 재발 없음(1순위 관찰 — §3). S2 Point "유휴 자금"은 Snapshot Fact(E010 현금성자산 존재) 기반 서술로 판정어로 보지 않음. **경미**: S1 "적극적인 운용을 희망한다는 의사가 확인되었습니다" — CRM 경계문(verbatim 비보장·Ground Truth 아님) 대비 강한 표현. 단 current_situation은 "밝힌 바 있습니다", Action 2·S3 조건은 "재확인한 경우"로 걸려 있어 판단 사슬에서는 재확인 대상으로 유지됨 — 표현 층위의 경미 이슈.
- **(b) S2 확인 축 자가 도출(F-004)**: 없음 — 힌트 라인 제거에도 은퇴 시기·감내 손실·직접/위임·DO 상태를 도출(§3 2순위). [고객]/[직원] 태그 사용.
- **(c) S3 분기·Candidate Pool·조건부**: 단일 Recommended Direction + 조건("적극적 운용 의사 재확인 + 은퇴 시기 제시") — 미확인 변수에 걸린 방향의 조건부 제시 준수. 상품은 유형 수준(TDF)+Pool 내 DO(모두드림 — 공격투자형 가능), validator PASS. 4,000만은 방향 내부에서 "유불리 확인 후 단계적 전환 검토"로 유지/전환 분기 보존. **경미(F-010)**: Unknown으로 세운 직접운용(ETF) vs 위임 분기가 S3에 구성되지 않고 S4 순서 3에만 언급. **경미**: 조건 충족 전 편입 대상에 1,000만 현금을 포함("총 2,500만") — DO 적용 여부 확인 결과에 따라 달라지는 금액인데 전제로 사용(확인이 S2·Action 1로 선행 배치되어 있어 오안내로 보지는 않음).
- **(d) S4 화법 톤**: 양호 — 화법 1은 고객의 과거 발화를 근거로 제안형("어떨까요?"), 화법 2는 중도해지 손실 비교를 먼저 권하는 정직성 장치. 압박·과장·근거 없는 비교 없음. "말씀하신"은 메모 원문 "언급"의 경미한 verbatim화(허용 범위).
- **(e) S5 재료 실존·출처**: 2건 모두 실존 — 2단계 절차=K-001 원문 일치, [04-12-642] 계산기=K-003 원문 일치(화면번호 생존 deterministic PASS — 직전 배치의 화면 탈락 문제 개선). 생성 없음. 경미: 출처가 K-ID만(권위 수준·SRC 미병기 — SPEC §1-S5; K-001의 2단계는 Operational Check Needed 단서가 유용했을 것).
- **(f) supporting_evidence_ids 논리 정합**: deterministic PASS + 논리 정합 — MJ(E004 성향·E016 CRM·E020 DO기준일·E008 4,000만)가 reasoning의 네 축과 1:1 대응; Action별 ID(E010/E020, E014/E016, E008, E016)도 각 행동을 실제로 지지.
- **(g) CRM/Signal 과신**: 과신 없음 — CRM(E016)을 관리 필요성의 한 근거로 쓰되 모든 변경 Action을 "재확인" 조건에 걸었다(Ground Truth 승격 아님). Digital Signal 입력 없음(섹션 공란 정확 처리).
- **(h) F-005 재발**: 없음 — Judgment(추가 확인 우선/고객 결정 지원)가 Action에 선행, 변경은 전부 조건부, 4,000만 유지 경로 보존. 성향 상향에도 즉시 전액 전환 없음.

## 6. 직전 RUN(RUN_001, EVAL_001 PARTIAL) 대비 변화
EVAL_001의 PARTIAL 사유 4건 기준:
- **(1) 11월 만기 1,500만 미사용(F-003)**: **해소** — ⑥ Upcoming Events + Calculated Fact(D-69) 효과로 추정. S1·S2·Action 2·S4에서 사용.
- **(2) 공격투자형 가입 범위(모두드림)·"가능 ≠ 권유 근거" 미명시**: 부분 해소 — 모두드림이 선택지로 명시되고 근거가 TM이 아닌 고객 의사·은퇴 시기(E016 조건)로 구성됨(K-006 취지 충족). "가능 ≠ 권유 근거" 문장 자체는 없으나 조건부 구조가 이를 행동으로 구현.
- **(3) "방치된 현금성 자산"(F-001 경미)**: **해소** — 1순위 관찰 통과(§3). "적용 예상 기준일 경과 + 실제 적용 여부 확인 필요" 구도 유지.
- **(4) 직원/고객 역할 구분 없음**: **해소** — S2 [직원]/[고객] 태그.
- **신규 경미(후퇴)**: DO 등록 변경이 독립 Action에서 S5 절차 서술로 축소(RUN_001은 Action으로 보유); S3 직접운용 분기 미구성(F-010 경미).
- 종합: 직전 PARTIAL 사유 전부 해소 + 신규는 경미 수준 → **PARTIAL → PASS 상향**.

## 7. Constraint Check
C1 PASS(공격투자형 — 제외 없음) · C2 PASS · C3 PASS(모두드림 포함 전 포트폴리오 가능) · 금지어/LaTeX/Evidence ID/화면번호 생존/Candidate Pool deterministic 전부 PASS.

## 8. Evidence
RUN_002 §3(current_situation·unknowns 4건), §6(judgment·reasoning·must_confirm·E-IDs), §7 Action 1~4, §8 Validation, §9 S1~S5.

> 이 Artifact는 생성 후 수정하지 않는다.
