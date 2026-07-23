"""Unit tests for CERAModule (mocked LLM)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from scales.config import LLMConfig
from scales.models.exam import QuestionInput
from scales.modules.cera import (
    CERAExtractionResponse,
    CERAModule,
    CQAExtractionItem,
)
from scales.modules.exceptions import CERAValidationError
from scales.services.llm_client import LLMClient


def _item(**overrides) -> CQAExtractionItem:
    base = {
        "concept_id": "Q1_C1",
        "knowledge_point": "TCP uses three-way handshake",
        "target_criteria": "Mentions handshake",
        "marks": 1,
        "expected_keywords": ["handshake", "three-way"],
        "acceptable_variants": ["3-step setup"],
        "partial_credit_rule": None,
        "source_rubric_span": "1 mark for handshake",
        "source_reference_span": "TCP uses a three-way handshake",
    }
    base.update(overrides)
    return CQAExtractionItem(**base)


@pytest.fixture
def question() -> QuestionInput:
    return QuestionInput(
        question_id="Q1",
        question_text="Explain the three-way handshake in TCP.",
        reference_answer="TCP uses a three-way handshake (SYN → SYN-ACK → ACK).",
        rubric="1 mark handshake; 1 mark SYN; 1 mark SYN-ACK; 1 mark purpose.",
        total_marks=4,
    )


@pytest.fixture
def cera(monkeypatch) -> CERAModule:
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")
    client = LLMClient(LLMConfig(max_retries=1, retry_delay_seconds=0.01))
    return CERAModule(client, max_validation_retries=3)


def test_validate_marks_sum_ok(cera, question):
    items = [
        _item(concept_id="Q1_C1", marks=1),
        _item(concept_id="Q1_C2", marks=1, knowledge_point="SYN"),
        _item(concept_id="Q1_C3", marks=1, knowledge_point="SYN-ACK"),
        _item(concept_id="Q1_C4", marks=1, knowledge_point="purpose"),
    ]
    assert cera._validate_cqa_list(items, question) == []


def test_validate_marks_sum_mismatch(cera, question):
    items = [_item(concept_id="Q1_C1", marks=1), _item(concept_id="Q1_C2", marks=1)]
    errors = cera._validate_cqa_list(items, question)
    assert any("marks sum" in e for e in errors)


def test_validate_duplicate_ids(cera, question):
    items = [
        _item(concept_id="Q1_C1", marks=2),
        _item(concept_id="Q1_C1", marks=2, knowledge_point="other"),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("duplicate" in e for e in errors)


def test_validate_empty_keywords(cera, question):
    items = [
        _item(concept_id="Q1_C1", marks=4, expected_keywords=[]),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("expected_keywords" in e for e in errors)


def test_validate_bad_concept_id_prefix(cera, question):
    items = [_item(concept_id="Q2_C1", marks=4)]
    errors = cera._validate_cqa_list(items, question)
    assert any("must start with" in e for e in errors)


def test_prompt_contains_question_fields(cera, question):
    prompt = cera._build_prompt(question)
    assert "three-way handshake" in prompt
    assert "Q1" in prompt
    assert "4" in prompt


def test_prompt_feedback_appended(cera, question):
    prompt = cera._build_prompt(question, feedback="- marks sum mismatch")
    assert "marks sum mismatch" in prompt
    assert "validation checks" in prompt


@pytest.mark.asyncio
async def test_extract_concepts_success(cera, question):
    payload = CERAExtractionResponse(
        cqa_tuples=[
            _item(concept_id="Q1_C1", marks=1, knowledge_point="handshake"),
            _item(concept_id="Q1_C2", marks=1, knowledge_point="SYN"),
            _item(concept_id="Q1_C3", marks=1, knowledge_point="SYN-ACK"),
            _item(concept_id="Q1_C4", marks=1, knowledge_point="purpose"),
        ]
    )
    cera.llm.call = AsyncMock(return_value=payload)
    result = await cera.extract_concepts(question)
    assert len(result.cqa_tuples) == 4
    assert sum(c.marks for c in result.cqa_tuples) == 4
    assert all(c.question_id == "Q1" for c in result.cqa_tuples)
    assert result.extraction_metadata["concept_count"] == 4


@pytest.mark.asyncio
async def test_extract_retries_on_marks_mismatch_then_succeeds(cera, question):
    bad = CERAExtractionResponse(
        cqa_tuples=[
            _item(concept_id="Q1_C1", marks=1),
            _item(concept_id="Q1_C2", marks=1, knowledge_point="SYN"),
        ]
    )
    good = CERAExtractionResponse(
        cqa_tuples=[
            _item(concept_id="Q1_C1", marks=1),
            _item(concept_id="Q1_C2", marks=1, knowledge_point="SYN"),
            _item(concept_id="Q1_C3", marks=1, knowledge_point="SYN-ACK"),
            _item(concept_id="Q1_C4", marks=1, knowledge_point="purpose"),
        ]
    )
    cera.llm.call = AsyncMock(side_effect=[bad, good])
    result = await cera.extract_concepts(question)
    assert len(result.cqa_tuples) == 4
    assert cera.llm.call.await_count == 2
    second_prompt = cera.llm.call.await_args_list[1].kwargs["user_prompt"]
    assert "marks sum" in second_prompt


@pytest.mark.asyncio
async def test_extract_fails_after_retries(cera, question):
    bad = CERAExtractionResponse(
        cqa_tuples=[_item(concept_id="Q1_C1", marks=1)]
    )
    cera.llm.call = AsyncMock(return_value=bad)
    with pytest.raises(CERAValidationError):
        await cera.extract_concepts(question)


@pytest.mark.asyncio
async def test_single_mark_question(cera):
    q = QuestionInput(
        question_id="Q1",
        question_text="Name the protocol.",
        reference_answer="TCP",
        rubric="1 mark for naming TCP",
        total_marks=1,
    )
    cera.llm.call = AsyncMock(
        return_value=CERAExtractionResponse(
            cqa_tuples=[_item(concept_id="Q1_C1", marks=1, knowledge_point="TCP named")]
        )
    )
    result = await cera.extract_concepts(q)
    assert len(result.cqa_tuples) == 1
    assert result.cqa_tuples[0].marks == 1
