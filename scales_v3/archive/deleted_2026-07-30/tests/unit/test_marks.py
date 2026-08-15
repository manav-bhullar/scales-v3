"""Unit tests for concept-mark helpers (quarter steps + prompt format)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from scales.models.cqa import CQATuple
from scales.models.marks import (
    format_marks,
    is_multiple_of_mark_step,
    marks_sum_matches,
    validate_concept_marks,
)


@pytest.mark.parametrize(
    "value,ok",
    [
        (0.25, True),
        (0.5, True),
        (0.75, True),
        (1, True),
        (1.0, True),
        (1.25, True),
        (1.5, True),
        (2, True),
        (0.83, False),
        (1.1, False),
        (0, True),  # step check only; positivity enforced elsewhere
    ],
)
def test_is_multiple_of_mark_step(value: float, ok: bool):
    assert is_multiple_of_mark_step(value) is ok


def test_validate_concept_marks_accepts_quarters():
    assert validate_concept_marks(1.5) == 1.5
    assert validate_concept_marks(1.25) == 1.25
    assert validate_concept_marks(1) == 1.0


def test_validate_concept_marks_rejects_garbage():
    with pytest.raises(ValueError, match="multiple of 0.25"):
        validate_concept_marks(0.83)


def test_cqa_tuple_rejects_non_quarter():
    with pytest.raises(ValidationError):
        CQATuple(
            concept_id="Q1_C1",
            question_id="Q1",
            knowledge_point="x",
            marks=0.83,
            expected_keywords=["a"],
        )


def test_marks_sum_matches_float_safe():
    assert marks_sum_matches(1.25 + 1.25 + 1.25 + 1.25, 5)
    assert not marks_sum_matches(4.0, 5)


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1"),
        (1.0, "1"),
        (2.0, "2"),
        (0.5, "0.5"),
        (0.75, "0.75"),
        (1.25, "1.25"),
        (1.5, "1.5"),
    ],
)
def test_format_marks_stable(value: float, expected: str):
    assert format_marks(value) == expected
