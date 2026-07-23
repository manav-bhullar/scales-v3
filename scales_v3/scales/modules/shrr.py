"""Module 4: SHRR — Selective Human Review Resolution (individual review).

Skeleton scope (Sprint 5):
  - Build review queue from CBTE DEFER items
  - Record TeacherCorrection (AGREE / UPGRADE / DOWNGRADE / OVERRIDE)
  - Track review progress
  - No CQA mutation, no batch propagation
"""

from __future__ import annotations

from collections import defaultdict

from loguru import logger

from scales.config import AppSettings, get_settings
from scales.models.correction import CorrectionType, TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.review import CorrectionResult, ReviewItem, ReviewProgress
from scales.models.trust import CBTEResult, TrustDecision
from scales.modules.exceptions import SHRRValidationError


def derive_correction_type(
    system_verdict: Verdict,
    system_marks: float,
    teacher_verdict: Verdict,
    teacher_marks: float,
) -> CorrectionType:
    """Classify the teacher action relative to the system judgment."""
    same_verdict = system_verdict == teacher_verdict
    same_marks = abs(system_marks - teacher_marks) < 1e-9
    if same_verdict and same_marks:
        return CorrectionType.AGREE
    if teacher_marks > system_marks:
        return CorrectionType.UPGRADE
    if teacher_marks < system_marks:
        return CorrectionType.DOWNGRADE
    return CorrectionType.OVERRIDE


class SHRRModule:
    """Individual deferred-item review (no batch propagation)."""

    def __init__(self, settings: AppSettings | None = None) -> None:
        self.settings = settings or get_settings()
        self._allowed_fractions = list(self.settings.grading.allowed_marks_fractions)
        self._corrections: dict[tuple[str, str], TeacherCorrection] = {}

    # ─── Queue construction ───────────────────────────────────────────────

    def build_review_items(
        self,
        deferred: list[tuple[CBTEResult, CGRResult, CQATuple, str]],
        *,
        question_id: str = "",
    ) -> list[ReviewItem]:
        """Build review items from (CBTE, CGR, CQA, student_answer) deferrals."""
        items: list[ReviewItem] = []
        for cbte, cgr, cqa, answer in deferred:
            if cbte.decision != TrustDecision.DEFER:
                continue
            items.append(
                ReviewItem(
                    cbte_result_id=cbte.result_id,
                    cgr_result_id=cgr.result_id,
                    student_id=cbte.student_id,
                    concept_id=cbte.concept_id,
                    question_id=question_id or cqa.question_id,
                    knowledge_point=cqa.knowledge_point,
                    max_marks=cqa.marks,
                    student_answer=answer,
                    system_verdict=cgr.verdict,
                    system_marks=cgr.marks_awarded,
                    evidence_span=cgr.evidence_span,
                    reasoning=cgr.reasoning,
                    trust_score=cbte.trust_score,
                    defer_reason=cbte.reason,
                )
            )
        return items

    def group_by_concept(self, items: list[ReviewItem]) -> dict[str, list[ReviewItem]]:
        grouped: dict[str, list[ReviewItem]] = defaultdict(list)
        for item in items:
            grouped[item.concept_id].append(item)
        return dict(grouped)

    # ─── Corrections ──────────────────────────────────────────────────────

    def validate_teacher_marks(self, marks: float, max_marks: int) -> float:
        allowed = sorted({round(frac * max_marks, 10) for frac in self._allowed_fractions})
        if not any(abs(marks - value) < 1e-9 for value in allowed):
            raise SHRRValidationError(
                f"teacher_marks={marks} not in allowed discrete set {allowed} "
                f"for max_marks={max_marks}"
            )
        if marks > max_marks + 1e-9:
            raise SHRRValidationError(
                f"teacher_marks={marks} exceeds concept max_marks={max_marks}"
            )
        return float(marks)

    def submit_correction(
        self,
        item: ReviewItem,
        *,
        teacher_verdict: Verdict,
        teacher_marks: float,
        teacher_comment: str = "",
    ) -> CorrectionResult:
        """Record (or overwrite) a teacher correction for one review item."""
        marks = self.validate_teacher_marks(teacher_marks, item.max_marks)
        correction_type = derive_correction_type(
            item.system_verdict,
            item.system_marks,
            teacher_verdict,
            marks,
        )
        correction = TeacherCorrection(
            cbte_result_id=item.cbte_result_id,
            review_item_id=item.review_item_id,
            student_id=item.student_id,
            concept_id=item.concept_id,
            system_verdict=item.system_verdict,
            system_marks=item.system_marks,
            teacher_verdict=teacher_verdict,
            teacher_marks=marks,
            teacher_comment=teacher_comment,
            correction_type=correction_type,
        )
        key = (item.student_id, item.concept_id)
        if key in self._corrections:
            logger.info(
                "Overwriting correction for student={} concept={}",
                item.student_id,
                item.concept_id,
            )
        self._corrections[key] = correction
        progress = self.get_review_progress([item], list(self._corrections.values()))
        # Progress for a single item is not meaningful for queue-wide state —
        # callers should pass the full queue to get_review_progress.
        return CorrectionResult(correction=correction, progress=progress)

    def load_corrections(self, corrections: list[TeacherCorrection]) -> None:
        """Hydrate in-memory store (e.g. after loading JSON)."""
        self._corrections = {(c.student_id, c.concept_id): c for c in corrections}

    def get_corrections(self) -> list[TeacherCorrection]:
        return list(self._corrections.values())

    def get_correction(self, student_id: str, concept_id: str) -> TeacherCorrection | None:
        return self._corrections.get((student_id, concept_id))

    # ─── Progress ─────────────────────────────────────────────────────────

    def get_review_progress(
        self,
        queue: list[ReviewItem],
        corrections: list[TeacherCorrection] | None = None,
    ) -> ReviewProgress:
        resolved_keys = {
            (c.student_id, c.concept_id)
            for c in (corrections if corrections is not None else self.get_corrections())
        }
        total = len(queue)
        resolved = sum(1 for item in queue if (item.student_id, item.concept_id) in resolved_keys)
        remaining = total - resolved
        return ReviewProgress(
            total=total,
            resolved=resolved,
            remaining=remaining,
            is_complete=(total == 0) or (remaining == 0),
        )

    def is_review_complete(
        self,
        queue: list[ReviewItem],
        corrections: list[TeacherCorrection] | None = None,
    ) -> bool:
        return self.get_review_progress(queue, corrections).is_complete
