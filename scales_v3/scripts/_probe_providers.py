#!/usr/bin/env python3
"""Probe which configured LLM providers currently answer a small JSON request.

Usage (from scales_v3/):
  python scripts/_probe_providers.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MODELS = [
    "cerebras/llama3.1-8b",
    "cerebras/llama-3.3-70b",
    "zai/glm-4.7",
    "zai/glm-4.5-flash",
    "groq/llama-3.3-70b-versatile",
    "groq/llama-3.1-8b-instant",
    "gemini/gemini-2.0-flash",
    "openrouter/meta-llama/llama-3.3-70b-instruct",
]


def _load_keys() -> None:
    from scales.config import get_secrets

    secrets = get_secrets()
    pairs = [
        ("CEREBRAS_API_KEY", secrets.cerebras_api_key),
        ("ZAI_API_KEY", secrets.zai_api_key or secrets.z_ai_api_key),
        ("ZAI_API_BASE", secrets.zai_api_base),
        ("OPENROUTER_API_KEY", secrets.openrouter_api_key or secrets.open_router_api_key),
        ("GROQ_API_KEY", secrets.groq_api_key),
        ("MISTRAL_API_KEY", secrets.mistral_api_key),
    ]
    for name, value in pairs:
        if value:
            os.environ[name] = value
    keys = secrets.gemini_api_keys()
    if keys:
        os.environ["GOOGLE_API_KEY"] = keys[0]
        os.environ["GEMINI_API_KEY"] = keys[0]


def _kwargs_for(model: str) -> dict:
    lower = model.lower()
    if lower.startswith("zai/") or lower.startswith("zhipu/"):
        bare = model.split("/", 1)[1]
        return {
            "model": f"openai/{bare}",
            "api_base": (os.environ.get("ZAI_API_BASE") or "https://api.z.ai/api/paas/v4").rstrip(
                "/"
            ),
            "api_key": os.environ.get("ZAI_API_KEY") or "",
            "custom_llm_provider": "openai",
        }
    return {"model": model}


async def probe(model: str) -> None:
    import litellm

    try:
        response = await litellm.acompletion(
            **_kwargs_for(model),
            messages=[{"role": "user", "content": 'Return only json: {"ok": true}'}],
            max_tokens=64,
            timeout=45,
            response_format={"type": "json_object"},
        )
        text = (response.choices[0].message.content or "").strip().replace("\n", " ")
        print(f"{model:46s} OK    {text[:60]}")
    except Exception as exc:  # noqa: BLE001
        detail = str(exc).replace("\n", " ")
        print(f"{model:46s} FAIL  {type(exc).__name__}: {detail[:120]}")


async def main() -> int:
    _load_keys()
    import litellm

    litellm.suppress_debug_info = True
    from scales.config import get_secrets

    secrets = get_secrets()
    print(f"gemini_keys_configured={len(secrets.gemini_api_keys())}")
    print(f"cerebras_key={bool(secrets.cerebras_api_key)}")
    for model in MODELS:
        await probe(model)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
