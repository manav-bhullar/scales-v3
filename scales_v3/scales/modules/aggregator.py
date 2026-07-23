"""Module 5: Aggregator — discrete marks → FinalResult (no LLM).

Skeleton scope (Sprint 5):
  - Wait until every concept is ACCEPT or teacher-reviewed
  - Σ marks_awarded, clamp to [0, total_marks]
  - overall_trust = min(concept trust scores)
"""

from __future__ import annotations

from loguru import logger

from scales.models.correction import TeacherCorrection
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult
from scales.models.result import ConceptFeedback, FinalResult
from scales.models.trust import CBTEResult, TrustDecision
from scales.modules.exceptions import AggregatorValidationError


class AggregatorModule:
    """Pure arithmetic merge of auto-accepted and teacher-reviewed judgments."""

    def compute_final_result(
        self,
        *,
        student_id: str,
        question_id: str,
        total_marks: int,
        cqa_list: list[CQATuple],
        cgr_by_concept: dict[str, CGRResult],
        cbte_by_concept: dict[str, CBTEResult],
        corrections_by_concept: dict[str, TeacherCorrection],
    ) -> FinalResult:
        if total_marks <= 0:
            raise AggregatorValidationError("total_marks must be > 0")

        concept_results: list[ConceptFeedback] = []
        trust_scores: list[float] = []
        has_teacher = False

        for cqa in cqa_list:
            cid = cqa.concept_id
            cgr = cgr_by_concept.get(cid)
            cbte = cbte_by_concept.get(cid)
            if cgr is None or cbte is None:
                raise AggregatorValidationError(
                    f"Missing CGR/CBTE for student={student_id} concept={cid}"
                )

            if cbte.decision == TrustDecision.ACCEPT:
                feedback = ConceptFeedback(
                    concept_id=cid,
                    knowledge_point=cqa.knowledge_point,
                    verdict=cgr.verdict,
                    marks_awarded=cgr.marks_awarded,
                    max_marks=cqa.marks,
                    evidence_span=cgr.evidence_span,
                    reasoning=cgr.reasoning,
                    trust_score=cbte.trust_score,
                    reviewed_by="auto",
                    teacher_comment=None,
                )
            else:
                correction = corrections_by_concept.get(cid)
                if correction is None:
                    raise AggregatorValidationError(
                        f"Concept {cid} for student {student_id} is still deferred "
                        "(no teacher correction)"
                    )
                has_teacher = True
                feedback = ConceptFeedback(
                    concept_id=cid,
                    knowledge_point=cqa.knowledge_point,
                    verdict=correction.teacher_verdict,
                    marks_awarded=correction.teacher_marks,
                    max_marks=cqa.marks,
                    evidence_span=cgr.evidence_span,
                    reasoning=cgr.reasoning,
                    trust_score=cbte.trust_score,
                    reviewed_by="teacher",
                    teacher_comment=correction.teacher_comment or None,
                )

            concept_results.append(feedback)
            trust_scores.append(feedback.trust_score)

        raw_score = sum(item.marks_awarded for item in concept_results)
        final_score = max(0.0, min(float(total_marks), raw_score))
        if abs(final_score - raw_score) > 1e-9:
            logger.warning(
                "Final score clamped from {} to {} for student={}",
                raw_score,
                final_score,
                student_id,
            )

        overall_trust = min(trust_scores) if trust_scores else 0.0
        return FinalResult(
            student_id=student_id,
            question_id=question_id,
            final_score=final_score,
            total_marks=total_marks,
            overall_trust=overall_trust,
            has_deferred_concepts=has_teacher,
            all_concepts_resolved=True,
            concept_results=concept_results,
        )

    def compute_batch(
        self,
        *,
        question_id: str,
        total_marks: int,
        cqa_list: list[CQATuple],
        cgr_results: list[CGRResult],
        cbte_results: list[CBTEResult],
        corrections: list[TeacherCorrection],
        student_ids: list[str] | None = None,
    ) -> list[FinalResult]:
        """Aggregate finals for each student present in the grading results."""
        students = student_ids or sorted({r.student_id for r in cgr_results})
        results: list[FinalResult] = []
        for sid in students:
            cgr_map = {r.concept_id: r for r in cgr_results if r.student_id == sid}
            cbte_map = {r.concept_id: r for r in cbte_results if r.student_id == sid}
            corr_map = {
                c.concept_id: c for c in corrections if c.student_id == sid
            }
            results.append(
                self.compute_final_result(
                    student_id=sid,
                    question_id=question_id,
                    total_marks=total_marks,
                    cqa_list=cqa_list,
                    cgr_by_concept=cgr_map,
                    cbte_by_concept=cbte_map,
                    corrections_by_concept=corr_map,
                )
            )
        return results
