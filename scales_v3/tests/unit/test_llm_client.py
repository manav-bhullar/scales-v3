"""Unit tests for LLMClient (mocked LiteLLM)."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel, Field

from scales.config import LLMConfig
from scales.services.exceptions import LLMAPIError, LLMValidationError
from scales.services.llm_client import LLMClient


class DummySchema(BaseModel):
    verdict: str
    marks: float = Field(ge=0)


def _fake_response(content: str, prompt_tokens: int = 10, completion_tokens: int = 5):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens),
    )


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")
    return LLMClient(LLMConfig(max_retries=2, retry_delay_seconds=0.01, temperature=0.1))


@pytest.mark.asyncio
async def test_call_returns_validated_model(client):
    payload = {"verdict": "FULL", "marks": 1.0}
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = _fake_response(json.dumps(payload))
        result = await client.call(
            model="gemini/gemini-2.0-flash",
            system_prompt="sys",
            user_prompt="user",
            response_schema=DummySchema,
        )
    assert result.verdict == "FULL"
    assert result.marks == 1.0
    usage = client.get_usage()
    assert usage["total_calls"] == 1
    assert usage["total_input_tokens"] == 10
    assert usage["total_output_tokens"] == 5


@pytest.mark.asyncio
async def test_retry_then_success(client):
    payload = {"verdict": "ABSENT", "marks": 0.0}
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_call:
        mock_call.side_effect = [
            RuntimeError("429 rate limit"),
            _fake_response(json.dumps(payload)),
        ]
        result = await client.call(
            model="gemini/gemini-2.0-flash",
            system_prompt="sys",
            user_prompt="user",
            response_schema=DummySchema,
        )
    assert result.verdict == "ABSENT"
    assert mock_call.await_count == 2


@pytest.mark.asyncio
async def test_validation_correction_retry(client):
    bad = {"verdict": "FULL"}  # missing marks
    good = {"verdict": "FULL", "marks": 1.0}
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_call:
        mock_call.side_effect = [
            _fake_response(json.dumps(bad)),
            _fake_response(json.dumps(good)),
        ]
        result = await client.call(
            model="gemini/gemini-2.0-flash",
            system_prompt="sys",
            user_prompt="grade this",
            response_schema=DummySchema,
        )
    assert result.marks == 1.0
    # Second call prompt should include validation error feedback
    second_messages = mock_call.await_args_list[1].kwargs["messages"]
    assert "validation errors" in second_messages[-1]["content"].lower()


@pytest.mark.asyncio
async def test_api_failure_after_retries(client):
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_call:
        mock_call.side_effect = RuntimeError("500 server error")
        with pytest.raises(LLMAPIError):
            await client.call(
                model="gemini/gemini-2.0-flash",
                system_prompt="sys",
                user_prompt="user",
                response_schema=DummySchema,
            )


@pytest.mark.asyncio
async def test_persistent_validation_error(client):
    bad = {"verdict": "FULL"}
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = _fake_response(json.dumps(bad))
        with pytest.raises(LLMValidationError):
            await client.call(
                model="gemini/gemini-2.0-flash",
                system_prompt="sys",
                user_prompt="user",
                response_schema=DummySchema,
            )


def test_usage_accumulates(client):
    client._record_usage({"input_tokens": 100, "output_tokens": 20})
    client._record_usage({"input_tokens": 50, "output_tokens": 10})
    usage = client.get_usage()
    assert usage["total_calls"] == 2
    assert usage["total_input_tokens"] == 150
    assert usage["total_output_tokens"] == 30
    assert usage["estimated_cost_usd"] >= 0
