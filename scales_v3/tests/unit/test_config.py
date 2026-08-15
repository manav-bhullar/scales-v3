"""Sprint 1: configuration and model foundation tests."""

from __future__ import annotations

import pytest

from scales.config import PROJECT_ROOT, get_settings, load_yaml_settings, prompt_path
from scales.models import (
    CBTEResult,
    ConceptFeedback,
    CorrectionType,
    CQATuple,
    ExamInput,
    FinalResult,
    QuestionInput,
    StudentAnswer,
    TeacherCorrection,
    TrustDecision,
    Verdict,
)


def test_settings_yaml_loads():
    settings = get_settings()
    # Provider-agnostic: LiteLLM ids look like "groq/..." or "gemini/..."
    assert "/" in settings.llm.cera_model
    assert "/" in settings.llm.cgr_model
    assert settings.llm.cera_model.split("/", 1)[0] in {
        "groq",
        "gemini",
        "openai",
        "anthropic",
        "openrouter",
        "zai",
        "cerebras",
        "mistral",
    }
    assert settings.llm.cgr_model.split("/", 1)[0] in {
        "groq",
        "gemini",
        "openai",
        "anthropic",
        "openrouter",
        "zai",
        "cerebras",
        "mistral",
    }
    assert settings.cbte.tau == 0.5
    assert settings.cbte.enable_tier3 is False
    assert settings.cbte.tau_source == "manual"
    assert settings.grading.allowed_marks_fractions == [0.0, 0.5, 1.0]
    assert settings.nli.device == "cpu"


def test_settings_yaml_raw_parseable():
    raw = load_yaml_settings()
    assert "llm" in raw
    assert "cbte" in raw
    assert "paths" in raw


def test_prompt_templates_exist():
    for name in ("cera_extraction.txt", "cgr_grading.txt", "cgr_perturbation.txt"):
        path = prompt_path(name)
        assert path.exists(), f"Missing prompt template: {path}"
        assert path.read_text(encoding="utf-8").strip()


def test_project_layout_exists():
    required = [
        PROJECT_ROOT / "scales" / "models",
        PROJECT_ROOT / "scales" / "modules",
        PROJECT_ROOT / "scales" / "services",
        PROJECT_ROOT / "config" / "settings.yaml",
        PROJECT_ROOT / "tests" / "fixtures" / "sample_question.json",
        PROJECT_ROOT / ".env.example",
        PROJECT_ROOT / "requirements.txt",
    ]
    for path in required:
        assert path.exists(), f"Missing required path: {path}"


def test_exam_and_question_models(sample_exam, sample_question):
    assert isinstance(sample_exam, ExamInput)
    assert isinstance(sample_question, QuestionInput)
    assert sample_question.total_marks == 4
    assert len(sample_question.student_answers) == 5
    assert all(isinstance(a, StudentAnswer) for a in sample_question.student_answers)


def test_cqa_models(sample_cqa, sample_cqa_list):
    assert isinstance(sample_cqa, CQATuple)
    assert sample_cqa.marks == 1
    assert sum(c.marks for c in sample_cqa_list) == 4
    assert len({c.concept_id for c in sample_cqa_list}) == len(sample_cqa_list)


def test_cgr_result_model(sample_cgr_result_full):
    assert sample_cgr_result_full.verdict == Verdict.FULL
    assert sample_cgr_result_full.marks_awarded == 1.0


def test_cbte_and_correction_models(sample_cgr_result_full):
    cbte = CBTEResult(
        cgr_result_id=sample_cgr_result_full.result_id,
        student_id=sample_cgr_result_full.student_id,
        concept_id=sample_cgr_result_full.concept_id,
        trust_score=0.85,
        decision=TrustDecision.ACCEPT,
        tier_resolved=1,
        signal_1_evidence_verified=True,
        signal_4_keyword_score=0.6,
        keywords_found=["handshake"],
        reason="Tier 1 auto-accept",
    )
    assert cbte.decision == TrustDecision.ACCEPT

    correction = TeacherCorrection(
        cbte_result_id=cbte.result_id,
        student_id=cbte.student_id,
        concept_id=cbte.concept_id,
        system_verdict=Verdict.PARTIAL,
        system_marks=0.5,
        teacher_verdict=Verdict.FULL,
        teacher_marks=1.0,
        teacher_comment="Functionally equivalent",
        correction_type=CorrectionType.UPGRADE,
    )
    assert correction.correction_type == CorrectionType.UPGRADE


def test_final_result_model():
    result = FinalResult(
        student_id="STU001",
        question_id="Q1",
        final_score=3.5,
        total_marks=4,
        overall_trust=0.72,
        concept_results=[
            ConceptFeedback(
                concept_id="Q1_C1",
                knowledge_point="handshake",
                verdict=Verdict.FULL,
                marks_awarded=1.0,
                max_marks=1,
                evidence_span="three-way handshake",
                reasoning="Clear mention",
                trust_score=0.85,
                reviewed_by="auto",
            )
        ],
    )
    assert result.final_score == 3.5
    assert result.concept_results[0].reviewed_by == "auto"


def test_invalid_total_marks_rejected():
    with pytest.raises(Exception):
        QuestionInput(
            question_text="Q",
            reference_answer="R",
            total_marks=0,
        )
