"""Module 2: CGR — Concept-Level Grading & Reasoning."""

from __future__ import annotations

import asyncio
import hashlib
from typing import Iterable

from loguru import logger
from pydantic import BaseModel, Field

from scales.config import AppSettings, get_settings, prompt_path
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.marks import format_marks
from scales.modules.exceptions import CGRValidationError
from scales.services.exceptions import LLMAPIError, LLMValidationError
from scales.services.llm_client import LLMClient


class CGRLLMResponse(BaseModel):
    """Structured LLM output for one concept grade."""

    concept_id: str = Field(..., min_length=1)
    verdict: Verdict
    marks_awarded: float = Field(..., ge=0)
    evidence_span: str = ""
    reasoning: str = Field(..., min_length=1)
    counter_arguments: str = ""


class CGRModule:
    """Grade a student answer against one CQA at a time."""

    SYSTEM_PROMPT = (
        "You are a careful short-answer grader. Quote evidence exactly from the student "
        "answer. Return only valid JSON matching the schema. Use only discrete mark values."
    )

    def __init__(
        self,
        llm_client: LLMClient,
        settings: AppSettings | None = None,
        max_validation_retries: int = 2,
    ) -> None:
        self.llm = llm_client
        self.settings = settings or get_settings()
        self.max_validation_retries = max_validation_retries
        self._prompt_template = self._load_prompt_template()
        self._allowed_fractions = list(self.settings.grading.allowed_marks_fractions)

    def _load_prompt_template(self) -> str:
        path = prompt_path("cgr_grading.txt")
        if not path.exists():
            raise FileNotFoundError(f"CGR prompt template missing: {path}")
        return path.read_text(encoding="utf-8")

    def _allowed_marks(self, max_marks: float) -> list[float]:
        return sorted({round(frac * max_marks, 10) for frac in self._allowed_fractions})

    def _clamp_marks(self, marks_awarded: float, cqa: CQATuple) -> float:
        allowed = self._allowed_marks(cqa.marks)
        nearest = min(allowed, key=lambda value: abs(value - marks_awarded))
        if abs(nearest - marks_awarded) > 1e-9:
            logger.warning(
                "CGR marks clamped from {} to {} for {}",
                marks_awarded,
                nearest,
                cqa.concept_id,
            )
        return float(nearest)

    def _build_prompt(
        self,
        student_answer: str,
        cqa: CQATuple,
        question_text: str,
        feedback: str | None = None,
    ) -> str:
        half_marks = cqa.marks * 0.5
        prompt = (
            self._prompt_template.replace("{knowledge_point}", cqa.knowledge_point)
            .replace("{target_criteria}", cqa.target_criteria)
            .replace("{evidence_facets}", str(cqa.evidence_facets or []))
            .replace("{evidence_role}", getattr(cqa, "evidence_role", None) or "synonym_set")
            .replace(
                "{min_count}",
                str(getattr(cqa, "min_count", None) if getattr(cqa, "min_count", None) is not None else "null"),
            )
            .replace("{evidence_mode}", cqa.evidence_mode or "ANY")
            .replace("{expected_keywords}", str(cqa.expected_keywords))
            .replace("{acceptable_variants}", str(cqa.acceptable_variants))
            .replace(
                "{partial_credit_rule}",
                cqa.partial_credit_rule or "None (FULL or ABSENT/INCORRECT only)",
            )
            .replace("{marks}", format_marks(cqa.marks))
            .replace("{half_marks}", format_marks(half_marks))
            .replace("{question_text}", question_text)
            .replace(
                "{student_answer}",
                student_answer if student_answer.strip() else "(empty answer)",
            )
            .replace("{concept_id}", cqa.concept_id)
        )
        if feedback:
            prompt += (
                "\n\nYour previous response had these validation issues:\n"
                f"{feedback}\n"
                "Fix them and return corrected JSON."
            )
        return prompt

    def _prompt_hash(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]

    def _validate_and_normalize(
        self,
        raw: CGRLLMResponse,
        cqa: CQATuple,
    ) -> tuple[CGRLLMResponse, list[str]]:
        """Apply recoverable fixes; return (normalized, remaining hard errors)."""
        warnings: list[str] = []
        verdict = raw.verdict
        evidence = raw.evidence_span or ""
        marks = float(raw.marks_awarded)
        reasoning = (raw.reasoning or "").strip()
        counter = raw.counter_arguments or ""

        if raw.concept_id != cqa.concept_id:
            warnings.append(
                f"concept_id mismatch: got {raw.concept_id}, expected {cqa.concept_id}"
            )
            # Force correct id — recoverable
            concept_id = cqa.concept_id
        else:
            concept_id = raw.concept_id

        if not reasoning or len(reasoning) < 10:
            return raw, ["reasoning must be non-empty and at least 10 characters"]

        # Consistency repairs (Phase 3)
        if verdict == Verdict.ABSENT and evidence.strip():
            logger.warning(
                "ABSENT with non-empty evidence for {}; clearing evidence",
                cqa.concept_id,
            )
            evidence = ""
            warnings.append("cleared evidence_span for ABSENT")

        if verdict == Verdict.FULL and not evidence.strip():
            logger.warning(
                "FULL with empty evidence for {}; downgrading to ABSENT",
                cqa.concept_id,
            )
            verdict = Verdict.ABSENT
            marks = 0.0
            warnings.append("FULL without evidence → ABSENT")

        if verdict in (Verdict.PARTIAL, Verdict.INCORRECT) and not evidence.strip():
            # Small models sometimes claim PARTIAL/INCORRECT without a quote.
            # Treat as ABSENT rather than hard-failing the whole exam run.
            logger.warning(
                "{} with empty evidence for {}; downgrading to ABSENT",
                verdict.value,
                cqa.concept_id,
            )
            warnings.append(f"{verdict.value} without evidence → ABSENT")
            verdict = Verdict.ABSENT
            marks = 0.0
            evidence = ""

        if verdict != Verdict.ABSENT and not evidence.strip():
            # Remaining non-ABSENT verdicts must quote something from the student answer.
            return raw, [
                f"{verdict.value} requires non-empty evidence_span "
                "(quote exact text from the student answer)"
            ]

        marks = self._clamp_marks(marks, cqa)

        # Enforce verdict ↔ marks mapping after clamp
        if verdict == Verdict.FULL:
            marks = float(cqa.marks)
        elif verdict in (Verdict.ABSENT, Verdict.INCORRECT):
            marks = 0.0
        elif verdict == Verdict.PARTIAL:
            half = float(cqa.marks) * 0.5
            if marks <= 0 or marks >= cqa.marks:
                marks = half
                logger.warning(
                    "PARTIAL marks out of range for {}; set to {}",
                    cqa.concept_id,
                    marks,
                )

        if verdict == Verdict.ABSENT and evidence.strip():
            evidence = ""

        normalized = CGRLLMResponse(
            concept_id=concept_id,
            verdict=verdict,
            marks_awarded=marks,
            evidence_span=evidence,
            reasoning=reasoning,
            counter_arguments=counter,
        )
        # No hard errors if we got here
        _ = warnings
        return normalized, []

    async def grade_concept(
        self,
        student_id: str,
        student_answer: str,
        cqa: CQATuple,
        question_text: str,
    ) -> CGRResult:
        """Grade one (student, concept) pair."""
        # Empty answer: deterministic ABSENT — no LLM call needed
        if not student_answer.strip():
            logger.bind(module="cgr").info(
                "{}/{}: empty answer → ABSENT", student_id, cqa.concept_id
            )
            return CGRResult(
                student_id=student_id,
                concept_id=cqa.concept_id,
                cqa_version=cqa.version,
                verdict=Verdict.ABSENT,
                marks_awarded=0.0,
                evidence_span="",
                reasoning="Student answer is empty; concept not addressed.",
                counter_arguments="None.",
                llm_model="deterministic",
                prompt_hash="empty_answer",
            )

        feedback: str | None = None
        last_errors: list[str] = []

        for attempt in range(1, self.max_validation_retries + 1):
            user_prompt = self._build_prompt(
                student_answer, cqa, question_text, feedback=feedback
            )
            prompt_hash = self._prompt_hash(user_prompt)
            try:
                raw = await self.llm.call(
                    model=self.settings.llm.cgr_model,
                    system_prompt=self.SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                    response_schema=CGRLLMResponse,
                    temperature=self.settings.llm.temperature,
                    max_retries=self.settings.llm.max_retries,
                )
            except (LLMAPIError, LLMValidationError) as exc:
                logger.error(
                    "CGR LLM call failed for {}/{} attempt {}: {}",
                    student_id,
                    cqa.concept_id,
                    attempt,
                    exc,
                )
                if attempt >= self.max_validation_retries:
                    raise CGRValidationError(
                        f"CGR LLM failure for {student_id}/{cqa.concept_id}: {exc}"
                    ) from exc
                feedback = f"LLM call / parse failed: {exc}"
                continue

            normalized, hard_errors = self._validate_and_normalize(raw, cqa)
            if hard_errors:
                last_errors = hard_errors
                feedback = "\n".join(f"- {err}" for err in hard_errors)
                logger.warning(
                    "CGR validation failed {}/{} (attempt {}/{}): {}",
                    student_id,
                    cqa.concept_id,
                    attempt,
                    self.max_validation_retries,
                    "; ".join(hard_errors),
                )
                continue

            result = CGRResult(
                student_id=student_id,
                concept_id=normalized.concept_id,
                cqa_version=cqa.version,
                verdict=normalized.verdict,
                marks_awarded=normalized.marks_awarded,
                evidence_span=normalized.evidence_span,
                reasoning=normalized.reasoning,
                counter_arguments=normalized.counter_arguments,
                llm_model=self.settings.llm.cgr_model,
                prompt_hash=prompt_hash,
            )
            logger.bind(module="cgr").info(
                "{}/{}: verdict={} marks={} evidence={!r:.60}",
                student_id,
                cqa.concept_id,
                result.verdict.value,
                result.marks_awarded,
                result.evidence_span,
            )
            return result

        raise CGRValidationError(
            f"CGR validation failed for {student_id}/{cqa.concept_id} after "
            f"{self.max_validation_retries} retries: {'; '.join(last_errors)}"
        )

    async def grade_all_concepts(
        self,
        student_id: str,
        student_answer: str,
        cqa_list: Iterable[CQATuple],
        question_text: str,
        max_concurrent: int | None = None,
    ) -> list[CGRResult]:
        """Grade all CQAs for one student in parallel."""
        cqas = list(cqa_list)
        if not cqas:
            return []

        limit = max_concurrent or self.settings.llm.max_concurrent_calls
        semaphore = asyncio.Semaphore(limit)

        async def _one(cqa: CQATuple) -> CGRResult:
            async with semaphore:
                return await self.grade_concept(
                    student_id=student_id,
                    student_answer=student_answer,
                    cqa=cqa,
                    question_text=question_text,
                )

        results = await asyncio.gather(*[_one(cqa) for cqa in cqas])
        # Preserve CQA order
        by_id = {r.concept_id: r for r in results}
        return [by_id[cqa.concept_id] for cqa in cqas]
