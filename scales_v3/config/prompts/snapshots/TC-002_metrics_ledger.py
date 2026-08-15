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
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = PROJECT / "data" / "e2e_eval" / "METRICS_LEDGER.jsonl"

# Roadmap pass bar (data/e2e_eval/wave4/README.md).
PASS_BAR_MAX_DEFER_RATE = 0.40


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
            totals[c["student_id"]] = totals.get(c["student_id"], 0.0) + float(c["marks_awarded"])
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
    low_students = {g["student_id"] for g in gold["gold_labels"] if g.get("expected_band") == "low"}
    false_accept = 0
    for r in cbte:
        if r["decision"] != "ACCEPT" or r["student_id"] not in low_students:
            continue
        c = cgr_by_key[(r["student_id"], r["concept_id"])]
        if float(c["marks_awarded"]) > 0:
            false_accept += 1
    false_accept_rate = false_accept / n if n else 0.0

    # Silent zero: ACCEPT + 0 marks on a HIGH-band (GOOD) student.
    # Mid/partial students correctly get ABSENT on concepts they skipped; those
    # must not inflate this counter. The failure mode we care about is CGR
    # collapsing a strong answer to ABSENT (e.g. empty evidence) and CBTE
    # auto-accepting it so a teacher never sees it (Wave4 OS1 GOOD_01).
    high_students = {
        g["student_id"] for g in gold["gold_labels"] if g.get("expected_band") == "high"
    }
    silent_zero = 0
    silent_zero_by_verdict: dict[str, int] = {}
    for r in cbte:
        if r["decision"] != "ACCEPT" or r["student_id"] not in high_students:
            continue
        c = cgr_by_key[(r["student_id"], r["concept_id"])]
        if float(c["marks_awarded"]) > 0:
            continue
        silent_zero += 1
        verdict = c["verdict"]
        silent_zero_by_verdict[verdict] = silent_zero_by_verdict.get(verdict, 0) + 1
    silent_zero_rate = silent_zero / n if n else 0.0

    totals = _provisional_totals(cgr, cbte_by_key)
    gold_by_stu = {g["student_id"]: g for g in gold["gold_labels"]}

    band_hits = 0
    mae_sum = 0.0
    scored = 0
    underscored = 0
    overscored = 0
    zeroed_students: list[str] = []
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
        elif score < lo:
            underscored += 1
        else:
            overscored += 1
        if score == 0.0 and lo > 0.0:
            zeroed_students.append(sid)
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
        "silent_zero_count": silent_zero,
        "silent_zero_rate": round(silent_zero_rate, 4),
        "silent_zero_by_verdict": silent_zero_by_verdict,
        "zeroed_students": zeroed_students,
        "underscored_students": underscored,
        "overscored_students": overscored,
        "band_hit_rate": round(band_hits / scored, 4) if scored else 0.0,
        "mark_mae_vs_band_mid": round(mae_sum / scored, 4) if scored else 0.0,
        "per_student": per_student,
    }


def compute_post_review_metrics(
    grading: dict[str, Any],
    finals: dict[str, Any],
    corrections: dict[str, Any],
    gold: dict[str, Any],
) -> dict[str, Any]:
    """Metrics on FINAL scores after SHRR review (teacher-resolved DEFERs).

    Unlike compute_metrics (provisional, ACCEPT-only), this uses final_score
    from final_results.json, which folds in the resolved/agreed deferred marks.
    """
    cbte = grading["cbte_results"]
    n = len(cbte)
    n_defer = sum(1 for r in cbte if r["decision"] == "DEFER")

    corr_rows = corrections.get("corrections", corrections) if corrections else []
    if isinstance(corr_rows, dict):
        corr_rows = corr_rows.get("corrections", [])
    corr_types: dict[str, int] = {}
    for c in corr_rows:
        t = c.get("correction_type", "?")
        corr_types[t] = corr_types.get(t, 0) + 1

    final_rows = finals.get("final_results", finals if isinstance(finals, list) else [])
    gold_by_stu = {g["student_id"]: g for g in gold["gold_labels"]}

    band_hits = 0
    mae_sum = 0.0
    scored = 0
    per_student: list[dict] = []
    for r in sorted(final_rows, key=lambda x: x["student_id"]):
        sid = r["student_id"]
        g = gold_by_stu.get(sid)
        if not g:
            continue
        score = float(r["final_score"])
        lo, hi = g["expected_score_range"]
        mid = (lo + hi) / 2.0
        in_band = lo <= score <= hi
        band_hits += int(in_band)
        mae_sum += abs(score - mid)
        scored += 1
        per_student.append(
            {
                "student_id": sid,
                "final_score": score,
                "expected_range": [lo, hi],
                "in_band": in_band,
                "band": g.get("expected_band"),
            }
        )

    return {
        "n_items": n,
        "n_students": scored,
        "defer_count": n_defer,
        "defer_rate": round(n_defer / n, 4) if n else 0.0,
        "review_resolved": len(corr_rows),
        "correction_types": corr_types,
        "band_hit_rate": round(band_hits / scored, 4) if scored else 0.0,
        "mark_mae_vs_band_mid": round(mae_sum / scored, 4) if scored else 0.0,
        "per_student": per_student,
    }


def _row_score(row: dict[str, Any]) -> float:
    """Per-student score, whichever phase produced the row."""
    if "provisional_score" in row:
        return float(row["provisional_score"])
    return float(row["final_score"])


def evaluate_pass_bar(
    metrics: dict[str, Any],
    *,
    max_defer_rate: float = PASS_BAR_MAX_DEFER_RATE,
) -> dict[str, Any]:
    """Turn the Wave 4 roadmap pass-bar table into a machine verdict.

    Criteria that need a field the given metrics dict does not carry (e.g.
    false_accept on a post-review row) are reported as not applicable and do
    not affect the overall verdict.
    """
    per_student = metrics.get("per_student", [])
    criteria: list[dict[str, Any]] = []

    def add(
        name: str,
        *,
        applicable: bool,
        passed: bool | None,
        observed: Any,
        limit: Any,
        detail: str,
    ) -> None:
        criteria.append(
            {
                "name": name,
                "applicable": applicable,
                "pass": passed,
                "observed": observed,
                "limit": limit,
                "detail": detail,
            }
        )

    if "false_accept_count" in metrics:
        count = metrics["false_accept_count"]
        add(
            "no_false_accept_on_low",
            applicable=True,
            passed=count == 0,
            observed=count,
            limit=0,
            detail="Credit auto-accepted for a gold-low student.",
        )
    else:
        add(
            "no_false_accept_on_low",
            applicable=False,
            passed=None,
            observed=None,
            limit=0,
            detail="Not computed for this phase.",
        )

    if "silent_zero_count" in metrics:
        count = metrics["silent_zero_count"]
        add(
            "no_silent_zeros",
            applicable=True,
            passed=count == 0,
            observed=count,
            limit=0,
            detail=(
                "Zero marks auto-accepted on a HIGH-band (GOOD) student — "
                "teacher never reviews: "
                f"{metrics.get('silent_zero_by_verdict', {})}"
            ),
        )
    else:
        add(
            "no_silent_zeros",
            applicable=False,
            passed=None,
            observed=None,
            limit=0,
            detail="Not computed for this phase.",
        )

    defer_rate = metrics.get("defer_rate")
    add(
        "defer_rate_within_limit",
        applicable=defer_rate is not None,
        passed=None if defer_rate is None else defer_rate <= max_defer_rate,
        observed=defer_rate,
        limit=max_defer_rate,
        detail="Review queue too large to be practical for a teacher.",
    )

    high = [r for r in per_student if r.get("band") == "high"]
    high_missed = [r["student_id"] for r in high if not r["in_band"]]
    add(
        "high_band_students_in_band",
        applicable=bool(high),
        passed=None if not high else not high_missed,
        observed=high_missed,
        limit=[],
        detail="Strong answers must land in their gold band.",
    )

    middle = [r for r in per_student if r.get("band") not in ("high", "low")]
    any_credit = any(_row_score(r) > 0 for r in middle)
    add(
        "mid_band_not_all_zero",
        applicable=bool(middle),
        passed=None if not middle else any_credit,
        observed=sum(1 for r in middle if _row_score(r) == 0),
        limit=f"< {len(middle)}",
        detail="Every partial answer scored zero — grader is collapsing to ABSENT.",
    )

    failed = [c["name"] for c in criteria if c["applicable"] and not c["pass"]]
    return {"pass": not failed, "failed": failed, "criteria": criteria}


def format_pass_bar(report: dict[str, Any]) -> str:
    lines = ["PASS BAR: " + ("PASS" if report["pass"] else "FAIL")]
    for c in report["criteria"]:
        if not c["applicable"]:
            mark = "-"
        elif c["pass"]:
            mark = "PASS"
        else:
            mark = "FAIL"
        lines.append(f"  [{mark}] {c['name']}: observed={c['observed']} limit={c['limit']}")
        if c["applicable"] and not c["pass"]:
            lines.append(f"         {c['detail']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Append E2E metrics to research ledger")
    parser.add_argument("--exam-dir", required=True, help="Path to data/exams/{exam_id}")
    parser.add_argument("--gold", required=True, help="Path to gold_labels.json")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--cbte-override", default="", help="Optional cbte_reeval.json")
    parser.add_argument("--notes", default="")
    parser.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    parser.add_argument(
        "--post-review",
        action="store_true",
        help="Compute metrics on FINAL scores (after SHRR review) from final_results.json",
    )
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

    if args.post_review:
        finals = json.loads((exam_dir / "final_results.json").read_text(encoding="utf-8"))
        corr_path = exam_dir / "teacher_corrections.json"
        corrections = (
            json.loads(corr_path.read_text(encoding="utf-8")) if corr_path.exists() else {}
        )
        metrics = compute_post_review_metrics(grading, finals, corrections, gold)
        row = {
            "run_id": args.run_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "exam_id": grading.get("exam_id") or gold.get("exam_id"),
            "phase": "post_review",
            "notes": args.notes,
            **{k: v for k, v in metrics.items() if k != "per_student"},
            "per_student": metrics["per_student"],
        }
    else:
        metrics = compute_metrics(grading, gold, cbte_results=cbte_override)
        row = {
            "run_id": args.run_id,
            "timestamp": datetime.now(UTC).isoformat(),
            "exam_id": grading.get("exam_id") or gold.get("exam_id"),
            "phase": "pre_review",
            "notes": args.notes,
            "cbte_override": bool(args.cbte_override),
            **{k: v for k, v in metrics.items() if k != "per_student"},
            "per_student": metrics["per_student"],
        }

    pass_bar = evaluate_pass_bar(metrics)
    row["pass_bar"] = {"pass": pass_bar["pass"], "failed": pass_bar["failed"]}

    ledger_path = Path(args.ledger)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")

    print(json.dumps({k: row[k] for k in row if k != "per_student"}, indent=2))
    print(format_pass_bar(pass_bar))
    print(f"Appended -> {ledger_path}")


if __name__ == "__main__":
    main()
