"""Unit tests for ExamStore JSON persistence."""

from __future__ import annotations

from scales.models.correction import CorrectionType, TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.grading import CGRResult, Verdict
from scales.models.result import ConceptFeedback, FinalResult
from scales.models.trust import CBTEResult, TrustDecision
from scales.persistence import ExamStore


def test_round_trip_grading_and_corrections(tmp_path):
    store = ExamStore("exam_test", exams_dir=tmp_path)
    exam = ExamInput(
        exam_id="exam_test",
        subject="Networks",
        questions=[
            QuestionInput(
                question_id="Q1",
                question_text="Explain TCP handshake.",
                reference_answer="SYN SYN-ACK ACK",
                total_marks=2,
                student_answers=[StudentAnswer(student_id="S1", answer_text="SYN then ACK")],
            )
        ],
    )
    store.save_exam_config(exam)
    cqas = [
        CQATuple(
            concept_id="C1",
            question_id="Q1",
            knowledge_point="handshake",
            marks=1,
            expected_keywords=["SYN"],
        )
    ]
    store.save_cqa_tuples(cqas)
    store.save_student_answers(exam.questions[0].student_answers, "Q1")

    cgr = CGRResult(
        student_id="S1",
        concept_id="C1",
        verdict=Verdict.PARTIAL,
        marks_awarded=0.5,
        reasoning="partial",
    )
    cbte = CBTEResult(
        cgr_result_id=cgr.result_id,
        student_id="S1",
        concept_id="C1",
        trust_score=0.4,
        decision=TrustDecision.DEFER,
        tier_resolved=3,
        signal_1_evidence_verified=True,
        signal_4_keyword_score=0.2,
    )
    store.save_grading_results(
        question_id="Q1",
        status="awaiting_review",
        graded_students=["S1"],
        cgr_results=[cgr],
        cbte_results=[cbte],
    )
    loaded = store.load_grading_results()
    assert loaded["graded_students"] == ["S1"]
    assert loaded["cgr_results"][0].verdict == Verdict.PARTIAL

    corr = TeacherCorrection(
        cbte_result_id=cbte.result_id,
        student_id="S1",
        concept_id="C1",
        system_verdict=Verdict.PARTIAL,
        system_marks=0.5,
        teacher_verdict=Verdict.FULL,
        teacher_marks=1.0,
        correction_type=CorrectionType.UPGRADE,
    )
    store.save_corrections([corr])
    assert store.load_corrections()[0].teacher_marks == 1.0

    final = FinalResult(
        student_id="S1",
        question_id="Q1",
        final_score=1.0,
        total_marks=2,
        overall_trust=0.4,
        concept_results=[
            ConceptFeedback(
                concept_id="C1",
                knowledge_point="handshake",
                verdict=Verdict.FULL,
                marks_awarded=1.0,
                max_marks=1,
                trust_score=0.4,
                reviewed_by="teacher",
            )
        ],
    )
    store.save_final_results([final])
    assert store.load_final_results()[0].final_score == 1.0
    assert store.load_exam_config() is not None
