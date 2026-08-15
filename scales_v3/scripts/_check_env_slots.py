#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scales.config import EnvSecrets

print("--- .env slots ---")
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    s = line.strip()
    if not s or s.startswith("#") or "=" not in s:
        continue
    key, _, val = s.partition("=")
    val = val.strip()
    prefix = val[:4] if val else "-"
    print(f"{key.strip()}: set={bool(val)} len={len(val)} prefix={prefix}")

s = EnvSecrets()
print("--- loader ---")
print("gemini_count", len(s.gemini_api_keys()))
print("cerebras_set", bool(s.cerebras_api_key))
print("zai_set", bool(s.zai_api_key))
print("openrouter_set", bool(s.openrouter_api_key or s.open_router_api_key))
print("groq_set", bool(s.groq_api_key))
