"""Build the Wave 5 real-data pack from the Mohler ASAG dataset (E12.Q09).

Source: nkazi/MohlerASAG (Hugging Face), Mohler et al. 2011 (ACL P11-1076).
Question: "How do you delete a node from a binary search tree?" — 28 real
student answers from a UNT data-structures course, scored 0-10 by two human
graders (score_avg normalized to 0-5).

Gold bands are derived from the REAL grader scores (not LLM judgment):
  expected_score_range = [min(g)/2 - 0.5, max(g)/2 + 0.5] clamped to [0, 5]
  (per-grader scores for E12 are on a 0-10 scale; /2 puts them on 0-5)
Band: high if avg >= 4, low if avg <= 1 (range top clamped to 0.5 only for
true zeros), else mid / mid_low.

Usage (from scales_v3/):
  .venv/Scripts/python.exe scripts/build_mohler_pack.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow.parquet as pq

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "data" / "e2e_eval" / "wave5_real" / "mohler_raw_oe.parquet"
OUT = PROJECT / "data" / "e2e_eval" / "wave5_real" / "mohler_bst_delete"
QID = "E12.Q09"
TOTAL_MARKS = 5

RUBRIC = """Total 5 marks:
1) Locate/find the target node in the BST (search step). (1 mark)
2) Simple case: leaf node — remove it / set parent pointer to null. (1 mark)
3) Replacement rule for an internal node: replace with in-order successor
   (leftmost node of right subtree) OR in-order predecessor (rightmost node
   of left subtree). (2 marks — this is the core of the reference answer)
4) Tree integrity: re-link pointers / BST ordering property still holds after
   deletion (also satisfied by correctly describing the successor removal).
   (1 mark)
Partial credit (0.5) when an idea is present but incomplete or imprecise.
Award 0 for a concept that is absent, or contradicts BST behaviour.
NOTE: original UNT graders scored holistically 0-10 against a one-line
reference; expect calibration tension — human reviewer arbitrates."""


def band_for(avg: float) -> str:
    if avg >= 4.0:
        return "high"
    if avg <= 1.0:
        return "low"
    if avg < 2.5:
        return "mid_low"
    return "mid"


def main() -> None:
    rows = [r for r in pq.read_table(SRC).to_pylist() if r["id"].startswith(QID + ".")]
    rows.sort(key=lambda r: r["id"])
    assert rows, f"no rows for {QID}"

    question = rows[0]["question"].strip()
    reference = rows[0]["instructor_answer"].strip()

    answers = []
    gold = []
    for r in rows:
        sid = "MOH_" + r["id"].rsplit(".", 1)[1]  # MOH_A00 ...
        text = (r["student_answer"] or "").replace("<br>", "\n").strip()
        answers.append({"student_id": sid, "answer_text": text})

        g1, g2 = float(r["score_grader_1"]), float(r["score_grader_2"])
        avg = float(r["score_avg"])  # 0-5 scale
        lo = max(0.0, min(g1, g2) / 2 - 0.5)
        hi = min(float(TOTAL_MARKS), max(g1, g2) / 2 + 0.5)
        band = band_for(avg)
        if band == "low" and avg == 0.0:
            lo, hi = 0.0, 0.5
        gold.append(
            {
                "student_id": sid,
                "expected_band": band,
                "expected_score_range": [round(lo, 2), round(hi, 2)],
                "watch": (f"Real UNT grades: g1={g1}/10 g2={g2}/10 avg={avg}/5"),
            }
        )

    exam = {
        "exam": {
            "exam_id": "e2e_wave5_mohler_bst_delete",
            "subject": "Data Structures (real student answers)",
            "questions": [
                {
                    "question_id": "Q1",
                    "question_text": question,
                    "reference_answer": reference,
                    "rubric": RUBRIC,
                    "total_marks": TOTAL_MARKS,
                    "student_answers": answers,
                }
            ],
        },
        "meta": {
            "wave": 5,
            "question_key": "Q-REAL1",
            "n_students": len(answers),
            "source": (
                "Mohler ASAG dataset (Mohler, Bunescu, Mihalcea 2011, ACL P11-1076), "
                "University of North Texas data-structures course, item E12.Q09. "
                "Retrieved from huggingface.co/datasets/nkazi/MohlerASAG (raw-oe)."
            ),
            "focus": [
                "First REAL student answers (not synthetic) — breaks circularity",
                "Gold bands derived from two human graders' scores",
                "One-line exam-realistic stem; decomposable concept",
            ],
            "note": "Do not live-grade until VALIDATION.md approved",
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "exam.json").write_text(json.dumps(exam, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "gold_labels.json").write_text(
        json.dumps(
            {
                "exam_id": "e2e_wave5_mohler_bst_delete",
                "question_id": "Q1",
                "question_key": "Q-REAL1",
                "total_marks": TOTAL_MARKS,
                "gold_source": "UNT human graders (Mohler 2011), scores normalized 0-5",
                "gold_labels": gold,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}/exam.json ({len(answers)} answers) and gold_labels.json")
    bands = {}
    for g in gold:
        bands[g["expected_band"]] = bands.get(g["expected_band"], 0) + 1
    print("bands:", bands)


if __name__ == "__main__":
    main()
