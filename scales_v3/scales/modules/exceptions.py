"""Module-layer exceptions for CERA / CGR / CBTE / SHRR / Aggregator."""


class CERAValidationError(Exception):
    """CQA extraction failed validation after retries."""


class CGRValidationError(Exception):
    """Concept grading result failed validation after retries."""


class SHRRValidationError(Exception):
    """Teacher correction failed validation."""


class AggregatorValidationError(Exception):
    """Final aggregation failed validation (unresolved deferrals, etc.)."""
