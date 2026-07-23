"""Live integration test: CERA → CGR (opt-in, costs API money).

Run with:
  pytest tests/integration/test_cera_cgr_live.py -v --run-live
"""

from __future__ import annotations

import pytest

from scales.config import get_secrets, get_settings
from scales.models.exam import QuestionInput, StudentAnswer
from scales.models.grading import Verdict
from scales.modules.cera import CERAModule
from scales.modules.cgr import CGRModule
from scales.services.llm_client import LLMClient


@pytest.fixture
def run_live(request):
    return request.config.getoption("--run-live")


@pytest.mark.live
@pytest.mark.asyncio
async def test_cera_then_cgr_on_sample_answers(run_live, sample_question_data, sample_student_answers_data):
    if not run_live:
        pytest.skip("Pass --run-live to execute live CERA→CGR smoke test")

    secrets = get_secrets()
    assert secrets.google_api_key, "GOOGLE_API_KEY required in .env"
    settings = get_settings()
    client = LLMClient(settings.llm)

    question = QuestionInput(
        question_id=sample_question_data["question_id"],
        question_text=sample_question_data["question_text"],
        reference_answer=sample_question_data["reference_answer"],
        rubric=sample_question_data["rubric"],
        total_marks=sample_question_data["total_marks"],
        student_answers=[
            StudentAnswer(student_id=row["student_id"], answer_text=row["answer_text"])
            for row in sample_student_answers_data
        ],
    )

    cera = CERAModule(client, settings)
    cera_out = await cera.extract_concepts(question)
    assert len(cera_out.cqa_tuples) >= 1
    assert sum(c.marks for c in cera_out.cqa_tuples) == question.total_marks

    cgr = CGRModule(client, settings)
    # Grade first 3 non-empty answers to limit cost
    graded = 0
    for student in question.student_answers:
        if not student.answer_text.strip() and graded >= 2:
            continue
        results = await cgr.grade_all_concepts(
            student_id=student.student_id,
            student_answer=student.answer_text,
            cqa_list=cera_out.cqa_tuples,
            question_text=question.question_text,
        )
        assert len(results) == len(cera_out.cqa_tuples)
        assert all(isinstance(r.verdict, Verdict) for r in results)
        graded += 1
        if graded >= 3:
            break

    usage = client.get_usage()
    assert usage["total_calls"] >= 1
    print(f"Live CERA→CGR usage: {usage}")
