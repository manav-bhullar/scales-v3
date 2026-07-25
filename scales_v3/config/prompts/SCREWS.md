# Screws — current knobs

Named tuning knobs and their **latest** logged turn.
Before you tighten/loosen again, read `if_reverted` on the latest entry.

Full history: `PROMPT_CHANGELOG.md` / `changes.jsonl`.

| Screw | Last id | Direction | Kind | What (latest) | If reverted |
|-------|---------|-----------|------|---------------|-------------|
| `cbte.keyword_variant_matching` | TC-007 | loosen | code | acceptable_variants now match by token containment (>=0.7... | False DEFER on paraphrased-but-correct answers ... |
| `cera.rubric_constraint_fidelity` | PC-005 | tighten | prompt | Require CERA to preserve 0.5 rules on 1-mark concepts and... | CERA can simplify away teacher rubric exclusion... |
| `cgr.exact_evidence_quotes` | PC-002 | tighten | prompt | Require exact contiguous evidence quotes; forbid paraphra... | Signal-1 false DEFERs return on GOOD (Wave2 STU... |
| `cgr.partial_over_absent` | PC-003 | loosen | prompt | Partial-credit policy: prefer PARTIAL over ABSENT; accept... | Mid/purpose answers harsh ABSENT again; Wave3 m... |
| `cgr.partial_rule_precedence` | PC-004 | tighten | prompt | Made concept-specific partial-credit rules override the g... | Generic prefer-PARTIAL wording can override exp... |
| `cgr.structured_verdicts` | PC-001 | restructure | prompt | Initial v3 CGR prompt: mandatory evidence_span, discrete ... | Lose structured evidence for CBTE; fall back to... |
| `cgr.target_criteria_wiring` | TC-005 | restructure | code | Pass CQA target_criteria into every CGR prompt as the aut... | CGR grades from a lossy knowledge-point summary... |
| `dataset.cn2.human_gold` | TC-008 | tighten | dataset | Human CN2 review: clarified GOOD_01 sender wording; demot... | GOOD_02 wrongly treated as high-band full credi... |
| `dataset.os1.definition_required` | TC-004 | tighten | dataset | Clarified definition mark: FULL requires both explicit de... | CGR may again infer the missing definitions fro... |
| `dataset.real_data_wave5` | TC-010 | measure | dataset | Added first REAL-answer pack: Mohler ASAG E12.Q09 (BST no... | Evaluation evidence stays purely synthetic; FYP... |
| `grading.mark_granularity` | TC-009 | restructure | metric | CANDIDATE (not yet applied): add 0.25 and 0.75 to allowed... | Stays at 0/0.5/1.0; teacher keeps rounding bord... |
| `metrics.pass_bar` | TC-002 | measure | metric | Executable Wave4 pass bar (false ACCEPT, silent zeros, de... | Must manually interpret metrics; easy to miss h... |
| `metrics.silent_zero` | TC-006 | restructure | metric | Changed silent-zero from a hard gate to a review candidat... | Legitimate omitted concepts on otherwise high-b... |
| `ui.accept_audit_surface` | TC-011 | restructure | code | New GET /api/exams/{id}/breakdown plus ExplainPage UI: pe... | Teachers can only see DEFERs again. Accepted ze... |

## History per screw

### `cbte.keyword_variant_matching`

- **TC-007** (2026-07-25, loosen): acceptable_variants now match by token containment (>=0.75 of variant content tokens in answer) as fallback to exact normalized substring; stopword-only variants never hit
  - if reverted: False DEFER on paraphrased-but-correct answers returns (OS1 defer 10%->12.5%, wave3 27->28); Tier-2 NLI runs on items Tier 1 could clear

### `cera.rubric_constraint_fidelity`

- **PC-005** (2026-07-25, tighten): Require CERA to preserve 0.5 rules on 1-mark concepts and carry explicit FULL/PARTIAL/ABSENT exclusions literally
  - if reverted: CERA can simplify away teacher rubric exclusions, making CGR grade a different rubric from the one the teacher approved

### `cgr.exact_evidence_quotes`

- **PC-002** (2026-07-23, tighten): Require exact contiguous evidence quotes; forbid paraphrase/punctuation changes in evidence_span
  - if reverted: Signal-1 false DEFERs return on GOOD (Wave2 STU_GOOD C3/C4 style)

### `cgr.partial_over_absent`

- **PC-003** (2026-07-23, loosen): Partial-credit policy: prefer PARTIAL over ABSENT; accept synonyms/paraphrase; do not require literal word purpose
  - if reverted: Mid/purpose answers harsh ABSENT again; Wave3 mid under-score worsens

### `cgr.partial_rule_precedence`

- **PC-004** (2026-07-25, tighten): Made concept-specific partial-credit rules override the general PARTIAL preference; forbid inferring a concept from related subparts
  - if reverted: Generic prefer-PARTIAL wording can override explicit rubric exclusions and award inferred credit for omitted concepts

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
