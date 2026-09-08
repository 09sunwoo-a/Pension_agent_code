# p3_runs/ — P3 Selection 실험 기록

`prototype/out/`(git 제외) 에 떨어진 record 중 P3 실험 보고가 인용하는 것만 손으로 옮겨둔 폴더다.
코드가 여기에 쓰지 않는다 — `selector.py`·`product_selector.py`·`hybrid_selector.py`·`run_case.py` 는
전부 `out/` 에 쓴다. 보고서: `design/P3A_SELECTION_REPORT.md` · `P3B_SELECTION_REPORT.md` ·
`P3_RUN_COMPARISON.md` · `P3_HYBRID_INTEGRATION_REPORT.md`.

| 접두 | 무엇 | 재생성 |
|---|---|---|
| `p3a_selection_<GC>` | P3-A Knowledge Selection 로그 (deterministic) | 가능 |
| `p3b_pool_<GC>` | P3-B Product Candidate Pool 로그 (deterministic) | 가능 |
| `hybrid_knowledge_<GC>` · `hybrid_product_<GC>` · `mock_hybrid_*_MOCK_001` | Hybrid(det Recall → LLM Prune → det Gate) 로그 | LLM prune 이 섞여 있어 동일 재현 불가 |
| `p3a_run_manual_<GC>` / `p3a_run_selector_<GC>` | Human pack vs Selector pack 실 RUN record (Gemma 4 원출력·프롬프트 포함) | 불가 |
| `p3b_run_manual_<GC>` / `p3b_run_selector_<GC>` | 위와 같음, Product 축 | 불가 |
| `hy_run_know_<GC>` / `hy_run_prod_<GC>` | Hybrid 실 RUN record | 불가 |

`P3_RUN_COMPARISON.md` 가 «run record 14건 + selection log 8건» 이라 적은 것은 그 보고 시점의 수이고,
이후 Hybrid 통합에서 run 2건·log 14건이 더해져 지금은 run 16건 · log 22건이다.
