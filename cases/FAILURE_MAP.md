# Failure Map — Gemma 4 Failure Patterns (Failure Discovery Phase)

Case별 개별 문구가 아니라 **반복 가능한 Pattern**을 축적한다. 각 Pattern은 Evidence(RUN/EVAL Artifact)로 추적 가능해야 한다.

Severity: P0 Critical/Regulatory/Hard Constraint · P1 Decision/Logical · P2 Knowledge/Grounding · P3 Output/Meaning Preservation · P4 Wording/Presentation Quality

Revision Status: `OBSERVED` (수정 없음, 축적 중) · `GATED` (Human Gate 상정) · `APPROVED` · `REVISED` (RUN_00n으로 검증) · `CLOSED`

---

## F-001 Uncertainty Loss (Structured → Brief)

- **Pattern**: 구조화 출력(Unknown / Reason)에서는 불확실성을 유지하지만, 최종 Employee Brief에서 확정 표현으로 변환된다.
- **Severity**: P3 (Meaning Preservation). 판단 사슬이 그 전제로 진행되면 P1로 상향.
- **Cases Observed**: CASE_001, GC-01, GC-04, GC-10, GC-12
- **Evidence**: RUN_001 §3 Unknown #1 "발생 사유(단순 미운용 vs 교체매매 대기)" ↔ §9 "현금성자산으로 **방치되어** 수익률 저하가 우려되는 상황" (EVAL_001 §3 Must Not Assume #1 VIOLATED). Smoke_01/02: "우려" 표현은 재현, "방치"는 미재현.
- **Candidate Layer**: Presentation (primary) · Prompt / Schema (employee_brief 지시 "왜 지금 봐야 하는지") · LLM Reasoning
- **Reproducibility**: Formal 1/1 (방치), 3/3 (일반 가능성 → 개인 상황 "우려"); GC-01 RUN_001 경미("가능성 높음"→"전형적인"); GC-04 "강력히 선호"; GC-10 situation [추론] 표기가 Brief에서 "63세 전까지 운용 희망"으로 확정; GC-12 reason "100% 현금성 자산으로 **방치**"(입금 14일·사용 예정) — CASE_001 동일 어휘
- **Revision Status**: OBSERVED

## F-002 Knowledge Over-application

- **Pattern**: Source-derived 일반 서술(집단 통계·교육 일반론)을 고객 개인의 확정 상태 또는 관리 필요성 강화 근거로 확대 적용한다.
- **Severity**: P2
- **Cases Observed**: CASE_001
- **Evidence**: K-001 "수익률이 낮아질 가능성이 높은 고객"(영업전략 자료) → RUN_001 §9 "수익률 저하가 우려되는 상황"; K-004 연령=투자기간 축 → §6 reason "투자 기간 확보가 가능하므로 점검이 필요", §9 "연령 특성상 운용 효율화의 실익이 큽니다" (EVAL_001 §5). Smoke_01 "운용 효율성이 매우 낮음".
- **Candidate Layer**: Knowledge — Usage Boundary (Limitation 미전달 설계) · LLM Reasoning · Prompt / Grounding
- **Knowledge Issue Class**: Knowledge Usage Boundary (Content·Authority 문제 아님)
- **Reproducibility**: 3/3 (연령·효율 확장), 형태는 Run마다 다름
- **Revision Status**: OBSERVED — Limitation 전달 여부는 Gate D 후보 (Batch 종료 시 상정)

## F-003 Provided Fact Omission

- **Pattern**: Customer Input에 존재하는 시점·이벤트 정보가 known_facts_used에서 탈락하고 이후 판단에 사용되지 않는다.
- **Severity**: P2 (Must Consider 누락) — 누락된 Fact가 Constraint에 해당하면 P0/P1
- **Cases Observed**: CASE_001, GC-01
- **Evidence**: 입력 "최근 입금일: 2026-02-10 (개인부담금)" → RUN_001 전 단계에서 미사용 (EVAL_001 Must Consider #3 MISSED, Required Confirmation #5 MISSED). Smoke_01은 입금을 언급했음 → 비결정적.
- **Candidate Layer**: Context Interpretation · Prompt / Schema (known_facts_used가 자유 선택)
- **Reproducibility**: 1/3; GC-01 RUN_001 재현(스타뱅킹 이용·입금예정상품 미등록·LMS 발송 미사용)
- **Revision Status**: OBSERVED

## F-004 Confirmation Axis Gap

- **Pattern**: Required Confirmation 중 고객 "현재 의사·인지"에 해당하는 축이 명시되지 않고 Candidate 조건문 속에 암시로만 남거나 누락된다.
- **Severity**: P2
- **Cases Observed**: CASE_001, GC-01, GC-03, GC-06, GC-10
- **Evidence**: RUN_001 unknowns 2건(발생 사유 / 인지·사용계획)만 기재; 현재 운용 의사(암시), 디폴트옵션 미등록 인지 여부(누락), 디폴트옵션 등록/적용 조건(누락) (EVAL_001 §3 Required Confirmation).
- **Candidate Layer**: LLM Reasoning · Prompt / Schema (unknowns_or_confirmations 단일 리스트)
- **Reproducibility**: 3/3 (unknown 항목 수 2–3건으로 축소되는 경향); GC-01 RUN_001 재현(만기 길이 선호·채널 누락); GC-03 RUN_001 재현(직접/위임 선호·DO 인지·고민 내용 누락); GC-06 RUN_001 재현(결정 시한·익스포저 의사·내점 가능 여부); GC-10 재현(재취업·추가 납입·TDF 유지 의사)
- **Revision Status**: OBSERVED

## F-005 Non-change Path Absent

- **Pattern**: "확인 후 판단" 구조를 취하면서도 확인 결과의 분기가 모두 변경(운용지시·등록) 방향으로만 구성되고, "현 상태 유지 / 판단 보류" 경로가 후보에 나타나지 않는다.
- **Severity**: P1 (조건부 대안의 논리적 완결성 — Decision/Logical)
- **Cases Observed**: CASE_001, **GC-01**, **GC-04**, GC-03(경미), **GC-06**
- **Evidence**: RUN_001 §7 Candidates 1–4 (확인 / 원리금보장형 / 실적배당형 / 디폴트옵션), §9 "이후 고객 의사에 따라 … 안내" — 유지 경로 없음 (EVAL_001 Acceptable Direction Gap). Smoke_01/02 동일.
- **Candidate Layer**: LLM Reasoning · Prompt / Schema (solution_candidates에 비변경 결과의 자리 부재) · Concept Model (Solution ≠ 변경 이라는 Core §6.2 원칙의 전달 여부)
- **Reproducibility**: 3/3; GC-01 RUN_001 재현 — 등록된 지켜드림 자동 적용 수용(현 상태 유지) 경로 부재, reason이 "디폴트옵션에 맡기기보다"로 배제 프레이밍 (EVAL_001 §3)
- GC-04 RUN_001 변형: 내용은 정보안내·현상유지 존중인데 `management_need.decision`을 "관리가 필요함"으로 라벨링, "관리 필요성 낮음/현 상태 유지 합리" 결론 미명시 (EVAL_001 §2)
- GC-03 RUN_001: 확인 우선 구조는 정확하나 "당분간 현 상태 유지" 경로 미명시 (경미)
- GC-06 RUN_001: 판매중단 펀드 "유지(판매재개 가능성 포함)" 선택지 부재, 후보가 매도·전환·내점으로만 구성
- **Revision Status**: OBSERVED — **Cross-case 5/5** → Batch 종료 시 Architecture Revision Proposal 1순위 후보

## F-006 Provided Knowledge Under-use

- **Pattern**: Context에 전달된 Knowledge 중 현재 판단에 직접 필요한 항목(상품 특성·확인 화면·시점 충돌 등)을 인용·사용하지 않아, 판단이 제도 Fact 수준에서 멈추고 상품 비교 축·실행 조건이 빠진다.
- **Severity**: P2
- **Cases Observed**: GC-01, GC-04, GC-03, GC-06, GC-10, GC-12, GC-14
- **Evidence**: GC-01 RUN_001 — K-002(지켜드림 3년제), K-004(만기별 금리·월 한도·[04-12-17A]·계산기), K-006(예보 한도 충돌) 미인용; Brief에 만기 잠김·비교 축·화면 없음 (EVAL_001 §6).
- **Candidate Layer**: Prompt / Grounding (Knowledge 9건 평면 나열, Relevance·Limitation 미전달 설계) · LLM Reasoning
- GC-04 RUN_001 — K-005의 "최초 입금 후 2주 무지시 → 등록 DO 적용" 규칙을 300만원(입금 23일)에 미적용, "운용지시 필요"로만 서술
- GC-03 RUN_001 — K-004(55세 전 인출=해지·퇴직소득세)·K-005(환급 전 지급 제한) 미사용 → 확인 질문의 근거·직원 확인 항목 누락
- GC-06 RUN_001 — K-002(원인 분석·처분효과)·K-005(등급 확인 절차)·K-006(KPI 분리) 미사용
- GC-10 RUN_001 — K-003(수령방식·한도/연차·자유인출 ETF)·K-004(수령기간·TDF) 미사용, 센터 연계로 대체
- GC-12 RUN_001 — K-003(한도 산식·[02-12-221]·연차) 미사용 → 화면 연결 누락
- GC-14 RUN_001 — K-item은 전부 인용했으나 K-001 내부 세부(신청 시기 1개월·16.5%·90%)·K-004 환매일 탈락 (요약 경향)
- **Reproducibility**: 7/7
- **Revision Status**: OBSERVED — **Cross-case 7** → Architecture Revision Proposal 후보

## F-007 Employee Next Action Absent

- **Pattern**: Employee Brief가 "무엇을 확인·검토하라"까지만 말하고, 직원이 어떤 화면·채널·시점에 무엇을 실행할지(D12 Branch Practicality)를 제시하지 않는다.
- **Severity**: P2 (Practical Usefulness)
- **Cases Observed**: GC-01, GC-04(경미), GC-03, GC-12
- **Evidence**: GC-01 RUN_001 §9 — 예약변경 시점(만기 D-30, K-003)·스타뱅킹 URL/내점·[04-12-17A] 확인·고유계정대 200만원 처리 없음 (EVAL_001 §7).
- **Candidate Layer**: Prompt / Schema (employee_brief 지시에 화면·채널·시점 항목 없음) · Concept Model (D12가 Output에 자리 없음)
- GC-03 RUN_001 — DO 등록 경로·[04-12-644]·환급 상태 확인 화면 없음
- GC-06 RUN_001: **미재현** — 비교 자료 준비·내점 유도·특정상품 지양이 Brief에 제시됨
- GC-12 RUN_001 — [02-12-221] 한도 조회·환급·세액미공제 확인·9월 말 시한 일정 없음 (HD-1 "화면 연결" 누락)
- **Reproducibility**: 4/5
- **Revision Status**: OBSERVED

## F-008 Constraint / Condition Drift (Structured → Brief)

- **Pattern**: 구조화 출력(candidate `risk_level`)은 Constraint를 정확히 지키지만, Employee Brief에서 Constraint 범위를 다르게(대개 더 좁게) 재진술하여 Candidate와 모순되고 직원 오독을 유발한다. F-001과 같은 "Structured → Brief 의미 변형" 계열.
- **Severity**: P2 (Hard Constraint 위반은 아님; 확장 방향으로 변형되면 P0)
- **Cases Observed**: GC-03, GC-12
- **Evidence**: GC-03 RUN_001 §9 "위험중립형을 상한으로 하여, 그 이하의 위험수준(안정형, 안정추구형) 내에서만 Solution을 검토" vs Cand.3 "투자성향 범위 내(안정형~위험중립형)" (EVAL_001 §5). GC-12 RUN_001: Cand.1 condition "연금수령한도 내 인출 구조"가 Brief에서 탈락해 "퇴직소득세 절감(70% 적용)"만 남음(1억 전액 감면 오독 가능, P1); Cand.2의 확인 조건(기간·목표)도 Brief에서 "제시·등록하십시오" 지시로 소실.
- **Candidate Layer**: Presentation · LLM Reasoning · Validation (Brief-Candidate 대조 검사 부재)
- **Reproducibility**: 2/2 (Pattern 확장: Constraint 범위뿐 아니라 Candidate condition 소실 포함)
- **Revision Status**: OBSERVED

## F-009 Marketing Trigger as Management Basis

- **Pattern**: 입력에 포함된 행내 TM/Target 분류 사실을 Management Need의 근거로 직결한다("리스트에 포함되어 있어 관리가 필요"). Knowledge가 "KPI 분류는 근거가 아니다"를 명시해도 재생산될 수 있다. D10(Customer-interest Integrity) 직접 관련.
- **Severity**: P1 (판단 근거 오류; 고객 불이익 Solution으로 이어지면 P0)
- **Cases Observed**: GC-06 (CASE_001·GC-04·GC-03에서는 미발생 — GC-04는 명시적으로 분리)
- **Evidence**: GC-06 RUN_001 §6 reason "행내 TM 대상 리스트에 포함되어 있어 수익률 제고를 위한 관리가 필요한 시점" vs knowledge_pack K-006 (EVAL_001 §7 #1).
- **Candidate Layer**: Prompt / Knowledge Usage (Marketing 태그 Knowledge의 Limitation 미전달; 입력 Fact와 Knowledge 경고가 분리 전달) · LLM Reasoning
- **Reproducibility**: 1/4 (비결정적)
- **Revision Status**: OBSERVED

---

## Cross-case Summary (갱신)

| Pattern | Severity | Cases | Reproducibility | Status |
|---|---|---|---|---|
| F-001 Uncertainty Loss | P3 | CASE_001, GC-01, GC-04, GC-10, GC-12 | 5 cases | OBSERVED (**Cross-case 5**) |
| F-002 Knowledge Over-application | P2 | CASE_001 | 3/3 | OBSERVED |
| F-003 Provided Fact Omission | P2 | CASE_001, GC-01, GC-04(경미), GC-03(경미) | 4 cases | OBSERVED |
| F-004 Confirmation Axis Gap | P2 | CASE_001, GC-01, GC-03, GC-06, GC-10 | 5 cases | OBSERVED (**Cross-case 5**) |
| F-005 Non-change Path Absent | P1 | CASE_001, GC-01, GC-04, GC-03(경미), GC-06 | 5 cases | OBSERVED (**Cross-case 5**) |
| F-006 Provided Knowledge Under-use | P2 | GC-01, GC-04, GC-03, GC-06, GC-10, GC-12, GC-14 | 7/7 | OBSERVED (**Cross-case 7**) |
| F-007 Employee Next Action Absent | P2 | GC-01, GC-04(경미), GC-03, GC-12 (GC-06 미재현) | 4/5 | OBSERVED (**Cross-case 4**) |
| F-008 Constraint/Condition Drift (Structured→Brief) | P2 (GC-12 P1) | GC-03, GC-12 | 2/2 | OBSERVED |
| F-009 Marketing Trigger as Management Basis | P1 | GC-06 | 1/4 | OBSERVED |

Immediate Gate 해당 없음 (P0 없음, C1/C3 유효, 고객 유해 Solution 없음, Leakage 없음). GC-01·GC-04·GC-03·GC-06·GC-10·GC-12·GC-14: Stop Condition 해당 없음.
