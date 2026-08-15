"""Pydantic data models for SCALES v3.0."""

from scales.models.correction import CorrectionType, TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.grading import CGRResult, Verdict
from scales.models.pipeline import (
    GradingPhaseResult,
    PipelinePhase,
    PipelineStatus,
    ReviewPhaseResult,
)
from scales.models.result import ConceptFeedback, FinalResult
from scales.models.review import CorrectionResult, ReviewItem, ReviewProgress
from scales.models.rubric import RubricItem
from scales.models.trust import CBTEResult, TrustDecision

__all__ = [
    "CBTEResult",
    "CGRResult",
    "CQATuple",
    "ConceptFeedback",
    "CorrectionResult",
    "CorrectionType",
    "ExamInput",
    "FinalResult",
    "GradingPhaseResult",
    "PipelinePhase",
    "PipelineStatus",
    "QuestionInput",
    "ReviewItem",
    "ReviewPhaseResult",
    "ReviewProgress",
    "RubricItem",
    "StudentAnswer",
    "TeacherCorrection",
    "TrustDecision",
    "Verdict",
]
