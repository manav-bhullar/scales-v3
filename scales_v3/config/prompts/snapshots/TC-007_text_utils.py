"""Text normalization, evidence verification, and keyword grounding utilities.

Implements the documented DD-1 / P0-1 strategy:
case fold + whitespace collapse, then exact substring match on normalized text.

Robustness layer (bugfix — false "hallucinated quote" DEFERs):
LLMs rarely re-quote a student answer byte-for-byte. Two drift classes were
observed to trigger false hard vetoes in CBTE Signal 1:

  1. Unicode punctuation drift — the model swaps a straight ``'`` for a curly
     ``’`` (U+2019), an ASCII ``->`` for ``→`` (U+2192), ``-`` for an en/em
     dash, or inserts a non-breaking space. ``normalize_text`` now folds these
     to ASCII so the exact substring match survives cosmetic edits.
  2. Reformatting / paraphrase — the model concatenates or re-orders the
     student's own sentences (e.g. drops ``1) 2) 3)`` list markers). Exact
     substring then fails even though every word is present. ``verify_evidence``
     now falls back to a high-threshold token-containment check so genuine
     content is accepted while true fabrications (disjoint vocabulary) are
     still rejected.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable


_WHITESPACE_RE = re.compile(r"\s+")
_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Fraction of (content) evidence tokens that must appear in the student answer
# for the fuzzy fallback to accept an otherwise non-substring quote.
EVIDENCE_FUZZY_THRESHOLD = 0.85

# Fraction of a variant phrase's content tokens that must appear in the answer
# for the variant to count as a soft keyword hit. Lower than the evidence
# threshold because variants are teacher-authored paraphrase *hints*, not
# quotes: "threads run inside a process" should match "threads are smaller
# units inside it" (3/4 content tokens). A variant hit only adds soft credit
# (1/len(expected)); it never fabricates full keyword coverage.
VARIANT_FUZZY_THRESHOLD = 0.75

# Unicode punctuation the LLM commonly substitutes when re-quoting. Mapped to
# ASCII so cosmetic drift never looks like a hallucinated quote.
_PUNCT_MAP = {
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote / apostrophe
    "\u201a": "'",   # single low-9 quote
    "\u201b": "'",   # single high-reversed-9 quote
    "\u201c": '"',   # left double quote
    "\u201d": '"',   # right double quote
    "\u201e": '"',   # double low-9 quote
    "\u2013": "-",   # en dash
    "\u2014": "-",   # em dash
    "\u2212": "-",   # minus sign
    "\u2192": "->",  # rightwards arrow
    "\u21d2": "->",  # rightwards double arrow
    "\u2026": "...",  # ellipsis
    "\u00a0": " ",   # non-breaking space
}
_PUNCT_TABLE = {ord(k): v for k, v in _PUNCT_MAP.items()}

# Minimal stopword set removed before token-containment so common glue words do
# not inflate the fuzzy score toward a false accept.
_STOPWORDS = frozenset(
    {
        "a", "an", "the", "of", "to", "and", "or", "with", "its", "it", "is",
        "are", "in", "on", "for", "so", "that", "this", "then", "as", "by",
        "be", "was", "were", "at", "from", "into", "can", "will",
    }
)


def normalize_text(text: str) -> str:
    """Case-fold, fold Unicode punctuation to ASCII, and collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_PUNCT_TABLE)
    text = text.lower()
    text = _WHITESPACE_RE.sub(" ", text)
    return text.strip()


def _content_tokens(text: str) -> list[str]:
    """Alphanumeric tokens of ``text`` with stopwords removed."""
    return [t for t in _TOKEN_RE.findall(normalize_text(text)) if t not in _STOPWORDS]


def token_containment(evidence_span: str, student_answer: str) -> float:
    """Fraction of evidence content tokens that appear in the student answer.

    Returns 1.0 when the evidence carries no content tokens (nothing to verify).
    Order-independent: catches reformatting/paraphrase where every word of the
    quote is present but not as a contiguous substring.
    """
    ev_tokens = _content_tokens(evidence_span)
    if not ev_tokens:
        return 1.0
    answer_tokens = set(_content_tokens(student_answer))
    hits = sum(1 for tok in ev_tokens if tok in answer_tokens)
    return hits / len(ev_tokens)


def verify_evidence(
    evidence_span: str,
    student_answer: str,
    fuzzy_threshold: float = EVIDENCE_FUZZY_THRESHOLD,
) -> bool:
    """Tolerant evidence check.

    1. Empty evidence_span → valid (ABSENT path, nothing to verify).
    2. Normalized substring match (case/whitespace/Unicode-punct folded).
    3. Fuzzy fallback: accept if ≥ ``fuzzy_threshold`` of the evidence's content
       tokens appear in the answer (handles LLM reformatting of its own quote).
       Disjoint-vocabulary fabrications score ~0 and are still rejected.
    """
    if not evidence_span:
        return True
    if normalize_text(evidence_span) in normalize_text(student_answer):
        return True
    return token_containment(evidence_span, student_answer) >= fuzzy_threshold


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
        if not variant or not str(variant).strip():
            continue
        # Exact normalized substring, then token-containment fallback so a
        # paraphrased variant (word order / inflection drift) still counts
        # (TC-007: exact-only matching caused a false DEFER on a FULL verdict
        # the teacher confirmed — OS1_MID_01/Q1_C1).
        if normalize_text(variant) in answer_norm:
            variant_hit = True
            break
        if (
            _content_tokens(variant)
            and token_containment(variant, student_answer) >= VARIANT_FUZZY_THRESHOLD
        ):
            variant_hit = True
            break

    if variant_hit:
        score = min(1.0, score + (1.0 / len(expected)))

    return score, found
