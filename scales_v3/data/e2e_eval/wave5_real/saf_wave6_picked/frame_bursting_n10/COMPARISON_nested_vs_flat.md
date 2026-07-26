# Nested hybrid vs Flat (rubric=concept) — Q-BURST n=10
Same question, same 10 students, same model (gemini-3.1-flash-lite).
## 1. Nested analysis (before flat run)
- **Structure:** R1 Definition `atomic` → 1×1.5; R2 Adv+Disadv `may-split` → 0.75+0.75.
- **CERA obeyed** the atomic/split contract.
- **Main failure mode:** Advantage leaf (C2) required *mechanism* (“real data vs padding/garbage”), with **no PARTIAL**. Students who only said “more efficient” got **ABSENT** (8/10). That drove **UNDER** scores vs SAF humans (who credit efficiency without the why).
- Nested MAE **0.60**, band-hit **3/10**, OVER 1 / UNDER 6, DEFERs **12** (cohort audit piled on C2).

## 2. Flat CERA (what it produced)
- `Q1_C1` **1.5**: Definition of frame bursting
  - criteria: FULL: conveys that multiple frames are concatenated / sent in one transmission (and ideally without releasing the channel / shared medium control).
  - partial: PARTIAL (0.75): vague mention of bursting/sending multiple frames without the concatenation / single-transmission idea. ABSENT: missing or wrong.
- `Q1_C2` **1.5**: Advantage and disadvantage of frame bursting compared to carrier extension
  - criteria: FULL (1.5): states both an advantage (e.g., higher efficiency/no padding) AND a disadvantage (e.g., delay/buffering) vs carrier extension.
  - partial: PARTIAL (0.75): only advantage OR only disadvantage (one side present). ABSENT: neither side present or wrong.

## 3. Nested CERA (reminder)
- `Q1_C1` [R1] **1.5**: Definition of frame bursting
- `Q1_C2` [R2] **0.75**: Advantage of frame bursting over carrier extension
- `Q1_C3` [R2] **0.75**: Disadvantage of frame bursting over carrier extension

## 4. Score comparison
| student | human | nested | flat | Δ(n-h) | Δ(f-h) | winner |
|---|---:|---:|---:|---:|---:|:---:|
| BURST_00 | 3.00 | 1.50 | 3.00 | -1.50 | +0.00 | flat |
| BURST_01 | 3.00 | 2.25 | 2.25 | -0.75 | -0.75 | tie |
| BURST_02 | 3.00 | 3.00 | 3.00 | +0.00 | +0.00 | tie |
| BURST_03 | 2.25 | 3.00 | 3.00 | +0.75 | +0.75 | tie |
| BURST_04 | 2.25 | 1.50 | 2.25 | -0.75 | +0.00 | flat |
| BURST_05 | 2.25 | 2.25 | 2.25 | +0.00 | +0.00 | tie |
| BURST_06 | 2.25 | 1.50 | 2.25 | -0.75 | +0.00 | flat |
| BURST_07 | 1.50 | 0.75 | 1.50 | -0.75 | +0.00 | flat |
| BURST_08 | 1.50 | 0.75 | 1.50 | -0.75 | +0.00 | flat |
| BURST_09 | 0.00 | 0.00 | 0.00 | +0.00 | +0.00 | tie |

## 5. Aggregate
| metric | nested hybrid | flat rubric=concept |
|---|---:|---:|
| # concepts | 3 | 2 |
| MAE vs human | 0.6 | 0.15 |
| Band-hit (±~0.4) | 3/10 | 8/10 |
| OVER / UNDER | 1 / 6 | 1 / 1 |
| Mean score | 1.65 | 2.1 |
| DEFER items | 12 | 7 |
| Closer to human (per student) | 0 | 5 (ties 5) |

## 6. Verdict
**Flat wins on this pack** (MAE 0.15 vs 0.6).

Why: flat keeps Adv+Disadv as **one** concept with an explicit PARTIAL (one side → 0.75). Nested’s split made Advantage a separate leaf with a **stricter FULL bar and no PARTIAL**, so ‘more efficient’ → 0 instead of 0.75 toward the trade-off bucket. Splitting is correct structurally; the regression is **criteria tightness on the advantage leaf**, not the nesting machinery itself.

## 7. Flat per-student verdicts
- BURST_00: Q1_C1=FULL/1.5, Q1_C2=FULL/1.5 → **3.00**
- BURST_01: Q1_C1=FULL/1.5, Q1_C2=PARTIAL/0.75 → **2.25**
- BURST_02: Q1_C1=FULL/1.5, Q1_C2=FULL/1.5 → **3.00**
- BURST_03: Q1_C1=FULL/1.5, Q1_C2=FULL/1.5 → **3.00**
- BURST_04: Q1_C1=FULL/1.5, Q1_C2=PARTIAL/0.75 → **2.25**
- BURST_05: Q1_C1=FULL/1.5, Q1_C2=PARTIAL/0.75 → **2.25**
- BURST_06: Q1_C1=FULL/1.5, Q1_C2=PARTIAL/0.75 → **2.25**
- BURST_07: Q1_C1=ABSENT/0.0, Q1_C2=FULL/1.5 → **1.50**
- BURST_08: Q1_C1=ABSENT/0.0, Q1_C2=FULL/1.5 → **1.50**
- BURST_09: Q1_C1=ABSENT/0.0, Q1_C2=ABSENT/0.0 → **0.00**
