# Wave 4 — Multi-question smoke expansion

**Status:** authored, awaiting your gold validation before live API spend.

Wave 4 adds **three new subjects/topics** beyond TCP Wave 3. Each exam has **8 synthetic answers** (2 good / 2 mid / 2 partial / 2 low) for cheap smoke testing before scaling to 20+.

| Key | Folder | Exam ID | Subject | Topic |
|-----|--------|---------|---------|-------|
| Q-CN2 | `cn2_gbn_vs_sr/` | `e2e_wave4_cn2_gbn_vs_sr` | Computer Networks | Go-Back-N vs Selective Repeat |
| Q-OS1 | `os1_process_vs_thread/` | `e2e_wave4_os1_process_vs_thread` | Operating Systems | Process vs Thread |
| Q-DB1 | `db1_acid/` | `e2e_wave4_db1_acid` | Databases | ACID properties |

TCP Wave 3 (`../wave3/`) remains the **regression** set. Do not delete it.

## Roadmap (follow in order)

### Step 0 — Validate gold (you, ~30 min)

For each question folder, open `exam.json` + `gold_labels.json` and check:

- [ ] Question / reference / rubric look exam-realistic
- [ ] Each `expected_score_range` matches your judgment
- [ ] LOW answers must stay near 0 (safety)
- [ ] Reply **approve wave4** (or approve one key, e.g. `approve Q-OS1`) to allow live grading

### Step 1 — Unit regression (always)

```powershell
cd scales_v3
pytest tests/unit/ -v
# Roadmap gates only:
pytest tests/unit/ -v -m "contracts or harness or regression"
```

Gates covered:
- **contracts** — every `exam.json` ↔ `gold_labels.json` pair stays aligned
- **harness** — `run_pipeline` / `metrics_ledger` / `log_prompt_change` CLIs
- **regression** — CBTE decision surface + frozen Wave3 metrics invariants

`metrics_ledger.py` now also reports **silent zeros** (ACCEPT + 0 marks on non-low students) and prints an executable **pass bar**.

### Step 2 — Grade one question at a time (start with Q-OS1)

```powershell
# Example: OS first (new domain — most informative)
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave4/os1_process_vs_thread/exam.json

python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave4_os1_process_vs_thread `
  --gold data/e2e_eval/wave4/os1_process_vs_thread/gold_labels.json `
  --run-id wave4_os1_smoke_v1 `
  --notes "Wave4 OS smoke first live run"

python scripts/run_pipeline.py status --exam-id e2e_wave4_os1_process_vs_thread
```

Then same pattern for `cn2_gbn_vs_sr` and `db1_acid`.

### Step 3 — Diagnose before changing anything else

1. List false ACCEPTs on LOW students (must be ~0).
2. List high-band misses on GOOD students.
3. Check mid/partial for harsh ABSENT (should be PARTIAL when on-topic).
4. If you change a prompt, log it:

```powershell
python scripts/log_prompt_change.py add `
  --prompt cgr_grading.txt `
  --what "..." `
  --why "..." `
  --evidence "wave4 OS1 ..."
```

### Step 4 — SHRR + post-review metrics

```powershell
# After resolving DEFERs in UI or CLI:
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave4_os1_process_vs_thread `
  --gold data/e2e_eval/wave4/os1_process_vs_thread/gold_labels.json `
  --run-id wave4_os1_post_review `
  --post-review `
  --notes "after SHRR"
```

### Step 5 — Expand winners to n=20–24

Only after smoke band-hit / false-accept look sane, clone the pattern from Wave 3 and grow answer counts.

### Step 6 — TCP regression

Re-score Wave 3 (or at least compare ledger) after any prompt/threshold change so CN1 does not silently regress.

## Pass bar for Wave 4 smoke (per question)

| Metric | Pass |
|--------|------|
| False ACCEPT | 0 on the 2 LOW students |
| Silent-zero candidates | inspect ACCEPT+0 on HIGH students; gate only with concept-level human gold |
| GOOD students | provisional or post-review in high band |
| DEFER rate | not > 40% on n=8 (noisy; investigate if higher) |
| Mid/partial | not all scored 0 |

Printed automatically by `metrics_ledger.py` after each run.

## Files per question

```
wave4/<slug>/
  exam.json          # question + 8 answers
  gold_labels.json   # band gold
  VALIDATION.md      # approve checklist
```
