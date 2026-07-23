"""Live smoke tests for Sprint 2 services (opt-in, costs money / downloads model).

Run with:
  pytest tests/integration/test_services_live.py -v --run-live
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, Field

from scales.config import get_secrets, get_settings
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIService


@pytest.fixture
def run_live(request):
    return request.config.getoption("--run-live")


class SmokeReply(BaseModel):
    ok: bool
    message: str = Field(min_length=1)


@pytest.mark.live
@pytest.mark.asyncio
async def test_live_llm_call(run_live):
    if not run_live:
        pytest.skip("Pass --run-live to execute live LLM smoke test")
    secrets = get_secrets()
    assert secrets.google_api_key, "GOOGLE_API_KEY required"
    settings = get_settings()
    client = LLMClient(settings.llm)
    result = await client.call(
        model=settings.llm.cgr_model,
        system_prompt="You return compact JSON only.",
        user_prompt='Reply with ok=true and message="hello".',
        response_schema=SmokeReply,
    )
    assert result.ok is True
    assert result.message
    usage = client.get_usage()
    assert usage["total_calls"] == 1


@pytest.mark.live
def test_live_nli_entailment(run_live):
    if not run_live:
        pytest.skip("Pass --run-live to execute live NLI smoke test")
    settings = get_settings()
    nli = NLIService(settings.nli.model_name, device=settings.nli.device)
    pred = nli.predict("A cat is an animal", "There is an animal")
    assert pred.entailment > 0.5
