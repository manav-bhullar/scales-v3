"""Pre-grade calibration smoke: spot-check CQAs on a few answers before batch.

Warn-only by default. Optional strict mode raises if high-band (or long-answer)
students get ABSENT on a concept — use carefully; gold can be lenient.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from loguru import logger

from scales.models.cqa import CQATuple
from scales.models.exam import QuestionInput, StudentAnswer
from scales.models.grading import Verdict
from scales.modules.cgr import CGRModule
from scales.modules.exceptions import CERAValidationError


def _pick_sample_students(
    students: list[StudentAnswer],
    *,
    n: int,
    gold_by_sid: dict[str, dict[str, Any]] | None,
) -> list[StudentAnswer]:
    """Prefer high/mid gold bands when available; else longest non-empty answers."""
    by_id = {s.student_id: s for s in students}
    ordered: list[StudentAnswer] = []

    if gold_by_sid:
        prefer_bands = ("high", "mid_high", "mid")
        for band in prefer_bands:
            for sid, g in gold_by_sid.items():
                if g.get("expected_band") != band:
                    continue
                stu = by_id.get(sid)
                if stu and stu.answer_text.strip() and stu not in ordered:
                    ordered.append(stu)
                if len(ordered) >= n:
                    return ordered[:n]

    rest = sorted(
        [s for s in students if s.answer_text.strip()],
        key=lambda s: len(s.answer_text),
        reverse=True,
    )
    for stu in rest:
        if stu not in ordered:
            ordered.append(stu)
        if len(ordered) >= n:
            break
    return ordered[:n]


async def run_pregrade_calibration(
    cgr: CGRModule,
    cqa_list: list[CQATuple],
    question: QuestionInput,
    *,
    n: int = 2,
    gold_labels: list[dict[str, Any]] | None = None,
    strict: bool = False,
) -> dict[str, Any]:
    """Grade ``n`` sample answers; return flags. Never mutates batch results.

    Returns dict with keys: sample_students, flags (concept_id → student_ids),
    warnings (list[str]), results (list of per-concept verdicts).
    """
    gold_by_sid = {g["student_id"]: g for g in (gold_labels or []) if "student_id" in g}
    sample = _pick_sample_students(
        question.student_answers, n=max(1, n), gold_by_sid=gold_by_sid or None
    )
    if not sample:
        msg = "Calibration skipped: no non-empty student answers"
        logger.warning(msg)
        return {
            "sample_students": [],
            "flags": {},
            "warnings": [msg],
            "results": [],
        }

    absent_flags: dict[str, list[str]] = defaultdict(list)
    results: list[dict[str, Any]] = []

    logger.info(
        "Pre-grade calibration: sampling {} students {}",
        len(sample),
        [s.student_id for s in sample],
    )

    for student in sample:
        band = (gold_by_sid.get(student.student_id) or {}).get("expected_band", "")
        for cqa in cqa_list:
            gr = await cgr.grade_concept(
                student_id=f"CALIB_{student.student_id}",
                student_answer=student.answer_text,
                cqa=cqa,
                question_text=question.question_text,
            )
            results.append(
                {
                    "student_id": student.student_id,
                    "concept_id": cqa.concept_id,
                    "verdict": gr.verdict.value,
                    "marks_awarded": gr.marks_awarded,
                    "band": band,
                }
            )
            # Flag ABSENT on high/mid gold, or on any long answer when no gold.
            should_flag = gr.verdict == Verdict.ABSENT and (
                band in ("high", "mid_high", "mid")
                or (not gold_by_sid and len(student.answer_text) >= 40)
            )
            if should_flag:
                absent_flags[cqa.concept_id].append(student.student_id)

    warnings: list[str] = []
    for cid, sids in absent_flags.items():
        # Only warn if the same concept failed for a majority of the sample
        if len(sids) >= max(1, (len(sample) + 1) // 2):
            warn = (
                f"Calibration FLAG {cid}: ABSENT on sample {sids} — "
                "review evidence_mode / facets / target_criteria before trusting batch"
            )
            warnings.append(warn)
            logger.warning(warn)

    if not warnings:
        logger.info("Pre-grade calibration OK (no majority-ABSENT concept flags)")

    if strict and warnings:
        raise CERAValidationError(
            "Pre-grade calibration failed (strict mode): " + "; ".join(warnings)
        )

    return {
        "sample_students": [s.student_id for s in sample],
        "flags": {k: v for k, v in absent_flags.items()},
        "warnings": warnings,
        "results": results,
    }
