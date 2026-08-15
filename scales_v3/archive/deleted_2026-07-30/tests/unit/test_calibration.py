"""Unit tests for pre-grade calibration (mocked CGR)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from scales.models.cqa import CQATuple
from scales.models.exam import QuestionInput, StudentAnswer
from scales.models.grading import CGRResult, Verdict
from scales.modules.calibration import run_pregrade_calibration
from scales.modules.exceptions import CERAValidationError


def _cqa(cid: str = "Q1_C1") -> CQATuple:
    return CQATuple(
        concept_id=cid,
        question_id="Q1",
        knowledge_point="kp",
        marks=1,
        evidence_facets=["kp"],
        expected_keywords=["kp"],
    )


def _question(*texts: str) -> QuestionInput:
    return QuestionInput(
        question_id="Q1",
        question_text="Q?",
        reference_answer="Ref",
        rubric="1 mark",
        total_marks=1,
        student_answers=[
            StudentAnswer(student_id=f"S{i}", answer_text=text) for i, text in enumerate(texts)
        ],
    )


def _result(student_id: str, concept_id: str, verdict: Verdict) -> CGRResult:
    return CGRResult(
        student_id=student_id,
        concept_id=concept_id,
        verdict=verdict,
        marks_awarded=0.0 if verdict == Verdict.ABSENT else 1.0,
        evidence_span="" if verdict == Verdict.ABSENT else "kp",
        reasoning="mock",
    )


@pytest.mark.asyncio
async def test_calibration_warns_on_majority_absent():
    cgr = MagicMock()
    cgr.grade_concept = AsyncMock(
        side_effect=lambda **kw: _result(kw["student_id"], kw["cqa"].concept_id, Verdict.ABSENT)
    )
    q = _question(
        "long enough answer for student zero here",
        "another long enough answer here",
    )
    gold = [
        {"student_id": "S0", "expected_band": "high"},
        {"student_id": "S1", "expected_band": "high"},
    ]
    report = await run_pregrade_calibration(cgr, [_cqa()], q, n=2, gold_labels=gold, strict=False)
    assert report["warnings"]
    assert "Q1_C1" in report["flags"]


@pytest.mark.asyncio
async def test_calibration_strict_raises():
    cgr = MagicMock()
    cgr.grade_concept = AsyncMock(
        side_effect=lambda **kw: _result(kw["student_id"], kw["cqa"].concept_id, Verdict.ABSENT)
    )
    q = _question(
        "long enough answer for student zero here",
        "another long enough answer here",
    )
    gold = [
        {"student_id": "S0", "expected_band": "high"},
        {"student_id": "S1", "expected_band": "high"},
    ]
    with pytest.raises(CERAValidationError, match="calibration failed"):
        await run_pregrade_calibration(cgr, [_cqa()], q, n=2, gold_labels=gold, strict=True)


@pytest.mark.asyncio
async def test_calibration_ok_when_full():
    cgr = MagicMock()
    cgr.grade_concept = AsyncMock(
        side_effect=lambda **kw: _result(kw["student_id"], kw["cqa"].concept_id, Verdict.FULL)
    )
    q = _question("long enough answer for student zero here")
    report = await run_pregrade_calibration(cgr, [_cqa()], q, n=1, strict=False)
    assert report["warnings"] == []
