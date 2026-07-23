# Wave 2 E2E report (Groq)

**Provider:** Groq (`llama-3.3-70b-versatile` CERA, `llama-3.1-8b-instant` CGR)
**Exam:** `e2e_wave2_tcp_handshake_groq` · graded `STU_GOOD, STU_PARTIAL, STU_WRONG, STU_GOOD_ALT, STU_PURPOSE_FOCUS, STU_MID_DETAIL`

## Focus checks (from Wave 1)
1. False DEFER on good FULL answers (esp. C3/C4)
2. Harsh ABSENT on mid/purpose answers

## CERA concepts
- `Q1_C1` (1): SYN flag and client's initial sequence number in first TCP segment
  - keywords: ['SYN', 'initial sequence number']
- `Q1_C2` (1): SYN-ACK flags, server's ISN, and acknowledgement number in second TCP segment
  - keywords: ['SYN-ACK', 'server ISN', 'acknowledgement number']
- `Q1_C3` (1): ACK flag with acknowledgement number in third TCP segment
  - keywords: ['ACK', 'acknowledgement number']
- `Q1_C4` (1): Purpose of three-way handshake in TCP
  - keywords: ['purpose', 'three-way handshake']

## Per-student concept table

### STU_GOOD — provisional final **4.0/4**
| Concept | Verdict | Marks | CBTE | Trust | Tier |
|---------|---------|-------|------|-------|------|
| Q1_C1 | FULL | 1.0 | ACCEPT | 0.85 | 1 |
| Q1_C2 | FULL | 1.0 | ACCEPT | 0.85 | 1 |
| Q1_C3 | FULL | 1.0 | DEFER | 0.00 | 1 |
| Q1_C4 | FULL | 1.0 | ACCEPT | 0.85 | 1 |

### STU_GOOD_ALT — provisional final **4.0/4**
| Concept | Verdict | Marks | CBTE | Trust | Tier |
|---------|---------|-------|------|-------|------|
| Q1_C1 | FULL | 1.0 | ACCEPT | 0.85 | 1 |
| Q1_C2 | FULL | 1.0 | ACCEPT | 0.85 | 1 |
| Q1_C3 | FULL | 1.0 | ACCEPT | 0.85 | 1 |
| Q1_C4 | FULL | 1.0 | DEFER | 0.00 | 1 |

### STU_PARTIAL — provisional final **1.0/4**
| Concept | Verdict | Marks | CBTE | Trust | Tier |
|---------|---------|-------|------|-------|------|
| Q1_C1 | FULL | 1.0 | ACCEPT | 0.85 | 1 |
| Q1_C2 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C3 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C4 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |

### STU_PURPOSE_FOCUS — provisional final **1.0/4**
| Concept | Verdict | Marks | CBTE | Trust | Tier |
|---------|---------|-------|------|-------|------|
| Q1_C1 | ABSENT | 0.0 | DEFER | 0.45 | 3 |
| Q1_C2 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C3 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C4 | FULL | 1.0 | ACCEPT | 0.85 | 1 |

### STU_MID_DETAIL — provisional final **1.0/4**
| Concept | Verdict | Marks | CBTE | Trust | Tier |
|---------|---------|-------|------|-------|------|
| Q1_C1 | ABSENT | 0.0 | DEFER | 0.45 | 3 |
| Q1_C2 | ABSENT | 0.0 | DEFER | 0.40 | 3 |
| Q1_C3 | ABSENT | 0.0 | DEFER | 0.45 | 3 |
| Q1_C4 | FULL | 1.0 | DEFER | 0.30 | 3 |

### STU_WRONG — provisional final **0.0/4**
| Concept | Verdict | Marks | CBTE | Trust | Tier |
|---------|---------|-------|------|-------|------|
| Q1_C1 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C2 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C3 | ABSENT | 0.0 | ACCEPT | 0.90 | 1 |
| Q1_C4 | ABSENT | 0.0 | DEFER | 0.45 | 3 |

## Issue 1 — False DEFER on good answers (C3/C4)

| Student | Concept | Verdict | CBTE | NLI | KW |
|---------|---------|---------|------|-----|----|
| STU_GOOD | Q1_C3 | FULL | DEFER | None | 0.5 |
| STU_GOOD | Q1_C4 | FULL | ACCEPT | None | 0.5 |
| STU_GOOD_ALT | Q1_C3 | FULL | ACCEPT | None | 0.5 |
| STU_GOOD_ALT | Q1_C4 | FULL | DEFER | None | 0.0 |

**False DEFER count (FULL + DEFER on C3/C4 for good students):** 2 / 4

Still reproducing Wave 1 issue — keyword/NLI path weak on multi-word claims.

## Issue 2 — Harsh purpose scoring (C4)

| Student | Verdict | Marks | CBTE | Reasoning snippet |
|---------|---------|-------|------|-------------------|
| STU_PARTIAL | ABSENT | 0.0 | ACCEPT | The student answer does not mention the three-way handshake or its purpose, so it does not demonstrate the knowledge point. |
| STU_PURPOSE_FOCUS | FULL | 1.0 | ACCEPT | The student correctly identifies the purpose of the three-way handshake as synchronizing sequence numbers and establishing a reliable connection. This matches the expected evidence |
| STU_MID_DETAIL | FULL | 1.0 | DEFER | The student correctly identifies the purpose of the three-way handshake as making both ends ready and synchronizing them for reliable data transfer. This matches the expected evide |

- `STU_PARTIAL` purpose still **ABSENT/0** (Wave 1 harshness **reproduced**).
- `STU_PURPOSE_FOCUS` purpose correctly scored **FULL 1.0** (explicit purpose sentence recognized).

## Finals vs gold bands (provisional SHRR=AGREE)

| Student | Final | Gold range | Hit? |
|---------|-------|------------|------|
| STU_GOOD | 4.0/4 | 3.0–4.0 | YES |
| STU_PARTIAL | 1.0/4 | 1.0–2.5 | YES |
| STU_WRONG | 0.0/4 | 0.0–0.5 | YES |
| STU_GOOD_ALT | 4.0/4 | 3.0–4.0 | YES |
| STU_PURPOSE_FOCUS | 1.0/4 | 1.0–2.5 | YES |
| STU_MID_DETAIL | 1.0/4 | 1.5–3.0 | NO |

**Band hits:** 5/6

## Security note
Groq API key was pasted in chat earlier — rotate it at https://console.groq.com/keys
