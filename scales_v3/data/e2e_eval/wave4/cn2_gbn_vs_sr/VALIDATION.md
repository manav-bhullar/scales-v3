# Wave 4 / Q-CN2 - validation before live grading

**Exam id:** `e2e_wave4_cn2_gbn_vs_sr`  
**Topic:** Go-Back-N vs Selective Repeat (4 marks)  
**Students:** 8 synthetic

## Human review — 2026-07-25

Reviewed by the user (answers not rewritten by hand — fatigue). Changes applied:

| Item | Decision |
|------|----------|
| `CN2_GOOD_01` (c) | Wording fixed: "later packet" → "every packet already sent after it that is still in the current window" (past/sent packets, not future) |
| `CN2_GOOD_02` | Compressed wording too weak for full marks → gold band **mid**, range **2.5–3.5** (was high 3–4) |
| `CN2_MID_02` | Confirmed intentional: touches all four parts, none fully complete |
| `CN2_PARTIAL_B` | Only SR side — not "all parts partial" (that description is MID_02) |
| `CN2_LOW_01` | Intentionally wrong (ARQ confused with TCP congestion control) — keep as safety test |
| `CN2_LOW_02` | Intentionally empty ("I do not know") — must stay 0 |

**Question style note:** this pack still uses (a)–(d) subparts. Future packs (DB1+) must use **1-line or 2-part** stems closer to real exams; rubric concepts stay atomic internally.

## Approve checklist

- [x] Question + reference + rubric look exam-realistic *(accepted for CN2 smoke; style debt noted for next)*
- [x] Each gold `expected_score_range` matches human judgment *(after 2026-07-25 edits)*
- [x] `CN2_LOW_01` (congestion-control confusion) and `CN2_LOW_02` stay low band
- [x] Reply **approve Q-CN2** (or **approve wave4**) to run live grading

## After approval

```powershell
cd scales_v3
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave4/cn2_gbn_vs_sr/exam.json
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave4_cn2_gbn_vs_sr `
  --gold data/e2e_eval/wave4/cn2_gbn_vs_sr/gold_labels.json `
  --run-id wave4_cn2_smoke_v1 `
  --notes "Wave4 CN2 GBN vs SR smoke (human-reviewed gold)"
```

**Approved for live grading:** user — "grader now" — 2026-07-25.