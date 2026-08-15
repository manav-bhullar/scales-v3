"""CQA (Concept-Question-Answer) tuple produced by CERA / edited by teacher."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from scales.models.marks import validate_concept_marks

EvidenceMode = Literal["ANY", "ALL"]


def _utc_now() -> datetime:
    return datetime.now(UTC)


class CQATuple(BaseModel):
    """Atomic grading criterion for one knowledge point."""

    concept_id: str = Field(..., min_length=1)
    question_id: str = Field(..., min_length=1)
    knowledge_point: str = Field(..., min_length=1)
    target_criteria: str = Field(default="")
    marks: float = Field(..., gt=0)
    # Parent teacher bucket when nested rubrics are used; None = flat / legacy.
    rubric_item_id: str | None = None
    # Evidence facets from the reference answer; mode from question/rubric.
    # ANY (default): one facet suffices for FULL. ALL: all facets for FULL,
    # some for PARTIAL — requires partial_credit_rule.
    evidence_facets: list[str] = Field(default_factory=list)
    evidence_mode: EvidenceMode = "ANY"
    expected_keywords: list[str] = Field(default_factory=list)
    acceptable_variants: list[str] = Field(default_factory=list)
    partial_credit_rule: str | None = None
    source_rubric_span: str = Field(default="")
    source_reference_span: str = Field(default="")
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    @field_validator("marks")
    @classmethod
    def marks_must_be_quarter_step(cls, value: float) -> float:
        return validate_concept_marks(value)

    @field_validator("evidence_mode")
    @classmethod
    def evidence_mode_upper(cls, value: str) -> str:
        mode = value.strip().upper()
        if mode not in ("ANY", "ALL"):
            raise ValueError("evidence_mode must be ANY or ALL")
        return mode
