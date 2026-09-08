# demo/ — 현재 Demo HTML에서 역추출한 Demo Product / Case Specification

## Purpose

`demo/` 는 현재 발표용 Demo HTML(`퇴직연금 AI 대시보드 (standalone)`, 업로드 파일명
`76352690-_____AI______standalone.html`)을 분석해 **지금 실제로 구현된 Demo 서비스의 모습과
고객 Case 3종**을 사람이 읽을 수 있는 Markdown으로 옮긴 것이다.

이 폴더는 HTML을 **Source of Truth** 로 본다. HTML에 실제로 있는 값·문구·흐름을 그대로 기록하고,
기존 설계나 일반 금융지식과 다르더라도 **고치지 않고 `TO REVIEW` 로 남긴다**.

| 파일 | 역할 |
|---|---|
| `DEMO_TARGET_SPEC.md` | HTML 전체를 기준으로 서비스가 지향하는 경험(화면·정보모델·Brief 구조·Chat·업무화면) 정리 |
| `HTML_EXTRACTION_AUDIT.md` | 추출 범위, 발견한 고객 전수, HTML 내부 충돌, HTML↔Repo 차이, 사람 검토 항목 |
| `seed_cases/DEMO-01_KIM_SEOYEON.md` | 김서연 — 타행 ISA 만기 D-3 · ETF 조회 Case |
| `seed_cases/DEMO-02_LEE_SUMIN.md` | 이수민 — IRP 정기예금 만기 D-22 · 현금성 대기 · DO 미등록 Case |
| `seed_cases/DEMO-03_PARK_JEONGHO.md` | 박정호 — 퇴직급여 일반통장 수령 · 과세이연 60일 시한 Case |

## Authority

새로운 시연 Case를 설계할 때 참조 우선순위 (이 저장소 `09sunwoo-a/Pension_agent_code` 기준):

```text
1. demo/
   현재 시연 Product / UX / Case Story의 기준

2. sources/ + knowledge/
   제도·상품·업무절차 등의 실제 Grounding
   (sources/source_registry.md 로 원문을 찾고, knowledge/ 의 OK·PRD·HT·TALK·SCR Registry 로 정제 지식을 인용)

3. references/
   새로운 Demo Case 후보 발굴
   (references/planning/ 의 타겟 룰베이스·목업 9 Cases, references/06_주제별_추출지식/ — Grounding 근거로 쓰지 않는다)

4. golden/ + cases/
   판단 다양성 / Decision Boundary / Failure Pattern 참고
   (golden/HUMAN_DECISIONS.md · golden/GOLDEN_SET_DRAFT.md · cases/GC-xx · cases/FAILURE_MAP.md)

5. design/
   필요한 경우 Architecture 참고
   현재 Demo Target의 최상위 기준은 아님
   (design/EMPLOYEE_BRIEF_SPEC.md · design/CANONICAL_CONTRACTS.md 등과 Output 형식이 달라도 자동으로 design/ 을 우선하지 않는다)

prototype/
   Agent Runtime — 이번 demo/ 작업은 Runtime 을 수정하지 않는다
```

## Important Rule

`demo/` 는 금융제도나 상품 Fact의 공식 Source가 **아니다**.

- Demo Story(어떤 고객에게 어떤 화면·Brief·상담 흐름을 보여주는가)의 Source of Truth다.
- 세제 수치·상품·업무 절차 같은 업무지식의 정확성은 `sources/` 와 `knowledge/` 에서 검증한다.
- HTML 값이 기반지식과 다른 곳은 각 문서의 `TO REVIEW` / Audit 항목에 있다. 여기서 값을 고치지 않았다.
- 이 폴더의 문서는 `09sunwoo-a/Pension_agent` 저장소 브랜치
  `claude/pension-agent-html-reverse-engineer-8dkao8` 커밋 `a069b84` 에서 처음 작성된 뒤 이 저장소로
  이관됐다. HTML AS-IS 내용은 그대로 두고, 저장소 경로 표현과 «HTML ↔ Repo» 비교만 이 저장소 기준으로 다시 썼다.

## 표기 규약

- **HTML AS-IS** — HTML(JS 객체·마크업)에 실제 존재하는 값. 가능하면 위치(`DATA.ksy.hold`,
  `BRIEFS.ksy.s2` 등)를 함께 적는다.
- **Case Intent** — HTML 요소를 종합한 기획적 해석. Fact가 아니다.
- **TO REVIEW** — HTML 내부 충돌, 기반지식과의 정합성 확인 필요, 사람이 결정할 사항.

## 이 HTML의 구조 (읽는 사람을 위한 메모)

HTML은 번들러 포맷이다. `<script type="__bundler/template">` 안의 React 앱(`class Component extends
DCLogic`) 하나에 모든 데이터가 하드코딩돼 있다. 데이터 계층은 다음과 같다.

| 객체 | 내용 | 화면 렌더 여부 |
|---|---|---|
| `DATA` (+`OVR`/`EXT`/`EXT2`/`SCR`/`RC`) | 대시보드 고객 18명의 기본정보·보유상품·(구형) headline/metric/act/script | 기본정보·보유상품은 렌더. `head`/`metrics`/`act`/`why`/`tags`/`ai`/`pick`/`docs`/`cmp`/`refs` 등은 **현재 마크업에 바인딩되지 않은 dormant 데이터** |
| `QMETA` | 대시보드 리스트 행(스타클럽·관리단계·신호 태그·잔액·수익률) | 렌더 |
| `profileOf()` `FIX` | 3명 고정 프로필(나이·성별·등급·DO·수익률·계좌신규일·최근상품) — 나머지는 해시로 생성 | 렌더 |
| `BRIEFS` | 3명의 AI 브리핑 S1~S5 | 렌더 (`hasAiBrief`) |
| `QA` | 3명의 실시간 상담 챗(추천질문·답변·근거·CTA) | 렌더 (`agentOn`) |
| `SCR`/`COMMON`/`GEN` | 15명(대시보드 전용)의 «대응 가이드» 시뮬레이션 챗 | 렌더 (`agentOff`) |
| `RECO`/`FUNDS` | 디폴트옵션 4종·펀드 17종 카탈로그 | **현재 마크업에 바인딩되지 않음** |
| `BRIEF_SEGS` | 코스피 하락 브리핑 문구 | **미사용** — 화면의 부점 브리핑은 마크업 고정 텍스트 |
