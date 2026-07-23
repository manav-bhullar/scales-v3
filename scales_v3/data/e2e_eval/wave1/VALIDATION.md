# E2E evaluation — Wave 1 (awaiting your validation)

## Goal
Test Sprint 5 end-to-end on a **realistic short-answer exam item** with synthetic student answers, before Sprint 6.

## Source (public exam style)
- Inspired by: University of Calgary **CPSC 441** midterm TCP handshake short-answer  
- Archive: https://cspages.ucalgary.ca/~cwill/CPSC441/archive/2012/midterm2008.pdf  
- We adapted parts (a)–(c) + purpose into one 4-mark question with an explicit rubric.

## Wave plan (Gemini free-tier safe)
| Wave | Questions | Students | Approx Gemini calls | When |
|------|-----------|----------|---------------------|------|
| **1 (this)** | 1 | 3 | ~13 | After you approve materials |
| 2 | 1 | 6 | ~25 | After Wave 1 looks sane |
| 3 | 2 | 4 each | ~40+ | Only if quota remains |

Concurrency lowered to **3** in `config/settings.yaml` for free-tier RPM.

## What I need you to validate **before** any live Gemini run

### 1) Question + rubric (see `exam.json`)
- Is the question wording fair for a short-answer exam?
- Are the 4 mark points clear and non-overlapping?
- Any change to reference answer / rubric?

### 2) Synthetic student answers
| ID | Intent | Your check |
|----|--------|------------|
| `STU_GOOD` | Strong full answer | Would you give ~3–4/4? |
| `STU_PARTIAL` | Vague mid answer | Would you give ~1–2.5/4? |
| `STU_WRONG` | HTTP confusion | Would you give ~0? |

### 3) Gold ranges (`gold_labels.json`)
Confirm the expected score bands above (or tell me your marks).

## After you approve
I will:
1. Run `run_pipeline.py grade` on Wave 1  
2. Show **CERA concepts**, **per-concept verdicts**, **CBTE ACCEPT/DEFER**, **final scores**  
3. Compare to gold bands  
4. Ask you to validate any DEFER items (SHRR) if they appear  
5. Only then expand to Wave 2

## How to reply
Reply with something like:
- `APPROVE wave1` — run as-is  
- or list edits (question / rubric / rewrite a student answer / change gold bands)
