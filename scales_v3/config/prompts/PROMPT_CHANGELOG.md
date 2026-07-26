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


### TC-015 — 2026-07-26 — `scales/modules/calibration.py` — `cera.fake_partial_and_calibrate` (tighten)

**Kind:** code  
**Direction:** tighten

**Screw:** `cera.fake_partial_and_calibrate`

**What:** Reject fake partial_credit_rule strings (null/No partial…) when required; warn-only pre-grade calibration in pipeline (skip on resume; --calibrate-strict opt-in)

**Why:** CERA wrote string null as partial; silent hole. Calibration catches over-strict leaves before full batch.

**If reverted:** Fake partials pass validation again; no pre-batch smoke warnings

**Tradeoff:** Default calibrate adds ~2*N_concepts LLM calls on fresh grade; use --no-calibrate to skip

**Evidence:** Q-BURST v2 cqa had partial_credit_rule string null on C2/C3

**Snapshot:** `snapshots/TC-015_calibration.py`

**File hash (16):** `0c7e797c23d61547`


### TC-014 — 2026-07-26 — `scales/models/cqa.py` — `cera.evidence_facets_mode` (restructure)

**Kind:** code  
**Direction:** restructure

**Screw:** `cera.evidence_facets_mode`

**What:** Add evidence_facets + evidence_mode (ANY/ALL); validators for ALL-requires-partial, ANY AND-lint, keyword facet coverage, MAY-SPLIT child partial; CGR mechanical ANY/ALL; calibrate_cqas.py

**Why:** Nested Q-BURST under-scored because CERA wrote AND-chains and mechanism requirements with null partial on split leaves

**If reverted:** Advantage/disadvantage leaves become over-strict again; silent wrong zeros return

**Tradeoff:** Stricter CERA validation may need more retries; teacher ALL must write partial rule

**Evidence:** Q-BURST nested MAE 0.60 vs flat 0.15; BURST_00 delay ABSENT

**Snapshot:** `snapshots/TC-014_cqa.py`

**File hash (16):** `5deb7fbb5deadfb5`


### TC-013 — 2026-07-26 — `scales/models/rubric.py` — `cera.rubric_item_nesting` (restructure)

**Kind:** code  
**Direction:** restructure

**Screw:** `cera.rubric_item_nesting`

**What:** Optional RubricItem buckets above CQAs; hybrid 1:1 atomic or 1:N may-split; additive child sums; CERA prompt + validators

**Why:** Teacher rubrics are often coarse; short answers stay 1 rubric=1 concept; middle answers need controlled splits without a rule engine

**If reverted:** Lose bucket blast-radius control; CERA free to invent global splits again

**Tradeoff:** More validation surface; teacher must set atomic flags; UI for buckets deferred

**Evidence:** RATAS additive RKT; Wave6 Q-BURST 1.5+1.5; STRICTNESS_RESEARCH.md

**Snapshot:** `snapshots/TC-013_rubric.py`

**File hash (16):** `37d288cb34e9d817`


### TC-012 — 2026-07-26 — `scales/models/cqa.py` — `grading.concept_mark_quarters` (restructure)

**Kind:** code  
**Direction:** restructure

**Screw:** `grading.concept_mark_quarters`

**What:** Allow CQA concept marks as float multiples of 0.25 (e.g. 1.5); awards stay 0/half/full of the concept. Float-safe CERA mark-sum check; format_marks keeps whole numbers as '1' not '1.0' in CGR prompts; CERA prompt tells the LLM not to round half marks to int.

**Why:** Real teacher rubrics use 0.25/0.5/1.5 concept weights (SAF pack wrote 1.5+1.5 but CERA was forced to 1+2+1+1 by int schema).

**If reverted:** Concept weights snap back to integers; half-mark rubric clauses are silently rounded and CERA drifts from teacher rubrics again.

**Tradeoff:** PARTIAL of a 1.25-mark concept is 0.625; results/ledger may show finer decimals. LLM could still propose weird splits until validation rejects them.

**Evidence:** Wave5 SAF CERA drift 1+2+1+1 vs rubric 1+1.5+1.5+1; architecture review 2026-07-26

**Result:** Unit suite green; concept marks float+quarter validated; CGR/SHRR accept 0/0.75/1.5 for 1.5-mark concepts

**Also touched:** `cera_extraction.txt`

**Snapshot:** `snapshots/TC-012_cqa.py`

**File hash (16):** `a7bfdce7934f0f05`


### TC-011 — 2026-07-25 — `api/main.py` — `ui.accept_audit_surface` (restructure)

**Kind:** code  
**Direction:** restructure

**Screw:** `ui.accept_audit_surface`

**What:** New GET /api/exams/{id}/breakdown plus ExplainPage UI: per-student, per-concept 'why these marks' view (verdict, marks, reasoning, quoted evidence, keyword found/missing split, CBTE signals, teacher override). Adds a cohort 'rubric health' strip and a 'Zeros never checked' filter that lists ACCEPTed zero-mark judgments.

**Why:** Wave5 Mohler underscored 20/28 students and SHRR could not fix any of it: 72 of 79 zero-mark judgments were auto-ACCEPTed at Tier 1, so they never entered the DEFER queue. The review UI only ever showed DEFERs, making accepted zeros structurally invisible. There was also no way to tell an unearnable rubric concept (C4: 1/28 earned) from a genuinely missed one.

**If reverted:** Teachers can only see DEFERs again. Accepted zeros stay invisible, dead rubric concepts stay undetectable without a hand-written script, and every underscoring diagnosis needs a developer reading grading_results.json.

**Tradeoff:** Read-only surface: audit findings still cannot be corrected because SHRR only accepts corrections for items in the DEFER queue. Reviewing accepted zeros also costs teacher time the trust layer was meant to save, so it competes with the point of CBTE.

**Evidence:** data/e2e_eval/wave5_real/mohler_bst_delete/WAVE5_REAL1_REPORT.md; scripts/diagnose_wave5_underscore.py; tests/unit/test_api_breakdown.py

**Result:** Live on e2e_wave5_mohler_bst_delete: 28 students x 4 concepts served, 72 unchecked zeros surfaced, C1 (6/28 earned) and C4 (1/28) flagged as suspect concepts. Diagnostic: dropping C1+C4 moves MAE 2.14 -> 1.77 and in-band 8/28 -> 12/28, so rubric design is the largest cause and grader leniency the residual. 124 backend tests + frontend build pass.

**Snapshot:** `snapshots/TC-011_main.py`

**File hash (16):** `9aa2f82b8cf477fc`


### TC-010 — 2026-07-25 — `data/e2e_eval/wave5_real/mohler_bst_delete/exam.json` — `dataset.real_data_wave5` (measure)

**Kind:** dataset  
**Direction:** measure

**Screw:** `dataset.real_data_wave5`

**What:** Added first REAL-answer pack: Mohler ASAG E12.Q09 (BST node deletion), 28 UNT student answers, gold bands derived from two human graders (0-10 normalized to 0-5); 5-mark rubric authored by us

**Why:** All prior packs are synthetic LLM-authored; real data breaks circularity and tests DEFER behaviour on messy authentic text

**If reverted:** Evaluation evidence stays purely synthetic; FYP claim 'works on real answers' unsupported

**Tradeoff:** Rubric is ours, not UNT's (holistic 0-10) - calibration tension expected; band mix top-heavy (15 high/1 low) so false-ACCEPT signal weaker on this pack

**Evidence:** huggingface.co/datasets/nkazi/MohlerASAG; ACL P11-1076; data/e2e_eval/wave5_real/mohler_bst_delete/

**Result:** Pack built + contract tests pass (9); awaiting human approval before live grade

**File hash (16):** `12d766bb2114e8f9`


### TC-009 — 2026-07-25 — `config/settings.yaml` — `grading.mark_granularity` (restructure)

**Kind:** metric  
**Direction:** restructure

**Screw:** `grading.mark_granularity`

**What:** CANDIDATE (not yet applied): add 0.25 and 0.75 to allowed_marks_fractions so verdicts can express quarter-credit

**Why:** Teacher SHRR on CN2 PARTIAL_B/C1 and OS1: repeatedly wanted a mark between ABSENT(0) and PARTIAL(0.5), and between PARTIAL and FULL; 0/0.5/1.0 forces rounding that loses signal

**If reverted:** Stays at 0/0.5/1.0; teacher keeps rounding borderline answers, adding noise to band-hit/MAE

**Tradeoff:** Touches rubric text, CGR prompt few-shot, aggregator, and every existing gold expected_score_range; risks destabilizing frozen wave3 regression — must re-baseline

**Evidence:** teacher_corrections.json CN2 PARTIAL_B/C1 comment; user review 2026-07-25

**Result:** Deferred to before Phase D scale-up; logged only

**File hash (16):** `585941f9a31b4465`


### TC-008 — 2026-07-25 — `data/e2e_eval/wave4/cn2_gbn_vs_sr/gold_labels.json` — `dataset.cn2.human_gold` (tighten)

**Kind:** dataset  
**Direction:** tighten

**Screw:** `dataset.cn2.human_gold`

**What:** Human CN2 review: clarified GOOD_01 sender wording; demoted GOOD_02 gold to mid 2.5-3.5; documented LOW_01 as intentional congestion-control confusion; DB1 stem rewritten to one-line exam style; contract test allows human band demotions

**Why:** User found 'later packet' ambiguous; compressed GOOD_02 too weak for full marks; (a)-(d) stems are artificial vs real exams

**If reverted:** GOOD_02 wrongly treated as high-band full credit; ambiguous GBN wording returns; DB1 looks like a 4-part worksheet again

**Tradeoff:** CN2 now has only 1 high-band answer; band-hit math is slightly less balanced on n=8

**Evidence:** User review 2026-07-25; VALIDATION.md cn2 + db1; wave4 README authoring rule

**Result:** Gold + stem updates applied; awaiting approve Q-CN2 for live grade

**File hash (16):** `567543b659d606e5`


### TC-007 — 2026-07-25 — `scales/services/text_utils.py` — `cbte.keyword_variant_matching` (loosen)

**Kind:** code  
**Direction:** loosen

**Screw:** `cbte.keyword_variant_matching`

**What:** acceptable_variants now match by token containment (>=0.75 of variant content tokens in answer) as fallback to exact normalized substring; stopword-only variants never hit

**Why:** OS1 v6 false DEFER: MID_01/Q1_C1 FULL + verified evidence deferred at Tier 3 (kw=0.00) because variant 'threads run inside a process' missed paraphrase 'threads are smaller units inside it'; teacher SHRR confirmed FULL/1.0 (AGREE)

**If reverted:** False DEFER on paraphrased-but-correct answers returns (OS1 defer 10%->12.5%, wave3 27->28); Tier-2 NLI runs on items Tier 1 could clear

**Tradeoff:** Variant hit alone can push kw over tier1_keyword_threshold (1/len(expected)) and fast-accept a wrong FULL if CGR errs AND variant fuzzily matches; watch false ACCEPT on next live runs

**Evidence:** wave4 OS1 cbte_reeval_tc007.json (DEFER 5->4, only MID_01/Q1_C1 flips), wave3 cbte_reeval_tc007.json (28->27, flip agrees with teacher record W3_GOOD_04/Q1_C3)

**Result:** Offline replay: OS1 false DEFER 1->0, false ACCEPT unchanged 0; wave3 no decision moves against teacher corrections; 116 unit tests pass (3 new pins)

**Snapshot:** `snapshots/TC-007_text_utils.py`

**File hash (16):** `eaaf2de91733adfd`


### TC-006 — 2026-07-25 — `scripts/metrics_ledger.py` — `metrics.silent_zero` (restructure)

**Kind:** metric  
**Direction:** restructure

**Screw:** `metrics.silent_zero`

**What:** Changed silent-zero from a hard gate to a review candidate unless concept-level human gold confirms the zero was unexpected

**Why:** After adding a scored definition concept, GOOD_01 correctly received ABSENT there, but the band-only heuristic falsely called it a silent-zero failure

**If reverted:** Legitimate omitted concepts on otherwise high-band students can falsely fail the pass bar

**Tradeoff:** Silent-zero safety is advisory until concept-level gold is authored; total-score high-band gate still catches under-scoring

**Evidence:** wave4 OS1 5-mark v6; GOOD_01 expected definition=ABSENT

**Result:** Pass bar reports silent-zero as N/A/candidate without concept gold

**Snapshot:** `snapshots/TC-006_metrics_ledger.py`

**File hash (16):** `6787401117ee6146`


### TC-005 — 2026-07-25 — `scales/modules/cgr.py` — `cgr.target_criteria_wiring` (restructure)

**Kind:** code  
**Direction:** restructure

**Screw:** `cgr.target_criteria_wiring`

**What:** Pass CQA target_criteria into every CGR prompt as the authoritative scoring contract

**Why:** CERA preserved the OS1 strict definition rule in target_criteria, but CGR never rendered that field, so the grader could not see teacher FULL/PARTIAL/ABSENT exclusions

**If reverted:** CGR grades from a lossy knowledge-point summary and can violate teacher-authored scoring criteria

**Tradeoff:** Longer prompts and stricter rubric adherence may change Wave3 verdicts; run regression after verification

**Evidence:** cgr.py _build_prompt omitted cqa.target_criteria; OS1 v5 Q1_C1

**Result:** Pending OS1 v6 and Wave3 regression

**Also touched:** `cgr_grading.txt`

**Snapshot:** `snapshots/TC-005_cgr.py`

**File hash (16):** `fe068c5de987050b`


### TC-004 — 2026-07-25 — `data/e2e_eval/wave4/os1_process_vs_thread/exam.json` — `dataset.os1.definition_required` (tighten)

**Kind:** dataset  
**Direction:** tighten

**Screw:** `dataset.os1.definition_required`

**What:** Clarified definition mark: FULL requires both explicit definitions; PARTIAL requires one explicit definition; resource-sharing implication alone earns ABSENT

**Why:** In the first 5-mark rerun, CGR gave GOOD_02 FULL and GOOD_01/PARTIAL_A PARTIAL by inferring definitions from address-space sharing, contrary to human marking

**If reverted:** CGR may again infer the missing definitions from parts (a)-(d), allowing incomplete answers to recover definition credit

**Tradeoff:** Strict wording may mark concise but valid implicit distinctions as ABSENT; monitor independently written real answers

**Evidence:** wave4_os1_gemini_5mark_v2; Q1_C1 judgments for GOOD_01, GOOD_02, PARTIAL_A

**Result:** Pending strict 5-mark v3 rerun

**Snapshot:** `snapshots/TC-004_exam.json`

**File hash (16):** `11ec83783e27989b`


### TC-003 — 2026-07-25 — `data/e2e_eval/wave4/os1_process_vs_thread/exam.json` — `dataset.os1.definition_required` (tighten)

**Kind:** dataset  
**Direction:** tighten

**Screw:** `dataset.os1.definition_required`

**What:** Changed OS1 from 4 to 5 marks by adding an explicit process/thread definition-distinction concept; preserved student answers and revised human gold ranges

**Why:** Human gold review found GOOD_01 and GOOD_02 covered applied parts but omitted the core definition requested by the stem; the old rubric could still award 4/4

**If reverted:** The stem/reference will again require a definition that the rubric and CERA do not score, allowing incomplete answers to receive full marks

**Tradeoff:** Old 4-mark OS1 ledger/report is no longer directly comparable; CERA and grading must be rerun from scratch

**Evidence:** Human review 2026-07-25; OS1_GOOD_01 and OS1_GOOD_02; VALIDATION.md

**Result:** Pending fresh CERA+Gemini grade on the 5-mark rubric

**Snapshot:** `snapshots/TC-003_exam.json`

**File hash (16):** `78701185b170f496`


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


### PC-005 — 2026-07-25 — `cera_extraction.txt` — `cera.rubric_constraint_fidelity` (tighten)

**Kind:** prompt  
**Direction:** tighten

**Screw:** `cera.rubric_constraint_fidelity`

**What:** Require CERA to preserve 0.5 rules on 1-mark concepts and carry explicit FULL/PARTIAL/ABSENT exclusions literally

**Why:** OS1 strict definition exclusion was lost during CERA decomposition, so downstream CGR still inferred partial credit from resource-sharing text

**If reverted:** CERA can simplify away teacher rubric exclusions, making CGR grade a different rubric from the one the teacher approved

**Tradeoff:** Longer and stricter CQA rules may reduce generalization; inspect CQA tuples after each new question

**Evidence:** wave4 OS1 v4 Q1_C1 partial_credit_rule omitted resource-sharing-only=ABSENT

**Result:** Pending OS1 v5 verification

**Snapshot:** `snapshots/PC-005_cera_extraction.txt`

**File hash (16):** `b7a350be5def68c2`


### PC-004 — 2026-07-25 — `cgr_grading.txt` — `cgr.partial_rule_precedence` (tighten)

**Kind:** prompt  
**Direction:** tighten

**Screw:** `cgr.partial_rule_precedence`

**What:** Made concept-specific partial-credit rules override the general PARTIAL preference; forbid inferring a concept from related subparts

**Why:** Strict OS1 definition rule still received inferred PARTIAL credit from address-space answers, causing GOOD_02 to exceed human gold

**If reverted:** Generic prefer-PARTIAL wording can override explicit rubric exclusions and award inferred credit for omitted concepts

**Tradeoff:** Could increase ABSENT on terse answers whose concept is only implicit; must recheck Wave3 paraphrase performance and false DEFER

**Evidence:** wave4_os1_gemini_5mark_strict_v3 Q1_C1: GOOD_01, GOOD_02, PARTIAL_A

**Result:** Pending OS1 v4 and Wave3 regression

**Snapshot:** `snapshots/PC-004_cgr_grading.txt`

**File hash (16):** `96b0dd40c8839552`


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
