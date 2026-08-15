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
        self._gemini_keys: list[str] = []
        self._gemini_idx = 0
        self._configure_api_keys()

    def _configure_api_keys(self) -> None:
        secrets = get_secrets()
        self._gemini_keys = secrets.gemini_api_keys()
        if self._gemini_keys:
            self._activate_gemini_key(self._gemini_keys[0])
        if secrets.openai_api_key:
            os.environ.setdefault("OPENAI_API_KEY", secrets.openai_api_key)
        if secrets.anthropic_api_key:
            os.environ.setdefault("ANTHROPIC_API_KEY", secrets.anthropic_api_key)
        if secrets.groq_api_key:
            os.environ.setdefault("GROQ_API_KEY", secrets.groq_api_key)
        openrouter_key = secrets.openrouter_api_key or secrets.open_router_api_key
        if openrouter_key:
            os.environ.setdefault("OPENROUTER_API_KEY", openrouter_key)
        zai_key = secrets.zai_api_key or secrets.z_ai_api_key
        if zai_key:
            os.environ.setdefault("ZAI_API_KEY", zai_key)
        if secrets.zai_api_base:
            os.environ.setdefault("ZAI_API_BASE", secrets.zai_api_base.rstrip("/"))
        if secrets.cerebras_api_key:
            os.environ.setdefault("CEREBRAS_API_KEY", secrets.cerebras_api_key)
        if secrets.mistral_api_key:
            os.environ.setdefault("MISTRAL_API_KEY", secrets.mistral_api_key)

    def _activate_gemini_key(self, key: str) -> None:
        os.environ["GOOGLE_API_KEY"] = key
        os.environ["GEMINI_API_KEY"] = key

    def _rotate_gemini_key(self) -> bool:
        """Advance to the next Gemini key. Returns False if fewer than 2 keys."""
        if len(self._gemini_keys) < 2:
            return False
        self._gemini_idx = (self._gemini_idx + 1) % len(self._gemini_keys)
        self._activate_gemini_key(self._gemini_keys[self._gemini_idx])
        logger.warning(
            "Rotated Gemini API key -> slot {}/{}",
            self._gemini_idx + 1,
            len(self._gemini_keys),
        )
        return True

    @staticmethod
    def _is_gemini_model(model: str) -> bool:
        lower = model.lower()
        return lower.startswith("gemini/") or "gemini" in lower

    @staticmethod
    def _is_rate_limit_error(exc: Exception) -> bool:
        text = str(exc).lower()
        return any(
            token in text
            for token in ("rate limit", "429", "quota", "resource exhausted", "tpm", "rpm")
        )

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
                "Set CEREBRAS_API_KEY (cerebras/...), ZAI_API_KEY (zai/...), "
                "MISTRAL_API_KEY (mistral/...), "
                "OPENROUTER_API_KEY (openrouter/...), GROQ_API_KEY (groq/...), "
                "GOOGLE_API_KEY / GOOGLE_API_KEY_1..5 (gemini/...), "
                "OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env."
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
            except Exception as exc:
                last_error = exc
                if self._is_auth_error(exc):
                    # Auth on one Gemini key: try next key before giving up.
                    if self._is_gemini_model(model) and self._rotate_gemini_key():
                        continue
                    raise LLMAPIError(f"LLM authentication failed: {exc}") from exc
                if attempt >= max_retries:
                    break
                if self._is_gemini_model(model) and self._is_rate_limit_error(exc):
                    rotated = self._rotate_gemini_key()
                    sleep_for = 0.5 if rotated else delay * (2**attempt)
                else:
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
        cost = (self._total_input_tokens / 1_000_000) * _COST_PER_M_INPUT + (
            self._total_output_tokens / 1_000_000
        ) * _COST_PER_M_OUTPUT
        return {
            "total_calls": self._total_calls,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "estimated_cost_usd": round(cost, 6),
            "gemini_keys_configured": len(self._gemini_keys),
        }

    def _build_messages(self, system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _enforce_structured_output(self, model: str, schema: type[BaseModel]) -> dict[str, Any]:
        json_schema = schema.model_json_schema()
        return {
            "type": "json_schema",
            "json_schema": {
                "name": schema.__name__,
                "schema": json_schema,
            },
        }

    def _resolve_provider_kwargs(self, model: str) -> dict[str, Any]:
        """Map provider-specific model ids onto what this LiteLLM version supports."""
        lower = model.lower()
        if lower.startswith("zai/") or lower.startswith("zhipu/"):
            bare = model.split("/", 1)[1]
            api_base = (os.environ.get("ZAI_API_BASE") or "https://api.z.ai/api/paas/v4").rstrip(
                "/"
            )
            return {
                "model": f"openai/{bare}",
                "api_base": api_base,
                "api_key": os.environ.get("ZAI_API_KEY") or "",
                "custom_llm_provider": "openai",
            }
        if self._is_gemini_model(model) and self._gemini_keys:
            # Explicit api_key so rotation is honored even if env was stale.
            return {
                "model": model,
                "api_key": self._gemini_keys[self._gemini_idx],
            }
        return {"model": model}

    async def _invoke(
        self,
        model: str,
        messages: list[dict[str, str]],
        schema: type[BaseModel],
        temperature: float,
    ) -> tuple[str, dict[str, int]]:
        import litellm

        kwargs: dict[str, Any] = {
            **self._resolve_provider_kwargs(model),
            "messages": messages,
            "temperature": temperature,
            "timeout": 60,
            "max_tokens": 2048,
            "response_format": self._enforce_structured_output(model, schema),
        }
        schema_hint = "\n\nReturn ONLY valid JSON matching this schema:\n" + json.dumps(
            schema.model_json_schema()
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
        if lower.startswith("cerebras/"):
            return bool(os.environ.get("CEREBRAS_API_KEY"))
        if lower.startswith("zai/") or lower.startswith("zhipu/"):
            return bool(os.environ.get("ZAI_API_KEY"))
        if lower.startswith("openrouter/") or "openrouter" in lower:
            return bool(os.environ.get("OPENROUTER_API_KEY"))
        if lower.startswith("groq/") or "groq" in lower:
            return bool(os.environ.get("GROQ_API_KEY"))
        if lower.startswith("mistral/"):
            return bool(os.environ.get("MISTRAL_API_KEY"))
        if self._is_gemini_model(model):
            return bool(self._gemini_keys) or bool(
                os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            )
        if "gpt" in lower or lower.startswith("openai/"):
            return bool(os.environ.get("OPENAI_API_KEY"))
        if "claude" in lower or "anthropic" in lower:
            return bool(os.environ.get("ANTHROPIC_API_KEY"))
        return bool(
            os.environ.get("CEREBRAS_API_KEY")
            or os.environ.get("ZAI_API_KEY")
            or os.environ.get("MISTRAL_API_KEY")
            or os.environ.get("OPENROUTER_API_KEY")
            or os.environ.get("GROQ_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("ANTHROPIC_API_KEY")
        )

    @staticmethod
    def _is_auth_error(exc: Exception) -> bool:
        text = str(exc).lower()
        return any(
            token in text for token in ("api key", "unauthorized", "authentication", "401", "403")
        )
