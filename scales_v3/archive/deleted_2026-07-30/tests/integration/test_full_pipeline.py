"""Integration: CERA → CGR → CBTE with mocked LLM/NLI (free, no API)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from scales.config import CBTEConfig, LLMConfig
from scales.models.exam import QuestionInput
from scales.models.grading import Verdict
from scales.models.trust import TrustDecision
from scales.modules.cbte import CBTEModule
from scales.modules.cera import CERAExtractionResponse, CERAModule, CQAExtractionItem
from scales.modules.cgr import CGRModule
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIPrediction


def _cqa_item(n: int, kp: str, keywords: list[str]) -> CQAExtractionItem:
    facet = " ".join(keywords) if keywords else kp
    return CQAExtractionItem(
        concept_id=f"Q1_C{n}",
        knowledge_point=kp,
        target_criteria=kp,
        marks=1,
        evidence_facets=[facet],
        evidence_mode="ANY",
        expected_keywords=keywords,
        acceptable_variants=[],
        partial_credit_rule=None,
        source_rubric_span=f"1 mark for {kp}",
        source_reference_span=kp,
    )


@pytest.mark.asyncio
async def test_mocked_cera_cgr_cbte_pipeline(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")
    client = LLMClient(LLMConfig(max_retries=0, retry_delay_seconds=0.01))

    question = QuestionInput(
        question_id="Q1",
        question_text="Explain the three-way handshake in TCP.",
        reference_answer="TCP uses SYN, SYN-ACK, ACK for a reliable handshake.",
        rubric="1 each: name, SYN, SYN-ACK, purpose",
        total_marks=4,
    )

    # ── CERA (mocked) ──
    cera = CERAModule(client, max_validation_retries=1)
    cera.llm.call = AsyncMock(
        return_value=CERAExtractionResponse(
            cqa_tuples=[
                _cqa_item(1, "three-way handshake named", ["three-way", "handshake"]),
                _cqa_item(2, "client sends SYN", ["SYN", "client"]),
                _cqa_item(3, "server SYN-ACK", ["SYN-ACK", "server"]),
                _cqa_item(4, "purpose synchronization", ["reliable", "ready"]),
            ]
        )
    )
    cera_out = await cera.extract_concepts(question)
    assert sum(c.marks for c in cera_out.cqa_tuples) == 4

    # ── CGR (mocked per concept) ──
    cgr = CGRModule(client, max_validation_retries=1)

    async def fake_cgr_call(**kwargs):
        prompt = kwargs["user_prompt"]
        schema = kwargs["response_schema"]
        # Map concept from prompt
        if "Q1_C1" in prompt:
            return schema(
                concept_id="Q1_C1",
                verdict=Verdict.FULL,
                marks_awarded=1.0,
                evidence_span="three-way handshake",
                reasoning="Student names the three-way handshake clearly.",
                counter_arguments="None.",
            )
        if "Q1_C2" in prompt:
            return schema(
                concept_id="Q1_C2",
                verdict=Verdict.FULL,
                marks_awarded=1.0,
                evidence_span="client sends a SYN packet",
                reasoning="Student mentions client SYN transmission.",
                counter_arguments="None.",
            )
        if "Q1_C3" in prompt:
            return schema(
                concept_id="Q1_C3",
                verdict=Verdict.PARTIAL,
                marks_awarded=0.5,
                evidence_span="acknowledgment along with its own SYN",
                reasoning="Describes SYN-ACK functionally without the term.",
                counter_arguments="Missing explicit SYN-ACK token.",
            )
        return schema(
            concept_id="Q1_C4",
            verdict=Verdict.FULL,
            marks_awarded=1.0,
            evidence_span="both sides are ready",
            reasoning="States purpose of readiness/synchronization.",
            counter_arguments="None.",
        )

    cgr.llm.call = AsyncMock(side_effect=fake_cgr_call)

    student_answer = (
        "TCP establishes a connection using a three-way handshake. "
        "The client sends a SYN packet. The server then replies with an "
        "acknowledgment along with its own SYN. After the client confirms, "
        "the connection is established. This ensures both sides are ready."
    )
    cgr_results = await cgr.grade_all_concepts(
        student_id="STU004",
        student_answer=student_answer,
        cqa_list=cera_out.cqa_tuples,
        question_text=question.question_text,
    )
    assert len(cgr_results) == 4
    assert cgr_results[0].verdict == Verdict.FULL
    assert cgr_results[2].verdict == Verdict.PARTIAL

    # ── CBTE (mocked NLI) ──
    nli = MagicMock()
    nli.is_loaded.return_value = True
    nli.predict.return_value = NLIPrediction(entailment=0.55, contradiction=0.1, neutral=0.35)
    nli.predict_batch.side_effect = lambda pairs: [
        NLIPrediction(entailment=0.55, contradiction=0.1, neutral=0.35) for _ in pairs
    ]

    cbte = CBTEModule(
        nli_service=nli,
        config=CBTEConfig(tier1_keyword_threshold=0.3, tier2_nli_threshold=0.7, tau=0.5),
    )

    trust_results = []
    for cgr_result, cqa in zip(cgr_results, cera_out.cqa_tuples):
        trust_results.append(cbte.evaluate(cgr_result, student_answer, cqa))

    assert len(trust_results) == 4
    # C1/C2/C4 should have strong keywords → Tier 1 accept
    assert trust_results[0].decision == TrustDecision.ACCEPT
    assert trust_results[0].tier_resolved == 1
    assert trust_results[1].decision == TrustDecision.ACCEPT
    # C3 may escalate (keyword SYN-ACK missing) → Tier 2/3
    assert trust_results[2].tier_resolved in (1, 2, 3)
    assert all(r.signal_1_evidence_verified for r in trust_results)

    accepted = sum(1 for r in trust_results if r.decision == TrustDecision.ACCEPT)
    deferred = sum(1 for r in trust_results if r.decision == TrustDecision.DEFER)
    assert accepted + deferred == 4
    assert accepted >= 2  # pipeline should auto-accept clear concepts
