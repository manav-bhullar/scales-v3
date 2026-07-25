# Wave 4 / Q-OS1 — validation before live grading

**Exam id:** `e2e_wave4_os1_process_vs_thread`  
**Topic:** Process vs Thread (4 marks)  
**Students:** 8 synthetic  
**Recommended first live run** (new subject — best domain-transfer signal).

## Approve checklist

- [x] Question + reference + rubric look exam-realistic
- [x] Each gold `expected_score_range` matches your judgment
- [x] `OS1_LOW_01` (nonsense) and `OS1_LOW_02` stay low band
- [x] Approved for live grading (user: go for next — 2026-07-25; Gemini Flash-Lite)

## After approval

```powershell
cd scales_v3
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave4/os1_process_vs_thread/exam.json
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave4_os1_process_vs_thread `
  --gold data/e2e_eval/wave4/os1_process_vs_thread/gold_labels.json `
  --run-id wave4_os1_smoke_v1 `
  --notes "Wave4 OS process vs thread smoke"
```
