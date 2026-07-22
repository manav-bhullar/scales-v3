"""Teacher correction models (SHRR)."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

from scales.models.grading import Verdict


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CorrectionType(str, Enum):
    AGREE = "AGREE"
    UPGRADE = "UPGRADE"
    DOWNGRADE = "DOWNGRADE"
    OVERRIDE = "OVERRIDE"


class TeacherCorrection(BaseModel):
    """One teacher review of a deferred (student, concept) judgment."""

    correction_id: str = Field(default_factory=lambda: str(uuid4()))
    cbte_result_id: str = Field(..., min_length=1)
    review_item_id: str | None = None
    student_id: str = Field(..., min_length=1)
    concept_id: str = Field(..., min_length=1)
    system_verdict: Verdict
    system_marks: float = Field(..., ge=0)
    teacher_verdict: Verdict
    teacher_marks: float = Field(..., ge=0)
    teacher_comment: str = Field(default="")
    correction_type: CorrectionType
    created_at: datetime = Field(default_factory=_utc_now)
