"""Shared service-layer exceptions."""


class LLMAPIError(Exception):
    """Raised when the LLM API fails after retries (or on non-retriable auth errors)."""


class LLMValidationError(Exception):
    """Raised when the LLM response cannot be parsed/validated after correction retries."""
