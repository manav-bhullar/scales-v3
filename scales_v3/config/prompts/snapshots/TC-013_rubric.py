"""Teacher-facing rubric buckets (optional nesting above CQA concepts).

Hybrid contract
---------------
- Short answers (~60–70% of cases): one RubricItem == one Concept (atomic=True).
- Medium answers: one RubricItem may expand into N concepts that sum to the
  bucket marks (atomic=False). CERA invents the split; blast radius stays
  inside that bucket.

Partial credit (SCALES default, RATAS-style additive)
----------------------------------------------------
Bucket credit = sum(concept awards under that bucket).
No rule engine: we do NOT encode non-additive logic such as
"need at least one FULL before any PARTIAL counts."
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from scales.models.marks import validate_concept_marks


class RubricItem(BaseModel):
    """One coarse teacher rubric line / marks bucket."""

    rubric_item_id: str = Field(..., min_length=1)
    label: str = Field(..., min_length=1)
    marks: float = Field(..., gt=0)
    # If True, CERA must emit exactly one concept with the same marks.
    atomic: bool = False
    description: str = Field(default="")

    @field_validator("marks")
    @classmethod
    def marks_must_be_quarter_step(cls, value: float) -> float:
        return validate_concept_marks(value)
