"""Pipeline status / grading-phase result models (Sprint 5)."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult
from scales.models.result import FinalResult
from scales.models.trust import CBTEResult


class PipelinePhase(str, Enum):
    IDLE = "idle"
    GRADING = "grading"
    AWAITING_REVIEW = "awaiting_review"
    COMPLETE = "complete"


class PipelineStatus(BaseModel):
    exam_id: str
    phase: PipelinePhase = PipelinePhase.IDLE
    total_students: int = 0
    graded_students: list[str] = Field(default_factory=list)
    deferred_count: int = 0
    corrections_count: int = 0
    review_complete: bool = False
    final_results_count: int = 0
    message: str = ""


class GradingPhaseResult(BaseModel):
    """Output of Phase 1: CERA → CGR → CBTE (+ persisted JSON)."""

    exam_id: str
    question_id: str
    cqa_tuples: list[CQATuple] = Field(default_factory=list)
    cgr_results: list[CGRResult] = Field(default_factory=list)
    cbte_results: list[CBTEResult] = Field(default_factory=list)
    graded_students: list[str] = Field(default_factory=list)
    deferred_count: int = 0
    status: PipelineStatus | None = None


class ReviewPhaseResult(BaseModel):
    """Output of Phase 2: corrections applied + final aggregation."""

    exam_id: str
    question_id: str
    final_results: list[FinalResult] = Field(default_factory=list)
    status: PipelineStatus | None = None
