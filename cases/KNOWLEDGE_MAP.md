# Knowledge Map — IRP Knowledge Requirements (Failure Discovery Phase)

Case-local Knowledge가 실제 Runtime에서 어떻게 쓰였는지 축적한다. 공통 Domain Knowledge로의 의미적 승격은 Human 승인 없이 하지 않는다 (Reusable Knowledge 승격 정책은 P0 Batch Evidence 후 결정 — `AGENTS.md` §20.8).

Reusable Knowledge Candidate 기준: 둘 이상의 Case에서 필요하고 의미가 안정된 것. 현재 Case가 1개이므로 모두 `candidate (pending)`.

## Knowledge Items Used

| K-ID (Case) | Knowledge (요지) | Basis | Runtime 전달 | 모델 인용 (RUN_001) | Eval 관찰 | Reusable Candidate |
|---|---|---|---|---|---|---|
| CASE_001 K-001 | 고유계정대 = 현금성자산 = 운용지시 안 된 자산; 과다 보유 시 수익률 저하 "가능성" | Source-derived (SRC-002, SRC-001) | Knowledge + Authority | 인용 | F-002: 집단 가능성 → 개인 확정 | pending — 정의 부분만 |
| CASE_001 K-002 | 현금성자산 존재 ≠ 미운용; 입금 사유(교체매매·연금지급) 확인 | Source-derived (SRC-002 L178) | 〃 | 인용 | 구조화 출력에서는 작동, Brief에서 반대 사용 (F-001) | pending — 핵심 Reasoning Cue |
| CASE_001 K-003 | 상태 인지 → 사용계획 확인 → 필요 시 운용 검토; 이해 가능한 표현 | Source-derived (SRC-002) | 〃 | 인용 | 확인 우선 구조로 작동 | pending — 확인 순서 원칙 |
| CASE_001 K-004 | 자금 성격 → 투자기간·투자성향 두 축 | Source-derived (SRC-024) | 〃 | 인용 | F-002: 연령 → "실익 큼" 확장 | pending — Limitation 없이는 확장 위험 |
| CASE_001 K-005 | 디폴트옵션 정의; 자동운용 설정 여부 Context | Source-derived (SRC-089, SRC-088) | 〃 | 인용 | 조건부 후보로만 사용 (적절) | pending |
| CASE_001 K-007 | 원리금보장형 / 실적배당형 / 자동운용 어휘 | Source-derived (SRC-088) | 〃 | 인용 | 유형 수준 표현에 사용 | pending — 범용 어휘 |
| CASE_001 K-008 | C1 투자성향 5단계, 동등/하위만 허용 | Human-approved (Source Gap) | 〃 | 인용 | 준수 | → Constraint Map C1 |
| CASE_001 K-009 | 영업·마케팅 목적 Source와 관리 판단 분리 | Case-local Interpretation | 〃 | 미인용 | 위반 없음 (효과 여부 미확인) | pending |

## Knowledge Authority Classes (HD-3 반영)

Knowledge Pack의 각 K-item에는 다음 중 하나를 Authority로 기재한다.

| Class | 예 | Golden에서의 취급 |
|---|---|---|
| Official / Internal Rule | 연금개시 요건, 한도, 인출순서, 디폴트옵션 적용 시계, 위험자산 70% | Constraint 또는 제도 Fact 근거 (As-of 명시) |
| Product Fact | GIC/ELB 특성, TDF 빈티지·H/UH, 디폴트옵션 구성, 펀드 위험등급 | 상품 추론 근거; 월별 변경분은 "확인 필요" |
| Training Knowledge | 자금 성격→기간→성향, 연령대별 전략 | 판단 방향성 (규칙 아님) |
| **Operational Knowledge** (Hot Tip / Field Know-how) | 확인 순서·화면·채널·준비사항·현장 예외·실행 전 확인·화법 | 적극 활용. 단독으로 Hard Constraint·가입/실행 가능 여부 확정 불가 → `Operational Check Needed` |
| Marketing Practice | KPI 가중치, "무조건 IRP", 실물이전 불가 상품 유도 | 판단 근거 금지; 편향 원인 컨텍스트 |
| Public Explanation / Market·Product Data | KB Think, 웨비나, 시황·월간 포트폴리오 | 설명 수준 벤치마크 / 시점 병기 시에만 인용 |

## Source Traceability Gaps (Human-approved Business Fact 인데 공식 원문이 없는 것)

HD-2에 따라 아래 Gap은 Business Fact를 약화시키지 않는다. 공식 원문 확보 시 Source-grounded로 교체한다.

| Gap | 상태 | 영향 |
|---|---|---|
| 투자성향 ↔ 펀드 위험등급 Eligibility Mapping (C2) | Corpus에 매핑표 없음 (SRC-095 위험등급 라벨만) | C2는 Human-approved로 적용; Runtime Eligibility 검사는 매핑표 확보 전까지 "확인 절차 필요"로 |
| 투자성향 ↔ 디폴트옵션 Eligibility (C3) 공식 원문 | SRC-089 정리본만 (심의필 콘텐츠 기반) | C3 적용; 원문 확보 시 교체 |
| 투자성향 5단계 적합성 원칙 (C1) 공식 원문 | 미확보 | CASE_001 처리 유지 (소급 수정 없음) |

## GC-01 Knowledge Items (RUN_001 기준)

| K-ID | Knowledge (요지) | Authority Class | 모델 인용 | Eval 관찰 | Reusable Candidate |
|---|---|---|---|---|---|
| GC-01 K-001 | 자동 재예치 없음; DO 적용 시계(2주/4+2주/옵트인) | Public + Internal TM | 인용 | 정확 사용 | pending — GC-03/09/10 재사용 예상 |
| GC-01 K-002 | 지켜드림=3년제 정기예금; 성향별 가입범위 | Public + Product Data | 미인용 | F-006 (3년제 잠김 누락) | pending |
| GC-01 K-003 | 안전자산 선호 판단(펀드 이력) · 만기 D-30 예약변경 · 화면 | Operational (Internal) | 인용 | 판단 근거로 사용, 예약 시점 미사용 | pending |
| GC-01 K-004 | 원리금보장 4종 특징표 · 월 한도 · 만기별 금리 · 계산기 | Product Fact + Operational | 미인용 | F-006 | pending (GC-08) |
| GC-01 K-005 | 자금 성격→기간; 연금 수령이면 기간 재산정; 개시 요건 | Training + Internal | 인용 | 적절 | pending (GC-10/12) |
| GC-01 K-006 | 예보 한도 Source Conflict(5천만 vs 1억) | Conflict record | 미인용 | 위반 없음 | pending |
| GC-01 K-007 | 상담 순서·용어·금소법 | Communication | 인용 | 순서 반영 | pending |
| GC-01 K-008 | C1·C3 | Human-approved | 인용 | 준수 | → CONSTRAINT_MAP |
| GC-01 K-009 | KPI 분리 | Case-local | 미인용 | 위반 없음 | pending |

## GC-04 Knowledge Items (RUN_001 기준)

| K-ID | Knowledge (요지) | Authority Class | 모델 인용 | Eval 관찰 | Reusable Candidate |
|---|---|---|---|---|---|
| GC-04 K-001 | 성향=상한, 불일치≠관리 필요 (C1·C3) | Human-approved | 인용 | 정확 적용 | → CONSTRAINT_MAP (Reasoning Cue로도 재사용) |
| GC-04 K-002 | 안정형·원리금 100% 운용도 정당 | Operational/Public/Training | 인용 | 의사 존중에 사용 | pending |
| GC-04 K-003 | 성향-DO 불일치 TM = KPI 분류 | Marketing Practice | 인용 | KPI 분리 명시 | pending — D10 공통 후보 |
| GC-04 K-004 | 행동·이력≠현재 의사; Customer-stated 재확인 | Design | 인용 | Unknown#1로 반영 | pending — 공통 후보 (Core 원칙) |
| GC-04 K-005 | 자동 재예치 없음·DO 2주 적용·만기 금리 비교 | Public/Internal | 부분 인용 | F-006 (2주 규칙 미적용) | pending (GC-01 K-001과 통합 후보) |
| GC-04 K-006 | 개시 요건≠의무; 수령방식 3종 | Internal | 인용 | 적절 | pending (GC-10) |
| GC-04 K-007 | 물가 논리는 강제 근거 아님 | Training | 미인용 | 위반 없음 | pending |
| GC-04 K-008 | 상담 순서·톤 | Communication | 미인용 | 톤 적절 | pending |

## GC-03 Knowledge Items (RUN_001 기준)

| K-ID | Knowledge (요지) | Authority Class | 모델 인용 | Eval 관찰 | Reusable Candidate |
|---|---|---|---|---|---|
| GC-03 K-001 | 현금성 존재≠미운용; 입금사유·사용계획 확인 | Operational (Internal) | 인용 | 핵심 Cue로 작동 | **candidate — CASE_001 K-002/K-003과 동일 의미 (3 Case)** |
| GC-03 K-002 | DO 의무·최초입금 2주·등록된 경우만 | Public | 인용 | 정확 | candidate — GC-01 K-001/GC-04 K-005와 통합 (4 Case) |
| GC-03 K-003 | 개시 요건 55세+5년, 퇴직급여 시 55세만 | Internal 이론편 | 인용 | 정확 | candidate (GC-10/12) |
| GC-03 K-004 | 일시금 vs 연금 세금 구조 | Public 심의필 | 미인용 | F-006 | pending (GC-12/14) |
| GC-03 K-005 | 환급 전 지급·설계 제한 | Internal (Operational) | 미인용 | F-006 | pending |
| GC-03 K-006 | 자금 성격→기간→성향 | Training | 인용 | Unknown#3로 반영 | candidate (CASE_001 K-004 동일) |
| GC-03 K-007 | C1·C3 | Human-approved | 인용 | 준수 (Brief 재진술 오류 F-008) | → CONSTRAINT_MAP |
| GC-03 K-008 | KPI 분리 | Marketing 표시 | 미인용 | 위반 없음 | candidate — D10 공통 |

## Knowledge Gaps (기타 Traceability)

| Gap | 상태 | 영향 |
|---|---|---|
| 위험자산 100% 예외 상품 범위·초과 시 페널티 | SRC-077(Field) vs SRC-003/081 상이 → Source Conflict | GC-07: 공식 원문 확인 전 "확인 필요" |
| 연금수령 방식별 ETF 매도 절차 | SRC-084(Field); 불가 원칙은 SRC-003 | GC-11: Operational Check Needed |
| 중도인출 90%·신청 시한 1개월 원문 | SRC-003 검수필요 표시 | GC-14 |
| 예금자보호 한도 현행(1억) | SRC-001/087/089(2026) vs SRC-002/024(5천만) | 최신·공식 우선 |
| 연금개시 시 수수료 면제 조건 | SRC-003 ⟨판독불확실⟩ | GC-10/16 |

## Knowledge Issue Classification (EVAL_001 기준)

| 관찰 | 분류 |
|---|---|
| K-001 일반 가능성의 개인 확정화, K-004 연령 확장 | **Knowledge Usage Boundary** (Content·Authority 아님). Runtime이 Limitation 필드를 의도적으로 미전달한 설계와 연관 — Gate D 후보 |
| K-002 Brief에서 반대 방향 사용 | Prompt / Grounding 또는 Gemma Reasoning (Knowledge 자체는 정확) |

## Source Concerns 누적

- SRC-002 (As-of Unknown, 관련문서 2021): "1개월" 등 기준 — Threshold 미사용 유지.
- SRC-001 / SRC-037: 영업·이탈방어 목적 자료 — 판단 기준만 발췌, 목적은 배제 (K-009).
- SRC-088 / SRC-089: KB Think 정리본(원문 비복제) — 제도 사실 근거로 사용, 공식 원문 아님.
