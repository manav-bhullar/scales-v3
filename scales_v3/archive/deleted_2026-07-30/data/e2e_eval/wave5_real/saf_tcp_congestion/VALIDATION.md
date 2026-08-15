# Wave 5 / Q-REAL2 — validation before live grading

**Exam id:** `e2e_wave5_saf_tcp_congestion`  
**Question:** TCP congestion control — name the 2 phases and explain how
`cwnd` / `ss_thresh` change in each (5 marks)  
**Students:** **20 REAL answers** (stratified smoke from 65) — SAF subset of
ASAG2024 (`Meyerger/ASAG2024`, `data_source == "SAF"`).

## Why this dataset (vs Mohler)

- Mohler gold was **holistic and lenient** vs a one-line reference; SCALES grades
  atomically against evidenced concepts → systematic underscoring / bad
  calibration signal (`WAVE5_REAL1_REPORT.md`).
- SAF grades are **fractional credits already aligned to a long reference**
  (0.25 / 0.375 / 0.5 / … / 1.0). Better for testing whether SCALES matches
  reference-based human marking.
- Same TCP domain as Wave 3, but **real student text** (breaks synthetic
  circularity).

## Rubric design (Mohler lesson applied)

All four concepts are **asked for by the stem** (phases + how cwnd/ss_thresh
change). No “implied locate the node” / “mention BST property” traps.

Rebuild with `python scripts/build_saf_pack.py` (or `--full` for all 65).

## Known risks (read before approving)

1. **Rubric is ours**, not the original course sheet — edit `exam.json` if the
   mark split disagrees with how you would mark.
2. **No true zero** in this SAF question (lowest human grade 0.25 → 1.25/5).
   Band mix is **7 high / 7 mid / 6 mid_low / 0 low**. False-ACCEPT safety is
   weaker; use mid_low misses and DEFER behaviour as the main signals.
3. Gold ranges are ±0.5 around `normalized_grade × 5` (single score, not two
   graders).
4. Concept-level gold still does not exist — judge concepts in SHRR / explain UI.

## Approve checklist

- [ ] Question / reference / rubric look exam-realistic
- [ ] Spot-check 5 gold ranges vs answer text (esp. mid_low vs high)
- [ ] CERA concepts human-checked after extract
- [ ] Reply **approve Q-REAL2** to run live grading
      (~20 students × ~4 concepts ≈ ~80 CGR calls on Gemini Flash-Lite)

## After approval

```bash
cd scales_v3
python scripts/run_pipeline.py grade \
  --exam-json data/e2e_eval/wave5_real/saf_tcp_congestion/exam.json
python scripts/metrics_ledger.py \
  --exam-dir data/exams/e2e_wave5_saf_tcp_congestion \
  --gold data/e2e_eval/wave5_real/saf_tcp_congestion/gold_labels.json \
  --run-id wave5_real2_saf_tcp_v1 \
  --notes "SAF TCP congestion (stratified n=20)"
```
