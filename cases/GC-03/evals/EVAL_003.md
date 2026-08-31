# EVAL_003 — GC-03

## 1. Evaluation Metadata
- Case: GC-03 / Run: **RUN_003** (`cases/GC-03/runs/RUN_003.md`, Parent RUN_002) / Eval: **EVAL_003** / Evaluated At: **2026-08-31** / Evaluator: Claude (separate context from Builder Gemma 4)
- Runtime Revision: **REV-002** (Runtime commit fe9a84a — input_v2 Evidence Pack 8-섹션·Calculated Facts·5-섹션 Employee Brief·Evidence Provenance)
- Case Baseline: cases/GC-03/case.md FROZEN (commit 59e69ba, 변경 없음) / Input: cases/GC-03/input_v2.md (REV-002 변환, 원본 §2 의미 불변) / Knowledge Pack: 59e69ba (내용 변경 없음)
- Basis: case.md §5 (유일한 정답 기준); AGENTS.md §20.6; design/EMPLOYEE_BRIEF_SPEC.md §1·§3·§4·§5; cases/FAILURE_MAP.md

## 2. Verdict
**PASS** (RUN_001: PARTIAL → RUN_002: PARTIAL → RUN_003: PASS)

Judgment(추가 확인 우선 / 정보 안내 중심)와 "55세 이전 자금 사용 계획"을 첫 질문으로 두는 구조가 Golden의 핵심 판단방향과 정확히 일치한다. EVAL_002의 잔여 3건 중 2건이 해소되었다: (1) 과세이연 환급 처리 상태 확인(K-005)이 must_confirm·Action 3·S2 [직원]·S5 화면([06-12-501]·[04-12-644])까지 일관되게 들어왔고, (2) RUN_002에서 탈락했던 "확인 결과에 따른 조건부 유형" 분기가 S3에 복원되었다 — [55세 이후 유지+운용 의사] → 성향 내 원리금보장/실적배당(TDF 등 위임형) vs [55세 이전 사용 또는 유보] → 현금성 유지 + DO 지정 안내, 즉 "당분간 현 상태 유지" 경로 포함(F-010 해소). Critical Mistake·Hard Constraint 위반 없음, "방치"류 판정어 없음, DO 미등록 상태를 "자동 운용된다"로 오안내하지 않음(화법이 "미리 **지정해두신** 방향으로 운용될 수 있도록"으로 제도 정확).
잔여(경미, verdict 비변경): 직접/위임 운용 방식 선호가 명시 확인 축이 아닌 unknowns("디폴트옵션 지정 의사 및 상품 선호도")·S3 조건("운용 의사가 있는 경우")에만 암시(F-004 잔존), 고객 고민 내용·재취업 예정 미확인, S5 출처가 K-ID 표기만으로 권위 수준(공식/행내/Hot Tip) 미병기.

## 3. REV-002 신규 관찰 축
- **(a) S1 어휘 — Unknown의 사실 승격/단정(F-001)**: 없음. "방치" 계열 미출현(deterministic 금지어 PASS). current_situation이 "(추론: … 탐색 단계로 보임)"으로 추론 표기 유지. 경미 관찰: S1 "연금 수령 전까지 약 2년"은 연금 수령 의사를 전제한 듯 읽힐 수 있으나, S4 화법이 "연금으로 받으실 계획이신지 아니면 그전에 사용하실 계획이 있으신지"를 열린 질문으로 묻어 판단 사슬로 진행되지 않음 — 어휘 수준 관찰만.
- **(b) S2 확인 축 자체 도출(F-004)**: 입력에 Missing 힌트 없이 "55세 이전 자금 사용 계획"[고객]·"퇴직소득세 환급 처리 완료 여부"[직원]을 도출 — 특히 환급 축은 RUN_001·002 연속 누락이던 것을 입력 제거(과세이연 등록 상태 필드 삭제, 입금사유 코드만 잔존) 이후에 오히려 스스로 도출. 개선. 잔여: 직접/위임 선호·고민 내용·재취업 미도출(경미 — 핵심 첫 질문은 충족).
- **(c) S3 분기 규칙·Candidate Pool·조건부 유지**: Management Decision을 실제로 바꾸는 미확인 변수(자금 사용 시점)에만 분기 2개 생성 — 불필요 분기 없음, 필요한 분기 보존(RUN_002의 탈락 복원). 두 방향 모두 조건부("…경우 →") 형식. 특정 상품명 없음("TDF 등 위임형"은 유형 어휘 — K-006 준거), Candidate Pool deterministic PASS. 경미: 55세 전 사용 예정 시 "단기 원리금보장" 선택지(case §5 Acceptable) 대신 "현금성 유지"로 수렴 — 허용 경로("당분간 현 상태 유지도 가능")이므로 위반 아님, 선택지 폭 관찰만.
- **(d) S4 화법**: 실제 화법 2건 — 사용 가능, 압박·과장 없음, "천천히 결정하셔도 좋으나"로 CRM "생각해 보겠다" 존중. DO 의무 안내가 제도안내 톤(권유 아님). 용어 치환 적절("고유계정대" Brief 미출현, "현금성자산" 사용).
- **(e) S5 재료 실존·출처**: 2건 모두 Knowledge Pack 실존 — 환급 전 지급·연금설계 제한+화면(K-005 원문 일치), DO 스타뱅킹 지정 경로(K-002 원문 일치). 없는 팁 생성 없음. 출처 표기는 있으나 K-ID만이며 권위 수준·as-of 미병기(경미).
- **(f) supporting_evidence_ids 논리 정합**: PASS — Judgment(E011 현금 100%·E012 DO 미등록·E017 CRM·E018 7일 경과·E020 개시 미충족)가 "확인 우선+제도안내" 판단을 실제로 정당화. Action 1(E004·E020)·2(E012)·3(E014)도 정합. Deterministic Provenance PASS와 일치.
- **(g) DO "적용 예상 기준일 경과" 비약**: 해당 없음(GC-03은 DO **미등록** — Calculated Fact에 해당 R값 없음). 관련 경계는 준수: 미등록인데 "2주 후 자동 운용" 오안내 없음(Critical Mistake Check 항목, 미발생).
- **(h) CRM 메모 Ground Truth 과신**: 없음 — E017을 "개설 시 밝힌 바 있음"으로 시점 한정 인용하고, 그 위에서 확정하지 않고 확인 우선 판단으로 연결. 고민 내용 재탐색 질문이 없는 점만 경미 잔여.
- **(i) F-005 재발(유지/확인이 정답인 지점의 개입 생성)**: 없음 — 상품 확정·리밸런싱 개입 미생성, 확인·정보안내·절차 3 Action 구성, S3에 유보/유지 경로 존재.

## 4. 섹션별 평가 (SPEC §4)
| 섹션 | 판정 | 근거 |
|---|---|---|
| S1 | PASS | 핵심 사실 선택 적절(1.8억·7일·현금 100%·CRM·53세), 어휘 절제, 추론 구분 유지 |
| S2 | PASS(경미) | 포인트 1개+우선순위 명확, [고객]/[직원] 태그 사용, Evidence Trace 정합. 잔여: 직접/위임·고민 내용 축 |
| S3 | PASS | 분기 보존·조건부·유지 경로·Pool 준수. C1 재진술 "위험중립형 범위 내" 정확(RUN_001 축소 재발 없음) |
| S4 | PASS | 순서 논리(확인→계획→운용 논의→DO 안내), 화법 2건 사용 가능·비압박 |
| S5 | PASS(경미) | 실존 재료+화면 2건 생존, 출처 권위 수준 미병기 |

## 5. Failure Pattern Observation
| Pattern | RUN_002 | RUN_003 |
|---|---|---|
| F-001 Uncertainty Loss | 없음 | 없음 ("약 2년" 어휘 관찰만) |
| F-002 Knowledge Over-application | 없음 | 없음 |
| F-004 Confirmation Axis Gap | 잔존 — 직접/위임·고민 내용 | 경미 잔존 — 직접/위임(암시로만)·고민 내용·재취업; 환급 축은 해소 |
| F-005 Action/Change Bias | 없음(분기 탈락 관찰) | 없음 |
| F-006 Knowledge Under-use | K-005 미사용 | 해소 — K-005 사용(§5 knowledge_ids_used·S5) |
| F-007 Employee Next Action | 개선(DO 등록 경로) | 유지+개선 — 환급 확인 화면 [06-12-501]·[04-12-644] 추가 |
| F-008 Structured→Brief Drift | 해소 | 재발 없음 |
| F-010 Downstream Option Narrowing | 발생(조건부 분기 탈락) | **해소** — S3 조건부 2분기+유지 경로 복원 |

## 6. N/A 처리 축 (변환 규칙 — 추가 결정 2)
- input_v2 제외 필드: 최근 운용지시일(없음), 이연퇴직소득세 금액·과세이연 등록 상태 필드, "연금개시 요건 미충족" 파생 라인(R1 E020 대체).
- `N/A — Input removed by approved REV-002 schema`: **"과세이연 정보 등록됨" 필드·이연퇴직소득세 액수에 직접 근거한 관찰 축**(등록 상태 자체의 인용·세액 수치 취급 여부). PASS로 세지 않음.
- 비고: 환급 처리 확인 축 자체는 입금사유 코드("과세이연/계약이전입금", E014 유지)로 성립하므로 N/A가 아니며 정상 평가함(§3-b — 충족). "연금개시 미충족" 축은 E020으로 대체 성립 — 정상 평가(충족). GC-03의 핵심 Semantic Boundary는 입력 삭제 후에도 온전히 성립.

## 7. RUN_002 대비 변화
- **개선**: ① 환급 처리 상태 확인 축 신규 도출(EVAL_002 잔여 1 해소 — must_confirm·Action·S5 화면까지 일관), ② S3 조건부 유형 분기+현 상태 유지 경로 복원(EVAL_002 잔여 3·F-010 해소), ③ S4 화법 신설(사용 가능·비압박), ④ S5 신설 — 실존 재료·화면번호 생존.
- **유지**: 확인 우선 Judgment, C1 정확 재진술, "방치" 미출현, CRM 시점 한정 취급.
- **악화**: 없음.
- Verdict 이동: PARTIAL → **PASS**.

## 8. Critical Mistake Check
없음 — "방치·미운용" 단정 없음 / 연금개시 가능 오안내 없음(53세 불가 정확) / DO 미등록 자동 운용 오안내 없음 / C1·C3 위반 없음 / 사용계획 확인 전 상품 확정·특정 상품명 없음 / 세액 계산·수치 생성 없음.

## 9. Constraint Check
C1 PASS · C2 PASS · C3 PASS (Runtime deterministic validation). 금지어·LaTeX·Evidence Provenance·Candidate Pool PASS. **화면번호 생존 REVIEW 2건([01-12-213]·[04-12-648]) — Evaluator 해소**: 해당 화면은 과세이연 환급 신청·정보수정 절차 세부용으로 case §6 Out of Scope(과세이연 절차 세부)이며, 이 Case에 필요한 화면([06-12-501] 환급 상태·[04-12-644] 거래내역)은 S5에 생존. 판정 영향 없음.

## 10. Employee Brief (Diagnostic — 의미 보존)
Unknown→Fact 변환 없음 / 조건부→무조건 변환 없음(S3 전 방향 조건부) / Hard Constraint 소실 없음 / Judgment 왜곡 없음 / 고객 의사 왜곡 없음. 세부는 §3 (a)(h).

## 11. Evidence
RUN_003 §3 (situation·unknowns), §6 (judgment·reasoning·must_confirm·supporting_evidence_ids), §7 (Actions), §8 (deterministic validation), §9 (S1~S5 brief); knowledge_pack.md K-001~K-008 대조; EVAL_002 대조.

> 이 Artifact는 생성 후 수정하지 않는다.
