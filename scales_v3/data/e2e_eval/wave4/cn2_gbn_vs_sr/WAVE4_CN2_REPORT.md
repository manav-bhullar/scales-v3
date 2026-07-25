# Wave 4 / Q-CN2 — smoke report

**Authoritative run:** `grade_gemini_v1.log`  
**Ledger row:** `wave4_cn2_smoke_v1`  
**Model:** `gemini/gemini-3.1-flash-lite`  
**Date:** 2026-07-25  
**Gold:** human-reviewed (GOOD_01 wording fix; GOOD_02 capped 2.5–3.5)

## Pass bar: PASS

| Metric | Value |
|--------|------:|
| Items | 32 (8 × 4) |
| False ACCEPT | **0** |
| DEFER rate | 21.9% (7/32) |
| False DEFER | 9.4% (3/32) |
| Band hit (provisional) | 75% (6/8) |
| MAE vs band midpoint | 0.50 |

## Per-student provisional scores

Provisional = marks on **ACCEPT** only (DEFER marks held until SHRR).

| Student | Provisional | Raw CGR | Human range | In band? |
|---------|------------:|--------:|-------------|----------|
| GOOD_01 | 4.0 | 4.0 | 3.0–4.0 | yes |
| GOOD_02 | 3.0 | **4.0** | 2.5–3.5 | yes (only because C4 deferred) |
| MID_01 | 1.0 | 1.5 | 1.0–2.5 | yes |
| MID_02 | 2.0 | 2.5 | 1.5–3.0 | yes |
| PARTIAL_A | 0.0 | 1.0 | 0.5–1.5 | no (C1 deferred) |
| PARTIAL_B | 0.0 | 1.5 | 0.5–2.0 | no (3 DEFERs) |
| LOW_01 | 0.0 | 0.0 | 0.0–0.5 | yes |
| LOW_02 | 0.0 | 0.0 | 0.0 | yes |

## Safety

`LOW_01` (congestion-control confusion) and `LOW_02` ("I don't know") both scored **0** with all ABSENT accepted. No false ACCEPT.

## Watch on SHRR — GOOD_02

CGR gave **FULL on all four concepts** (raw 4.0) despite human gold capping this compressed answer at 2.5–3.5. Three FULLs are already **ACCEPT**; only trade-off (`Q1_C4`) is in the review queue.

- If you **AGREE** C4 = FULL/1.0 → final **4.0** (above your band).
- To stay in band: **OVERRIDE** C4 to PARTIAL/0.5 (final 3.5) or ABSENT/0 (final 3.0).

This is the same structural lesson as OS1 `GOOD_02`: once CBTE accepts, SHRR cannot fix that concept.

## Review queue (7)

| Student / concept | System | Why deferred |
|-------------------|--------|--------------|
| GOOD_02 / C4 | FULL 1.0 | Tier 3, low NLI |
| MID_01 / C4 | PARTIAL 0.5 | Tier 3 |
| MID_02 / C4 | PARTIAL 0.5 | Tier 3 |
| PARTIAL_A / C1 | FULL 1.0 | Tier 3 |
| PARTIAL_B / C1 | ABSENT 0.0 | suspicious ABSENT (kw present) |
| PARTIAL_B / C2 | FULL 1.0 | Tier 3 |
| PARTIAL_B / C3 | PARTIAL 0.5 | Tier 3 |

## CQAs (hand-check)

| ID | Marks | Knowledge point |
|----|------:|-----------------|
| C1 | 1 | GBN receiver behavior |
| C2 | 1 | SR receiver behavior |
| C3 | 1 | Sender retransmission difference |
| C4 | 1 | Trade-off GBN vs SR |

Marks sum = 4. Looks MECE.

## SHRR outcome (post-review) — 2026-07-25

All 7 DEFERs resolved in the UI. Ledger row: `wave4_cn2_post_review`.
Corrections: **5 AGREE, 1 DOWNGRADE, 1 UPGRADE**. **Pass bar: PASS.**

| Metric | Pre-review | Post-review |
|--------|-----------:|------------:|
| Band hit | 75% (6/8) | **87.5% (7/8)** |
| MAE vs band midpoint | 0.50 | **0.4375** |

### Teacher corrections

| Student / concept | System | Teacher | Type | Note |
|-------------------|--------|---------|------|------|
| GOOD_02 / C4 | FULL 1.0 | FULL 1.0 | AGREE | — |
| MID_01 / C4 | PARTIAL 0.5 | PARTIAL 0.5 | AGREE | — |
| MID_02 / C4 | PARTIAL 0.5 | PARTIAL 0.5 | AGREE | — |
| PARTIAL_A / C1 | FULL 1.0 | **PARTIAL 0.5** | DOWNGRADE | GBN receiver named "discard out-of-order" but never explained window/how-many; borderline — teacher chose partial |
| PARTIAL_B / C1 | ABSENT 0.0 | **PARTIAL 0.5** | UPGRADE | Individual ACK + lost-packet-resent idea present; couldn't explain GBN. Teacher: "between partial and zero → partial" |
| PARTIAL_B / C2 | FULL 1.0 | FULL 1.0 | AGREE | — |
| PARTIAL_B / C3 | PARTIAL 0.5 | PARTIAL 0.5 | AGREE | — |

### Final post-review totals

| Student | Final | Human range | In band? |
|---------|------:|-------------|----------|
| GOOD_01 | 4.0 | 3.0–4.0 | yes |
| GOOD_02 | **4.0** | 2.5–3.5 | **no — over** |
| MID_01 | 1.5 | 1.0–2.5 | yes |
| MID_02 | 2.5 | 1.5–3.0 | yes |
| PARTIAL_A | 0.5 | 0.5–1.5 | yes |
| PARTIAL_B | 2.0 | 0.5–2.0 | yes |
| LOW_01 | 0.0 | 0.0–0.5 | yes |
| LOW_02 | 0.0 | 0.0 | yes |

**GOOD_02 finalized at 4.0, above your 2.5–3.5 band.** You AGREEd the deferred
trade-off, but the other three FULLs were auto-accepted and never entered the
queue — so SHRR could not pull the total down. Same lesson as OS1 GOOD_02:
**concept-level gold** is the only mechanism that catches accepted over-scores
on compressed-but-technically-complete answers.

### Teacher signal for the backlog

On both PARTIAL_B/C1 and in the OS1 review you noted the 0/0.5/1.0 scale is too
coarse — you wanted **0.25 and 0.75** steps. Logged as a candidate screw
(`grading.mark_granularity`); not changed now because it touches the rubric,
CGR prompt, and every existing gold range. Revisit before Phase D scale-up.

## Next

1. **DB1** (one-line stem already rewritten) — say `approve Q-DB1` to grade.
2. Optional: concept-level gold for CN2 or OS1 to gate the GOOD_02-style over-accept.
3. Then Step 5 (scale 8 → 20–24) once all three smokes + SHRR are clean.
