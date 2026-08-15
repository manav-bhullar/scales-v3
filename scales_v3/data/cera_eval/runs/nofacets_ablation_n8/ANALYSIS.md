# No-facets ablation (CGR skip_facets=True)

CGR prompt receives empty Evidence Facets / keywords / variants; role forced to
`synonym_set` in the prompt. Target Criteria from corrected CQAs unchanged.

| Question | n | MAE no-facets | MAE with-facets (same students) | Δ MAE |
|---|---:|---:|---:|---:|
| CE08 | 8 | 0.562 | 0.625 | -0.063 |
| CE03 | 8 | 0.688 | 0.875 | -0.187 |
| CE10 | 8 | 1.047 | 0.891 | +0.156 |
| CE01 | 8 | 0.469 | 0.5 | -0.031 |
| CE05 | 8 | 0.562 | 0.5 | +0.062 |
| CE06 | 8 | 0.375 | 0.375 | +0.000 |
| CE07 | 8 | 0.25 | 0.344 | -0.094 |

(negative Δ = no-facets closer to human)

========================================================================

## CE08 · MAE no-facets 0.562 · with-facets 0.625

------------------------------------------------------------------------
### CE08_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
Heterogeneity: In wireless network, capabilities, responsibilities, and constraints of nodes might be different. For instance, the battery life of mobile devices, the transmission range, the radios may be different. Thus, putting those conditions into consideration is important.   Fairness: Fairness might be an issue in fixed and wired networks. However, the drastic change in mobile network topology leads to difficulty in maintaining fairness.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | Heterogeneity: In wireless network, capabilities, responsibilities, and constraints of nodes might be different. For instance, the battery life of mobile devices, the transmission range, the radios may be different. Thus, putting those conditions into consideration is importan… |
| `CE08_C2` | FULL | 1.5/1.5 | the drastic change in mobile network topology leads to difficulty in maintaining fairness. |
| `CE08_C3` | FULL | 1.5/1.5 | However, the drastic change in mobile network topology leads to difficulty in maintaining fairness. |

------------------------------------------------------------------------
### CE08_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3.5 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3.5 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
The network no longer has an ether to which all nodes are connected. Instead each node has its own radius, where it can send and receive communication.  The differences and overlaps of various radius cause problems like the hidden terminal or exposed terminal.  Also, due to the node’s mobility, the networks topology can change rapidly. Which routes are optimal, or even possible, changes with that.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | problems like the hidden terminal or exposed terminal.  Also, due to the node’s mobility, the networks topology can change rapidly. |
| `CE08_C2` | FULL | 1.5/1.5 | due to the node’s mobility, the networks topology can change rapidly. Which routes are optimal, or even possible, changes with that. |
| `CE08_C3` | FULL | 1.5/1.5 | due to the node’s mobility, the networks topology can change rapidly. Which routes are optimal, or even possible, changes with that. |

------------------------------------------------------------------------
### CE08_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
A first challenge is called Hidden Terminals. This means, that there might are nodes existing who can not hear each other. As a consequence like the example in the lecture collisions can be caused because two nodes who can not hear each other, might are communicating with one in between them, because one sends to the one in the middle. The other one doesn't know. Collision detection fails as well  A second challenge is "near and far terminals". Here the distance between nodes influences the strength of the signal. As a consequence the one who is closer to the communication partner drowns out the weaker one. This can cause further problems because the communication between two nodes is not working.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | A first challenge is called Hidden Terminals. ... A second challenge is "near and far terminals". |
| `CE08_C2` | FULL | 1.5/1.5 | A first challenge is called Hidden Terminals. This means, that there might are nodes existing who can not hear each other. As a consequence like the example in the lecture collisions can be caused because two nodes who can not hear each other, might are communicating with one … |
| `CE08_C3` | FULL | 1.5/1.5 | A second challenge is "near and far terminals". Here the distance between nodes influences the strength of the signal. As a consequence the one who is closer to the communication partner drowns out the weaker one. |

------------------------------------------------------------------------
### CE08_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 1.5 |

**Student answer**

```
Two challenges are hidden terminals, which occurs when two nodes can communicate over the same AP but not directly to each other, and exposed terminals, which occurs when two devices want to transmit data at the same time, but encounter a channel interference.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | Two challenges are hidden terminals, which occurs when two nodes can communicate over the same AP but not directly to each other, and exposed terminals, which occurs when two devices want to transmit data at the same time, but encounter a channel interference. |
| `CE08_C2` | FULL | 1.5/1.5 | hidden terminals, which occurs when two nodes can communicate over the same AP but not directly to each other |
| `CE08_C3` | FULL | 1.5/1.5 | exposed terminals, which occurs when two devices want to transmit data at the same time, but encounter a channel interference. |

------------------------------------------------------------------------
### CE08_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
HIDDEN TERMINALS: Node A and Node C can not receive message from each other, and they send messages to Node B simultaneously. But the transmission can conllide at Node B and both messages are lost, then Node A and Node C are hidden from each other. EXPOSED TERMINALS: Node A, D are outside of range of each other and in the miiddle Node B, C are inside of the range of each other. B sends to A currently and C wants to send to D. But C has to wait because it considers that it will has interference. However the transmission can take place as A is out of range of C. C is exposed to B.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | HIDDEN TERMINALS: Node A and Node C can not receive message from each other, and they send messages to Node B simultaneously. But the transmission can conllide at Node B and both messages are lost, then Node A and Node C are hidden from each other. EXPOSED TERMINALS: Node A, D… |
| `CE08_C2` | FULL | 1.5/1.5 | Node A and Node C can not receive message from each other, and they send messages to Node B simultaneously. But the transmission can conllide at Node B and both messages are lost |
| `CE08_C3` | FULL | 1.5/1.5 | EXPOSED TERMINALS: Node A, D are outside of range of each other and in the miiddle Node B, C are inside of the range of each other. B sends to A currently and C wants to send to D. But C has to wait because it considers that it will has interference. However the transmission c… |

------------------------------------------------------------------------
### CE08_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3.5 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
Two of the many challenges of mobile routing compared to fixed / wired networks are Hidden Terminals and security issues. Hidden Terminal can occur, when the nodes are quite far apart, while some nodes are not able to detect nodes anymore, while more centered nodes are able to detect messages from both the distant nodes. Then the distant nodes are not able to detect collisions occuring in the „middle“ of the network at the centered nodes, because the signal is not transmitted over all network nodes. One of the security issues can be, that wifi is set up inside of a building. A normal ethernet network over cable would connect all the nodes inside, and then can be configured to discard all the internal packages at the outgoing router to the internet. A wifi network cannot be configured, to only nodes inside of the building are able to receive the packages. If the network is available outside of the building, then any node outside will be able to detect the network.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | Two of the many challenges of mobile routing compared to fixed / wired networks are Hidden Terminals and security issues. |
| `CE08_C2` | FULL | 1.5/1.5 | One of the security issues can be, that wifi is set up inside of a building. A normal ethernet network over cable would connect all the nodes inside, and then can be configured to discard all the internal packages at the outgoing router to the internet. A wifi network cannot b… |
| `CE08_C3` | FULL | 1.5/1.5 | A wifi network cannot be configured, to only nodes inside of the building are able to receive the packages. If the network is available outside of the building, then any node outside will be able to detect the network. |

------------------------------------------------------------------------
### CE08_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3.5 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
(Due to the question in the forum, i will relate to slide 3, not to Challenges in Mobile Communications, which are on slide 10ff).

One basic challenge in Mobile Networking is the Power control: mobile devices have only a limited amount of power which should be used wisely and as little as possible.

In addition, the routing in Mobile Networking has to deal with a high amount of dynamic so it needs to find new routes as nodes move or conditions change.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | One basic challenge in Mobile Networking is the Power control: mobile devices have only a limited amount of power which should be used wisely and as little as possible. In addition, the routing in Mobile Networking has to deal with a high amount of dynamic so it needs to find … |
| `CE08_C2` | FULL | 1.5/1.5 | One basic challenge in Mobile Networking is the Power control: mobile devices have only a limited amount of power which should be used wisely and as little as possible. |
| `CE08_C3` | FULL | 1.5/1.5 | the routing in Mobile Networking has to deal with a high amount of dynamic so it needs to find new routes as nodes move or conditions change. |

------------------------------------------------------------------------
### CE08_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
Services Discovery is a challenge in Mobile Routing, since devices move around, so it becomes difficult to know where services are placed and how to be aware of them. Power control is also a challenge. In order for a device to have a certain range and suffer less interference, it needs a certain signal strength, which depends on the power.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | Services Discovery is a challenge in Mobile Routing, since devices move around, so it becomes difficult to know where services are placed and how to be aware of them. Power control is also a challenge. |
| `CE08_C2` | FULL | 1.5/1.5 | Services Discovery is a challenge in Mobile Routing, since devices move around, so it becomes difficult to know where services are placed and how to be aware of them. |
| `CE08_C3` | FULL | 1.5/1.5 | Power control is also a challenge. In order for a device to have a certain range and suffer less interference, it needs a certain signal strength, which depends on the power. |

========================================================================

## CE03 · MAE no-facets 0.688 · with-facets 0.875

------------------------------------------------------------------------
### CE03_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 3.5 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
In asynchronous transmission each character is bounded by a start and a stop bit. This is simple and inexpensive but has a low transmission. 
Synchronous transmission, sveral characters are put together to frames. This is more complex but has a higher transmission rate.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | In asynchronous transmission each character is bounded by a start and a stop bit. |
| `CE03_C2` | FULL | 1/1 | sveral characters are put together to frames. |
| `CE03_C3` | FULL | 1/1 | This is simple and inexpensive but has a low transmission. |
| `CE03_C4` | FULL | 1/1 | This is more complex but has a higher transmission rate. |

------------------------------------------------------------------------
### CE03_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Asynchronous transmission:
-Each character is bounded by a start bit and a stop bit
-Simple + inexpensive, but low transmission rates, often up to 200 bit/sec

Synchronous transmission:
-Several characters pooled to frames
-Frames defined by SYN or flag 
-More complex, but higher transmission rates
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | -Each character is bounded by a start bit and a stop bit |
| `CE03_C2` | FULL | 1/1 | -Several characters pooled to frames -Frames defined by SYN or flag |
| `CE03_C3` | FULL | 1/1 | Simple + inexpensive, but low transmission rates |
| `CE03_C4` | FULL | 1/1 | More complex, but higher transmission rates |

------------------------------------------------------------------------
### CE03_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Asynchronous transmission 
-Each character is bounded by a start bit and a stop bit 
-Simple + inexpensive, but low transmission rates, often up to 200 bit/sec 

Synchronous transmission 
-Several characters pooled to frames 
-Frames defined by SYN or flag 
-More complex, but higher transmission rates
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | -Each character is bounded by a start bit and a stop bit |
| `CE03_C2` | FULL | 1/1 | -Several characters pooled to frames  -Frames defined by SYN or flag |
| `CE03_C3` | FULL | 1/1 | Simple + inexpensive, but low transmission rates |
| `CE03_C4` | FULL | 1/1 | More complex, but higher transmission rates |

------------------------------------------------------------------------
### CE03_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
While in asynchronous transmission every character is bounded by a start and a end bit, in synchronous transmission several character are bound to frames, these frames are bound by SYN or flag. The asynchronous transmission is simple and inexpensive, but has a low transmission rate, up to 200 bit/sec, while the synchronous transmission has a higher transmission rate, but is more complex.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | in asynchronous transmission every character is bounded by a start and a end bit |
| `CE03_C2` | FULL | 1/1 | in synchronous transmission several character are bound to frames, these frames are bound by SYN or flag. |
| `CE03_C3` | FULL | 1/1 | The asynchronous transmission is simple and inexpensive, but has a low transmission rate |
| `CE03_C4` | FULL | 1/1 | the synchronous transmission has a higher transmission rate, but is more complex. |

------------------------------------------------------------------------
### CE03_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **2 / 4** |
| System (with facets) | 2 / 4 |
| abs err no-facets | 2 |

**Student answer**

```
asynchronous transmission:
-works character by character
-each character who should transmission has a start and stop bit

synchronous transmission:
-several characters pooled to frames
-the frames where defined by SYN or flag
-different data formats (bit-synchronization, character-synchronization)
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | -works character by character -each character who should transmission has a start and stop bit |
| `CE03_C2` | FULL | 1/1 | -several characters pooled to frames -the frames where defined by SYN or flag |
| `CE03_C3` | ABSENT | 0/1 | — |
| `CE03_C4` | ABSENT | 0/1 | — |

------------------------------------------------------------------------
### CE03_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3 / 4** |
| System (with facets) | 2.5 / 4 |
| abs err no-facets | 1 |

**Student answer**

```
In an asynchronous transmission each byte is sent separately and has a start and an end bit.
In a synchronous transmission data is sent in frames which can lead to higher transmission rates but becomes more complex.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | In an asynchronous transmission each byte is sent separately and has a start and an end bit. |
| `CE03_C2` | FULL | 1/1 | In a synchronous transmission data is sent in frames |
| `CE03_C3` | ABSENT | 0/1 | — |
| `CE03_C4` | FULL | 1/1 | In a synchronous transmission data is sent in frames which can lead to higher transmission rates but becomes more complex. |

------------------------------------------------------------------------
### CE03_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
Synchronous Data transmission means that many characters/symbols are transferred within a frame while asynchronous transmission transfers the data byte wise /character wise each, so the data is not collected into a frame. Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start is slowing down the speed especially in fast transmission.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start is slowing down the speed especially in fast transmission. |
| `CE03_C2` | FULL | 1/1 | Synchronous Data transmission means that many characters/symbols are transferred within a frame |
| `CE03_C3` | FULL | 1/1 | Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start is slowing down the speed especially in fast transmission. |
| `CE03_C4` | PARTIAL | 0.5/1 | Asynchronous is definitely simpler |

------------------------------------------------------------------------
### CE03_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **2 / 4** |
| System (with facets) | 2 / 4 |
| abs err no-facets | 2 |

**Student answer**

```
Asynchronous mode:
Each character is bounded by a start bit and a stop bit.

Synchronous mode:
Several characters are pooled to one frame which is defined by a SYN or a flag.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | Each character is bounded by a start bit and a stop bit. |
| `CE03_C2` | FULL | 1/1 | Several characters are pooled to one frame which is defined by a SYN or a flag. |
| `CE03_C3` | ABSENT | 0/1 | — |
| `CE03_C4` | ABSENT | 0/1 | — |

========================================================================

## CE10 · MAE no-facets 1.047 · with-facets 0.891

------------------------------------------------------------------------
### CE10_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **5 / 5** |
| System (no facets) | **5 / 5** |
| System (with facets) | 5 / 5 |
| abs err no-facets | 0 |

**Student answer**

```
Phase 1： Slow Start.
Phase 2:  Congestion avoidance.

When cwnd < ss_thresh: cwnd increases rate exponentially. 
When cwnd >=ss_thresh: TCP slows down the increase of cwnd. Cwnd increases additively(i.e. cwdn ++);
When timeout, ss_thresh is set to half of the current value of cwnd, and cwnd is set to 1. The whole proccess start from Slow Start again.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1： Slow Start. Phase 2:  Congestion avoidance. |
| `CE10_C2` | FULL | 2/2 | When cwnd < ss_thresh: cwnd increases rate exponentially. |
| `CE10_C3` | FULL | 2/2 | Cwnd increases additively(i.e. cwdn ++); |

------------------------------------------------------------------------
### CE10_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3.75 / 5** |
| System (no facets) | **2 / 5** |
| System (with facets) | 3 / 5 |
| abs err no-facets | 1.75 |

**Student answer**

```
1. Slow start: Each time a segment is acknowledged cwnd is incremented by one. Continues until cwnd reaches ss_thresh or a packet gets lost. 2. Congestion Avoidance If congestions occurs ss_thresh is set to 50% of the current cwnd an the new cwnd is set to one. Then the slow start is entered.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | 1. Slow start: Each time a segment is acknowledged cwnd is incremented by one. Continues until cwnd reaches ss_thresh or a packet gets lost. 2. Congestion Avoidance |
| `CE10_C2` | PARTIAL | 1/2 | Each time a segment is acknowledged cwnd is incremented by one. |
| `CE10_C3` | ABSENT | 0/2 | — |

------------------------------------------------------------------------
### CE10_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4.4 / 5** |
| System (no facets) | **2 / 5** |
| System (with facets) | 3 / 5 |
| abs err no-facets | 2.4 |

**Student answer**

```
The phases are slow start and congestion avoidance.
In the slow phase, the cwnd starts getting bigger in size, first slowly, then rapidly, until the ssthresh is reached. Once reached, the congestion control phase begins, where the cwnd slowly grows in size until a congestion occurs (timeout). In this case the slow start phase is entered again, the cwnd is reset and a new ssthresh is calculated (half of reached cwnd before timeout.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | The phases are slow start and congestion avoidance. |
| `CE10_C2` | ABSENT | 0/2 | — |
| `CE10_C3` | PARTIAL | 1/2 | Once reached, the congestion control phase begins, where the cwnd slowly grows in size until a congestion occurs (timeout). |

------------------------------------------------------------------------
### CE10_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2.5 / 5** |
| System (no facets) | **3 / 5** |
| System (with facets) | 3 / 5 |
| abs err no-facets | 0.5 |

**Student answer**

```
Phase 1 (Slow Start):  cwnd++ for each acknowledged segmentPhase 2 (Congestion Avoidance):  ss_thresh = cwnd / 2  cwnd = 1
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1 (Slow Start):  cwnd++ for each acknowledged segmentPhase 2 (Congestion Avoidance):  ss_thresh = cwnd / 2  cwnd = 1 |
| `CE10_C2` | FULL | 2/2 | cwnd++ for each acknowledged segment |
| `CE10_C3` | INCORRECT | 0/2 | Phase 2 (Congestion Avoidance):  ss_thresh = cwnd / 2  cwnd = 1 |

------------------------------------------------------------------------
### CE10_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4.4 / 5** |
| System (no facets) | **5 / 5** |
| System (with facets) | 5 / 5 |
| abs err no-facets | 0.6 |

**Student answer**

```
Phase 1 (Slow Start)Phase 2 (Congestion Avoidance)The congestion Window is increased exponentially. After the cwnd >= ss_resh, the phase 2 starts and the cwnd is increased linear over time. If a congestion happens, cwnd is set again to 1 and ss_tresh is set to half the cwnd at the time of the congestion. With these new values, the phase 1 starts again.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1 (Slow Start)Phase 2 (Congestion Avoidance) |
| `CE10_C2` | FULL | 2/2 | The congestion Window is increased exponentially. |
| `CE10_C3` | FULL | 2/2 | the cwnd is increased linear over time |

------------------------------------------------------------------------
### CE10_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3.125 / 5** |
| System (no facets) | **2 / 5** |
| System (with facets) | 5 / 5 |
| abs err no-facets | 1.125 |

**Student answer**

```
Phase 1: Slow start (getting to equilibrium) Phase 2: Congestion Avoidance In the Slow Start phase each time when a segment is acknowledged cwnd gets incremented by one until we reach ss_thresh or have packet loss. So in the slow start phase its always cwnd less than ss_tresh and when cwnd >= ss_tresh the increase of cwnd slows down. In the Phase of Congestion Avoidance, when we have a timeout, ss_tresh is set to 50% of the current size of the congestion window, cwnd gets reset to one and we enter slow-start.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1: Slow start (getting to equilibrium) Phase 2: Congestion Avoidance |
| `CE10_C2` | PARTIAL | 1/2 | In the Slow Start phase each time when a segment is acknowledged cwnd gets incremented by one |
| `CE10_C3` | ABSENT | 0/2 | — |

------------------------------------------------------------------------
### CE10_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4.4 / 5** |
| System (no facets) | **5 / 5** |
| System (with facets) | 5 / 5 |
| abs err no-facets | 0.6 |

**Student answer**

```
Phase 1: Slow start
The sender sends as much segemnts as specified in cwnd and for each ACK received, cwnd is increased by one. This exponential growth continues until the ss_thresh is reached.
Phase 2: Congestion avoidance
In the congestion avoidance phase the cwnd is only increased by one per roundtrip time. If a timeout (= congestion) occurs the ss_tresh is set to cwnd/2 and cwnd is reset to 1.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1: Slow start ... Phase 2: Congestion avoidance |
| `CE10_C2` | FULL | 2/2 | for each ACK received, cwnd is increased by one. This exponential growth continues until the ss_thresh is reached. |
| `CE10_C3` | FULL | 2/2 | In the congestion avoidance phase the cwnd is only increased by one per roundtrip time. |

------------------------------------------------------------------------
### CE10_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4.4 / 5** |
| System (no facets) | **3 / 5** |
| System (with facets) | 3 / 5 |
| abs err no-facets | 1.4 |

**Student answer**

```
Phase one is slow start and phase two is congestion avoidance, cwnd starts at 1, and will rapidly grow until the value reached ss_thresh, after that cwnd will grow slowly, when a timeout occured, set ss_thresh to 50% of the current cwnd and cwnd is reset to one, then start over from slow start.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase one is slow start and phase two is congestion avoidance |
| `CE10_C2` | PARTIAL | 1/2 | cwnd starts at 1, and will rapidly grow until the value reached ss_thresh |
| `CE10_C3` | PARTIAL | 1/2 | after that cwnd will grow slowly |

========================================================================

## CE01 · MAE no-facets 0.469 · with-facets 0.5

------------------------------------------------------------------------
### CE01_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.5 / 3** |
| System (with facets) | 2.25 / 3 |
| abs err no-facets | 0.5 |

**Student answer**

```
1. Unconfirmed connectionless service: transmission of isolated, idependent units without acknowledgement, possible loss of data / no flow control
2. Confirmed connectionless service: transmission with acknowledgement with no loss, has timeouts and retransmission / no flow control
3. Connection-oriented service:  connection over error free channel with a flow control
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | 1. Unconfirmed connectionless service: transmission of isolated, idependent units without acknowledgement, possible loss of data / no flow control 2. Confirmed connectionless service: transmission with acknowledgement with no loss, has timeouts and retransmission / no flow con… |
| `CE01_C2` | FULL | 0.5/0.5 | transmission of isolated, idependent units without acknowledgement, possible loss of data / no flow control |
| `CE01_C3` | PARTIAL | 0.25/0.5 | 2. Confirmed connectionless service: transmission with acknowledgement with no loss, has timeouts and retransmission / no flow control |
| `CE01_C4` | PARTIAL | 0.25/0.5 | 3. Connection-oriented service:  connection over error free channel with a flow control |

------------------------------------------------------------------------
### CE01_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.75 / 3** |
| System (with facets) | 2.25 / 3 |
| abs err no-facets | 0.25 |

**Student answer**

```
three service classes are:
1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error

2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible
,has sequencing error
3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | three service classes are: 1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error  2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible ,has sequencing er… |
| `CE01_C2` | FULL | 0.5/0.5 | 1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error |
| `CE01_C3` | PARTIAL | 0.25/0.5 | 2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible ,has sequencing error |
| `CE01_C4` | FULL | 0.5/0.5 | 3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error |

------------------------------------------------------------------------
### CE01_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets) | 3 / 3 |
| abs err no-facets | 0 |

**Student answer**

```
The three services are called Unconfirmed Connectionless Service, Confirmed Connectionless Service and Connection-Oriented Service. These differ in their characteristics and areas of application. The first two services differ in whether or not the receiver acknowledges a packet when it receives it. The Unconfirmed Connectionless service does not include confirmation and assumes that the sent packets have arrived correctly. By confirming in the Confirmed Connectionless  service, this service can ensure that all packets have arrived at the receiver. Lost packets cannot be confirmed and so the recipient sends the packet again after a specified timeout. Both mentioned services have no flow control and no explicit requests to establish or disconnect a connection. The Confirmed Connectionless service has an implicit confirmation if a connection can be established, exactly when its packets are confirmed by the receiver. The confirmation of the second service class can cause duplicates to appear at the receiver, when the confirmation of a packet does not arrive at the sender. The third service class executes a three-phase communication and tries to establish a connection first. If the connection is confirmed, packets are sent until a request for disconnection is sent and confirmed. If the communication takes place over an error-free channel, no losses, no duplicates and no sequence errors are to be expected. Flow control is guaranteed by the "handshake". The first service type is usually used for the transition of isolated single units in channels with very low error rate (e.g. LANs, voice communication). The second service type can be used for channels with a high error rate such as mobile communication. The last service type is preferred for long and persistent communication.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | The three services are called Unconfirmed Connectionless Service, Confirmed Connectionless Service and Connection-Oriented Service. |
| `CE01_C2` | FULL | 0.5/0.5 | The Unconfirmed Connectionless service does not include confirmation and assumes that the sent packets have arrived correctly. ... Both mentioned services have no flow control and no explicit requests to establish or disconnect a connection. |
| `CE01_C3` | FULL | 0.5/0.5 | By confirming in the Confirmed Connectionless  service, this service can ensure that all packets have arrived at the receiver. ... Both mentioned services have no flow control and no explicit requests to establish or disconnect a connection. ... The confirmation of the second … |
| `CE01_C4` | FULL | 0.5/0.5 | If the communication takes place over an error-free channel, no losses, no duplicates and no sequence errors are to be expected. Flow control is guaranteed by the "handshake". |

------------------------------------------------------------------------
### CE01_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.5 / 3** |
| System (with facets) | 2.25 / 3 |
| abs err no-facets | 0.5 |

**Student answer**

```
L2 Service Class “Unconfirmed Connectionless Service”: Transmission of isolated, independent units (frames). The data may be lost.
L2 Service Class “Confirmed Connectionless Service”: Each single frame is acknowledged so there is no loss. Timeout and retransmit if the sender does not receive an acknowledgement within a certain time frame. Duplicates and sequence errors may happen due to “retransmit”.
L2 Service Class “Connection-Oriented Service”: Three-phased communication: 1. Connection 2. Data Transfer 3. Disconnection. Hence no loss, no duplication, no sequencing error.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | L2 Service Class “Unconfirmed Connectionless Service”: Transmission of isolated, independent units (frames). The data may be lost. L2 Service Class “Confirmed Connectionless Service”: Each single frame is acknowledged so there is no loss. Timeout and retransmit if the sender d… |
| `CE01_C2` | PARTIAL | 0.25/0.5 | The data may be lost. |
| `CE01_C3` | FULL | 0.5/0.5 | Each single frame is acknowledged so there is no loss. Timeout and retransmit if the sender does not receive an acknowledgement within a certain time frame. Duplicates and sequence errors may happen due to “retransmit”. |
| `CE01_C4` | PARTIAL | 0.25/0.5 | Three-phased communication: 1. Connection 2. Data Transfer 3. Disconnection. Hence no loss, no duplication, no sequencing error. |

------------------------------------------------------------------------
### CE01_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.75 / 3** |
| System (with facets) | 3 / 3 |
| abs err no-facets | 0.25 |

**Student answer**

```
three service classes are:
1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error

2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible
,has sequencing error
3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | three service classes are: 1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error  2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible ,has sequencing er… |
| `CE01_C2` | FULL | 0.5/0.5 | 1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error |
| `CE01_C3` | PARTIAL | 0.25/0.5 | 2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible ,has sequencing error |
| `CE01_C4` | FULL | 0.5/0.5 | 3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error |

------------------------------------------------------------------------
### CE01_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.25 / 3** |
| System (with facets) | 2.25 / 3 |
| abs err no-facets | 0.75 |

**Student answer**

```
Unconfirmed connectionless service: Data is sent directly and no acknowledgements are returned
Confirmed Connectionless service: Data is sent directly and acknowledgements are returned by the receiver when the data has arrived. If the sender does not receive an acknowledgement with a defined time interval, the data is retransmitted.
Connectionoriented service: Three phases of communication: 1. The connection is initialized by exchanging parameters 2. data is transferred 3. Connection is closed due to that flow control is possible in this case.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | Unconfirmed connectionless service: Data is sent directly and no acknowledgements are returned Confirmed Connectionless service: Data is sent directly and acknowledgements are returned by the receiver when the data has arrived. If the sender does not receive an acknowledgement… |
| `CE01_C2` | PARTIAL | 0.25/0.5 | Unconfirmed connectionless service: Data is sent directly and no acknowledgements are returned |
| `CE01_C3` | PARTIAL | 0.25/0.5 | Confirmed Connectionless service: Data is sent directly and acknowledgements are returned by the receiver when the data has arrived. If the sender does not receive an acknowledgement with a defined time interval, the data is retransmitted. |
| `CE01_C4` | PARTIAL | 0.25/0.5 | Connectionoriented service: Three phases of communication: 1. The connection is initialized by exchanging parameters 2. data is transferred 3. Connection is closed due to that flow control is possible in this case. |

------------------------------------------------------------------------
### CE01_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.25 / 3** |
| System (with facets) | 2.5 / 3 |
| abs err no-facets | 0.75 |

**Student answer**

```
For the Data Link Layer there are 3 service classes: unconfirmed conn.less service, confirmed conn.less service and connection-oriented service. 
In unconfirmed conn.less service a data is sent to receiver. In this case a sender does not know if the sent data has arrived at the receiver. In other words, we don't get any confirmation from the receiver about arrived data. In case of loss data the data will be not resend. If any Correct data arrives, there is no correcting mechanism implemented.
Confirmed conn.less service is a bidirectional communication between sender and receiver. After a sender sends a frame, a receiver sends an acknowledgement as answer. In the case of loss data a frame will be retransmit (after timeout) as long as the sender gets an acknowledgement from the receiver. In confirmed conn.less service there is no flow control implemented. 
In the last kind of service, connection-oriented service, a connection between parties has to be estabilished firstly before we can send any data. We speak of 3-phased communication: connection estabilishment (a sender sends a request to receiver, the receiver confirms it); data transfer (after the receiver gets a frame, sends an acknowledgement to the sender); disconnection (analog to connection estabilishment). In connection-oriented service there is flow control implemented.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | For the Data Link Layer there are 3 service classes: unconfirmed conn.less service, confirmed conn.less service and connection-oriented service. |
| `CE01_C2` | PARTIAL | 0.25/0.5 | In this case a sender does not know if the sent data has arrived at the receiver. In other words, we don't get any confirmation from the receiver about arrived data. In case of loss data the data will be not resend. |
| `CE01_C3` | PARTIAL | 0.25/0.5 | After a sender sends a frame, a receiver sends an acknowledgement as answer. In the case of loss data a frame will be retransmit (after timeout) as long as the sender gets an acknowledgement from the receiver. In confirmed conn.less service there is no flow control implemented. |
| `CE01_C4` | PARTIAL | 0.25/0.5 | a connection between parties has to be estabilished firstly before we can send any data. We speak of 3-phased communication: connection estabilishment (a sender sends a request to receiver, the receiver confirms it); data transfer (after the receiver gets a frame, sends an ack… |

------------------------------------------------------------------------
### CE01_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **2.25 / 3** |
| System (with facets) | 2.5 / 3 |
| abs err no-facets | 0.75 |

**Student answer**

```
1.unconfirmed connection-less service 2.confirmed connection-less service 3.connection-oriented service.
2. there is flow-control in connection-oriented service. But in other two there's no flow-control, no connect or disconnect.
There is no loss, no duplication, no sequencing error in connection-oriented service.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | 1.unconfirmed connection-less service 2.confirmed connection-less service 3.connection-oriented service. |
| `CE01_C2` | PARTIAL | 0.25/0.5 | But in other two there's no flow-control, no connect or disconnect. |
| `CE01_C3` | ABSENT | 0/0.5 | — |
| `CE01_C4` | FULL | 0.5/0.5 | there is flow-control in connection-oriented service. ... There is no loss, no duplication, no sequencing error in connection-oriented service. |

========================================================================

## CE05 · MAE no-facets 0.562 · with-facets 0.5

------------------------------------------------------------------------
### CE05_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Some of the objectives are: support billion of end-systems, reduce routing tables, simplify protocol processing, increase security, support real ti,e data traffic, provide multicasting, support mobility, be open for change, coexistence with existing protocols
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | support billion of end-systems, reduce routing tables |
| `CE05_C2` | FULL | 1/1 | simplify protocol processing, increase security |
| `CE05_C3` | FULL | 1/1 | support real ti,e data traffic, provide multicasting, support mobility |
| `CE05_C4` | FULL | 1/1 | be open for change, coexistence with existing protocols |

------------------------------------------------------------------------
### CE05_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 1 |

**Student answer**

```
Longer addresses (16 bytes) should be supported in order to increase the address space such that more destinations can be specified than via IPv4 addresses.

Security means should be integrated into the protocol to increase security when using it (Implementation of IPsec within the IPv6 standard which enables encryption and verification of the authenticity of IP packets).

The protocol processing should be simplified by simplifying the header data.

Real time data traffic with tracked quality of service should be supported by introducing flow labels and traffic classes.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | Longer addresses (16 bytes) should be supported in order to increase the address space such that more destinations can be specified than via IPv4 addresses. |
| `CE05_C2` | FULL | 1/1 | Security means should be integrated into the protocol to increase security when using it |
| `CE05_C3` | FULL | 1/1 | Real time data traffic with tracked quality of service should be supported by introducing flow labels and traffic classes. |
| `CE05_C4` | ABSENT | 0/1 | — |

------------------------------------------------------------------------
### CE05_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
The objective of IPv6 is to support assigning IP to new systems, and simplify the header.

1. Supporting billions of end systems by providing longer address.
2. Simplifying protocol processing by providing simplified header.
3. Supporting real time data traffic by creating flow label and differentiating traffic class.
4. Support multicasting and mobility or roaming.
5. Open for change in future. like extension header,
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | 1. Supporting billions of end systems by providing longer address. |
| `CE05_C2` | FULL | 1/1 | 2. Simplifying protocol processing by providing simplified header. |
| `CE05_C3` | FULL | 1/1 | 3. Supporting real time data traffic by creating flow label and differentiating traffic class. 4. Support multicasting and mobility or roaming. |
| `CE05_C4` | FULL | 1/1 | 5. Open for change in future. like extension header, |

------------------------------------------------------------------------
### CE05_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
The objectives of IPv6:
Firstly, to support billions of end-systems.
Secondly, to reduce routing tables. 
Thirdly, to simplify protocol processing.
Fourthly, to increase security and this security means integrated.
Fifthly, to support real time data traffic (quality of service) such as flow label, traffic class.
Sixthly, to provide multicasting.
Seventhly, to support mobility (roaming).
Eighthly, to be open for change (future). 
Ninthly, to coexistence with existing protocols.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | Firstly, to support billions of end-systems. |
| `CE05_C2` | FULL | 1/1 | Thirdly, to simplify protocol processing. |
| `CE05_C3` | FULL | 1/1 | Fifthly, to support real time data traffic (quality of service) such as flow label, traffic class. |
| `CE05_C4` | FULL | 1/1 | Eighthly, to be open for change (future). Ninthly, to coexistence with existing protocols. |

------------------------------------------------------------------------
### CE05_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **2 / 4** |
| System (with facets) | 2 / 4 |
| abs err no-facets | 2 |

**Student answer**

```
To support billions of end-systems
To reduce routing tables
To simplify protocol processing
To increase security
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | To support billions of end-systems |
| `CE05_C2` | FULL | 1/1 | To simplify protocol processing |
| `CE05_C3` | ABSENT | 0/1 | — |
| `CE05_C4` | ABSENT | 0/1 | — |

------------------------------------------------------------------------
### CE05_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3.5 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
The first main objective for the introduction of IPv6 was the support of more addresses in the network. While IPv4 with 4 byte addresses only allowed roughly about 4 billion participants, IPv6 enables up to 2^128 addresses, what should be enough for the next centuries. This enlargement of the address room became important with the introduction of mobile computing, smart home and internet of things. 
The second objective was to simplify the process of forwarding and building routing tables by simplifying the header of IPv6-addresses, which are now easier and faster to decode for routers. 
Furthermore, the way IPv6 addresses are handled in a network allowed a higher level of security in comparison to IPv4.
IPv6 allows better guarantees for Quality of Service, especially for real time traffic. This is also due to changes of the header of such an IP-packet. 
Another important lesson learnd from the development history of IPv4 and therefore a main objective for IPv6 was to make it adaptive to future developments: So the IPv6 protocol allows introduction of extension headers for future functionalities.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | PARTIAL | 0.5/1 | The second objective was to simplify the process of forwarding and building routing tables by simplifying the header of IPv6-addresses |
| `CE05_C2` | FULL | 1/1 | The second objective was to simplify the process of forwarding and building routing tables by simplifying the header of IPv6-addresses, which are now easier and faster to decode for routers. |
| `CE05_C3` | FULL | 1/1 | IPv6 allows better guarantees for Quality of Service, especially for real time traffic. |
| `CE05_C4` | FULL | 1/1 | make it adaptive to future developments: So the IPv6 protocol allows introduction of extension headers for future functionalities. |

------------------------------------------------------------------------
### CE05_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
1.	Supporting billions of end-systems: With its longer addresses IPv6 can support more end-systems.
2.	Supporting real time data traffic: The flow label field („traffic class“) allows another quality of service.
3.	Simplifying protocol processing: The header in IPv4 is much more complex than the header of IPv6, so with IPv6 the processing of protocols is simpler. 
4.	Openness for potential change in the future: With the option to use the extension headers, IPv6 provides something that can be useful in the future.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | 1.	Supporting billions of end-systems: With its longer addresses IPv6 can support more end-systems. |
| `CE05_C2` | FULL | 1/1 | 3. Simplifying protocol processing: The header in IPv4 is much more complex than the header of IPv6, so with IPv6 the processing of protocols is simpler. |
| `CE05_C3` | FULL | 1/1 | 2. Supporting real time data traffic: The flow label field („traffic class“) allows another quality of service. |
| `CE05_C4` | FULL | 1/1 | 4.	Openness for potential change in the future: With the option to use the extension headers, IPv6 provides something that can be useful in the future. |

------------------------------------------------------------------------
### CE05_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 1 |

**Student answer**

```
To support billions of end systems To increase security To support real time data traffic To support mobility To reduce routing tables
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | To support billions of end systems |
| `CE05_C2` | FULL | 1/1 | To increase security |
| `CE05_C3` | FULL | 1/1 | To support real time data traffic |
| `CE05_C4` | ABSENT | 0/1 | — |

========================================================================

## CE06 · MAE no-facets 0.375 · with-facets 0.375

------------------------------------------------------------------------
### CE06_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2 / 4** |
| System (no facets) | **3 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 1 |

**Student answer**

```
The dhcp protocol is a protocol to configure systems that join a network.
It is used to assign ip addresses to systems within the network. 
If a system joins the network it can ask the dhcp server for network configuration and an ip address that it should use in the future.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | It is used to assign ip addresses to systems within the network. If a system joins the network it can ask the dhcp server for network configuration and an ip address |
| `CE06_C2` | PARTIAL | 1/2 | It is used to assign ip addresses to systems within the network. |

------------------------------------------------------------------------
### CE06_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
DHCP is a network management protocol which extends the functionality of RARP and BOOTP. DHCP simplifies installation and cofiguration of end systems. It also allows for manual and automatic IP address assignment.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is a network management protocol... It also allows for manual and automatic IP address assignment. |
| `CE06_C2` | FULL | 2/2 | DHCP simplifies installation and cofiguration of end systems. It also allows for manual and automatic IP address assignment. |

------------------------------------------------------------------------
### CE06_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
DHCP is a network management protocol in which it simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment, and may provide additional configuration information. DHCP server is used for assignments in which the address is assigned for a limited time only before it expires.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is a network management protocol in which it simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment, and may provide additional configuration information. |
| `CE06_C2` | FULL | 2/2 | simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment, and may provide additional configuration information. |

------------------------------------------------------------------------
### CE06_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **3 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 1 |

**Student answer**

```
DHCP is used to assign IP addresses and other configuration to (new) hosts in a network. After an initial DHCP DISCOVER packet of a client the server sends the assigned IP address back with additional information, like DNS server or netmask.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is used to assign IP addresses and other configuration to (new) hosts in a network. |
| `CE06_C2` | PARTIAL | 1/2 | DHCP is used to assign IP addresses and other configuration to (new) hosts in a network. |

------------------------------------------------------------------------
### CE06_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **1 / 4** |
| System (no facets) | **2 / 4** |
| System (with facets) | 3 / 4 |
| abs err no-facets | 1 |

**Student answer**

```
DHCP is a newer version of RARP. 
Systems use this protocol to resolve their own IP address in a network from their hardware/MAC address. 
A specific DHCP server assigns the IP addresses and is contacted to resolve them.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | PARTIAL | 1/2 | A specific DHCP server assigns the IP addresses |
| `CE06_C2` | PARTIAL | 1/2 | A specific DHCP server assigns the IP addresses and is contacted to resolve them. |

------------------------------------------------------------------------
### CE06_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
The Dynamic Host Configuration Protocol (DHCP) is Internet Protocol based on the special server that uses for manually or automatically IP addresses assignment and other network configuration parameters, such as subnet masks and default gateways, to each device on a network so they can communicate with other IP networks.
This server need not be on the same LAN as the requesting host. Since the DHCP server may not be reachable by broadcasting, a DHCP relay agent is needed on each LAN.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | The Dynamic Host Configuration Protocol (DHCP) is Internet Protocol based on the special server that uses for manually or automatically IP addresses assignment and other network configuration parameters, such as subnet masks and default gateways |
| `CE06_C2` | FULL | 2/2 | uses for manually or automatically IP addresses assignment and other network configuration parameters, such as subnet masks and default gateways |

------------------------------------------------------------------------
### CE06_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Dynamic Host Configuration Protocol (DHCP) is a protocol for managing IP addresses in a TCP / IP network and distributing them to the requesting hosts. With DHCP, every network participant is able to configure itself automatically. 
To set up a network via TCP/IP, it is necessary to carry out an IP configuration on each host. For a TCP/IP network, the following settings must be made on each host:
- Allocation of a unique IP address
- Assign a subnet mask
- Assign the responsible default or standard gateway
- Assign the responsible DNS server
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | Dynamic Host Configuration Protocol (DHCP) is a protocol for managing IP addresses in a TCP / IP network and distributing them to the requesting hosts. With DHCP, every network participant is able to configure itself automatically. |
| `CE06_C2` | FULL | 2/2 | managing IP addresses in a TCP / IP network and distributing them to the requesting hosts. With DHCP, every network participant is able to configure itself automatically. |

------------------------------------------------------------------------
### CE06_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2 / 4** |
| System (no facets) | **2 / 4** |
| System (with facets) | 2 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
DHCP is a protocol for automatic or manual allocation of IP addresses to devices, which is usually done by a DHCP server.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | PARTIAL | 1/2 | DHCP is a protocol for automatic or manual allocation of IP addresses to devices |
| `CE06_C2` | PARTIAL | 1/2 | automatic or manual allocation of IP addresses to devices |

========================================================================

## CE07 · MAE no-facets 0.25 · with-facets 0.344

------------------------------------------------------------------------
### CE07_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Extension Headers enable you to add additional header information to the already existing header if you really need them. They are placed between the header and the payload, by reducing the payload size if they get appended. The main advantage is, that you can overcome the size problem of the header and add additional information without changing the original header size.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Extension Headers enable you to add additional header information to the already existing header if you really need them. ... The main advantage is, that you can overcome the size problem of the header and add additional information without changing the original header size. |
| `CE07_C2` | FULL | 1/1 | They are placed between the header and the payload |
| `CE07_C3` | FULL | 1.5/1.5 | The main advantage is, that you can overcome the size problem of the header and add additional information without changing the original header size. |

------------------------------------------------------------------------
### CE07_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 4** |
| System (no facets) | **2.5 / 4** |
| System (with facets) | 2.5 / 4 |
| abs err no-facets | 0.5 |

**Student answer**

```
The header in IPv6 has a fixed length and is designed to be used for easy processing, it only contains information needed for routing. Any additional information is stored in extension headers. They carry optional information and can be found in between the fixed header and the playload. Since the whole IPv6 packet is only allowed a certain size, these additional extension headers take up space of the payload. The main advantage of extension headers is that they can be added optionally and help to overcome size limitation.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Any additional information is stored in extension headers. They carry optional information and can be found in between the fixed header and the playload. |
| `CE07_C2` | FULL | 1/1 | They carry optional information and can be found in between the fixed header and the playload. |
| `CE07_C3` | ABSENT | 0/1.5 | — |

------------------------------------------------------------------------
### CE07_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2 / 4** |
| System (no facets) | **1.75 / 4** |
| System (with facets) | 1.75 / 4 |
| abs err no-facets | 0.25 |

**Student answer**

```
Extension Headers are extensions for the normal header. You can support multiple addresses or specify more options for your header and packet, like e.g. authentication.

The Extension Headers are located between the normal header and the payload, they will be attached to the normal header. 

The biggest advantage of Extension Headers is the possibility to use broadcasting.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | PARTIAL | 0.75/1.5 | Extension Headers are extensions for the normal header. You can support multiple addresses or specify more options for your header and packet |
| `CE07_C2` | FULL | 1/1 | The Extension Headers are located between the normal header and the payload |
| `CE07_C3` | ABSENT | 0/1.5 | — |

------------------------------------------------------------------------
### CE07_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
The extension headers replace the "option-field" in IPv4 and include optional more informations. They are placed between the actual header and the payload. The main advantage is that they can expand the header informations upon need without expanding the fixed header structure.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | they can expand the header informations upon need without expanding the fixed header structure. |
| `CE07_C2` | FULL | 1/1 | They are placed between the actual header and the payload. |
| `CE07_C3` | FULL | 1.5/1.5 | The main advantage is that they can expand the header informations upon need without expanding the fixed header structure. |

------------------------------------------------------------------------
### CE07_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Extension headers are header that can be added to a packet for a new functionality. Extension headers are present between fixed header and payload. 
Advantages:
1. They allow appending new options without changing fixed header
2. They help in overcoming size limitation on packets.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Extension headers are header that can be added to a packet for a new functionality. They allow appending new options without changing fixed header |
| `CE07_C2` | FULL | 1/1 | Extension headers are present between fixed header and payload. |
| `CE07_C3` | FULL | 1.5/1.5 | They allow appending new options without changing fixed header |

------------------------------------------------------------------------
### CE07_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 4** |
| System (no facets) | **1.75 / 4** |
| System (with facets) | 1.75 / 4 |
| abs err no-facets | 1.25 |

**Student answer**

```
Extension headers are optional fields in IPv6 address, placed between the header and the playload. The main advantage compared to IPv4 is that extension headers allow for extra information to be headed, overcaming the address size limitation
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | PARTIAL | 0.75/1.5 | extension headers allow for extra information to be headed |
| `CE07_C2` | FULL | 1/1 | placed between the header and the playload |
| `CE07_C3` | INCORRECT | 0/1.5 | The main advantage compared to IPv4 is that extension headers allow for extra information to be headed, overcaming the address size limitation |

------------------------------------------------------------------------
### CE07_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 3.25 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Extension headers are optional information/options that can be append without changing the fixed header.
the extension headers are located between the header and payload of a packet. 
thanks to the extension headers it is easier to overcome the size limitation
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Extension headers are optional information/options that can be append without changing the fixed header. |
| `CE07_C2` | FULL | 1/1 | the extension headers are located between the header and payload of a packet. |
| `CE07_C3` | FULL | 1.5/1.5 | Extension headers are optional information/options that can be append without changing the fixed header. |

------------------------------------------------------------------------
### CE07_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **4 / 4** |
| System (no facets) | **4 / 4** |
| System (with facets) | 4 / 4 |
| abs err no-facets | 0 |

**Student answer**

```
Extension headers are optional headers placed between fixed header and payload.
The advantages are the help to overcome size limitation and the possibility to append new options without changing the fixed header.
```

**Our check (skip_facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Extension headers are optional headers placed between fixed header and payload. The advantages are the help to overcome size limitation and the possibility to append new options without changing the fixed header. |
| `CE07_C2` | FULL | 1/1 | placed between fixed header and payload |
| `CE07_C3` | FULL | 1.5/1.5 | the possibility to append new options without changing the fixed header. |
