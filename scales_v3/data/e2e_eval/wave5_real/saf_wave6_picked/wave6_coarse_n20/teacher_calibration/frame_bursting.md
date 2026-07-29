# Teacher calibration sheet — Q-BURST

This does not change grading. Please read each concept below and answer the
question in **bold**. Your answers will be used to correct concept weights
and/or facet definitions, not to add a new scoring rule engine.

## Question (3 marks)
What is "frame bursting"? Also, give 1 advantage and disadvantage compared to the carrier extension.

## Reference answer
Frame bursting reduces the overhead for transmitting small frames by concatenating a sequence of multiple frames in one single transmission, without ever releasing control of the channel.
Advantage :it is more efficient than carrier extension as single frames not filled up with garbage.
Disadvantage :need frames waiting for transmission or buffering and delay of frames

## Rubric as given
Total 3 marks:
1) Definition of frame bursting (1.5 marks)
2) Advantage and disadvantage vs carrier extension (1.5 marks)

---
## Concept `Q1_C1` — Definition of frame bursting (1.5 marks)
- Rubric item: `R1`
- CERA's target criteria: _any of: concatenating multiple frames / single transmission / not releasing channel control counts as the definition_
- CERA's evidence facets: ['concatenating a sequence of multiple frames', 'single transmission', 'without releasing control of the channel']
- Award rate across cohort: **85%** (FULL=17 PARTIAL=0 ABSENT/INCORRECT=3 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QBURST_17` (human gold=1.5/3)
  - answer: "Advantage: better efficiency
Disadvantage: needs frame waiting for transmission"
  - CGR reasoning: "The student did not provide a definition for frame bursting. The answer only addresses the advantage and disadvantage of the mechanism without explaining what it is."
- `QBURST_18` (human gold=1.5/3)
  - answer: "Frame bursting is a communication protocol feature for the principle of shared broadcast mode in gigabit ethernet. 
Advantage: frame bursting has a better efficiency than carrier extension. 
Disadvantage: needs frames wa"
  - CGR reasoning: "The student defines frame bursting as a 'communication protocol feature for the principle of shared broadcast mode in gigabit ethernet' but fails to describe the actual mechanism of the concept, such "
- `QBURST_19` (human gold=0.0/3)
  - answer: "Frame bursting is  a Transmission technique which is used to increase the Transmission rate of data Frames in the data link layer.
Advantage:the number of collision chances is reduced.
Disadvantage:Frame Bursting does no"
  - CGR reasoning: "The student defines frame bursting as a technique to increase transmission rate, but fails to mention the mechanism of concatenating frames, single transmission, or holding channel control."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C2` — Advantage of frame bursting over carrier extension (0.75 marks)
- Rubric item: `R2`
- CERA's target criteria: _any of: more efficient / not filled with garbage counts as the advantage_
- CERA's evidence facets: ['more efficient', 'not filled up with garbage']
- Award rate across cohort: **90%** (FULL=18 PARTIAL=0 ABSENT/INCORRECT=2 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QBURST_02` (human gold=3.0/3)
  - answer: "Advantage:
Allows the sender to transmit a series of frames in a single transmission in order to achieve a 
higher throughput.

Disadvantage:
Increases end-to-end-delay, as receiver has to wait for all the frames."
  - CGR reasoning: "The student describes the advantage of frame bursting as achieving higher throughput by sending multiple frames, but fails to mention the specific advantage over carrier extension, which is the avoida"
- `QBURST_19` (human gold=0.0/3)
  - answer: "Frame bursting is  a Transmission technique which is used to increase the Transmission rate of data Frames in the data link layer.
Advantage:the number of collision chances is reduced.
Disadvantage:Frame Bursting does no"
  - CGR reasoning: "The student identifies the advantage as 'the number of collision chances is reduced', which does not address the efficiency or the avoidance of garbage padding/carrier extension overhead as required b"

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C3` — Disadvantage of frame bursting over carrier extension (0.75 marks)
- Rubric item: `R2`
- CERA's target criteria: _any of: waiting for frames / buffering / delay counts as the disadvantage_
- CERA's evidence facets: ['waiting for frames', 'buffering', 'delay of frames']
- Award rate across cohort: **85%** (FULL=17 PARTIAL=0 ABSENT/INCORRECT=3 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QBURST_14` (human gold=2.25/3)
  - answer: "Frame bursting allows the sender to send a concatenated sequence of multiple frames in a single transmission. The efficiency is higher compared too carrier extension because the package length stays the same."
  - CGR reasoning: "The student failed to mention any disadvantage related to waiting for frames, buffering, or delay. The student only provided an advantage regarding efficiency."
- `QBURST_16` (human gold=2.25/3)
  - answer: "In frame bursting, the sender can transmit multiple frames by concatenating them in single transmission.
The carrier extension provides really low efficiency with only 46byte  user data being transmitted using 512 byte.
"
  - CGR reasoning: "The student failed to mention any disadvantage related to waiting, buffering, or delay. The student only discussed the performance advantage of frame bursting compared to carrier extension."
- `QBURST_19` (human gold=0.0/3)
  - answer: "Frame bursting is  a Transmission technique which is used to increase the Transmission rate of data Frames in the data link layer.
Advantage:the number of collision chances is reduced.
Disadvantage:Frame Bursting does no"
  - CGR reasoning: "The student identifies a disadvantage related to header overhead, which does not align with the required knowledge point regarding waiting, buffering, or delay."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____
