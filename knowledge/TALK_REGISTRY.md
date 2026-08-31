# Talk Registry (TALK-xxx) — 상담화법

- 내용: 상담화법(연금왕찐천재·이탈대응 스크립트·TM 스크립트 등) — **원문 발췌 + 상황 태그**. 화법의 채택 여부 판단은 A/Human 몫.
- 공통 규칙: `knowledge/README.md` §2~§6.

## 항목 스키마

```markdown
### TALK-xxx. <화법 한 줄 제목>

| 필드 | 값 | 비고 |
|---|---|---|
| source | SRC-xxx §<위치> | 예: SRC-009 거절유형 Top4 |
| authority | T2-InternalGuide / T3-FieldTip / Public / UNCLEAR | 연수교재·부서 스크립트는 T2, Hot Tip 내 화법은 T3 |
| as_of | 원천 기준 시점 또는 Unknown | |
| status | ACTIVE / ... | |
| delivered_for | REQ-xxx (해당 시) | |
| registered | YYYY-MM-DD | |
| situation_tags | 상황 태그 (쉼표 구분) — §태그 어휘 | |
| audience | 대상 고객 유형 (원천에 명시된 경우만) | 예: 타행 IRP 보유, 손실 구간, 권유 사절 이력 |
| caution | 원천에 함께 적힌 유의사항 (있을 때만) | |

**원문 발췌** (재작성 금지, 발췌 범위 명시):

> 발췌 범위: <문서 내 위치>
>
> (스크립트/화법 원문 그대로)
```

### 상황 태그 어휘 (초안 — 필요 시 append)

`신규권유` `계약이전_유치` `이탈대응` `거절극복` `손실구간` `만기안내` `재예치` `수익률불만` `수수료불만` `세액공제` `과세이연` `연금수령` `퇴직금` `디폴트옵션` `재접근` `TM` `해피콜` `bank_objective_포함`

### 기재 규칙 (TALK 전용)

1. 화법 원문은 재작성·윤문 금지. STT 전사본의 구어체·오전사도 그대로 두되, 명백한 전사 잡음은 `(전사 불명)`으로 표기 가능.
2. 화법 속 제도·수치 주장(수수료율·세율 등)은 검증 없이 옮긴다 — 단 `공식 근거 확인 필요` 노트를 달고 공식 버전은 OK-xxx로 분리 구축한다.
3. 어떤 상황에 이 화법을 쓸지에 대한 서술은 원천에 있는 것만 audience/caution에 옮긴다. B의 자체 상황 판단은 situation_tags(검색용)까지만.
4. HD-7·G4: KPI·실적 목적이 섞인 화법은 원문 보존하되 `bank_objective_포함` 태그 필수 — Brief 추천사유로의 사용 가능 여부 판단은 A/Evaluator 몫.

---

## 항목

(승인 후 B-1에서 등록)
