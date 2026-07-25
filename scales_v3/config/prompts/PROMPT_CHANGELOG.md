# Tuning Changelog (prompts + screws)

Tracks **what** we changed, **why**, which **screw**, **tighten/loosen**, and
**if reverted** what happens. This is the research trail — not a general diary.

| File | Role |
|------|------|
| `PROMPT_CHANGELOG.md` | Human-readable history (this file; auto-rebuilt) |
| `SCREWS.md` | Index of named knobs + latest turn |
| `changes.jsonl` | Append-only machine ledger |
| `snapshots/` | Frozen copies after each logged change |
| `../../scripts/log_prompt_change.py` | CLI |

## How to log a change

```powershell
cd scales_v3
# Prompt
python scripts/log_prompt_change.py add `
  --prompt cgr_grading.txt `
  --screw cgr.partial_over_absent `
  --direction loosen `
  --what "..." `
  --why "..." `
  --if-reverted "..." `
  --tradeoff "..." `
  --evidence "wave / student / metric"

# Code / metric / settings
python scripts/log_prompt_change.py add `
  --kind metric `
  --artifact scripts/metrics_ledger.py `
  --screw metrics.silent_zero `
  --direction measure `
  --what "..." `
  --why "..." `
  --if-reverted "..." `
  --evidence "..."
```

## Directions

| Direction | Meaning |
|-----------|---------|
| `tighten` | Stricter (harder to get credit / more DEFER) |
| `loosen` | Softer (more PARTIAL/ACCEPT) |
| `restructure` | Behavioural redesign (not a simple dial) |
| `measure` | New metric / observability only (no grader change) |

## Rules

- Log **every** intentional prompt, threshold, code, or metric change.
- **Why** must name the failure (student id, wave, metric, failure mode).
- **if-reverted** is mandatory — so the next person knows the cost of undoing.
- Do not rewrite old entries — append a new turn on the same `--screw`.

---

## History


### TC-002 — 2026-07-25 — `scripts/metrics_ledger.py` — `metrics.pass_bar` (measure)

**Kind:** metric  
**Direction:** measure

**Screw:** `metrics.pass_bar`

**What:** Executable Wave4 pass bar (false ACCEPT, silent zeros, defer rate, high-band hit, mid not all zero)

**Why:** Roadmap pass table was eyeballed; need machine verdict after every ledger row

**If reverted:** Must manually interpret metrics; easy to miss high-band misses or silent zeros

**Tradeoff:** Smoke thresholds (defer<=40 percent) are noisy on n=8; investigate not auto-tune from FAIL alone

**Evidence:** data/e2e_eval/wave4/README.md pass bar; tests/unit/test_pass_bar.py

**Result:** metrics_ledger prints PASS BAR and stores pass_bar in JSONL

**Snapshot:** `snapshots/TC-002_metrics_ledger.py`

**File hash (16):** `c1a0c1af8ce04f23`


### TC-001 — 2026-07-25 — `scripts/metrics_ledger.py` — `metrics.silent_zero` (measure)

**Kind:** metric  
**Direction:** measure

**Screw:** `metrics.silent_zero`

**What:** Count ACCEPT+0 marks on HIGH-band (GOOD) students as silent_zero

**Why:** GOOD answers collapsed PARTIAL->ABSENT then Tier-1 ACCEPT; false_accept only watches LOW so this failure was invisible

**If reverted:** Pass bar and ledger cannot detect Wave4 OS1-style silent zeros on GOOD

**Tradeoff:** Scoped to HIGH band only; mid ABSENT accepts stay normal and do not inflate the counter

**Evidence:** wave4 OS1 grade_run1.log; Wave3 provisional under-score analysis

**Result:** metric + pass-bar criterion no_silent_zeros; unit tests pinned

**Snapshot:** `snapshots/TC-001_metrics_ledger.py`

**File hash (16):** `c1a0c1af8ce04f23`


### PC-003 — 2026-07-23 — `cgr_grading.txt` — `cgr.partial_over_absent` (loosen)

**Kind:** prompt  
**Direction:** loosen

**Screw:** `cgr.partial_over_absent`

**What:** Partial-credit policy: prefer PARTIAL over ABSENT; accept synonyms/paraphrase; do not require literal word purpose

**Why:** Mid/purpose-focus answers marked ABSENT with empty evidence despite informal on-topic wording

**If reverted:** Mid/purpose answers harsh ABSENT again; Wave3 mid under-score worsens

**Tradeoff:** May give PARTIAL on thin on-topic text; monitor false ACCEPT on LOW

**Evidence:** data/e2e_eval/wave2/DEFER_DIAGNOSIS.txt; wave3/VALIDATION.md (measures this change)

**Result:** Softer ABSENT on mid band; Wave3 evaluates at n=24

**Snapshot:** `snapshots/PC-003_cgr_grading.txt`


### PC-002 — 2026-07-23 — `cgr_grading.txt` — `cgr.exact_evidence_quotes` (tighten)

**Kind:** prompt  
**Direction:** tighten

**Screw:** `cgr.exact_evidence_quotes`

**What:** Require exact contiguous evidence quotes; forbid paraphrase/punctuation changes in evidence_span

**Why:** Signal-1 false DEFER on good answers: hallucinated or normalized quotes not found in student text (curly apostrophe, arrows)

**If reverted:** Signal-1 false DEFERs return on GOOD (Wave2 STU_GOOD C3/C4 style)

**Tradeoff:** Stricter quoting can empty evidence → PARTIAL downgraded to ABSENT (watch silent zeros)

**Evidence:** data/e2e_eval/wave2/WAVE2_SIGNAL1_REEVAL.md; FIX_VERIFICATION.txt; STU_GOOD/Q1_C3, STU_GOOD_ALT/Q1_C4

**Result:** With code normalize fix, GOOD C3 flipped DEFER->ACCEPT


### PC-001 — 2026-07-20 — `cgr_grading.txt` — `cgr.structured_verdicts` (restructure)

**Kind:** prompt  
**Direction:** restructure

**Screw:** `cgr.structured_verdicts`

**What:** Initial v3 CGR prompt: mandatory evidence_span, discrete FULL/PARTIAL/ABSENT/INCORRECT marks

**Why:** CBTE Tier-1 needs externally verifiable quotes; structured concept grading replaces holistic LLM scores

**If reverted:** Lose structured evidence for CBTE; fall back to holistic scores CBTE cannot trust

**Tradeoff:** Requires models that follow JSON schema and quote evidence faithfully

**Evidence:** documentation/design/implementation_plan.md; engineering reviews

**Result:** Baseline prompts for Wave1-Wave3

**Also touched:** `cera_extraction.txt`

**Snapshot:** `snapshots/PC-001_cera_extraction.txt`
