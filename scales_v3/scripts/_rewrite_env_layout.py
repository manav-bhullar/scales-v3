#!/usr/bin/env python3
"""Rewrite .env: drop DeepSeek, add Cerebras + multi-Gemini slots; keep existing secrets."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"


def main() -> None:
    raw = ENV.read_text(encoding="utf-8") if ENV.exists() else ""
    vals: dict[str, str] = {}
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        key, _, value = s.partition("=")
        key = key.strip().upper()
        if key.startswith("DEEPSEEK"):
            continue
        vals[key] = value.strip()

    def get(*names: str) -> str:
        for name in names:
            if vals.get(name):
                return vals[name]
        return ""

    google = get("GOOGLE_API_KEY", "GOOGLE_API_KEY_1")
    lines = [
        "# SCALES v3.0 — API keys (never commit this file)",
        "# DeepSeek removed (paid). Fill Cerebras + extra Gemini keys as needed.",
        "",
        "# --- Gemini (Google AI Studio) — up to 5 keys for rate-limit rotation ---",
        f"GOOGLE_API_KEY={google}",
        f"GOOGLE_API_KEY_2={get('GOOGLE_API_KEY_2')}",
        f"GOOGLE_API_KEY_3={get('GOOGLE_API_KEY_3')}",
        f"GOOGLE_API_KEY_4={get('GOOGLE_API_KEY_4')}",
        f"GOOGLE_API_KEY_5={get('GOOGLE_API_KEY_5')}",
        "",
        "# --- Cerebras (https://cloud.cerebras.ai) ---",
        f"CEREBRAS_API_KEY={get('CEREBRAS_API_KEY')}",
        "",
        "# --- Z.ai GLM ---",
        f"ZAI_API_KEY={get('ZAI_API_KEY', 'Z_AI_API_KEY')}",
        "",
        "# --- OpenRouter / Groq ---",
        f"OPENROUTER_API_KEY={get('OPENROUTER_API_KEY', 'OPEN_ROUTER_API_KEY')}",
        f"GROQ_API_KEY={get('GROQ_API_KEY')}",
        "",
        "# --- Mistral (https://console.mistral.ai) ---",
        f"MISTRAL_API_KEY={get('MISTRAL_API_KEY')}",
        "",
        "# --- Optional ---",
        f"OPENAI_API_KEY={get('OPENAI_API_KEY')}",
        f"ANTHROPIC_API_KEY={get('ANTHROPIC_API_KEY')}",
        "",
    ]
    ENV.write_text("\n".join(lines), encoding="utf-8")
    print("rewrote", ENV)


if __name__ == "__main__":
    main()
