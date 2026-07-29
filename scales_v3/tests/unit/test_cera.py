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
        "evidence_facets": ["three-way handshake"],
        "evidence_role": "synonym_set",
        "min_count": None,
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


def test_validate_quarter_mark_split_ok(cera):
    """Rubric 1 + 1.5 + 1.5 + 1 on a 5-mark question must validate."""
    q = QuestionInput(
        question_id="Q1",
        question_text="TCP congestion phases?",
        reference_answer="Slow start and congestion avoidance.",
        rubric="1 + 1.5 + 1.5 + 1",
        total_marks=5,
    )
    items = [
        _item(concept_id="Q1_C1", marks=1, knowledge_point="names"),
        _item(concept_id="Q1_C2", marks=1.5, knowledge_point="slow start"),
        _item(concept_id="Q1_C3", marks=1.5, knowledge_point="CA"),
        _item(concept_id="Q1_C4", marks=1, knowledge_point="loss"),
    ]
    assert cera._validate_cqa_list(items, q) == []


def test_validate_rejects_non_quarter_marks(cera, question):
    items = [
        _item(concept_id="Q1_C1", marks=0.83),
        _item(concept_id="Q1_C2", marks=1.17, knowledge_point="SYN"),
        _item(concept_id="Q1_C3", marks=1, knowledge_point="SYN-ACK"),
        _item(concept_id="Q1_C4", marks=1, knowledge_point="purpose"),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("multiple of 0.25" in e for e in errors)


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
    assert "partial_credit_rule whenever the rubric allows partial marks" in prompt
    assert "a 1-mark CQA" in prompt
    assert "multiple of 0.25" in prompt
    assert "do not round to int" in prompt
    assert "Never broaden an exclusion" in prompt


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


def test_nested_atomic_one_to_one_ok(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="Frame bursting?",
        reference_answer="Concatenates frames.",
        rubric="Definition 1.5; Adv/Disadv 1.5",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=True),
            RubricItem(rubric_item_id="R2", label="Adv/Disadv", marks=1.5, atomic=True),
        ],
    )
    items = [
        _item(
            concept_id="Q1_C1",
            marks=1.5,
            rubric_item_id="R1",
            knowledge_point="def",
            evidence_facets=["concatenates frames"],
            expected_keywords=["concatenates"],
        ),
        _item(
            concept_id="Q1_C2",
            marks=1.5,
            rubric_item_id="R2",
            knowledge_point="trade",
            evidence_facets=["advantage", "disadvantage"],
            evidence_role="checklist",
            expected_keywords=["advantage", "disadvantage"],
            partial_credit_rule="one side only → half",
            target_criteria="FULL requires both advantage and disadvantage",
        ),
    ]
    assert cera._validate_cqa_list(items, q) == []


def test_nested_may_split_additive_ok(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="Frame bursting?",
        reference_answer="Concatenates frames without releasing channel.",
        rubric="Definition 1.5; Adv/Disadv 1.5",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=False),
            RubricItem(rubric_item_id="R2", label="Adv/Disadv", marks=1.5, atomic=False),
        ],
    )
    items = [
        _item(
            concept_id="Q1_C1",
            marks=0.75,
            rubric_item_id="R1",
            knowledge_point="concat",
            evidence_facets=["concatenates frames"],
            expected_keywords=["concatenates"],
            partial_credit_rule="vague mention → half",
        ),
        _item(
            concept_id="Q1_C2",
            marks=0.75,
            rubric_item_id="R1",
            knowledge_point="channel",
            evidence_facets=["without releasing channel"],
            expected_keywords=["channel"],
            partial_credit_rule="vague mention → half",
        ),
        _item(
            concept_id="Q1_C3",
            marks=0.75,
            rubric_item_id="R2",
            knowledge_point="adv",
            evidence_facets=["more efficient", "no padding"],
            expected_keywords=["efficient", "padding"],
            target_criteria="any of: more efficient / no padding",
            partial_credit_rule="vague efficiency claim → half",
        ),
        _item(
            concept_id="Q1_C4",
            marks=0.75,
            rubric_item_id="R2",
            knowledge_point="disadv",
            evidence_facets=["waiting", "buffering", "delay"],
            expected_keywords=["waiting", "buffering", "delay"],
            target_criteria="any of: waiting / buffering / delay",
            partial_credit_rule="vague disadvantage → half",
        ),
    ]
    assert cera._validate_cqa_list(items, q) == []


def test_nested_atomic_rejects_split(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="Frame bursting?",
        reference_answer="Concatenates frames.",
        rubric="Definition 1.5",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=True),
            RubricItem(rubric_item_id="R2", label="Adv/Disadv", marks=1.5, atomic=True),
        ],
    )
    items = [
        _item(
            concept_id="Q1_C1",
            marks=0.75,
            rubric_item_id="R1",
            knowledge_point="a",
            evidence_facets=["a"],
            expected_keywords=["a"],
            partial_credit_rule="half",
        ),
        _item(
            concept_id="Q1_C2",
            marks=0.75,
            rubric_item_id="R1",
            knowledge_point="b",
            evidence_facets=["b"],
            expected_keywords=["b"],
            partial_credit_rule="half",
        ),
        _item(
            concept_id="Q1_C3",
            marks=1.5,
            rubric_item_id="R2",
            knowledge_point="c",
            evidence_facets=["c"],
            expected_keywords=["c"],
        ),
    ]
    errors = cera._validate_cqa_list(items, q)
    assert any("atomic=True" in e for e in errors)


def test_nested_child_sum_mismatch(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="x",
        reference_answer="y",
        rubric="z",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=False),
            RubricItem(rubric_item_id="R2", label="Adv/Disadv", marks=1.5, atomic=False),
        ],
    )
    items = [
        _item(
            concept_id="Q1_C1",
            marks=1.0,
            rubric_item_id="R1",
            knowledge_point="a",
            evidence_facets=["a"],
            expected_keywords=["a"],
        ),
        _item(
            concept_id="Q1_C2",
            marks=2.0,
            rubric_item_id="R2",
            knowledge_point="b",
            evidence_facets=["b"],
            expected_keywords=["b"],
        ),
    ]
    errors = cera._validate_cqa_list(items, q)
    assert any("child concept marks sum" in e for e in errors)


def test_prompt_includes_structured_rubric_items(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="Frame bursting?",
        reference_answer="Concatenates frames.",
        rubric="Definition 1.5; Adv/Disadv 1.5",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=False),
            RubricItem(
                rubric_item_id="R2",
                label="Adv and disadv",
                marks=1.5,
                atomic=True,
            ),
        ],
    )
    prompt = cera._build_prompt(q)
    assert "R1" in prompt and "MAY SPLIT" in prompt
    assert "R2" in prompt and "ATOMIC" in prompt
    assert "Prefer 1 rubric item → 1 concept" in prompt


@pytest.mark.asyncio
async def test_extract_rejects_bad_rubric_item_totals(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="x",
        reference_answer="y",
        rubric="z",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="A", marks=1.0, atomic=True),
            RubricItem(rubric_item_id="R2", label="B", marks=1.0, atomic=True),
        ],
    )
    with pytest.raises(CERAValidationError, match="rubric_items"):
        await cera.extract_concepts(q)


def test_evidence_facets_required(cera, question):
    items = [
        _item(concept_id="Q1_C1", marks=1, evidence_facets=[]),
        _item(concept_id="Q1_C2", marks=1, knowledge_point="SYN"),
        _item(concept_id="Q1_C3", marks=1, knowledge_point="SYN-ACK"),
        _item(concept_id="Q1_C4", marks=1, knowledge_point="purpose"),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("evidence_facets must be non-empty" in e for e in errors)


def test_checklist_role_requires_partial(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["name", "explain"],
            evidence_role="checklist",
            expected_keywords=["name", "explain"],
            partial_credit_rule=None,
            target_criteria="FULL requires name and explain",
        ),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("evidence_role=checklist requires" in e for e in errors)


def test_any_mode_rejects_and_chain_criteria(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["waiting", "delay"],
            evidence_role="synonym_set",
            expected_keywords=["waiting", "delay"],
            target_criteria="Must explain waiting leading to delay",
        ),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("AND-chain" in e for e in errors)


def test_any_mode_allows_because_in_or_explanation(cera, question):
    """'because' alone is not enough to flag — used in facet glosses."""
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["more efficient", "no padding"],
            evidence_role="synonym_set",
            expected_keywords=["efficient", "padding"],
            target_criteria="any of: more efficient (e.g. because no padding) / no padding",
        ),
    ]
    assert cera._validate_cqa_list(items, question) == []



def test_any_mode_or_set_ok(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["waiting", "delay"],
            evidence_role="synonym_set",
            expected_keywords=["waiting", "delay"],
            target_criteria="any of: waiting / delay counts",
        ),
    ]
    assert cera._validate_cqa_list(items, question) == []


def test_any_mode_requires_any_of_phrase(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["waiting", "delay"],
            evidence_role="synonym_set",
            expected_keywords=["waiting", "delay"],
            target_criteria="Student mentions waiting or delay somehow",
        ),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("any of:" in e for e in errors)

def test_keywords_must_cover_facets(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["waiting for frames", "increased delay"],
            expected_keywords=["waiting"],  # delay uncovered
            target_criteria="any of waiting / delay",
        ),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("cover every evidence facet" in e for e in errors)


def test_may_split_child_requires_partial(cera):
    from scales.models.rubric import RubricItem

    q = QuestionInput(
        question_id="Q1",
        question_text="Frame bursting?",
        reference_answer="Concatenates frames. Advantage efficient. Disadvantage delay.",
        rubric="Def 1.5; Adv/Disadv 1.5",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=True),
            RubricItem(rubric_item_id="R2", label="Adv/Disadv", marks=1.5, atomic=False),
        ],
    )
    items = [
        _item(
            concept_id="Q1_C1",
            marks=1.5,
            rubric_item_id="R1",
            knowledge_point="def",
            evidence_facets=["concatenates"],
            expected_keywords=["concatenates"],
        ),
        _item(
            concept_id="Q1_C2",
            marks=0.75,
            rubric_item_id="R2",
            knowledge_point="adv",
            evidence_facets=["efficient"],
            expected_keywords=["efficient"],
            partial_credit_rule=None,
            target_criteria="efficiency",
        ),
        _item(
            concept_id="Q1_C3",
            marks=0.75,
            rubric_item_id="R2",
            knowledge_point="disadv",
            evidence_facets=["delay"],
            expected_keywords=["delay"],
            partial_credit_rule=None,
            target_criteria="delay",
        ),
    ]
    errors = cera._validate_cqa_list(items, q)
    assert any("MAY-SPLIT child" in e for e in errors)


def test_may_split_rejects_fake_null_partial_string(cera):
    from scales.models.rubric import RubricItem
    from scales.modules.cera import is_real_partial_credit_rule, normalize_partial_credit_rule

    assert not is_real_partial_credit_rule("null")
    assert not is_real_partial_credit_rule("No partial credit defined for this specific sub-concept.")
    assert not is_real_partial_credit_rule("none")
    assert normalize_partial_credit_rule("null") is None
    assert is_real_partial_credit_rule("vague mention → half")

    q = QuestionInput(
        question_id="Q1",
        question_text="Frame bursting?",
        reference_answer="Concatenates frames. Advantage efficient. Disadvantage delay.",
        rubric="Def 1.5; Adv/Disadv 1.5",
        total_marks=3,
        rubric_items=[
            RubricItem(rubric_item_id="R1", label="Definition", marks=1.5, atomic=True),
            RubricItem(rubric_item_id="R2", label="Adv/Disadv", marks=1.5, atomic=False),
        ],
    )
    items = [
        _item(
            concept_id="Q1_C1",
            marks=1.5,
            rubric_item_id="R1",
            knowledge_point="def",
            evidence_facets=["concatenates"],
            expected_keywords=["concatenates"],
        ),
        _item(
            concept_id="Q1_C2",
            marks=0.75,
            rubric_item_id="R2",
            knowledge_point="adv",
            evidence_facets=["efficient"],
            expected_keywords=["efficient"],
            partial_credit_rule="null",
            target_criteria="efficiency",
        ),
        _item(
            concept_id="Q1_C3",
            marks=0.75,
            rubric_item_id="R2",
            knowledge_point="disadv",
            evidence_facets=["delay"],
            expected_keywords=["delay"],
            partial_credit_rule="No partial credit defined.",
            target_criteria="delay",
        ),
    ]
    errors = cera._validate_cqa_list(items, q)
    assert any("real partial_credit_rule" in e for e in errors)


def test_checklist_rejects_fake_null_partial(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=["name", "explain"],
            evidence_role="checklist",
            expected_keywords=["name", "explain"],
            partial_credit_rule="null",
            target_criteria="FULL requires name and explain",
        ),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("evidence_role=checklist requires a real partial_credit_rule" in e for e in errors)


def test_prompt_mentions_evidence_roles(cera, question):
    prompt = cera._build_prompt(question)
    assert "evidence_facets" in prompt
    assert "evidence_role" in prompt
    assert "synonym_set" in prompt and "checklist" in prompt and "select_n" in prompt


def test_select_n_requires_min_count_and_partial(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_facets=[
                "Adaptation",
                "Security",
                "Medium Access Control",
                "Quality of Service",
                "Scalability",
                "Power Consumption",
            ],
            evidence_role="select_n",
            min_count=None,
            expected_keywords=[
                "Adaptation",
                "Security",
                "Medium Access Control",
                "Quality of Service",
                "Scalability",
                "Power Consumption",
            ],
            target_criteria="FULL = at least 2 distinct valid challenges",
            partial_credit_rule="exactly one → 0.5",
        ),
    ]
    errors = cera._validate_cqa_list(items, question)
    assert any("min_count" in e for e in errors)


def test_select_n_name_two_of_six_ok(cera, question):
    """CE08-style naming: select_n with min_count=2 validates cleanly."""
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            knowledge_point="Student must name two distinct mobile routing challenges",
            evidence_facets=[
                "Adaptation",
                "Security",
                "Medium Access Control",
                "Quality of Service",
                "Scalability",
                "Power Consumption",
            ],
            evidence_role="select_n",
            min_count=2,
            expected_keywords=[
                "Adaptation",
                "Security",
                "Medium Access Control",
                "Quality of Service",
                "Scalability",
                "Power Consumption",
            ],
            target_criteria=(
                "FULL = at least 2 distinct valid challenges from the catalog; "
                "PARTIAL = exactly 1; ABSENT = 0"
            ),
            partial_credit_rule="exactly one valid challenge named → 0.5 marks",
        ),
    ]
    assert cera._validate_cqa_list(items, question) == []


def test_legacy_evidence_mode_all_maps_to_checklist():
    item = CQAExtractionItem(
        concept_id="Q1_C1",
        knowledge_point="name and explain",
        target_criteria="FULL requires both",
        marks=1,
        evidence_facets=["name", "explain"],
        evidence_mode="ALL",
        expected_keywords=["name", "explain"],
        partial_credit_rule="name only → half",
        source_rubric_span="x",
        source_reference_span="y",
    )
    assert item.evidence_role == "checklist"
    assert item.evidence_mode == "ALL"


def test_to_cqa_preserves_select_n(cera, question):
    items = [
        _item(
            concept_id="Q1_C1",
            marks=4,
            evidence_role="select_n",
            min_count=2,
            evidence_facets=["A", "B", "C"],
            expected_keywords=["A", "B", "C"],
            target_criteria="FULL = at least 2 distinct valid items from the catalog",
            partial_credit_rule="one → half",
        ),
    ]
    assert cera._validate_cqa_list(items, question) == []
    cqas = cera._to_cqa_tuples(items, question)
    assert cqas[0].evidence_role == "select_n"
    assert cqas[0].min_count == 2
    assert cqas[0].evidence_mode == "ANY"  # legacy derived