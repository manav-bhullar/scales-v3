# Wave 2 CBTE re-eval (Signal-1 fix)

- Exam: `e2e_wave3_tcp_handshake_expanded`
- NLI: on
- DEFER before → after: **28 → 27**
- Decision/tier flips: **2**
- False DEFER on STU_GOOD/STU_GOOD_ALT C3/C4: **0** (none)

## Flips

- `W3_GOOD_04/Q1_C3`: DEFER(t3) → ACCEPT(t1) | sig1=True
  - old: Tier 3: trust=0.30 (nli=0.01, stab=1.0, kw=0.00, tau=0.50)
  - new: Tier 1 auto-accept: evidence verified, keyword_score=0.50 (0 keywords found)
- `W3_GOOD_05/Q1_C3`: ACCEPT(t2) → ACCEPT(t1) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.89
  - new: Tier 1 auto-accept: evidence verified, keyword_score=0.50 (0 keywords found)
