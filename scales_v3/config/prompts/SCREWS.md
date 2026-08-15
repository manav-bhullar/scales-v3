# Screws — current knobs

Named tuning knobs and their **latest** logged turn.
Before you tighten/loosen again, read `if_reverted` on the latest entry.

Full history: `PROMPT_CHANGELOG.md` / `changes.jsonl`.

| Screw | Last id | Direction | Kind | What (latest) | If reverted |
|-------|---------|-----------|------|---------------|-------------|
| `cbte.keyword_variant_matching` | TC-007 | loosen | code | acceptable_variants now match by token containment (>=0.7... | False DEFER on paraphrased-but-correct answers ... |
| `cera.cqa_quality_bar` | PC-007 | tighten | prompt | General CERA CQA quality bar: gradable claims not topic l... | CERA again collapses multi-property definitions... |
| `cera.evidence_facets_mode` | TC-014 | restructure | code | Add evidence_facets + evidence_mode (ANY/ALL); validators... | Advantage/disadvantage leaves become over-stric... |
| `cera.evidence_role_shapes` | PC-010 | restructure | prompt | Question-shape step; emit evidence_role+min_count instead... | CERA emits wrong ANY/ALL for name-N-of-M and ch... |
| `cera.fake_partial_and_calibrate` | TC-015 | tighten | code | Reject fake partial_credit_rule strings (null/No partial…... | Fake partials pass validation again; no pre-bat... |
| `cera.hybrid_facet_policy` | PC-013 | restructure | prompt | Hybrid facet policy: single-claim synonym_set prefers emp... | CERA again emits select_n min=2 of 3 for frame-... |
| `cera.multi_property_all_mode` | PC-006 | tighten | prompt | When reference defines a class as a checklist of distingu... | Multi-property class definitions collapse back ... |
| `cera.multipart_definition_select_n` | PC-012 | tighten | prompt | Multi-part definitions use select_n (e.g. min_count=2 of ... | Definition concepts award FULL for a single par... |
| `cera.paraphrase_claim_shape` | PC-008 | tighten | prompt | Claim-shaped KPs, semantic facets, 3-5 variants, ANY any-... | CERA returns quote-like labels and brittle face... |
| `cera.rubric_constraint_fidelity` | PC-005 | tighten | prompt | Require CERA to preserve 0.5 rules on 1-mark concepts and... | CERA can simplify away teacher rubric exclusion... |
| `cera.rubric_item_nesting` | TC-013 | restructure | code | Optional RubricItem buckets above CQAs; hybrid 1:1 atomic... | Lose bucket blast-radius control; CERA free to ... |
| `cgr.criteria_first_roles` | PC-011 | restructure | prompt | Remove mechanical ANY=FULL override; criteria-first + rol... | CGR awards FULL when any single catalog facet a... |
| `cgr.exact_evidence_quotes` | PC-002 | tighten | prompt | Require exact contiguous evidence quotes; forbid paraphra... | Signal-1 false DEFERs return on GOOD (Wave2 STU... |
| `cgr.partial_over_absent` | PC-003 | loosen | prompt | Partial-credit policy: prefer PARTIAL over ABSENT; accept... | Mid/purpose answers harsh ABSENT again; Wave3 m... |
| `cgr.partial_rule_precedence` | PC-004 | tighten | prompt | Made concept-specific partial-credit rules override the g... | Generic prefer-PARTIAL wording can override exp... |
| `cgr.semantic_matching` | PC-009 | loosen | prompt | Add meaning-check step and semantic matching block for pa... | CGR returns to literal phrase matching and unde... |
| `cgr.skip_facets_ablation` | TC-017 | measure | code | Add CGRModule(skip_facets=True): blank facets/keywords/va... | Cannot run no-facets ablation without manually ... |
| `cgr.structured_verdicts` | PC-001 | restructure | prompt | Initial v3 CGR prompt: mandatory evidence_span, discrete ... | Lose structured evidence for CBTE; fall back to... |
| `cgr.target_criteria_wiring` | TC-005 | restructure | code | Pass CQA target_criteria into every CGR prompt as the aut... | CGR grades from a lossy knowledge-point summary... |
| `dataset.cn2.human_gold` | TC-008 | tighten | dataset | Human CN2 review: clarified GOOD_01 sender wording; demot... | GOOD_02 wrongly treated as high-band full credi... |
| `dataset.os1.definition_required` | TC-004 | tighten | dataset | Clarified definition mark: FULL requires both explicit de... | CGR may again infer the missing definitions fro... |
| `dataset.real_data_wave5` | TC-010 | measure | dataset | Added first REAL-answer pack: Mohler ASAG E12.Q09 (BST no... | Evaluation evidence stays purely synthetic; FYP... |
| `eval.nofacets_vs_facets` | TC-020 | measure | metric | CE04 2x2 factorial n=8: A1 mae0.50 A2 0.188 A3 0.125 A4 0... | Lose factorial isolation of CE04 MAE drivers |
| `grading.concept_mark_quarters` | TC-012 | restructure | code | Allow CQA concept marks as float multiples of 0.25 (e.g. ... | Concept weights snap back to integers; half-mar... |
| `grading.mark_granularity` | TC-009 | restructure | metric | CANDIDATE (not yet applied): add 0.25 and 0.75 to allowed... | Stays at 0/0.5/1.0; teacher keeps rounding bord... |
| `metrics.pass_bar` | TC-002 | measure | metric | Executable Wave4 pass bar (false ACCEPT, silent zeros, de... | Must manually interpret metrics; easy to miss h... |
| `metrics.silent_zero` | TC-006 | restructure | metric | Changed silent-zero from a hard gate to a review candidat... | Legitimate omitted concepts on otherwise high-b... |
| `ui.accept_audit_surface` | TC-011 | restructure | code | New GET /api/exams/{id}/breakdown plus ExplainPage UI: pe... | Teachers can only see DEFERs again. Accepted ze... |

## History per screw

### `cbte.keyword_variant_matching`

- **TC-007** (2026-07-25, loosen): acceptable_variants now match by token containment (>=0.75 of variant content tokens in answer) as fallback to exact normalized substring; stopword-only variants never hit
  - if reverted: False DEFER on paraphrased-but-correct answers returns (OS1 defer 10%->12.5%, wave3 27->28); Tier-2 NLI runs on items Tier 1 could clear

### `cera.cqa_quality_bar`

- **PC-007** (2026-07-28, tighten): General CERA CQA quality bar: gradable claims not topic labels; ANY only for synonym/one-idea facets; ALL for checklists/compare-contrast/name+explain; name-alone never FULL when ref lists properties; variants paraphrase properties; nested buckets may split independent ideas
  - if reverted: CERA again collapses multi-property definitions and explain-differences questions into weak ANY CQAs; calibrate UI shows concept≈label again

### `cera.evidence_facets_mode`

- **TC-014** (2026-07-26, restructure): Add evidence_facets + evidence_mode (ANY/ALL); validators for ALL-requires-partial, ANY AND-lint, keyword facet coverage, MAY-SPLIT child partial; CGR mechanical ANY/ALL; calibrate_cqas.py
  - if reverted: Advantage/disadvantage leaves become over-strict again; silent wrong zeros return

### `cera.evidence_role_shapes`

- **PC-010** (2026-07-29, restructure): Question-shape step; emit evidence_role+min_count instead of mechanical ANY/ALL
  - if reverted: CERA emits wrong ANY/ALL for name-N-of-M and checklists

### `cera.fake_partial_and_calibrate`

- **TC-015** (2026-07-26, tighten): Reject fake partial_credit_rule strings (null/No partial…) when required; warn-only pre-grade calibration in pipeline (skip on resume; --calibrate-strict opt-in)
  - if reverted: Fake partials pass validation again; no pre-batch smoke warnings

### `cera.hybrid_facet_policy`

- **PC-013** (2026-07-30, restructure): Hybrid facet policy: single-claim synonym_set prefers empty facets; select_n/checklist only for true enumerate/algorithm; forbid over-splitting one definition (frame bursting) into select_n of 3; replace few-shot that taught select_n on concat/transmission/channel-hold
  - if reverted: CERA again emits select_n min=2 of 3 for frame-bursting-style defs → systematic −0.5 PARTIAL tax

### `cera.multi_property_all_mode`

- **PC-006** (2026-07-28, tighten): When reference defines a class as a checklist of distinguishing properties (ACK/loss/flow/connect), use evidence_mode=ALL with per-property partial — not ANY
  - if reverted: Multi-property class definitions collapse back to ANY; one-phrase FULL returns

### `cera.multipart_definition_select_n`

- **PC-012** (2026-07-29, tighten): Multi-part definitions use select_n (e.g. min_count=2 of 3), not synonym_set
  - if reverted: Definition concepts award FULL for a single partial phrase again

### `cera.paraphrase_claim_shape`

- **PC-008** (2026-07-29, tighten): Claim-shaped KPs, semantic facets, 3-5 variants, ANY any-of format, name-any-N list handling
  - if reverted: CERA returns quote-like labels and brittle facets; name-any-N becomes overstrict

### `cera.rubric_constraint_fidelity`

- **PC-005** (2026-07-25, tighten): Require CERA to preserve 0.5 rules on 1-mark concepts and carry explicit FULL/PARTIAL/ABSENT exclusions literally
  - if reverted: CERA can simplify away teacher rubric exclusions, making CGR grade a different rubric from the one the teacher approved

### `cera.rubric_item_nesting`

- **TC-013** (2026-07-26, restructure): Optional RubricItem buckets above CQAs; hybrid 1:1 atomic or 1:N may-split; additive child sums; CERA prompt + validators
  - if reverted: Lose bucket blast-radius control; CERA free to invent global splits again

### `cgr.criteria_first_roles`

- **TC-016** (2026-07-29, restructure): Add evidence_role (synonym_set|checklist|select_n) + min_count; derive legacy evidence_mode; criteria-first CGR; CERA validators for roles
  - if reverted: CE08 naming awards FULL for one challenge again; CGR returns to mechanical ANY=FULL
- **PC-011** (2026-07-29, restructure): Remove mechanical ANY=FULL override; criteria-first + role guidance including select_n count
  - if reverted: CGR awards FULL when any single catalog facet appears

### `cgr.exact_evidence_quotes`

- **PC-002** (2026-07-23, tighten): Require exact contiguous evidence quotes; forbid paraphrase/punctuation changes in evidence_span
  - if reverted: Signal-1 false DEFERs return on GOOD (Wave2 STU_GOOD C3/C4 style)

### `cgr.partial_over_absent`

- **PC-003** (2026-07-23, loosen): Partial-credit policy: prefer PARTIAL over ABSENT; accept synonyms/paraphrase; do not require literal word purpose
  - if reverted: Mid/purpose answers harsh ABSENT again; Wave3 mid under-score worsens

### `cgr.partial_rule_precedence`

- **PC-004** (2026-07-25, tighten): Made concept-specific partial-credit rules override the general PARTIAL preference; forbid inferring a concept from related subparts
  - if reverted: Generic prefer-PARTIAL wording can override explicit rubric exclusions and award inferred credit for omitted concepts

### `cgr.semantic_matching`

- **PC-009** (2026-07-29, loosen): Add meaning-check step and semantic matching block for paraphrase tolerance
  - if reverted: CGR returns to literal phrase matching and under-scores paraphrases

### `cgr.skip_facets_ablation`

- **TC-017** (2026-07-30, measure): Add CGRModule(skip_facets=True): blank facets/keywords/variants in prompt; force synonym_set in prompt for criteria-only ablation tests
  - if reverted: Cannot run no-facets ablation without manually emptying every CQA; CE04-style false PARTIAL tax returns when facets over-split one claim

### `cgr.structured_verdicts`

- **PC-001** (2026-07-20, restructure): Initial v3 CGR prompt: mandatory evidence_span, discrete FULL/PARTIAL/ABSENT/INCORRECT marks
  - if reverted: Lose structured evidence for CBTE; fall back to holistic scores CBTE cannot trust

### `cgr.target_criteria_wiring`

- **TC-005** (2026-07-25, restructure): Pass CQA target_criteria into every CGR prompt as the authoritative scoring contract
  - if reverted: CGR grades from a lossy knowledge-point summary and can violate teacher-authored scoring criteria

### `dataset.cn2.human_gold`

- **TC-008** (2026-07-25, tighten): Human CN2 review: clarified GOOD_01 sender wording; demoted GOOD_02 gold to mid 2.5-3.5; documented LOW_01 as intentional congestion-control confusion; DB1 stem rewritten to one-line exam style; contract test allows human band demotions
  - if reverted: GOOD_02 wrongly treated as high-band full credit; ambiguous GBN wording returns; DB1 looks like a 4-part worksheet again

### `dataset.os1.definition_required`

- **TC-003** (2026-07-25, tighten): Changed OS1 from 4 to 5 marks by adding an explicit process/thread definition-distinction concept; preserved student answers and revised human gold ranges
  - if reverted: The stem/reference will again require a definition that the rubric and CERA do not score, allowing incomplete answers to receive full marks
- **TC-004** (2026-07-25, tighten): Clarified definition mark: FULL requires both explicit definitions; PARTIAL requires one explicit definition; resource-sharing implication alone earns ABSENT
  - if reverted: CGR may again infer the missing definitions from parts (a)-(d), allowing incomplete answers to recover definition credit

### `dataset.real_data_wave5`

- **TC-010** (2026-07-25, measure): Added first REAL-answer pack: Mohler ASAG E12.Q09 (BST node deletion), 28 UNT student answers, gold bands derived from two human graders (0-10 normalized to 0-5); 5-mark rubric authored by us
  - if reverted: Evaluation evidence stays purely synthetic; FYP claim 'works on real answers' unsupported

### `eval.nofacets_vs_facets`

- **TC-018** (2026-07-30, measure): Document CE04 no-facets vs facets MAE and policy: facets for enumerate/count only; criteria-only for single-claim concepts
  - if reverted: Lose CE04 ablation numbers and facet-usage policy note
- **TC-019** (2026-07-30, measure): skip_facets ablation n=8 on CE01/03/05/06/07/08/10 vs facet smoke: CE03/07/08 slightly better without facets; CE10 worse (+0.156 MAE); CE06 tie; CE04 separate run still largest win
  - if reverted: Lose multi-question no-facets vs facets MAE table
- **TC-020** (2026-07-30, measure): CE04 2x2 factorial n=8: A1 mae0.50 A2 0.188 A3 0.125 A4 0.125; criteria rewrite dominates; A3=A4 so empty facets fine once holistic
  - if reverted: Lose factorial isolation of CE04 MAE drivers

### `grading.concept_mark_quarters`

- **TC-012** (2026-07-26, restructure): Allow CQA concept marks as float multiples of 0.25 (e.g. 1.5); awards stay 0/half/full of the concept. Float-safe CERA mark-sum check; format_marks keeps whole numbers as '1' not '1.0' in CGR prompts; CERA prompt tells the LLM not to round half marks to int.
  - if reverted: Concept weights snap back to integers; half-mark rubric clauses are silently rounded and CERA drifts from teacher rubrics again.

### `grading.mark_granularity`

- **TC-009** (2026-07-25, restructure): CANDIDATE (not yet applied): add 0.25 and 0.75 to allowed_marks_fractions so verdicts can express quarter-credit
  - if reverted: Stays at 0/0.5/1.0; teacher keeps rounding borderline answers, adding noise to band-hit/MAE

### `metrics.pass_bar`

- **TC-002** (2026-07-25, measure): Executable Wave4 pass bar (false ACCEPT, silent zeros, defer rate, high-band hit, mid not all zero)
  - if reverted: Must manually interpret metrics; easy to miss high-band misses or silent zeros

### `metrics.silent_zero`

- **TC-001** (2026-07-25, measure): Count ACCEPT+0 marks on HIGH-band (GOOD) students as silent_zero
  - if reverted: Pass bar and ledger cannot detect Wave4 OS1-style silent zeros on GOOD
- **TC-006** (2026-07-25, restructure): Changed silent-zero from a hard gate to a review candidate unless concept-level human gold confirms the zero was unexpected
  - if reverted: Legitimate omitted concepts on otherwise high-band students can falsely fail the pass bar

### `ui.accept_audit_surface`

- **TC-011** (2026-07-25, restructure): New GET /api/exams/{id}/breakdown plus ExplainPage UI: per-student, per-concept 'why these marks' view (verdict, marks, reasoning, quoted evidence, keyword found/missing split, CBTE signals, teacher override). Adds a cohort 'rubric health' strip and a 'Zeros never checked' filter that lists ACCEPTed zero-mark judgments.
  - if reverted: Teachers can only see DEFERs again. Accepted zeros stay invisible, dead rubric concepts stay undetectable without a hand-written script, and every underscoring diagnosis needs a developer reading grading_results.json.
