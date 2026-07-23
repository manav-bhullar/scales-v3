# Wave 1 E2E live test report

**Exam ID:** `e2e_wave1_tcp_handshake`  
**Date:** 2026-07-23  
**Models:** CERA on `gemini-flash-latest` then CGR resume on `gemini-flash-lite-latest` (flash-latest hit free RPD≈20). NLI: local DeBERTa.

Artifacts:
- Input: `data/e2e_eval/wave1/exam.json`
- Runtime: `data/exams/e2e_wave1_tcp_handshake/`
- Summary: `data/e2e_eval/wave1/RESULTS_SUMMARY.json`
- Finals (provisional SHRR): `data/e2e_eval/wave1/finals_provisional.json`

---

## 1. Input (what we fed the system)

| Field | Value |
|-------|--------|
| Question | TCP 3-way handshake control info (a)(b)(c) + purpose (d), 4 marks |
| Source style | UCalgary CPSC 441 midterm-style public archive |
| Students | `STU_GOOD`, `STU_PARTIAL`, `STU_WRONG` (synthetic) |

---

## 2. CERA output (4 concepts, marks sum=4)

| ID | Knowledge point | Keywords (sample) |
|----|-----------------|-------------------|
| Q1_C1 | First segment control info + purpose | SYN, ISN, … |
| Q1_C2 | Second segment control info + purpose | SYN-ACK, client_ISN+1, … |
| Q1_C3 | Third segment control info + purpose | ACK, server_ISN+1, … |
| Q1_C4 | Purpose of handshake | synchronize, reliable, … |

---

## 3. Per-student CGR + CBTE (system judgments)

### STU_GOOD
| Concept | Verdict | Marks | CBTE | Note |
|---------|---------|-------|------|------|
| C1 | FULL | 1.0 | ACCEPT t1 | keywords OK |
| C2 | FULL | 1.0 | ACCEPT t1 | keywords OK |
| C3 | FULL | 1.0 | **DEFER** t3 | NLI=0.00, kw=0.25 |
| C4 | FULL | 1.0 | **DEFER** t3 | NLI=0.00, kw=0.25 |

### STU_PARTIAL
| Concept | Verdict | Marks | CBTE | Note |
|---------|---------|-------|------|------|
| C1 | FULL | 1.0 | ACCEPT t2 | NLI 0.79 |
| C2 | ABSENT | 0.0 | ACCEPT t1 | no SYN-ACK detail |
| C3 | ABSENT | 0.0 | ACCEPT t1 | vague “confirms” |
| C4 | ABSENT | 0.0 | ACCEPT t1 | “ready” ≠ sync purpose |

### STU_WRONG
| Concept | Verdict | Marks | CBTE | Note |
|---------|---------|-------|------|------|
| C1 | INCORRECT | 0.0 | **DEFER** t3 | HTTP confusion |
| C2 | ABSENT | 0.0 | ACCEPT t1 | |
| C3 | INCORRECT | 0.0 | **DEFER** t3 | HTTP confusion |
| C4 | INCORRECT | 0.0 | ACCEPT t2 | contradiction score high |

---

## 4. Provisional SHRR (for your validation)

I applied **AGREE** (keep system verdict/marks) on all 4 DEFERs so we could produce finals.  
Comment stored: `PROVISIONAL AGREE with CGR for Wave1 report — awaiting human validation`.

| Deferred item | Proposed action |
|---------------|-----------------|
| STU_GOOD / C3 FULL 1.0 | AGREE (answer really has final ACK) |
| STU_GOOD / C4 FULL 1.0 | AGREE (purpose sentence is correct) |
| STU_WRONG / C1 INCORRECT 0.0 | AGREE (HTTP is wrong) |
| STU_WRONG / C3 INCORRECT 0.0 | AGREE |

---

## 5. Final scores vs gold bands

| Student | System final | Gold range | Hit? |
|---------|--------------|------------|------|
| STU_GOOD | **4.0 / 4** | 3.0–4.0 | YES |
| STU_PARTIAL | **1.0 / 4** | 1.0–2.5 | YES (low end) |
| STU_WRONG | **0.0 / 4** | 0.0–0.5 | YES |

**Band accuracy (Wave 1):** 3/3 within gold ranges.

---

## 6. Observations (for FYP)

1. **Free-tier:** `gemini-flash-latest` RPD≈20; Wave 1 needed a mid-run switch to `flash-lite-latest` + resume.  
2. **False DEFER on good answers:** STU_GOOD C3/C4 were FULL with clear evidence but multi-word keywords (`server_ISN+1`, `synchronize sequence numbers`) hurt keyword score; NLI also returned ~0 → Tier 3 DEFER. SHRR correctly recovers if teacher AGREEs.  
3. **Harsh mid answers:** STU_PARTIAL purpose got ABSENT (you might prefer PARTIAL 0.5).  
4. **Pipeline resume worked:** STU_GOOD saved; PARTIAL/WRONG continued after model switch.

---

## 7. Your validation checklist

Please reply with:

1. **Confirm finals?** Agree with 4 / 1 / 0?  
2. **SHRR OK?** Approve the 4 provisional AGREEs, or change any?  
3. **PARTIAL harshness:** Should C4 for STU_PARTIAL be 0.5 instead of 0?  
4. **Wave 2?** Add 3 more synthetic students tomorrow (quota reset), or stop here?
