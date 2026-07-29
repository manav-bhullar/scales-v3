"""JSON persistence helpers for per-exam grading artifacts (Sprint 5)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger

from scales.config import AppSettings, get_settings, resolve_path
from scales.models.correction import TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, StudentAnswer
from scales.models.grading import CGRResult
from scales.models.result import FinalResult
from scales.models.trust import CBTEResult


class ExamStore:
    """Load/save exam grading JSON under ``data/exams/{exam_id}/``."""

    def __init__(
        self,
        exam_id: str,
        *,
        exams_dir: str | Path | None = None,
        settings: AppSettings | None = None,
    ) -> None:
        self.exam_id = exam_id
        self.settings = settings or get_settings()
        root = Path(exams_dir) if exams_dir else resolve_path(self.settings.paths.exams_dir)
        self.root = root / exam_id
        self.root.mkdir(parents=True, exist_ok=True)

    # ─── Paths ────────────────────────────────────────────────────────────

    @property
    def exam_config_path(self) -> Path:
        return self.root / "exam_config.json"

    @property
    def cqa_path(self) -> Path:
        return self.root / "cqa_tuples.json"

    @property
    def answers_path(self) -> Path:
        return self.root / "student_answers.json"

    @property
    def grading_path(self) -> Path:
        return self.root / "grading_results.json"

    @property
    def corrections_path(self) -> Path:
        return self.root / "teacher_corrections.json"

    @property
    def final_path(self) -> Path:
        return self.root / "final_results.json"

    @property
    def calibration_path(self) -> Path:
        return self.root / "calibration_report.json"

    @property
    def teacher_calibration_path(self) -> Path:
        return self.root / "teacher_calibration.json"

    # ─── Generic I/O ──────────────────────────────────────────────────────

    def _write_json(self, path: Path, payload: dict[str, Any]) -> None:
        path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        logger.debug("Wrote {}", path)

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    # ─── Exam / CQA / answers ─────────────────────────────────────────────

    def save_exam_config(self, exam: ExamInput) -> None:
        self._write_json(self.exam_config_path, {"exam": exam.model_dump(mode="json")})

    def load_exam_config(self) -> ExamInput | None:
        raw = self._read_json(self.exam_config_path)
        if not raw.get("exam"):
            return None
        return ExamInput.model_validate(raw["exam"])

    def save_cqa_tuples(self, cqas: list[CQATuple]) -> None:
        self._write_json(
            self.cqa_path,
            {"exam_id": self.exam_id, "cqa_tuples": [c.model_dump(mode="json") for c in cqas]},
        )

    def load_cqa_tuples(self) -> list[CQATuple]:
        raw = self._read_json(self.cqa_path)
        return [CQATuple.model_validate(row) for row in raw.get("cqa_tuples", [])]

    def save_calibration_report(self, report: dict[str, Any]) -> None:
        self._write_json(self.calibration_path, {"exam_id": self.exam_id, **report})

    def save_teacher_calibration(self, payload: dict[str, Any]) -> None:
        self._write_json(
            self.teacher_calibration_path,
            {"exam_id": self.exam_id, **payload},
        )

    def load_teacher_calibration(self) -> dict[str, Any] | None:
        raw = self._read_json(self.teacher_calibration_path)
        if not raw:
            return None
        return raw

    def save_student_answers(self, answers: list[StudentAnswer], question_id: str) -> None:
        self._write_json(
            self.answers_path,
            {
                "exam_id": self.exam_id,
                "question_id": question_id,
                "student_answers": [a.model_dump(mode="json") for a in answers],
            },
        )

    def load_student_answers(self) -> list[StudentAnswer]:
        raw = self._read_json(self.answers_path)
        return [StudentAnswer.model_validate(row) for row in raw.get("student_answers", [])]

    # ─── Grading results ──────────────────────────────────────────────────

    def save_grading_results(
        self,
        *,
        question_id: str,
        status: str,
        graded_students: list[str],
        cgr_results: list[CGRResult],
        cbte_results: list[CBTEResult],
    ) -> None:
        self._write_json(
            self.grading_path,
            {
                "exam_id": self.exam_id,
                "question_id": question_id,
                "status": status,
                "graded_students": list(graded_students),
                "cgr_results": [r.model_dump(mode="json") for r in cgr_results],
                "cbte_results": [r.model_dump(mode="json") for r in cbte_results],
            },
        )

    def load_grading_results(self) -> dict[str, Any]:
        raw = self._read_json(self.grading_path)
        if not raw:
            return {
                "exam_id": self.exam_id,
                "question_id": "",
                "status": "empty",
                "graded_students": [],
                "cgr_results": [],
                "cbte_results": [],
            }
        return {
            "exam_id": raw.get("exam_id", self.exam_id),
            "question_id": raw.get("question_id", ""),
            "status": raw.get("status", "unknown"),
            "graded_students": list(raw.get("graded_students", [])),
            "cgr_results": [CGRResult.model_validate(r) for r in raw.get("cgr_results", [])],
            "cbte_results": [CBTEResult.model_validate(r) for r in raw.get("cbte_results", [])],
        }

    # ─── Corrections ──────────────────────────────────────────────────────

    def save_corrections(self, corrections: list[TeacherCorrection]) -> None:
        self._write_json(
            self.corrections_path,
            {
                "exam_id": self.exam_id,
                "corrections": [c.model_dump(mode="json") for c in corrections],
            },
        )

    def load_corrections(self) -> list[TeacherCorrection]:
        raw = self._read_json(self.corrections_path)
        return [TeacherCorrection.model_validate(row) for row in raw.get("corrections", [])]

    # ─── Final results ────────────────────────────────────────────────────

    def save_final_results(self, results: list[FinalResult]) -> None:
        self._write_json(
            self.final_path,
            {
                "exam_id": self.exam_id,
                "final_results": [r.model_dump(mode="json") for r in results],
            },
        )

    def load_final_results(self) -> list[FinalResult]:
        raw = self._read_json(self.final_path)
        return [FinalResult.model_validate(row) for row in raw.get("final_results", [])]
