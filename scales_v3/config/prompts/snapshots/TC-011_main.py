"""Sprint 6 FastAPI layer over GradingPipeline (review / status / finalize).

Live grading stays on the CLI — these endpoints never load the NLI model.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scales.config import get_settings, resolve_path  # noqa: E402
from scales.models.grading import Verdict  # noqa: E402
from scales.modules.exceptions import (  # noqa: E402
    AggregatorValidationError,
    SHRRValidationError,
)
from scales.persistence import ExamStore  # noqa: E402
from scales.pipeline import GradingPipeline  # noqa: E402
from scales.services.llm_client import LLMClient  # noqa: E402

app = FastAPI(title="SCALES v3 API", version="0.6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CorrectionBody(BaseModel):
    student_id: str = Field(..., min_length=1)
    concept_id: str = Field(..., min_length=1)
    verdict: Verdict
    marks: float = Field(..., ge=0)
    comment: str = ""


def _exams_root() -> Path:
    return resolve_path(get_settings().paths.exams_dir)


def _pipeline_for(exam_id: str) -> GradingPipeline:
    """Review/status/finalize factory — no NLI load (avoids OOM on CPU)."""
    settings = get_settings()
    # LLMClient only wires env keys; never invoked on these paths.
    llm = LLMClient(settings.llm)
    pipe = GradingPipeline(llm, nli_service=None, settings=settings, exam_id=exam_id)
    try:
        pipe.load_from_store(exam_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return pipe


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/exams")
def list_exams() -> list[dict[str, Any]]:
    root = _exams_root()
    if not root.exists():
        return []
    out: list[dict[str, Any]] = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        exam_id = child.name
        store = ExamStore(exam_id)
        exam = store.load_exam_config()
        if exam is None:
            continue
        try:
            pipe = _pipeline_for(exam_id)
            status = pipe.get_grading_status()
            total_items = max(len(pipe._cbte_results), 1)
            defer_rate = status.deferred_count / total_items
            out.append(
                {
                    "exam_id": exam_id,
                    "subject": exam.subject,
                    "phase": status.phase.value,
                    "total_students": status.total_students,
                    "graded_count": len(status.graded_students),
                    "deferred_count": status.deferred_count,
                    "corrections_count": status.corrections_count,
                    "review_complete": status.review_complete,
                    "final_results_count": status.final_results_count,
                    "defer_rate": round(defer_rate, 4),
                    "message": status.message,
                }
            )
        except Exception as exc:  # noqa: BLE001
            out.append(
                {
                    "exam_id": exam_id,
                    "subject": exam.subject if exam else "",
                    "phase": "idle",
                    "total_students": 0,
                    "graded_count": 0,
                    "deferred_count": 0,
                    "corrections_count": 0,
                    "review_complete": False,
                    "final_results_count": 0,
                    "defer_rate": 0.0,
                    "message": f"unavailable: {exc}",
                }
            )
    return out


@app.get("/api/exams/{exam_id}/status")
def exam_status(exam_id: str) -> dict[str, Any]:
    pipe = _pipeline_for(exam_id)
    return pipe.get_grading_status().model_dump(mode="json")


@app.get("/api/exams/{exam_id}/review")
def exam_review(exam_id: str) -> dict[str, Any]:
    pipe = _pipeline_for(exam_id)
    items = pipe.get_review_queue()
    progress = pipe.get_review_progress()
    corrected = {(c.student_id, c.concept_id) for c in pipe.shrr.get_corrections()}
    unresolved = [i for i in items if (i.student_id, i.concept_id) not in corrected]
    cbte_map = {(r.student_id, r.concept_id): r for r in pipe._cbte_results}
    enriched = []
    for item in unresolved:
        row = item.model_dump(mode="json")
        cbte = cbte_map.get((item.student_id, item.concept_id))
        row["signals"] = (
            {
                "tier_resolved": cbte.tier_resolved,
                "signal_1_evidence_verified": cbte.signal_1_evidence_verified,
                "signal_2_nli_score": cbte.signal_2_nli_score,
                "signal_3_stability": cbte.signal_3_stability,
                "signal_4_keyword_score": cbte.signal_4_keyword_score,
                "keywords_found": cbte.keywords_found,
                "reason": cbte.reason,
            }
            if cbte
            else None
        )
        enriched.append(row)
    return {"items": enriched, "progress": progress.model_dump(mode="json")}


@app.post("/api/exams/{exam_id}/review")
def submit_review(exam_id: str, body: CorrectionBody) -> dict[str, Any]:
    pipe = _pipeline_for(exam_id)
    try:
        result = pipe.submit_correction(
            student_id=body.student_id,
            concept_id=body.concept_id,
            teacher_verdict=body.verdict,
            teacher_marks=body.marks,
            teacher_comment=body.comment,
        )
    except SHRRValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.model_dump(mode="json")


@app.post("/api/exams/{exam_id}/finalize")
def finalize_exam(exam_id: str) -> dict[str, Any]:
    pipe = _pipeline_for(exam_id)
    try:
        result = pipe.run_review_phase()
    except AggregatorValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result.model_dump(mode="json")


@app.get("/api/exams/{exam_id}/breakdown")
def exam_breakdown(exam_id: str) -> dict[str, Any]:
    """Per-student, per-concept "why these marks" view.

    Unlike /results this does not need finalize: it reads the CGR verdict +
    CBTE trust signals straight out of the grading store, so a teacher can
    audit ACCEPTed judgments too (not just the DEFER queue). That audit path
    is what surfaces silently-accepted zeros.
    """
    pipe = _pipeline_for(exam_id)
    question = pipe._question
    if question is None:
        raise HTTPException(status_code=404, detail=f"No question loaded for {exam_id}")

    cqa_by_id = {c.concept_id: c for c in pipe._cqa_list}
    cbte_by_key = {(r.student_id, r.concept_id): r for r in pipe._cbte_results}
    corr_by_key = {(c.student_id, c.concept_id): c for c in pipe.shrr.get_corrections()}
    answer_by_id = {a.student_id: a.answer_text for a in question.student_answers}

    grouped: dict[str, list[Any]] = {}
    for cgr in pipe._cgr_results:
        grouped.setdefault(cgr.student_id, []).append(cgr)

    students: list[dict[str, Any]] = []
    for student_id in pipe._graded_students:
        rows = grouped.get(student_id, [])
        concepts: list[dict[str, Any]] = []
        auto_score = 0.0
        current_score = 0.0
        deferred = 0
        corrected = 0
        for cgr in sorted(rows, key=lambda r: r.concept_id):
            cqa = cqa_by_id.get(cgr.concept_id)
            cbte = cbte_by_key.get((student_id, cgr.concept_id))
            corr = corr_by_key.get((student_id, cgr.concept_id))
            expected = list(cqa.expected_keywords) if cqa else []
            found = list(cbte.keywords_found) if cbte else []
            found_norm = {k.lower() for k in found}
            is_deferred = bool(cbte and cbte.decision.value == "DEFER")

            auto_score += float(cgr.marks_awarded)
            current_score += float(
                corr.teacher_marks if corr else cgr.marks_awarded
            )
            deferred += int(is_deferred and corr is None)
            corrected += int(corr is not None)

            concepts.append(
                {
                    "concept_id": cgr.concept_id,
                    "knowledge_point": cqa.knowledge_point if cqa else cgr.concept_id,
                    "target_criteria": cqa.target_criteria if cqa else "",
                    "max_marks": float(cqa.marks) if cqa else 0.0,
                    "verdict": cgr.verdict.value,
                    "marks_awarded": float(cgr.marks_awarded),
                    "evidence_span": cgr.evidence_span,
                    "reasoning": cgr.reasoning,
                    "counter_arguments": cgr.counter_arguments,
                    "decision": cbte.decision.value if cbte else "ACCEPT",
                    "trust_score": float(cbte.trust_score) if cbte else 0.0,
                    "tier_resolved": cbte.tier_resolved if cbte else 0,
                    "trust_reason": cbte.reason if cbte else "",
                    "signal_1_evidence_verified": (
                        bool(cbte.signal_1_evidence_verified) if cbte else False
                    ),
                    "signal_2_nli_score": cbte.signal_2_nli_score if cbte else None,
                    "signal_3_stability": cbte.signal_3_stability if cbte else None,
                    "signal_4_keyword_score": (
                        float(cbte.signal_4_keyword_score) if cbte else 0.0
                    ),
                    "expected_keywords": expected,
                    "keywords_found": found,
                    "keywords_missing": [
                        k for k in expected if k.lower() not in found_norm
                    ],
                    "source": "teacher" if corr else "auto",
                    "teacher_verdict": corr.teacher_verdict.value if corr else None,
                    "teacher_marks": float(corr.teacher_marks) if corr else None,
                    "teacher_comment": corr.teacher_comment if corr else None,
                    "correction_type": corr.correction_type.value if corr else None,
                }
            )

        students.append(
            {
                "student_id": student_id,
                "answer_text": answer_by_id.get(student_id, ""),
                "auto_score": round(auto_score, 2),
                "current_score": round(current_score, 2),
                "total_marks": float(question.total_marks),
                "deferred_count": deferred,
                "corrected_count": corrected,
                "concepts": concepts,
            }
        )

    return {
        "exam_id": exam_id,
        "question": {
            "question_id": question.question_id,
            "question_text": question.question_text,
            "reference_answer": question.reference_answer,
            "rubric": question.rubric,
            "total_marks": float(question.total_marks),
        },
        "concepts": [
            {
                "concept_id": c.concept_id,
                "knowledge_point": c.knowledge_point,
                "target_criteria": c.target_criteria,
                "marks": float(c.marks),
                "expected_keywords": list(c.expected_keywords),
                "acceptable_variants": list(c.acceptable_variants),
            }
            for c in pipe._cqa_list
        ],
        "students": students,
    }


@app.get("/api/exams/{exam_id}/results")
def exam_results(exam_id: str) -> list[dict[str, Any]]:
    pipe = _pipeline_for(exam_id)
    finals = pipe._final_results or (
        pipe.store.load_final_results() if pipe.store else []
    )
    return [r.model_dump(mode="json") for r in finals]
