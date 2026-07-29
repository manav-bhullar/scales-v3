#!/usr/bin/env python3
"""Build Wave6 coarse-rubric packs (n=20) for nested + flat A/B testing.

Four locked SAF questions; teacher rubrics cut to \"Label (marks)\" only.
Nested exam keeps rubric_items; flat exam clears them (rubric=concept).

Usage (from scales_v3/):
  .venv/bin/python scripts/build_wave6_coarse_packs.py
  .venv/bin/python scripts/build_wave6_coarse_packs.py --n 20
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pyarrow.parquet as pq

PROJECT = Path(__file__).resolve().parents[1]
OUT_ROOT = PROJECT / "data" / "e2e_eval" / "wave5_real" / "saf_wave6_picked" / "wave6_coarse_n20"
CACHE = (
    Path.home()
    / ".cache/huggingface/hub/datasets--Meyerger--ASAG2024"
    / "snapshots/9a7a179de4e227f5e78625bc9ded2d8761f1ff09/train.parquet"
)

# Coarse teacher rubrics — labels + marks only (CERA invents FULL/PARTIAL detail).
QUESTIONS = [
    {
        "key": "Q-CONN",
        "folder": "conn_oriented_vs_less",
        "exam_id_nested": "e2e_wave6_conn_n20_nested",
        "exam_id_flat": "e2e_wave6_conn_n20_flat",
        "total_marks": 5,
        "question_text": (
            "Consider the following scenario: You are browsing the web for a very "
            "specific and important piece of information. However, you are not quite "
            "sure how to find it and adopt an iterative process of refining your query "
            "after every search, depending on the shown results and a skim of the first "
            "few websites. Is it better to use a connection-oriented or connectionless "
            "service for your communication in this scenario? Explain your answer in "
            "1-4 sentences."
        ),
        "rubric": (
            "Total 5 marks:\n"
            "1) Chooses connectionless (1 mark)\n"
            "2) Reasoning for the choice (many partners / short interactions / overhead) (4 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Chooses connectionless",
                "marks": 1.0,
                "atomic": True,
                "description": "Do not subdivide — the choice itself.",
            },
            {
                "rubric_item_id": "R2",
                "label": "Reasoning for the choice",
                "marks": 4.0,
                "atomic": False,
                "description": "MAY SPLIT into partners / short interactions / overhead arguments.",
            },
        ],
    },
    {
        "key": "Q-DLL3",
        "folder": "dll_service_classes",
        "exam_id_nested": "e2e_wave6_dll3_n20_nested",
        "exam_id_flat": "e2e_wave6_dll3_n20_flat",
        "total_marks": 3,
        "question_text": (
            "Name the 3 service classes the Data Link Layer offers and explain "
            "the differences between the classes."
        ),
        "rubric": (
            "Total 3 marks:\n"
            "1) Three DLL service classes named and distinguished (3 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Three DLL service classes named and distinguished",
                "marks": 3.0,
                "atomic": False,
                "description": "MAY SPLIT into the three service classes.",
            },
        ],
    },
    {
        "key": "Q-ASYNC",
        "folder": "async_vs_sync_dll",
        "exam_id_nested": "e2e_wave6_async_n20_nested",
        "exam_id_flat": "e2e_wave6_async_n20_flat",
        "total_marks": 4,
        "question_text": (
            "What is the difference between asynchronous and synchronous "
            "transmission mode in the Data Link Layer."
        ),
        "rubric": (
            "Total 4 marks:\n"
            "1) Framing difference (async start/stop + sync frames/SYN/flag) (2 marks)\n"
            "2) Trade-offs (rates / complexity / synchronization) (2 marks)"
        ),
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Framing difference",
                "marks": 2.0,
                "atomic": False,
                "description": "MAY SPLIT into async framing + sync framing.",
            },
            {
                "rubric_item_id": "R2",
                "label": "Trade-offs",
                "marks": 2.0,
                "atomic": False,
                "description": "MAY SPLIT into async trade-off + sync trade-off.",
            },
        ],
    },
    {
        "key": "Q-BURST",
        "folder": "frame_bursting",
        "exam_id_nested": "e2e_wave6_burst_n20_nested",
        "exam_id_flat": "e2e_wave6_burst_n20_flat",
        "total_marks": 3,
        "question_text": (
            'What is "frame bursting"? Also, give 1 advantage and disadvantage '
            "compared to the carrier extension."
        ),
        "rubric": (
            "Total 3 marks:\n"
            "1) Definition of frame bursting (1.5 marks)\n"
            "2) Advantage and disadvantage vs carrier extension (1.5 marks)"
        ),
        # Definition stays atomic; adv/disadv may split.
        "rubric_items": [
            {
                "rubric_item_id": "R1",
                "label": "Definition of frame bursting",
                "marks": 1.5,
                "atomic": True,
                "description": "Do not subdivide.",
            },
            {
                "rubric_item_id": "R2",
                "label": "Advantage and disadvantage vs carrier extension",
                "marks": 1.5,
                "atomic": False,
                "description": "MAY SPLIT into advantage + disadvantage.",
            },
        ],
    },
]


def band_for(score: float, total: float) -> str:
    frac = score / total if total else 0.0
    if frac >= 0.75:
        return "high"
    if frac <= 0.2:
        return "low"
    if frac < 0.5:
        return "mid_low"
    return "mid"


def stratified_sample(rows: list[dict], n: int, total_marks: float) -> list[dict]:
    """Mix bands: prefer coverage of low/mid/high rather than all imperfect zeros."""
    by: dict[str, list[dict]] = {"low": [], "mid_low": [], "mid": [], "high": []}
    for r in rows:
        text = str(r.get("provided_answer") or "").strip()
        if not text:
            continue
        s = float(r["normalized_grade"]) * total_marks
        by[band_for(s, total_marks)].append(r)
    for b in by:
        # diversify by answer length within band
        by[b].sort(
            key=lambda r: (
                float(r["normalized_grade"]),
                len(str(r["provided_answer"])),
                str(r["provided_answer"]),
            )
        )

    picked: list[dict] = []
    seen: set[str] = set()

    def take(band: str, k: int) -> None:
        for r in by[band]:
            if len([p for p in picked if True]) >= n:
                return
            text = str(r["provided_answer"]).strip()
            if text in seen:
                continue
            seen.add(text)
            picked.append(r)
            k -= 1
            if k <= 0:
                return

    # Target mix for n=20: ~5 low, ~5 mid_low, ~5 mid, ~5 high (clamp to available)
    quotas = {
        "low": max(1, n // 4),
        "mid_low": max(1, n // 4),
        "mid": max(1, n // 4),
        "high": max(1, n - 3 * (n // 4)),
    }
    for band, k in quotas.items():
        before = len(picked)
        take(band, k)
        # if short, leave quota unused

    if len(picked) < n:
        rest = []
        for band in ("mid", "high", "mid_low", "low"):
            rest.extend(by[band])
        for r in rest:
            text = str(r["provided_answer"]).strip()
            if text in seen:
                continue
            seen.add(text)
            picked.append(r)
            if len(picked) >= n:
                break

    picked.sort(key=lambda r: (-float(r["normalized_grade"]), str(r["provided_answer"])))
    return picked[:n]


def build_one(spec: dict, rows: list[dict], n: int) -> None:
    total = float(spec["total_marks"])
    picked = stratified_sample(rows, n, total)
    if len(picked) < n:
        raise SystemExit(f"{spec['key']}: only {len(picked)} answers available")

    ref = str(picked[0]["reference_answer"]).strip()
    answers = []
    gold = []
    for i, r in enumerate(picked):
        sid = f"{spec['key'].replace('-', '')}_{i:02d}"
        text = str(r["provided_answer"] or "").replace("\xa0", " ").strip()
        answers.append({"student_id": sid, "answer_text": text})
        norm = float(r["normalized_grade"])
        score = round(norm * total, 4)
        band = band_for(score, total)
        lo = max(0.0, round(score - 0.5, 2))
        hi = min(total, round(score + 0.5, 2))
        if band == "low":
            lo, hi = 0.0, round(total * 0.2, 2)
        gold.append(
            {
                "student_id": sid,
                "expected_band": band if band != "mid_low" else "mid",
                "expected_score_range": [lo, hi],
                "human_normalized": norm,
                "human_score": score,
                "watch": f"SAF human {norm} → {score}/{total}",
            }
        )

    folder = OUT_ROOT / spec["folder"]
    folder.mkdir(parents=True, exist_ok=True)

    def write_exam(exam_id: str, architecture: str, rubric_items: list) -> Path:
        exam = {
            "exam": {
                "exam_id": exam_id,
                "subject": f"SAF Wave6 coarse — {spec['key']} ({architecture})",
                "questions": [
                    {
                        "question_id": "Q1",
                        "question_text": spec["question_text"],
                        "reference_answer": ref,
                        "rubric": spec["rubric"],
                        "total_marks": int(total) if total == int(total) else int(total),
                        "rubric_items": rubric_items,
                        "student_answers": answers,
                    }
                ],
            },
            "meta": {
                "wave": 6,
                "question_key": spec["key"],
                "architecture": architecture,
                "n_students": len(answers),
                "rubric_style": "coarse_label_marks_only",
            },
        }
        # total_marks must be int in QuestionInput currently — all our totals are ints
        exam["exam"]["questions"][0]["total_marks"] = int(total)
        path = folder / f"exam_{architecture}.json"
        path.write_text(json.dumps(exam, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    nested_path = write_exam(spec["exam_id_nested"], "nested", spec["rubric_items"])
    flat_path = write_exam(spec["exam_id_flat"], "flat", [])

    gold_path = folder / "gold_labels.json"
    gold_path.write_text(
        json.dumps(
            {
                "question_key": spec["key"],
                "total_marks": int(total),
                "gold_source": "SAF ASAG2024 normalized_grade",
                "gold_labels": gold,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    from collections import Counter

    bands = Counter(g["expected_band"] for g in gold)
    print(f"{spec['key']}: n={len(answers)} bands={dict(bands)}")
    print(f"  nested → {nested_path.name} ({spec['exam_id_nested']})")
    print(f"  flat   → {flat_path.name} ({spec['exam_id_flat']})")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=20)
    args = parser.parse_args()

    if not CACHE.exists():
        raise SystemExit(f"ASAG2024 parquet missing: {CACHE}")

    df = pq.read_table(CACHE).to_pandas()
    df = df[df["data_source"] == "SAF"]

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for spec in QUESTIONS:
        g = df[df["question"] == spec["question_text"]].copy()
        if g.empty:
            raise SystemExit(f"No rows for {spec['key']}")
        # cache source slice
        folder = OUT_ROOT / spec["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        g.to_parquet(folder / "source.parquet", index=False)
        build_one(spec, g.to_dict(orient="records"), args.n)

    # Update approved rubrics to coarse form
    approved = {
        "status": "q1_q4_coarse_locked",
        "n_target_per_question": args.n,
        "notes": (
            "Coarse teacher rubrics (label + marks only). Nested uses rubric_items; "
            "flat clears them. Packs under wave6_coarse_n20/."
        ),
        "questions": [
            {
                "key": s["key"],
                "folder": s["folder"],
                "approved": True,
                "question_text": s["question_text"],
                "rubric": s["rubric"],
                "rubric_items": s["rubric_items"],
                "total_marks": s["total_marks"],
            }
            for s in QUESTIONS
        ],
    }
    approved_path = (
        PROJECT
        / "data/e2e_eval/wave5_real/saf_wave6_picked/_approved_rubrics.json"
    )
    # Keep references from existing file if present
    if approved_path.exists():
        old = json.loads(approved_path.read_text())
        old_by_key = {q["key"]: q for q in old.get("questions", [])}
        for q in approved["questions"]:
            if q["key"] in old_by_key and "reference_answer" in old_by_key[q["key"]]:
                q["reference_answer"] = old_by_key[q["key"]]["reference_answer"]
            if q["key"] in old_by_key and "n_available" in old_by_key[q["key"]]:
                q["n_available"] = old_by_key[q["key"]]["n_available"]
    approved_path.write_text(json.dumps(approved, indent=2) + "\n", encoding="utf-8")
    print(f"\nUpdated {approved_path}")
    print(f"Packs at {OUT_ROOT}")


if __name__ == "__main__":
    main()
