# Wave 3 E2E report

**Exam:** `e2e_wave3_tcp_handshake_expanded` (24 students, TCP handshake Q1)  
**Providers:** Groq for first ~15 students, then **OpenRouter** (`meta-llama/llama-3.3-70b-instruct` CERA already done; `meta-llama/llama-3.1-8b-instruct` CGR) for the remainder.

## Headline metrics (ledger `wave3_openrouter_mixed`)

| Metric | Value |
|--------|------:|
| Items (student×concept) | 96 |
| DEFER rate | 29.2% (28/96) |
| False DEFER (FULL+DEFER) | 4.2% (4/96) |
| False ACCEPT (low-band marks>0) | 0.0% |
| Band hit rate (provisional ACCEPT-only totals) | **37.5%** |
| Mark MAE vs band midpoint | 1.06 |

> Provisional scores **exclude deferred concepts** until SHRR review. High DEFER on mid answers pulls provisional totals down and hurts band-hit — expected before teacher corrections.

## Ops notes from this run
1. Groq free TPM stalled mid-run → switched to OpenRouter.
2. OpenRouter 8B occasionally emitted **65k-token** runaway completions → added `max_tokens=2048` in `LLMClient`.
3. Empty-evidence PARTIAL/FULL hard-failed the pipeline → soft-downgrade to **ABSENT** so eval runs complete.

## Artifacts
- Store: `data/exams/e2e_wave3_tcp_handshake_expanded/`
- Gold: `data/e2e_eval/wave3/gold_labels.json`
- Ledger: `data/e2e_eval/METRICS_LEDGER.jsonl`
- Logs: `data/e2e_eval/wave3/grade_resume_openrouter*.log`
