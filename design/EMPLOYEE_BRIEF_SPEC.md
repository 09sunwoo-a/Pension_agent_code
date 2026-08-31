# Employee Brief Spec — 5-섹션 Output 명세 (확정본)

- Status: **HUMAN CONFIRMED — Step 3 결정 반영 (2026-08-31)**. 5-섹션 구조 승인(결정 3-1), S3 분기 규칙 수정(3-2), Candidate Pool(3-3), Evidence Trace(3-4), Validator 수정(3-5·3-6), S5 수동 동봉(3-7), Regression 8 Case(5).
- 근거: `design/evidence/BRIEF_SECTION_AUDIT.md`(18 Case 전수 감사) · `SCREENS_HOTTIPS_INVENTORY.md` · `P1_CASE_EVIDENCE.md`. 필수/금지 요소는 실제 발생 사례가 있는 것만.
- Brief 성격: **직원용 Recommendation Brief** (HD-6 갱신 — Target Output으로 승격; 단 운영 검증 완료를 의미하지 않으며 REV-002/P2 Regression·직원 검증 대상). 입장을 갖고 커밋하되 불확실성은 필요한 분기로 유지. 고객 직접 제공 문서 아님. 내부 판단 라벨 비노출.

감사 요약 (18 Case, 최신 RUN): S1 재배치(단 F-001 5건 전부 S1) · S2 재배치 · S3 재배치+검증 신설(F-008 발생 지점) · S4 순서 재배치+**화법 신규(0/18)** · S5 **사실상 신규**(화면번호 Brief 생존 1/18, Hot Tip·출처 0/18).

---

## 1. 섹션별 명세

### S1. 고객 상황

- **정의**: 현재 데이터상 고객이 어떤 상황인지 핵심만 간결하게. 관리 포인트와 연결되는 사실의 **선택**. 절제된 해석 허용.
- **원재료**: `current_situation` (재배치) + Evidence Pack의 A/R Fact.
- **필수**: Fact/추론 구분 유지 — 허용 문형 준거: "~로 추론되나 확인되지 않았다"(GC-05), "~로 분류될 수 있다"(GC-02), "가능성이 높다"(GC-14), "결정하지 않은 상태". 구조화 판단부의 Unknown이 S1 산문에서 사실로 승격되지 않을 것(F-001 5건 전부 이 지점).
- **금지** (실제 발생 사례 있음): 판정어 "방치" 및 동계열(CASE_001·GC-09·GC-17) — 대체 어휘 "운용으로 연결되지 않은 상태", "적용 예상 기준일 경과·실제 적용 여부 미확인" / 고객 의사·시점의 확정화(GC-10)·휴리스틱의 사실화(GC-01) / 강화 수식어(GC-04 RUN_001).
- DO 관련(결정 2-4 연동): 입력은 "적용 예상 기준일 경과"까지만 준다 — 실제 적용 여부·미적용 사유는 S1에서 확정하지 않고 확인 축으로 남긴다.

### S2. 핵심 관리 포인트 (+ 먼저 확인하세요)

- **정의**: "지금 무엇을 관리하는 것이 중요한가"에 대한 커밋 + 바로 아래 "먼저 확인하세요"(Required Confirmation 종속 — 확인은 포인트 실행의 첫 행동).
- **원재료**: `management_judgment` (재배치) + `must_confirm_before_action`. **Required Confirmation은 Agent가 도출한다** — 입력에 Decision Variable 슬롯이 없으므로(결정 2-11), 확인 축 도출 능력 자체가 평가 대상(F-004).
- **필수**:
  - 관리 포인트 1개(복수 이슈 시 우선순위 명시; 부차 시한 항목은 부 포인트 또는 S5 후속관리로 수용 — GC-09 대책).
  - "먼저 확인하세요"에 **[고객 확인] / [직원 확인(Operational Check)]** 태그(GC-07·GC-16 실례).
  - **Evidence Trace**(결정 3-4): Management Point에 `supporting_evidence_ids`(+필요 시 `supporting_knowledge_ids`)를 내부 필드로 남긴다 — 직원 화면 노출용이 아니라 판단의 Evidence Provenance 검증용. 근거가 Customer Evidence로 추적되지 않는 포인트는 REVIEW/FAIL(결정 3-5; HD-7의 검증 축).
- **Judgment 결과별 변형** (내부 라벨 비노출, 포인트 서술로 번역):
  | 내부 판단 | S2 포인트의 형태 |
  |---|---|
  | 개입 필요 | "○○ 관리가 필요합니다" + 먼저 확인 + 확인 후 연결 |
  | 추가 확인 우선 | "이번 접점의 목적은 ○○ 확인입니다" |
  | 현상유지 가능 | "현 운용 유지가 합리적입니다" + 다음 관리 시점 예약 |
  | 정보 안내 중심 | "○○ 제도 안내가 필요합니다" (권유 아님 명시) |
  | 고객 결정 지원 | "선택지·상충관계 안내로 결정을 지원합니다" |
  | 실행 불가 | "요청하신 ○○는 현재 불가 — 사유·충족 시점 안내가 포인트" |

### S3. 추천 운용 방향

- **정의**: 관리 포인트를 운용방향·Solution으로 연결. 연령·자금 성격·예상 기간·투자성향·자산구성·고객 의사 고려.
- **원재료**: `next_actions`(kind=변경/유지/고객 결정 지원) + condition + risk_level (재배치) + Candidate Pool(Reference Data).
- **분기 규칙** (결정 3-2 — **Branch Preservation, not Branch Creation**):
  - **Management Decision을 실제로 바꾸는 미확인 변수가 존재하는 경우에만** 조건 분기를 생성한다.
  - 존재하는 분기는 보존한다(F-010 대책 — GC-07 교체매매 vs 추가입금, GC-08 유지 vs 교체).
  - 불필요한 분기를 새로 만들지 않는다. Evidence만으로 방향이 충분히 결정된 경우 **단일 Recommended Direction 허용**.
  - 미확인 변수에 걸린 방향은 반드시 조건부("…이 확인되면 →")로 제시.
- **상품 수준 연결** (결정 3-3 = TARGET_CONCEPT §4.1 Candidate Pool 원칙):
  - 상품유형 판단은 가능. 특정 상품은 **승인된 Candidate Pool 내부에서만**(REV-002: Case별 Reference Data 동봉 — GC-17 TDF 라인업 방식).
  - C1/C2/C3 + 판매가능/채널 Constraint 통과 필수. LLM의 임의 상품 생성 금지.
  - 고객 의사/실행조건 미확인 시 조건부 제시, 고객의 최종 선택 전제.
- **기타 필수**: Constraint 범위의 정확 재진술(GC-03 RUN_001 축소 재발 방지) / Action condition·한도 개념의 변환 보존(F-008 — GC-12 잔존) / 수치의 as_of 동반 / 최종 계산값은 HD-1대로 화면·계산기 연결 / Recommended Direction에도 `supporting_evidence_ids` 부여(결정 3-4).
- **비해당 유형 표기 규칙**: 상품 권유 금지 사례(GC-14) → "이 상담에서 상품 권유는 하지 않습니다(사유)" 명시 / 실행 불가(GC-15) → "대안 경로 확인"으로 대체 / 이탈 대응(GC-16) → "대안 제시 + 고객 결정권 명시"로 대체.

### S4. 상담 Point

- **정의**: 직원의 접근 논리·순서 + 실제 고객 설명 문구.
- **원재료**: 순서·논리는 재배치(GC-02·GC-05·GC-16 준거). **화법 문장은 완전 신규(0/18)** — 스키마 필드·프롬프트 지시 신설.
- **필수**: 접근 순서 번호 목록(화살표는 플레인 "→" — LaTeX 잔재 방지) / **실제 화법 최소 1개** — 공급원: 용어 치환 사전·설명 순서 패턴·정직성 장치·이탈 골격(SCREENS_HOTTIPS_INVENTORY §3) / 단정·압박 회피 톤.
- **금지**: 근거 없는 비교·과장 / 용어 미치환("고유계정대" 그대로) / 압박성 설득(수익률 하위 등 비교·분류를 설득 근거로 — GC-05가 스스로 지킨 것의 승격. ※Bank Signal은 입력에서 제거되어 구조적으로도 차단됨).

### S5. 관련 TIP & GUIDE

- **정의**: 행내 자료에서 이 Case에 도움이 되는 실무 재료를 **출처와 함께** 연결: Hot Tip·확인 순서·반론 대응·관련 화면·업무 절차·후속관리·제도 유의사항.
- **공급 방식** (결정 3-7): Case별 Knowledge Pack에 **수동 동봉**. Retrieval 구축 금지·자동 색인 보류. **없는 Hot Tip/Guide 생성 금지** — 자료가 없으면 "관련 자료 없음 / 공식 화면·부서 확인 필요" 형태 허용(빈약 영역: 중도인출·상속/압류·공식 수수료율·연금수령 세부 세제).
- **필수**: 화면번호는 **[번호]+화면명+한 줄 용도**로 최종 출력까지 유지(GC-11 준거; GC-08·16 탈락 사례) / 출처: 자료명 또는 SRC-ID + 권위 수준(공식/행내 가이드/Hot Tip — Hot Tip은 HD-3 단서 "실행 전 공식 확인") / 시점 의존 수치 as-of / KPI 동기성 재료는 동기 제거·절차만 / Execution-time Check(수령한도·계산기·수수료율 — 결정 1-4)가 여기의 "확인하러 갈 곳" 목록으로 연결됨 / S2의 부차 시한 후속관리 구체화.

## 2. 스키마 방향 (구현 상세는 Step 4)

- `employee_brief` 단일 문자열 → 5개 필드(brief_s1~s5). S2 {포인트, 근거, 먼저_확인[{항목, 태그}]}, S3 {방향[{조건?, 내용, risk_level}] | 비해당{유형, 사유}} — condition은 미확인 변수가 있을 때만, S5 {항목[{내용, 출처, as_of?}]}.
- 구조화 판단부는 REV-001 스키마 유지 + **`supporting_evidence_ids` / `supporting_knowledge_ids`** 추가(Management Point·Recommended Direction 단위). Evidence 항목에는 직렬화 시 참조 가능한 ID를 부여한다. — Chain-of-Thought 저장이 아니라 Provenance 검증 구조(결정 3-4).

## 3. 검증 경계 (결정 3-6 — deterministic과 Evaluator 판정 분리)

**의미 판정을 문자열 Validator로 억지 구현하지 않는다.**

### 3.1 Deterministic Validator (문자열/구조만으로 확정 판정 — Step 4 구현)

| 검사 | 규칙 |
|---|---|
| 금지어 | "방치" 등 금지 어휘 목록 검출 (S1 포함 전 섹션) |
| 형식 | LaTeX 잔재(`$\rightarrow$` 등) 검출 |
| Constraint ID/range | C1/C2/C3 재진술 범위를 원문과 문자 대조 (기존 validator 확장) |
| Required field | 5-섹션 필드·구조화 condition 필드 존재 여부 |
| Evidence ID | `supporting_evidence_ids`의 존재 + 실제 Evidence Pack ID와 대조 — 부재·불일치 시 REVIEW/FAIL (**결정 3-5: 구 "Bank Signals 인용 FAIL" 규칙 대체** — Management Point는 실제 Customer Evidence로 추적 가능해야 한다) |
| 화면번호 형식·생존 | 입력/Knowledge에 있는 화면번호가 출력 어디에도 없으면 REVIEW; 형식 [NN-NN-NNN] 검사 |
| Candidate Pool | S3의 특정 상품명이 동봉된 Pool 목록 밖이면 FAIL |

### 3.2 Evaluator Review 대상 (Claude Evaluator — 의미 판정)

- Unknown이 사실로 승격되었는가 (F-001의 의미 층위).
- 표현이 과도하게 단정적인가 / 강화 수식어.
- Management Point가 Evidence와 논리적으로 정합한가 (Trace ID 존재는 deterministic, 논리 정합은 Evaluator).
- 분기 규칙 준수: 만들어야 할 분기의 누락(F-010) / 불필요한 분기 생성.
- 상담 화법이 압박적으로 들리는가 / 용어 치환 적절성.
- S5 재료의 실존·적합성 (생성 여부는 Knowledge Pack 대조로 부분 deterministic).

## 4. 섹션별 평가 축 (Regression 관찰)

- S1: 핵심 사실 선택 / 어휘 절제 / Fact-추론 구분.
- S2: 포인트의 Evidence 정합(Trace) / 확인 축 도출의 완전성(**입력 힌트 없이** — F-004 재관찰) / Judgment 유형 정합(유지·불가 Case에서 개입 포인트 미생성 — **F-005 재발 감지**).
- S3: 분기 규칙(보존 누락도, 과잉 생성도 감점) / Constraint 정확성 / Candidate Pool 준수 / 비해당 유형 규칙.
- S4: 순서 논리 / 화법 사용 가능성·톤.
- S5: 실존 재료·출처·as-of / 실무 유용성(F-007 계열).
- 신규 관찰 축: DO "적용 예상 기준일 경과"를 받은 Case(GC-09·17)에서 미적용 확정·"방치" 재발 여부 / CRM 메모(verbatim 비보장)를 Ground Truth로 승격하는지.

## 5. Regression 대표 Case — 8개 확정 (결정 5)

| Case | 선정 사유 |
|---|---|
| GC-04 + GC-05 | **Counterfactual Pair 필수 유지** — F-005 재도입 감지선 |
| GC-03 | 확인 우선 + F-008 최초 발생 (조건 보존 검증) |
| GC-09 | 개입 필요 + F-001 "방치" + F-003 부차 만기 (⑥ Upcoming 효과) |
| GC-11 | 실행 불가(조건부) + S5 화면 생존 모범 — **유지** 확인 |
| GC-14 | S3 비해당(상품 권유 금지) 표기 규칙 |
| GC-16 | 이탈 대응 유형 + S4 반론·S5 탈락 개선 |
| **GC-17** | **추가(결정 5)** — DO 적용 예상시점/미적용 해석과 F-001 재발을 GC-09와 함께 검증 |

변환 규칙: 기존 Frozen case.md 불변. `input_v2`는 **기존 정보량 유지·조직 구조만 변환·새 사실 추가 금지** (Arithmetic/Rule-derived Fact는 기존 값의 파생이므로 허용). 새 스키마에서 제외된 필드(예: GC-05 마이데이터·TM, GC-09 DO 자동적용 이력)의 처리는 Step 3 보고 §6 확인 항목.
