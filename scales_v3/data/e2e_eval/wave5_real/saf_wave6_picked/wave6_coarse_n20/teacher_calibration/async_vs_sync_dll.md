# Teacher calibration sheet — Q-ASYNC

This does not change grading. Please read each concept below and answer the
question in **bold**. Your answers will be used to correct concept weights
and/or facet definitions, not to add a new scoring rule engine.

## Question (4 marks)
What is the difference between asynchronous and synchronous transmission mode in the Data Link Layer.

## Reference answer
Asynchronous transmission: Every character a self-contained unit surrounded by a start bit and a stop bit, which is an easy and cheap pattern, but causes low transmission rates.

Synchronous transmission: Several characters pooled to a continuous stream of data (frames), Frames defined by SYN or flag, higher complexity, but higher transmission rates. Requires synchronization between sender and receiver.

## Rubric as given
Total 4 marks:
1) Asynchronous framing (start/stop) (1 mark)
2) Asynchronous trade-off (simple/cheap vs low rate) (1 mark)
3) Synchronous framing (frames / SYN / flag) (1 mark)
4) Synchronous trade-off (rate / sync / complexity) (1 mark)

---
## Concept `Q1_C1` — Asynchronous transmission framing (1.0 marks)
- Rubric item: `R1`
- CERA's target criteria: _any of: start bit / stop bit counts as the framing mechanism_
- CERA's evidence facets: ['start bit', 'stop bit']
- Award rate across cohort: **88%** (FULL=17 PARTIAL=1 ABSENT/INCORRECT=2 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QASYNC_17` (human gold=3.0/4)
  - answer: "In Synchronous Transmission, data is sent in form of blocks or frames，this transmission is full-duplex mode And the data flow is constant.But in Asynchronous Transmission,data is sent in form of bit or characters,this tr"
  - CGR reasoning: "The student describes asynchronous transmission as sending data in the form of bits or characters and mentions that the data flow is random, but they do not mention start bits or stop bits, which are "
- `QASYNC_19` (human gold=2.0/4)
  - answer: "In synchronous transmission for multiple bytes to be transmitted there is only one frame consisting of a start marker, all the bytes and a stop marker. Asynchronous transmission though uses one frame per byte so no marke"
  - CGR reasoning: "The student explicitly states that 'no markers are needed' for asynchronous transmission, which directly contradicts the knowledge point that asynchronous transmission relies on start and stop bits fo"

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C2` — Asynchronous transmission trade-off (1.0 marks)
- Rubric item: `R2`
- CERA's target criteria: _any of: easy pattern / cheap pattern / low transmission rates counts as the trade-off_
- CERA's evidence facets: ['easy pattern', 'cheap pattern', 'low transmission rates']
- Award rate across cohort: **35%** (FULL=6 PARTIAL=2 ABSENT/INCORRECT=12 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QASYNC_02` (human gold=4.0/4)
  - answer: "Asynchronous Transmission: Each character is bounded by a start bit and a stop bit.
Synchronous Transmission: Several characters pooled to a Frames."
  - CGR reasoning: "The student describes the framing mechanism of asynchronous transmission (start and stop bits) but does not mention the trade-offs associated with it, such as its simplicity, cost-effectiveness, or lo"
- `QASYNC_03` (human gold=4.0/4)
  - answer: "Asynchronous mode:
Each character is bounded by a start bit and a stop bit.

Synchronous mode:
Several characters are pooled to one frame which is defined by a SYN or a flag."
  - CGR reasoning: "The student describes the framing mechanism of asynchronous transmission (start and stop bits) but does not mention the trade-offs such as simplicity, cost, or transmission rate."
- `QASYNC_04` (human gold=4.0/4)
  - answer: "Asynchronous transmission sends single bytes which are bounded by a start bit and an end bit.

In comparison synchronous transmission is able to send a block of bytes (Frame). These blocks are defined by SYN or flag."
  - CGR reasoning: "The student describes the mechanism of asynchronous transmission (start/stop bits) but does not mention the trade-offs such as simplicity, cost, or transmission rate limitations."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C3` — Synchronous transmission framing (1.0 marks)
- Rubric item: `R3`
- CERA's target criteria: _any of: frames / SYN / flag counts as the framing mechanism_
- CERA's evidence facets: ['frames', 'SYN', 'flag']
- Award rate across cohort: **98%** (FULL=19 PARTIAL=1 ABSENT/INCORRECT=0 / n=20)

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C4` — Synchronous transmission trade-off (1.0 marks)
- Rubric item: `R4`
- CERA's target criteria: _any of: higher complexity / higher transmission rates / requires synchronization counts as the trade-off_
- CERA's evidence facets: ['higher complexity', 'higher transmission rates', 'requires synchronization']
- Award rate across cohort: **40%** (FULL=6 PARTIAL=4 ABSENT/INCORRECT=10 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QASYNC_02` (human gold=4.0/4)
  - answer: "Asynchronous Transmission: Each character is bounded by a start bit and a stop bit.
Synchronous Transmission: Several characters pooled to a Frames."
  - CGR reasoning: "The student describes the structural difference between asynchronous and synchronous transmission (start/stop bits vs. frames) but does not mention the trade-offs of complexity, transmission rates, or"
- `QASYNC_03` (human gold=4.0/4)
  - answer: "Asynchronous mode:
Each character is bounded by a start bit and a stop bit.

Synchronous mode:
Several characters are pooled to one frame which is defined by a SYN or a flag."
  - CGR reasoning: "The student describes the framing mechanism of synchronous transmission (using SYN or flags) but does not mention the trade-offs associated with it, such as higher complexity, higher transmission rate"
- `QASYNC_04` (human gold=4.0/4)
  - answer: "Asynchronous transmission sends single bytes which are bounded by a start bit and an end bit.

In comparison synchronous transmission is able to send a block of bytes (Frame). These blocks are defined by SYN or flag."
  - CGR reasoning: "The student describes the structural difference between asynchronous and synchronous transmission (sending bytes vs. blocks/frames) but does not mention the trade-offs of complexity, transmission rate"

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____
