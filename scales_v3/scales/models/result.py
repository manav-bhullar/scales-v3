"""Final aggregated grading result models."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from scales.models.grading import Verdict


def _utc_now() -> datetime:
    return datetime.now(UTC)


class ConceptFeedback(BaseModel):
    """Per-concept feedback line in the final result."""

    concept_id: str
    knowledge_point: str
    verdict: Verdict
    marks_awarded: float = Field(..., ge=0)
    max_marks: float = Field(..., gt=0)
    evidence_span: str = Field(default="")
    reasoning: str = Field(default="")
    trust_score: float = Field(..., ge=0.0, le=1.0)
    reviewed_by: str = Field(..., pattern="^(auto|teacher)$")
    teacher_comment: str | None = None


class FinalResult(BaseModel):
    """Module 5 output for one student on one question."""

    student_id: str
    question_id: str
    final_score: float = Field(..., ge=0)
    total_marks: int = Field(..., gt=0)
    overall_trust: float = Field(..., ge=0.0, le=1.0)
    has_deferred_concepts: bool = False
    all_concepts_resolved: bool = True
    concept_results: list[ConceptFeedback] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
