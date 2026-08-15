#!/usr/bin/env python3
"""Verify the SCALES v3.0 development environment (Sprint 1 checks)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _ok(msg: str) -> None:
    print(f"✓ {msg}")


def _fail(msg: str) -> None:
    print(f"✗ {msg}")


def main() -> int:
    failures = 0

    # 1. Python version
    if sys.version_info < (3, 11):
        _fail(f"Python 3.11+ required (found {sys.version.split()[0]})")
        failures += 1
    else:
        _ok(f"Python {sys.version.split()[0]}")

    # 2. Core imports for Sprint 1
    missing = []
    for package in ("pydantic", "yaml", "dotenv"):
        try:
            __import__(
                "yaml" if package == "yaml" else package if package != "dotenv" else "dotenv"
            )
        except ImportError:
            missing.append(package)
    if missing:
        _fail(f"Missing packages: {', '.join(missing)} — run pip install -r requirements.txt")
        failures += 1
    else:
        _ok("Core Sprint 1 packages importable (pydantic, pyyaml, python-dotenv)")

    # 3. Settings
    try:
        from scales.config import PROJECT_ROOT, get_secrets, get_settings, prompt_path

        settings = get_settings()
        _ok(f"settings.yaml loaded (CERA model={settings.llm.cera_model})")
    except Exception as exc:  # noqa: BLE001
        _fail(f"settings.yaml failed to load: {exc}")
        failures += 1
        return failures

    # 4. .env
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        _fail(".env file missing — copy .env.example to .env and set GOOGLE_API_KEY")
        failures += 1
    else:
        _ok(".env file exists")
        secrets = get_secrets()
        if secrets.google_api_key and secrets.google_api_key != "your-google-api-key-here":
            _ok("GOOGLE_API_KEY is set")
        else:
            _fail("GOOGLE_API_KEY is missing or still a placeholder")
            failures += 1

    # 5. Prompt templates
    for name in ("cera_extraction.txt", "cgr_grading.txt", "cgr_perturbation.txt"):
        path = prompt_path(name)
        if path.exists():
            _ok(f"Prompt template present: {name}")
        else:
            _fail(f"Missing prompt template: {name}")
            failures += 1

    # 6. Data directories writable
    for rel in ("data/exams", "data/calibration", "logs", "results"):
        path = PROJECT_ROOT / rel
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write_test"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            _ok(f"Writable: {rel}/")
        except OSError as exc:
            _fail(f"Not writable: {rel}/ ({exc})")
            failures += 1

    # 7. Optional heavy deps (informational for Sprint 1)
    for package, label in (
        ("litellm", "LiteLLM"),
        ("transformers", "transformers"),
        ("torch", "torch"),
    ):
        try:
            __import__(package)
            _ok(f"{label} installed")
        except ImportError:
            print(f"• {label} not installed yet (required from Sprint 2)")

    # 8. NLI cache (informational)
    try:
        from huggingface_hub import try_to_load_from_cache

        cached = try_to_load_from_cache(settings.nli.model_name, "config.json")
        if cached:
            _ok(f"NLI model appears cached: {settings.nli.model_name}")
        else:
            print("• NLI model not cached yet — run: python scripts/download_models.py")
    except Exception:
        print("• Could not check HuggingFace cache (optional for Sprint 1)")

    print()
    if failures:
        print(f"Setup incomplete: {failures} issue(s) found.")
        return 1

    print("Setup complete for Sprint 1 foundation. Ready to continue to Sprint 2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
