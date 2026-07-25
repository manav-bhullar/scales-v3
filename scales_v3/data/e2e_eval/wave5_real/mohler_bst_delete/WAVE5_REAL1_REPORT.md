# Wave 5 / Q-REAL1 — Mohler BST delete (first real-data pack)

**Authoritative run:** `grade_gemini_v1.log`  
**Ledger row:** `wave5_real1_smoke_v1`  
**Model:** `gemini/gemini-3.1-flash-lite`  
**Date:** 2026-07-25  
**CQAs:** human-locked from `cqa_review.json` (CERA skip on grade)

## Pass bar: FAIL (pre-review)

| Metric | Value |
|--------|------:|
| Items | 112 (28 × 4) |
| False ACCEPT on LOW | **0** |
| DEFER rate | 20.5% (23/112) |
| Band hit (provisional) | **28.6%** (8/28) |
| MAE vs band midpoint | 2.64 |
| Underscored students | 20 |
| Silent-zero candidates | 31 (advisory; mostly ABSENT on C1/C4) |

Fails only `high_band_students_in_band` — **all 15 high-band students underscored**.

## What this means (honest)

This is the first pack with **real** student text and **real** human total scores.
Safety held: the only true LOW (`MOH_A22`, blank) stayed at 0.

Accuracy vs UNT gold is **poor pre-review**, for a structural reason we already flagged
in VALIDATION.md:

1. **UNT graded holistically** (0–10 vs a one-line reference).  
2. **We graded atomically** against 4 locked concepts.  
3. Real students rarely write “first find the node” (C1) or “BST property”
   (C4) — they jump straight to the deletion cases. CGR marks those ABSENT and
   CBTE often **auto-accepts** the zero → provisional totals collapse even when
   C2/C3 (the meat of the answer) look PARTIAL/FULL and are waiting in DEFER.

So this is **not** “SCALES cannot handle real CS answers.” It is **calibration
mismatch + silent ABSENT on implied concepts** — exactly the accept-audit /
concept-gold class of problem from OS1/CN2 GOOD_02, now at scale.

## Concept behaviour (raw pattern)

| Concept | Pattern on real answers |
|---------|-------------------------|
| C1 locate (1) | Often ABSENT — students skip saying “search/find” |
| C2 cases (2) | Often PARTIAL, frequently DEFERRED |
| C3 replacement (1) | Mixed FULL/PARTIAL/ABSENT; several DEFER |
| C4 BST property (1) | Almost always ABSENT (implicit, not stated) |

## Review queue: 23 items

Open the UI for `e2e_wave5_mohler_bst_delete`. Priority:

1. High-band students with deferred C2/C3 PARTIAL/FULL — AGREE if the quote is fair.  
2. Suspicious ABSENT DEFERs (`A08/C1`, `A11/C1`) — check whether “find” is implied.  
3. `A23` INCORRECT DEFERs — confirm wrong procedure stays 0.  
4. Remember: **accepted ABSENT on C1/C4 never enters the queue** — SHRR cannot
   fix those. If after review totals still undershoot UNT gold, that is evidence
   for: drop/merge C1+C4, or accept-audit on accepted zeros for high-band students.

## Diagnosis: rubric, grader strictness, or architecture?

Reproduce with `python scripts/diagnose_wave5_underscore.py`.

### Evidence 1 — two of four concepts are effectively unearnable

| Concept | Marks | Students earning > 0 |
|---------|------:|---------------------:|
| C1 locate the node | 1 | 6/28 |
| C2 handle the three cases | 2 | 15/28 |
| C3 replacement rule | 1 | 11/28 |
| **C4 maintain BST property** | 1 | **1/28** |

C1 + C4 hold **2 of the 5 marks (40%)** and the cohort earns almost none of them.
A concept that 27/28 real students miss is not measuring the class — it is
measuring my rubric. Neither is asked for by the stem ("How do you delete a node
from a binary search tree?"); both are things a *grader* would assume, not things
a student is prompted to write.

### Evidence 2 — deleting them helps, but does not fix it

| Scoring | MAE vs UNT | In band |
|---------|-----------:|--------:|
| A) all 4 concepts (raw CGR) | 2.14 | 8/28 |
| B) C2 + C3 only, rescaled to 5 | **1.77** | **12/28** |

Dropping the dead concepts recovers roughly a third of the gap. **1.77 marks out
of 5 remain**, so concept design is the largest single cause but not the whole
story.

### Evidence 3 — the residual is grader leniency, not a defect

UNT's two human graders were holistic and generous. Verbatim answers with their
gold range on our 0–5 scale:

- `MOH_A07` → **3.0–5.0**: *"Link the to-be-deleted's left child to the
  to-be-deleted's parent's left child pointer."* This is wrong as a general
  algorithm (it only works in one narrow case) and says nothing about the
  two-child case. It still scored 60–100%.
- `MOH_A03` → **2.0–4.25**: *"If you delete a node from a tree, you have to link
  that nodes parents to the children of that node."*
- `MOH_A02` → **2.5–4.25**: *"first attaching the elements from the node to be
  deleting to alternate nodes and then deleting that node. delete node;"*

Those graders rewarded *being in the right direction*. SCALES requires the
criterion to be **evidenced in the text**. Both are legitimate marking policies;
they are not the same policy, and we validated against the wrong one. SCALES has
no strictness dial, so its strictness is currently an accident of how the rubric
was worded.

### Evidence 4 — the architectural defect is visibility, not scoring

79 concept judgments came out at 0 marks. **72 of them (91%) were auto-ACCEPTed**
and never reached the teacher; only 7 were deferred.

The reason is a genuine flaw in the trust model: CBTE reads "verdict ABSENT +
zero rubric keywords matched" as *strong corroboration* and accepts at Tier 1
with trust ≈ 0.90. But that signal pattern is **identical** whether the student
genuinely omitted the concept or the concept was badly specified in the first
place. The case that most needs a human is the case CBTE is most confident about.
Architecture did not cause the low marks — it removed the teacher's ability to
undo them, so SHRR could never have rescued this run.

### Verdict

| Cause | Share | Fixable how |
|-------|-------|-------------|
| Rubric / concept design (C1, C4 unearnable) | Largest | Drop or merge C1+C4; require CERA concepts to be answerable from the stem |
| Grader strictness mismatch (holistic vs atomic) | Substantial residual (MAE 1.77) | Not a bug — needs an explicit strictness setting, and honest reporting that gold came from lenient graders |
| Architecture (accepted zeros invisible) | Amplifier, not cause | Accept-audit surface — shipped as the "Zeros never checked" filter in the new explain UI |

Bottom line: **mostly rubric, with a real architectural amplifier.** The pipeline
graded consistently and safely (0 false ACCEPT on the blank answer); it graded
against criteria the question never asked for, then hid the resulting zeros.

## Next

1. You: resolve the 23 DEFERs (concept check as you planned).  
2. You: open `/exams/e2e_wave5_mohler_bst_delete/explain` → "Zeros never checked"
   and spot-check the 72 accepted zeros. That queue is the accept-audit.  
3. Me: post-review ledger + compare to UNT totals.  
4. Then **one screw only** — likeliest first move is the C1/C4 concept edit,
   since it is the largest measured cause.
