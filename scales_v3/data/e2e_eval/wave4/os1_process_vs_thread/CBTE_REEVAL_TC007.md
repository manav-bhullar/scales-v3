# Wave 2 CBTE re-eval (Signal-1 fix)

- Exam: `e2e_wave4_os1_process_vs_thread`
- NLI: on
- DEFER before → after: **5 → 4**
- Decision/tier flips: **2**
- False DEFER on STU_GOOD/STU_GOOD_ALT C3/C4: **0** (none)

## Flips

- `OS1_GOOD_01/Q1_C5`: ACCEPT(t2) → ACCEPT(t1) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.98
  - new: Tier 1 auto-accept: evidence verified, keyword_score=0.50 (1 keywords found)
- `OS1_MID_01/Q1_C1`: DEFER(t3) → ACCEPT(t1) | sig1=True
  - old: Tier 3: trust=0.37 (nli=0.17, stab=1.0, kw=0.00, tau=0.50)
  - new: Tier 1 auto-accept: evidence verified, keyword_score=0.33 (0 keywords found)
