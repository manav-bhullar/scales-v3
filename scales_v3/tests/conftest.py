"""Shared pytest fixtures for SCALES v3.0."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.grading import CGRResult, Verdict

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def pytest_addoption(parser):
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="Run live LLM/NLI smoke tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "live: tests that call real external services")


def _load_json(name: str):
    with (FIXTURES_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture
def sample_question_data() -> dict:
    return _load_json("sample_question.json")


@pytest.fixture
def sample_cqa_data() -> list[dict]:
    return _load_json("sample_cqa_tuples.json")


@pytest.fixture
def sample_student_answers_data() -> list[dict]:
    return _load_json("sample_student_answers.json")


@pytest.fixture
def sample_question(sample_question_data, sample_student_answers_data) -> QuestionInput:
    answers = [
        StudentAnswer(student_id=row["student_id"], answer_text=row["answer_text"])
        for row in sample_student_answers_data
    ]
    return QuestionInput(
        question_id=sample_question_data["question_id"],
        question_text=sample_question_data["question_text"],
        reference_answer=sample_question_data["reference_answer"],
        rubric=sample_question_data["rubric"],
        total_marks=sample_question_data["total_marks"],
        student_answers=answers,
    )


@pytest.fixture
def sample_exam(sample_question, sample_question_data) -> ExamInput:
    return ExamInput(
        subject=sample_question_data.get("subject", "Computer Networks"),
        questions=[sample_question],
    )


@pytest.fixture
def sample_cqa(sample_cqa_data) -> CQATuple:
    return CQATuple.model_validate(sample_cqa_data[0])


@pytest.fixture
def sample_cqa_list(sample_cqa_data) -> list[CQATuple]:
    return [CQATuple.model_validate(row) for row in sample_cqa_data]


@pytest.fixture
def sample_student_answer_good(sample_student_answers_data) -> str:
    return next(row["answer_text"] for row in sample_student_answers_data if row["label"] == "good")


@pytest.fixture
def sample_student_answer_partial(sample_student_answers_data) -> str:
    return next(
        row["answer_text"] for row in sample_student_answers_data if row["label"] == "partial"
    )


@pytest.fixture
def sample_student_answer_absent(sample_student_answers_data) -> str:
    return next(
        row["answer_text"] for row in sample_student_answers_data if row["label"] == "absent"
    )


@pytest.fixture
def sample_cgr_result_full(sample_cqa) -> CGRResult:
    return CGRResult(
        student_id="STU001",
        concept_id=sample_cqa.concept_id,
        cqa_version=sample_cqa.version,
        verdict=Verdict.FULL,
        marks_awarded=float(sample_cqa.marks),
        evidence_span="three-way handshake",
        reasoning="Student explicitly mentions three-way handshake.",
        counter_arguments="None.",
        llm_model="gemini/gemini-2.0-flash",
        prompt_hash="abc123",
    )
