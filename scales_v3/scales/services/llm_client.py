"""Unified LLM API client via LiteLLM (structured output, retries, cost tracking)."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from typing import Any, TypeVar

from loguru import logger
from pydantic import BaseModel, ValidationError

from scales.config import LLMConfig, get_secrets
from scales.services.exceptions import LLMAPIError, LLMValidationError

T = TypeVar("T", bound=BaseModel)

# Rough USD / 1M tokens for cost estimates (Gemini Flash ballpark).
_COST_PER_M_INPUT = 0.10
_COST_PER_M_OUTPUT = 0.40


class LLMClient:
    """Single interface for all LLM calls in SCALES v3.0."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()
        self._total_calls = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._configure_api_keys()

    def _configure_api_keys(self) -> None:
        secrets = get_secrets()
        if secrets.google_api_key:
            os.environ.setdefault("GOOGLE_API_KEY", secrets.google_api_key)
            os.environ.setdefault("GEMINI_API_KEY", secrets.google_api_key)
        if secrets.openai_api_key:
            os.environ.setdefault("OPENAI_API_KEY", secrets.openai_api_key)
        if secrets.anthropic_api_key:
            os.environ.setdefault("ANTHROPIC_API_KEY", secrets.anthropic_api_key)

    async def call(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        response_schema: type[T],
        temperature: float | None = None,
        max_retries: int | None = None,
    ) -> T:
        """Call an LLM and return a validated Pydantic object."""
        temperature = self.config.temperature if temperature is None else temperature
        max_retries = self.config.max_retries if max_retries is None else max_retries
        delay = self.config.retry_delay_seconds

        if not self._has_credentials(model):
            raise LLMAPIError(
                f"No API key configured for model '{model}'. "
                "Set GOOGLE_API_KEY in .env for Gemini models."
            )

        messages = self._build_messages(system_prompt, user_prompt)
        prompt_hash = hashlib.sha256(
            (system_prompt + "\n" + user_prompt).encode("utf-8")
        ).hexdigest()[:12]

        last_error: Exception | None = None
        correction_attempts = 0
        max_correction_retries = 2

        for attempt in range(max_retries + 1):
            started = time.perf_counter()
            try:
                raw_text, usage = await self._invoke(model, messages, response_schema, temperature)
                duration_ms = (time.perf_counter() - started) * 1000
                self._record_usage(usage)
                self._log_call(
                    model=model,
                    prompt_hash=prompt_hash,
                    tokens_in=usage.get("input_tokens", 0),
                    tokens_out=usage.get("output_tokens", 0),
                    duration_ms=duration_ms,
                )
                try:
                    return self._validate_response(raw_text, response_schema)
                except (ValidationError, json.JSONDecodeError, ValueError) as exc:
                    last_error = exc
                    if correction_attempts >= max_correction_retries:
                        raise LLMValidationError(
                            f"Response failed validation after {correction_attempts} corrections: {exc}"
                        ) from exc
                    correction_attempts += 1
                    messages = self._build_messages(
                        system_prompt,
                        user_prompt
                        + "\n\nYour previous response had these validation errors: "
                        + str(exc)
                        + ". Please fix and return valid JSON matching the schema.",
                    )
                    logger.warning(
                        "LLM validation failure; correction retry {}/{}",
                        correction_attempts,
                        max_correction_retries,
                    )
                    continue
            except LLMValidationError:
                raise
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                if self._is_auth_error(exc):
                    raise LLMAPIError(f"LLM authentication failed: {exc}") from exc
                if attempt >= max_retries:
                    break
                sleep_for = delay * (2**attempt)
                logger.error(
                    "API call failed ({}). Retry {}/{} in {}s.",
                    type(exc).__name__,
                    attempt + 1,
                    max_retries,
                    sleep_for,
                )
                await asyncio.sleep(sleep_for)

        raise LLMAPIError(f"LLM API failed after {max_retries} retries: {last_error}")

    def get_usage(self) -> dict[str, Any]:
        cost = (
            (self._total_input_tokens / 1_000_000) * _COST_PER_M_INPUT
            + (self._total_output_tokens / 1_000_000) * _COST_PER_M_OUTPUT
        )
        return {
            "total_calls": self._total_calls,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "estimated_cost_usd": round(cost, 6),
        }

    def _build_messages(self, system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _enforce_structured_output(self, model: str, schema: type[BaseModel]) -> dict[str, Any]:
        json_schema = schema.model_json_schema()
        # Prefer json_schema when supported; Gemini via LiteLLM accepts this form.
        return {
            "type": "json_schema",
            "json_schema": {
                "name": schema.__name__,
                "schema": json_schema,
            },
        }

    async def _invoke(
        self,
        model: str,
        messages: list[dict[str, str]],
        schema: type[BaseModel],
        temperature: float,
    ) -> tuple[str, dict[str, int]]:
        import litellm

        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "timeout": 30,
            "response_format": self._enforce_structured_output(model, schema),
        }
        # Ask for JSON explicitly in case the provider ignores response_format.
        schema_hint = (
            "\n\nReturn ONLY valid JSON matching this schema:\n"
            + json.dumps(schema.model_json_schema())
        )
        keyed_messages = list(messages)
        keyed_messages[-1] = {
            **keyed_messages[-1],
            "content": keyed_messages[-1]["content"] + schema_hint,
        }
        kwargs["messages"] = keyed_messages

        try:
            response = await litellm.acompletion(**kwargs)
        except Exception:
            # Fallback: json_object mode without strict schema envelope.
            kwargs["response_format"] = {"type": "json_object"}
            response = await litellm.acompletion(**kwargs)

        content = response.choices[0].message.content or ""
        usage_obj = getattr(response, "usage", None)
        usage = {
            "input_tokens": int(getattr(usage_obj, "prompt_tokens", 0) or 0),
            "output_tokens": int(getattr(usage_obj, "completion_tokens", 0) or 0),
        }
        return content, usage

    def _validate_response(self, raw_response: str, schema: type[T]) -> T:
        text = raw_response.strip()
        if text.startswith("```"):
            # Strip markdown fences if the model wraps JSON.
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        data = json.loads(text)
        return schema.model_validate(data)

    def _record_usage(self, usage: dict[str, int]) -> None:
        self._total_calls += 1
        self._total_input_tokens += usage.get("input_tokens", 0)
        self._total_output_tokens += usage.get("output_tokens", 0)

    def _log_call(
        self,
        model: str,
        prompt_hash: str,
        tokens_in: int,
        tokens_out: int,
        duration_ms: float,
    ) -> None:
        logger.bind(module="llm").info(
            "model={} hash={} in={} out={} duration_ms={:.0f}",
            model,
            prompt_hash,
            tokens_in,
            tokens_out,
            duration_ms,
        )

    def _has_credentials(self, model: str) -> bool:
        lower = model.lower()
        if "gemini" in lower or lower.startswith("gemini/"):
            return bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
        if "gpt" in lower or "openai" in lower:
            return bool(os.environ.get("OPENAI_API_KEY"))
        if "claude" in lower or "anthropic" in lower:
            return bool(os.environ.get("ANTHROPIC_API_KEY"))
        # Unknown provider — let LiteLLM decide; require at least one key.
        return bool(
            os.environ.get("GOOGLE_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("ANTHROPIC_API_KEY")
        )

    @staticmethod
    def _is_auth_error(exc: Exception) -> bool:
        text = str(exc).lower()
        return any(token in text for token in ("api key", "unauthorized", "authentication", "401", "403"))
