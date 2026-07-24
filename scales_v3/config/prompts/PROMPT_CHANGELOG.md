# Prompt Fine-Tuning Changelog

Tracks **what we changed in grader/extractor prompts** and **why**.

This is the research trail for prompt iteration — not a general project diary.

| File | Role |
|------|------|
| `PROMPT_CHANGELOG.md` | Human-readable history (this file; auto-rebuilt from `changes.jsonl`) |
| `changes.jsonl` | Append-only machine ledger |
| `snapshots/` | Frozen copies of prompt files after each logged change |
| `../../scripts/log_prompt_change.py` | CLI to record a change |

## How to log a prompt edit

```powershell
cd scales_v3
python scripts/log_prompt_change.py add `
  --prompt cgr_grading.txt `
  --what "Describe the wording change" `
  --why "What failure / metric motivated it" `
  --evidence "wave / student ids / paths" `
  --result "What improved (optional)"
```

## Rules

- Log **every** intentional prompt edit, even small wording tweaks.
- **Why** must name the failure you saw (student id, wave, metric, or failure mode).
- Do not rewrite old entries — append a correction entry if needed.

---

## History


### PC-003 — 2026-07-23 — `cgr_grading.txt`

**What:** Partial-credit policy: prefer PARTIAL over ABSENT; accept synonyms/paraphrase; do not require literal word purpose

**Why:** Mid/purpose-focus answers marked ABSENT with empty evidence despite informal on-topic wording

**Evidence:** data/e2e_eval/wave2/DEFER_DIAGNOSIS.txt; wave3/VALIDATION.md (measures this change)

**Result:** Softer ABSENT on mid band; Wave3 evaluates at n=24

**Snapshot:** `snapshots/PC-003_cgr_grading.txt`


### PC-002 — 2026-07-23 — `cgr_grading.txt`

**What:** Require exact contiguous evidence quotes; forbid paraphrase/punctuation changes in evidence_span

**Why:** Signal-1 false DEFER on good answers: hallucinated or normalized quotes not found in student text (curly apostrophe, arrows)

**Evidence:** data/e2e_eval/wave2/WAVE2_SIGNAL1_REEVAL.md; FIX_VERIFICATION.txt; STU_GOOD/Q1_C3, STU_GOOD_ALT/Q1_C4

**Result:** With code normalize fix, GOOD C3 flipped DEFER->ACCEPT


### PC-001 — 2026-07-20 — `cgr_grading.txt`

**What:** Initial v3 CGR prompt: mandatory evidence_span, discrete FULL/PARTIAL/ABSENT/INCORRECT marks

**Why:** CBTE Tier-1 needs externally verifiable quotes; structured concept grading replaces holistic LLM scores

**Evidence:** documentation/design/implementation_plan.md; engineering reviews

**Result:** Baseline prompts for Wave1-Wave3

**Also touched:** `cera_extraction.txt`

**Snapshot:** `snapshots/PC-001_cera_extraction.txt`
