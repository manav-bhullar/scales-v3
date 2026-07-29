# Teacher calibration sheet — Q-DLL3

This does not change grading. Please read each concept below and answer the
question in **bold**. Your answers will be used to correct concept weights
and/or facet definitions, not to add a new scoring rule engine.

## Question (3 marks)
Name the 3 service classes the Data Link Layer offers and explain the differences between the classes.

## Reference answer
1.unconfirmed connectionless - no ACK, loss of data possible, no flow control, no connect or disconnect.
2.confirmed connectionless - with ACK, no loss of data (timeout and retransmit instead→ duplicates and sequence errors possible), no flow control, no connect or disconnect.
3.connection-oriented - no data loss, duplication or sequencing errors. Instead a 3 phased communication with connect and disconnect, and flow control

## Rubric as given
Total 3 marks:
1) Unconfirmed connectionless (1 mark)
2) Confirmed connectionless (1 mark)
3) Connection-oriented (1 mark)

---
## Concept `Q1_C1` — Unconfirmed connectionless service class (1.0 marks)
- Rubric item: `R1`
- CERA's target criteria: _any of: no ACK / no flow control / no connection setup counts as the definition_
- CERA's evidence facets: ['no ACK', 'no flow control', 'no connection setup']
- Award rate across cohort: **90%** (FULL=17 PARTIAL=2 ABSENT/INCORRECT=1 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QDLL3_19` (human gold=0.0/3)
  - answer: "1. Flow Control: ensures that a transmitter does not send faster than a receiver can receive
2. Framing: data are packed in a frame, this frame contains e.g. the data, destination address and source 
3. Error Detection: "
  - CGR reasoning: "The student lists three functions of the Data Link Layer (Flow Control, Framing, Error Detection) but does not mention or define the unconfirmed connectionless service class."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C2` — Confirmed connectionless service class (1.0 marks)
- Rubric item: `R2`
- CERA's target criteria: _any of: with ACK / no loss of data / duplicates possible / sequence errors possible counts as the definition_
- CERA's evidence facets: ['with ACK', 'no loss of data', 'duplicates possible', 'sequence errors possible']
- Award rate across cohort: **92%** (FULL=18 PARTIAL=1 ABSENT/INCORRECT=1 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QDLL3_19` (human gold=0.0/3)
  - answer: "1. Flow Control: ensures that a transmitter does not send faster than a receiver can receive
2. Framing: data are packed in a frame, this frame contains e.g. the data, destination address and source 
3. Error Detection: "
  - CGR reasoning: "The student lists functions of the Data Link Layer (Flow Control, Framing, Error Detection) but does not mention the service classes (unacknowledged connectionless, acknowledged connectionless, or con"

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C3` — Connection-oriented service class (1.0 marks)
- Rubric item: `R3`
- CERA's target criteria: _any of: 3 phased communication / flow control / no data loss / connect and disconnect counts as the definition_
- CERA's evidence facets: ['3 phased communication', 'flow control', 'no data loss', 'connect and disconnect']
- Award rate across cohort: **90%** (FULL=16 PARTIAL=4 ABSENT/INCORRECT=0 / n=20)

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____
