# Screws — current knobs

Named tuning knobs and their **latest** logged turn.
Before you tighten/loosen again, read `if_reverted` on the latest entry.

Full history: `PROMPT_CHANGELOG.md` / `changes.jsonl`.

| Screw | Last id | Direction | Kind | What (latest) | If reverted |
|-------|---------|-----------|------|---------------|-------------|
| `cgr.exact_evidence_quotes` | PC-002 | tighten | prompt | Require exact contiguous evidence quotes; forbid paraphra... | Signal-1 false DEFERs return on GOOD (Wave2 STU... |
| `cgr.partial_over_absent` | PC-003 | loosen | prompt | Partial-credit policy: prefer PARTIAL over ABSENT; accept... | Mid/purpose answers harsh ABSENT again; Wave3 m... |
| `cgr.structured_verdicts` | PC-001 | restructure | prompt | Initial v3 CGR prompt: mandatory evidence_span, discrete ... | Lose structured evidence for CBTE; fall back to... |
| `metrics.pass_bar` | TC-002 | measure | metric | Executable Wave4 pass bar (false ACCEPT, silent zeros, de... | Must manually interpret metrics; easy to miss h... |
| `metrics.silent_zero` | TC-001 | measure | metric | Count ACCEPT+0 marks on HIGH-band (GOOD) students as sile... | Pass bar and ledger cannot detect Wave4 OS1-sty... |

## History per screw

### `cgr.exact_evidence_quotes`

- **PC-002** (2026-07-23, tighten): Require exact contiguous evidence quotes; forbid paraphrase/punctuation changes in evidence_span
  - if reverted: Signal-1 false DEFERs return on GOOD (Wave2 STU_GOOD C3/C4 style)

### `cgr.partial_over_absent`

- **PC-003** (2026-07-23, loosen): Partial-credit policy: prefer PARTIAL over ABSENT; accept synonyms/paraphrase; do not require literal word purpose
  - if reverted: Mid/purpose answers harsh ABSENT again; Wave3 mid under-score worsens

### `cgr.structured_verdicts`

- **PC-001** (2026-07-20, restructure): Initial v3 CGR prompt: mandatory evidence_span, discrete FULL/PARTIAL/ABSENT/INCORRECT marks
  - if reverted: Lose structured evidence for CBTE; fall back to holistic scores CBTE cannot trust

### `metrics.pass_bar`

- **TC-002** (2026-07-25, measure): Executable Wave4 pass bar (false ACCEPT, silent zeros, defer rate, high-band hit, mid not all zero)
  - if reverted: Must manually interpret metrics; easy to miss high-band misses or silent zeros

### `metrics.silent_zero`

- **TC-001** (2026-07-25, measure): Count ACCEPT+0 marks on HIGH-band (GOOD) students as silent_zero
  - if reverted: Pass bar and ledger cannot detect Wave4 OS1-style silent zeros on GOOD
