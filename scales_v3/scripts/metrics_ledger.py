"""Compute E2E metrics and append one row to the research ledger.

Reads grading_results (+ optional CBTE override) and gold_labels.

Usage (from scales_v3/):
  python scripts/metrics_ledger.py \\
    --exam-dir data/exams/e2e_wave2_tcp_handshake_groq \\
    --gold data/e2e_eval/wave2/gold_labels.json \\
    --run-id wave2_post_signal1 \\
    --cbte-override data/e2e_eval/wave2/cbte_reeval.json \\
    --notes "offline CBTE after evidence-verify fix"
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = PROJECT / "data" / "e2e_eval" / "METRICS_LEDGER.jsonl"


def _provisional_totals(
    cgr_results: list[dict],
    cbte_by_key: dict[tuple[str, str], dict],
) -> dict[str, float]:
    """Sum marks for ACCEPT items only (DEFER marks excluded until review)."""
    totals: dict[str, float] = {}
    for c in cgr_results:
        key = (c["student_id"], c["concept_id"])
        decision = cbte_by_key[key]["decision"]
        if isinstance(decision, str):
            dec = decision
        else:
            dec = decision  # already str from json
        if dec == "ACCEPT":
            totals[c["student_id"]] = totals.get(c["student_id"], 0.0) + float(
                c["marks_awarded"]
            )
        else:
            totals.setdefault(c["student_id"], totals.get(c["student_id"], 0.0))
    # Ensure every student appears
    for c in cgr_results:
        totals.setdefault(c["student_id"], 0.0)
    return totals


def compute_metrics(
    grading: dict[str, Any],
    gold: dict[str, Any],
    cbte_results: list[dict] | None = None,
) -> dict[str, Any]:
    cgr = grading["cgr_results"]
    cbte = cbte_results if cbte_results is not None else grading["cbte_results"]
    cbte_by_key = {(r["student_id"], r["concept_id"]): r for r in cbte}
    cgr_by_key = {(r["student_id"], r["concept_id"]): r for r in cgr}

    n = len(cbte)
    n_defer = sum(1 for r in cbte if r["decision"] == "DEFER")
    defer_rate = n_defer / n if n else 0.0

    # False DEFER: FULL verdict deferred (system distrusts a confident full credit)
    false_defer = 0
    for r in cbte:
        if r["decision"] != "DEFER":
            continue
        c = cgr_by_key[(r["student_id"], r["concept_id"])]
        if c["verdict"] == "FULL":
            false_defer += 1
    false_defer_rate = false_defer / n if n else 0.0

    # False ACCEPT: ACCEPT with marks>0 on students gold-labeled low band
    low_students = {
        g["student_id"]
        for g in gold["gold_labels"]
        if g.get("expected_band") == "low"
    }
    false_accept = 0
    for r in cbte:
        if r["decision"] != "ACCEPT" or r["student_id"] not in low_students:
            continue
        c = cgr_by_key[(r["student_id"], r["concept_id"])]
        if float(c["marks_awarded"]) > 0:
            false_accept += 1
    false_accept_rate = false_accept / n if n else 0.0

    totals = _provisional_totals(cgr, cbte_by_key)
    gold_by_stu = {g["student_id"]: g for g in gold["gold_labels"]}

    band_hits = 0
    mae_sum = 0.0
    scored = 0
    per_student: list[dict] = []
    for sid, score in sorted(totals.items()):
        g = gold_by_stu.get(sid)
        if not g:
            continue
        lo, hi = g["expected_score_range"]
        mid = (lo + hi) / 2.0
        in_band = lo <= score <= hi
        if in_band:
            band_hits += 1
        mae_sum += abs(score - mid)
        scored += 1
        per_student.append(
            {
                "student_id": sid,
                "provisional_score": score,
                "expected_range": [lo, hi],
                "in_band": in_band,
                "band": g.get("expected_band"),
            }
        )

    return {
        "n_items": n,
        "n_students": scored,
        "defer_count": n_defer,
        "defer_rate": round(defer_rate, 4),
        "false_defer_count": false_defer,
        "false_defer_rate": round(false_defer_rate, 4),
        "false_accept_count": false_accept,
        "false_accept_rate": round(false_accept_rate, 4),
        "band_hit_rate": round(band_hits / scored, 4) if scored else 0.0,
        "mark_mae_vs_band_mid": round(mae_sum / scored, 4) if scored else 0.0,
        "per_student": per_student,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Append E2E metrics to research ledger")
    parser.add_argument("--exam-dir", required=True, help="Path to data/exams/{exam_id}")
    parser.add_argument("--gold", required=True, help="Path to gold_labels.json")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--cbte-override", default="", help="Optional cbte_reeval.json")
    parser.add_argument("--notes", default="")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    args = parser.parse_args()

    exam_dir = Path(args.exam_dir)
    if not exam_dir.is_absolute():
        exam_dir = PROJECT / exam_dir
    gold_path = Path(args.gold)
    if not gold_path.is_absolute():
        gold_path = PROJECT / gold_path

    grading = json.loads((exam_dir / "grading_results.json").read_text(encoding="utf-8"))
    gold = json.loads(gold_path.read_text(encoding="utf-8"))

    cbte_override = None
    if args.cbte_override:
        ov = Path(args.cbte_override)
        if not ov.is_absolute():
            ov = PROJECT / ov
        payload = json.loads(ov.read_text(encoding="utf-8"))
        cbte_override = payload["cbte_results"]

    metrics = compute_metrics(grading, gold, cbte_results=cbte_override)
    row = {
        "run_id": args.run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "exam_id": grading.get("exam_id") or gold.get("exam_id"),
        "notes": args.notes,
        "cbte_override": bool(args.cbte_override),
        **{k: v for k, v in metrics.items() if k != "per_student"},
        "per_student": metrics["per_student"],
    }

    ledger_path = Path(args.ledger)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")

    print(json.dumps({k: row[k] for k in row if k != "per_student"}, indent=2))
    print(f"Appended -> {ledger_path}")


if __name__ == "__main__":
    main()
