# Target Concept — Customer Evidence Pack · 판단 파이프라인 · Employee Brief (REV-002 대상)

- Status: **DRAFT — Step 2 산출물, Step 3 Human Gate 대기** (2026-08-31)
- 이 문서는 Human이 제시한 Input·Brief Target Concept을 Step 1 증거(`design/evidence/` 5건, 18개 Case 전수 역추적)와 결합해 정식화한 것이다. 여기의 모든 원칙에는 실증 근거를 병기했다. 확정은 Step 3에서 Human이 한다.
- 상세 명세: Input은 `design/EVIDENCE_PACK_SPEC.md`, Output은 `design/EMPLOYEE_BRIEF_SPEC.md`. 계획 전체는 `design/INPUT_BRIEF_WORK_PLAN.md`.

---

## 1. 중심 원칙

> Agent에게 "고객을 설명한 결론(판단 완료형 라벨)"을 주지 말고, "고객을 스스로 재구성할 수 있는 Evidence"를 시간·맥락·확실성 정보와 함께 준다. **계산은 시스템이 하고, 해석과 판단은 Agent가 한다.**

18개 Case(CASE_001 + GC-01~17)의 실증이 이 원칙을 지지한다:

| 원칙 요소 | 실증 근거 (evidence/ 문서) |
|---|---|
| 결론 라벨 금지 — Evidence만 | 입금사유·경과일이 없으면 모델이 "방치"를 채워 넣음(CASE_001·GC-12); 사유별 분해([04-12-644])를 준 GC-11은 "연금지급 대기 1,800만=정상 / 만기상환 300만=운용 대상"을 정확히 갈라 PASS (P1 관찰 1) |
| 계산은 시스템 | GC-04 RUN_001은 "입금 23일+DO 등록→2주 자동적용 도과"를 놓침(P0 관찰 4). P1에서 경과일 계산은 대체로 성공했으나 **계산 성공 ≠ 해석 성공** — GC-09(7주)·GC-17(10주)은 경과일을 맞게 계산하고도 산문에서 "방치"로 확정(P1 관찰 2) |
| 시점(as_of) 필수 | 발화 일자가 있어야 "재확인 필요" 판단 가능(GC-04 6개월 전·GC-06 8개월 전); GC-08은 입력의 금리 as-of를 출력에서 재생산하지 못함 → 동반 유지 규칙 필요 |
| 발화는 원문+일자+채널 | P1 9개 중 발화 3요소가 제공된 7개 Case 모두 판단 방향의 최우선 근거로 정확히 사용(P1 관찰 3); 부수 언급의 의사 승격(GC-10 "국민연금 63세")은 원문·확실성 구분 부재에서 발생 |
| Signal/Provenance 라벨링 | "행내 TM 대상 분류"·"참고" 라벨이 붙은 GC-05는 F-009 재발 없이 Contextual Evidence로만 사용 — 라벨 설계의 실증(P1 관찰 4) |

## 2. 판단 파이프라인 (판단층 / 전달층 분리)

```
Customer Evidence Pack (9-섹션 입력)
  ↓
① Customer State Interpretation   "어떤 상황이고 왜 이렇게 됐나" — Fact/추론 구분 명시
  ↓
② Management Judgment (방향 중립)  REV-001 재사용: 개입 필요 / 추가 확인 우선 / 현 상태 유지 가능
  ↓                               / 정보 안내 중심 / 고객 결정 지원 / 실행 불가
③ 핵심 관리 포인트 + 관리전략       ②의 결과를 기회 언어로 조직 (조건부 분기 유지)
  ↓
④ Required Confirmation           고객 확인 vs 직원 Operational Check 구분
  ↓
⑤ Employee Brief (5-섹션 출력)
```

- **F-005 재발 방지 구조**: "관리기회" 언어는 ③ 이후(전달층)에만 존재한다. ②는 REV-001이 17 Case에서 검증한 방향 중립 판단(Action/Change Bias 강한 재현 0/17)을 그대로 유지하며, "관리할 것 없음·유지·불가"도 동등한 정답이다.
- **핵심 관리 포인트의 넓은 정의**: 확인 우선("○○ 확인이 이번 접점의 목적"), 유지("유지가 합리적 + 다음 관리 시점 예약"), 실행 불가("불가 사유 정확 안내 + 대안 경로")도 모두 관리 포인트다. Golden Set의 Negative Case 5개·Counterfactual Pair 3쌍이 이 정의의 시험대다.
- **④의 구분 태그 근거**: GC-07(페널티 규정 존재 여부)·GC-16(이전 가능 여부 확정)은 확인 항목이 고객이 아니라 **직원의 Operational Check**였다 — 두 종류를 태그로 구분한다(BRIEF_SECTION_AUDIT (b)-2).

## 3. Input — Customer Evidence Pack (요약; 상세는 EVIDENCE_PACK_SPEC.md)

4덩어리: **Snapshot + Event Timeline + Wider Context + Evidence Metadata.** 9개 섹션:

| # | 섹션 | 핵심 실증 |
|---|---|---|
| 1 | Customer / Pension Profile | 성향 **변경 이력**(직전 분석일·결과)이 있어야 "상향"이라는 사건 자체가 인지됨(GC-09) |
| 2 | IRP Current Snapshot | 비중·수익률은 전처리 계산 제공(Excel [9C]도 SUMMARY를 집계 제공— "LLM이 직접 합산하지 않도록" 설계돼 있음) |
| 3 | IRP Event Timeline | 입금(+사유)·매매·운용지시·DO 자동적용 이력·성향 분석. **과거 시점의 파생값 스냅샷**(GC-07 "매수 당시 비중 66%")이 원인 추론에 결정적 |
| 4 | Whole-Asset Context | P1의 새 축: 타행 ISA(GC-13)·타사 연금저축(GC-15)·총급여·재직 여부가 판단의 **중심**이 된 Case 존재. 계좌 밖 데이터에도 값+일자+확실성("해지환급금: 미확인") 구조 필요(P1 관찰 8) |
| 5 | Investment Activity | 매매 빈도·1개월 증감액 등 수치형 행동 신호(Excel ACTIVITY 시트가 필드 원형) |
| 6 | Upcoming Events | 부차 항목(11월 만기 1,500만)이 평평한 나열에서 탈락(GC-09 F-003) → **시한·할 일 성격을 표시한 구조**로 분리 제공(P1 관찰 5) |
| 7 | Digital Signals | 조회·클릭·메뉴 진입 — "관심의 Evidence, 의사 아님" 개념 주석 필수. 구체 필드는 룰베이스 Excel이 유일 참고원 |
| 8 | Known Customer Intent | 발화 3요소(원문·일자·채널) 필수. 부수 언급과 명시 의사 구분 |
| 9 | Existing Bank Signals | TM/캠페인 분류는 Trigger Provenance로 격리 — 판단 근거 자리 금지(F-009) |

횡단 규칙: 모든 항목 `value + as_of` / `Fact · Calculated · Signal` 3분류 / 변화가 의미 있는 항목엔 변화량 / **Missing은 고정 슬롯으로 명시** / **NULL(값 없음)·0·"해당없음"(대상 아님) 3분 구분, 임의 보완 금지**(룰베이스 코드_거버넌스 원칙 차용).

## 4. Output — Employee Brief 5-섹션 (요약; 상세는 EMPLOYEE_BRIEF_SPEC.md)

직원의 업무 흐름을 미러링한 Recommendation Brief. 감사 결과(18 Case)가 보여준 현재와의 거리:

| 섹션 | 현 출력 대비 | 핵심 규칙 |
|---|---|---|
| S1 고객 상황 | 재배치 (18/18 존재) | **F-001 5건 전부 S1에서 발생** → 단정 어휘 금지가 1순위 규칙 |
| S2 핵심 관리 포인트 + 먼저 확인하세요 | 재배치 (REV-001 judgment+must_confirm이 원형) | 확인 항목은 관리 포인트에 종속; 고객/직원 확인 구분 |
| S3 추천 운용 방향 | 재배치 + 검증 신설 | 조건부 형식 강제; **F-008은 S3의 조건·제약 재진술부에서 발생**(GC-12 잔존) → 원재료 대조 검증; 비해당 유형(중도인출·실행불가·이탈)의 표기 규칙 정의 |
| S4 상담 Point | 순서는 재배치, **화법은 완전 신규 (0/18)** | 화법 공급원은 존재(용어 치환 사전·반론 세트·설명 순서 패턴 — SCREENS_HOTTIPS_INVENTORY §3) |
| S5 관련 TIP & GUIDE | **사실상 신규** (화면번호 Brief 생존 1/18, Hot Tip·출처 0/18) | 공급원은 충분(SRC-027 화면 마스터 68개 + Hot Tip 50건 6분류); Case→재료 색인이 병목 |

단일 문단 `employee_brief`가 F-001(단정)·F-008(조건 탈락)의 공통 발생 지점임이 확인됨 → **섹션화된 출력 스키마 + 섹션별 원재료 대조 검증**이 Spec의 전제.

## 5. Business 관점 원칙

> 은행의 Business Objective가 고객의 관리 필요성을 **만들어내서는 안 된다.** 하지만 고객에게 유효한 관리기회가 존재한다면, 허용 가능한 범위 안에서 그 기회를 은행의 관리행동(운용 활성화·장기 운용 연결·만기 재운용·추가납입·리밸런싱·이탈방어·연금관계 지속·후속관리)으로 **적극 연결해야 한다.**

- 판별 기준 = **근거 출처 테스트**: 관리 포인트의 근거가 Customer Fact/Event에서 출발하면 유효한 기회, KPI·캠페인·타겟 리스트에서 출발하면 필요성 창출(F-009, Critical Mistake 유지).
- D10(고객이익-영업압력 분리)의 폐기가 아니라 정밀화다. Hot Tip (f)군(KPI 동기성 9건)은 "동기는 버리고 절차만 발라내는" 편집 규칙으로 처리한다(SCREENS_HOTTIPS_INVENTORY §2).
- GC-04·GC-05의 출력이 이미 스스로 지킨 원칙("TM 분류를 압박 수단으로 쓰지 않는다")을 Spec 차원으로 승격한다.

## 6. Step 3 Human Gate — 결정 목록

이 컨셉을 구현(REV-002)으로 넘기기 전에 Human이 확정할 항목:

1. **Availability 확정**: EVIDENCE_PACK_SPEC의 모든 `?` — 은행 시스템에서 실제 확보 가능한 필드인지.
2. **HD-6 갱신**: Employee Brief를 Diagnostic Output → 직원용 실제 Output으로 승격.
3. **HD-7 신설**: §5 Business 관점 원칙 + 근거 출처 테스트의 명문화.
4. **SYSTEM_ROLE 원칙 5 변경**: 현 runtime은 "특정 상품명을 추천하지 않는다"(전면 금지)인데, 새 S3는 조건 충족 시 상품 수준 연결을 요구한다. 변경안: "확인 미완 상태에서의 상품 확정 금지 + 성향 Eligibility 준수 + 금소법 채널 제약(비대면 특정 펀드 언급 유의) 하에서 상품 유형→상품 연결 허용". **Runtime Semantic Change이므로 명시 승인 필요.**
5. **Evidence Pack 필드 취사선택**: 특히 (a) 피어 비교 통계(동연령대 수익률 — GC-05에서 압박에 쓰지 않는 것이 정답이었던 항목) 포함 여부, (b) 고객 식별 메타(성명·등급·관리점 — 기존 Case는 의도적 제외) 포함 여부, (c) 직원 화면 조회값의 입력 동봉 기준(판단 전 필요 vs 실행 전 필요 — P1 관찰 7) 승인.
6. **S5 재료 색인 구축 범위**: Case 유형→화면/Hot Tip/화법 역색인은 §20.8 보류 항목(Reusable Knowledge)과 경계가 닿는다. REV-002에서는 **Case별 Knowledge Pack에 S5 재료를 수동 동봉**(현행 방식 유지)하고 색인 자동화는 보류하는 것을 권고 — 승인 필요.
7. **Regression 범위**: 대표 6~8 Case 선정안 승인 (EMPLOYEE_BRIEF_SPEC §5의 제안 참조).

## 7. REV-002 구현 범위 (Step 4 예고 — Step 3 승인 후)

- `prototype/runtime.py`: (a) case.md §2를 9-섹션 Evidence Pack으로 파싱/직렬화, (b) 전처리 레이어(Calculated Fact — EVIDENCE_PACK_SPEC §4의 산식), (c) 출력 스키마를 5-섹션 Brief 구조로 분해, (d) 섹션별 원재료 대조 검증(F-001 어휘·F-008 조건 보존), (e) 기존 C1/C2/C3 validator 유지.
- 보류(§20.8 준수): Retrieval/색인 자동화, Reusable KB, Multi-Agent, 자동 Evaluator.
