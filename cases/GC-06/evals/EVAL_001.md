# EVAL_001 — GC-06

## 1. Evaluation Metadata
- Case: GC-06 / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-06/case.md FROZEN (commit bdec1bf) / Knowledge Pack: bdec1bf / Runtime: 601aa1b
- Basis: case.md §5; AGENTS.md §20.6

## 2. Verdict
**PARTIAL**

톤과 채널 판단이 Golden 경계에 잘 맞는다: 판매중단의 구조적 한계를 "조심스럽게" 안내, 유선 특정 상품 추천 지양·내점 유도(K-004), 고객 요청대로 비교 자료 준비, 분할 매도/매수(K-003), 교체 후 성과 약속 없음, C1/C3 정확 인용. Critical Mistake 없음.
PARTIAL 사유: (1) **행내 TM 리스트 포함을 관리 필요 근거로 사용**("TM 대상 리스트에 포함되어 있어 수익률 제고를 위한 관리가 필요한 시점") — Applicable Constraints·K-006이 금지한 Marketing 근거 재생산(P1, Hard Constraint 위반은 아님), (2) 선택지에 **"유지"(판매재개 가능성 포함)** 가 없고 모든 후보가 매도·전환·내점으로 수렴, (3) 손실 원인 분석(시장 vs 상품)·계좌 전체 관점(나머지 상품 양호 → −9.4%의 원인) 미사용, (4) 결정 시한·국내주식 익스포저 유지 의사 미확인.

## 3. Expected Judgment Check
| Must Consider | Result | Evidence |
|---|---|---|
| 판매중단 의미·한계, 성과 보장 불가 | MET (부분) | brief "구조적 한계를 조심스럽게"; 판매재개 가능성(K-001)은 미언급 |
| 비교 자료 준비 + 선택지 제시가 핵심 | PARTIAL | 비교 자료·분할매도는 있음; "유지" 선택지 없음 |
| 계좌 전체 관점 | PARTIAL | 15.9% 비중 언급, Unknown#3 다른 상품 유지 의사. 나머지 양호 → 손실 원인 설명 없음 |
| 손실 원인 분석(시장 vs 상품) | MISSED | — |
| 대안은 위험중립 범위 유형 | MET | Cand.1·2 위험중립형; brief C1/C3 명시 |
| 2026-01 매매 → 이미 조치했는지 | MET | Unknown#1 (비교 자료 수령·검토 여부) |

| Must Not Assume | Result |
|---|---|
| 즉시 전량 매도 | COMPLIANT (분할·동의 조건) |
| 회복 약속 | COMPLIANT |
| 위험중립 초과·모두드림 | COMPLIANT (모두드림 제외 명시) |
| 비교 자료 미수령 단정 | COMPLIANT (Unknown으로) |
| 판매중단 = 손실 확정 필요 | COMPLIANT |

| Required Confirmation | Result |
|---|---|
| 손실 감내 한도·결정 시한 | PARTIAL (한도 IDENTIFIED, 시한 MISSED) |
| 국내주식 익스포저 유지 의사 | MISSED |
| 2026-01 매매·이후 상황 | IDENTIFIED |
| 내점 가능 여부 | PARTIAL (내점 유도, 가능 여부 확인은 없음) |
| 직원: 최근 성과·재개 여부·추천펀드 자료 | PARTIAL (비교 자료 준비만) |

- Acceptable Direction: WITHIN — 관리 필요 높음 + 조심스러운 비교 상담 준비. Gap: 유지 선택지 부재, TM 근거 혼입.
- Forbidden: NO.

## 4. Critical Mistake Check
없음 (전량 매도 지시·회복 약속·등급 초과 확정 추천·유선 특정펀드·수치 생성 없음).

## 5. Constraint Check
- C1: PASS. C3: Runtime REVIEW(brief에 '모두드림' 언급) → Evaluator 확인: 부정문("모두드림은 제외") → **PASS**. C2: DETECT 없음(등급 라벨 미언급).
- 비-Hard 제약 위반: **Marketing/KPI 근거 사용**(reason) — Applicable Constraints "TM 리스트 = 관리 근거 아님" 위반. Hard Constraint 아님 → FAIL 아님.

## 6. Grounding Check
- Grounded: K-001, K-003, K-004, K-007, C1, C3 — 인용 정확. `knowledge_ids_used`에 'C1','C3'를 K-ID처럼 기재(형식 이탈, 무해).
- Weak: reason의 "TM 대상 리스트 … 수익률 제고를 위한 관리 필요" — K-006이 정반대로 정의한 내용. "추론: 심리적 부담이 크며…" 는 추론 표시가 되어 있어 적절.
- Under-used: K-002(예측 금지·처분효과 — 원인 분석 축), K-005(위험등급 확인 절차), K-006(KPI 분리 — 반대로 사용).
- Traceability: PASS.

## 7. Observed Failures → Failure Map
| # | 관찰 | Sev | Map |
|---|---|---|---|
| 1 | TM 리스트 포함을 관리 필요 근거로 사용 | **P1** | **F-009 (신규) Marketing Trigger as Management Basis** |
| 2 | "유지" 경로 부재 (판매재개 가능성 포함) | P1 | **F-005** (5/5) |
| 3 | K-002/K-005/K-006 미사용 → 원인 분석·등급 확인 절차 누락 | P2 | **F-006** (4/4) |
| 4 | 결정 시한·익스포저 의사·내점 가능 여부 미확인 | P2 | **F-004** (4 cases) |
| 5 | 나머지 상품 양호·전체 수익률 원인 설명 없음 | P2 | F-003 계열 (입력 Fact 미사용) |
| — | 직원 준비물(비교 자료·내점)·채널 제시됨 | — | F-007 **미재현** (이 Case에서는 양호) |

## 8. Candidate Failure Layer
- F-009: Prompt / Knowledge Usage — 입력에 "행내 TM 대상 분류" Fact가 있고 K-006이 "근거 아님"을 말했지만 Knowledge는 평면 나열로 전달됨(Limitation 미전달). LLM Reasoning이 입력 Fact를 관리 근거로 직결. CASE_001(위반 없음)·GC-04(명시적 분리)와 대조 → 비결정적.
- F-005: 동일 구조.

## 9. Evidence
RUN_001 §6 reason 2문장, §7 Cand.1~3, §9 brief; knowledge_pack K-001(재개 가능성), K-002, K-006.

## 10. Suggested Direction
F-009는 D10(Customer-interest Integrity) 직접 관련 — Batch 종료 시 "Marketing 태그 Knowledge/Fact의 전달 방식" 검토 후보. Stop Condition 없음(고객 불이익 Solution 아님). Human Gate 불필요.

> 이 Artifact는 생성 후 수정하지 않는다.
