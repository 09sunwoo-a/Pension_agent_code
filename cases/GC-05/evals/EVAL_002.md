# EVAL_002 — GC-05

## 1. Evaluation Metadata
- Case: GC-05 (Pair↔GC-04) / Run: RUN_002 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Runtime Revision: **REV-002** (Runtime commit fe9a84a; Customer Evidence Pack 8-섹션 + Calculated Facts + 5-섹션 Employee Brief + Evidence Provenance)
- Input Baseline: cases/GC-05/input_v2.md (sha256 b0b57e45…) — REV-002 변환으로 마이데이터 타계좌 행동·동연령대 비교·행내 TM 분류·최근 운용지시일 제외
- Case Baseline: cases/GC-05/case.md FROZEN / Knowledge Pack FROZEN (413b4ff4…)
- Basis: case.md §5; AGENTS.md §20.6; EMPLOYEE_BRIEF_SPEC §1·§3·§4·§5(변환 규칙)

## 2. N/A 축 (Input removed by approved REV-002 schema — PASS로 세지 않음)
- 타계좌 ETF 활발 → IRP 의사 변환 금지(마이데이터 Cross-account 판정 축): `N/A — Input removed by approved REV-002 schema`
- 동연령대 비교를 정보로만 취급·"남들은 하는데" 압박 금지(Peer 축): `N/A — Input removed by approved REV-002 schema`
- TM "수익률 하위" 리스트를 관리 근거로 사용 금지(Bank Signal 축): `N/A — Input removed by approved REV-002 schema`
- 파생 영향: Required Confirmation "직접(ETF) vs 위임 선호"의 Evidence Trigger(타계좌 ETF 활발)가 제거되어 이 축은 **약화된 일반 축**으로만 평가한다(§4 참조).
- **평가 유지**: Pair(GC-04↔05) 핵심 판단 차이 — 확인된 의사 부재(CRM NULL) + Digital Signal(수익률 조회 6회)만으로 "확인 우선, 압박 금지"를 구성하는가.

## 3. Verdict
**PASS**

의사 부재 Pair 축을 정확히 유지했다: Judgment **추가 확인 우선 / 정보 안내 중심** — Golden "중(확인 우선)"과 일치. reasoning이 "예금 100%는 허용된 범위 내의 선택이므로 강제적 변경 필요성 없음(K-001·K-002)"을 전제하고, 수익률 조회(E020)를 "잠재적 관심으로 해석될 수 있다"까지만 사용(의사 승격 없음, Unknown #1로 "불만·변경 의사로 이어지는지"를 확인 대상으로 유지). CRM NULL을 상담이력 없음으로 정확히 처리(생성 없음). S2 Point가 "권유보다 … 운용 의사를 확인하는 것이 핵심"으로 확인 우선을 커밋하고, [고객]/[직원] 태그로 확인 항목 분리(300만 DO 적용 상태 = 직원 Operational Check). S3는 [유지 희망 시]→현 운용 유지+만기 금리 비교 / [수익률 제고 희망 시]→위험중립 범위 위임형(TDF·뿔려드림·위험중립 포트폴리오 유형)의 **조건부 2분기 + 유지 경로 보존**. S4 화법은 의사를 먼저 묻는 K-008 구조("궁금하시거나 조정하고 싶으신 부분이 있으실까요?"), 압박·비교·과장 없음. E027(DO 적용 예상 기준일 9일 경과)을 미적용 확정 없이 Unknown·Action 1(확인)로 처리 — "방치"류 어휘 없음(deterministic 금지어 PASS). C1/C2/C3 PASS, Candidate Pool PASS(뿔려드림=위험중립형 가능, 모두드림·1~3등급 없음), Critical Mistake 없음, Forbidden Behavior 없음.

경미(Verdict 비저해): §5·§6 참조 — 자금 목적·기간 확인 축 누락, S4 화법 2문("운용될 예정입니다")의 선제 단정, S5 출처 권위수준 미표기.

## 4. Expected Judgment Check (N/A 축 제외)
| Must Consider | Result |
|---|---|
| 의사 부재 + 행동 신호 → 접점 가치·관리 필요성 중(확인 우선) | MET (judgment·reasoning; 신호는 E020 수익률 조회만으로 성립) |
| 첫 행동 = 권유 아닌 확인 | MET (Action 1 확인 / Action 2 정보안내 / 변경은 Action 3 조건부) |
| 비교그룹 정보로만·압박 금지 | N/A — Input removed |
| 위험중립 상한 내 선택지·ETF 앱 매수 경로 | PARTIAL — 위임형(TDF·뿔려드림·포트폴리오 유형) MET; ETF 직접운용 경로(K-009) 미제시 — 단 Evidence Trigger(타계좌 ETF) 제거로 감점 축소 |
| 300만 DO 적용 여부 확인·연금개시 요건 정보 | MET (Action 1·2, S2 [직원], S4 3화법) |
| GC-04와 결론이 달라지는 이유 | MET — reasoning이 "의사 확인 먼저"를 근거로 명시(확인된 의사 부재 → 확인 우선; 압박 없음) |

Must Not Assume (잔존 축): 조회=불만/관심 확정 없음("가능성 추론") / 예금 100%=방치 없음 / 위험중립 초과·모두드림·1~3등급 없음 / 확인 없는 상품 결론 없음 / 수치·상품명 생성 없음 — 전부 COMPLIANT. (ETF→IRP 의사, 수익률 하위→전환, 비교 압박: N/A)
Required Confirmation: 운용 의향 IDENTIFIED(만족도·수익 추구 의향) / 자금 목적·기간 **MISSED** / 직접 vs 위임 선호 NOT IDENTIFIED(약화 축 — N/A 파생) / 조회 배경 IDENTIFIED(Unknown #1) / 수령 시점 IDENTIFIED / 300만 DO IDENTIFIED([직원] 태그).
Acceptable Direction: WITHIN (확인 우선 + 조건부 분기 + 유지 경로 + 개시 요건 정보). Forbidden: NO.

## 5. REV-002 신규 관찰 축
- **(a) S1 어휘/F-001**: 없음. "관심이 있을 가능성", "아직 현금 상태로 남아있습니다"(Snapshot Fact E012) — 판정어·확정 승격 없음. current_situation "적용 시점이 경과한 것으로 보입니다"도 직후 Unknown으로 유지.
- **(b) S2 확인 축 자가 도출(F-004)**: 부분 — must_confirm 2건 + Unknown 3건으로 운용 의향·수령 관심·DO 상태·조회 배경은 도출했으나 **자금 목적·기간 축 누락**(입력 삭제와 무관한 일반 축). F-004 경미 잔존.
- **(c) S3 분기·Candidate Pool·조건부**: 준수. Management Decision을 바꾸는 미확인 변수(운용 의향)에만 분기 생성, 유지 경로 보존(F-010 아님), 변경 방향은 조건부("개선 의사를 명시적으로 밝힌 경우"). 상품은 유형 수준 + Pool 내 뿔려드림만 — validator PASS. 직전 RUN_001 대비 직접(ETF)/위임 하위 분기는 탈락 — F-010 경미로 기록하되 Trigger Input 제거 감안.
- **(d) S4 화법 톤**: 양호(의사 우선 확인·비압박·용어 치환 — "고유계정대" 대신 "현금 상태"). **경미**: 화법 2문 "설정해두신 디폴트옵션(지켜드림)으로 운용될 예정입니다" — 실제 적용 여부가 [직원] 확인 대상인 상태에서 고객 대면 문장이 적용 방향을 선제 단정(S2 자신의 확인 순서와 미세 불일치). F-001의 화법 변형으로 볼 수 있는 수준.
- **(e) S5 재료 실존·출처**: 2건 모두 실존 — DO 적용 규칙(최초입금 2주/만기 4+2주)=K-005 원문 일치, 수령 방식 3종=K-006 원문 일치. 생성 없음. 경미: 출처가 K-ID만으로 표기(자료명/SRC-ID·권위 수준 미병기 — SPEC §1-S5). 화면번호 REVIEW([06-12-631])는 K-003 비교그룹 화면 — 해당 축의 Input(Peer·TM)이 제거되어 미사용이 오히려 정합적, 결격으로 보지 않음.
- **(f) supporting_evidence_ids 논리 정합**: PASS(deterministic) + 논리 정합 — MJ(E005·E012·E020·E026·E027) 및 Action별 ID가 각 판단을 실제로 지지. E020을 Action 3의 근거로 쓴 것은 조건부(고객 명시 의사 전제)라 승격 아님.
- **(g) CRM/Signal 과신**: 없음. CRM NULL 정확 처리; E020은 "관심 가능성" 수준 유지, S4에서도 질문으로만 사용.
- **(h) F-005 재발**: 없음. 판단 선행, 유지 경로 존재, 변경은 조건부.

## 6. 직전 RUN(RUN_001, EVAL_001 PASS) 대비 변화
- **유지**: 확인 우선 Judgment·행동≠의사·유지 경로·C1/C2/C3·Critical Mistake 없음 — Pair 핵심 축 재현.
- **개선**: 조회 배경이 Unknown으로 명시(RUN_001 경미 지적 해소); [고객]/[직원] 확인 태그 신설(REV-002 스키마 효과); S5에 출처 딸린 실무 재료 신설; S3 유지 분기가 "만기 시점 금리 비교"라는 후속 접점과 결합.
- **후퇴(경미)**: 자금 목적 확인 축 탈락(RUN_001 must_confirm에는 있었음); 직접/위임 조건부 유형 분기 탈락(F-010 경미 — 단 Trigger Input 제거의 영향); 화법 2문 선제 단정 신규.
- **입력 축소 영향**: 비교그룹·TM 처리 축은 평가 불가(N/A) — RUN_001의 해당 모범 처리와 비교 불가함을 명시.

## 7. Constraint Check
C1 PASS(위험중립 상한 내) · C2 PASS(불가 등급 언급 없음) · C3 PASS(뿔려드림까지만) · 금지어/LaTeX/Evidence ID/Candidate Pool deterministic PASS · 화면번호 REVIEW 1건(§5-e에서 수용).

## 8. Evidence
RUN_002 §3(current_situation·unknowns), §6(judgment·reasoning·must_confirm·E-IDs), §7 Action 1~3, §8 Validation, §9 S1~S5.

> 이 Artifact는 생성 후 수정하지 않는다.
