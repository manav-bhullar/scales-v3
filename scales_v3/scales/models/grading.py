"""CGR (concept-level grading) result models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(UTC)


class Verdict(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    ABSENT = "ABSENT"
    INCORRECT = "INCORRECT"


class CGRResult(BaseModel):
    """Output of Module 2 for one (student, concept) pair."""

    result_id: str = Field(default_factory=lambda: str(uuid4()))
    student_id: str = Field(..., min_length=1)
    concept_id: str = Field(..., min_length=1)
    cqa_version: int = Field(default=1, ge=1)
    verdict: Verdict
    marks_awarded: float = Field(..., ge=0)
    evidence_span: str = Field(default="")
    reasoning: str = Field(..., min_length=1)
    counter_arguments: str = Field(default="")
    llm_model: str = Field(default="")
    prompt_hash: str = Field(default="")
    created_at: datetime = Field(default_factory=_utc_now)
