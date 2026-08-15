"""NLI domain benchmark (opt-in).

Run with:
  pytest tests/integration/test_nli_benchmark.py -v --run-live

Metric is CBTE Tier-2 aligned: binary entailment detection
(gold entailment vs non-entailment), using P(entailment) >= 0.5.
3-way neutral/contradiction confusion is common for MNLI models on
unrelated premises and does not affect Tier-2 accept/escalate.
"""

from __future__ import annotations

import json

import pytest

from scales.config import PROJECT_ROOT, get_settings
from scales.services.nli_service import NLIService

PAIRS_PATH = PROJECT_ROOT / "data" / "nli_benchmark" / "domain_pairs.json"
ENTAILMENT_THRESHOLD = 0.5


@pytest.fixture
def run_live(request):
    return request.config.getoption("--run-live")


@pytest.mark.live
def test_nli_domain_benchmark_accuracy(run_live):
    if not run_live:
        pytest.skip("Pass --run-live to run NLI domain benchmark (~1.7GB model)")

    assert PAIRS_PATH.exists(), f"Missing benchmark file: {PAIRS_PATH}"
    payload = json.loads(PAIRS_PATH.read_text(encoding="utf-8"))
    pairs = payload["pairs"]
    assert len(pairs) >= 50

    settings = get_settings()
    nli = NLIService(settings.nli.model_name, device=settings.nli.device)

    correct = 0
    for row in pairs:
        pred = nli.predict(row["premise"], row["hypothesis"])
        gold_entailment = row["label"] == "entailment"
        pred_entailment = pred.entailment >= ENTAILMENT_THRESHOLD
        if gold_entailment == pred_entailment:
            correct += 1

    accuracy = correct / len(pairs)
    print(
        f"NLI binary entailment accuracy: {accuracy:.3f} ({correct}/{len(pairs)}) "
        f"@ threshold={ENTAILMENT_THRESHOLD}"
    )
    assert accuracy >= 0.80, (
        f"NLI binary accuracy {accuracy:.3f} < 0.80 — consider LLM-entailment fallback "
        "(Sprint 4 risk mitigation)"
    )
