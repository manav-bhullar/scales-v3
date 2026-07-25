# Wave 4 / Q-OS1 — Gemini smoke report

**Run id:** `wave4_os1_gemini_smoke_v1`
**Model:** `gemini/gemini-3.1-flash-lite` (temperature 0.1, max_concurrent_calls 1)
**Date:** 2026-07-25
**Log:** `grade_gemini_v1.log`
**Exam store:** `data/exams/e2e_wave4_os1_process_vs_thread/`

Supersedes the earlier `grade_run1.log` (OpenRouter Llama-3.1-8B), which is not
usable as evidence: repeated JSON truncation at `max_tokens=2048` emptied
`evidence_span`, CGR downgraded PARTIAL to ABSENT, and CBTE Tier 1 auto-accepted
those zeros at trust 0.90.

## Pass bar — PASS

| Criterion | Observed | Limit |
|-----------|----------|-------|
| `no_false_accept_on_low` | 0 | 0 |
| `no_silent_zeros` | 0 | 0 |
| `defer_rate_within_limit` | 0.2188 | 0.40 |
| `high_band_students_in_band` | none missed | none |
| `mid_band_not_all_zero` | 0 of 4 zeroed | < 4 |

Other metrics: `n_items=32`, `band_hit_rate=1.0`, `mark_mae_vs_band_mid=0.25`,
`false_defer_count=5` (0.1562).

## CQAs (hand-check — Phase B exit criterion)

Marks sum = 4 = `total_marks`. Decomposition is MECE and matches the rubric.

| Concept | Marks | Knowledge point | Expected keywords |
|---------|-------|-----------------|-------------------|
| `Q1_C1` | 1 | Resources shared by threads within a process | address space, shared memory, code, data, heap |
| `Q1_C2` | 1 | Resources private to each thread | stack, registers, program counter, thread context |
| `Q1_C3` | 1 | Advantage of multithreading over multiprocess | lighter weight, faster context switch, shared memory communication |
| `Q1_C4` | 1 | Disadvantage or risk of multithreading | isolation, memory corruption, synchronization, race conditions |

## Per-student provisional (ACCEPT-only totals)

| Student | Band | Prov | Gold range | In band | Concept trace |
|---------|------|------|------------|---------|---------------|
| `OS1_GOOD_01` | high | 4.0 | 3.0–4.0 | yes | C1 FULL T1, C2 FULL T1, C3 FULL T2, C4 FULL T2 — all ACCEPT |
| `OS1_GOOD_02` | high | 4.0 | 3.0–4.0 | yes | all four FULL, ACCEPT at Tier 1 |
| `OS1_MID_01` | mid_low | 2.0 | 1.0–2.5 | yes | C1 FULL T2 ACCEPT, C2 ABSENT T1 ACCEPT, C3 FULL T2 ACCEPT, **C4 FULL T3 DEFER** |
| `OS1_MID_02` | mid | 2.0 | 1.5–3.0 | yes | C1 FULL T2 ACCEPT, **C2 FULL T3 DEFER**, C3 FULL T2 ACCEPT, **C4 FULL T3 DEFER** |
| `OS1_PARTIAL_A` | mid_low | 1.0 | 0.5–1.5 | yes | C1 FULL T1 ACCEPT, C2/C3/C4 ABSENT T1 ACCEPT (correctly sparse) |
| `OS1_PARTIAL_B` | mid_low | 1.0 | 0.5–2.0 | yes | C1 FULL T2 ACCEPT, C2 ABSENT T1 ACCEPT, **C3 FULL T3 DEFER**, **C4 FULL T3 DEFER** |
| `OS1_LOW_01` | low | 0.0 | 0.0–0.5 | yes | C1/C2 INCORRECT 0.0 T3 DEFER, C3/C4 ABSENT T1 ACCEPT |
| `OS1_LOW_02` | low | 0.0 | 0.0–0.0 | yes | all four ABSENT T1 ACCEPT |

Safety reads correctly: both LOW students sit at 0.0, and `OS1_LOW_01`'s two
inverted-fact concepts were routed to a human rather than silently credited.

## Worst remaining failure mode — false DEFER on FULL

5 of 32 items (15.6%). CGR returned FULL with evidence that is genuinely present
in the answer, but Tier 1 did not fire and NLI did not clear 0.7, so Tier 3
deferred.

| Item | Verdict | Evidence | Tier 3 trust |
|------|---------|----------|--------------|
| `OS1_MID_02/Q1_C2` | FULL 1.0 | `Each thread has its own stack.` | 0.38 (nli 0.00, kw 0.25) |
| `OS1_PARTIAL_B/Q1_C4` | FULL 1.0 | `need synchronization because of races` | 0.38 (nli 0.00, kw 0.25) |
| `OS1_PARTIAL_B/Q1_C3` | FULL 1.0 | `threads are lighter and can share memory easily` | 0.31 (nli 0.03, kw 0.00) |
| `OS1_MID_01/Q1_C4` | FULL 1.0 | `But threads can interfere with each other.` | 0.36 (nli 0.15, kw 0.00) |
| `OS1_MID_02/Q1_C4` | FULL 1.0 | `I know there is some isolation problem` | 0.38 (nli 0.00, kw 0.25) |

Mechanism: `expected_keywords` are multi-word phrases (`program counter`,
`race conditions`), so a correct short answer matches at most one of four terms.
`keyword_score = 1/4 = 0.25`, which is below `tier1_keyword_threshold = 0.3`, so
the item escalates. Tier 2 then compares a short evidence fragment against the
knowledge point and scores near 0. Tier 3 sums to ~0.31–0.38, under `tau = 0.5`.

This costs teacher time but not safety — `false_accept_count` stays 0.

## Next screw (one change only)

Candidate: **`cbte.tier1_keyword_threshold`** (or phrase-level matching in
`fuzzy_keyword_match`) so a FULL verdict with verified evidence and one strong
keyword hit resolves at Tier 1.

Do **not** touch the CGR prompt yet — Gemini's grading judgment matched gold on
all 8 students. The problem is trust estimation, not grading.

Whatever we change, log it:

```powershell
python scripts/log_prompt_change.py add `
  --kind settings --artifact config/settings.yaml `
  --screw cbte.tier1_keyword_threshold --direction loosen `
  --what "..." --why "..." --if-reverted "..." `
  --evidence "wave4 OS1 MID_02/Q1_C2, PARTIAL_B/Q1_C3"
```

## Open items

- [ ] SHRR review of the 7 DEFERs, then `metrics_ledger --post-review`
- [ ] Wave 3 TCP regression after any threshold change (Step 6)
- [ ] Q-CN2 and Q-DB1 smoke on the same settings
