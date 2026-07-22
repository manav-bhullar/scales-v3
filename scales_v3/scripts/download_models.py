#!/usr/bin/env python3
"""Download and cache the DeBERTa-NLI model used by CBTE Tier 2."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    try:
        from scales.config import get_settings
    except Exception as exc:  # noqa: BLE001
        print(f"✗ Failed to import scales.config: {exc}")
        print("  Tip: pip install -r requirements.txt")
        return 1

    settings = get_settings()
    model_name = settings.nli.model_name
    print(f"Downloading NLI model: {model_name}")
    print("This may take several minutes (~1.7 GB) on first run.")

    try:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
    except ImportError:
        print("✗ transformers is not installed. Run: pip install -r requirements.txt")
        return 1

    try:
        AutoTokenizer.from_pretrained(model_name)
        AutoModelForSequenceClassification.from_pretrained(model_name)
    except Exception as exc:  # noqa: BLE001
        print(f"✗ Model download failed: {exc}")
        return 1

    print("✓ Model downloaded and cached.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
