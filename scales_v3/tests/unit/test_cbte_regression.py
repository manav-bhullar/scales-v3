"""L5 — CBTE decision-surface pinning + frozen Wave3 offline replay (Step 6)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from scales.config import CBTEConfig, CBTETier3Weights
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.trust import TrustDecision
from scales.modules.cbte import CBTEModule
from scales.services.nli_service import NLIPrediction

PROJECT = Path(__file__).resolve().parents[2]
WAVE3_EXAM = PROJECT / "data" / "exams" / "e2e_wave3_tcp_handshake_expanded"
WAVE3_GOLD = PROJECT / "data" / "e2e_eval" / "wave3" / "gold_labels.json"


def _load_metrics():
    spec = importlib.util.spec_from_file_location(
        "metrics_ledger_reg",
        PROJECT / "scripts" / "metrics_ledger.py",
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _cfg() -> CBTEConfig:
    return CBTEConfig(
        tier1_keyword_threshold=0.3,
        tier2_nli_threshold=0.7,
        tier3_weights=CBTETier3Weights(nli=0.4, stability=0.3, keyword=0.3),
        tau=0.5,
        tau_source="manual",
        enable_tier3=False,
    )


def _cqa(**kwargs) -> CQATuple:
    base = dict(
        concept_id="Q1_C1",
        question_id="Q1",
        knowledge_point="TCP three-way handshake",
        marks=1,
        expected_keywords=["SYN", "handshake"],
        acceptable_variants=[],
    )
    base.update(kwargs)
    return CQATuple(**base)


def _cgr(**kwargs) -> CGRResult:
    base = dict(
        student_id="S1",
        concept_id="Q1_C1",
        verdict=Verdict.FULL,
        marks_awarded=1.0,
        evidence_span="three-way handshake with SYN",
        reasoning="Unit-test reasoning that is long enough.",
        counter_arguments="None.",
    )
    base.update(kwargs)
    return CGRResult(**base)


def _nli(entailment: float = 0.9) -> MagicMock:
    service = MagicMock()
    service.is_loaded.return_value = True
    service.predict.return_value = NLIPrediction(
        entailment=entailment,
        contradiction=0.05,
        neutral=max(0.0, 1.0 - entailment - 0.05),
    )
    service.predict_batch.side_effect = lambda pairs: [
        NLIPrediction(entailment=entailment, contradiction=0.05, neutral=0.05) for _ in pairs
    ]
    return service


@pytest.mark.regression
def test_decision_surface_absent_scarce_keywords_auto_accepts():
    """ABSENT + no keyword hits → Tier1 ACCEPT (confirmed empty)."""
    cbte = CBTEModule(_nli(), config=_cfg())
    result = cbte.evaluate(
        _cgr(verdict=Verdict.ABSENT, marks_awarded=0.0, evidence_span=""),
        student_answer="I honestly have no idea about this topic.",
        cqa=_cqa(expected_keywords=["isolation", "concurrent"]),
    )
    assert result.decision == TrustDecision.ACCEPT
    assert result.tier_resolved == 1
    assert result.trust_score == 0.90


@pytest.mark.regression
def test_decision_surface_hallucinated_evidence_defers():
    cbte = CBTEModule(_nli(), config=_cfg())
    result = cbte.evaluate(
        _cgr(evidence_span="this quote is not in the answer"),
        student_answer="TCP uses a three-way handshake with SYN.",
        cqa=_cqa(),
    )
    assert result.decision == TrustDecision.DEFER
    assert result.tier_resolved == 1
    assert result.trust_score == 0.0


@pytest.mark.regression
def test_decision_surface_full_with_keywords_tier1_accept():
    cbte = CBTEModule(_nli(), config=_cfg())
    answer = "TCP uses a three-way handshake. Client sends SYN."
    result = cbte.evaluate(
        _cgr(evidence_span="three-way handshake"),
        student_answer=answer,
        cqa=_cqa(),
    )
    assert result.decision == TrustDecision.ACCEPT
    assert result.tier_resolved == 1


@pytest.mark.regression
def test_decision_surface_suspicious_absent_escalates():
    """ABSENT but keywords present must not Tier-1 accept."""
    cbte = CBTEModule(_nli(entailment=0.2), config=_cfg())
    answer = "Threads share the process address space and use SYN weirdly."
    result = cbte.evaluate(
        _cgr(verdict=Verdict.ABSENT, marks_awarded=0.0, evidence_span=""),
        student_answer=answer,
        cqa=_cqa(expected_keywords=["SYN", "handshake"]),
    )
    assert result.tier_resolved >= 2
    # With low NLI and tau=0.5 → DEFER at Tier 3
    assert result.decision == TrustDecision.DEFER


@pytest.mark.regression
@pytest.mark.skipif(
    not (WAVE3_EXAM / "grading_results.json").exists(),
    reason="Frozen Wave3 exam artifacts not present",
)
def test_frozen_wave3_metrics_invariants():
    """Pin safety + known harshness on the committed Wave3 run."""
    ml = _load_metrics()
    grading = json.loads((WAVE3_EXAM / "grading_results.json").read_text(encoding="utf-8"))
    gold = json.loads(WAVE3_GOLD.read_text(encoding="utf-8"))
    m = ml.compute_metrics(grading, gold)

    assert m["n_students"] == 24
    assert m["n_items"] == 96
    assert m["false_accept_count"] == 0  # safety must not regress
    assert m["defer_rate"] == pytest.approx(0.2917, abs=1e-3)
    assert m["band_hit_rate"] == pytest.approx(0.375, abs=1e-3)
    # Wave3 GOOD misses are mostly DEFER-held marks (not silent ABSENT accepts)
    assert m["silent_zero_count"] == 0
    assert len(m["zeroed_students"]) >= 4  # mid/partial wiped provisional
    assert m["underscored_students"] > m["overscored_students"]

    report = ml.evaluate_pass_bar(m)
    assert report["pass"] is False
    assert "no_false_accept_on_low" not in report["failed"]
    assert "no_silent_zeros" not in report["failed"]
    assert "high_band_students_in_band" in report["failed"]
