# CERA Batch Quality Review — cera_eval_v1

Date: 2026-07-29  
Prompts: PC-007 base + paraphrase-tolerance updates (claim rewrite / CGR semantic matching)

## Batch status

| ID | Status | Concepts | Marks sum | Notes |
|----|--------|----------|-----------|-------|
| CE01 | ok | 4 | 3.0 | Good property-style facets |
| CE02 | ok | 2 | 5.0 | Ran on old 5-mark rubric; needs rerun on corrected 3-mark |
| CE03 | ok | 4 | 4.0 | Good split mechanism/trade-off; KPs still label-like |
| CE04 | ok | 3 | 3.0 | Solid definition + adv/disadv |
| CE05 | ok | 4 | 4.0 | Objectives split into 4 concepts |
| CE06 | ok | 2 | 4.0 | Definition / uses clean |
| CE07 | ok | 3 | 4.0 | Needed retry; ANY OR-format fragile |
| CE08 | ok | 3 | 4.0 | Naming concept wrongly ALL of 6 challenges |
| CE09 | ok | 2 | 4.0 | Benefits / drawbacks buckets |
| CE10 | ok | 3 | 4.0 | Ran on old 4-mark naming=1; needs rerun on 1.5/3 |

## Quality dimensions

### 1) Claim-shaped knowledge_point

**Finding:** Mixed / weak. Many KPs are still topic labels:
- Bad: "Mechanism of asynchronous transmission"
- Better: "Justification based on the overhead of connection establishment for short, frequent interactions"

**Score:** ~2/10 strong claim-shaped; most are noun-phrase labels.

### 2) Semantic facets (not verbatim quotes)

**Finding:** Strong. Facets are mostly property-like ("overhead in connecting and disconnecting", "character as self-contained unit") rather than long reference quotes.

**Score:** ~9/10.

### 3) Acceptable variants diversity

**Finding:** Strong. Almost all concepts have 3–6 variants including plain-language paraphrases ("avoids the high cost of setting up and tearing down connections").

**Score:** ~9/10.

### 4) ANY/ALL correctness

**Finding:** Mostly good on compare/contrast and multi-property classes. Failures:
- CE07/CE08 initially failed validator because ANY facets lacked `target_criteria` starting with `any of:`
- CE08 naming used ALL with all 6 challenge names (requires naming every challenge for FULL) — wrong for "name any 2"

**Score:** ~6/10.

## Patterns to feed back into prompts

1. Force claim-shaped KP: must contain a verb and state what student must demonstrate.
2. "Name any N from a longer list" → do not ALL-require the full list; facets should support selecting N options (ANY / partial rule), with the full catalog in acceptable_variants.
3. Keep the STRICT `any of:` prefix rule for multi-facet ANY concepts.
4. When concept keeps failing OR-format, collapse to one core facet and put paraphrases in acceptable_variants.

## Decision

Implement prompt iteration (Strategy C feedback), then rerun CE01/CE02/CE08/CE10 with corrected mark allocations.
