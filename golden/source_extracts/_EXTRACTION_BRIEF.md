# Source Extraction Brief (for 개인형IRP 사후관리 Agent Golden Set 설계)

You are reading part of a Korean bank's internal corpus about 개인형IRP (individual retirement pension) customer management.
Repository root: /Users/leesunwoo/clone-test/Pension_agent_code
Source index: sources/source_registry.md  (maps SRC-xxx IDs to file paths — use it to label each file with its SRC id)

Goal: NOT a summary. Extract *business knowledge a competent IRP after-care employee uses*, so that evaluation cases (Golden Set) can be designed. Read every assigned file fully (use sed -n / cat in chunks). Write the result to the output file given to you, in Korean, markdown.

For EACH source file produce a section with:

## SRC-xxx | title | 지식 성격
- 지식 성격 (Authority type): one or more of {Official/Internal Rule, Product Fact, Training Knowledge, Branch Know-how, Customer Communication Know-how, Marketing Practice, Public Explanation, Market/Product Data}. Note As-of / time-dependent items.
- 1. 고객을 무엇으로 이해하는가 — which customer contexts the source actually treats as important (연령, 가입기간, 납입상태, 자산구성, 현금성자산/고유계정대, 운용이력, 거래변화, 투자성향, 고객의도, 자금목적, 연금단계, 퇴직금 입금, 만기, 상담이력, KPI-related segments, etc). Include contexts NOT on this list if the source stresses them.
- 2. 직원이 판단하는 것 — the decisions the employee makes (관리 필요 여부, 단순안내 vs 관리, 추가확인 우선, 현상유지 가능, 운용변경 검토, 방향 선택, 실행 불가 판단 ...).
- 3. 업무 Fact / Rule — concrete institutional/product facts with numbers, dates, thresholds, procedures, 화면번호, legal limits (e.g., 위험자산 70% 한도, 세액공제 한도, 55세, 연금수령한도, 디폴트옵션 적용조건, 만기 후 처리, 중도인출 사유, 수수료 규정, 계약이전 요건). Quote precisely with line refs (file:line). Mark whether the source states it as official rule vs. employee's understanding.
- 4. 현장 확인사항 (Field checks) — what the employee must ask the customer or check before acting; what cannot be judged from system data alone; pre-consultation checks; pre-product-change checks; branch points by customer purpose; easy-to-make mistakes.
- 5. 상담/설명 노하우 — how difficult terms are explained, explanation order, avoiding fear/over-selling, product comparison framing, confirmation questions, distinguishing 제도안내 vs 투자권유, differences between employee-internal judgment and customer-facing talk. Abstract them into behaviors (do not just copy scripts, but quote 1-2 representative lines with file:line).
- 6. 상품 지식 — product types, characteristics (위험/기간/유동성/수익구조/보수/만기), which customer situations they are considered for, what must be known before choosing.
- 7. 현실적 고객상황 (Scenario seeds) — concrete customer situations depicted in the source (with the data fields that appear), usable as synthetic case seeds. Include both "action needed" and "no action / confirm first / keep as-is" situations if present.
- 8. Constraint 후보 — anything that reads like a hard limit (법/제도/투자성향/계좌상태/판매가능여부/채널) vs. soft guidance.
- 9. Source 간 충돌 / 시점 의존 / 주의 — anything contradictory, dated, or KPI-driven (marketing pressure) that should NOT be treated as customer-best-interest truth.

At the END write:
## 폴더 종합
- 반복되는 고객 Segment / Archetype
- 반복되는 판단축 (decision axes) — the variables that flip the judgment
- 이 폴더가 Golden Set에서 맡을 수 있는 역할
- 이 폴더에서 발견된, 제도/상품 Fact vs 현장 Know-how vs 마케팅 Practice 의 구분에서 특히 주의할 점
- 10-20개의 "유능한 직원이라면 알아야/판단해야 하는 것" 목록 (short bullets)

Be concrete, prefer specifics over generalities, keep file:line references. Length: as long as needed (typically 400-900 lines). Do NOT read files outside your assignment except source_registry.md.
