"""Module 1: CERA — Concept Extraction from Reference Answer."""

from __future__ import annotations

import re
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field

from scales.config import AppSettings, get_settings, prompt_path
from scales.models.cqa import CQATuple
from scales.models.exam import QuestionInput
from scales.models.marks import (
    format_marks,
    is_multiple_of_mark_step,
    marks_sum_matches,
)
from scales.models.rubric import RubricItem
from scales.modules.exceptions import CERAValidationError
from scales.services.exceptions import LLMAPIError, LLMValidationError
from scales.services.llm_client import LLMClient

_CONCEPT_ID_RE = re.compile(r"^[^_]+_C\d+$")


class CQAExtractionItem(BaseModel):
    """LLM-facing CQA schema (question_id / version filled by CERA)."""

    concept_id: str = Field(..., min_length=1)
    knowledge_point: str = Field(..., min_length=1)
    target_criteria: str = ""
    marks: float = Field(..., gt=0)
    rubric_item_id: str | None = None
    expected_keywords: list[str] = Field(default_factory=list)
    acceptable_variants: list[str] = Field(default_factory=list)
    partial_credit_rule: str | None = None
    source_rubric_span: str = ""
    source_reference_span: str = ""


class CERAExtractionResponse(BaseModel):
    cqa_tuples: list[CQAExtractionItem] = Field(..., min_length=1)


class CERAOutput(BaseModel):
    """Validated CERA result for one question."""

    question_id: str
    cqa_tuples: list[CQATuple]
    extraction_metadata: dict[str, Any] = Field(default_factory=dict)


class CERAModule:
    """Decompose question + reference + rubric into orthogonal CQA tuples."""

    SYSTEM_PROMPT = (
        "You are an expert university examiner. Return only valid JSON matching the "
        "requested schema. Enforce MECE concept decomposition and exact mark totals."
    )

    def __init__(
        self,
        llm_client: LLMClient,
        settings: AppSettings | None = None,
        max_validation_retries: int = 3,
    ) -> None:
        self.llm = llm_client
        self.settings = settings or get_settings()
        self.max_validation_retries = max_validation_retries
        self._prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        path = prompt_path("cera_extraction.txt")
        if not path.exists():
            raise FileNotFoundError(f"CERA prompt template missing: {path}")
        return path.read_text(encoding="utf-8")

    def _format_rubric_items(self, items: list[RubricItem]) -> str:
        if not items:
            return (
                "(No structured rubric_items — treat each rubric line as one concept "
                "unless the line clearly contains multiple independent ideas.)"
            )
        lines: list[str] = []
        for ri in items:
            mode = "ATOMIC (exactly 1 concept, same marks)" if ri.atomic else (
                "MAY SPLIT (1..N concepts whose marks sum to this bucket)"
            )
            desc = f" — {ri.description}" if ri.description.strip() else ""
            lines.append(
                f"- {ri.rubric_item_id}: {ri.label} "
                f"({format_marks(ri.marks)} marks) [{mode}]{desc}"
            )
        return "\n".join(lines)

    def _build_prompt(self, question: QuestionInput, feedback: str | None = None) -> str:
        # Use replace() — prompt templates contain literal JSON braces / {N} patterns.
        rubric = (
            question.rubric.strip()
            if question.rubric
            else "(No rubric provided — extract from reference answer only.)"
        )
        prompt = (
            self._prompt_template.replace("{question_id}", question.question_id)
            .replace("{question_text}", question.question_text)
            .replace("{reference_answer}", question.reference_answer)
            .replace("{rubric}", rubric)
            .replace("{total_marks}", format_marks(question.total_marks))
            .replace("{rubric_items}", self._format_rubric_items(question.rubric_items))
        )
        if feedback:
            prompt += (
                "\n\nYour previous extraction failed these validation checks:\n"
                f"{feedback}\n"
                "Fix all issues and return a corrected CQA list."
            )
        return prompt

    def _validate_rubric_items(self, question: QuestionInput) -> list[str]:
        errors: list[str] = []
        items = question.rubric_items
        if not items:
            return errors
        ids = [ri.rubric_item_id for ri in items]
        if len(ids) != len(set(ids)):
            errors.append("duplicate rubric_item_id values found")
        bucket_sum = sum(float(ri.marks) for ri in items)
        if not marks_sum_matches(bucket_sum, question.total_marks):
            errors.append(
                f"rubric_items marks sum {bucket_sum} != total_marks "
                f"{question.total_marks}"
            )
        for ri in items:
            if not ri.label.strip():
                errors.append(f"{ri.rubric_item_id}: label is empty")
            if not is_multiple_of_mark_step(ri.marks):
                errors.append(
                    f"{ri.rubric_item_id}: marks must be a multiple of 0.25 "
                    f"(got {ri.marks})"
                )
        return errors

    def _validate_nested_linkage(
        self,
        items: list[CQAExtractionItem],
        question: QuestionInput,
    ) -> list[str]:
        """When rubric_items are present: additive bucket sums + atomic rules."""
        errors: list[str] = []
        by_id = {ri.rubric_item_id: ri for ri in question.rubric_items}
        children: dict[str, list[CQAExtractionItem]] = {rid: [] for rid in by_id}

        for item in items:
            rid = item.rubric_item_id
            if not rid:
                errors.append(
                    f"{item.concept_id}: rubric_item_id required when "
                    "question has rubric_items"
                )
                continue
            if rid not in by_id:
                errors.append(
                    f"{item.concept_id}: unknown rubric_item_id '{rid}'"
                )
                continue
            children[rid].append(item)

        for rid, ri in by_id.items():
            kids = children[rid]
            if not kids:
                errors.append(f"{rid}: no concepts linked to this rubric item")
                continue
            child_sum = sum(float(k.marks) for k in kids)
            if not marks_sum_matches(child_sum, ri.marks):
                errors.append(
                    f"{rid}: child concept marks sum {child_sum} != "
                    f"bucket marks {ri.marks}"
                )
            if ri.atomic and len(kids) != 1:
                errors.append(
                    f"{rid}: atomic=True requires exactly 1 concept "
                    f"(got {len(kids)})"
                )
            elif ri.atomic and kids and not marks_sum_matches(
                float(kids[0].marks), ri.marks
            ):
                errors.append(
                    f"{rid}: atomic concept marks {kids[0].marks} != "
                    f"bucket marks {ri.marks}"
                )
        return errors

    def _validate_cqa_list(
        self,
        items: list[CQAExtractionItem],
        question: QuestionInput,
    ) -> list[str]:
        errors: list[str] = []
        if not items:
            errors.append("cqa_tuples must contain at least one concept")
            return errors

        marks_sum = sum(float(item.marks) for item in items)
        if not marks_sum_matches(marks_sum, question.total_marks):
            errors.append(
                f"marks sum {marks_sum} != total_marks {question.total_marks}"
            )

        ids = [item.concept_id for item in items]
        if len(ids) != len(set(ids)):
            errors.append("duplicate concept_id values found")

        for item in items:
            if not item.knowledge_point.strip():
                errors.append(f"{item.concept_id}: knowledge_point is empty")
            if item.marks <= 0:
                errors.append(f"{item.concept_id}: marks must be > 0")
            elif not is_multiple_of_mark_step(item.marks):
                errors.append(
                    f"{item.concept_id}: marks must be a multiple of 0.25 "
                    f"(got {item.marks})"
                )
            if not item.expected_keywords:
                errors.append(f"{item.concept_id}: expected_keywords must be non-empty")
            expected_prefix = f"{question.question_id}_C"
            if not item.concept_id.startswith(expected_prefix):
                errors.append(
                    f"{item.concept_id}: must start with '{expected_prefix}' "
                    f"(pattern {{question_id}}_C{{N}})"
                )
            elif not _CONCEPT_ID_RE.match(item.concept_id):
                errors.append(
                    f"{item.concept_id}: must match pattern '{{question_id}}_C{{N}}'"
                )

        if question.rubric_items:
            errors.extend(self._validate_nested_linkage(items, question))
        return errors

    def _to_cqa_tuples(
        self,
        items: list[CQAExtractionItem],
        question: QuestionInput,
    ) -> list[CQATuple]:
        return [
            CQATuple(
                concept_id=item.concept_id,
                question_id=question.question_id,
                knowledge_point=item.knowledge_point.strip(),
                target_criteria=item.target_criteria.strip(),
                marks=item.marks,
                rubric_item_id=item.rubric_item_id,
                expected_keywords=[kw.strip() for kw in item.expected_keywords if kw.strip()],
                acceptable_variants=[
                    v.strip() for v in item.acceptable_variants if v and v.strip()
                ],
                partial_credit_rule=item.partial_credit_rule,
                source_rubric_span=item.source_rubric_span.strip(),
                source_reference_span=item.source_reference_span.strip(),
                version=1,
            )
            for item in items
        ]

    async def extract_concepts(self, question: QuestionInput) -> CERAOutput:
        """Run CERA with validation retries until CQAs are valid."""
        if question.total_marks <= 0:
            raise CERAValidationError("total_marks must be > 0")

        ri_errors = self._validate_rubric_items(question)
        if ri_errors:
            raise CERAValidationError(
                "Invalid rubric_items: " + "; ".join(ri_errors)
            )

        if not question.rubric.strip():
            logger.warning(
                "No rubric provided for {}; extracting from reference answer only",
                question.question_id,
            )

        feedback: str | None = None
        last_errors: list[str] = []
        usage_before = self.llm.get_usage()

        for attempt in range(1, self.max_validation_retries + 1):
            user_prompt = self._build_prompt(question, feedback=feedback)
            try:
                response = await self.llm.call(
                    model=self.settings.llm.cera_model,
                    system_prompt=self.SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                    response_schema=CERAExtractionResponse,
                    temperature=self.settings.llm.temperature,
                    max_retries=self.settings.llm.max_retries,
                )
            except (LLMAPIError, LLMValidationError) as exc:
                logger.error("CERA LLM call failed on attempt {}: {}", attempt, exc)
                if attempt >= self.max_validation_retries:
                    raise
                feedback = f"LLM call / parse failed: {exc}"
                continue

            errors = self._validate_cqa_list(response.cqa_tuples, question)
            if not errors:
                cqas = self._to_cqa_tuples(response.cqa_tuples, question)
                usage_after = self.llm.get_usage()
                metadata = {
                    "model_used": self.settings.llm.cera_model,
                    "attempts": attempt,
                    "tokens_used": (
                        usage_after["total_input_tokens"]
                        + usage_after["total_output_tokens"]
                        - usage_before["total_input_tokens"]
                        - usage_before["total_output_tokens"]
                    ),
                    "concept_count": len(cqas),
                }
                logger.bind(module="cera").info(
                    "Extracted {} CQAs for {} (marks sum={})",
                    len(cqas),
                    question.question_id,
                    sum(c.marks for c in cqas),
                )
                return CERAOutput(
                    question_id=question.question_id,
                    cqa_tuples=cqas,
                    extraction_metadata=metadata,
                )

            last_errors = errors
            feedback = "\n".join(f"- {err}" for err in errors)
            logger.warning(
                "CERA validation failed (attempt {}/{}): {}",
                attempt,
                self.max_validation_retries,
                "; ".join(errors),
            )

        raise CERAValidationError(
            "CERA validation failed after "
            f"{self.max_validation_retries} retries: {'; '.join(last_errors)}"
        )
