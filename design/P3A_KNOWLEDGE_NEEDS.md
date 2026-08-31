# P3-A Knowledge Needs — Minimal Selector 입력 (Human-defined)

- Status: P3-A 실험 입력 (2026-08-31). **Knowledge Need 자체는 수동(Human 정의) 유지** — 이 파일은 기존 K-REQ(`design/KNOWLEDGE_REQUESTS.md`)와 Frozen knowledge_pack의 Human 구성에서 **전사(transcribe)** 한 것이며, 새 Need를 창작하지 않는다. 각 Need의 origin에 원 출처를 명시한다.
- 소비자: `prototype/selector.py` (Minimal Selection Layer). 파서 규약:
  - `## <CASE-ID>` 아래 `### KN-xx` 블록의 표(`| 필드 | 값 |`)를 읽는다.
  - `topic`은 `;` 구분 키워드/구절 목록 — 후보 탐색의 유일한 질의다.
  - `### manual_keep`의 불릿(`- K-xxx …`)은 Frozen knowledge_pack에서 **그대로 유지**할 항목(P3-A 자동화 범위 밖: TALK/HT/PRD/SCR 계열).
- 매칭 규칙(Selector v1): Registry 항목의 topics/applicability_tags/title 토큰이 need의 topic 구절 안에 **포함**되면 후보 (정규화: 공백·괄호 제거). Authority와 Relevance는 합산하지 않는다 — status → authority(purpose별) gate 순서 고정.

---

## GC-21

### KN-01
| 필드 | 값 |
|---|---|
| origin | REQ-007 (Human 정의; NOT_FOUND — Human-accepted Knowledge Gap, DB-003 §1) |
| purpose | definition (제도·정의 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 고객보유수익률; 상품수익률; 수익률 표시 기준; 매수 시점 효과; 두 수익률의 정의 |
| need_text | 고객보유수익률 vs 상품(기간)수익률의 표시 기준·차이(매수 시점 효과) 설명 자료 — 화면상 두 수익률의 정의 포함 |

### KN-02
| 필드 | 값 |
|---|---|
| origin | Frozen GC-21 knowledge_pack K-003 (Human 구성; COMMON — HD-2.1 Eligibility) |
| purpose | eligibility (판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 투자성향; 위험등급 적합성; 권유 가능 범위 (적극투자형 상한) |
| need_text | (고객 의향 확인 후) 위험 축소 대안을 논의하게 될 경우의 후보 선별 기준 — 투자성향의 해석과 권유 가능 등급 범위 |

### manual_keep
- K-002 (TALK 화법 — REQ-008 납품분. P3-A 수동 유지 범위: TALK Retrieval)

## GC-23

### KN-01
| 필드 | 값 |
|---|---|
| origin | Frozen GC-23 knowledge_pack K-001 (Human 구성; 원 납품 REQ-003 → OK-002) |
| purpose | procedure (제도·절차 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 계약이전 전출 접수 처리; 이전 의사확인; 손익 리스크 고지; 전출취소 |
| need_text | 계약이전(전출) 접수 고객 처리 절차·원칙 — 이전 유형·대상 확인, 손익 영향 고지, 고객 결정 존중 |

### KN-02
| 필드 | 값 |
|---|---|
| origin | REQ-011 (Human 정의 — F-010 재검증의 핵심 동봉물) |
| purpose | execution_feasibility (실행가능성 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 부분이전; 부분 이전 절차; 현금이전; 정기예금 중도해지이율 적용; 실물이전 |
| need_text | 부분 이전(일부 상품만 이전) 절차 + 현금이전 시 정기예금 중도해지이율 적용 구조·확인 화면 |

### manual_keep
- K-004 (GIC 특성·금리 비교 — PRD-018 연계 Product 재료. P3-A 수동 유지 범위: PRD Retrieval)

## GC-24

### KN-01
| 필드 | 값 |
|---|---|
| origin | REQ-012 (Human 정의) |
| purpose | tax_rule (세제 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 연금계좌 세액공제 구조; 총급여 구간별 공제율 16.5% 13.2%; 결정세액 조건; 세액공제 실효 확인; 원천징수영수증; [06-12-151] |
| need_text | 연금계좌 세액공제 구조: 총급여 구간별 공제율(16.5%/13.2%)·결정세액 조건(결정세액 < 공제액이면 실효 없음)·실효 확인 경로(원천징수영수증, [06-12-151]) |

### KN-02
| 필드 | 값 |
|---|---|
| origin | Frozen GC-24 knowledge_pack K-002 (Human 구성; 원 납품 OK-009) |
| purpose | tax_rule (세제 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 납입 후 중도인출·중도해지 시 과세 구조; 기타소득세; 과세제외 (장기 구속 고지) |
| need_text | 추가 납입 논의 시 장기 구속 고지 — 납입 후 중도인출·해지 시의 과세 구조 |

### KN-03
| 필드 | 값 |
|---|---|
| origin | Frozen GC-24 knowledge_pack K-003 (Human 구성; COMMON — HD-2.1 Eligibility) |
| purpose | eligibility (판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 투자성향; 위험등급 권유 가능 범위 (안정추구형) |
| need_text | 상품 이야기가 나올 경우의 선별 기준 — 안정추구형 고객의 상품 선택 범위 |

## GC-25

### KN-01
| 필드 | 값 |
|---|---|
| origin | REQ-013 (Human 정의) |
| purpose | tax_rule (세제 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | IRP 중도해지 과세 구조; 세액공제분·운용수익 기타소득세; 미공제분 과세제외; 미신청분 등록 [06-12-622]; 연금납입확인서; 소득·세액공제확인서 발급 시점 7월 1일 |
| need_text | IRP 중도해지 과세 구조: 세액공제분·운용수익 기타소득세 16.5%, 미공제(미신청)분 과세 제외 + 미신청분 등록 절차([06-12-622]), 직전 연도분 증빙 발급 개시 시점(7/1) |

### KN-02
| 필드 | 값 |
|---|---|
| origin | Frozen GC-25 knowledge_pack K-002 (Human 구성; 원 납품 OK-011·OK-003) |
| purpose | institutional (제도 — 판단 근거 Authority T1/T2 요구) |
| authority_required | T1/T2 |
| topic | 정기예금 중도해지이율; 특별중도해지 해당 여부; 중도해지 예상조회 |
| need_text | 계좌 해지 시 보유 정기예금의 중도해지 이율 구조 — 일반/특별중도해지 구분과 예상액 확인 경로 |
