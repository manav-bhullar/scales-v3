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
| `dataset.os1.definition_required` | TC-004 | tighten | dataset | Clarified definition mark: FULL requires both explicit de... | CGR may again infer the missing definitions fro... |
| `metrics.pass_bar` | TC-002 | measure | metric | Executable Wave4 pass bar (false ACCEPT, silent zeros, de... | Must manually interpret metrics; easy to miss h... |
| `metrics.silent_zero` | TC-006 | restructure | metric | Changed silent-zero from a hard gate to a review candidat... | Legitimate omitted concepts on otherwise high-b... |

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

### `dataset.os1.definition_required`

- **TC-003** (2026-07-25, tighten): Changed OS1 from 4 to 5 marks by adding an explicit process/thread definition-distinction concept; preserved student answers and revised human gold ranges
  - if reverted: The stem/reference will again require a definition that the rubric and CERA do not score, allowing incomplete answers to receive full marks
- **TC-004** (2026-07-25, tighten): Clarified definition mark: FULL requires both explicit definitions; PARTIAL requires one explicit definition; resource-sharing implication alone earns ABSENT
  - if reverted: CGR may again infer the missing definitions from parts (a)-(d), allowing incomplete answers to recover definition credit

### `metrics.pass_bar`

- **TC-002** (2026-07-25, measure): Executable Wave4 pass bar (false ACCEPT, silent zeros, defer rate, high-band hit, mid not all zero)
  - if reverted: Must manually interpret metrics; easy to miss high-band misses or silent zeros

### `metrics.silent_zero`

- **TC-001** (2026-07-25, measure): Count ACCEPT+0 marks on HIGH-band (GOOD) students as silent_zero
  - if reverted: Pass bar and ledger cannot detect Wave4 OS1-style silent zeros on GOOD
- **TC-006** (2026-07-25, restructure): Changed silent-zero from a hard gate to a review candidate unless concept-level human gold confirms the zero was unexpected
  - if reverted: Legitimate omitted concepts on otherwise high-band students can falsely fail the pass bar
