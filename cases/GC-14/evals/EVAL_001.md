# EVAL_001 — GC-14

## 1. Evaluation Metadata
- Case: GC-14 / Run: RUN_001 / Evaluated At: 2026-08-31 / Evaluator: Claude (separate context)
- Case Baseline: cases/GC-14/case.md FROZEN (commit 9e0cb60) / Knowledge Pack: 9e0cb60 / Runtime: 601aa1b
- Basis: case.md §5; AGENTS.md §20.6; HD-1/HD-3

## 2. Verdict
**PARTIAL** (PASS 경계에 가까움)

절차·세금 구조 판단이 정확하고 실무적이다: 법정 사유 가능성과 증빙 확인(Cand.1), 비대면 불가·창구 접수·서류 고지(K-003), 세전 신청 → 실수령 역산(K-002, Unknown#2 "세후 기준인지"), 매도 순서·현금성·정기예금 우선·중도해지 원금 미달 고지(K-004), 세액공제 미신청분 등록(K-005), **이 시점 추가납입·상품 권유 금지를 스스로 명시**(K-006). Critical Mistake·Constraint 위반 없음. Brief가 직원 행동 순서로 구성되어 F-007 미재현.
PARTIAL 사유: (1) **신청 가능 시기(계약 체결일~잔금 지급일 후 1개월 이내)** 미언급 — 시한 Fact 누락, (2) 잔금일 10/15 **역산 일정**(TDF 환매 3~10영업일·후선 처리 소요·내점 시기)이 "소요 기간 안내" 수준에 머묾, (3) 기타소득세 16.5% 구조 미언급(세전/세후 개념은 있음), (4) 내점 가능 시기 확인 누락.

## 3. Expected Judgment Check
| Must Consider | Result | Evidence |
|---|---|---|
| 사유·신청 시기·서류·무주택 확인 | PARTIAL | 사유·서류·무주택 MET; 신청 시기(잔금 후 1개월) MISSED |
| 세전 신청 → 실수령 감소(16.5%) → 역산 | PARTIAL | 역산 MET; 16.5% 구조 미언급 |
| 재원 비교 → 잔금일 역산 일정 | PARTIAL | 현금성·정기예금 우선, 원금 미달 고지 MET; TDF 환매일·10/15 역산 일정 없음 |
| 창구 접수·후선 소요 → 내점 시기 | PARTIAL | 창구 방문 MET; 시기 확인 없음 |
| 연금수령 중 아님 → 부분 인출 가능 | MET (암묵) | — |
| 권유 금지 | MET | brief 마지막 문장 |

| Must Not Assume | Result |
|---|---|
| 불가 / 사유 무관 가능 | COMPLIANT ("사실로 확인된다면 … 가능성이 높습니다") |
| 세후 신청 | COMPLIANT (정반대로 정확) |
| 비대면 가능 | COMPLIANT |
| 퇴직소득세 적용 | COMPLIANT (언급 없음) |
| 중도해지 손실 없음 | COMPLIANT (원금 미달 고지) |
| 무주택 확정 | COMPLIANT (Unknown#1) |

| Required Confirmation | Result |
|---|---|
| 무주택·서류 | IDENTIFIED |
| 3,000만 세후 기준인지 | IDENTIFIED |
| 재원 선호 | PARTIAL (우선순위 제안, 선호 확인 없음) |
| 내점 시기 | MISSED |
| 직원: 장표·매도 일정·미신청분 | PARTIAL (미신청분 MET) |

- Acceptable Direction: WITHIN — 실행 지원 구조가 정확.
- Forbidden: NO.

## 4. Critical Mistake Check
없음.

## 5. Constraint Check
- C1/C3: PASS (해당없음 라벨). HD-1: 세액 계산값 없음 → 준수. HD-3: Operational 항목(비대면 불가·세전 신청)을 사실로 안내 — 이 Case에서는 Knowledge가 그렇게 전달됐고 공식 Source와 정합(SRC-003)하므로 문제 없음.

## 6. Grounding Check
- Grounded: K-001~K-006 전부 정확 인용, 허위 없음.
- Weak: "재원은 확보되어 있으며"(situation) — 평가금액 3,800만 > 3,000만 이라는 단순 비교; 세전 신청·최대 90% 조건을 고려하면 여유가 크지 않음(3,000만 세후를 위해 세전 신청액이 커지면 90% 한도에 근접) — 이 계산은 Scope 밖이나 "여유 있다"는 인상은 과함.
- Under-used: K-001의 신청 시기·90%·16.5%; K-004의 펀드 환매일.
- Traceability: PASS.

## 7. Observed Failures → Failure Map
| # | 관찰 | Sev | Map |
|---|---|---|---|
| 1 | 신청 시기(잔금 후 1개월)·16.5%·90% 등 K-001 세부 미사용 | P2 | **F-006** (7/7) |
| 2 | 잔금일 역산 일정·내점 시기 없음 | P2 | **F-007** 경미 (행동 순서는 있음) |
| 3 | 재원 선호·내점 시기 확인 누락 | P3 | **F-004** (경미) |
| 4 | known_facts_used에 "자산 구성" 헤더만 기재(항목 미전개) | P3 | F-003 (형식) |

## 8. Candidate Failure Layer
- F-006: 이번에는 K-item은 전부 인용했으나 항목 내부의 세부(시기·세율)가 탈락 — Knowledge 길이 대비 요약 경향(LLM Reasoning).

## 9. Evidence
RUN_001 §3, §7 Cand.1~3, §9 brief; knowledge_pack K-001 L7–9(시기), K-004(환매일).

## 10. Suggested Direction
절차형 Case에서는 Brief 품질이 높음(GC-14·GC-06) — 판단형 Case(GC-01/04/10)와의 차이가 Batch 종료 시 분석 대상. Stop Condition 없음.

> 이 Artifact는 생성 후 수정하지 않는다.
