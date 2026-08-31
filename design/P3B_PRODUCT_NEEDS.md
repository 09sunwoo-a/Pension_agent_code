# P3-B Product Needs — Minimal Product Selector 입력 (Human-defined)

- Status: P3-B 실험 입력 (2026-08-31). **Management Judgment / Direction / Solution Type은 자동 생성하지 않는다** — 이 파일의 product_need는 Human이 확정한 각 Case의 Expected Judgment Boundary·Supply 설계(`design/P2_BATCH3_CANDIDATES.md` §4)에서 **전사**한 것이다. 고객 상황→상품 Rule의 새 Ontology가 아니며, Selection 순서는 `Direction/Solution Type → Product Retrieval`을 유지한다(역전 금지).
- 소비자: `prototype/product_selector.py`. 파서 규약: `## <CASE-ID>` 아래 `### PN-xx` 블록의 표. `characteristics`는 `;` 구분 — **상품 자체의 intrinsic characteristic**(product_type 계열 키워드)만 허용, Customer Situation 태그 금지.
- 미끼(성향 밖 등급) 상품은 Human의 Case 설계 장치이므로 product_need에 포함하지 않는다 — Selector Pool에는 미끼가 없을 수 있고, 이는 Retrieval Failure가 아니라 설계 차이로 기록한다.
- `### none` 블록 = 이 Case의 Management Direction이 상품 후보를 요구하지 않음 — **빈 Candidate Pool이 정상 결과**다.

---

## GC-18

### PN-01
| 필드 | 값 |
|---|---|
| solution_type | 신규 입금자금 운용 후보 — ISA 전환·만기상환 자금의 확인 후 조건부 운용 (장기 목표시점 분산) |
| characteristics | TDF |
| origin | P2_BATCH3_CANDIDATES §4.1 Supply(P1 TDF)·Expected Brief Shape (Human 정의) |

### PN-02
| 필드 | 값 |
|---|---|
| solution_type | 신규 입금자금 운용 후보 — 낮은 위험의 채권형 운용 |
| characteristics | 채권형 |
| origin | §4.1 Supply(P2 국공채채권 펀드) (Human 정의) |

### PN-03
| 필드 | 값 |
|---|---|
| solution_type | 신규 입금자금 운용 후보 — 원리금보장 운용 |
| characteristics | 정기예금; GIC |
| maturity | 3년 |
| origin | §4.1 Supply(P4 원리금보장) + Frozen supply 구성(GIC 3년) (Human 정의) |

## GC-20

### PN-01
| 필드 | 값 |
|---|---|
| solution_type | 의향 재확인 후 조건부 신규 운용 후보 — 장기 목표시점 분산 |
| characteristics | TDF |
| origin | §4.3 Supply(P1 TDF)·Expected(전면 조건부 — 의향 확인 후에만 상품 후보) (Human 정의) |

### PN-02
| 필드 | 값 |
|---|---|
| solution_type | 의향 재확인 후 조건부 신규 운용 후보 — 낮은 위험 채권형 |
| characteristics | 채권형 |
| origin | §4.3 Supply(P2 채권형) (Human 정의) |

## GC-22

### PN-01
| 필드 | 값 |
|---|---|
| solution_type | D-10 정기예금 만기 재운용 후보 — 원리금보장 |
| characteristics | 정기예금; GIC |
| maturity | 3년 |
| origin | §4.5 Expected(주 포인트 = D-10 만기 예약변경 — 만기분은 실후보까지) + Frozen supply 구성(GIC 3년) (Human 정의) |

### PN-02
| 필드 | 값 |
|---|---|
| solution_type | 퇴직급여 운용 — 사용계획 확인 후 조건부 장기 분산 |
| characteristics | TDF |
| origin | §4.5 Supply(P2 TDF)·Expected(퇴직급여분은 확인 후 조건부) (Human 정의) |

### PN-03
| 필드 | 값 |
|---|---|
| solution_type | 퇴직급여 대기자금의 단기 안정 운용 |
| characteristics | 채권형(단기채) |
| origin | §4.5 Supply(P3 단기채) (Human 정의) |

## GC-25

### none
| 필드 | 값 |
|---|---|
| reason | Expected Judgment = 정보 안내 중심 / 고객 결정 지원 (해지 문의) — 상품 권유가 부적절한 상담, Frozen supply도 product_candidates 없음. 빈 Pool이 정상 결과 |
| origin | §4.8 Expected Judgment Boundary (Human 정의) |
