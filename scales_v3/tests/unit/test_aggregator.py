"""Unit tests for AggregatorModule."""

from __future__ import annotations

import pytest

from scales.models.correction import CorrectionType, TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.trust import CBTEResult, TrustDecision
from scales.modules.aggregator import AggregatorModule
from scales.modules.exceptions import AggregatorValidationError


def _cqa(cid: str, marks: int = 1) -> CQATuple:
    return CQATuple(
        concept_id=cid,
        question_id="Q1",
        knowledge_point=cid,
        marks=marks,
        expected_keywords=[],
    )


def _cgr(sid: str, cid: str, verdict: Verdict, marks: float) -> CGRResult:
    return CGRResult(
        student_id=sid,
        concept_id=cid,
        verdict=verdict,
        marks_awarded=marks,
        reasoning="ok",
        evidence_span="x",
    )


def _cbte(sid: str, cid: str, cgr_id: str, decision: TrustDecision, trust: float) -> CBTEResult:
    return CBTEResult(
        cgr_result_id=cgr_id,
        student_id=sid,
        concept_id=cid,
        trust_score=trust,
        decision=decision,
        tier_resolved=1,
        signal_1_evidence_verified=True,
        signal_4_keyword_score=1.0,
    )


@pytest.fixture
def agg() -> AggregatorModule:
    return AggregatorModule()


def test_all_full_sums_total(agg: AggregatorModule):
    cqas = [_cqa("C1"), _cqa("C2"), _cqa("C3")]
    cgrs = [
        _cgr("S1", "C1", Verdict.FULL, 1.0),
        _cgr("S1", "C2", Verdict.FULL, 1.0),
        _cgr("S1", "C3", Verdict.FULL, 1.0),
    ]
    cbtes = [
        _cbte("S1", c.concept_id, c.result_id, TrustDecision.ACCEPT, 0.9) for c in cgrs
    ]
    result = agg.compute_final_result(
        student_id="S1",
        question_id="Q1",
        total_marks=3,
        cqa_list=cqas,
        cgr_by_concept={c.concept_id: c for c in cgrs},
        cbte_by_concept={c.concept_id: t for c, t in zip(cgrs, cbtes)},
        corrections_by_concept={},
    )
    assert result.final_score == 3.0
    assert result.overall_trust == 0.9
    assert all(f.reviewed_by == "auto" for f in result.concept_results)


def test_mixed_marks_and_min_trust(agg: AggregatorModule):
    cqas = [_cqa("C1"), _cqa("C2"), _cqa("C3")]
    cgrs = [
        _cgr("S1", "C1", Verdict.FULL, 1.0),
        _cgr("S1", "C2", Verdict.PARTIAL, 0.5),
        _cgr("S1", "C3", Verdict.ABSENT, 0.0),
    ]
    trusts = [0.95, 0.7, 0.85]
    cbtes = [
        _cbte("S1", c.concept_id, c.result_id, TrustDecision.ACCEPT, t)
        for c, t in zip(cgrs, trusts)
    ]
    result = agg.compute_final_result(
        student_id="S1",
        question_id="Q1",
        total_marks=3,
        cqa_list=cqas,
        cgr_by_concept={c.concept_id: c for c in cgrs},
        cbte_by_concept={c.concept_id: t for c, t in zip(cgrs, cbtes)},
        corrections_by_concept={},
    )
    assert result.final_score == 1.5
    assert result.overall_trust == 0.7


def test_all_absent_zero(agg: AggregatorModule):
    cqas = [_cqa("C1"), _cqa("C2")]
    cgrs = [
        _cgr("S1", "C1", Verdict.ABSENT, 0.0),
        _cgr("S1", "C2", Verdict.ABSENT, 0.0),
    ]
    cbtes = [
        _cbte("S1", c.concept_id, c.result_id, TrustDecision.ACCEPT, 0.9) for c in cgrs
    ]
    result = agg.compute_final_result(
        student_id="S1",
        question_id="Q1",
        total_marks=2,
        cqa_list=cqas,
        cgr_by_concept={c.concept_id: c for c in cgrs},
        cbte_by_concept={c.concept_id: t for c, t in zip(cgrs, cbtes)},
        corrections_by_concept={},
    )
    assert result.final_score == 0.0


def test_teacher_override_used(agg: AggregatorModule):
    cqas = [_cqa("C1"), _cqa("C2")]
    cgr_auto = _cgr("S1", "C1", Verdict.FULL, 1.0)
    cgr_def = _cgr("S1", "C2", Verdict.ABSENT, 0.0)
    cbte_auto = _cbte("S1", "C1", cgr_auto.result_id, TrustDecision.ACCEPT, 0.9)
    cbte_def = _cbte("S1", "C2", cgr_def.result_id, TrustDecision.DEFER, 0.3)
    corr = TeacherCorrection(
        cbte_result_id=cbte_def.result_id,
        student_id="S1",
        concept_id="C2",
        system_verdict=Verdict.ABSENT,
        system_marks=0.0,
        teacher_verdict=Verdict.FULL,
        teacher_marks=1.0,
        teacher_comment="paraphrase ok",
        correction_type=CorrectionType.UPGRADE,
    )
    result = agg.compute_final_result(
        student_id="S1",
        question_id="Q1",
        total_marks=2,
        cqa_list=cqas,
        cgr_by_concept={"C1": cgr_auto, "C2": cgr_def},
        cbte_by_concept={"C1": cbte_auto, "C2": cbte_def},
        corrections_by_concept={"C2": corr},
    )
    assert result.final_score == 2.0
    assert result.has_deferred_concepts is True
    teacher_line = next(f for f in result.concept_results if f.concept_id == "C2")
    assert teacher_line.reviewed_by == "teacher"
    assert teacher_line.teacher_comment == "paraphrase ok"


def test_unresolved_defer_raises(agg: AggregatorModule):
    cqas = [_cqa("C1")]
    cgr = _cgr("S1", "C1", Verdict.PARTIAL, 0.5)
    cbte = _cbte("S1", "C1", cgr.result_id, TrustDecision.DEFER, 0.2)
    with pytest.raises(AggregatorValidationError):
        agg.compute_final_result(
            student_id="S1",
            question_id="Q1",
            total_marks=1,
            cqa_list=cqas,
            cgr_by_concept={"C1": cgr},
            cbte_by_concept={"C1": cbte},
            corrections_by_concept={},
        )


def test_score_clamped_to_total(agg: AggregatorModule):
    cqas = [_cqa("C1", marks=2), _cqa("C2", marks=2)]
    cgrs = [
        _cgr("S1", "C1", Verdict.FULL, 2.0),
        _cgr("S1", "C2", Verdict.FULL, 2.0),
    ]
    cbtes = [
        _cbte("S1", c.concept_id, c.result_id, TrustDecision.ACCEPT, 1.0) for c in cgrs
    ]
    result = agg.compute_final_result(
        student_id="S1",
        question_id="Q1",
        total_marks=3,  # sum of concepts is 4 > total
        cqa_list=cqas,
        cgr_by_concept={c.concept_id: c for c in cgrs},
        cbte_by_concept={c.concept_id: t for c, t in zip(cgrs, cbtes)},
        corrections_by_concept={},
    )
    assert result.final_score == 3.0
