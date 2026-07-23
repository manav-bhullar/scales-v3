# Wave 2 CBTE re-eval (Signal-1 fix)

- Exam: `e2e_wave2_tcp_handshake_groq`
- NLI: on
- DEFER before → after: **8 → 7**
- Decision/tier flips: **2**
- False DEFER on STU_GOOD/STU_GOOD_ALT C3/C4: **1** (STU_GOOD_ALT/Q1_C4)

## Flips

- `STU_GOOD/Q1_C3`: DEFER(t1) → ACCEPT(t1) | sig1=True
  - old: LLM quoted evidence not found in student answer (hallucinated quote)
  - new: Tier 1 auto-accept: evidence verified, keyword_score=0.50 (1 keywords found)
- `STU_GOOD_ALT/Q1_C4`: DEFER(t1) → DEFER(t3) | sig1=True
  - old: LLM quoted evidence not found in student answer (hallucinated quote)
  - new: Tier 3: trust=0.33 (nli=0.09, stab=1.0, kw=0.00, tau=0.50)
