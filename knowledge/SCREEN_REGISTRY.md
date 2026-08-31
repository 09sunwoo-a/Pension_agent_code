# Screen Registry (SCR-xxx) — 화면·절차 Master

- 내용: 화면번호·화면명·surface(staff/starbanking)·기능·메뉴 경로.
- **G3의 원천 Master**: Brief S5 화면 Reference·`validate_screen_refs`의 근거. **화면번호 오기 = deterministic FAIL과 직결** — 정확성이 최우선이며, 원천 대조 없이 번호를 쓰지 않는다.
- 공통 규칙: `knowledge/README.md` §2~§6. 주 원천: SRC-027(퇴직연금 주요거래 화면번호 안내) + Hot Tip·가이드 내 등장 화면.

## 항목 스키마 (표형 — 화면은 필드가 정형이므로 1행 1화면)

| 필드 | 정의 |
|---|---|
| id | SCR-xxx |
| surface | `staff`(단말) / `starbanking` / `internet_banking` / `corp_internet_banking` |
| screen_no | staff 단말 화면번호 `[nn-nn-nnn]` — **원천 표기 그대로.** 비대면 채널은 생략(`-`) |
| screen_name | 화면명 — 원천 표기 그대로 |
| menu_path | 비대면 채널 메뉴 경로 (예: `퇴직연금 > 개인형IRP > 운용상품 변경`). staff는 보통 `-` |
| actions | 이 화면에서 가능한 업무 — 원천의 '주요업무' 서술 기반 |
| source | SRC-xxx(+문서 내 위치). 복수 원천 대조 시 모두 기재 |
| authority / as_of / status / delivered_for / registered | README §3 공통 |
| verify | 검증 수준: `single`(원천 1건) / `cross`(2건 이상 일치) / `mismatch`(원천 간 불일치 — SC-xxx 병기) |

## Registry 표

| id | surface | screen_no | screen_name | menu_path | actions | source | authority | as_of | status | verify | delivered_for | registered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

(승인 후 B-1에서 등록 — REQ-014 화면 8종 + StarBanking 경로 3종 우선)

## 기재 규칙 (SCR 전용)

1. **화면번호는 원천에서 복사 대조한다.** 원천 간 번호·화면명이 다르면 임의 선택하지 않고 `verify=mismatch` + SC-xxx 기록 후 Human 판단.
2. 원천에서 확인되지 않는 화면은 등록하지 않는다(생성 금지). K-REQ 요청 화면이 원천에 없으면 해당 REQ를 NOT_FOUND로 회신.
3. 같은 화면번호가 여러 업무 맥락에 등장하면 actions에 병기하고 source를 모두 남긴다 (항목 분리 금지 — 1 화면번호 = 1 SCR ID).
4. 비대면 채널은 화면번호 대신 menu_path가 식별자다 — 경로 표기도 원천 그대로 옮기고, 개편 가능성이 있으므로 as_of를 반드시 남긴다.
5. 화면의 실존·현행 여부는 corpus 기준 확인까지만 — 실제 단말 검증은 프로젝트 밖(Limitation). 이 한계는 A가 인용 시 인지하도록 status/verify로 드러낸다.
