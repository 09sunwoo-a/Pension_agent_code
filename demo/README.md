# Demo Runs — 시연용 Golden Case 실행 기록

`design/DEMO_GOLDEN_CASE_DESIGN.md`에서 역설계한 시연 Case 5종(DEMO-A~E)의 실제 End-to-End 실행 결과.

## 구조

- `cases/DEMO-x/canonical.json` — 시연 고객 Evidence Pack (수기 작성, Fact/Signal/Unknown 원칙 준수) + supply(실존 SCR 화면·HT/TALK 원문 발췌 수동 동봉)
- `DEMO-x_RUN.json` / `DEMO-x_RUN.md` — 실행 기록 (LLM 5 Call: Knowledge Need → Hybrid 지식선택 prune → 관리판단 → Hybrid 상품선택 prune → Final Brief)

## 실행 방법

```bash
export GEMINI_API_KEY="..."   # 절대 커밋 금지
python3 prototype/demo_pipeline.py DEMO-A DEMO-B DEMO-C DEMO-D DEMO-E
```

`prototype/demo_pipeline.py`는 `mock_pipeline.py`(Mock v0)의 파이프라인을 그대로 재사용하되 Raw adapter 대신 이 폴더의 canonical.json을 직접 로드한다. Knowledge/Product Selection 상세 로그는 `prototype/out/demo_hybrid_*.json`(git 제외).

## Case ↔ 설계 문서 대응

| Case | 주제 (설계 §4) |
|---|---|
| DEMO-A | 타행 ISA 만기 D-25 × IRP 전환입금 × 추가 세액공제 (메인 E2E) |
| DEMO-B | 연금개시 예정 × 정기예금 만기 D-21 × 원리금보장 4종 심층 비교 |
| DEMO-C | 급여계좌 퇴직금 1.8억 발견 × 60일 과세이연 재입금 5-Step |
| DEMO-D | 디폴트옵션 자동매수 실행예정 D-7 × 대기자금 6,000만 |
| DEMO-E | "IRP 해지" 문의 × 중도인출 경로 확인 (Pattern B) |

## 주의

- RUN.md 상단 "Raw: prototype/mock/…" 표기는 재사용한 렌더러의 잔재 — 실제 입력은 `demo/cases/<CASE>/canonical.json`이다.
- 실행 결과는 시연 준비용 관찰 기록이며 Golden RUN/EVAL 체계(cases/GC-xx)와 별개다. Frozen 아님.
