"""Contract tests for the /breakdown endpoint (per-concept "why these marks").

Guards the shape the teacher UI depends on: every graded student appears with
one row per concept, keyword accounting splits into found/missing, and teacher
corrections win over the machine verdict in `current_score`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from scales.models.correction import CorrectionType, TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.grading import CGRResult, Verdict
from scales.models.trust import CBTEResult, TrustDecision
from scales.persistence import ExamStore

PROJECT = Path(__file__).resolve().parents[2]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

EXAM_ID = "breakdown_contract_exam"


def _seed(exams_dir: Path) -> None:
    exam = ExamInput(
        exam_id=EXAM_ID,
        subject="OS",
        questions=[
            QuestionInput(
                question_id="Q1",
                question_text="Difference between a process and a thread?",
                reference_answer="A process owns its address space; threads share one.",
                rubric="1 mark address space, 1 mark sharing",
                total_marks=2,
                student_answers=[
                    StudentAnswer(
                        student_id="S1",
                        answer_text="A process has its own address space.",
                    ),
                    StudentAnswer(student_id="S2", answer_text="They are the same."),
                ],
            )
        ],
    )
    store = ExamStore(EXAM_ID, exams_dir=exams_dir)
    store.save_exam_config(exam)
    store.save_student_answers(exam.questions[0].student_answers, "Q1")
    store.save_cqa_tuples(
        [
            CQATuple(
                concept_id="Q1_C1",
                question_id="Q1",
                knowledge_point="process owns address space",
                target_criteria="States a process has its own address space",
                marks=1,
                expected_keywords=["address space", "own"],
            ),
            CQATuple(
                concept_id="Q1_C2",
                question_id="Q1",
                knowledge_point="threads share address space",
                target_criteria="States threads share the address space",
                marks=1,
                expected_keywords=["share", "thread"],
            ),
        ]
    )

    cgr = [
        CGRResult(
            result_id="cgr-s1-c1",
            student_id="S1",
            concept_id="Q1_C1",
            verdict=Verdict.FULL,
            marks_awarded=1.0,
            evidence_span="has its own address space",
            reasoning="Explicitly states the process owns its address space.",
        ),
        CGRResult(
            result_id="cgr-s1-c2",
            student_id="S1",
            concept_id="Q1_C2",
            verdict=Verdict.ABSENT,
            marks_awarded=0.0,
            evidence_span="",
            reasoning="Never mentions threads sharing anything.",
        ),
        CGRResult(
            result_id="cgr-s2-c1",
            student_id="S2",
            concept_id="Q1_C1",
            verdict=Verdict.INCORRECT,
            marks_awarded=0.0,
            evidence_span="They are the same",
            reasoning="Claims equivalence, which is wrong.",
        ),
        CGRResult(
            result_id="cgr-s2-c2",
            student_id="S2",
            concept_id="Q1_C2",
            verdict=Verdict.ABSENT,
            marks_awarded=0.0,
            evidence_span="",
            reasoning="Nothing about sharing.",
        ),
    ]
    cbte = [
        CBTEResult(
            result_id="cbte-s1-c1",
            cgr_result_id="cgr-s1-c1",
            student_id="S1",
            concept_id="Q1_C1",
            trust_score=0.95,
            decision=TrustDecision.ACCEPT,
            tier_resolved=1,
            signal_1_evidence_verified=True,
            signal_4_keyword_score=1.0,
            keywords_found=["address space", "own"],
            reason="Tier 1 accept.",
        ),
        # Accepted zero: the case the UI must flag as never human-checked.
        CBTEResult(
            result_id="cbte-s1-c2",
            cgr_result_id="cgr-s1-c2",
            student_id="S1",
            concept_id="Q1_C2",
            trust_score=0.9,
            decision=TrustDecision.ACCEPT,
            tier_resolved=1,
            signal_1_evidence_verified=False,
            signal_4_keyword_score=0.0,
            keywords_found=[],
            reason="ABSENT with no keywords present.",
        ),
        CBTEResult(
            result_id="cbte-s2-c1",
            cgr_result_id="cgr-s2-c1",
            student_id="S2",
            concept_id="Q1_C1",
            trust_score=0.4,
            decision=TrustDecision.DEFER,
            tier_resolved=2,
            signal_1_evidence_verified=True,
            signal_2_nli_score=0.2,
            signal_4_keyword_score=0.0,
            keywords_found=[],
            reason="Low trust.",
        ),
        CBTEResult(
            result_id="cbte-s2-c2",
            cgr_result_id="cgr-s2-c2",
            student_id="S2",
            concept_id="Q1_C2",
            trust_score=0.88,
            decision=TrustDecision.ACCEPT,
            tier_resolved=1,
            signal_1_evidence_verified=False,
            signal_4_keyword_score=0.0,
            keywords_found=[],
            reason="ABSENT confirmed.",
        ),
    ]
    store.save_grading_results(
        question_id="Q1",
        status="awaiting_review",
        graded_students=["S1", "S2"],
        cgr_results=cgr,
        cbte_results=cbte,
    )
    store.save_corrections(
        [
            TeacherCorrection(
                cbte_result_id="cbte-s2-c1",
                student_id="S2",
                concept_id="Q1_C1",
                system_verdict=Verdict.INCORRECT,
                system_marks=0.0,
                teacher_verdict=Verdict.PARTIAL,
                teacher_marks=0.5,
                teacher_comment="Gestures at the idea.",
                correction_type=CorrectionType.UPGRADE,
            )
        ]
    )


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    exams_dir = tmp_path / "exams"
    exams_dir.mkdir()

    from api import main as api_main
    from scales.config import get_settings

    # Point exams_dir at tmp via settings so both the API helpers and the
    # ExamStore instances the pipeline builds internally follow along.
    settings = get_settings()
    settings.paths.exams_dir = str(exams_dir)
    monkeypatch.setattr(api_main, "get_settings", lambda *a, **k: settings)
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")

    _seed(exams_dir)
    return TestClient(api_main.app)


@pytest.mark.contracts
def test_breakdown_returns_every_student_and_concept(client):
    body = client.get(f"/api/exams/{EXAM_ID}/breakdown").json()
    assert body["question"]["total_marks"] == 2.0
    assert [c["concept_id"] for c in body["concepts"]] == ["Q1_C1", "Q1_C2"]
    assert [s["student_id"] for s in body["students"]] == ["S1", "S2"]
    for student in body["students"]:
        assert [c["concept_id"] for c in student["concepts"]] == ["Q1_C1", "Q1_C2"]
        assert student["answer_text"], "answer text must be joinable for highlighting"


@pytest.mark.contracts
def test_breakdown_carries_reasoning_and_keyword_split(client):
    body = client.get(f"/api/exams/{EXAM_ID}/breakdown").json()
    s1 = next(s for s in body["students"] if s["student_id"] == "S1")
    c1, c2 = s1["concepts"]

    assert c1["verdict"] == "FULL"
    assert c1["reasoning"]
    assert c1["evidence_span"] in s1["answer_text"]
    assert c1["keywords_found"] == ["address space", "own"]
    assert c1["keywords_missing"] == []

    # ABSENT + accepted + zero marks: the silent-zero audit case.
    assert c2["verdict"] == "ABSENT"
    assert c2["marks_awarded"] == 0.0
    assert c2["decision"] == "ACCEPT"
    assert c2["source"] == "auto"
    assert sorted(c2["keywords_missing"]) == ["share", "thread"]


@pytest.mark.contracts
def test_breakdown_applies_teacher_correction_to_current_score(client):
    body = client.get(f"/api/exams/{EXAM_ID}/breakdown").json()
    s2 = next(s for s in body["students"] if s["student_id"] == "S2")
    corrected = next(c for c in s2["concepts"] if c["concept_id"] == "Q1_C1")

    assert corrected["source"] == "teacher"
    assert corrected["verdict"] == "INCORRECT", "machine verdict stays visible"
    assert corrected["teacher_verdict"] == "PARTIAL"
    assert corrected["teacher_marks"] == 0.5
    assert corrected["correction_type"] == "UPGRADE"

    assert s2["auto_score"] == 0.0
    assert s2["current_score"] == 0.5
    assert s2["corrected_count"] == 1
    assert s2["deferred_count"] == 0, "resolved DEFER no longer counts as waiting"


@pytest.mark.contracts
def test_breakdown_404_on_unknown_exam(client):
    assert client.get("/api/exams/no_such_exam/breakdown").status_code == 404
