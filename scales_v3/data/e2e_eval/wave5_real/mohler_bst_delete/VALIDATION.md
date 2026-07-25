# Wave 5 / Q-REAL1 — validation before live grading

**Exam id:** `e2e_wave5_mohler_bst_delete`  
**Question:** "How do you delete a node from a binary search tree?" (5 marks)  
**Students:** **28 REAL answers** — Mohler ASAG dataset (UNT data-structures
course, item E12.Q09; Mohler, Bunescu & Mihalcea 2011, ACL P11-1076;
retrieved from `huggingface.co/datasets/nkazi/MohlerASAG`).

## Why this dataset

- Real undergraduate answers (typos, fragments, half-knowledge, one student
  answered about linked lists) — breaks the synthetic circularity.
- Gold comes from **two human UNT graders** (0–10 each, normalized 0–5), not
  from any LLM.
- Same shape as our smokes: one-line stem, decomposable concept, 0–5 marks.

## Known calibration risks (read before approving)

1. **Rubric is mine, not UNT's.** Original graders scored holistically against
   a one-line reference. My 5-mark rubric splits: find (1) + leaf case (1) +
   replacement rule (2) + tree integrity (1). If you disagree, edit the rubric
   in `exam.json` before grading.
2. **Grader disagreement is real** (up to 5/10 apart on some answers). Gold
   ranges span both graders ±0.5, so bands are wide; band-hit will be a softer
   signal than on synthetic packs.
3. Band mix is top-heavy (15 high / 6 mid / 6 mid_low / 1 low) — real class
   distribution, not our usual 2/2/2/2. False-ACCEPT safety signal is weaker
   (only one true zero); DEFER behaviour on messy text is the main thing this
   pack tests.
4. Concept-level gold does not exist — you said you will judge concepts
   manually in SHRR. That is the plan.

## Approve checklist

- [x] Question/reference/rubric wording OK (edit rubric if you disagree)
- [x] Gold ranges (from real graders) look reasonable — spot-check 5
- [x] CERA concepts human-checked (user: "i have done checking move forward" — 2026-07-25)
- [x] Reply **approve Q-REAL1** to run live grading (28 students ≈ ~112 CGR
      calls on Gemini Flash-Lite)

**Approved:** concepts locked from `cqa_review.json`; grading started 2026-07-25.

## After approval

```powershell
cd scales_v3
python scripts/run_pipeline.py grade --exam-json data/e2e_eval/wave5_real/mohler_bst_delete/exam.json
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave5_mohler_bst_delete `
  --gold data/e2e_eval/wave5_real/mohler_bst_delete/gold_labels.json `
  --run-id wave5_real1_smoke_v1 `
  --notes "First real-data pack (Mohler E12.Q09)"
```
