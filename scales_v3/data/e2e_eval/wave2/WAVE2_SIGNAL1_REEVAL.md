# Wave 2 CBTE re-eval (Signal-1 fix)

- Exam: `e2e_wave5_mohler_bst_delete`
- NLI: off
- DEFER before → after: **23 → 33**
- Decision/tier flips: **10**
- False DEFER on STU_GOOD/STU_GOOD_ALT C3/C4: **0** (none)

## Flips

- `MOH_A05/Q1_C3`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.98
  - new: Tier 3: trust=0.36 (nli=0.00, stab=1.0, kw=0.20, tau=0.50)
- `MOH_A11/Q1_C2`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.97
  - new: Tier 3: trust=0.30 (nli=0.00, stab=1.0, kw=0.00, tau=0.50)
- `MOH_A11/Q1_C3`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.98
  - new: Tier 3: trust=0.36 (nli=0.00, stab=1.0, kw=0.20, tau=0.50)
- `MOH_A12/Q1_C2`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 1.00
  - new: Tier 3: trust=0.38 (nli=0.00, stab=1.0, kw=0.25, tau=0.50)
- `MOH_A15/Q1_C3`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.96
  - new: Tier 3: trust=0.30 (nli=0.00, stab=1.0, kw=0.00, tau=0.50)
- `MOH_A17/Q1_C3`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.99
  - new: Tier 3: trust=0.30 (nli=0.00, stab=1.0, kw=0.00, tau=0.50)
- `MOH_A20/Q1_C3`: ACCEPT(t3) → DEFER(t3) | sig1=True
  - old: Tier 3: trust=0.58 (nli=0.54, stab=1.0, kw=0.20, tau=0.50)
  - new: Tier 3: trust=0.36 (nli=0.00, stab=1.0, kw=0.20, tau=0.50)
- `MOH_A21/Q1_C2`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.76
  - new: Tier 3: trust=0.38 (nli=0.00, stab=1.0, kw=0.25, tau=0.50)
- `MOH_A24/Q1_C2`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.95
  - new: Tier 3: trust=0.38 (nli=0.00, stab=1.0, kw=0.25, tau=0.50)
- `MOH_A26/Q1_C2`: ACCEPT(t2) → DEFER(t3) | sig1=True
  - old: Tier 2 accept: NLI entailment = 0.94
  - new: Tier 3: trust=0.30 (nli=0.00, stab=1.0, kw=0.00, tau=0.50)
