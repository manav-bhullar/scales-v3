# Where to find “why did the system score this?”

SCALES keeps an **audit trail per exam** under `data/exams/{exam_id}/`.  
That is the main log for testing — not the prompt changelog (that tracks *code/prompt* changes over time).

## Per-exam files (grading why)

| File | What it tells you |
|------|-------------------|
| `cqa_tuples.json` | What CERA decided concepts are: marks, facets, mode ANY/ALL, partial rules, keywords |
| `calibration_report.json` | Pre-grade smoke: which concepts looked wrongly ABSENT on sample answers |
| `grading_results.json` | **Main why-log**: per student × concept → verdict, marks, **evidence_span** (quoted text), **reasoning**, counter_arguments |
| `grading_results.json` → `cbte_results` | Trust decision: ACCEPT vs DEFER, tier, keyword/NLI scores, **reason** string |
| `teacher_corrections.json` | Human overrides after DEFER |
| `final_results.json` | Final scores after review/aggregate |

### Example (from CGR)

```json
{
  "student_id": "BURST_00",
  "concept_id": "Q1_C1",
  "verdict": "FULL",
  "marks_awarded": 1.5,
  "evidence_span": "concatenated sequence of multiple frames...",
  "reasoning": "The student explicitly mentions ... which satisfies ..."
}
```

### Example (from CBTE)

```json
{
  "decision": "DEFER",
  "tier_resolved": 3,
  "reason": "Tier 3: trust=0.40 (nli=0.00, stab=1.0, kw=0.33, tau=0.50)"
}
```

## Live console logs (loguru)

While grading runs, stdout shows:

- `cera`: extraction attempts / validation failures (why CERA retried)
- `cgr`: `STUDENT/CONCEPT: verdict=… marks=… evidence='…'`
- `cbte`: ACCEPT/DEFER + reason
- `llm_client`: model, token counts, latency, key rotation

Redirect if you want a session file:

```bash
.venv/bin/python scripts/run_pipeline.py grade --exam-json ... 2>&1 | tee run.log
```

## UI explain trail

API: `GET /api/exams/{exam_id}/breakdown`  
Returns per-concept evidence + reasoning (same fields as `grading_results.json`).

## Prompt / screw changelog (different purpose)

| File | Purpose |
|------|---------|
| `config/prompts/changes.jsonl` | Append-only history of **tuning** changes (TC-012, TC-014…) |
| `config/prompts/PROMPT_CHANGELOG.md` | Human-readable version of that |
| `config/prompts/SCREWS.md` | Named knobs |

Use this to answer “why did we change the system last week?” — **not** “why did student X get 1.5?”.

## Metrics ledger

`data/e2e_eval/METRICS_LEDGER.jsonl` — wave-level MAE / band-hit summaries after you log a run with `scripts/metrics_ledger.py`.
