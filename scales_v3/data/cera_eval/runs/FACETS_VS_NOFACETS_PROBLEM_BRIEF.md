# Problem brief: Should CGR use evidence facets or not?

**Purpose of this document:** Self-contained problem statement for an independent LLM (or human) to analyze. Do **not** assume prior chat context. Answer the questions in §7 with a clear recommendation.

**Domain:** Automated short-answer grading (ASAG) for computer-networking exam questions.  
**System:** SCALES v3 — concept-level grading.  
**Date of experiments:** 2026-07-30  
**Human gold:** ASAG2024 SAF dataset (`normalized_grade` × question total marks). Gold is a single total mark; **no per-concept human labels**.

---

## 1. System overview (what CGR sees)

For each **concept** (atomic scoring unit), the grader LLM receives a prompt with fields including:

| Field | Role |
|---|---|
| **Knowledge point** | What the concept is about |
| **Target criteria** | Authoritative FULL / PARTIAL / ABSENT rules |
| **Evidence facets** | Catalog of phrases / parts / options derived from the reference answer |
| **Evidence role** | How to use facets: `synonym_set` \| `checklist` \| `select_n` |
| **Min count** | For `select_n` only (e.g. name ≥4 challenges) |
| **Acceptable variants / keywords** | Extra paraphrase hints |
| **Partial credit rule** | How PARTIAL is scored |
| Question + student answer | Input text |

**Evidence roles (intended semantics):**

- `synonym_set` — facets are alternate phrasings of **one** claim; one good paraphrase → FULL.
- `checklist` — student must cover required properties; partial coverage → PARTIAL.
- `select_n` — count distinct catalog hits; FULL if hits ≥ `min_count`.

Prompt policy already says: *Target Criteria are authoritative; facets are hints unless role says checklist/select_n. When facets are empty, fall back to Target Criteria alone.*

**Metric:** MAE = mean absolute error between system total marks and human total marks (marks units, not normalized).

---

## 2. The design tension

**Why facets exist**

1. Make scoring auditable (“which parts were present?”).
2. Support questions that require **counting distinct things** (name N challenges, list 2 benefits).
3. Reduce free-form LLM leniency / inconsistency.

**Why facets hurt**

1. **Over-splitting one idea** into multiple facets → false PARTIAL.  
   Example (CE04 definition): reference says  
   *“…concatenating a sequence of multiple frames in one single transmission, without ever releasing control of the channel.”*  
   Facets were treated as 3 parts with `select_n min_count=2`:  
   (a) concatenate multiple frames, (b) one transmission, (c) without releasing channel.  
   Students writing “concatenated … in a single transmission” often got **PARTIAL 0.5** instead of FULL 1.0, even though (a)+(b) are essentially one claim and (c) is arguably implied by “one transmission.”
2. **Narrow catalog / paraphrase miss** — student states the idea in different words (or typo: “efficency”); facet matcher under-credits.
3. **Mismatch with human graders** — SAF humans grade holistically; facet-literal systems look “harsh” vs gold even when faithful to the reference.

**Core question:** Should production grading keep feeding facets into the grader, drop them (criteria-only), or use a **hybrid policy by concept shape**?

---

## 3. Two experiments (do not conflate)

### Experiment A — CE04 dedicated redesign (confounded)

- **n = 8** students (same answers in both arms).
- **With facets:** existing CQA; C1 = `select_n min=2` of 3 definition facets.
- **No facets:** empty facet/keyword/variant lists **and** rewritten C1 Target Criteria to a single holistic claim (“multiple frames together in one burst”; channel-hold **not** required separately). C2/C3 also criteria-only.

| Arm | MAE |
|---|---:|
| With facets | 0.500 |
| No facets + rewritten criteria | **0.125** |

This shows a large win, but **two changes happened at once** (no facet list **and** softer/holistic criteria). Not a pure ablation of “facets in the prompt.”

### Experiment B — Multi-question `skip_facets` ablation (cleaner)

- Flag: `CGRModule(skip_facets=True)`.
- Effect on **prompt only**: facets=[], keywords=[], variants=[]; role forced to `synonym_set` / min_count=null **in the prompt**.
- **On-disk CQAs unchanged** (Target Criteria still may say “need 2 of 3 catalog parts”).
- Same first **n = 8** students per question as the facet-based smoke run.
- Excluded from this ablation: CE02, CE09 (known gold/label issues, not the system).

| Question | Concept mix (roles) | MAE no-facets | MAE with-facets | Δ (neg = no-facets better) |
|---|---|---:|---:|---:|
| CE08 | select_n(min=4) + 2× synonym_set | 0.562 | 0.625 | −0.063 |
| CE03 | 4× checklist | 0.688 | 0.875 | −0.187 |
| CE10 | checklist + 2× synonym_set | 1.047 | 0.891 | **+0.156** |
| CE01 | 4× checklist | 0.469 | 0.500 | −0.031 |
| CE05 | 4× synonym_set | 0.562 | 0.500 | +0.062 |
| CE06 | 2× select_n(min=2) | 0.375 | 0.375 | 0.000 |
| CE07 | select_n(min=2) + 2× synonym_set | 0.250 | 0.344 | −0.094 |

**CE04 Experiment A** (for comparison only): Δ = −0.375 with criteria rewrite.

Rough pattern from B: small gains for some checklist/select_n questions when catalog is hidden; **CE10 gets worse**; CE06 unchanged; CE05 slightly worse.

---

## 4. Worked example (CE04) — why facets mattered

**Question (3 marks):** What is frame bursting? Give 1 advantage and 1 disadvantage vs carrier extension.

**Reference definition:** concatenating multiple frames in one transmission, without releasing the channel.

**Typical student:**  
> “transmit a Concatenated sequence of multiple frames in a single transmission. It has better efficiency however it needs frames waiting for transmission.”

| Arm | C1 definition | C2 adv | C3 disadv | Total | Human |
|---|---|---|---|---:|---:|
| With facets (`select_n`≥2 of 3) | PARTIAL 0.5 | FULL 1 | FULL 1 | 2.5 | 3 |
| No facets + holistic C1 | FULL 1 | FULL 1 | FULL 1 | 3 | 3 |

Across 8 students, with-facets C1 was almost always PARTIAL → systematic −0.5 tax → MAE 0.50. Removing that tax (Experiment A) → MAE 0.125.

---

## 5. Constraints & caveats (must respect in analysis)

1. **Human gold is noisy / lenient** relative to reference on some items (especially CE02: humans often credit wrong service choice). Do not optimize blindly to MAE=0.
2. **n = 8 per question** — directional only; not a large-sample conclusion.
3. **Experiment A ≠ Experiment B.** A changes criteria; B only blanks catalog inputs while criteria text may still assume a catalog.
4. When `skip_facets=True` but Target Criteria still say “count ≥N distinct facets,” the grader loses the catalog needed to count → expected failure mode (candidate explanation for CE10).
5. Facets still matter for **true multi-item requirements** (e.g. CE08 naming: need ≥4 named challenges from a pool). Dropping facets globally may over-award short lists.
6. Goal is not only match SAF humans; also stay **faithful to the written reference/rubric** and give teachers auditable concept feedback.

---

## 6. Current internal hypothesis (challenge or refine this)

Use a **hybrid policy**:

| Concept shape | Recommendation |
|---|---|
| Single claim (one advantage, one disadvantage, holistic definition) | Empty facets; criteria-only (`synonym_set`) |
| Enumerate / count (name N of M, “two benefits”, true multi-property checklist) | Keep facets + `select_n` / `checklist` |
| Never | Split logically redundant phrases into separate facets (e.g. “one transmission” vs “without releasing channel”) |

---

## 7. Questions for the analyzing model

Please answer **all** of the following:

1. **Verdict:** Given Experiments A and B, should production CGR default to (a) always facets, (b) always no facets, or (c) hybrid by concept shape? Justify with the table, not vibes.

2. **Confound:** How much of CE04’s −0.375 Δ should be attributed to “removing facets” vs “rewriting Target Criteria / dropping channel-hold as a separate requirement”? What follow-up experiment would isolate that?

3. **CE10 regression:** Why might blanking facets *increase* MAE on CE10 while helping CE03? Propose a mechanism tied to role types (checklist / synonym_set / select_n) and criteria wording.

4. **select_n without facets:** Is it coherent to keep `select_n` / `checklist` in the CQA schema while omitting the facet list from the prompt? If not, what should the schema/prompt do instead?

5. **Policy proposal:** Write a concrete decision rule a CERA extractor or teacher UI could apply when creating a concept: when to emit facets, how many, and which role. Include failure modes to avoid (over-split, under-specified catalog, criteria–facet mismatch).

6. **Evaluation design:** Propose the next 1–2 experiments (minimal compute) that would most reduce uncertainty between “facets bad” vs “bad facet design.”

7. **Risks:** If we adopt criteria-only widely, what failure modes worsen (over-scoring, under-scoring, inconsistency, loss of auditability)?

---

## 8. Desired response format

```
## Recommendation
(a / b / c) + 3–6 sentence justification

## CE04 confound
...

## CE10 mechanism
...

## Decision rule (bullet policy)

## Next experiments
1.
2.

## Risks
- ...
```

Be concrete. Prefer falsifiable claims over general ASAG literature. If data are insufficient, say what is missing rather than inventing precision.
