# Wave 3 — validation before live grading

**Exam id:** `e2e_wave3_tcp_handshake_expanded`  
**Students:** 24 synthetic answers (same TCP handshake question as Waves 1–2)  
**Do not run live Groq until you approve this file.**

## Why Wave 3
- Grow gold from 6 → 24 so defer/accuracy metrics are less noisy
- Includes strong / mid / low / one-sided partial answers
- Intended to measure: Signal-1 evidence fix + CGR partial-credit prompt change

## Question / rubric
Same as Wave 2 (`data/e2e_eval/wave3/exam.json`). Total 4 marks, 1 per concept (SYN, SYN-ACK, final ACK, purpose).

## Band summary (see `gold_labels.json` for ranges)

| Band | Count | Student ids |
|------|------:|-------------|
| high | 5 | W3_GOOD_01 … 05 |
| mid / mid_low | 14 | W3_MID_*, W3_PARTIAL_* |
| low | 5 | W3_LOW_01 … 05 |

## Approve checklist
- [ ] Question + reference + rubric look exam-realistic
- [ ] Each gold `expected_score_range` matches your judgment of that answer
- [ ] Wrong-protocol / blank answers stay in low band
- [ ] Reply **approve wave3** to run live grading

## After approval
```powershell
cd scales_v3
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave3/exam.json
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave3_tcp_handshake_expanded `
  --gold data/e2e_eval/wave3/gold_labels.json `
  --run-id wave3_post_calib `
  --notes "after Signal-1 fix + CGR partial prompt"
```
