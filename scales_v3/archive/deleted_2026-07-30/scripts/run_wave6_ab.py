#!/usr/bin/env python3
"""Grade Wave6 coarse packs (nested + flat) and write comparison summary.

Usage (from scales_v3/):
  .venv/bin/python scripts/run_wave6_ab.py
  .venv/bin/python scripts/run_wave6_ab.py --only Q-BURST
  .venv/bin/python scripts/run_wave6_ab.py --arch nested
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

PACK_ROOT = PROJECT / "data/e2e_eval/wave5_real/saf_wave6_picked/wave6_coarse_n20"

QUESTIONS = [
    ("Q-CONN", "conn_oriented_vs_less"),
    ("Q-DLL3", "dll_service_classes"),
    ("Q-ASYNC", "async_vs_sync_dll"),
    ("Q-BURST", "frame_bursting"),
]


async def grade_one(exam_path: Path, gold_path: Path, *, no_calibrate: bool) -> str:
    from scales.config import get_settings
    from scales.models.exam import ExamInput
    from scales.pipeline import GradingPipeline
    from scales.services.llm_client import LLMClient
    from scales.services.nli_service import NLIService

    payload = json.loads(exam_path.read_text(encoding="utf-8"))
    exam = ExamInput.model_validate(payload["exam"])
    gold_doc = json.loads(gold_path.read_text(encoding="utf-8"))
    gold_labels = gold_doc.get("gold_labels", [])

    settings = get_settings()
    llm = LLMClient(settings.llm)
    nli = NLIService(settings.nli.model_name, device=settings.nli.device)
    pipeline = GradingPipeline(llm, nli, settings=settings, exam_id=exam.exam_id)
    result = await pipeline.run_grading_phase(
        exam,
        resume=False,
        calibrate=not no_calibrate,
        calibrate_strict=False,
        calibrate_n=2,
        gold_labels=gold_labels,
    )
    print(
        f"DONE {exam.exam_id}: graded={len(result.status.graded_students) if result.status else '?'} "
        f"deferred={result.deferred_count}"
    )
    return exam.exam_id


def score_exam(exam_id: str, gold_path: Path) -> dict:
    store = PROJECT / "data/exams" / exam_id
    grades = json.loads((store / "grading_results.json").read_text())
    gold = {g["student_id"]: g for g in json.loads(gold_path.read_text())["gold_labels"]}
    cqas = json.loads((store / "cqa_tuples.json").read_text()).get("cqa_tuples", [])
    by = defaultdict(dict)
    for r in grades["cgr_results"]:
        by[r["student_id"]][r["concept_id"]] = r
    scores = {sid: sum(float(by[sid][c]["marks_awarded"]) for c in by[sid]) for sid in by}
    errs, hit, over, under = [], 0, 0, 0
    for sid, sys in scores.items():
        g = gold[sid]
        human = float(g.get("human_score", g.get("human_score_3", 0)))
        lo, hi = g["expected_score_range"]
        errs.append(abs(sys - human))
        if lo <= sys <= hi:
            hit += 1
        elif sys > hi:
            over += 1
        else:
            under += 1
    defers = sum(1 for r in grades["cbte_results"] if r["decision"] == "DEFER")
    return {
        "exam_id": exam_id,
        "n_concepts": len(cqas),
        "concepts": [
            {
                "id": c["concept_id"],
                "marks": c["marks"],
                "mode": c.get("evidence_mode"),
                "facets": c.get("evidence_facets"),
                "kp": c["knowledge_point"],
                "rid": c.get("rubric_item_id"),
            }
            for c in cqas
        ],
        "mae": round(sum(errs) / len(errs), 4) if errs else None,
        "band_hit": hit,
        "n": len(scores),
        "over": over,
        "under": under,
        "defers": defers,
        "scores": scores,
    }


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default="", help="Q-CONN|Q-DLL3|Q-ASYNC|Q-BURST")
    parser.add_argument("--arch", choices=["both", "nested", "flat"], default="both")
    parser.add_argument("--no-calibrate", action="store_true")
    args = parser.parse_args()

    jobs = []
    for key, folder in QUESTIONS:
        if args.only and key != args.only:
            continue
        folder_path = PACK_ROOT / folder
        gold = folder_path / "gold_labels.json"
        if args.arch in ("both", "nested"):
            jobs.append((key, "nested", folder_path / "exam_nested.json", gold))
        if args.arch in ("both", "flat"):
            jobs.append((key, "flat", folder_path / "exam_flat.json", gold))

    summary: dict = {"runs": []}
    for key, arch, exam_path, gold in jobs:
        print(f"\n===== GRADING {key} / {arch} =====")
        exam_id = await grade_one(exam_path, gold, no_calibrate=args.no_calibrate)
        metrics = score_exam(exam_id, gold)
        metrics["question_key"] = key
        metrics["architecture"] = arch
        summary["runs"].append(metrics)
        print(
            f"  MAE={metrics['mae']} band_hit={metrics['band_hit']}/{metrics['n']} "
            f"OVER={metrics['over']} UNDER={metrics['under']} DEFER={metrics['defers']} "
            f"concepts={metrics['n_concepts']}"
        )

    out = PACK_ROOT / "AB_COMPARISON.json"
    out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    # Markdown table
    lines = ["# Wave6 coarse n=20 — nested vs flat\n\n"]
    lines.append("| question | arch | concepts | MAE | band-hit | OVER | UNDER | DEFER |\n")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|\n")
    for r in summary["runs"]:
        lines.append(
            f"| {r['question_key']} | {r['architecture']} | {r['n_concepts']} | "
            f"{r['mae']} | {r['band_hit']}/{r['n']} | {r['over']} | {r['under']} | {r['defers']} |\n"
        )
    md = PACK_ROOT / "AB_COMPARISON.md"
    md.write_text("".join(lines), encoding="utf-8")
    print(f"\nWrote {out}\nWrote {md}")
    print("".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
