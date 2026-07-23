"""Unit tests for SHRRModule."""

from __future__ import annotations

import pytest

from scales.models.correction import CorrectionType
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.trust import CBTEResult, TrustDecision
from scales.modules.exceptions import SHRRValidationError
from scales.modules.shrr import SHRRModule, derive_correction_type


def _cqa(cid: str = "Q1_C1", marks: int = 1) -> CQATuple:
    return CQATuple(
        concept_id=cid,
        question_id="Q1",
        knowledge_point="TCP handshake",
        marks=marks,
        expected_keywords=["SYN"],
    )


def _cgr(student: str, cid: str, verdict: Verdict, marks: float) -> CGRResult:
    return CGRResult(
        student_id=student,
        concept_id=cid,
        verdict=verdict,
        marks_awarded=marks,
        reasoning="system judgment",
        evidence_span="SYN",
    )


def _cbte_defer(student: str, cid: str, cgr_id: str) -> CBTEResult:
    return CBTEResult(
        cgr_result_id=cgr_id,
        student_id=student,
        concept_id=cid,
        trust_score=0.4,
        decision=TrustDecision.DEFER,
        tier_resolved=3,
        signal_1_evidence_verified=True,
        signal_4_keyword_score=0.1,
        reason="Tier 3 below tau",
    )


@pytest.fixture
def shrr() -> SHRRModule:
    return SHRRModule()


def test_derive_correction_types():
    assert (
        derive_correction_type(Verdict.FULL, 1.0, Verdict.FULL, 1.0)
        == CorrectionType.AGREE
    )
    assert (
        derive_correction_type(Verdict.ABSENT, 0.0, Verdict.FULL, 1.0)
        == CorrectionType.UPGRADE
    )
    assert (
        derive_correction_type(Verdict.FULL, 1.0, Verdict.PARTIAL, 0.5)
        == CorrectionType.DOWNGRADE
    )
    assert (
        derive_correction_type(Verdict.INCORRECT, 0.0, Verdict.ABSENT, 0.0)
        == CorrectionType.OVERRIDE
    )


def test_build_queue_groups_by_concept(shrr: SHRRModule):
    cgr1 = _cgr("S1", "Q1_C1", Verdict.PARTIAL, 0.5)
    cgr2 = _cgr("S2", "Q1_C1", Verdict.ABSENT, 0.0)
    cgr3 = _cgr("S1", "Q1_C2", Verdict.FULL, 1.0)
    deferred = [
        (_cbte_defer("S1", "Q1_C1", cgr1.result_id), cgr1, _cqa("Q1_C1"), "ans1"),
        (_cbte_defer("S2", "Q1_C1", cgr2.result_id), cgr2, _cqa("Q1_C1"), "ans2"),
        (_cbte_defer("S1", "Q1_C2", cgr3.result_id), cgr3, _cqa("Q1_C2"), "ans1"),
    ]
    items = shrr.build_review_items(deferred, question_id="Q1")
    grouped = shrr.group_by_concept(items)
    assert set(grouped) == {"Q1_C1", "Q1_C2"}
    assert len(grouped["Q1_C1"]) == 2


def test_submit_upgrade_and_progress(shrr: SHRRModule):
    cgr = _cgr("S1", "Q1_C1", Verdict.ABSENT, 0.0)
    items = shrr.build_review_items(
        [(_cbte_defer("S1", "Q1_C1", cgr.result_id), cgr, _cqa(), "text")],
        question_id="Q1",
    )
    assert shrr.get_review_progress(items).remaining == 1
    result = shrr.submit_correction(
        items[0],
        teacher_verdict=Verdict.FULL,
        teacher_marks=1.0,
        teacher_comment="student had it",
    )
    assert result.correction.correction_type == CorrectionType.UPGRADE
    assert shrr.is_review_complete(items)
    assert shrr.get_review_progress(items).resolved == 1


def test_invalid_marks_rejected(shrr: SHRRModule):
    cgr = _cgr("S1", "Q1_C1", Verdict.PARTIAL, 0.5)
    items = shrr.build_review_items(
        [(_cbte_defer("S1", "Q1_C1", cgr.result_id), cgr, _cqa(marks=1), "text")],
    )
    with pytest.raises(SHRRValidationError):
        shrr.submit_correction(items[0], teacher_verdict=Verdict.FULL, teacher_marks=0.75)


def test_overwrite_correction(shrr: SHRRModule):
    cgr = _cgr("S1", "Q1_C1", Verdict.PARTIAL, 0.5)
    items = shrr.build_review_items(
        [(_cbte_defer("S1", "Q1_C1", cgr.result_id), cgr, _cqa(), "text")],
    )
    shrr.submit_correction(items[0], teacher_verdict=Verdict.FULL, teacher_marks=1.0)
    second = shrr.submit_correction(
        items[0], teacher_verdict=Verdict.ABSENT, teacher_marks=0.0
    )
    assert second.correction.correction_type == CorrectionType.DOWNGRADE
    assert len(shrr.get_corrections()) == 1


def test_zero_deferred_is_complete(shrr: SHRRModule):
    assert shrr.is_review_complete([])
