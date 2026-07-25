# Wave 4 / Q-OS1 — validation before live grading

**Exam id:** `e2e_wave4_os1_process_vs_thread`  
**Topic:** Process vs Thread (5 marks)  
**Students:** 8 synthetic  
**Recommended first live run** (new subject — best domain-transfer signal).

## Human gold correction — 2026-07-25

The first 4-mark version asked for the difference in the stem/reference but did
not award a rubric/CQA mark for defining a process and a thread. Human review
identified that `OS1_GOOD_01` and `OS1_GOOD_02` answered all four applied parts
but omitted the core definition, so they should not receive full marks.

The exam is now 5 marks: definition/distinction + the original four concepts.
Student answers were deliberately preserved so the revised test measures the
omission rather than editing it away. The previous `wave4_os1_gemini_smoke_v1`
result applies only to the superseded 4-mark rubric and must not be compared as
if it used the same measurement stick.

## Approve checklist

- [x] Question + reference + 5-mark rubric look exam-realistic
- [x] Human gold updated: GOOD answers capped below 5 because definition is absent
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
