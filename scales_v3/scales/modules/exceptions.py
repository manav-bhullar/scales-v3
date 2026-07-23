"""Module-layer exceptions for CERA / CGR / CBTE."""


class CERAValidationError(Exception):
    """CQA extraction failed validation after retries."""


class CGRValidationError(Exception):
    """Concept grading result failed validation after retries."""
