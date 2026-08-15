"""Integration: full lifecycle CERA→CGR→CBTE→SHRR→Aggregator (mocked)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from scales.config import LLMConfig
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.grading import Verdict
from scales.models.trust import TrustDecision
from scales.modules.cera import CERAExtractionResponse, CQAExtractionItem
from scales.persistence import ExamStore
from scales.pipeline import GradingPipeline
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIPrediction


def _cqa_item(n: int, kp: str, keywords: list[str]) -> CQAExtractionItem:
    return CQAExtractionItem(
        concept_id=f"Q1_C{n}",
        knowledge_point=kp,
        target_criteria=kp,
        marks=1,
        evidence_facets=[kp],
        evidence_mode="ANY",
        expected_keywords=keywords,
        acceptable_variants=[],
        partial_credit_rule=None,
        source_rubric_span=f"1 mark for {kp}",
        source_reference_span=kp,
    )


@pytest.mark.asyncio
async def test_full_lifecycle_with_review_and_resume(tmp_path, monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")
    client = LLMClient(LLMConfig(max_retries=0, retry_delay_seconds=0.01))

    # Low NLI → force Tier 3 / possible DEFER on weak answers
    nli = MagicMock()
    nli.is_loaded.return_value = True
    nli.predict.return_value = NLIPrediction(entailment=0.2, contradiction=0.1, neutral=0.7)
    nli.predict_batch.side_effect = lambda pairs: [NLIPrediction(0.2, 0.1, 0.7) for _ in pairs]

    exam = ExamInput(
        exam_id="exam_lifecycle",
        subject="Networks",
        questions=[
            QuestionInput(
                question_id="Q1",
                question_text="Explain the three-way handshake in TCP.",
                reference_answer="TCP uses SYN, SYN-ACK, ACK.",
                rubric="1 each: name, SYN",
                total_marks=2,
                student_answers=[
                    StudentAnswer(
                        student_id="S1",
                        answer_text="TCP uses a three-way handshake. Client sends SYN.",
                    ),
                    StudentAnswer(
                        student_id="S2",
                        answer_text="Something vague about connections.",
                    ),
                ],
            )
        ],
    )

    store = ExamStore(exam.exam_id, exams_dir=tmp_path)
    pipeline = GradingPipeline(client, nli, exam_store=store)

    cera_response = CERAExtractionResponse(
        cqa_tuples=[
            _cqa_item(1, "three-way handshake named", ["three-way", "handshake"]),
            _cqa_item(2, "client sends SYN", ["SYN", "client"]),
        ]
    )

    async def fake_llm(**kwargs):
        schema = kwargs["response_schema"]
        prompt = kwargs.get("user_prompt", "")
        if (
            schema is CERAExtractionResponse
            or getattr(schema, "__name__", "") == "CERAExtractionResponse"
        ):
            return cera_response
        # CGR
        is_s1 = "three-way handshake" in prompt and "Client sends SYN" in prompt
        if "Q1_C1" in prompt or "three-way handshake named" in prompt:
            if is_s1:
                return schema(
                    concept_id="Q1_C1",
                    verdict=Verdict.FULL,
                    marks_awarded=1.0,
                    evidence_span="three-way handshake",
                    reasoning="Student named the three-way handshake clearly.",
                    counter_arguments="None noted.",
                )
            return schema(
                concept_id="Q1_C1",
                verdict=Verdict.PARTIAL,
                marks_awarded=0.5,
                evidence_span="connections",
                reasoning="Only a vague mention of connections was found.",
                counter_arguments="Handshake steps unclear.",
            )
        if is_s1:
            return schema(
                concept_id="Q1_C2",
                verdict=Verdict.FULL,
                marks_awarded=1.0,
                evidence_span="Client sends SYN",
                reasoning="Student explicitly mentions client sending SYN.",
                counter_arguments="None noted.",
            )
        return schema(
            concept_id="Q1_C2",
            verdict=Verdict.ABSENT,
            marks_awarded=0.0,
            evidence_span="",
            reasoning="No SYN step is present in the student answer.",
            counter_arguments="Concept missing entirely.",
        )

    client.call = AsyncMock(side_effect=fake_llm)

    phase1 = await pipeline.run_grading_phase(exam, resume=False, calibrate=False)
    assert set(phase1.graded_students) == {"S1", "S2"}
    assert store.grading_path.exists()

    # Resume should skip re-grading (already complete)
    phase1b = await pipeline.run_grading_phase(exam, resume=True)
    assert set(phase1b.graded_students) == {"S1", "S2"}

    queue = pipeline.get_review_queue()
    # Resolve any deferred items with teacher UPGRADE/AGREE
    for item in queue:
        pipeline.submit_correction(
            student_id=item.student_id,
            concept_id=item.concept_id,
            teacher_verdict=Verdict.FULL
            if item.system_verdict != Verdict.FULL
            else item.system_verdict,
            teacher_marks=float(item.max_marks)
            if item.system_verdict != Verdict.FULL
            else item.system_marks,
            teacher_comment="reviewed",
        )

    assert pipeline.get_review_progress().is_complete
    phase2 = pipeline.run_review_phase()
    assert len(phase2.final_results) == 2
    assert store.final_path.exists()
    assert all(fr.all_concepts_resolved for fr in phase2.final_results)

    # Reload from disk
    pipeline2 = GradingPipeline(client, nli, exam_store=ExamStore(exam.exam_id, exams_dir=tmp_path))
    pipeline2.load_from_store()
    assert pipeline2.get_grading_status().final_results_count == 2


@pytest.mark.asyncio
async def test_no_deferrals_auto_finalizes(tmp_path, monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-not-real")
    client = LLMClient(LLMConfig(max_retries=0, retry_delay_seconds=0.01))
    nli = MagicMock()
    nli.is_loaded.return_value = True
    nli.predict.return_value = NLIPrediction(0.95, 0.02, 0.03)
    nli.predict_batch.side_effect = lambda pairs: [NLIPrediction(0.95, 0.02, 0.03) for _ in pairs]

    exam = ExamInput(
        exam_id="exam_auto",
        questions=[
            QuestionInput(
                question_id="Q1",
                question_text="Explain TCP handshake.",
                reference_answer="SYN SYN-ACK ACK",
                total_marks=1,
                student_answers=[
                    StudentAnswer(
                        student_id="S1",
                        answer_text="TCP uses a three-way handshake with SYN.",
                    )
                ],
            )
        ],
    )
    store = ExamStore(exam.exam_id, exams_dir=tmp_path)
    pipeline = GradingPipeline(client, nli, exam_store=store)
    cera_response = CERAExtractionResponse(
        cqa_tuples=[_cqa_item(1, "three-way handshake named", ["three-way", "handshake", "SYN"])]
    )

    async def fake_llm(**kwargs):
        schema = kwargs["response_schema"]
        if (
            schema is CERAExtractionResponse
            or getattr(schema, "__name__", "") == "CERAExtractionResponse"
        ):
            return cera_response
        return schema(
            concept_id="Q1_C1",
            verdict=Verdict.FULL,
            marks_awarded=1.0,
            evidence_span="three-way handshake",
            reasoning="Student clearly names the three-way handshake.",
            counter_arguments="None noted.",
        )

    client.call = AsyncMock(side_effect=fake_llm)
    phase1 = await pipeline.run_grading_phase(exam, resume=False, calibrate=False)
    assert phase1.deferred_count == 0
    assert phase1.status is not None
    assert phase1.status.final_results_count == 1
    assert all(r.decision == TrustDecision.ACCEPT for r in phase1.cbte_results)
