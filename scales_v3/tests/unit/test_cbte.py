"""Unit tests for CBTEModule (mocked NLI)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from scales.config import CBTEConfig, CBTETier3Weights
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.trust import TrustDecision
from scales.modules.cbte import CBTEModule, build_verdict_hypothesis
from scales.services.nli_service import NLIPrediction


@pytest.fixture
def cqa() -> CQATuple:
    return CQATuple(
        concept_id="Q1_C1",
        question_id="Q1",
        knowledge_point="TCP uses three-way handshake for connection establishment",
        marks=1,
        expected_keywords=["three-way", "handshake", "SYN"],
        acceptable_variants=["3-step connection setup"],
    )


@pytest.fixture
def cbte_config() -> CBTEConfig:
    return CBTEConfig(
        tier1_keyword_threshold=0.3,
        tier2_nli_threshold=0.7,
        tier3_weights=CBTETier3Weights(nli=0.4, stability=0.3, keyword=0.3),
        tau=0.5,
        tau_source="manual",
        enable_tier3=False,
    )


def _mock_nli(entailment: float = 0.9) -> MagicMock:
    service = MagicMock()
    service.is_loaded.return_value = True
    service.predict.return_value = NLIPrediction(
        entailment=entailment, contradiction=0.05, neutral=max(0.0, 1.0 - entailment - 0.05)
    )
    service.predict_batch.side_effect = lambda pairs: [
        NLIPrediction(entailment=entailment, contradiction=0.05, neutral=0.05) for _ in pairs
    ]
    return service


def _cgr(
    *,
    verdict: Verdict,
    evidence: str,
    marks: float = 1.0,
    student_id: str = "STU001",
    concept_id: str = "Q1_C1",
) -> CGRResult:
    return CGRResult(
        student_id=student_id,
        concept_id=concept_id,
        verdict=verdict,
        marks_awarded=marks,
        evidence_span=evidence,
        reasoning="Unit-test reasoning that is long enough.",
        counter_arguments="None.",
    )


def test_build_verdict_hypothesis_variants():
    kp = "SYN-ACK response"
    # Bare knowledge point (MNLI-compatible); verdict does not wrap the text.
    assert build_verdict_hypothesis(kp, Verdict.FULL) == kp
    assert build_verdict_hypothesis(kp, Verdict.PARTIAL) == kp
    assert build_verdict_hypothesis(kp, Verdict.INCORRECT) == kp
    assert build_verdict_hypothesis(kp, Verdict.ABSENT) == kp


def test_tier1_hallucinated_evidence_defers(cbte_config, cqa):
    module = CBTEModule(_mock_nli(), config=cbte_config)
    answer = "TCP uses a three-way handshake with SYN and ACK."
    cgr = _cgr(verdict=Verdict.FULL, evidence="UDP datagram checksum")
    result = module.evaluate(cgr, answer, cqa)
    assert result.decision == TrustDecision.DEFER
    assert result.tier_resolved == 1
    assert result.trust_score == 0.0
    assert result.signal_1_evidence_verified is False


def test_tier1_clean_pass_full(cbte_config, cqa):
    module = CBTEModule(_mock_nli(), config=cbte_config)
    answer = "TCP establishes a connection using a three-way handshake. Client sends SYN."
    cgr = _cgr(verdict=Verdict.FULL, evidence="three-way handshake")
    result = module.evaluate(cgr, answer, cqa)
    assert result.decision == TrustDecision.ACCEPT
    assert result.tier_resolved == 1
    assert result.trust_score == 0.85
    assert result.signal_1_evidence_verified is True
    assert result.signal_2_nli_score is None
    assert result.signal_4_keyword_score >= 0.3


def test_tier1_absent_confirmed(cbte_config, cqa):
    module = CBTEModule(_mock_nli(), config=cbte_config)
    answer = "HTTP uses GET and POST for web browsing."
    cgr = _cgr(verdict=Verdict.ABSENT, evidence="", marks=0.0)
    result = module.evaluate(cgr, answer, cqa)
    assert result.decision == TrustDecision.ACCEPT
    assert result.tier_resolved == 1
    assert result.trust_score == 0.90
    assert "ABSENT" in result.reason


def test_tier1_suspicious_absent_escalates(cbte_config, cqa):
    """ABSENT but keywords present → must not Tier-1 accept (A-9)."""
    module = CBTEModule(_mock_nli(entailment=0.2), config=cbte_config)
    answer = "The three-way handshake uses SYN then SYN-ACK then ACK."
    cgr = _cgr(verdict=Verdict.ABSENT, evidence="", marks=0.0)
    result = module.evaluate(cgr, answer, cqa)
    assert result.tier_resolved in (2, 3)
    # Should not be the Tier-1 ABSENT auto-accept
    assert not (result.tier_resolved == 1 and result.trust_score == 0.90)


def test_tier1_low_keywords_escalates(cbte_config, cqa):
    module = CBTEModule(_mock_nli(entailment=0.85), config=cbte_config)
    # Evidence is real but uses paraphrase with almost no expected keywords
    answer = "Hosts exchange packets to open a session reliably."
    cgr = _cgr(verdict=Verdict.FULL, evidence="exchange packets to open a session")
    result = module.evaluate(cgr, answer, cqa)
    # keyword_score near 0 → Tier 2; high NLI → accept at tier 2
    assert result.tier_resolved == 2
    assert result.decision == TrustDecision.ACCEPT
    assert result.signal_2_nli_score is not None
    assert result.signal_2_nli_score >= 0.7


def test_tier2_nli_accepts(cbte_config, cqa):
    module = CBTEModule(_mock_nli(entailment=0.8), config=cbte_config)
    answer = "Hosts exchange packets to open a session reliably."
    cgr = _cgr(verdict=Verdict.PARTIAL, evidence="open a session reliably", marks=0.5)
    result = module.evaluate(cgr, answer, cqa)
    assert result.tier_resolved == 2
    assert result.decision == TrustDecision.ACCEPT
    assert result.signal_2_nli_score == pytest.approx(0.8)


def test_tier2_nli_borderline_goes_to_tier3(cbte_config, cqa):
    module = CBTEModule(_mock_nli(entailment=0.65), config=cbte_config)
    answer = "Hosts exchange packets to open a session."
    cgr = _cgr(verdict=Verdict.FULL, evidence="open a session")
    result = module.evaluate(cgr, answer, cqa)
    assert result.tier_resolved == 3
    assert result.signal_3_stability == 1.0
    assert result.signal_2_nli_score == pytest.approx(0.65)


def test_tier3_accept_when_trust_above_tau(cbte_config, cqa):
    # trust = 0.4*0.6 + 0.3*1.0 + 0.3*0.0 = 0.24+0.3+0 = 0.54 >= 0.5
    module = CBTEModule(_mock_nli(entailment=0.6), config=cbte_config)
    answer = "Something unrelated about routing tables only."
    cgr = _cgr(verdict=Verdict.FULL, evidence="Something unrelated about routing")
    result = module.evaluate(cgr, answer, cqa, tau=0.5)
    assert result.tier_resolved == 3
    assert result.decision == TrustDecision.ACCEPT
    assert result.trust_score == pytest.approx(0.54)


def test_tier3_defer_when_trust_below_tau(cbte_config, cqa):
    # trust = 0.4*0.2 + 0.3*1.0 + 0.3*0.0 = 0.08+0.3 = 0.38 < 0.5
    module = CBTEModule(_mock_nli(entailment=0.2), config=cbte_config)
    answer = "Something unrelated about routing tables only."
    cgr = _cgr(verdict=Verdict.FULL, evidence="Something unrelated about routing")
    result = module.evaluate(cgr, answer, cqa, tau=0.5)
    assert result.tier_resolved == 3
    assert result.decision == TrustDecision.DEFER
    assert result.trust_score == pytest.approx(0.38)


def test_empty_keywords_score_one_allows_tier1(cbte_config):
    cqa = CQATuple(
        concept_id="Q1_C9",
        question_id="Q1",
        knowledge_point="Purpose of handshake",
        marks=1,
        expected_keywords=[],  # vacuous score 1.0
    )
    module = CBTEModule(_mock_nli(), config=cbte_config)
    answer = "This ensures both sides are ready."
    cgr = _cgr(
        verdict=Verdict.FULL,
        evidence="both sides are ready",
        concept_id="Q1_C9",
    )
    result = module.evaluate(cgr, answer, cqa)
    assert result.tier_resolved == 1
    assert result.signal_4_keyword_score == 1.0
    assert result.decision == TrustDecision.ACCEPT


def test_normalized_evidence_match_passes_signal1(cbte_config, cqa):
    module = CBTEModule(_mock_nli(), config=cbte_config)
    answer = "TCP uses a three-way handshake. Client sends SYN."
    cgr = _cgr(verdict=Verdict.FULL, evidence="TCP  uses\na three-way handshake")
    result = module.evaluate(cgr, answer, cqa)
    assert result.signal_1_evidence_verified is True
    assert result.decision == TrustDecision.ACCEPT
    assert result.tier_resolved == 1


def test_nli_unavailable_escalates_to_tier3(cbte_config, cqa):
    module = CBTEModule(nli_service=None, config=cbte_config)
    answer = "Hosts exchange packets to open a session."
    cgr = _cgr(verdict=Verdict.FULL, evidence="open a session")
    result = module.evaluate(cgr, answer, cqa)
    assert result.tier_resolved == 3
    assert result.signal_2_nli_score == 0.0


def test_evaluate_batch_mix(cbte_config, cqa):
    module = CBTEModule(_mock_nli(entailment=0.9), config=cbte_config)
    good_answer = "TCP uses three-way handshake and SYN."
    bad_evidence_answer = "TCP uses three-way handshake and SYN."
    items = [
        (
            _cgr(verdict=Verdict.FULL, evidence="three-way handshake", student_id="S1"),
            good_answer,
            cqa,
        ),
        (
            _cgr(
                verdict=Verdict.FULL,
                evidence="hallucinated UDP claim",
                student_id="S2",
            ),
            bad_evidence_answer,
            cqa,
        ),
    ]
    results = module.evaluate_batch(items)
    assert len(results) == 2
    assert results[0].decision == TrustDecision.ACCEPT
    assert results[0].tier_resolved == 1
    assert results[1].decision == TrustDecision.DEFER
    assert results[1].tier_resolved == 1
