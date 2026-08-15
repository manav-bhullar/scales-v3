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

from datetime import UTC

from scales.config import get_settings, resolve_path
from scales.models.grading import Verdict
from scales.modules.exceptions import (
    AggregatorValidationError,
    SHRRValidationError,
)
from scales.persistence import ExamStore
from scales.pipeline import GradingPipeline
from scales.services.llm_client import LLMClient

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


class ConceptCalibrationBody(BaseModel):
    concept_id: str = Field(..., min_length=1)
    needed_for_rubric: bool = True
    partial_credit_note: str = ""
    matching_note: str = ""


class RubricCalibrationBody(BaseModel):
    rubric_item_id: str = Field(..., min_length=1)
    required_for_full_marks: bool = True
    concepts: list[ConceptCalibrationBody] = Field(default_factory=list)


class TeacherCalibrationBody(BaseModel):
    rubrics: list[RubricCalibrationBody] = Field(default_factory=list)


def _exams_root() -> Path:
    return resolve_path(get_settings().paths.exams_dir)


def _paper_meta(exam_id: str, subject: str, question_text: str = "") -> dict[str, str]:
    """Derive question-paper grouping from subject / exam_id.

    Examples
    --------
    subject \"SAF Wave6 coarse — Q-ASYNC (nested)\"
      → paper_id=saf_wave6_coarse, paper_title=SAF Wave6 coarse, question_key=Q-ASYNC
    """
    import re

    subject = (subject or "").strip()
    paper_title = subject
    question_key = ""

    # Split on em-dash / en-dash / " - "
    parts = re.split(r"\s*[—–]\s*|\s+-\s+", subject, maxsplit=1)
    if len(parts) == 2:
        paper_title = parts[0].strip()
        tail = parts[1].strip()
        m = re.search(r"\b(Q-[A-Z0-9]+)\b", tail, re.IGNORECASE)
        if m:
            question_key = m.group(1).upper()
        else:
            question_key = re.sub(r"\s*\(.*?\)\s*", "", tail).strip() or tail
    else:
        m = re.search(r"\b(Q-[A-Z0-9]+)\b", subject, re.IGNORECASE)
        if m:
            question_key = m.group(1).upper()

    if not question_key:
        # Fallback from exam_id tokens: e2e_wave6_async_n20_nested → ASYNC
        m = re.search(
            r"(?:^|_)(async|burst|conn|dll3|dll|os1|db1|cn2)(?:_|$)",
            exam_id,
            re.IGNORECASE,
        )
        if m:
            token = m.group(1).upper()
            question_key = {
                "ASYNC": "Q-ASYNC",
                "BURST": "Q-BURST",
                "CONN": "Q-CONN",
                "DLL3": "Q-DLL3",
                "DLL": "Q-DLL",
                "OS1": "Q-OS1",
                "DB1": "Q-DB1",
                "CN2": "Q-CN2",
            }.get(token, f"Q-{token}")

    if not paper_title:
        paper_title = exam_id

    paper_id = re.sub(r"[^a-z0-9]+", "_", paper_title.lower()).strip("_") or "paper"
    short_label = question_key or exam_id
    return {
        "paper_id": paper_id,
        "paper_title": paper_title,
        "question_key": question_key or short_label,
        "question_label": short_label,
        "question_preview": (question_text or "")[:120],
    }


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
        q0 = exam.questions[0] if exam.questions else None
        meta = _paper_meta(
            exam_id,
            exam.subject,
            q0.question_text if q0 else "",
        )
        try:
            pipe = _pipeline_for(exam_id)
            status = pipe.get_grading_status()
            total_items = max(len(pipe._cbte_results), 1)
            defer_rate = status.deferred_count / total_items
            cal = store.load_teacher_calibration()
            out.append(
                {
                    "exam_id": exam_id,
                    "subject": exam.subject,
                    **meta,
                    "total_marks": float(q0.total_marks) if q0 else 0.0,
                    "calibrated": bool(cal),
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
                    **meta,
                    "total_marks": float(q0.total_marks) if q0 else 0.0,
                    "calibrated": False,
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


@app.get("/api/papers")
def list_papers() -> list[dict[str, Any]]:
    """Group exams into question papers for the teacher dashboard."""
    exams = list_exams()
    by_paper: dict[str, dict[str, Any]] = {}
    for e in exams:
        pid = e["paper_id"]
        if pid not in by_paper:
            by_paper[pid] = {
                "paper_id": pid,
                "paper_title": e["paper_title"],
                "questions": [],
                "deferred_count": 0,
                "question_count": 0,
                "calibrated_count": 0,
            }
        paper = by_paper[pid]
        paper["questions"].append(e)
        paper["deferred_count"] += int(e.get("deferred_count") or 0)
        paper["question_count"] += 1
        paper["calibrated_count"] += int(bool(e.get("calibrated")))
    papers = list(by_paper.values())
    for p in papers:
        p["questions"].sort(key=lambda q: (q.get("question_key") or "", q.get("exam_id") or ""))
    papers.sort(key=lambda p: p["paper_title"].lower())
    return papers


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
            current_score += float(corr.teacher_marks if corr else cgr.marks_awarded)
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
                    "signal_4_keyword_score": (float(cbte.signal_4_keyword_score) if cbte else 0.0),
                    "expected_keywords": expected,
                    "keywords_found": found,
                    "keywords_missing": [k for k in expected if k.lower() not in found_norm],
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


def _build_calibrate_payload(pipe: GradingPipeline, exam_id: str) -> dict[str, Any]:
    """Question → rubric items → nested concepts for the teacher calibrate UI."""
    question = pipe._question
    if question is None:
        raise HTTPException(status_code=404, detail="No question loaded")

    store = pipe.store or ExamStore(exam_id)
    saved = store.load_teacher_calibration() or {}
    saved_rubrics = {
        r["rubric_item_id"]: r for r in saved.get("rubrics", []) if "rubric_item_id" in r
    }

    by_rubric: dict[str | None, list[Any]] = {}
    for cqa in pipe._cqa_list:
        by_rubric.setdefault(cqa.rubric_item_id, []).append(cqa)

    rubric_items = list(question.rubric_items)
    if not rubric_items:
        # Flat / legacy: one synthetic bucket holding all concepts.
        rubric_rows: list[dict[str, Any]] = [
            {
                "rubric_item_id": "_flat",
                "label": "Concepts (no nested rubric)",
                "marks": float(question.total_marks),
                "atomic": False,
                "description": "",
                "synthetic": True,
            }
        ]
        flat_concepts = list(pipe._cqa_list)
        groups: dict[str, list[Any]] = {"_flat": flat_concepts}
    else:
        rubric_rows = [
            {
                "rubric_item_id": ri.rubric_item_id,
                "label": ri.label,
                "marks": float(ri.marks),
                "atomic": bool(ri.atomic),
                "description": ri.description,
                "synthetic": False,
            }
            for ri in rubric_items
        ]
        groups = {ri.rubric_item_id: by_rubric.get(ri.rubric_item_id, []) for ri in rubric_items}
        # Orphans (CQA with missing/unknown rubric_item_id)
        known = {ri.rubric_item_id for ri in rubric_items}
        orphans = [c for rid, cs in by_rubric.items() for c in cs if rid not in known]
        if orphans:
            rubric_rows.append(
                {
                    "rubric_item_id": "_orphan",
                    "label": "Unbucketed concepts",
                    "marks": float(sum(c.marks for c in orphans)),
                    "atomic": False,
                    "description": "",
                    "synthetic": True,
                }
            )
            groups["_orphan"] = orphans

    rubrics_out: list[dict[str, Any]] = []
    for row in rubric_rows:
        rid = row["rubric_item_id"]
        saved_r = saved_rubrics.get(rid, {})
        saved_concepts = {
            c["concept_id"]: c for c in saved_r.get("concepts", []) if "concept_id" in c
        }
        concepts_out: list[dict[str, Any]] = []
        for cqa in groups.get(rid, []):
            sc = saved_concepts.get(cqa.concept_id, {})
            concepts_out.append(
                {
                    "concept_id": cqa.concept_id,
                    "knowledge_point": cqa.knowledge_point,
                    "target_criteria": cqa.target_criteria,
                    "marks": float(cqa.marks),
                    "evidence_facets": list(cqa.evidence_facets),
                    "evidence_role": getattr(cqa, "evidence_role", None) or "synonym_set",
                    "min_count": getattr(cqa, "min_count", None),
                    "evidence_mode": cqa.evidence_mode,
                    "partial_credit_rule": cqa.partial_credit_rule,
                    "needed_for_rubric": bool(sc.get("needed_for_rubric", True)),
                    "partial_credit_note": str(sc.get("partial_credit_note", "")),
                    "matching_note": str(sc.get("matching_note", "")),
                }
            )
        rubrics_out.append(
            {
                **row,
                "required_for_full_marks": bool(saved_r.get("required_for_full_marks", True)),
                "concepts": concepts_out,
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
        "rubrics": rubrics_out,
        "saved": bool(saved),
        "updated_at": saved.get("updated_at"),
    }


@app.get("/api/exams/{exam_id}/calibrate")
def get_calibrate(exam_id: str) -> dict[str, Any]:
    """Teacher policy UI payload: question → rubric → concepts."""
    pipe = _pipeline_for(exam_id)
    payload = _build_calibrate_payload(pipe, exam_id)
    exam = pipe._exam
    subject = exam.subject if exam else ""
    qtext = payload["question"]["question_text"]
    meta = _paper_meta(exam_id, subject, qtext)
    payload.update(meta)
    # Sibling questions on the same paper (for in-page switcher)
    siblings = [
        {
            "exam_id": e["exam_id"],
            "question_key": e["question_key"],
            "question_label": e["question_label"],
            "calibrated": e["calibrated"],
            "total_marks": e["total_marks"],
        }
        for e in list_exams()
        if e["paper_id"] == meta["paper_id"]
    ]
    siblings.sort(key=lambda s: (s["question_key"], s["exam_id"]))
    payload["siblings"] = siblings
    return payload


@app.put("/api/exams/{exam_id}/calibrate")
def put_calibrate(exam_id: str, body: TeacherCalibrationBody) -> dict[str, Any]:
    """Persist teacher required/optional policy. Does not re-grade."""
    from datetime import datetime

    pipe = _pipeline_for(exam_id)
    store = pipe.store or ExamStore(exam_id)
    payload = {
        "updated_at": datetime.now(UTC).isoformat(),
        "rubrics": [r.model_dump() for r in body.rubrics],
    }
    store.save_teacher_calibration(payload)
    return get_calibrate(exam_id)


@app.get("/api/exams/{exam_id}/results")
def exam_results(exam_id: str) -> list[dict[str, Any]]:
    pipe = _pipeline_for(exam_id)
    finals = pipe._final_results or (pipe.store.load_final_results() if pipe.store else [])
    return [r.model_dump(mode="json") for r in finals]
