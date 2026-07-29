# Teacher calibration sheet — Q-CONN

This does not change grading. Please read each concept below and answer the
question in **bold**. Your answers will be used to correct concept weights
and/or facet definitions, not to add a new scoring rule engine.

## Question (5 marks)
Consider the following scenario: You are browsing the web for a very specific and important piece of information. However, you are not quite sure how to find it and adopt an iterative process of refining your query after every search, depending on the shown results and a skim of the first few websites. Is it better to use a connection-oriented or connectionless service for your communication in this scenario? Explain your answer in 1-4 sentences.

## Reference answer
Connectionless, because you will communicate with various partners (websites) for short periods of time. If you would initiate a connection with every website you skim, that would incur a lot of overhead in the connecting and disconnecting phase, just to have very short data transfers.

## Rubric as given
Total 5 marks:
1) Chooses connectionless (1 mark)
2) Many / changing partners (websites) (1.5 marks)
3) Short / brief interactions per site (1 mark)
4) Connection-oriented setup/teardown overhead argument (1.5 marks)

---
## Concept `Q1_C1` — Selection of connectionless service (1.0 marks)
- Rubric item: `R1`
- CERA's target criteria: _Student correctly identifies connectionless service as the appropriate choice._
- CERA's evidence facets: ['Connectionless']
- Award rate across cohort: **30%** (FULL=6 PARTIAL=0 ABSENT/INCORRECT=14 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QCONN_02` (human gold=5.0/5)
  - answer: "It is better to use a connection oriented service since you will be communicating especially with one search engine multiple times, and a loss of the query data is not acceptable."
  - CGR reasoning: "The student explicitly identifies a connection-oriented service as the better choice, which directly contradicts the required knowledge point of selecting a connectionless service."
- `QCONN_06` (human gold=2.5/5)
  - answer: "Connection-oriented service is better due to the importance of the information so in this waz will be losed."
  - CGR reasoning: "The student explicitly chooses connection-oriented service, which contradicts the requirement to identify connectionless service as the appropriate choice for the described scenario."
- `QCONN_07` (human gold=2.5/5)
  - answer: "Connection-oriented service is better, cause it has to use this, for an iterative process with very specific and important information."
  - CGR reasoning: "The student explicitly identifies 'Connection-oriented service' as the better choice, which directly contradicts the required knowledge point of selecting a connectionless service."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C2` — Reasoning based on multiple partners (1.5 marks)
- Rubric item: `R2`
- CERA's target criteria: _any of: communicate with various partners / multiple websites counts as the reason_
- CERA's evidence facets: ['communicate with various partners', 'websites']
- Award rate across cohort: **12%** (FULL=1 PARTIAL=3 ABSENT/INCORRECT=16 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QCONN_01` (human gold=5.0/5)
  - answer: "In this case it is better to use a conncetionless service, because it is not necessary to hold a connection in the time you are reading the first results. So more people can search at the same time."
  - CGR reasoning: "The student does not mention communicating with multiple partners or websites as the reason for choosing a connectionless service. The student focuses on the idle time between searches rather than the"
- `QCONN_03` (human gold=5.0/5)
  - answer: "It is better to use a connectionless service in this scenario.
During the process of refining the query, the connection would be idle but still blocked for other users.
Therefor a connectionless service is better here."
  - CGR reasoning: "The student does not mention communicating with multiple partners or websites as the reason for choosing a connectionless service. They focus on the connection being idle and blocked for other users."
- `QCONN_04` (human gold=5.0/5)
  - answer: "It is better to use a connectionless service, because subsequent telegrams from sender to receiver use different lines. This method can avoid connection failure."
  - CGR reasoning: "The student mentions that telegrams use different lines, but does not mention communicating with multiple partners or websites as the reason for choosing a connectionless service."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C3` — Reasoning based on short interaction duration (1.0 marks)
- Rubric item: `R3`
- CERA's target criteria: _any of: short periods of time / short data transfers counts as the reason_
- CERA's evidence facets: ['short periods of time', 'short data transfers']
- Award rate across cohort: **5%** (FULL=1 PARTIAL=0 ABSENT/INCORRECT=19 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QCONN_00` (human gold=5.0/5)
  - answer: "Für das gestellte Stenario ist Connectionless Service besser. Da durch Skalierbarkeit mehrere Webseiten gleichzeitig aufgeruden und gefunden werden können. Dadurch lässt sich schneller ein Ziel definieren und finden."
  - CGR reasoning: "The student argues for connectionless service based on scalability and speed, but does not mention short periods of time, short data transfers, skimming, or brief browsing as the reason for the choice"
- `QCONN_02` (human gold=5.0/5)
  - answer: "It is better to use a connection oriented service since you will be communicating especially with one search engine multiple times, and a loss of the query data is not acceptable."
  - CGR reasoning: "The student does not mention short periods of time, short data transfers, or skimming/brief browsing as a reason for their choice of protocol."
- `QCONN_03` (human gold=5.0/5)
  - answer: "It is better to use a connectionless service in this scenario.
During the process of refining the query, the connection would be idle but still blocked for other users.
Therefor a connectionless service is better here."
  - CGR reasoning: "The student identifies that a connectionless service is better, but their reasoning focuses on the connection being 'idle' and 'blocked for other users' rather than the short duration or brief nature "

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____

---
## Concept `Q1_C4` — Reasoning based on connection overhead (1.5 marks)
- Rubric item: `R4`
- CERA's target criteria: _Student explains that connection-oriented services incur unnecessary overhead for setup and teardown._
- CERA's evidence facets: ['overhead in the connecting and disconnecting phase']
- Award rate across cohort: **0%** (FULL=0 PARTIAL=0 ABSENT/INCORRECT=20 / n=20)

> No reliable auto-classifier for "genuine gap vs. facet-matching miss" (tested and rejected, see script header) — please read these and judge yourself.

Sample ABSENT/INCORRECT answers:
- `QCONN_00` (human gold=5.0/5)
  - answer: "Für das gestellte Stenario ist Connectionless Service besser. Da durch Skalierbarkeit mehrere Webseiten gleichzeitig aufgeruden und gefunden werden können. Dadurch lässt sich schneller ein Ziel definieren und finden."
  - CGR reasoning: "The student argues for connectionless service based on scalability and speed of searching, but does not mention connection overhead, setup, or teardown."
- `QCONN_01` (human gold=5.0/5)
  - answer: "In this case it is better to use a conncetionless service, because it is not necessary to hold a connection in the time you are reading the first results. So more people can search at the same time."
  - CGR reasoning: "The student discusses the benefit of not holding a connection open, but does not mention the overhead associated with the setup and teardown phases of a connection-oriented service."
- `QCONN_02` (human gold=5.0/5)
  - answer: "It is better to use a connection oriented service since you will be communicating especially with one search engine multiple times, and a loss of the query data is not acceptable."
  - CGR reasoning: "The student does not mention connection overhead, setup, or teardown. Instead, they argue for a connection-oriented service based on the need for reliability and repeated communication."

**Q1 — Is this concept required for FULL marks on the question, or is it bonus/optional?**
Your answer: _____

**Q2 — What should count as PARTIAL credit here, if anything?**
Your answer: _____

**Q3 — For the ABSENT samples above: did those students actually attempt this idea in different words, or is it genuinely missing?**
Your answer: _____
