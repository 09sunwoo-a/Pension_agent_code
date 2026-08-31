# Official Knowledge Registry (OK-xxx)

- 내용: 제도·절차·과세·시한 등 공식 지식. **Case-agnostic 서술 + Limitation 필수.**
- 공통 규칙: `knowledge/README.md` §2~§6. 세제·제도 Rule은 공식(T1/T2) 근거만 확정 기술(HD-8).

## 항목 스키마

각 항목은 아래 블록 형식으로 기재한다 (표 1행에 담기에는 서술·Limitation이 길어 블록형 채택):

```markdown
### OK-xxx. <title>

| 필드 | 값 |
|---|---|
| source | SRC-xxx §<위치> (복수 시 나열) |
| authority | T1-Official / T2-InternalGuide / T3-FieldTip / Public / UNCLEAR |
| as_of | YYYY-MM(-DD) 또는 Unknown |
| status | ACTIVE / PROVISIONAL / CONFLICT / SUPERSEDED |
| delivered_for | REQ-xxx (해당 시) |
| registered | YYYY-MM-DD |
| topics | 검색용 키워드 (쉼표 구분) |

**Content** (Case-agnostic — 원천이 말하는 제도 사실만. 수치·시한·요건은 원문 값 그대로, 시점 의존 값은 as-of 병기):
- ...

**Limitation** (필수 — 단정 금지 경계):
- 이 지식이 확정해 주지 않는 것 / 개별 확인이 필요한 것 / 공식 근거 수준의 한계(T3·Public만 근거일 때 "공식 근거 미확보" 명기) / Agent Scope 밖(최종 확정 계산값 등 — HD-1).
```

### 기재 규칙 (OK 전용)

1. Content에는 "무엇이 제도상 사실인가"만 — 특정 고객에의 적용 판단·권유 문구 금지.
2. 조건부 사실은 조건부로 기재한다(조건 탈락 금지). 예: "~인 경우에 한해", "~은 별도 확인 필요".
3. 최종 세액·수령액 등 확정 계산값은 지식으로 기재하지 않는다 — 산식·구조·확인 화면까지만(HD-1).
4. 동일 주제를 여러 SRC가 다르게 말하면 통합하지 않고 SC-xxx 기록 후 각각의 서술을 보존한다.

---

## 항목

(승인 후 B-1에서 등록)
