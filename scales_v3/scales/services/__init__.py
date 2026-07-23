"""Infrastructure services for SCALES v3.0."""

from scales.services.exceptions import LLMAPIError, LLMValidationError
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIPrediction, NLIService
from scales.services.text_utils import (
    fuzzy_keyword_match,
    normalize_and_match,
    normalize_text,
    verify_evidence,
)

__all__ = [
    "LLMClient",
    "LLMAPIError",
    "LLMValidationError",
    "NLIService",
    "NLIPrediction",
    "normalize_text",
    "verify_evidence",
    "normalize_and_match",
    "fuzzy_keyword_match",
]
