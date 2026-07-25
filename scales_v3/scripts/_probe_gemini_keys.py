#!/usr/bin/env python3
"""Probe each Gemini key separately (no Cerebras)."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


async def probe_key(idx: int, key: str) -> None:
    import litellm

    litellm.suppress_debug_info = True
    os.environ["GOOGLE_API_KEY"] = key
    os.environ["GEMINI_API_KEY"] = key
    try:
        r = await litellm.acompletion(
            model="gemini/gemini-3.1-flash-lite",
            api_key=key,
            messages=[{"role": "user", "content": 'Return only json: {"ok": true}'}],
            max_tokens=32,
            timeout=45,
            response_format={"type": "json_object"},
        )
        text = (r.choices[0].message.content or "").strip().replace("\n", " ")
        print(f"gemini_key_{idx}: OK   {text[:50]}")
    except Exception as exc:  # noqa: BLE001
        msg = str(exc).replace("\n", " ")
        if "429" in msg or "rate" in msg.lower() or "quota" in msg.lower():
            short = "RATE/QUOTA (429)"
        elif "401" in msg or "403" in msg or "auth" in msg.lower() or "invalid" in msg.lower():
            short = "AUTH/INVALID"
        else:
            short = f"{type(exc).__name__}: {msg[:100]}"
        print(f"gemini_key_{idx}: FAIL {short}")


async def main() -> int:
    from scales.config import EnvSecrets

    keys = EnvSecrets().gemini_api_keys()
    print(f"probing {len(keys)} gemini keys (cerebras skipped)")
    for i, key in enumerate(keys, 1):
        await probe_key(i, key)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
