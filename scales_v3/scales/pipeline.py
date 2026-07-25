"""SCALES v3.0 grading pipeline orchestrator (Sprint 5).

Phase 1 — grading: CERA → CGR → CBTE → persist JSON
Phase 2 — review:  SHRR corrections → Aggregator → final_results.json
"""

from __future__ import annotations

from loguru import logger

from scales.config import AppSettings, get_settings
from scales.models.correction import TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.exam import ExamInput, QuestionInput, StudentAnswer
from scales.models.grading import CGRResult, Verdict
from scales.models.pipeline import (
    GradingPhaseResult,
    PipelinePhase,
    PipelineStatus,
    ReviewPhaseResult,
)
from scales.models.result import FinalResult
from scales.models.review import CorrectionResult, ReviewItem, ReviewProgress
from scales.models.trust import CBTEResult, TrustDecision
from scales.modules.aggregator import AggregatorModule
from scales.modules.cbte import CBTEModule, apply_cohort_absent_audit
from scales.modules.cera import CERAModule
from scales.modules.cgr import CGRModule
from scales.modules.exceptions import AggregatorValidationError, SHRRValidationError
from scales.modules.shrr import SHRRModule
from scales.persistence import ExamStore
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIService


class GradingPipeline:
    """Two-phase end-to-end orchestrator with JSON persistence + resume."""

    def __init__(
        self,
        llm_client: LLMClient,
        nli_service: NLIService | None,
        *,
        settings: AppSettings | None = None,
        exam_store: ExamStore | None = None,
        exam_id: str | None = None,
        exams_dir: str | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.llm = llm_client
        self.nli = nli_service
        self.cera = CERAModule(llm_client, self.settings)
        self.cgr = CGRModule(llm_client, self.settings)
        self.cbte = CBTEModule(nli_service, llm_client, self.settings)
        self.shrr = SHRRModule(self.settings)
        self.aggregator = AggregatorModule()

        self._exam: ExamInput | None = None
        self._question: QuestionInput | None = None
        self._cqa_list: list[CQATuple] = []
        self._cgr_results: list[CGRResult] = []
        self._cbte_results: list[CBTEResult] = []
        self._graded_students: list[str] = []
        self._final_results: list[FinalResult] = []
        self._review_items: list[ReviewItem] = []
        self._phase = PipelinePhase.IDLE

        if exam_store is not None:
            self.store = exam_store
        elif exam_id:
            self.store = ExamStore(exam_id, exams_dir=exams_dir, settings=self.settings)
        else:
            self.store = None  # bound in run_grading_phase from exam.exam_id

    # ─── Phase 1: grading ─────────────────────────────────────────────────

    async def run_grading_phase(
        self,
        exam: ExamInput,
        *,
        resume: bool = True,
    ) -> GradingPhaseResult:
        if not exam.questions:
            raise ValueError("Exam has no questions")
        # Skeleton: one question per exam
        question = exam.questions[0]
        self._exam = exam
        self._question = question
        self._phase = PipelinePhase.GRADING

        if self.store is None:
            self.store = ExamStore(exam.exam_id, settings=self.settings)
        self.store.save_exam_config(exam)
        self.store.save_student_answers(question.student_answers, question.question_id)

        # Resume prior grading if present
        prior = self.store.load_grading_results() if resume else None
        prior_cqa = self.store.load_cqa_tuples() if resume else []
        if resume and prior and prior["cgr_results"] and prior_cqa:
            self._cqa_list = prior_cqa
            self._cgr_results = list(prior["cgr_results"])
            self._cbte_results = list(prior["cbte_results"])
            self._graded_students = list(prior["graded_students"])
            logger.info(
                "Resuming exam={} with {} graded students",
                exam.exam_id,
                len(self._graded_students),
            )
        else:
            self._cqa_list = []
            self._cgr_results = []
            self._cbte_results = []
            self._graded_students = []

        if not self._cqa_list:
            # Human-locked CQAs from a prior CERA review gate (skip re-extraction).
            locked = self.store.load_cqa_tuples() if resume else []
            if locked:
                self._cqa_list = locked
                logger.info(
                    "Using {} locked CQAs from store (skip CERA re-extraction)",
                    len(locked),
                )
            else:
                cera_out = await self.cera.extract_concepts(question)
                self._cqa_list = cera_out.cqa_tuples
                self.store.save_cqa_tuples(self._cqa_list)

        already = set(self._graded_students)
        for student in question.student_answers:
            if student.student_id in already:
                continue
            await self._grade_one_student(student, question)
            self._graded_students.append(student.student_id)
            self.store.save_grading_results(
                question_id=question.question_id,
                status="in_progress",
                graded_students=self._graded_students,
                cgr_results=self._cgr_results,
                cbte_results=self._cbte_results,
            )

        # Cohort audit (TC-012): must run here, once the whole batch is in —
        # CBTEModule grades one student at a time and cannot see this pattern.
        apply_cohort_absent_audit(self._cgr_results, self._cbte_results, self.cbte.config)

        deferred = sum(
            1 for r in self._cbte_results if r.decision == TrustDecision.DEFER
        )
        status_label = "awaiting_review" if deferred else "graded"
        self.store.save_grading_results(
            question_id=question.question_id,
            status=status_label,
            graded_students=self._graded_students,
            cgr_results=self._cgr_results,
            cbte_results=self._cbte_results,
        )

        # Hydrate corrections + review queue
        self.shrr.load_corrections(self.store.load_corrections())
        self._review_items = self._build_review_queue()
        self._phase = (
            PipelinePhase.AWAITING_REVIEW if deferred else PipelinePhase.COMPLETE
        )

        # If nothing deferred, aggregate immediately
        if deferred == 0:
            finals = self.aggregator.compute_batch(
                question_id=question.question_id,
                total_marks=question.total_marks,
                cqa_list=self._cqa_list,
                cgr_results=self._cgr_results,
                cbte_results=self._cbte_results,
                corrections=[],
                student_ids=list(self._graded_students),
            )
            self._final_results = finals
            self.store.save_final_results(finals)
            self._phase = PipelinePhase.COMPLETE

        status = self.get_grading_status()
        return GradingPhaseResult(
            exam_id=exam.exam_id,
            question_id=question.question_id,
            cqa_tuples=self._cqa_list,
            cgr_results=self._cgr_results,
            cbte_results=self._cbte_results,
            graded_students=list(self._graded_students),
            deferred_count=deferred,
            status=status,
        )

    async def _grade_one_student(
        self, student: StudentAnswer, question: QuestionInput
    ) -> None:
        cgr_results = await self.cgr.grade_all_concepts(
            student_id=student.student_id,
            student_answer=student.answer_text,
            cqa_list=self._cqa_list,
            question_text=question.question_text,
        )
        cgr_by_id = {r.concept_id: r for r in cgr_results}
        batch_items = [
            (cgr_by_id[cqa.concept_id], student.answer_text, cqa)
            for cqa in self._cqa_list
            if cqa.concept_id in cgr_by_id
        ]
        # region agent log
        try:
            import json as _dj
            import time as _dt

            with open(
                r"D:\OneDrive - MSFT\Codes\text ans eval system\debug-5194ac.log",
                "a",
                encoding="utf-8",
            ) as _f:
                _f.write(
                    _dj.dumps(
                        {
                            "sessionId": "5194ac",
                            "hypothesisId": "H6",
                            "location": "scales/pipeline.py:_grade_one_student",
                            "message": "evaluate_batch call scope",
                            "data": {
                                "student_id": student.student_id,
                                "item_count": len(batch_items),
                                "distinct_student_ids_in_batch": list(
                                    {student.student_id}
                                ),
                                "concept_ids_in_batch": [c.concept_id for _, _, c in batch_items],
                            },
                            "timestamp": int(_dt.time() * 1000),
                        }
                    )
                    + "\n"
                )
        except Exception:
            pass
        # endregion agent log
        cbte_results = self.cbte.evaluate_batch(batch_items)
        self._cgr_results.extend(cgr_results)
        self._cbte_results.extend(cbte_results)

    # ─── Review helpers ───────────────────────────────────────────────────

    def _answer_text(self, student_id: str) -> str:
        if self._question is None:
            return ""
        for row in self._question.student_answers:
            if row.student_id == student_id:
                return row.answer_text
        return ""

    def _cqa_map(self) -> dict[str, CQATuple]:
        return {c.concept_id: c for c in self._cqa_list}

    def _build_review_queue(self) -> list[ReviewItem]:
        cqa_map = self._cqa_map()
        cgr_map = {(r.student_id, r.concept_id): r for r in self._cgr_results}
        deferred_rows: list[tuple[CBTEResult, CGRResult, CQATuple, str]] = []
        for cbte in self._cbte_results:
            if cbte.decision != TrustDecision.DEFER:
                continue
            cgr = cgr_map.get((cbte.student_id, cbte.concept_id))
            cqa = cqa_map.get(cbte.concept_id)
            if cgr is None or cqa is None:
                continue
            deferred_rows.append(
                (cbte, cgr, cqa, self._answer_text(cbte.student_id))
            )
        qid = self._question.question_id if self._question else ""
        return self.shrr.build_review_items(deferred_rows, question_id=qid)

    def get_review_queue(self) -> list[ReviewItem]:
        if not self._review_items:
            self._review_items = self._build_review_queue()
        return list(self._review_items)

    def get_review_progress(self) -> ReviewProgress:
        return self.shrr.get_review_progress(
            self.get_review_queue(), self.shrr.get_corrections()
        )

    def submit_correction(
        self,
        *,
        student_id: str,
        concept_id: str,
        teacher_verdict: Verdict,
        teacher_marks: float,
        teacher_comment: str = "",
    ) -> CorrectionResult:
        queue = self.get_review_queue()
        item = next(
            (
                i
                for i in queue
                if i.student_id == student_id and i.concept_id == concept_id
            ),
            None,
        )
        if item is None:
            raise SHRRValidationError(
                f"No deferred review item for student={student_id} concept={concept_id}"
            )
        result = self.shrr.submit_correction(
            item,
            teacher_verdict=teacher_verdict,
            teacher_marks=teacher_marks,
            teacher_comment=teacher_comment,
        )
        # Recompute progress against full queue
        progress = self.shrr.get_review_progress(queue, self.shrr.get_corrections())
        result = CorrectionResult(correction=result.correction, progress=progress)
        if self.store is not None:
            self.store.save_corrections(self.shrr.get_corrections())
        return result

    # ─── Phase 2: review → aggregate ──────────────────────────────────────

    def run_review_phase(self) -> ReviewPhaseResult:
        if self._exam is None or self._question is None:
            raise AggregatorValidationError(
                "run_grading_phase must complete before run_review_phase"
            )
        queue = self.get_review_queue()
        progress = self.shrr.get_review_progress(queue, self.shrr.get_corrections())
        if not progress.is_complete:
            raise AggregatorValidationError(
                f"Review incomplete: {progress.remaining}/{progress.total} remaining"
            )

        finals = self.aggregator.compute_batch(
            question_id=self._question.question_id,
            total_marks=self._question.total_marks,
            cqa_list=self._cqa_list,
            cgr_results=self._cgr_results,
            cbte_results=self._cbte_results,
            corrections=self.shrr.get_corrections(),
            student_ids=list(self._graded_students),
        )
        self._final_results = finals
        if self.store is not None:
            self.store.save_final_results(finals)
            self.store.save_grading_results(
                question_id=self._question.question_id,
                status="complete",
                graded_students=self._graded_students,
                cgr_results=self._cgr_results,
                cbte_results=self._cbte_results,
            )
        self._phase = PipelinePhase.COMPLETE
        return ReviewPhaseResult(
            exam_id=self._exam.exam_id,
            question_id=self._question.question_id,
            final_results=finals,
            status=self.get_grading_status(),
        )

    # ─── Status ───────────────────────────────────────────────────────────

    def get_grading_status(self) -> PipelineStatus:
        exam_id = self._exam.exam_id if self._exam else (
            self.store.exam_id if self.store else "unknown"
        )
        queue = self._review_items or []
        deferred = sum(
            1 for r in self._cbte_results if r.decision == TrustDecision.DEFER
        )
        progress = self.shrr.get_review_progress(queue, self.shrr.get_corrections())
        total_students = (
            len(self._question.student_answers) if self._question else len(self._graded_students)
        )
        return PipelineStatus(
            exam_id=exam_id,
            phase=self._phase,
            total_students=total_students,
            graded_students=list(self._graded_students),
            deferred_count=deferred,
            corrections_count=len(self.shrr.get_corrections()),
            review_complete=progress.is_complete,
            final_results_count=len(self._final_results),
            message=(
                f"phase={self._phase.value} graded={len(self._graded_students)}/"
                f"{total_students} deferred={deferred} "
                f"corrections={len(self.shrr.get_corrections())}"
            ),
        )

    def load_from_store(self, exam_id: str | None = None) -> None:
        """Hydrate pipeline state from persisted JSON (for resume / review CLI)."""
        if exam_id and (self.store is None or self.store.exam_id != exam_id):
            self.store = ExamStore(exam_id, settings=self.settings)
        if self.store is None:
            raise ValueError("No exam store bound")
        exam = self.store.load_exam_config()
        if exam is None:
            raise FileNotFoundError(f"No exam_config.json for {self.store.exam_id}")
        self._exam = exam
        self._question = exam.questions[0] if exam.questions else None
        self._cqa_list = self.store.load_cqa_tuples()
        grading = self.store.load_grading_results()
        self._cgr_results = list(grading["cgr_results"])
        self._cbte_results = list(grading["cbte_results"])
        self._graded_students = list(grading["graded_students"])
        self.shrr.load_corrections(self.store.load_corrections())
        self._review_items = self._build_review_queue()
        self._final_results = self.store.load_final_results()
        deferred = sum(
            1 for r in self._cbte_results if r.decision == TrustDecision.DEFER
        )
        if self._final_results:
            self._phase = PipelinePhase.COMPLETE
        elif deferred:
            self._phase = PipelinePhase.AWAITING_REVIEW
        elif self._graded_students:
            self._phase = PipelinePhase.COMPLETE
        else:
            self._phase = PipelinePhase.IDLE
