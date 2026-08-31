# Decisions B (DB-xxx) — Session B가 받은 Human 결정 기록

- `design/PARALLEL_WORKPLAN_A_B.md` §2: `golden/`은 A 소유이므로, B가 받은 Human 결정은 여기 기록하고 `golden/HUMAN_DECISIONS.md` 통합은 Human 지시 시에만 한다.
- 판단·Boundary에 영향 주는 발견(B-4)의 보고와 그 결정도 여기에 남긴다.

## 기록

| id | 일자 | 결정/보고 | 상태 |
|---|---|---|---|
| DB-001 | 2026-08-31 | B-0 Registry 스키마(필드·ID 체계·기재 규칙) 승인 — knowledge/ 7파일 구조·Stable ID·Authority T1/T2/T3/Public/UNCLEAR·Status 어휘 확정. 이후 항목 추가는 B 자율(PARALLEL_WORKPLAN §5 B-0 Gate 통과) | 확정 |
| DB-002 | 2026-08-31 | **[보고 — Human 결정 대기] R4 위험자산 한도의 원천 발견**: ① SRC-087(KB Think 공개 페이지, 준법심의필) L68 "주식형·주식혼합형 펀드 등 위험자산은 평가금액의 70% 이내에서만 운용 가능" ② SRC-098(연수 교재 T2) L60 "위험자산 70% 한도 규제 예외 — 고용노동부 승인 중위험·고위험 디폴트옵션 포트폴리오는 70% 초과 매수·운용 가능" ③ SRC-077(Hot Tip T3) 70% 한도·100% 투자 가능 예외 상품 정리. HD-8(공식 rule_source 확보 전 비활성화)·B-4(판단 영향 발견은 Registry 등재 전 Human 보고)에 따라 **Registry에 미등재** — 법령·내규 원문은 아니나 행내 공식 채널 2건(T2+Public)이 70% 한도·DO 예외를 서술함. R4 활성화 여부·근거 충분성은 Human 결정 사항 | 확정 (DB-003 §2로 결정 — 지식 등록 허용, deterministic Rule은 비활성 유지) |
| DB-003 | 2026-08-31 | **B-1 승인 및 후속 운영 결정 (Human)** — ① B-1 Knowledge 구축 결과 승인. **필수 K-REQ 완료 조건에 `Human-accepted NOT_FOUND` 허용** — 자료 부재 확인 시 임의 대체 Knowledge 생성 금지. REQ-007 = Accepted Knowledge Gap(GC-21에서 차이 원인을 Knowledge 없이 임의 생성하지 않는지 검증) / REQ-006 = Accepted Knowledge Gap(HT-003은 인접 자료이지 동일 화법의 대체 정답 아님). ② **R4**: 70% 한도·DO 예외 지식의 Registry 등록 허용(Source/Authority/Limitation 보존, → OK-012). 단 R4 deterministic Hard Constraint는 HD-8에 따라 **계속 비활성** — 공식 rule_source 확보 후 별도 Human Gate에서 활성화 판단. ③ **SC**: SC-001 OPEN 유지(확정 Rule 사용 금지) / SC-002 — 현재 Mock Screen Master에서 **[06-12-622] 채택**, SC 기록 보존, 실제 시스템 확인 전까지 타 번호 사용 금지 / SC-003 OPEN 유지(항목번호에 Brief/Rule 비의존). ④ **GC-23**: 부분이전 절차 미발견을 "부분이전 불가능"으로 승격 금지 — Knowledge 상태는 `현재 확보된 근거로 확인되지 않음` 유지. ⑤ **Product Registry**: sellable/channels null 상품의 판매·채널 실행가능성 확정 금지 — **Product Fit과 Execution Eligibility 구분**. ⑥ **B-3 전수 확장 정지** — 현재 Registry 규모로 P2 Integration·Knowledge Selection Logic 검증 충분. 이후 A의 신규 K-REQ 최우선 처리, B-3는 P2에서 실제 Knowledge Gap/Selection Gap이 확인된 영역부터 선택적 확장 | 확정 |
