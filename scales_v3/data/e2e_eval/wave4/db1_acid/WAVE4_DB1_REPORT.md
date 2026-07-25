# Wave 4 / Q-DB1 — smoke report

**Authoritative run:** `grade_gemini_v1.log`  
**Ledger row:** `wave4_db1_smoke_v1`  
**Model:** `gemini/gemini-3.1-flash-lite`  
**Date:** 2026-07-25  
**Stem style:** one exam-realistic line (no (a)–(d) subparts) — first pack under the new authoring rule.

## Pass bar: FAIL (pre-review only)

Fails a single check: `DB1_GOOD_02` provisional 2.0 vs gold 3.0–4.0. Its raw
CGR total is **3.5 (in band)** — 1.5 marks are simply parked in the DEFER queue.
Expected to pass after SHRR. Not the accepted-over-score pattern from CN2/OS1.

| Metric | Value |
|--------|------:|
| Items | 32 (8 × 4) |
| False ACCEPT | **0** |
| DEFER rate | 28.1% (9/32) — highest of the three smokes |
| False DEFER (FULL deferred) | 9.4% (3/32) |
| Band hit (provisional) | 62.5% (5/8) |
| MAE vs band midpoint | 0.78 |

## CERA under the one-line stem

The one-line stem did **not** hurt concept extraction: CERA produced exactly
4 atomic CQAs (Atomicity / Consistency / Isolation / Durability), marks sum 4.
The (a)–(d) worksheet format is not needed for MECE concepts.

## Per-student provisional scores

Provisional = ACCEPT marks only; DEFER marks held until review.

| Student | Provisional | Raw CGR | Human range | In band? |
|---------|------------:|--------:|-------------|----------|
| GOOD_01 | 4.0 | 4.0 | 3.0–4.0 | yes |
| GOOD_02 | 2.0 | 3.5 | 3.0–4.0 | no (2 DEFERs hold 1.5) |
| MID_01 | 0.5 | 1.0 | 1.0–2.5 | no (1 DEFER holds 0.5) |
| MID_02 | 0.5 | 3.0 | 2.0–3.5 | no (3 DEFERs hold 2.5) |
| PARTIAL_A | 2.0 | 2.0 | 1.0–2.5 | yes |
| PARTIAL_B | 1.5 | 1.5 | 1.0–2.5 | yes |
| LOW_01 | 0.0 | 0.0 | 0.0–0.5 | yes |
| LOW_02 | 0.0 | 0.0 | 0.0 | yes |

## Safety

- `LOW_01` (ASCII/CPU-atom/DNS nonsense): all four concepts **INCORRECT 0**;
  three deferred for confirmation — safe direction, zero marks either way.
- `LOW_02` ("I do not know"): all ABSENT, all accepted at 0.
- **False ACCEPT: 0.**

## Review queue (9)

| Student / concept | System | Note |
|-------------------|--------|------|
| GOOD_02 / C2 | FULL 1.0 | telegraphic "C = constraints/rules still hold" — likely AGREE |
| GOOD_02 / C3 | PARTIAL 0.5 | "appear not to step on each other" — teacher call |
| MID_01 / C1 | PARTIAL 0.5 | "completing fully" — thin but on-topic |
| MID_02 / C1 | FULL 1.0 | "commits completely or is undone" |
| MID_02 / C3 | PARTIAL 0.5 | locking guess, unsure of formal meaning |
| MID_02 / C4 | FULL 1.0 | "data remains after commit even if system fails" |
| LOW_01 / C1, C3, C4 | INCORRECT 0.0 | confirm nonsense stays 0 (likely AGREE) |

## Pattern worth noting — DEFER rate 28%

Same signature as before: correct-but-paraphrased answers score `kw=0.00`
(e.g. "commits completely or is undone" misses Atomicity keyword list) and low
NLI, landing at Tier 3 below tau. Definitional one-liners re-worded by students
are exactly where keyword lists are weakest. If this repeats at scale, the next
screw candidate is CERA's `expected_keywords`/`acceptable_variants` breadth for
definition-type concepts — **not** tau.

## SHRR outcome (post-review) — 2026-07-25

All 9 DEFERs resolved: **9 AGREE, 0 overrides**. Ledger: `wave4_db1_post_review`.

| Metric | Pre-review | Post-review |
|--------|-----------:|------------:|
| Band hit | 62.5% (5/8) | **100% (8/8)** |
| MAE | 0.78 | **0.28** |
| Pass bar | FAIL (GOOD_02 provisional) | **PASS** |

Final totals: GOOD_01 4.0, GOOD_02 3.5, MID_01 1.0, MID_02 3.0,
PARTIAL_A 2.0, PARTIAL_B 1.5, LOW_01 0.0, LOW_02 0.0 — all in human gold bands.

Grader + trust layer were well-calibrated on this pack: teacher never had to
override a mark, only confirm deferred ones.

## Next

All three Wave 4 smokes + SHRR are complete. Discuss next session: Step 5
scale-up vs accept-audit / concept-gold vs mark granularity (TC-009).
