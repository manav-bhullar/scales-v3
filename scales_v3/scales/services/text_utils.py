"""Text normalization, evidence verification, and keyword grounding utilities.

Implements the documented DD-1 / P0-1 strategy:
case fold + whitespace collapse, then exact substring match on normalized text.
"""

from __future__ import annotations

import re
from typing import Iterable


_WHITESPACE_RE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Strip whitespace artifacts and case before comparison."""
    text = text.lower()
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def verify_evidence(evidence_span: str, student_answer: str) -> bool:
    """Tolerant evidence check: normalized substring match.

    Empty evidence_span is treated as valid (ABSENT path — nothing to verify).
    """
    if not evidence_span:
        return True
    return normalize_text(evidence_span) in normalize_text(student_answer)


def normalize_and_match(evidence_span: str, student_answer: str) -> bool:
    """Alias used by CBTE Signal 1 (documented name)."""
    return verify_evidence(evidence_span, student_answer)


def _keyword_present(keyword: str, haystack_normalized: str) -> bool:
    """Case-insensitive keyword / phrase match on normalized text."""
    needle = normalize_text(keyword)
    if not needle:
        return False
    if " " in needle or "-" in needle:
        return needle in haystack_normalized
    pattern = rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])"
    return re.search(pattern, haystack_normalized) is not None


def fuzzy_keyword_match(
    expected_keywords: Iterable[str],
    student_answer: str,
    acceptable_variants: Iterable[str] | None = None,
) -> tuple[float, list[str]]:
    """Return (keyword_score, list_of_found_keywords).

    Primary score: |found expected keywords| / |expected keywords|.
    Acceptable variants that appear count as an additional soft hit
    (P0-4), capped at 1.0. Empty expected_keywords → score 1.0.
    """
    expected = [kw for kw in expected_keywords if kw and str(kw).strip()]
    if not expected:
        return 1.0, []

    answer_norm = normalize_text(student_answer)
    found = [kw for kw in expected if _keyword_present(kw, answer_norm)]
    score = len(found) / len(expected)

    variant_hit = False
    for variant in acceptable_variants or []:
        if variant and normalize_text(variant) in answer_norm:
            variant_hit = True
            break

    if variant_hit:
        score = min(1.0, score + (1.0 / len(expected)))

    return score, found
