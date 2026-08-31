# Hot Tip Registry (HT-xxx)

- 내용: Hot Tip **원문 보존** + Metadata 구조화. **원문 재작성 금지** — 검색용 요약은 별도 필드로만.
- 공통 규칙: `knowledge/README.md` §2~§6. HD-3: 좋아요 = 공감 Signal이지 공식성 근거 아님.
- Metadata 원천: corpus `03_스타런_영업점_Hottip/posts/*.md`의 frontmatter에 글번호·제목·작성자(소속/직급)·작성일·조회수·좋아요·배지·해시태그·원문 URL이 실존한다(REQ-016 관련 — 임의 생성 불필요).

## 항목 스키마

```markdown
### HT-xxx. <원문 제목>

| 필드 | 값 | 비고 |
|---|---|---|
| source | SRC-xxx (글번호 nnnnnn) | corpus 03 폴더 |
| kind | field_hot_tip / official_guide | CANONICAL_CONTRACTS §2.2 — 행내 공식 가이드 발췌는 official_guide |
| author | 이름 (소속 / 직급) | frontmatter 그대로 — 없으면 생략 |
| written_at | YYYY-MM-DD | frontmatter 작성일 |
| likes | n | frontmatter 좋아요 — corpus 수집 시점 기준 |
| views | n | frontmatter 조회수 (선택) |
| authority | T3-FieldTip (03 폴더 기본값) | |
| as_of | 작성일 기준 | |
| status | ACTIVE / ... | |
| delivered_for | REQ-xxx (해당 시) | |
| registered | YYYY-MM-DD | |
| situation_tags | 검색용 상황 태그 (쉼표 구분) | B 작성 — 원문 아님 |
| search_summary | 검색용 1~2문장 요약 | B 작성 — **원문 아님을 이 필드로 격리** |

**원문 발췌** (excerpt — 재작성·윤문 금지, 발췌 범위 명시. supply HotTip.body의 원천):

> 발췌 범위: <문서 내 위치>
>
> (원문 그대로)
```

### 기재 규칙 (HT 전용)

1. 원문 발췌는 오탈자 포함 그대로 옮긴다. 강조 마크업(`==`·`**`)은 가독을 위해 제거할 수 있으나 문장·어휘는 불변. 이미지 설명은 `[이미지: ...]`로 표기해 원문과 구분한다.
2. 발췌는 Tip의 핵심 단위(전체가 필요하면 전체)로 하되, 어디부터 어디까지인지 명시한다.
3. Tip 안의 제도·세제 서술은 이 Registry에서 검증하지 않는다 — 공식 확인이 필요한 서술이 포함되면 항목에 `공식 근거 확인 필요` 노트를 남기고, 해당 제도 사실의 공식 버전은 OK-xxx로 별도 구축한다.
4. KPI·실적 관련 내용(HD-7: Bank Objective)은 원문 보존 대상이지만, situation_tags에 `bank_objective_포함`을 달아 A가 인용 시 식별할 수 있게 한다.
5. author 등 개인 식별 정보는 frontmatter에 있는 그대로만 옮긴다(가공·보완 금지).

---

## 항목

(승인 후 B-1에서 등록)
