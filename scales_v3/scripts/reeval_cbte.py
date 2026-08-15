"""Re-run CBTE only on saved CGR results (no new LLM calls).

Usage (from scales_v3/):
  python scripts/reeval_cbte.py --exam-id e2e_wave2_tcp_handshake_groq
  python scripts/reeval_cbte.py --exam-id e2e_wave2_tcp_handshake_groq --no-nli
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from scales.config import get_settings
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult
from scales.modules.cbte import CBTEModule, apply_cohort_absent_audit
from scales.services.nli_service import NLIService

PROJECT = Path(__file__).resolve().parents[1]


def _load_exam_bundle(exam_id: str) -> tuple[dict, list[CQATuple], dict[str, str]]:
    exam_dir = PROJECT / "data" / "exams" / exam_id
    grading = json.loads((exam_dir / "grading_results.json").read_text(encoding="utf-8"))
    cqas = [
        CQATuple.model_validate(c)
        for c in json.loads((exam_dir / "cqa_tuples.json").read_text(encoding="utf-8"))[
            "cqa_tuples"
        ]
    ]
    answers = {
        a["student_id"]: a["answer_text"]
        for a in json.loads((exam_dir / "student_answers.json").read_text(encoding="utf-8"))[
            "student_answers"
        ]
    }
    return grading, cqas, answers


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline CBTE re-eval on saved CGR results")
    parser.add_argument("--exam-id", required=True)
    parser.add_argument(
        "--no-nli",
        action="store_true",
        help="Skip NLI load (Tier 2 scores as 0; useful for Signal-1-only checks)",
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="Optional output dir (default: data/e2e_eval/<wave or exam_id>/)",
    )
    args = parser.parse_args()

    grading, cqas, answers = _load_exam_bundle(args.exam_id)
    cqa_map = {c.concept_id: c for c in cqas}
    settings = get_settings()

    nli = None
    if not args.no_nli:
        nli = NLIService(
            model_name=settings.nli.model_name,
            device=settings.nli.device,
        )
    cbte = CBTEModule(nli_service=nli, settings=settings)

    items: list[tuple[CGRResult, str, CQATuple]] = []
    for raw in grading["cgr_results"]:
        cgr = CGRResult.model_validate(raw)
        cqa = cqa_map[cgr.concept_id]
        items.append((cgr, answers[cgr.student_id], cqa))

    results = cbte.evaluate_batch(items)

    cgr_only = [cgr for cgr, _answer, _cqa in items]
    flipped_by_audit = apply_cohort_absent_audit(cgr_only, results, settings.cbte)
    if flipped_by_audit:
        print(
            f"Cohort audit escalated {len(flipped_by_audit)} ABSENT auto-accepts "
            "to DEFER (see per-concept warnings above)."
        )

    # Compare old vs new decisions
    old_by_key = {(r["student_id"], r["concept_id"]): r for r in grading["cbte_results"]}
    flips: list[dict] = []
    defer_before = 0
    defer_after = 0
    false_defer_good = []  # FULL+DEFER on STU_GOOD / STU_GOOD_ALT

    new_cbte = []
    for r in results:
        key = (r.student_id, r.concept_id)
        old = old_by_key[key]
        if old["decision"] == "DEFER":
            defer_before += 1
        if r.decision.value == "DEFER":
            defer_after += 1
        if old["decision"] != r.decision.value or old["tier_resolved"] != r.tier_resolved:
            flips.append(
                {
                    "student_id": r.student_id,
                    "concept_id": r.concept_id,
                    "old_decision": old["decision"],
                    "new_decision": r.decision.value,
                    "old_tier": old["tier_resolved"],
                    "new_tier": r.tier_resolved,
                    "old_reason": old["reason"],
                    "new_reason": r.reason,
                    "signal_1": r.signal_1_evidence_verified,
                }
            )
        cgr_raw = next(
            x
            for x in grading["cgr_results"]
            if x["student_id"] == r.student_id and x["concept_id"] == r.concept_id
        )
        if (
            r.student_id in ("STU_GOOD", "STU_GOOD_ALT")
            and cgr_raw["verdict"] == "FULL"
            and r.decision.value == "DEFER"
            and r.concept_id in ("Q1_C3", "Q1_C4")
        ):
            false_defer_good.append(f"{r.student_id}/{r.concept_id}")
        new_cbte.append(r.model_dump(mode="json"))

    out_dir = Path(args.out_dir) if args.out_dir else PROJECT / "data" / "e2e_eval" / "wave2"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "exam_id": args.exam_id,
        "reeval_at": stamp,
        "nli_enabled": not args.no_nli,
        "defer_before": defer_before,
        "defer_after": defer_after,
        "flips": flips,
        "false_defer_good_c3_c4": false_defer_good,
        "cbte_results": new_cbte,
    }
    out_json = out_dir / "cbte_reeval.json"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Wave 2 CBTE re-eval (Signal-1 fix)",
        "",
        f"- Exam: `{args.exam_id}`",
        f"- NLI: {'on' if not args.no_nli else 'off'}",
        f"- DEFER before → after: **{defer_before} → {defer_after}**",
        f"- Decision/tier flips: **{len(flips)}**",
        f"- False DEFER on STU_GOOD/STU_GOOD_ALT C3/C4: "
        f"**{len(false_defer_good)}** ({', '.join(false_defer_good) or 'none'})",
        "",
        "## Flips",
        "",
    ]
    if not flips:
        lines.append("(none)")
    else:
        for f in flips:
            lines.append(
                f"- `{f['student_id']}/{f['concept_id']}`: "
                f"{f['old_decision']}(t{f['old_tier']}) → {f['new_decision']}(t{f['new_tier']}) "
                f"| sig1={f['signal_1']}"
            )
            lines.append(f"  - old: {f['old_reason']}")
            lines.append(f"  - new: {f['new_reason']}")
    report = out_dir / "WAVE2_SIGNAL1_REEVAL.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_json}")
    print(f"Wrote {report}")
    print(f"DEFER {defer_before}->{defer_after}; false_defer_good_c3_c4={len(false_defer_good)}")


if __name__ == "__main__":
    main()
