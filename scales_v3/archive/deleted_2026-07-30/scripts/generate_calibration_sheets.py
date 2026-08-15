#!/usr/bin/env python3
"""Generate teacher calibration sheets for the 4 locked Wave6 questions.

For each question, reads the already-extracted CQA concepts + already-graded
results (nested exam) and produces a markdown sheet per concept:
  - the concept's target criteria / facets as CERA proposed them
  - award rate across the graded cohort
  - 2-3 sample ABSENT student answers, pre-sorted into a "likely genuine gap"
    vs "likely facet-matching miss" bucket using a cheap heuristic over CGR's
    own reasoning text
  - a plain question for the teacher to confirm/edit: required for full marks?
    what should count as partial?

This does NOT change any grading behavior. It is a paper (well, markdown)
artifact for a human to fill in before we touch rubric weights.

Usage (from scales_v3/):
  .venv/bin/python scripts/generate_calibration_sheets.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
BASE = PROJECT / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20"

QUESTIONS = [
    {"key": "Q-CONN", "folder": "conn_oriented_vs_less", "exam_id": "e2e_wave6_conn_n20_nested"},
    {"key": "Q-DLL3", "folder": "dll_service_classes", "exam_id": "e2e_wave6_dll3_n20_nested"},
    {"key": "Q-ASYNC", "folder": "async_vs_sync_dll", "exam_id": "e2e_wave6_async_n20_nested"},
    {"key": "Q-BURST", "folder": "frame_bursting", "exam_id": "e2e_wave6_burst_n20_nested"},
]


# NOTE: an earlier version of this script tried to auto-classify ABSENT
# reasoning text into "genuine gap" vs "facet-matching gap" (Cause A vs B)
# using a regex over phrases like "describes X but does not mention Y".
# Tested against ASYNC's trade-off concept (where we already know from manual
# reading that the gap is genuine, Cause A) it produced 12/12 false positives
# labeled "B" — the pattern can't distinguish "same idea, different words"
# from "answered a completely different sub-question". Removed rather than
# shipped with false confidence; every ABSENT sample below is shown as-is for
# a human to read instead of an unreliable auto-guess.
def has_descriptive_reasoning(reasoning: str) -> bool:
    """True if CGR's reasoning describes *some* alternate content (worth a read)."""
    return bool(
        re.search(
            r"\b(discusses?|argues?|focuses? on|describes?|mentions?)\b", reasoning, re.IGNORECASE
        )
    )


def load_question(spec: dict) -> dict:
    folder = BASE / spec["folder"]
    exam = json.loads((folder / "exam_nested.json").read_text())["exam"]
    q = exam["questions"][0]
    cqa = json.loads(Path(PROJECT / f"data/exams/{spec['exam_id']}/cqa_tuples.json").read_text())
    gr = json.loads(
        Path(PROJECT / f"data/exams/{spec['exam_id']}/grading_results.json").read_text()
    )
    answers = {a["student_id"]: a["answer_text"] for a in q["student_answers"]}
    gold = json.loads((folder / "gold_labels.json").read_text())["gold_labels"]
    gold_by = {g["student_id"]: g for g in gold}
    return {
        "question": q,
        "cqa": cqa["cqa_tuples"],
        "cgr": gr["cgr_results"],
        "answers": answers,
        "gold_by": gold_by,
    }


def build_sheet(spec: dict, data: dict) -> str:
    q = data["question"]
    cqa_list = data["cqa"]
    by_concept: dict[str, list[dict]] = {}
    for r in data["cgr"]:
        by_concept.setdefault(r["concept_id"], []).append(r)

    lines: list[str] = []
    lines.append(f"# Teacher calibration sheet — {spec['key']}")
    lines.append("")
    lines.append("This does not change grading. Please read each concept below and answer the")
    lines.append("question in **bold**. Your answers will be used to correct concept weights")
    lines.append("and/or facet definitions, not to add a new scoring rule engine.")
    lines.append("")
    lines.append(f"## Question ({q['total_marks']} marks)")
    lines.append(q["question_text"])
    lines.append("")
    lines.append("## Reference answer")
    lines.append(q["reference_answer"])
    lines.append("")
    lines.append("## Rubric as given")
    lines.append(q["rubric"])
    lines.append("")

    for cqa in cqa_list:
        cid = cqa["concept_id"]
        results = by_concept.get(cid, [])
        n = len(results)
        full = sum(1 for r in results if r["verdict"] == "FULL")
        partial = sum(1 for r in results if r["verdict"] == "PARTIAL")
        absent = sum(1 for r in results if r["verdict"] in ("ABSENT", "INCORRECT"))
        award_rate = (
            round(sum(r["marks_awarded"] for r in results) / (n * cqa["marks"]), 3)
            if n and cqa["marks"]
            else 0.0
        )

        lines.append(f"---\n## Concept `{cid}` — {cqa['knowledge_point']} ({cqa['marks']} marks)")
        lines.append(f"- Rubric item: `{cqa.get('rubric_item_id') or '(flat)'}`")
        lines.append(f"- CERA's target criteria: _{cqa['target_criteria']}_")
        lines.append(f"- CERA's evidence facets: {cqa['evidence_facets']}")
        lines.append(
            f"- Award rate across cohort: **{award_rate * 100:.0f}%** (FULL={full} PARTIAL={partial} ABSENT/INCORRECT={absent} / n={n})"
        )
        lines.append("")

        absent_rows = [
            r for r in results if r["verdict"] in ("ABSENT", "INCORRECT") and r.get("reasoning")
        ]

        if absent_rows:
            lines.append(
                '> No reliable auto-classifier for "genuine gap vs. facet-matching miss" '
                "(tested and rejected, see script header) — please read these and judge yourself."
            )
            lines.append("")
            lines.append("Sample ABSENT/INCORRECT answers:")
            for r in absent_rows[:3]:
                sid = r["student_id"]
                ans = data["answers"].get(sid, "")
                gold = data["gold_by"].get(sid, {})
                lines.append(f"- `{sid}` (human gold={gold.get('human_score')}/{q['total_marks']})")
                lines.append(f'  - answer: "{ans[:220]}"')
                lines.append(f'  - CGR reasoning: "{r["reasoning"][:200]}"')
            lines.append("")

        lines.append(
            "**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**"
        )
        lines.append("Your answer: _____")
        lines.append("")
        lines.append("**Q2 — What should count as PARTIAL credit here, if anything?**")
        lines.append("Your answer: _____")
        lines.append("")
        lines.append(
            "**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**"
        )
        lines.append("Your answer: _____")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    out_dir = BASE / "teacher_calibration"
    out_dir.mkdir(parents=True, exist_ok=True)
    for spec in QUESTIONS:
        data = load_question(spec)
        sheet = build_sheet(spec, data)
        path = out_dir / f"{spec['folder']}.md"
        path.write_text(sheet, encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
