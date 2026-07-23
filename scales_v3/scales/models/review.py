"""SHRR review-queue models (Sprint 5)."""

from __future__ import annotations

from uuid import uuid4

from pydantic import BaseModel, Field

from scales.models.correction import TeacherCorrection
from scales.models.grading import Verdict


class ReviewItem(BaseModel):
    """One deferred (student, concept) judgment awaiting teacher review."""

    review_item_id: str = Field(default_factory=lambda: str(uuid4()))
    cbte_result_id: str = Field(..., min_length=1)
    cgr_result_id: str = Field(..., min_length=1)
    student_id: str = Field(..., min_length=1)
    concept_id: str = Field(..., min_length=1)
    question_id: str = Field(default="")
    knowledge_point: str = Field(..., min_length=1)
    max_marks: int = Field(..., gt=0)
    student_answer: str = Field(default="")
    system_verdict: Verdict
    system_marks: float = Field(..., ge=0)
    evidence_span: str = Field(default="")
    reasoning: str = Field(default="")
    trust_score: float = Field(..., ge=0.0, le=1.0)
    defer_reason: str = Field(default="")


class ReviewProgress(BaseModel):
    """Progress through the deferred review queue."""

    total: int = Field(..., ge=0)
    resolved: int = Field(..., ge=0)
    remaining: int = Field(..., ge=0)
    is_complete: bool = False


class CorrectionResult(BaseModel):
    """Return payload after submitting a teacher correction."""

    correction: TeacherCorrection
    progress: ReviewProgress
