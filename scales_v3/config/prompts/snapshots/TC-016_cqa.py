"""CQA (Concept-Question-Answer) tuple produced by CERA / edited by teacher."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from scales.models.marks import validate_concept_marks

EvidenceMode = Literal["ANY", "ALL"]
EvidenceRole = Literal["synonym_set", "checklist", "select_n"]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def derive_evidence_mode(role: EvidenceRole) -> EvidenceMode:
    """Legacy mode derived from role (CGR no longer uses mode as a hard override)."""
    if role == "checklist":
        return "ALL"
    # synonym_set and select_n historically mapped near ANY; select_n is not mechanical ANY.
    return "ANY"


def derive_evidence_role(mode: EvidenceMode) -> EvidenceRole:
    """Map legacy ANY/ALL onto roles when loading older CQAs."""
    if mode == "ALL":
        return "checklist"
    return "synonym_set"


class CQATuple(BaseModel):
    """Atomic grading criterion for one knowledge point."""

    concept_id: str = Field(..., min_length=1)
    question_id: str = Field(..., min_length=1)
    knowledge_point: str = Field(..., min_length=1)
    target_criteria: str = Field(default="")
    marks: float = Field(..., gt=0)
    # Parent teacher bucket when nested rubrics are used; None = flat / legacy.
    rubric_item_id: str | None = None
    # Evidence catalog / checklist / option pool from the reference answer.
    evidence_facets: list[str] = Field(default_factory=list)
    # How facets should be satisfied (authoritative for CGR guidance).
    evidence_role: EvidenceRole = "synonym_set"
    # Required when evidence_role=select_n (e.g. name at least 2 challenges).
    min_count: int | None = None
    # Legacy ANY/ALL — derived from evidence_role for old consumers.
    evidence_mode: EvidenceMode = "ANY"
    expected_keywords: list[str] = Field(default_factory=list)
    acceptable_variants: list[str] = Field(default_factory=list)
    partial_credit_rule: str | None = None
    source_rubric_span: str = Field(default="")
    source_reference_span: str = Field(default="")
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    @model_validator(mode="before")
    @classmethod
    def migrate_role_and_mode(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        role = data.get("evidence_role")
        mode = data.get("evidence_mode")
        if not role and mode:
            mode_u = str(mode).strip().upper()
            data["evidence_role"] = derive_evidence_role(
                "ALL" if mode_u == "ALL" else "ANY"
            )
            role = data["evidence_role"]
        if not role:
            data["evidence_role"] = "synonym_set"
            role = "synonym_set"
        role_s = str(role).strip().lower()
        if role_s not in ("synonym_set", "checklist", "select_n"):
            raise ValueError(
                "evidence_role must be synonym_set, checklist, or select_n"
            )
        data["evidence_role"] = role_s
        data["evidence_mode"] = derive_evidence_mode(role_s)  # type: ignore[arg-type]
        return data

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

    @field_validator("evidence_role")
    @classmethod
    def evidence_role_lower(cls, value: str) -> str:
        role = value.strip().lower()
        if role not in ("synonym_set", "checklist", "select_n"):
            raise ValueError(
                "evidence_role must be synonym_set, checklist, or select_n"
            )
        return role

    @field_validator("min_count")
    @classmethod
    def min_count_positive(cls, value: int | None) -> int | None:
        if value is None:
            return None
        if value < 1:
            raise ValueError("min_count must be >= 1 when set")
        return value
