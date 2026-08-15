"""CBTE (trust estimation) result models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(UTC)


class TrustDecision(str, Enum):
    ACCEPT = "ACCEPT"
    DEFER = "DEFER"


class CBTEResult(BaseModel):
    """Output of Module 3 for one CGR judgment."""

    result_id: str = Field(default_factory=lambda: str(uuid4()))
    cgr_result_id: str = Field(..., min_length=1)
    student_id: str = Field(..., min_length=1)
    concept_id: str = Field(..., min_length=1)
    trust_score: float = Field(..., ge=0.0, le=1.0)
    decision: TrustDecision
    tier_resolved: int = Field(..., ge=1, le=3)
    signal_1_evidence_verified: bool
    signal_2_nli_score: float | None = None
    signal_3_stability: float | None = None
    signal_4_keyword_score: float = Field(..., ge=0.0, le=1.0)
    keywords_found: list[str] = Field(default_factory=list)
    reason: str = Field(default="")
    created_at: datetime = Field(default_factory=_utc_now)
