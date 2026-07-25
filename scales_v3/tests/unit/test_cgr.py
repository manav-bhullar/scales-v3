"""Unit tests for CGRModule (mocked LLM)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from scales.config import LLMConfig
from scales.models.cqa import CQATuple
from scales.models.grading import Verdict
from scales.modules.cgr import CGRLLMResponse, CGRModule
from scales.modules.exceptions import CGRValidationError
from scales.services.llm_client import LLMClient


@pytest.fixture
def cqa() -> CQATuple:
    return CQATuple(
        concept_id="Q1_C1",
        question_id="Q1",
        knowledge_point="TCP uses three-way handshake for connection establishment",
        target_criteria="Mentions handshake",
        marks=1,
        expected_keywords=["three-way", "handshake"],
        acceptable_variants=["3-step connection setup"],
        partial_credit_rule=None,
    )


@pytest.fixture
def cqa_two_marks() -> CQATuple:
    return CQATuple(
        concept_id="Q1_C2",
        question_id="Q1",
        knowledge_point="Client sends SYN",
        marks=2,
        expected_keywords=["SYN", "client"],
        acceptable_variants=[],
        partial_credit_rule="1 mark if SYN mentioned without client role",
    )


@pytest.fixture
def cgr(monkeypatch) -> CGRModule:
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")
    client = LLMClient(LLMConfig(max_retries=1, retry_delay_seconds=0.01))
    return CGRModule(client, max_validation_retries=2)


def test_clamp_marks_over(cgr, cqa_two_marks):
    # Nearest discrete step among {0, 1.0, 2.0}
    assert cgr._clamp_marks(1.7, cqa_two_marks) == 2.0
    assert cgr._clamp_marks(1.2, cqa_two_marks) == 1.0


def test_clamp_marks_under(cgr, cqa):
    assert cgr._clamp_marks(-0.5, cqa) == 0.0


def test_clamp_marks_mid(cgr, cqa):
    assert cgr._clamp_marks(0.3, cqa) == 0.5


def test_allowed_marks_for_two(cgr, cqa_two_marks):
    assert cgr._allowed_marks(cqa_two_marks.marks) == [0.0, 1.0, 2.0]


def test_prompt_rendering(cgr, cqa):
    prompt = cgr._build_prompt(
        student_answer="TCP uses a three-way handshake.",
        cqa=cqa,
        question_text="Explain TCP handshake.",
    )
    assert "Q1_C1" in prompt
    assert "three-way handshake" in prompt
    assert "0.5" in prompt or "0.5" in prompt.replace(" ", "")
    assert cqa.target_criteria in prompt
    assert "{target_criteria}" not in prompt
    assert "OVERRIDES the general preference" in prompt
    assert "Do not infer this knowledge point" in prompt


def test_normalize_full_without_evidence_becomes_absent(cgr, cqa):
    raw = CGRLLMResponse(
        concept_id="Q1_C1",
        verdict=Verdict.FULL,
        marks_awarded=1.0,
        evidence_span="",
        reasoning="Student mentioned the concept clearly enough.",
        counter_arguments="None",
    )
    normalized, errors = cgr._validate_and_normalize(raw, cqa)
    assert errors == []
    assert normalized.verdict == Verdict.ABSENT
    assert normalized.marks_awarded == 0.0


def test_normalize_partial_without_evidence_becomes_absent(cgr, cqa):
    raw = CGRLLMResponse(
        concept_id="Q1_C1",
        verdict=Verdict.PARTIAL,
        marks_awarded=0.5,
        evidence_span="",
        reasoning="Vague mention without a quotable span.",
        counter_arguments="None",
    )
    normalized, errors = cgr._validate_and_normalize(raw, cqa)
    assert errors == []
    assert normalized.verdict == Verdict.ABSENT
    assert normalized.marks_awarded == 0.0

def test_normalize_absent_clears_evidence(cgr, cqa):
    raw = CGRLLMResponse(
        concept_id="Q1_C1",
        verdict=Verdict.ABSENT,
        marks_awarded=0.0,
        evidence_span="some leftover quote",
        reasoning="No relevant content found in the answer.",
        counter_arguments="None",
    )
    normalized, errors = cgr._validate_and_normalize(raw, cqa)
    assert errors == []
    assert normalized.evidence_span == ""
    assert normalized.marks_awarded == 0.0


def test_normalize_partial_marks_forced_to_half(cgr, cqa_two_marks):
    raw = CGRLLMResponse(
        concept_id="Q1_C2",
        verdict=Verdict.PARTIAL,
        marks_awarded=2.0,  # invalid for PARTIAL
        evidence_span="client sends SYN",
        reasoning="Mentions SYN but incomplete detail on client role.",
        counter_arguments="Missing full explanation",
    )
    normalized, errors = cgr._validate_and_normalize(raw, cqa_two_marks)
    assert errors == []
    assert normalized.marks_awarded == 1.0


@pytest.mark.asyncio
async def test_empty_answer_short_circuits(cgr, cqa):
    result = await cgr.grade_concept(
        student_id="STU005",
        student_answer="",
        cqa=cqa,
        question_text="Explain TCP.",
    )
    assert result.verdict == Verdict.ABSENT
    assert result.marks_awarded == 0.0
    assert result.evidence_span == ""
    assert result.llm_model == "deterministic"


@pytest.mark.asyncio
async def test_grade_concept_full(cgr, cqa):
    cgr.llm.call = AsyncMock(
        return_value=CGRLLMResponse(
            concept_id="Q1_C1",
            verdict=Verdict.FULL,
            marks_awarded=1.0,
            evidence_span="three-way handshake",
            reasoning="Student explicitly mentions three-way handshake.",
            counter_arguments="None.",
        )
    )
    result = await cgr.grade_concept(
        student_id="STU001",
        student_answer="TCP uses a three-way handshake to connect.",
        cqa=cqa,
        question_text="Explain TCP.",
    )
    assert result.verdict == Verdict.FULL
    assert result.marks_awarded == 1.0
    assert result.evidence_span == "three-way handshake"
    assert result.prompt_hash


@pytest.mark.asyncio
async def test_grade_concept_retries_on_short_reasoning(cgr, cqa):
    bad = CGRLLMResponse(
        concept_id="Q1_C1",
        verdict=Verdict.FULL,
        marks_awarded=1.0,
        evidence_span="handshake",
        reasoning="ok",  # too short
        counter_arguments="",
    )
    good = CGRLLMResponse(
        concept_id="Q1_C1",
        verdict=Verdict.FULL,
        marks_awarded=1.0,
        evidence_span="handshake",
        reasoning="Student clearly names the handshake process.",
        counter_arguments="None.",
    )
    cgr.llm.call = AsyncMock(side_effect=[bad, good])
    result = await cgr.grade_concept(
        student_id="STU001",
        student_answer="uses handshake",
        cqa=cqa,
        question_text="Explain TCP.",
    )
    assert result.verdict == Verdict.FULL
    assert cgr.llm.call.await_count == 2


@pytest.mark.asyncio
async def test_grade_all_concepts_parallel(cgr, sample_cqa_list):
    async def fake_call(**kwargs):
        schema = kwargs["response_schema"]
        # Extract concept_id from prompt
        prompt = kwargs["user_prompt"]
        concept_id = "Q1_C1"
        for cqa in sample_cqa_list:
            if cqa.concept_id in prompt:
                concept_id = cqa.concept_id
                break
        return schema(
            concept_id=concept_id,
            verdict=Verdict.ABSENT,
            marks_awarded=0.0,
            evidence_span="",
            reasoning="Concept not present in this mock answer text.",
            counter_arguments="None.",
        )

    cgr.llm.call = AsyncMock(side_effect=fake_call)
    results = await cgr.grade_all_concepts(
        student_id="STU003",
        student_answer="HTTP uses GET and POST.",
        cqa_list=sample_cqa_list,
        question_text="Explain TCP handshake.",
        max_concurrent=4,
    )
    assert len(results) == 4
    assert [r.concept_id for r in results] == [c.concept_id for c in sample_cqa_list]
    assert all(r.verdict == Verdict.ABSENT for r in results)


@pytest.mark.asyncio
async def test_grade_fails_after_retries(cgr, cqa):
    cgr.llm.call = AsyncMock(
        return_value=CGRLLMResponse(
            concept_id="Q1_C1",
            verdict=Verdict.FULL,
            marks_awarded=1.0,
            evidence_span="x",
            reasoning="bad",  # too short every time
            counter_arguments="",
        )
    )
    with pytest.raises(CGRValidationError):
        await cgr.grade_concept(
            student_id="STU001",
            student_answer="x",
            cqa=cqa,
            question_text="Explain TCP.",
        )
