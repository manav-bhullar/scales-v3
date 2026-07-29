"""Module 1: CERA — Concept Extraction from Reference Answer."""

from __future__ import annotations

import re
from typing import Any, Literal

from loguru import logger
from pydantic import BaseModel, Field, field_validator, model_validator

from scales.config import AppSettings, get_settings, prompt_path
from scales.models.cqa import (
    CQATuple,
    EvidenceRole,
    derive_evidence_mode,
    derive_evidence_role,
)
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
# Prose AND-chains that must not appear for synonym_set with multiple facets.
# Keep this narrow — "because" alone is too common in OR-set explanations.
_AND_CHAIN_RE = re.compile(
    r"\b("
    r"must explain|"
    r"leading to|leads to|"
    r"as well as|"
    r"and also|"
    r"both\s+.{1,40}?\s+and"
    r")\b",
    re.IGNORECASE,
)
# LLM sometimes writes the string "null" / "No partial credit…" instead of JSON null.
_FAKE_PARTIAL_RE = re.compile(
    r"^(?:"
    r"null|none|n/?a|nil|"
    r"no partial(?:\s+credit)?(?:\s+defined)?(?:\s+for this(?: specific)? sub-?concept)?\.?|"
    r"partial(?:\s+credit)?\s*[:=]?\s*(?:none|null|n/?a|not (?:defined|specified|applicable))"
    r")$",
    re.IGNORECASE,
)


def is_real_partial_credit_rule(rule: str | None) -> bool:
    """True only for a usable half-credit rule (not None / empty / fake null text)."""
    if rule is None:
        return False
    text = rule.strip()
    if not text:
        return False
    if _FAKE_PARTIAL_RE.match(text):
        return False
    if text.lower().startswith("no partial"):
        return False
    return True


def normalize_partial_credit_rule(rule: str | None) -> str | None:
    """Return rule if real, else None."""
    return rule.strip() if is_real_partial_credit_rule(rule) else None



class CQAExtractionItem(BaseModel):
    """LLM-facing CQA schema (question_id / version filled by CERA)."""

    concept_id: str = Field(..., min_length=1)
    knowledge_point: str = Field(..., min_length=1)
    target_criteria: str = ""
    marks: float = Field(..., gt=0)
    rubric_item_id: str | None = None
    evidence_facets: list[str] = Field(default_factory=list)
    evidence_role: EvidenceRole = "synonym_set"
    min_count: int | None = None
    # Legacy field — derived from evidence_role when omitted.
    evidence_mode: Literal["ANY", "ALL"] = "ANY"
    expected_keywords: list[str] = Field(default_factory=list)
    acceptable_variants: list[str] = Field(default_factory=list)
    partial_credit_rule: str | None = None
    source_rubric_span: str = ""
    source_reference_span: str = ""

    @model_validator(mode="before")
    @classmethod
    def migrate_role_and_mode(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        role = data.get("evidence_role")
        mode = data.get("evidence_mode")
        if not role and mode:
            mode_u = str(mode).strip().upper()
            data["evidence_role"] = derive_evidence_role(
                "ALL" if mode_u == "ALL" else "ANY"
            )
            role = data["evidence_role"]
        if not role:
            data["evidence_role"] = "synonym_set"
            role = "synonym_set"
        role_s = str(role).strip().lower()
        if role_s not in ("synonym_set", "checklist", "select_n"):
            raise ValueError(
                "evidence_role must be synonym_set, checklist, or select_n"
            )
        data["evidence_role"] = role_s
        data["evidence_mode"] = derive_evidence_mode(role_s)  # type: ignore[arg-type]
        return data

    @field_validator("evidence_mode", mode="before")
    @classmethod
    def normalize_evidence_mode(cls, value: object) -> str:
        if value is None or value == "":
            return "ANY"
        mode = str(value).strip().upper()
        if mode not in ("ANY", "ALL"):
            raise ValueError("evidence_mode must be ANY or ALL")
        return mode

    @field_validator("min_count")
    @classmethod
    def min_count_positive(cls, value: int | None) -> int | None:
        if value is None:
            return None
        if int(value) < 1:
            raise ValueError("min_count must be >= 1 when set")
        return int(value)


class CERAExtractionResponse(BaseModel):
    cqa_tuples: list[CQAExtractionItem] = Field(..., min_length=1)


class CERAOutput(BaseModel):
    """Validated CERA result for one question."""

    question_id: str
    cqa_tuples: list[CQATuple]
    extraction_metadata: dict[str, Any] = Field(default_factory=dict)


def _facet_has_keyword_coverage(facet: str, keywords: list[str]) -> bool:
    """True if some keyword is a case-insensitive substring of the facet (or vice versa)."""
    f = facet.strip().lower()
    if not f:
        return False
    for kw in keywords:
        k = kw.strip().lower()
        if not k:
            continue
        if k in f or f in k:
            return True
    return False


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
        max_validation_retries: int = 5,
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

    def _validate_evidence_fields(self, item: CQAExtractionItem) -> list[str]:
        """Validate facets / role / partial / AND-lint / keyword coverage."""
        errors: list[str] = []
        cid = item.concept_id
        facets = [f.strip() for f in item.evidence_facets if f and f.strip()]
        if not facets:
            errors.append(
                f"{cid}: evidence_facets must be non-empty "
                "(extract observable evidence phrases from the reference answer)"
            )
            return errors

        role = (item.evidence_role or "synonym_set").strip().lower()
        criteria = item.target_criteria or ""
        criteria_l = criteria.lower()

        if role == "checklist":
            if not is_real_partial_credit_rule(item.partial_credit_rule):
                errors.append(
                    f"{cid}: evidence_role=checklist requires a real partial_credit_rule "
                    "(some facets → PARTIAL / half marks). "
                    "Do not write 'null' or 'No partial credit…' as text."
                )
            if "full requires" not in criteria_l and "requires" not in criteria_l:
                errors.append(
                    f"{cid}: evidence_role=checklist should state FULL requirements "
                    "in target_criteria (e.g. 'FULL requires: …')."
                )

        elif role == "select_n":
            if item.min_count is None or int(item.min_count) < 1:
                errors.append(
                    f"{cid}: evidence_role=select_n requires min_count >= 1 "
                    "(e.g. name at least 2 challenges → min_count=2)."
                )
            elif len(facets) < int(item.min_count):
                errors.append(
                    f"{cid}: evidence_role=select_n needs len(evidence_facets) >= "
                    f"min_count ({item.min_count}); got {len(facets)} facets."
                )
            if not is_real_partial_credit_rule(item.partial_credit_rule):
                errors.append(
                    f"{cid}: evidence_role=select_n requires a real partial_credit_rule "
                    "(e.g. 'exactly 1 valid item → half marks')."
                )
            if "at least" not in criteria_l and "min_count" not in criteria_l:
                # Prefer explicit count language in criteria.
                if str(item.min_count) not in criteria:
                    errors.append(
                        f"{cid}: evidence_role=select_n target_criteria must state "
                        f"FULL needs at least {item.min_count} distinct valid items "
                        f"from the catalog."
                    )

        elif role == "synonym_set":
            if len(facets) > 1:
                match = _AND_CHAIN_RE.search(criteria)
                if match:
                    errors.append(
                        f"{cid}: evidence_role=synonym_set with multiple facets but "
                        f"target_criteria looks like an AND-chain "
                        f"(matched '{match.group(0)}'). "
                        "Rewrite as an OR-set ('any of: …'), or switch to checklist "
                        "if all properties are required."
                    )
                elif "any of" not in criteria_l:
                    errors.append(
                        f"{cid}: evidence_role=synonym_set with multiple facets "
                        "requires target_criteria to state an OR-set starting with "
                        f"'any of: …' (facets={facets})."
                    )
            if item.min_count is not None:
                errors.append(
                    f"{cid}: evidence_role=synonym_set must not set min_count "
                    "(use select_n when a minimum count is required)."
                )
        else:
            errors.append(
                f"{cid}: evidence_role must be synonym_set, checklist, or select_n "
                f"(got {role!r})"
            )

        uncovered = [
            f for f in facets if not _facet_has_keyword_coverage(f, item.expected_keywords)
        ]
        if uncovered:
            errors.append(
                f"{cid}: expected_keywords must cover every evidence facet "
                f"(uncovered: {uncovered}). Add at least one keyword per facet."
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
            # Split children must keep partial-credit semantics.
            if (not ri.atomic) and len(kids) > 1:
                for kid in kids:
                    if not is_real_partial_credit_rule(kid.partial_credit_rule):
                        errors.append(
                            f"{kid.concept_id}: MAY-SPLIT child under {rid} "
                            "requires a real partial_credit_rule "
                            "(not null / 'No partial credit…')"
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
            errors.extend(self._validate_evidence_fields(item))

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
                evidence_facets=[f.strip() for f in item.evidence_facets if f and f.strip()],
                evidence_role=item.evidence_role,
                min_count=item.min_count,
                evidence_mode=derive_evidence_mode(item.evidence_role),
                expected_keywords=[kw.strip() for kw in item.expected_keywords if kw.strip()],
                acceptable_variants=[
                    v.strip() for v in item.acceptable_variants if v and v.strip()
                ],
                partial_credit_rule=normalize_partial_credit_rule(item.partial_credit_rule),
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
