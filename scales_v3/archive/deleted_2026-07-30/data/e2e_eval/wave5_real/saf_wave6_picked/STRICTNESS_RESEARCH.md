# Practical strictness controls for nested / hybrid rubrics

Branch: `feat/nested-rubric-items`  
Goal: keep teacher rubrics coarse when natural, allow CERA to split only when a bucket needs it, and control over-strict grading without inventing a custom rule engine.

## Partial credit (what we use)

**Additive (RATAS-style).** If a bucket is worth 1.5 and CERA splits it into two 0.75 concepts, and the student nails one:

- Bucket credit = 0.75 + 0 = **0.75** (half the bucket via sum)

We do **not** require “at least one FULL” before PARTIAL counts. That would be a **rule engine** — hand-written non-additive logic like “2 of 3 concepts must be FULL” or “PARTIAL only if sibling is FULL.” SCALES stays deterministic: grade each leaf 0 / half / full of its max, then sum.

## What a “rule engine” means here

Anything beyond `score = Σ leaf awards`. Examples we are **not** building:

- “Award the Definition bucket only if Advantage is also present”
- “Need 2 of 3 FULL for any credit”
- Softmax / learned weights over criteria

RATAS still aggregates up a tree, but leaf scores compose by design; complex non-additive teacher policies would need extra code we skip.

## Hybrid contract (your constraint)

| Case | Frequency (your estimate) | Behaviour |
|------|---------------------------|-----------|
| 1 rubric line = 1 concept | ~60–70% short answers | `atomic=True` — CERA must not invent a split |
| 1 rubric line = N concepts | middle-length answers | `atomic=False` — CERA splits; child marks sum to bucket |

Blast radius of a bad split stays **inside one bucket**, which is why nesting is useful even when CERA invents the split.

## Practical controls (deployable, not theory-only)

Drawn from deployed / evaluated LLM grading work (Cloud Codex boolean criteria + code scoring; Grade Guard temperature/confidence; Rubric-Conditioned grading + deferral; RATAS RKT; our Mohler/SAF lessons).

### 1. Atomic flag (highest leverage for short answers)
Mark teacher lines that should not be subdivided. Validator rejects 1:N under those items. Prevents CERA inventing “name” vs “explain” when the teacher already priced that as one PARTIAL rule.

### 2. Earnability gate (Mohler lesson)
Every concept must be answerable from the student-facing question + reference. Reject / flag CQAs that only exist in an internal marking key the student never saw. Over-strictness often comes from **unearnable** leaves, not from nesting itself.

### 3. Keep scoring in code; LLM judges presence
Same as Cloud Codex / RATAS leaves: model outputs FULL / PARTIAL / ABSENT (or met / not), code multiplies by marks. Do not ask the LLM for a free-form bucket number.

### 4. Prefer fewer, stem-aligned leaves when uncertain
Finer decomposition is measurably stricter (“Rubric Is All You Need”: PRE more lenient than CRE). Mitigation: if a bucket is already ≤1 mark and atomic-ish, default to 1:1 unless the teacher text clearly has two independent ideas.

### 5. Calibration loop on a gold slice (not a dial alone)
Hold out ~10–15 answers per question with human bands. Measure MAE / over- vs under-score rate. If systematically under (too strict): merge leaves under the same bucket, or loosen `partial_credit_rule` wording — don’t invent a global “strictness temperature” as the only fix. Grade Guard tunes temperature via RMSE; we already have CBTE/SHRR deferral for uncertainty.

### 6. Consensus / defer when gray (already partly in SCALES)
Rubric-Conditioned grading and Grade Guard: if N samples disagree, defer to human. Use this for PARTIAL gray zones rather than forcing a harsh ABSENT.

### 7. Teacher review of CERA splits before batch grade
Especially for `atomic=False` buckets (e.g. Q-BURST definition 1.5). One human glance at the concept list per question is cheaper than fixing 50 wrong grades. UI later; for Wave6, review JSON is enough.

### 8. Explicit PARTIAL rules in the bucket text
“Names only → half” beats hoping the model invents fairness. Q-DLL3 pattern is the template.

## What we will implement on this branch

1. `RubricItem` model + optional `question.rubric_items`
2. `CQATuple.rubric_item_id` linkage
3. CERA validation: flat (legacy) **or** nested additive sums; enforce `atomic`
4. Prompt guidance: split only when a rubric item clearly has multiple independent ideas; otherwise 1:1
5. Keep aggregator as Σ concepts (bucket scores = derived sums for explain UI later)

## Wave6 test fixtures

Q1–Q4 locked in `_approved_rubrics.json` (Q-BURST uses two non-atomic 1.5 buckets — good stress case for 1:N).
