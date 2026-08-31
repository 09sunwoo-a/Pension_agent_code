# Source Conflicts (SC-xxx)

- Source 간 충돌 기록. **임의 통합·평균·해소 금지**(HD-3) — 공식성·최신성·적용범위 판단이 필요한 해소는 Human 몫.
- 관련 Registry 항목은 `status=CONFLICT` + 이 파일의 SC-ID를 병기한다.

## 스키마

| 필드 | 정의 |
|---|---|
| id | SC-xxx (append-only) |
| topic | 충돌 주제 한 줄 |
| sources | 충돌하는 SRC-ID들 + 각각의 주장 요지 (각 원문 위치 명시) |
| related | 관련 Registry 항목 ID (OK/PRD/HT/TALK/SCR) |
| found | 발견일 |
| resolution | Human 결정 전 `OPEN`. 결정 후 결정 요지 + DB-xxx 참조 |

## 기록

| id | topic | sources | related | found | resolution |
|---|---|---|---|---|---|

(발견 시 기록)
