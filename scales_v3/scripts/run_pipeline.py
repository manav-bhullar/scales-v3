#!/usr/bin/env python3
"""CLI entry for SCALES grading pipeline (Sprint 5).

Examples:
  python scripts/run_pipeline.py grade --exam-json path/to/exam.json
  python scripts/run_pipeline.py status --exam-id exam_abc
  python scripts/run_pipeline.py review --exam-id exam_abc \\
      --student STU001 --concept Q1_C1 --verdict FULL --marks 1.0
  python scripts/run_pipeline.py finalize --exam-id exam_abc
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _build_pipeline(exam_id: str | None = None):
    from scales.config import get_settings
    from scales.pipeline import GradingPipeline
    from scales.services.llm_client import LLMClient
    from scales.services.nli_service import NLIService

    settings = get_settings()
    llm = LLMClient(settings.llm)
    nli = NLIService(settings.nli.model_name, device=settings.nli.device)
    return GradingPipeline(llm, nli, settings=settings, exam_id=exam_id)


async def cmd_grade(args: argparse.Namespace) -> int:
    from scales.models.exam import ExamInput

    path = Path(args.exam_json)
    payload = json.loads(path.read_text(encoding="utf-8"))
    exam = ExamInput.model_validate(payload.get("exam", payload))
    gold_labels = None
    if args.gold_json:
        gold_path = Path(args.gold_json)
        gold_doc = json.loads(gold_path.read_text(encoding="utf-8"))
        gold_labels = gold_doc.get("gold_labels", gold_doc)
    pipeline = _build_pipeline(exam.exam_id)
    result = await pipeline.run_grading_phase(
        exam,
        resume=not args.no_resume,
        calibrate=not args.no_calibrate,
        calibrate_strict=args.calibrate_strict,
        calibrate_n=args.calibrate_n,
        gold_labels=gold_labels,
    )
    print(json.dumps(result.status.model_dump(mode="json") if result.status else {}, indent=2))
    print(f"Deferred items: {result.deferred_count}")
    print(f"Exam store: data/exams/{exam.exam_id}/")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    pipeline = _build_pipeline(args.exam_id)
    pipeline.load_from_store(args.exam_id)
    status = pipeline.get_grading_status()
    print(json.dumps(status.model_dump(mode="json"), indent=2))
    queue = pipeline.get_review_queue()
    if queue:
        print(f"\nReview queue ({len(queue)}):")
        for item in queue:
            print(
                f"  - {item.student_id} / {item.concept_id}: "
                f"{item.system_verdict.value} ({item.system_marks}) — {item.defer_reason[:80]}"
            )
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    from scales.models.grading import Verdict

    pipeline = _build_pipeline(args.exam_id)
    pipeline.load_from_store(args.exam_id)
    result = pipeline.submit_correction(
        student_id=args.student,
        concept_id=args.concept,
        teacher_verdict=Verdict(args.verdict),
        teacher_marks=float(args.marks),
        teacher_comment=args.comment or "",
    )
    print(json.dumps(result.model_dump(mode="json"), indent=2, default=str))
    return 0


def cmd_finalize(args: argparse.Namespace) -> int:
    pipeline = _build_pipeline(args.exam_id)
    pipeline.load_from_store(args.exam_id)
    result = pipeline.run_review_phase()
    print(json.dumps(result.status.model_dump(mode="json") if result.status else {}, indent=2))
    for fr in result.final_results:
        print(f"{fr.student_id}: {fr.final_score}/{fr.total_marks} trust={fr.overall_trust:.2f}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SCALES v3 grading pipeline CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_grade = sub.add_parser("grade", help="Run CERA→CGR→CBTE grading phase")
    p_grade.add_argument("--exam-json", required=True, help="Path to ExamInput JSON")
    p_grade.add_argument("--no-resume", action="store_true", help="Ignore prior grading JSON")
    p_grade.add_argument(
        "--no-calibrate",
        action="store_true",
        help="Skip warn-only pre-grade CQA smoke (default: run calibration)",
    )
    p_grade.add_argument(
        "--calibrate-strict",
        action="store_true",
        help="Abort grading if calibration flags majority-ABSENT concepts",
    )
    p_grade.add_argument(
        "--calibrate-n",
        type=int,
        default=2,
        help="Number of sample answers for pre-grade calibration (default 2)",
    )
    p_grade.add_argument(
        "--gold-json",
        default="",
        help="Optional gold_labels.json to prefer high-band students for calibration",
    )
    p_grade.set_defaults(func=lambda a: asyncio.run(cmd_grade(a)))

    p_status = sub.add_parser("status", help="Show grading/review status")
    p_status.add_argument("--exam-id", required=True)
    p_status.set_defaults(func=cmd_status)

    p_review = sub.add_parser("review", help="Submit one teacher correction")
    p_review.add_argument("--exam-id", required=True)
    p_review.add_argument("--student", required=True)
    p_review.add_argument("--concept", required=True)
    p_review.add_argument("--verdict", required=True, choices=["FULL", "PARTIAL", "ABSENT", "INCORRECT"])
    p_review.add_argument("--marks", required=True, type=float)
    p_review.add_argument("--comment", default="")
    p_review.set_defaults(func=cmd_review)

    p_fin = sub.add_parser("finalize", help="Aggregate finals after review is complete")
    p_fin.add_argument("--exam-id", required=True)
    p_fin.set_defaults(func=cmd_finalize)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
