# Wave 4 / Q-CN2 — validation before live grading

**Exam id:** `e2e_wave4_cn2_gbn_vs_sr`  
**Topic:** Go-Back-N vs Selective Repeat (4 marks)  
**Students:** 8 synthetic

## Approve checklist

- [ ] Question + reference + rubric look exam-realistic
- [ ] Each gold `expected_score_range` matches your judgment
- [ ] `CN2_LOW_01` (congestion-control confusion) and `CN2_LOW_02` stay low band
- [ ] Reply **approve Q-CN2** (or **approve wave4**) to run live grading

## After approval

```powershell
cd scales_v3
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave4/cn2_gbn_vs_sr/exam.json
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave4_cn2_gbn_vs_sr `
  --gold data/e2e_eval/wave4/cn2_gbn_vs_sr/gold_labels.json `
  --run-id wave4_cn2_smoke_v1 `
  --notes "Wave4 CN2 GBN vs SR smoke"
```
