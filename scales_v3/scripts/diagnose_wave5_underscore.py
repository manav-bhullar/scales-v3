"""Diagnose Wave5 underscoring: rubric/concept design vs architecture.

Tests three scorings against the real UNT human gold:
  A) all 4 locked concepts (what we shipped)
  B) core concepts only (C2 cases + C3 replacement), rescaled to 5
  C) all 4 concepts but DEFERs counted at raw CGR marks (removes queue effect)

If (B) tracks UNT gold far better than (A), the miss is concept/rubric design.
Also reports how many zero-marks were AUTO-ACCEPTED (invisible to teacher)
vs deferred — that part is architectural.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
EXAM = PROJECT / "data/exams/e2e_wave5_mohler_bst_delete"
GOLD = PROJECT / "data/e2e_eval/wave5_real/mohler_bst_delete/gold_labels.json"

g = json.loads((EXAM / "grading_results.json").read_text(encoding="utf-8"))
gold = json.loads(GOLD.read_text(encoding="utf-8"))
gold_by = {x["student_id"]: x for x in gold["gold_labels"]}

cbte = {(r["student_id"], r["concept_id"]): r for r in g["cbte_results"]}
by_stu: dict[str, list[dict]] = defaultdict(list)
for r in g["cgr_results"]:
    by_stu[r["student_id"]].append(r)


def mid(rng: list[float]) -> float:
    return (rng[0] + rng[1]) / 2


rows = []
absent_accepted = 0
absent_deferred = 0
absent_by_concept: dict[str, int] = defaultdict(int)

for sid in sorted(by_stu):
    marks = {}
    for r in by_stu[sid]:
        cid = r["concept_id"]
        marks[cid] = float(r["marks_awarded"])
        t = cbte[(sid, cid)]
        if float(r["marks_awarded"]) == 0.0:
            absent_by_concept[cid] += 1
            if t["decision"] == "ACCEPT":
                absent_accepted += 1
            else:
                absent_deferred += 1

    a_all = sum(marks.values())                      # all 4, raw CGR
    core = marks.get("Q1_C2", 0) + marks.get("Q1_C3", 0)   # 3 marks max
    b_core = core * 5.0 / 3.0                        # rescaled to 5
    gl = gold_by[sid]
    rows.append((sid, a_all, b_core, mid(gl["expected_score_range"]), gl))

def report(name: str, idx: int) -> None:
    err = [abs(r[idx] - r[3]) for r in rows]
    inband = sum(
        1 for r in rows if r[4]["expected_score_range"][0] <= r[idx] <= r[4]["expected_score_range"][1]
    )
    print(f"{name}: MAE vs UNT mid = {sum(err)/len(err):.2f} | in-band {inband}/{len(rows)}")

print("=== Scoring variants vs real UNT gold (28 students) ===")
report("A) all 4 concepts (raw CGR) ", 1)
report("B) core C2+C3 rescaled to 5 ", 2)

print("\n=== Zero-mark visibility (architecture) ===")
print(f"zero-mark concept judgments: {absent_accepted + absent_deferred}")
print(f"  auto-ACCEPTED (teacher never sees): {absent_accepted}")
print(f"  DEFERRED (teacher sees):            {absent_deferred}")
print("\nzero-marks by concept:")
for cid in sorted(absent_by_concept):
    print(f"  {cid}: {absent_by_concept[cid]}/28 students scored 0")

print("\n=== Worst A-vs-gold gaps (per student) ===")
for sid, a, b, m, gl in sorted(rows, key=lambda r: r[3] - r[1], reverse=True)[:6]:
    print(f"{sid}: ours(all4)={a:.1f} ours(core)={b:.1f} UNT_mid={m:.2f} band={gl['expected_band']}")
