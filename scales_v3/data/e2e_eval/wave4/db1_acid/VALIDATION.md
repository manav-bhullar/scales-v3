# Wave 4 / Q-DB1 — validation before live grading

**Exam id:** `e2e_wave4_db1_acid`  
**Topic:** ACID properties (4 marks)  
**Students:** 8 synthetic

## Approve checklist

- [ ] Question + reference + rubric look exam-realistic
- [ ] Each gold `expected_score_range` matches your judgment
- [ ] `DB1_LOW_01` (wrong definitions) and `DB1_LOW_02` stay low band
- [ ] Reply **approve Q-DB1** (or **approve wave4**) to run live grading

## After approval

```powershell
cd scales_v3
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave4/db1_acid/exam.json
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave4_db1_acid `
  --gold data/e2e_eval/wave4/db1_acid/gold_labels.json `
  --run-id wave4_db1_smoke_v1 `
  --notes "Wave4 DB ACID smoke"
```
