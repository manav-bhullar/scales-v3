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
