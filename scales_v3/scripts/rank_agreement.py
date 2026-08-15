"""Strictness-invariant checks: does SCALES *rank* students like the humans?

MAE punishes a calibration gap (lenient human vs strict rubric) even when the
system's ordering is perfect. Rank correlation ignores the offset and asks the
question that actually matters for a grading engine: did it separate strong
answers from weak ones?
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
EXAM = PROJECT / "data/exams/e2e_wave5_mohler_bst_delete"
GOLD = PROJECT / "data/e2e_eval/wave5_real/mohler_bst_delete/gold_labels.json"


def rank(values: list[float]) -> list[float]:
    """Average ranks, ties shared."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = sum((x - ma) ** 2 for x in a) ** 0.5
    db = sum((y - mb) ** 2 for y in b) ** 0.5
    return num / (da * db) if da and db else 0.0


def spearman(a: list[float], b: list[float]) -> float:
    return pearson(rank(a), rank(b))


def kendall_tau(a: list[float], b: list[float]) -> float:
    n = len(a)
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            sa = (a[i] > a[j]) - (a[i] < a[j])
            sb = (b[i] > b[j]) - (b[i] < b[j])
            if sa * sb > 0:
                conc += 1
            elif sa * sb < 0:
                disc += 1
    total = conc + disc
    return (conc - disc) / total if total else 0.0


def main() -> None:
    g = json.loads((EXAM / "grading_results.json").read_text(encoding="utf-8"))
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    gold_by = {x["student_id"]: x for x in gold["gold_labels"]}

    by_stu: dict[str, float] = defaultdict(float)
    core_by_stu: dict[str, float] = defaultdict(float)
    for r in g["cgr_results"]:
        by_stu[r["student_id"]] += float(r["marks_awarded"])
        if r["concept_id"] in ("Q1_C2", "Q1_C3"):
            core_by_stu[r["student_id"]] += float(r["marks_awarded"])

    sids = sorted(by_stu)
    ours = [by_stu[s] for s in sids]
    core = [core_by_stu[s] for s in sids]
    human = [
        (gold_by[s]["expected_score_range"][0] + gold_by[s]["expected_score_range"][1]) / 2
        for s in sids
    ]

    print(f"n = {len(sids)} students\n")
    print("Does SCALES ORDER students like the humans did?")
    print(
        f"  all 4 concepts : Spearman {spearman(ours, human):+.2f} | Kendall {kendall_tau(ours, human):+.2f}"
    )
    print(
        f"  C2+C3 only     : Spearman {spearman(core, human):+.2f} | Kendall {kendall_tau(core, human):+.2f}"
    )

    print("\nFor scale, absolute-score agreement (what we measured before):")
    mae = sum(abs(o - h) for o, h in zip(ours, human)) / len(ours)
    print(f"  MAE all 4 concepts: {mae:.2f} marks")

    print("\nTop / bottom by each grader (all-4 scoring):")
    ranked_ours = sorted(sids, key=lambda s: -by_stu[s])
    ranked_human = sorted(sids, key=lambda s: -dict(zip(sids, human))[s])
    print(f"  ours  top5: {ranked_ours[:5]}")
    print(f"  human top5: {ranked_human[:5]}")
    print(f"  ours  bot5: {ranked_ours[-5:]}")
    print(f"  human bot5: {ranked_human[-5:]}")


if __name__ == "__main__":
    main()
