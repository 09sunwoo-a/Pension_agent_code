# Knowledge Requests (K-REQ 대장) — Session A ↔ Session B 인터페이스

- 운영 규칙: `design/PARALLEL_WORKPLAN_A_B.md` §3.1. **두 세션의 유일한 공동 편집 파일.**
- 편집 권한: **A** = 행 추가, 상태를 REQUESTED/CLARIFY-답변으로 갱신 / **B** = 상태를 DELIVERED(납품 Registry ID 병기)·NOT_FOUND(사유)·CLARIFY(질문)로 갱신, 메모 열 기입. **서로의 행을 삭제·재작성하지 않는다.**
- 상태 흐름: `REQUESTED → DELIVERED(OK-xxx 등 병기) | NOT_FOUND(사유) | CLARIFY(질문) → (A 답변 후) REQUESTED`
- 필요 시점: **필수** = 해당 Case Freeze 전 DELIVERED가 전제 / **RUN 전** = Freeze는 가능하나 RUN 전 반영 / **참고** = 비차단.
- 배경 맥락: 각 Case의 상세 설계는 `design/P2_BATCH3_CANDIDATES.md` §4. B는 필요 시 참조하되 cases/·prototype/ 수정 금지.

| REQ-ID | Case | 유형 | 필요 내용 | 시점 | 상태 | 납품(Registry ID) | 메모 |
|---|---|---|---|---|---|---|---|
| REQ-001 | GC-18 | official | ISA 만기자금의 연금계좌(IRP/연금저축) 전환: 만기 후 60일 시한·전환 한도·전환 시 세액공제 추가한도 구조. 공식 Source 근거 필수(세제 Rule — 추정 금지) | 필수 | REQUESTED | | |
| REQ-002 | GC-18 | hot_tip | "IRP만 보지 말고 전체 자산 흐름을 먼저 여쭤보라" 취지의 field tip 원문+Metadata (Whole-Asset 접근 화법) | RUN 전 | REQUESTED | | |
| REQ-003 | GC-19 | official | 계약이전(전출) 접수 고객 처리 원칙: 이전 유형·대상 확인, 손익 영향 고지, 고객 결정 존중·절차 지연 금지. SRC-003 §03 원문 확인·항목화 | 필수 | REQUESTED | | |
| REQ-004 | GC-19 | talk/hot_tip | 이전 신호(메뉴 진입·비교 조회) 고객에 대한 접점 화법 — 고객 관점 톤(서비스 불편 확인 우선). 이탈대응 교육자료(SRC-013~017)에서 발췌 | RUN 전 | REQUESTED | | |
| REQ-005 | GC-20 | official | 투자성향 재분석·상향 변경 고객 안내 원칙: 성향 상향 = 권유 가능 상한 확대이며 운용 요구 아님(HD-2 해석과 정합하는 행내 근거) | 필수 | REQUESTED | | |
| REQ-006 | GC-20 | talk/hot_tip | 과거 "투자상품 권유 사절" 이력 고객 재접근 화법 — 과거 의사 존중 + 현재 의사 재확인 구조 | RUN 전 | REQUESTED | | |
| REQ-007 | GC-21 | official | 고객보유수익률 vs 상품(기간)수익률의 표시 기준·차이(매수 시점 효과) 설명 자료 — 화면상 두 수익률의 정의 포함 | 필수 | REQUESTED | | |
| REQ-008 | GC-21 | talk/hot_tip | 손실 구간 고객 상담 화법 — 숫자의 의미 설명 우선, 교체 압박 아님 | RUN 전 | REQUESTED | | |
| REQ-009 | GC-22 | official | 퇴직연금 정기예금 만기 처리: 자동 재예치 없음·만기 1개월 전부터 예약변경·만기 후 운용지시 없을 때 경로, **DO 미등록 계좌의 만기 후 처리 경로** 포함. SRC-001/002 확인 | 필수 | REQUESTED | | |
| REQ-010 | GC-22 | hot_tip | 퇴직급여 거액 입금 직후 상담 순서 tip — "계획 확인이 먼저, 상품은 다음" 취지 | RUN 전 | REQUESTED | | |
| REQ-011 | GC-23 | official | **부분 이전(일부 상품만 이전) 절차** + 현금이전 시 정기예금 중도해지이율 적용 구조·확인 화면. F-010 재검증의 핵심 동봉물 — 절차가 공식 Source에 실존하는지가 관건 | 필수 | REQUESTED | | |
| REQ-012 | GC-24 | official | 연금계좌 세액공제 구조: 총급여 구간별 공제율(16.5%/13.2%)·**결정세액 조건(결정세액 < 공제액이면 실효 없음)**·실효 확인 경로(원천징수영수증, [06-12-151]). 공식 Source 필수 | 필수 | REQUESTED | | |
| REQ-013 | GC-25 | official | IRP 중도해지 과세 구조: 세액공제분·운용수익 기타소득세 16.5%, **미공제(미신청)분 과세 제외 + 미신청분 등록 절차([06-12-622])**, 직전 연도분 증빙(연금납입확인서) 발급 개시 시점(7/1) | 필수 | REQUESTED | | |
| REQ-014 | COMMON | screen | Screen Master 1차: [04-12-642] [04-12-640] [06-AD-080] [04-12-17A] [06-12-151] [06-12-622] [02-12-221] [04-12-644] + StarBanking 경로(운용상품 변경 / 상품찾기 / 연금수령 정보) — 화면번호·화면명·surface·기능 실존 확인. **G3 validator(validate_screen_refs)의 원천 Master — 번호 정확성이 deterministic FAIL과 직결** | 필수 | REQUESTED | | |
| REQ-015 | COMMON | product | Product 카드 재료: TDF(빈티지별 등급 차이 포함)·채권형(국공채/단기채)·인컴형 펀드·저축은행 특별제공 정기예금·GIC + **미끼용 2~3등급 상품 2건 이상** — 상품명·유형·위험등급·수익률(측정기간·as-of)·sellable·채널. `design/CANONICAL_CONTRACTS.md` ProductCandidate 필드 정합 | 필수 | REQUESTED | | |
| REQ-016 | COMMON | hot_tip | Hot Tip Metadata(작성자·작성일·좋아요·출처) 원천 실존 확인 및 구조화 방식 확정 — HD-PRE-P2-BRIEF §4.6 확인사항("이미 그런 메타데이터가 있다"는 Human 확인)의 실납품. corpus 03_스타런_영업점_Hottip 기준 | 필수 | REQUESTED | | |

## 이력

- 2026-08-31: REQ-001~016 초기 등록 (Session A, A-0 — `design/P2_BATCH3_CANDIDATES.md` §4에서 도출).
