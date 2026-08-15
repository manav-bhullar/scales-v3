# No-facets grading — current state & CE04 result

**Date:** 2026-07-30  
**Logged as:** TC-017 (code flag), metric note in `changes.jsonl`  
**Code flag:** `CGRModule(..., skip_facets=True)` in `scales/modules/cgr.py`

## What “no facets” means

When `skip_facets=True`, CGR still uses the CQA’s **Target Criteria** and **partial_credit_rule**, but the LLM prompt gets:

- `Evidence Facets: []`
- `Expected Keywords: []`
- `Acceptable Variants: []`
- `Evidence Role: synonym_set` / `Min Count: null` (prompt only; on-disk CQA unchanged)

Prompt already says: *When Evidence Facets is empty, fall back to Target Criteria alone.*

## CE04 dedicated run (rewrote C1 criteria + empty facets)

Path: `data/cera_eval/runs/ce04_nofacets_n8/`

| | MAE (n=8, same students) |
|---|---:|
| With facets (`select_n` min=2 on definition) | 0.500 |
| No facets + holistic C1 criteria | **0.125** |

Driver of the gap: facet-split definition (“concat” / “one transmission” / “channel hold”) taxed almost everyone −0.5 on C1 even when “multiple frames in one transmission” was clearly stated. Channel-hold is not a separate requirement for FULL under the no-facets C1 criteria.

## Policy (current recommendation)

| Concept shape | Facets? |
|---|---|
| Single claim (one advantage, one disadvantage, holistic definition) | Prefer **no** / empty facets; criteria-only |
| Enumerate / count (name N of M, checklist of distinct parts) | **Keep** facets + `select_n` / `checklist` |
| Do not | Split logically identical ideas into separate facets (CE04 channel-hold) |

## Follow-up ablation (this session)

`scripts/run_nofacets_ablation.py` — grades other smoke questions with `skip_facets=True` **without** rewriting CQA criteria (isolates prompt omission of the facet catalog).

Output: `data/cera_eval/runs/nofacets_ablation_n8/`

### Multi-question results (n=8 each, same students as smoke)

| Question | MAE no-facets | MAE with-facets | Δ (neg = no-facets better) |
|---|---:|---:|---:|
| CE08 | 0.562 | 0.625 | −0.063 |
| CE03 | 0.688 | 0.875 | −0.187 |
| CE10 | 1.047 | 0.891 | **+0.156** (facets better) |
| CE01 | 0.469 | 0.500 | −0.031 |
| CE05 | 0.562 | 0.500 | +0.062 |
| CE06 | 0.375 | 0.375 | 0 |
| CE07 | 0.250 | 0.344 | −0.094 |
| **CE04*** | **0.125** | **0.500** | **−0.375** |

\*CE04 used rewritten holistic C1 criteria + empty facets (`ce04_nofacets_n8`), not only `skip_facets` on the old `select_n` pack.

**Takeaway:** Blanking facets helps when criteria already encode a single claim (CE03/CE07/CE08 mild; CE04 large with criteria fix). Hurts when Target Criteria still say “count N catalog parts” but the catalog was removed from the prompt (CE10). Keep facets for genuine enumerate/count concepts.

## CE04 2×2 factorial (2026-07-30) — isolates confound

Path: `data/cera_eval/runs/ce04_factorial_2x2/` · Logged **TC-020**, hybrid CERA policy **PC-013**.

| Arm | Facets | Criteria | MAE | mean bias |
|---|---|---|---:|---:|
| A1 | present (`select_n`) | strict | 0.500 | −0.438 |
| A2 | absent | strict | 0.188 | −0.125 |
| A3 | present (synonym) | holistic | **0.125** | +0.062 |
| A4 | absent | holistic | **0.125** | +0.062 |

Contrasts (Δ MAE; negative = second better):
- A1→A2 (blank facets, strict): **−0.312**
- A1→A3 (criteria rewrite, facets on): **−0.375**
- A3→A4 (blank under holistic): **0.000**

**Readout:** Criteria rewrite dominates; once holistic, empty vs synonym facets tie. Landed **A4-style** into `cera_eval_v1_corrected/CE04.json` (holistic + empty facets). Production stays `skip_facets=False`; hybrid is encoded in CQA/CERA, not a global CGR flag.
