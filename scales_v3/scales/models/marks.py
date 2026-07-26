"""Concept-mark helpers: quarter steps + stable prompt formatting."""

from __future__ import annotations

MARK_STEP = 0.25
_SUM_TOLERANCE = 1e-6


def is_multiple_of_mark_step(value: float, step: float = MARK_STEP) -> bool:
    """True when value is a positive-or-zero multiple of `step` (within float noise)."""
    if step <= 0:
        return False
    scaled = float(value) / step
    return abs(scaled - round(scaled)) < 1e-9


def validate_concept_marks(value: float) -> float:
    """Concept weights must be > 0 and a multiple of 0.25."""
    marks = float(value)
    if marks <= 0:
        raise ValueError("cqa.marks must be > 0")
    if not is_multiple_of_mark_step(marks):
        raise ValueError(
            f"cqa.marks must be a multiple of {MARK_STEP} (got {marks})"
        )
    # Snap to nearest step so 0.7500000002 stores cleanly.
    snapped = round(round(marks / MARK_STEP) * MARK_STEP, 10)
    return snapped


def marks_sum_matches(total: float, expected: float) -> bool:
    """Float-safe equality for concept mark totals."""
    return abs(float(total) - float(expected)) <= _SUM_TOLERANCE


def format_marks(value: float) -> str:
    """Render marks for prompts without trailing '.0' on whole numbers.

    Keeps integer concept prompts byte-stable (\"1\" not \"1.0\") after the
    int→float migration. Quarters/halves keep their decimal form.
    """
    marks = float(value)
    if abs(marks - round(marks)) < 1e-9:
        return str(int(round(marks)))
    text = f"{marks:.10f}".rstrip("0").rstrip(".")
    return text or "0"
