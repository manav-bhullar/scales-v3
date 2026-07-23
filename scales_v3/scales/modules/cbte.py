"""Module 3: CBTE — Consistency-Based Trust Estimation (tiered pipeline).

Skeleton scope (Sprint 4 / Phase 3):
  Tier 1 — evidence verification + keyword grounding (free)
  Tier 2 — DeBERTa NLI entailment check
  Tier 3 — placeholder (stability=1.0; synonym swap deferred)
"""

from __future__ import annotations

from loguru import logger

from scales.config import AppSettings, CBTEConfig, get_settings
from scales.models.cqa import CQATuple
from scales.models.grading import CGRResult, Verdict
from scales.models.trust import CBTEResult, TrustDecision
from scales.services.llm_client import LLMClient
from scales.services.nli_service import NLIService
from scales.services.text_utils import fuzzy_keyword_match, verify_evidence


def build_verdict_hypothesis(knowledge_point: str, verdict: Verdict | str | None = None) -> str:
    """Build the NLI hypothesis from a concept claim.

    Uses the bare knowledge point (MNLI-compatible). Meta prefixes such as
    \"The student correctly demonstrates: …\" make DeBERTa predict *neutral*
    on otherwise valid evidence and collapse Tier 2 (domain accuracy ~0.40).

    ``verdict`` is accepted for API compatibility; scoring selects the class
    probability in ``_score_nli_prediction``.
    """
    _ = verdict  # reserved for future hypothesis variants
    return knowledge_point.strip()


def _score_nli_prediction(pred, verdict: Verdict | str) -> float:
    """Map NLI class probs to a trust-relevant score for the CGR verdict."""
    value = verdict.value if isinstance(verdict, Verdict) else str(verdict)
    if value == Verdict.INCORRECT.value:
        return float(pred.contradiction)
    if value == Verdict.ABSENT.value:
        return float(pred.neutral)
    # FULL / PARTIAL — evidence should entail the concept claim
    return float(pred.entailment)


class CBTEModule:
    """Tiered trust estimation for one CGR judgment."""

    def __init__(
        self,
        nli_service: NLIService | None,
        llm_client: LLMClient | None = None,
        settings: AppSettings | None = None,
        config: CBTEConfig | None = None,
    ) -> None:
        self.nli = nli_service
        self.llm = llm_client  # reserved for Tier 3 synonym swap (future)
        self.settings = settings or get_settings()
        self.config = config or self.settings.cbte

    # ─── Public API ───────────────────────────────────────────────────────

    def evaluate(
        self,
        cgr_result: CGRResult,
        student_answer: str,
        cqa: CQATuple,
        tau: float | None = None,
    ) -> CBTEResult:
        """Run the tiered pipeline for one (student, concept) judgment."""
        threshold = self.config.tau if tau is None else tau

        # Signal 1 + Signal 4 always computed (needed for all tiers / audit)
        evidence_ok = verify_evidence(cgr_result.evidence_span, student_answer)
        keyword_score, keywords_found = fuzzy_keyword_match(
            cqa.expected_keywords,
            student_answer,
            acceptable_variants=cqa.acceptable_variants,
        )

        tier1 = self._tier1_check(
            cgr_result=cgr_result,
            evidence_ok=evidence_ok,
            keyword_score=keyword_score,
            keywords_found=keywords_found,
        )
        if tier1 is not None:
            return tier1

        tier2 = self._tier2_check(
            cgr_result=cgr_result,
            cqa=cqa,
            evidence_ok=evidence_ok,
            keyword_score=keyword_score,
            keywords_found=keywords_found,
        )
        if tier2 is not None:
            return tier2

        return self._tier3_check(
            cgr_result=cgr_result,
            evidence_ok=evidence_ok,
            keyword_score=keyword_score,
            keywords_found=keywords_found,
            nli_score=self._last_nli_score,
            tau=threshold,
        )

    def evaluate_batch(
        self,
        items: list[tuple[CGRResult, str, CQATuple]],
        tau: float | None = None,
    ) -> list[CBTEResult]:
        """Evaluate many judgments; batches NLI for pairs that reach Tier 2."""
        threshold = self.config.tau if tau is None else tau
        results: list[CBTEResult | None] = [None] * len(items)
        need_tier2: list[tuple[int, CGRResult, str, CQATuple, bool, float, list[str]]] = []

        for idx, (cgr_result, student_answer, cqa) in enumerate(items):
            evidence_ok = verify_evidence(cgr_result.evidence_span, student_answer)
            keyword_score, keywords_found = fuzzy_keyword_match(
                cqa.expected_keywords,
                student_answer,
                acceptable_variants=cqa.acceptable_variants,
            )
            tier1 = self._tier1_check(
                cgr_result=cgr_result,
                evidence_ok=evidence_ok,
                keyword_score=keyword_score,
                keywords_found=keywords_found,
            )
            if tier1 is not None:
                results[idx] = tier1
            else:
                need_tier2.append(
                    (
                        idx,
                        cgr_result,
                        student_answer,
                        cqa,
                        evidence_ok,
                        keyword_score,
                        keywords_found,
                    )
                )

        # Batch NLI for escalated items
        nli_scores: dict[int, float] = {}
        if need_tier2 and self.nli is not None and self.nli.is_loaded():
            pairs: list[tuple[str, str]] = []
            pair_indices: list[int] = []
            for idx, cgr_result, _answer, cqa, _eok, _kw, _found in need_tier2:
                evidence = (cgr_result.evidence_span or "").strip()
                if not evidence:
                    nli_scores[idx] = 0.0
                    continue
                hypothesis = build_verdict_hypothesis(cqa.knowledge_point, cgr_result.verdict)
                pairs.append((evidence, hypothesis))
                pair_indices.append(idx)
            if pairs:
                preds = self.nli.predict_batch(pairs)
                # Align scores with the CGR verdict for each escalated item
                for i, pred in enumerate(preds):
                    src_idx = pair_indices[i]
                    # need_tier2 rows are (idx, cgr_result, ...)
                    cgr_for_pair = next(r[1] for r in need_tier2 if r[0] == src_idx)
                    nli_scores[src_idx] = _score_nli_prediction(pred, cgr_for_pair.verdict)
        elif need_tier2:
            for idx, *_rest in need_tier2:
                nli_scores[idx] = 0.0
            if self.nli is None or not self.nli.is_loaded():
                logger.error("NLI service unavailable; Tier 2 skipped → Tier 3")

        nli_threshold = self.config.tier2_nli_threshold
        for idx, cgr_result, _answer, cqa, evidence_ok, keyword_score, keywords_found in need_tier2:
            nli_score = nli_scores.get(idx, 0.0)
            if nli_score >= nli_threshold:
                results[idx] = self._make_result(
                    cgr_result=cgr_result,
                    trust_score=nli_score,
                    decision=TrustDecision.ACCEPT,
                    tier=2,
                    evidence_ok=evidence_ok,
                    keyword_score=keyword_score,
                    keywords_found=keywords_found,
                    nli_score=nli_score,
                    stability=None,
                    reason=f"Tier 2 accept: NLI entailment = {nli_score:.2f}",
                )
            else:
                results[idx] = self._tier3_check(
                    cgr_result=cgr_result,
                    evidence_ok=evidence_ok,
                    keyword_score=keyword_score,
                    keywords_found=keywords_found,
                    nli_score=nli_score,
                    tau=threshold,
                )

        return [r if r is not None else self._impossible_fallback(items[i][0]) for i, r in enumerate(results)]

    # ─── Tier logic ───────────────────────────────────────────────────────

    def _tier1_check(
        self,
        cgr_result: CGRResult,
        evidence_ok: bool,
        keyword_score: float,
        keywords_found: list[str],
    ) -> CBTEResult | None:
        """Return a result if resolved at Tier 1, else None to escalate."""
        # Signal 1 hard veto — hallucinated evidence
        if not evidence_ok:
            return self._make_result(
                cgr_result=cgr_result,
                trust_score=0.0,
                decision=TrustDecision.DEFER,
                tier=1,
                evidence_ok=False,
                keyword_score=keyword_score,
                keywords_found=keywords_found,
                nli_score=None,
                stability=None,
                reason=(
                    "LLM quoted evidence not found in student answer "
                    "(hallucinated quote)"
                ),
            )

        kw_threshold = self.config.tier1_keyword_threshold
        verdict = cgr_result.verdict

        # ABSENT path (Phase 1 A-9 / Phase 3 matrix):
        #   keywords scarce → confirm ABSENT at Tier 1
        #   keywords present (≥ threshold) → suspicious → escalate
        if verdict == Verdict.ABSENT:
            if keyword_score < kw_threshold and not (cgr_result.evidence_span or "").strip():
                return self._make_result(
                    cgr_result=cgr_result,
                    trust_score=0.90,
                    decision=TrustDecision.ACCEPT,
                    tier=1,
                    evidence_ok=True,
                    keyword_score=keyword_score,
                    keywords_found=keywords_found,
                    nli_score=None,
                    stability=None,
                    reason=(
                        "Tier 1 auto-accept: ABSENT verdict confirmed by "
                        f"missing keywords (score={keyword_score:.2f})"
                    ),
                )
            # Suspicious ABSENT (keywords found) or ABSENT with evidence residual
            return None

        # FULL / PARTIAL / INCORRECT: high keyword grounding → fast accept
        if keyword_score >= kw_threshold:
            return self._make_result(
                cgr_result=cgr_result,
                trust_score=0.85,
                decision=TrustDecision.ACCEPT,
                tier=1,
                evidence_ok=True,
                keyword_score=keyword_score,
                keywords_found=keywords_found,
                nli_score=None,
                stability=None,
                reason=(
                    f"Tier 1 auto-accept: evidence verified, "
                    f"keyword_score={keyword_score:.2f} "
                    f"({len(keywords_found)} keywords found)"
                ),
            )

        # Low keywords → escalate
        return None

    def _tier2_check(
        self,
        cgr_result: CGRResult,
        cqa: CQATuple,
        evidence_ok: bool,
        keyword_score: float,
        keywords_found: list[str],
    ) -> CBTEResult | None:
        """Return ACCEPT if NLI clears threshold; else None → Tier 3."""
        nli_score = self._run_nli(cgr_result, cqa)
        self._last_nli_score = nli_score

        if nli_score >= self.config.tier2_nli_threshold:
            return self._make_result(
                cgr_result=cgr_result,
                trust_score=nli_score,
                decision=TrustDecision.ACCEPT,
                tier=2,
                evidence_ok=evidence_ok,
                keyword_score=keyword_score,
                keywords_found=keywords_found,
                nli_score=nli_score,
                stability=None,
                reason=f"Tier 2 accept: NLI entailment = {nli_score:.2f}",
            )
        return None

    def _tier3_check(
        self,
        cgr_result: CGRResult,
        evidence_ok: bool,
        keyword_score: float,
        keywords_found: list[str],
        nli_score: float,
        tau: float,
    ) -> CBTEResult:
        """Final tier: combined trust. Stability placeholder = 1.0 when Tier3 disabled."""
        weights = self.config.tier3_weights
        # Synonym-swap stability deferred (enable_tier3 / DD-2)
        if self.config.enable_tier3 and self.llm is not None:
            # Future: re-prompt with perturbed knowledge point
            stability = 1.0
            logger.warning(
                "enable_tier3=true but synonym swap not implemented; stability=1.0"
            )
        else:
            stability = 1.0

        trust = (
            weights.nli * nli_score
            + weights.stability * stability
            + weights.keyword * keyword_score
        )
        # Clamp for floating-point safety
        trust = max(0.0, min(1.0, trust))

        decision = TrustDecision.ACCEPT if trust >= tau else TrustDecision.DEFER
        reason = (
            f"Tier 3: trust={trust:.2f} "
            f"(nli={nli_score:.2f}, stab={stability:.1f}, kw={keyword_score:.2f}, "
            f"tau={tau:.2f})"
        )
        return self._make_result(
            cgr_result=cgr_result,
            trust_score=trust,
            decision=decision,
            tier=3,
            evidence_ok=evidence_ok,
            keyword_score=keyword_score,
            keywords_found=keywords_found,
            nli_score=nli_score,
            stability=stability,
            reason=reason,
        )

    # ─── Helpers ──────────────────────────────────────────────────────────

    _last_nli_score: float = 0.0

    def _run_nli(self, cgr_result: CGRResult, cqa: CQATuple) -> float:
        evidence = (cgr_result.evidence_span or "").strip()
        if not evidence:
            return 0.0
        if self.nli is None or not self.nli.is_loaded():
            logger.error("NLI service not loaded; treating nli_score=0.0")
            return 0.0
        hypothesis = build_verdict_hypothesis(cqa.knowledge_point, cgr_result.verdict)
        # Truncate very long evidence for DeBERTa (Phase 4 decision: soft warn)
        if len(evidence) > 2000:
            logger.warning("NLI evidence truncated for length (concept={})", cqa.concept_id)
            evidence = evidence[:2000]
        pred = self.nli.predict(premise=evidence, hypothesis=hypothesis)
        return _score_nli_prediction(pred, cgr_result.verdict)

    def _make_result(
        self,
        *,
        cgr_result: CGRResult,
        trust_score: float,
        decision: TrustDecision,
        tier: int,
        evidence_ok: bool,
        keyword_score: float,
        keywords_found: list[str],
        nli_score: float | None,
        stability: float | None,
        reason: str,
    ) -> CBTEResult:
        result = CBTEResult(
            cgr_result_id=cgr_result.result_id,
            student_id=cgr_result.student_id,
            concept_id=cgr_result.concept_id,
            trust_score=trust_score,
            decision=decision,
            tier_resolved=tier,
            signal_1_evidence_verified=evidence_ok,
            signal_2_nli_score=nli_score,
            signal_3_stability=stability,
            signal_4_keyword_score=keyword_score,
            keywords_found=list(keywords_found),
            reason=reason,
        )
        logger.bind(module="cbte").info(
            "{}/{}: tier={} {} trust={:.2f} — {}",
            cgr_result.student_id,
            cgr_result.concept_id,
            tier,
            decision.value,
            trust_score,
            reason,
        )
        return result

    def _impossible_fallback(self, cgr_result: CGRResult) -> CBTEResult:
        return self._make_result(
            cgr_result=cgr_result,
            trust_score=0.0,
            decision=TrustDecision.DEFER,
            tier=3,
            evidence_ok=False,
            keyword_score=0.0,
            keywords_found=[],
            nli_score=0.0,
            stability=0.0,
            reason="Internal error: unresolved CBTE path",
        )
