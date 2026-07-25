# Wave 4 / Q-OS1 — human-locked 5-mark report

**Authoritative grading artifact:** `grade_gemini_5mark_target_v6.log`  
**Ledger row:** `wave4_os1_gemini_5mark_v6_metricfix`  
**Model:** `gemini/gemini-3.1-flash-lite`  
**Date:** 2026-07-25

## Human correction

Human review found that `OS1_GOOD_01` and `OS1_GOOD_02` answered the four
applied subparts but did not explicitly define a process and a thread. The
original 4-mark rubric could therefore award full marks despite the question
stem/reference requiring the distinction.

The exam is now 5 marks:

1. explicit process/thread definitions and relationship;
2. shared resources;
3. private per-thread resources;
4. advantage;
5. disadvantage/risk.

The student answers were deliberately preserved. This tests the omission
instead of editing synthetic answers to fit the gold.

## Changes and screw trail

| Entry | Screw | Change |
|-------|-------|--------|
| `TC-003` | `dataset.os1.definition_required` | Added the fifth definition mark |
| `TC-004` | same | Clarified that resource sharing alone does not define either term |
| `PC-004` | `cgr.partial_rule_precedence` | Concept-specific rules override generic prefer-PARTIAL |
| `PC-005` | `cera.rubric_constraint_fidelity` | Preserve 0.5 and ABSENT exclusions during CERA |
| `TC-005` | `cgr.target_criteria_wiring` | Fixed missing `target_criteria` in the CGR prompt |
| `TC-006` | `metrics.silent_zero` | Candidate only until concept-level human gold exists |
| `TC-007` | `cbte.keyword_variant_matching` | Variants match by token containment, not exact substring |

The `target_criteria` wiring was an architecture bug: CERA had the teacher's
strict FULL/PARTIAL/ABSENT contract, but CGR never received that field.

## Final v6 metrics

| Metric | Value |
|--------|-------|
| Items | 40 (8 students × 5 concepts) |
| False ACCEPT | **0** |
| DEFER rate | **12.5%** (5/40) |
| False DEFER | 2.5% (1/40) |
| Band hit (pre-review) | 75% (6/8) |
| MAE vs band midpoint | 0.4688 |
| Silent-zero candidates | 1, advisory (no concept gold yet) |

**Pass bar: FAIL** only on `high_band_students_in_band`.

## Definition-concept judgments

| Student | Human expectation | CGR |
|---------|-------------------|-----|
| `GOOD_01` | ABSENT (0) | **ABSENT (0)** |
| `GOOD_02` | ABSENT (0) | **PARTIAL (0.5)** — still too generous |
| `MID_01` | FULL (1) | **FULL (1)** |
| `MID_02` | ABSENT (0) | **ABSENT (0)** |
| `PARTIAL_A` | ABSENT (0) | **ABSENT (0)** |
| `PARTIAL_B` | ABSENT (0) | **ABSENT (0)** |
| `LOW_01` | INCORRECT (0) | **INCORRECT (0)** |
| `LOW_02` | ABSENT (0) | **ABSENT (0)** |

The architectural fixes corrected the three clearest inference errors. One
disagreement remains: Gemini interprets “Process owns the address space that
sibling threads share” as one partial definition for `GOOD_02`; the human gold
does not. This should be resolved in SHRR as 0, not by moving the gold to fit
the model.

## Final student totals

| Student | Provisional | Raw CGR | Human range |
|---------|-------------|---------|-------------|
| `GOOD_01` | 4.0 | 4.0 | 3.5–4.0 |
| `GOOD_02` | 4.5 | 4.5 | 3.5–4.0 |
| `MID_01` | 2.0 | 3.5 | 2.0–3.5 |
| `MID_02` | 2.0 | 2.5 | 2.5–3.5 |
| `PARTIAL_A` | 1.0 | 1.0 | 0.5–1.5 |
| `PARTIAL_B` | 2.5 | 2.5 | 1.0–2.5 |
| `LOW_01` | 0.0 | 0.0 | 0.0–0.5 |
| `LOW_02` | 0.0 | 0.0 | 0.0 |

## SHRR outcome (post-review)

All five v6 DEFERs were resolved in the review UI on 2026-07-25; the teacher
**agreed with the system on every item**, including FULL/1.0 for
`MID_01/Q1_C1` — human confirmation that this was a false DEFER.

Post-review ledger row: `wave4_os1_post_review_v6`.

| Metric | Pre-review | Post-review |
|--------|-----------:|------------:|
| Band hit | 75% (6/8) | **87.5% (7/8)** |
| MAE vs band midpoint | 0.4688 | **0.4062** |
| Pass bar | FAIL (GOOD_02 over band) | FAIL (same, unchanged) |

`GOOD_02` finalizes at 4.5/5, above its 3.5–4.0 human range, because the
too-generous PARTIAL on `Q1_C1` was **accepted** (trust 0.85) and therefore
never reached the review queue. SHRR cannot correct what CBTE accepts; only
concept-level human gold (TC-006) can gate this class of miss.

## TC-007 — false-DEFER fix (Step 3, Path A)

**Screw:** `cbte.keyword_variant_matching` (loosen).
`acceptable_variants` previously matched only as exact normalized substrings.
`MID_01/Q1_C1` wrote "threads are smaller units inside it"; the variant
"threads run inside a process" missed, keyword score stayed 0.00, and a FULL
verdict with verified evidence fell to Tier 3 and deferred (trust 0.37).
Variants now also hit via token containment (≥ 0.75 of the variant's content
tokens present in the answer).

Verified by offline CBTE replay (`reeval_cbte.py`, no API spend, exam store
untouched):

| Run | Result |
|-----|--------|
| OS1 (`cbte_reeval_tc007.json`) | DEFER 5 → 4; the only decision flip is `MID_01/Q1_C1` DEFER → Tier-1 ACCEPT, matching the teacher's AGREE; false DEFER 1 → 0 |
| Wave 3 regression (`wave3/cbte_reeval_tc007.json`) | DEFER 28 → 27; the flipped item `W3_GOOD_04/Q1_C3` had teacher AGREE on record, so no decision moves against human judgment |
| Unit tests | 116 pass (3 new pins in `test_text_utils.py`) |

Tradeoff (logged in TC-007): a variant hit alone contributes
`1/len(expected_keywords)` and can clear `tier1_keyword_threshold` (0.3),
fast-accepting a wrong FULL if CGR errs *and* a variant fuzzily matches.
Watch false ACCEPT on the next live runs (CN2/DB1).

## Superseded runs

The following are diagnostic history, not final evidence:

- `grade_run1.log` — Llama JSON truncation / empty-evidence failures;
- `grade_gemini_v1.log` — old 4-mark rubric;
- `grade_gemini_5mark_v2.log` — first 5-mark draft;
- `grade_gemini_5mark_v3.log` — strict dataset rule, before prompt fixes;
- `grade_gemini_5mark_prompt_v4.log` — before CERA fidelity fix;
- `grade_gemini_5mark_cera_v5.log` — before `target_criteria` wiring.

## Next action

SHRR and the false-DEFER fix are done. Two items remain before OS1 is closed:

1. **Concept-level human gold** for OS1 (expected verdict per student ×
   concept). This is what turns silent-zero into a real gate (TC-006) and the
   only mechanism that can catch accepted-but-wrong items like
   `GOOD_02/Q1_C1` (should be ABSENT/0 under the locked rubric, currently an
   accepted PARTIAL/0.5).
2. Move to **Q-CN2 / Q-DB1 smoke** (Step 3, Path B) with the same loop:
   human gold lock → grade on Gemini → ledger + pass bar → report → SHRR.
   TC-007's tradeoff (variant fuzzy hits enabling Tier-1 accepts) gets its
   first real false-ACCEPT check there.
