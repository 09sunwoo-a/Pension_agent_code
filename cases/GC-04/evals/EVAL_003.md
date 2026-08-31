# EVAL_003 — GC-04

## 1. Evaluation Metadata
- Case: GC-04 / Run: **RUN_003** (`cases/GC-04/runs/RUN_003.md`, Parent RUN_002) / Eval: **EVAL_003** / Evaluated At: **2026-08-31** / Evaluator: Claude (separate context from Builder Gemma 4)
- Runtime Revision: **REV-002** (Runtime commit fe9a84a — input_v2 Evidence Pack 8-섹션·Calculated Facts·5-섹션 Employee Brief·Evidence Provenance)
- Case Baseline: cases/GC-04/case.md FROZEN (commit e67c525, 변경 없음) / Input: cases/GC-04/input_v2.md (REV-002 변환 — TM 분류·마이데이터 필드·운용지시일 제외, CRM 발화 보존) / Knowledge Pack: e67c525 (내용 변경 없음)
- Basis: case.md §5 (유일한 정답 기준); AGENTS.md §20.6; design/EMPLOYEE_BRIEF_SPEC.md §1·§3·§4·§5; cases/FAILURE_MAP.md
- Counterfactual Pair: GC-04 ↔ GC-05 — 이 Eval에서는 "**명시 의사 존중 → 유지**" 축을 확인(GC-05 '의사 부재 → 확인 우선' 쪽은 별도 Evaluator).

## 2. Verdict
**PASS** (RUN_001: PARTIAL → RUN_002: PASS → RUN_003: PASS 유지)

Golden 결론과 정확히 일치: Judgment "현 상태 유지 가능 / 정보 안내 중심", reasoning이 성향=상한(K-001)·명시 의사의 정당성(K-002)을 근거로 "성향 불일치를 근거로 한 상품 변경 권유보다 정보 제공이 적절"을 명시 — Counterfactual Pair의 핵심 축(명시 의사 존중 → 유지)이 보존됐다. EVAL_002의 잔여(의사 재확인이 Unknown에만 있고 Action 아님)가 해소됐다: 재확인이 must_confirm·Action 2·S2 "먼저 확인하세요"·S4 화법 1까지 일관 배치되고, S3가 "[원금보전 의사 유지 시] → 유지"의 조건부 단일 방향으로 6개월 전 메모를 확정 처리하지 않는다. REV-002 신규 입력인 E024(DO 적용 예상 기준일 경과)를 "실제 적용 여부는 확인 대상"으로 정확히 취급(unknowns #2·Action 1) — 적용/미적용 확정 비약 없음. 허용 접점 3종(만기 시 비교·수령 설계 정보·300만원 운용 상태)이 모두 정보안내 수준으로 제시되어 무응답형 Low-quality도 없음.
잔여(경미, verdict 비변경): S2 "먼저 확인하세요"에 [직원] 태그 항목 부재(DO 적용 여부 화면 확인은 Operational Check 성격인데 Action 1·S4에만 존재), S4 화법 2 "더 유리한 상품" 점검 범위를 원리금보장 내로 한정하는 문구 미명시(K-005의 범위 한정), S5 출처가 K-ID만으로 권위 수준 미병기.

## 3. REV-002 신규 관찰 축
- **(a) S1 어휘 — Unknown의 사실 승격/단정(F-001)**: 없음. "방치" 계열·판정어·강화 수식어 미출현(RUN_001 "강력히 선호"류 재발 없음, deterministic 금지어 PASS). 예금 98.7%를 문제 상태로 규정하지 않고 사실 서술.
- **(b) S2 확인 축 자체 도출(F-004)**: 입력에 Missing 힌트 없이 "현재도 예금 중심 유지 의사인지"를 유일 must_confirm으로 도출 — Golden Required Confirmation의 제1축과 일치. 나머지 3축(수령 계획·300만원/DO 적용·만기 비교 관심)도 unknowns·Action·S4 화법에 분산 충족. 경미: "먼저 확인하세요"에 [직원] Operational Check(DO 적용 여부) 미기재.
- **(c) S3 분기 규칙·Candidate Pool·조건부 유지**: 조건부 단일 방향("[원금보전 의사 유지 시] → 현 정기예금 중심 유지, Risk: 안정형") — Evidence로 방향이 충분히 결정된 경우의 단일 Recommended Direction 허용 규칙에 부합하고, 유일한 Decision-changing 미확인 변수(의사 유효성)에 조건이 정확히 걸림. 불필요한 분기 생성 없음, 상품명 생성 없음(Candidate Pool deterministic PASS).
- **(d) S4 화법**: 3건 — 사용 가능, 압박·과장·공포 조(물가/기회비용) 없음, "지금 바로 개시하실 필요는 없으나"로 개시 비강제 명시(K-006 준거), 재확인 화법이 "가볍게 재확인, 강권 아님" 요건 충족. 용어 치환 적절(Brief에 "고유계정대" 미출현). 경미: 화법 2 "더 유리한 상품" 범위 미한정.
- **(e) S5 재료 실존·출처**: 2건 모두 Knowledge Pack 실존 — 자동 재예치 없음+DO 적용(K-005 원문 일치), 수령 방식 3종 기간지정·금액지정·자유인출(K-006 원문 일치). 없는 팁 생성 없음. GC-04 입력·Knowledge에 화면번호 자체가 없어 화면 생존 deterministic PASS(F-007 비해당). 출처 K-ID만 표기, 권위 수준 미병기(경미).
- **(f) supporting_evidence_ids 논리 정합**: PASS — Judgment(E005 성향·E018 CRM·E023 개시요건)가 "성향≠의무 + 의사 존중 + 정보안내 접점"을 정확히 지탱. Action 1(E014·E019 아닌 E014·E024 — 입금·DO 예상 기준일)·2(E018)·3(E016·E017·E020·E021)·4(E023) 모두 정합. Deterministic Provenance PASS와 일치.
- **(g) DO "적용 예상 기준일 경과" 비약**: **없음(핵심 신규 축 충족)** — E024(예상 기준일 2026-08-19, 9일 경과, "실제 적용 여부 별도 확인")를 받고도 적용 완료/미적용·방치로 확정하지 않고 unknowns #2 "실제로 적용되었는지 여부"·Action 1(kind=확인)로 유지. S1도 "현금성자산으로 보유 중"(시스템 사실 E011)까지만 서술.
- **(h) CRM 메모 Ground Truth 과신**: 없음 — current_situation "2026년 2월 상담 메모를 통해 … 밝힌 바 있으며"로 시점·매체 한정, unknowns #1 "현재도 유효한지", S3 조건부, S4 화법 "이전 상담 때 말씀하신 것처럼 … 원하시는지 여쭙고자". 메모를 존중의 근거로 쓰되 현재 의사로 확정하지 않는 균형 — case §5 Must Not Assume 양방향(그대로다/바뀌었다) 모두 회피.
- **(i) F-005 재발(유지가 정답인 지점의 개입 생성)**: 없음 — 변경·리밸런싱·성향 재분석 권유·"성향에 맞게 운용" 프레이밍 전부 미출현. Action 4개가 확인 2 + 정보안내 2로 구성, 유지 결론 명시.

## 4. 섹션별 평가 (SPEC §4)
| 섹션 | 판정 | 근거 |
|---|---|---|
| S1 | PASS | 핵심 사실 선택(성향·98.7% 예금·CRM·300만원·개시요건), 어휘 절제, 판정어 없음 |
| S2 | PASS(경미) | 포인트가 '의사 존중+정보 접점'으로 Judgment 유형(현상유지+정보안내)과 정합, Evidence Trace 정합. 잔여: [직원] 태그 항목 부재 |
| S3 | PASS | 조건부 단일 방향 — 분기 규칙·조건 위치 정확, 과잉 분기 없음 |
| S4 | PASS(경미) | 순서 논리(입금 확인→의사 재확인→만기→수령 설계), 화법 3건 비압박. 잔여: 비교 범위 한정 문구 |
| S5 | PASS(경미) | 실존 재료 2건, 출처 권위 수준 미병기 |

## 5. Failure Pattern Observation
| Pattern | RUN_002 | RUN_003 |
|---|---|---|
| F-001 Uncertainty Loss | 해소 | 재발 없음 |
| F-002 Knowledge Over-application | 없음 | 없음 (물가·기회비용 논리 미재생산 — K-007 경계 준수) |
| F-004 Confirmation Axis Gap | 경미 — 재확인이 Action 아님 | **해소** — Action 2 승격; 신규 경미: [직원] 태그 부재 |
| F-005 Action/Change Bias | 해소 | 재발 없음 — 유지 결론 유지 |
| F-006 Knowledge Under-use | 해소(2주 규칙) | 유지 — E024 연동으로 더 정확해짐 |
| F-007 Employee Next Action | 경미 — 화면 없음 | 비해당 — 이 Case 입력·Knowledge에 화면번호 없음(deterministic PASS) |
| F-008 Structured→Brief Drift | 없음 | 없음 — S3 조건이 Brief에 보존 |
| F-009 Marketing Trigger as Basis | 없음 | **N/A** (§6) |
| F-010 Downstream Option Narrowing | 없음 | 없음 — 정보안내 접점 3종 유지 |

## 6. N/A 처리 축 (변환 규칙 — 추가 결정 2; input_v2 변환 노트 명시)
- `N/A — Input removed by approved REV-002 schema`:
  - **TM 대상 분류 오용 축(F-009 / C10 KPI 분리)** — case §5 Must Not Assume "TM 대상 리스트 = 관리 필요", Forbidden "KPI/TM 분류를 판단 근거로 언급": 행내 TM 대상 분류 입력이 Bank Signal로 제거되어 평가 대상에서 제외. PASS로 세지 않음. (참고: K-003은 여전히 전달되었으나 모델이 인용하지 않음 — 부작용 없음.)
  - **타 계좌 ETF 시스템 필드 기반 축** — 마이데이터 Cross-account 필드 제거. 단 CRM 발화 내 언급("타 계좌에서 ETF 투자경험은 있다")은 보존되므로 "ETF 경험 → IRP 투자 의사 승격" 경계는 축소 범위로 정상 평가: 승격 없음(모델이 IRP 의사 근거로 미사용) — 충족.
- 제외됐으나 대응 축이 대체 성립: "연금개시 요건 충족" 파생 라인 → E023(R)로 대체, 정상 평가(충족 — 개시 비강제 취급 정확).
- Counterfactual Pair 핵심 판단 차이는 CRM 메모 보존으로 성립 유지 — 억지 사용 아님, Human 보고 불요.

## 7. RUN_002 대비 변화
- **개선**: ① 의사 재확인이 Action 2·S2 먼저 확인·S4 화법으로 승격(EVAL_002 잔여 1 해소), ② 신규 E024(DO 적용 예상 기준일)를 확정 비약 없이 확인 축으로 처리 — REV-002 관찰 축 (g) 충족, ③ S3 조건부 형식으로 CRM 확정화 위험 구조적 차단, ④ S4 화법·S5 신설(실존 재료).
- **유지**: 현 상태 유지 결론, 성향=상한 해석, 정보안내 접점 3종, C1~C3 PASS.
- **악화**: 없음. (F-007 '화면 없음' 잔여는 이 Case 재료에 화면이 없어 비해당으로 재분류.)
- Verdict 이동: PASS → **PASS (유지)**.

## 8. Critical Mistake Check
없음 — "공격투자형이므로 실적배당/고위험 DO 변경 필요" 단정 없음 / 명시 의사 무시·"성향에 맞게" 프레이밍 없음 / 예금 100% 문제 규정·리밸런싱 스크립트 재생산 없음 / 성향 재분석 권유 없음 / KPI·TM 언급 없음(입력 제거와 무관하게 K-003 미인용) / 수치·상품명 생성 없음.

## 9. Constraint Check
C1 PASS · C2 PASS · C3 PASS (Runtime deterministic validation; REVIEW 항목 없음). 금지어·LaTeX·Evidence Provenance·화면번호·Candidate Pool 모두 PASS.

## 10. Employee Brief (Diagnostic — 의미 보존)
Unknown→Fact 변환 없음(E024·CRM 모두 확인 대상 유지) / 조건부→무조건 변환 없음(S3 조건 보존) / Hard Constraint 소실 없음 / Judgment 왜곡 없음(유지 결론이 S2·S3에 그대로) / 고객 의사 왜곡 없음. 세부는 §3 (g)(h).

## 11. Evidence
RUN_003 §3 (situation·unknowns), §6 (judgment·reasoning·must_confirm·supporting_evidence_ids), §7 (Actions 1–4), §8 (deterministic validation), §9 (S1~S5 brief); knowledge_pack.md K-001~K-008 대조; input_v2.md 변환 노트; EVAL_002 대조.

> 이 Artifact는 생성 후 수정하지 않는다.
