"""Exam input models — question, reference, rubric, student answers."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class StudentAnswer(BaseModel):
    """One student's digitized (pre-OCR'd) answer text."""

    student_id: str = Field(..., min_length=1)
    answer_text: str = Field(default="")


class QuestionInput(BaseModel):
    """A single exam question with reference answer and rubric."""

    question_id: str = Field(default="Q1", min_length=1)
    question_text: str = Field(..., min_length=1)
    reference_answer: str = Field(..., min_length=1)
    rubric: str = Field(default="")
    total_marks: int = Field(..., gt=0)
    student_answers: list[StudentAnswer] = Field(default_factory=list)

    @field_validator("total_marks")
    @classmethod
    def total_marks_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("total_marks must be > 0")
        return value


class ExamInput(BaseModel):
    """Top-level exam container (one question per exam for the skeleton)."""

    exam_id: str = Field(default_factory=lambda: f"exam_{uuid4().hex[:12]}")
    subject: str = Field(default="")
    questions: list[QuestionInput] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
