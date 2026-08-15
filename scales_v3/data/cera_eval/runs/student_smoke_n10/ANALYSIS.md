# System vs human — flat analysis

Excluded: CE02, CE09 (answer/gold issues).
Overall MAE excl CE02/CE09: **0.605** (n=80).

Order: remaining MAE worst-first.

**Marks legend**
- **Human evaluator marks** = SAF `normalized_grade` × question total (no per-concept human split).
- **Our system marks** = sum of CGR concept awards.

Note: CE04_C2 was under-crediting efficiency paraphrases (e.g. S10 “high efficency”); CQA broadened and those rows re-checked.

========================================================================

## CE08  |  MAE 0.80  |  total marks = 4

### Question

WHAT are the challenges of Mobile Routing compared to routing in fixed and wired networks? Please NAME and DESCRIBE two challenges.

### Reference

Possible Challenges:
1.Adaptation: The network has to handle the dynamic positioning of the nodes/topology changes. Additionally, nodes can leave or join the network anywhere (within signal range) at any time.
2.Security: Interception of packets or injection of faulty packages is easily possible in wireless networks. This may necessitate encryption and authentication.
3.Medium Access Control: Wireless networks feature new possibilities for inference and collisions of the transmitted signals.
4.Quality of Service (QoS): Due to the rapidly changing network topology, imprecise network information, and resource constraints of participating nodes, it is challenging to provide the desired QoS.
5.Scalability: Since it is not possible to know the number of participating nodes beforehand, it is vital that routing protocols are capable of dealing with increasing network sizes.
6.Power Consumption: As most mobile devices are battery-powered, power consumption becomes an important optimization factor.

### Our concepts

- `CE08_C1` (1, select_n, min=4): The student names at least four distinct mobile routing challenges from the catalog.
  - facets: ['Adaptation', 'Security', 'Medium Access Control', 'Quality of Service', 'Scalability', 'Power Consumption']
- `CE08_C2` (1.5, synonym_set): The student provides a valid description for the first chosen challenge.
  - facets: ['Adaptation: dynamic positioning or node mobility', 'Security: packet interception or injection', 'Medium Access Control: signal interference or collisions', 'Quality of Service: topology changes or resource constraints', 'Scalability: increasing network size', 'Power Consumption: battery-powered optimization']
- `CE08_C3` (1.5, synonym_set): The student provides a valid description for the second chosen challenge.
  - facets: ['Adaptation: dynamic positioning or node mobility', 'Security: packet interception or injection', 'Medium Access Control: signal interference or collisions', 'Quality of Service: topology changes or resource constraints', 'Scalability: increasing network size', 'Power Consumption: battery-powered optimization']

### Per-student

------------------------------------------------------------------------
### CE08_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 4** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Heterogeneity: In wireless network, capabilities, responsibilities, and constraints of nodes might be different. For instance, the battery life of mobile devices, the transmission range, the radios may be different. Thus, putting those conditions into consideration is important.   Fairness: Fairness might be an issue in fixed and wired networks. However, the drastic change in mobile network topology leads to difficulty in maintaining fairness.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | For instance, the battery life of mobile devices, the transmission range, the radios may be different. |
| `CE08_C3` | FULL | 1.5/1.5 | the drastic change in mobile network topology leads to difficulty in maintaining fairness. |

*Human evaluator total only: **3/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3.5 / 4** |
| Human raw / normalized (SAF 0–1) | 0.875 / 0.875 |
| **Our system marks** | **3.5 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The network no longer has an ether to which all nodes are connected. Instead each node has its own radius, where it can send and receive communication.  The differences and overlaps of various radius cause problems like the hidden terminal or exposed terminal.  Also, due to the node’s mobility, the networks topology can change rapidly. Which routes are optimal, or even possible, changes with that.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | the hidden terminal or exposed terminal.  Also, due to the node’s mobility, the networks topology can change rapidly. |
| `CE08_C2` | FULL | 1.5/1.5 | due to the node’s mobility, the networks topology can change rapidly. |
| `CE08_C3` | FULL | 1.5/1.5 | Also, due to the node’s mobility, the networks topology can change rapidly. |

*Human evaluator total only: **3.5/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
A first challenge is called Hidden Terminals. This means, that there might are nodes existing who can not hear each other. As a consequence like the example in the lecture collisions can be caused because two nodes who can not hear each other, might are communicating with one in between them, because one sends to the one in the middle. The other one doesn't know. Collision detection fails as well  A second challenge is "near and far terminals". Here the distance between nodes influences the strength of the signal. As a consequence the one who is closer to the communication partner drowns out the weaker one. This can cause further problems because the communication between two nodes is not working.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | As a consequence like the example in the lecture collisions can be caused because two nodes who can not hear each other, might are communicating with one in between them, because one sends to the one in the middle. |
| `CE08_C3` | FULL | 1.5/1.5 | A second challenge is "near and far terminals". Here the distance between nodes influences the strength of the signal. As a consequence the one who is closer to the communication partner drowns out the weaker one. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2 / 4** |
| Human raw / normalized (SAF 0–1) | 0.5 / 0.5 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | +1 |

**Student answer**

```
Two challenges are hidden terminals, which occurs when two nodes can communicate over the same AP but not directly to each other, and exposed terminals, which occurs when two devices want to transmit data at the same time, but encounter a channel interference.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | exposed terminals, which occurs when two devices want to transmit data at the same time, but encounter a channel interference. |
| `CE08_C3` | FULL | 1.5/1.5 | exposed terminals, which occurs when two devices want to transmit data at the same time, but encounter a channel interference. |

*Human evaluator total only: **2/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
HIDDEN TERMINALS: Node A and Node C can not receive message from each other, and they send messages to Node B simultaneously. But the transmission can conllide at Node B and both messages are lost, then Node A and Node C are hidden from each other. EXPOSED TERMINALS: Node A, D are outside of range of each other and in the miiddle Node B, C are inside of the range of each other. B sends to A currently and C wants to send to D. But C has to wait because it considers that it will has interference. However the transmission can take place as A is out of range of C. C is exposed to B.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | But the transmission can conllide at Node B and both messages are lost |
| `CE08_C3` | FULL | 1.5/1.5 | B sends to A currently and C wants to send to D. But C has to wait because it considers that it will has interference. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3.5 / 4** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Two of the many challenges of mobile routing compared to fixed / wired networks are Hidden Terminals and security issues. Hidden Terminal can occur, when the nodes are quite far apart, while some nodes are not able to detect nodes anymore, while more centered nodes are able to detect messages from both the distant nodes. Then the distant nodes are not able to detect collisions occuring in the „middle“ of the network at the centered nodes, because the signal is not transmitted over all network nodes. One of the security issues can be, that wifi is set up inside of a building. A normal ethernet network over cable would connect all the nodes inside, and then can be configured to discard all the internal packages at the outgoing router to the internet. A wifi network cannot be configured, to only nodes inside of the building are able to receive the packages. If the network is available outside of the building, then any node outside will be able to detect the network.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | Two of the many challenges of mobile routing compared to fixed / wired networks are Hidden Terminals and security issues. |
| `CE08_C2` | FULL | 1.5/1.5 | Then the distant nodes are not able to detect collisions occuring in the „middle“ of the network at the centered nodes, because the signal is not transmitted over all network nodes. |
| `CE08_C3` | FULL | 1.5/1.5 | If the network is available outside of the building, then any node outside will be able to detect the network. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3.5 / 4** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
(Due to the question in the forum, i will relate to slide 3, not to Challenges in Mobile Communications, which are on slide 10ff).

One basic challenge in Mobile Networking is the Power control: mobile devices have only a limited amount of power which should be used wisely and as little as possible.

In addition, the routing in Mobile Networking has to deal with a high amount of dynamic so it needs to find new routes as nodes move or conditions change.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | PARTIAL | 0.5/1 | One basic challenge in Mobile Networking is the Power control: mobile devices have only a limited amount of power which should be used wisely and as little as possible. In addition, the routing in Mobile Networking has to deal with a high amount of dynamic so it needs to find new routes as nodes … |
| `CE08_C2` | FULL | 1.5/1.5 | mobile devices have only a limited amount of power which should be used wisely and as little as possible. |
| `CE08_C3` | FULL | 1.5/1.5 | the routing in Mobile Networking has to deal with a high amount of dynamic so it needs to find new routes as nodes move or conditions change. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
Services Discovery is a challenge in Mobile Routing, since devices move around, so it becomes difficult to know where services are placed and how to be aware of them. Power control is also a challenge. In order for a device to have a certain range and suffer less interference, it needs a certain signal strength, which depends on the power.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | Services Discovery is a challenge in Mobile Routing, since devices move around, so it becomes difficult to know where services are placed and how to be aware of them. |
| `CE08_C3` | FULL | 1.5/1.5 | Power control is also a challenge. In order for a device to have a certain range and suffer less interference, it needs a certain signal strength, which depends on the power. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3.5 / 4** |
| Human raw / normalized (SAF 0–1) | 0.875 / 0.875 |
| **Our system marks** | **1.5 / 4** |
| Absolute error |sys−human| | 2 |
| Bias (sys−human) | -2 |

**Student answer**

```
One challenge is the hidden terminal problem. CSMA doesn't work in mobile networks because a node cant see the whole transmission medium. They can't detect if there is some other node sending,to the same destination, at the moment so the send to and cause a collision. An other challenge is the exposed terminal problem. It can happen that a node tells all other nodes in range not to send, to avoid collisions at their receiver. But some nodes then need to be silent even though they aren't even in range with the receiver of the other transmission and therefore can't create a collision. So the wait unnecessary and Utilization is lower than it could be.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | They can't detect if there is some other node sending,to the same destination, at the moment so the send to and cause a collision. |
| `CE08_C3` | ABSENT | 0/1.5 | — |

*Human evaluator total only: **3.5/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE08_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
One challenge in mobile routing is the so-called hidden terminal problem. As nodes have an inherently limited transmission range, different nodes in the network may be located to far from each other to directly be able to communicate. However, there can be other nodes in the intersection range of these nodes that can send and receive to/ from both sides, increasing the risk of transmission collisions from the hidden nodes. Also, the limited transmission range itself poses a challenge fro mobile routing as the signal strength of a sending node decreases proportionally to the square of the distance. Therefor, stronger signals from nearer nodes can completely overwrite weaker signals from more distant nodes.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE08_C1` | ABSENT | 0/1 | — |
| `CE08_C2` | FULL | 1.5/1.5 | However, there can be other nodes in the intersection range of these nodes that can send and receive to/ from both sides, increasing the risk of transmission collisions from the hidden nodes. |
| `CE08_C3` | FULL | 1.5/1.5 | However, there can be other nodes in the intersection range of these nodes that can send and receive to/ from both sides, increasing the risk of transmission collisions from the hidden nodes. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

========================================================================

## CE03  |  MAE 0.75  |  total marks = 4

### Question

What is the difference between asynchronous and synchronous transmission mode in the Data Link Layer.

### Reference

Asynchronous transmission: Every character a self-contained unit surrounded by a start bit and a stop bit, which is an easy and cheap pattern, but causes low transmission rates.

Synchronous transmission: Several characters pooled to a continuous stream of data (frames), Frames defined by SYN or flag, higher complexity, but higher transmission rates. Requires synchronization between sender and receiver.

### Our concepts

- `CE03_C1` (1, checklist): Mechanism of asynchronous transmission
  - facets: ['character as self-contained unit', 'surrounded by start and stop bits']
- `CE03_C2` (1, checklist): Mechanism of synchronous transmission
  - facets: ['pooled into continuous stream of data', 'frames defined by SYN or flag', 'requires synchronization between sender and receiver']
- `CE03_C3` (1, checklist): Trade-offs of asynchronous transmission
  - facets: ['easy and cheap pattern', 'low transmission rates']
- `CE03_C4` (1, checklist): Trade-offs of synchronous transmission
  - facets: ['higher complexity', 'higher transmission rates']

### Per-student

------------------------------------------------------------------------
### CE03_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3.5 / 4** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
In asynchronous transmission each character is bounded by a start and a stop bit. This is simple and inexpensive but has a low transmission. 
Synchronous transmission, sveral characters are put together to frames. This is more complex but has a higher transmission rate.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | In asynchronous transmission each character is bounded by a start and a stop bit. |
| `CE03_C2` | PARTIAL | 0.5/1 | sveral characters are put together to frames. |
| `CE03_C3` | FULL | 1/1 | This is simple and inexpensive but has a low transmission. |
| `CE03_C4` | FULL | 1/1 | This is more complex but has a higher transmission rate. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

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

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | -Each character bounded by a start bit and stop bit |
| `CE03_C2` | FULL | 1/1 | -Several characters pooled together to frames -Frames defined by Flag or SYN |
| `CE03_C3` | FULL | 1/1 | Simple, inexpensive, but low transmission rates |
| `CE03_C4` | FULL | 1/1 | More complex, but higher transmission rates |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

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

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | -Each character is bounded by a start bit and a stop bit |
| `CE03_C2` | FULL | 1/1 | -Several characters pooled to frames  -Frames defined by SYN or flag |
| `CE03_C3` | FULL | 1/1 | Simple + inexpensive, but low transmission rates |
| `CE03_C4` | FULL | 1/1 | More complex, but higher transmission rates |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
While in asynchronous transmission every character is bounded by a start and a end bit, in synchronous transmission several character are bound to frames, these frames are bound by SYN or flag. The asynchronous transmission is simple and inexpensive, but has a low transmission rate, up to 200 bit/sec, while the synchronous transmission has a higher transmission rate, but is more complex.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | in asynchronous transmission every character is bounded by a start and a end bit |
| `CE03_C2` | FULL | 1/1 | in synchronous transmission several character are bound to frames, these frames are bound by SYN or flag. |
| `CE03_C3` | FULL | 1/1 | The asynchronous transmission is simple and inexpensive, but has a low transmission rate |
| `CE03_C4` | FULL | 1/1 | the synchronous transmission has a higher transmission rate, but is more complex. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2 / 4** |
| Absolute error |sys−human| | 2 |
| Bias (sys−human) | -2 |

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

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | -works character by character -each character who should transmission has a start and stop bit |
| `CE03_C2` | FULL | 1/1 | -several characters pooled to frames -the frames where defined by SYN or flag |
| `CE03_C3` | ABSENT | 0/1 | — |
| `CE03_C4` | ABSENT | 0/1 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 4** |
| Absolute error |sys−human| | 1.5 |
| Bias (sys−human) | -1.5 |

**Student answer**

```
In an asynchronous transmission each byte is sent separately and has a start and an end bit.
In a synchronous transmission data is sent in frames which can lead to higher transmission rates but becomes more complex.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | In an asynchronous transmission each byte is sent separately and has a start and an end bit. |
| `CE03_C2` | PARTIAL | 0.5/1 | In a synchronous transmission data is sent in frames |
| `CE03_C3` | ABSENT | 0/1 | — |
| `CE03_C4` | FULL | 1/1 | can lead to higher transmission rates but becomes more complex. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
Synchronous Data transmission means that many characters/symbols are transferred within a frame while asynchronous transmission transfers the data byte wise /character wise each, so the data is not collected into a frame. Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start is slowing down the speed especially in fast transmission.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | asynchronous transmission transfers the data byte wise /character wise each, so the data is not collected into a frame. Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start |
| `CE03_C2` | PARTIAL | 0.5/1 | Synchronous Data transmission means that many characters/symbols are transferred within a frame |
| `CE03_C3` | FULL | 1/1 | Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start is slowing down the speed |
| `CE03_C4` | PARTIAL | 0.5/1 | Asynchronous is definitely simpler but the permanent needed start, stop and time gap in between a stop and the next start is slowing down the speed especially in fast transmission. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2 / 4** |
| Absolute error |sys−human| | 2 |
| Bias (sys−human) | -2 |

**Student answer**

```
Asynchronous mode:
Each character is bounded by a start bit and a stop bit.

Synchronous mode:
Several characters are pooled to one frame which is defined by a SYN or a flag.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | Each character is bounded by a start bit and a stop bit. |
| `CE03_C2` | FULL | 1/1 | Several characters are pooled to one frame which is defined by a SYN or a flag. |
| `CE03_C3` | ABSENT | 0/1 | — |
| `CE03_C4` | ABSENT | 0/1 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3.5 / 4** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
With asynchronous transmission, each transmitted character is send together with one start bit and stop bit.
With synchronous transmission, several characters are send together as a frame, defined with special flags (SYN) at the beginning and the end of each frame. 
Asynchronous transmission is simpler, but does only allow for slow data transmission rates compared to the synchronous transmission mode.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | each transmitted character is send together with one start bit and stop bit. |
| `CE03_C2` | FULL | 1/1 | With synchronous transmission, several characters are send together as a frame, defined with special flags (SYN) at the beginning and the end of each frame. |
| `CE03_C3` | FULL | 1/1 | Asynchronous transmission is simpler, but does only allow for slow data transmission rates compared to the synchronous transmission mode. |
| `CE03_C4` | PARTIAL | 0.5/1 | Asynchronous transmission is simpler, but does only allow for slow data transmission rates compared to the synchronous transmission mode. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE03_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Asynchronous transmission bound each character by a start bit and a stop bit. It is simple and effective, however, it has low transmission rates, 200bit/sec. 

Synchronous Transmission has several characters pooled to frames, each frame define by SYN or Flag, it is complex but has higher transmission rates than asynchronous transmission.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE03_C1` | FULL | 1/1 | Asynchronous transmission bound each character by a start bit and a stop bit. |
| `CE03_C2` | FULL | 1/1 | Synchronous Transmission has several characters pooled to frames, each frame define by SYN or Flag |
| `CE03_C3` | FULL | 1/1 | It is simple and effective, however, it has low transmission rates |
| `CE03_C4` | FULL | 1/1 | it is complex but has higher transmission rates than asynchronous transmission. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

========================================================================

## CE10  |  MAE 0.72  |  total marks = 5

### Question

In the lecture you have learned about congestion control with TCP. Name the 2 phases of congestion control and explain how the Congestion Window (cwnd) and the Slow Start Threshold (ss_thresh) change in each phase (after initialization, where cwnd = 1 and ss_thresh = advertised window size) in 1-4 sentences total.

### Reference

Slow start (cwnd less than ss_thresh):
In the slow start phase, cwnd is incremented by one every time a segment is acknowledged. This results in an exponential growth as cwnd is essentially doubled after each Round Trip Time (RTT). This is done until either a packet is lost or ss_thresh is reached. When cwnd >= ss_thresh, the congestion avoidance phase is entered.
After a packet is lost / congestion the following adaption is made in both phases: ss_thresh = cwnd / 2. Then cwnd is reset to 1.

Congestion Avoidance (cwnd >= ss_thresh):
In the congestion avoidance phase, cwnd is incremented more slowly. There are different incrementation strategies, but they usually grow linearly, e.g. only increment cwnd by 1 after all sent segments have been acknowledged. This is done until a packet is lost. Typically, this means that cwnd less than ss_thresh and the slow start phase is entered again.
After a packet is lost / congestion the following adaption is made in both phases: ss_thresh = cwnd / 2. Then cwnd is reset to 1.

### Our concepts

- `CE10_C1` (1, checklist): The student identifies the two phases of TCP congestion control as Slow Start and Congestion Avoidance.
  - facets: ['Slow Start', 'Congestion Avoidance']
- `CE10_C2` (2, synonym_set): The student explains that in the Slow Start phase, the congestion window (cwnd) grows exponentially.
  - facets: ['cwnd incremented by one per segment acknowledged', 'exponential growth', 'doubled after each RTT']
- `CE10_C3` (2, synonym_set): The student explains that in the Congestion Avoidance phase, the congestion window (cwnd) grows linearly.
  - facets: ['cwnd grows linearly', 'increment cwnd by 1 after all sent segments acknowledged']

### Per-student

------------------------------------------------------------------------
### CE10_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **5 / 5** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **5 / 5** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Phase 1： Slow Start.
Phase 2:  Congestion avoidance.

When cwnd < ss_thresh: cwnd increases rate exponentially. 
When cwnd >=ss_thresh: TCP slows down the increase of cwnd. Cwnd increases additively(i.e. cwdn ++);
When timeout, ss_thresh is set to half of the current value of cwnd, and cwnd is set to 1. The whole proccess start from Slow Start again.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1： Slow Start. Phase 2:  Congestion avoidance. |
| `CE10_C2` | FULL | 2/2 | When cwnd < ss_thresh: cwnd increases rate exponentially. |
| `CE10_C3` | FULL | 2/2 | Cwnd increases additively(i.e. cwdn ++); |

*Human evaluator total only: **5/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3.75 / 5** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **3 / 5** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
1. Slow start: Each time a segment is acknowledged cwnd is incremented by one. Continues until cwnd reaches ss_thresh or a packet gets lost. 2. Congestion Avoidance If congestions occurs ss_thresh is set to 50% of the current cwnd an the new cwnd is set to one. Then the slow start is entered.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | 1. Slow start: Each time a segment is acknowledged cwnd is incremented by one. Continues until cwnd reaches ss_thresh or a packet gets lost. 2. Congestion Avoidance |
| `CE10_C2` | FULL | 2/2 | Each time a segment is acknowledged cwnd is incremented by one. |
| `CE10_C3` | ABSENT | 0/2 | — |

*Human evaluator total only: **3.75/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4.4 / 5** |
| Human raw / normalized (SAF 0–1) | 0.88 / 0.88 |
| **Our system marks** | **3 / 5** |
| Absolute error |sys−human| | 1.4 |
| Bias (sys−human) | -1.4 |

**Student answer**

```
The phases are slow start and congestion avoidance.
In the slow phase, the cwnd starts getting bigger in size, first slowly, then rapidly, until the ssthresh is reached. Once reached, the congestion control phase begins, where the cwnd slowly grows in size until a congestion occurs (timeout). In this case the slow start phase is entered again, the cwnd is reset and a new ssthresh is calculated (half of reached cwnd before timeout.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | The phases are slow start and congestion avoidance. |
| `CE10_C2` | PARTIAL | 1/2 | In the slow phase, the cwnd starts getting bigger in size, first slowly, then rapidly, until the ssthresh is reached. |
| `CE10_C3` | PARTIAL | 1/2 | Once reached, the congestion control phase begins, where the cwnd slowly grows in size until a congestion occurs (timeout). |

*Human evaluator total only: **4.4/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2.5 / 5** |
| Human raw / normalized (SAF 0–1) | 0.5 / 0.5 |
| **Our system marks** | **3 / 5** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | +0.5 |

**Student answer**

```
Phase 1 (Slow Start):  cwnd++ for each acknowledged segmentPhase 2 (Congestion Avoidance):  ss_thresh = cwnd / 2  cwnd = 1
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1 (Slow Start):  cwnd++ for each acknowledged segmentPhase 2 (Congestion Avoidance):  ss_thresh = cwnd / 2  cwnd = 1 |
| `CE10_C2` | FULL | 2/2 | cwnd++ for each acknowledged segment |
| `CE10_C3` | INCORRECT | 0/2 | Phase 2 (Congestion Avoidance):  ss_thresh = cwnd / 2  cwnd = 1 |

*Human evaluator total only: **2.5/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4.4 / 5** |
| Human raw / normalized (SAF 0–1) | 0.88 / 0.88 |
| **Our system marks** | **5 / 5** |
| Absolute error |sys−human| | 0.6 |
| Bias (sys−human) | +0.6 |

**Student answer**

```
Phase 1 (Slow Start)Phase 2 (Congestion Avoidance)The congestion Window is increased exponentially. After the cwnd >= ss_resh, the phase 2 starts and the cwnd is increased linear over time. If a congestion happens, cwnd is set again to 1 and ss_tresh is set to half the cwnd at the time of the congestion. With these new values, the phase 1 starts again.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1 (Slow Start)Phase 2 (Congestion Avoidance) |
| `CE10_C2` | FULL | 2/2 | The congestion Window is increased exponentially. |
| `CE10_C3` | FULL | 2/2 | the cwnd is increased linear over time |

*Human evaluator total only: **4.4/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3.12 / 5** |
| Human raw / normalized (SAF 0–1) | 0.625 / 0.625 |
| **Our system marks** | **5 / 5** |
| Absolute error |sys−human| | 1.88 |
| Bias (sys−human) | +1.88 |

**Student answer**

```
Phase 1: Slow start (getting to equilibrium) Phase 2: Congestion Avoidance In the Slow Start phase each time when a segment is acknowledged cwnd gets incremented by one until we reach ss_thresh or have packet loss. So in the slow start phase its always cwnd less than ss_tresh and when cwnd >= ss_tresh the increase of cwnd slows down. In the Phase of Congestion Avoidance, when we have a timeout, ss_tresh is set to 50% of the current size of the congestion window, cwnd gets reset to one and we enter slow-start.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1: Slow start (getting to equilibrium) Phase 2: Congestion Avoidance |
| `CE10_C2` | FULL | 2/2 | cwnd size grows very rapidy (doubles after every RTT) |
| `CE10_C3` | FULL | 2/2 | Phase 2: cwnd size grows no longer exponentially, but linearly from ss_tresh on to gain as much bandwith as possible. |

*Human evaluator total only: **3.12/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4.4 / 5** |
| Human raw / normalized (SAF 0–1) | 0.88 / 0.88 |
| **Our system marks** | **5 / 5** |
| Absolute error |sys−human| | 0.6 |
| Bias (sys−human) | +0.6 |

**Student answer**

```
Phase 1: Slow start
The sender sends as much segemnts as specified in cwnd and for each ACK received, cwnd is increased by one. This exponential growth continues until the ss_thresh is reached.
Phase 2: Congestion avoidance
In the congestion avoidance phase the cwnd is only increased by one per roundtrip time. If a timeout (= congestion) occurs the ss_tresh is set to cwnd/2 and cwnd is reset to 1.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1: Slow start ...  Phase 2: Congestion avoidance |
| `CE10_C2` | FULL | 2/2 | for each ACK received, cwnd is increased by one. This exponential growth continues until the ss_thresh is reached. |
| `CE10_C3` | FULL | 2/2 | In the congestion avoidance phase the cwnd is only increased by one per roundtrip time. |

*Human evaluator total only: **4.4/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4.4 / 5** |
| Human raw / normalized (SAF 0–1) | 0.88 / 0.88 |
| **Our system marks** | **3 / 5** |
| Absolute error |sys−human| | 1.4 |
| Bias (sys−human) | -1.4 |

**Student answer**

```
Phase one is slow start and phase two is congestion avoidance, cwnd starts at 1, and will rapidly grow until the value reached ss_thresh, after that cwnd will grow slowly, when a timeout occured, set ss_thresh to 50% of the current cwnd and cwnd is reset to one, then start over from slow start.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase one is slow start and phase two is congestion avoidance |
| `CE10_C2` | PARTIAL | 1/2 | cwnd starts at 1, and will rapidly grow until the value reached ss_thresh |
| `CE10_C3` | PARTIAL | 1/2 | after that cwnd will grow slowly |

*Human evaluator total only: **4.4/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3.75 / 5** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **3 / 5** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
Phase 1 ist slow start. The initial value of cwnd is 1, ss_thresh is the advertised window size. Each time a segment is acknowledged cwnd is inreased by one, until cwnd >= ss_thresh or packet loss, then Phase 2: Congestion Avoidance is entered.
In Congestion Avoidance each time a congestion occurs: ss_thresh = cwnd / 2 and cwnd = 1 and slow start is entered.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | Phase 1 ist slow start. ... then Phase 2: Congestion Avoidance is entered. |
| `CE10_C2` | FULL | 2/2 | Each time a segment is acknowledged cwnd is inreased by one |
| `CE10_C3` | ABSENT | 0/2 | — |

*Human evaluator total only: **3.75/5** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE10_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **5 / 5** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **5 / 5** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The first phase, slow start, will double cwnd every round-trip time by increasing it by 1 for each received ACK. When cwnd reaches ss_thresh, the congestion avoidance phase is entered. The congestion avoidance phase will additively increase cwnd by 1 every round-trip time.If congestion is encountered in any of the phases, ss_thresh is set to half the value of cwnd, cwnd is set to 1 and the slow start phase is entered.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE10_C1` | FULL | 1/1 | The first phase, slow start, will double cwnd every round-trip time by increasing it by 1 for each received ACK. When cwnd reaches ss_thresh, the congestion avoidance phase is entered. |
| `CE10_C2` | FULL | 2/2 | The first phase, slow start, will double cwnd every round-trip time by increasing it by 1 for each received ACK. |
| `CE10_C3` | FULL | 2/2 | The congestion avoidance phase will additively increase cwnd by 1 every round-trip time. |

*Human evaluator total only: **5/5** (no per-concept human split in SAF).*

========================================================================

## CE01  |  MAE 0.50  |  total marks = 3

### Question

Name the 3 service classes the Data Link Layer offers and explain the differences between the classes.

### Reference

1.unconfirmed connectionless - no ACK, loss of data possible, no flow control, no connect or disconnect.
2.confirmed connectionless - with ACK, no loss of data (timeout and retransmit instead→ duplicates and sequence errors possible), no flow control, no connect or disconnect.
3.connection-oriented - no data loss, duplication or sequencing errors. Instead a 3 phased communication with connect and disconnect, and flow control

### Our concepts

- `CE01_C1` (1.5, checklist): Identify the three service classes offered by the Data Link Layer
  - facets: ['unconfirmed connectionless', 'confirmed connectionless', 'connection-oriented']
- `CE01_C2` (0.5, checklist): Describe the distinguishing properties of unconfirmed connectionless service
  - facets: ['no ACK', 'loss of data possible', 'no flow control', 'no connect or disconnect']
- `CE01_C3` (0.5, checklist): Describe the distinguishing properties of confirmed connectionless service
  - facets: ['with ACK', 'no loss of data', 'duplicates and sequence errors possible', 'no flow control', 'no connect or disconnect']
- `CE01_C4` (0.5, checklist): Describe the distinguishing properties of connection-oriented service
  - facets: ['no data loss', 'no duplication or sequencing errors', '3 phased communication with connect and disconnect', 'flow control']

### Per-student

------------------------------------------------------------------------
### CE01_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.25 / 3** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
1. Unconfirmed connectionless service: transmission of isolated, idependent units without acknowledgement, possible loss of data / no flow control
2. Confirmed connectionless service: transmission with acknowledgement with no loss, has timeouts and retransmission / no flow control
3. Connection-oriented service:  connection over error free channel with a flow control
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | 1. Unconfirmed connectionless service: transmission of isolated, idependent units without acknowledgement, possible loss of data / no flow control 2. Confirmed connectionless service: transmission with acknowledgement with no loss, has timeouts and retransmission / no flow control 3. Connection-o… |
| `CE01_C2` | PARTIAL | 0.25/0.5 | transmission of isolated, idependent units without acknowledgement, possible loss of data / no flow control |
| `CE01_C3` | PARTIAL | 0.25/0.5 | 2. Confirmed connectionless service: transmission with acknowledgement with no loss, has timeouts and retransmission / no flow control |
| `CE01_C4` | PARTIAL | 0.25/0.5 | 3. Connection-oriented service:  connection over error free channel with a flow control |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.25 / 3** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
three service classes are:
1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error

2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible
,has sequencing error
3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | three service classes are: 1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error  2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible ,has sequencing error 3.Connection-Ori… |
| `CE01_C2` | PARTIAL | 0.25/0.5 | no flow control,connection less,loss of data happens |
| `CE01_C3` | PARTIAL | 0.25/0.5 | 2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible ,has sequencing error |
| `CE01_C4` | PARTIAL | 0.25/0.5 | 3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 3** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The three services are called Unconfirmed Connectionless Service, Confirmed Connectionless Service and Connection-Oriented Service. These differ in their characteristics and areas of application. The first two services differ in whether or not the receiver acknowledges a packet when it receives it. The Unconfirmed Connectionless service does not include confirmation and assumes that the sent packets have arrived correctly. By confirming in the Confirmed Connectionless  service, this service can ensure that all packets have arrived at the receiver. Lost packets cannot be confirmed and so the recipient sends the packet again after a specified timeout. Both mentioned services have no flow control and no explicit requests to establish or disconnect a connection. The Confirmed Connectionless service has an implicit confirmation if a connection can be established, exactly when its packets are confirmed by the receiver. The confirmation of the second service class can cause duplicates to appear at the receiver, when the confirmation of a packet does not arrive at the sender. The third service class executes a three-phase communication and tries to establish a connection first. If the connection is confirmed, packets are sent until a request for disconnection is sent and confirmed. If the communication takes place over an error-free channel, no losses, no duplicates and no sequence errors are to be expected. Flow control is guaranteed by the "handshake". The first service type is usually used for the transition of isolated single units in channels with very low error rate (e.g. LANs, voice communication). The second service type can be used for channels with a high error rate such as mobile communication. The last service type is preferred for long and persistent communication.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | The three services are called Unconfirmed Connectionless Service, Confirmed Connectionless Service and Connection-Oriented Service. |
| `CE01_C2` | FULL | 0.5/0.5 | The Unconfirmed Connectionless service does not include confirmation and assumes that the sent packets have arrived correctly. ... Both mentioned services have no flow control and no explicit requests to establish or disconnect a connection. |
| `CE01_C3` | FULL | 0.5/0.5 | By confirming in the Confirmed Connectionless  service, this service can ensure that all packets have arrived at the receiver. . . Both mentioned services have no flow control and no explicit requests to establish or disconnect a connection. . . The confirmation of the second service class can ca… |
| `CE01_C4` | FULL | 0.5/0.5 | The third service class executes a three-phase communication and tries to establish a connection first. If the connection is confirmed, packets are sent until a request for disconnection is sent and confirmed. If the communication takes place over an error-free channel, no losses, no duplicates a… |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.25 / 3** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
L2 Service Class “Unconfirmed Connectionless Service”: Transmission of isolated, independent units (frames). The data may be lost.
L2 Service Class “Confirmed Connectionless Service”: Each single frame is acknowledged so there is no loss. Timeout and retransmit if the sender does not receive an acknowledgement within a certain time frame. Duplicates and sequence errors may happen due to “retransmit”.
L2 Service Class “Connection-Oriented Service”: Three-phased communication: 1. Connection 2. Data Transfer 3. Disconnection. Hence no loss, no duplication, no sequencing error.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | L2 Service Class “Unconfirmed Connectionless Service”: Transmission of isolated, independent units (frames). The data may be lost. L2 Service Class “Confirmed Connectionless Service”: Each single frame is acknowledged so there is no loss. Timeout and retransmit if the sender does not receive an a… |
| `CE01_C2` | PARTIAL | 0.25/0.5 | Transmission of isolated, independent units (frames). The data may be lost. |
| `CE01_C3` | PARTIAL | 0.25/0.5 | Each single frame is acknowledged so there is no loss. Timeout and retransmit if the sender does not receive an acknowledgement within a certain time frame. Duplicates and sequence errors may happen due to “retransmit”. |
| `CE01_C4` | PARTIAL | 0.25/0.5 | Three-phased communication: 1. Connection 2. Data Transfer 3. Disconnection. Hence no loss, no duplication, no sequencing error. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 3** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
three service classes are:
1.Unconfirmed Connection less Service :no flow control,connection less,loss of data happens,no duplicates,no sequencing error

2.Confirmed Connection less Service :no flow control,connection less,no loss of data,duplicates possible
,has sequencing error
3.Connection-Oriented Service -flow control -connection oriented -no loss of data -no duplicates -no sequencing error
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | Unconfirmed Connection less Service: - Transmission of isolated, independent Frames - Loss of Data possible - No flow control - No connect or disconnect Confirmed Connectionless Service: - No loss of Data (acknowledged transfer) - Timeout and retransmit (if sender does not receive ACK)     - Dupl… |
| `CE01_C2` | FULL | 0.5/0.5 | - Loss of Data possible - No flow control - No connect or disconnect |
| `CE01_C3` | FULL | 0.5/0.5 | Confirmed Connectionless Service: - No loss of Data (acknowledged transfer) - Timeout and retransmit (if sender does not receive ACK)     - Duplicates and sequence errors possible, due to retransmits - No flow control - No connect or disconnect |
| `CE01_C4` | FULL | 0.5/0.5 | Connection-Oriented Service: - No loss of Data - No duplication, no sequencing error - Flow control - 3-phase communication (Connect, Transfer, Disconnect) |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.25 / 3** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
Unconfirmed connectionless service: Data is sent directly and no acknowledgements are returned
Confirmed Connectionless service: Data is sent directly and acknowledgements are returned by the receiver when the data has arrived. If the sender does not receive an acknowledgement with a defined time interval, the data is retransmitted.
Connectionoriented service: Three phases of communication: 1. The connection is initialized by exchanging parameters 2. data is transferred 3. Connection is closed due to that flow control is possible in this case.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | Unconfirmed connectionless service: Data is sent directly and no acknowledgements are returned Confirmed Connectionless service: Data is sent directly and acknowledgements are returned by the receiver when the data has arrived. If the sender does not receive an acknowledgement with a defined time… |
| `CE01_C2` | PARTIAL | 0.25/0.5 | Data is sent directly and no acknowledgements are returned |
| `CE01_C3` | PARTIAL | 0.25/0.5 | Confirmed Connectionless service: Data is sent directly and acknowledgements are returned by the receiver when the data has arrived. If the sender does not receive an acknowledgement with a defined time interval, the data is retransmitted. |
| `CE01_C4` | PARTIAL | 0.25/0.5 | Three phases of communication: 1. The connection is initialized by exchanging parameters 2. data is transferred 3. Connection is closed due to that flow control is possible in this case. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
For the Data Link Layer there are 3 service classes: unconfirmed conn.less service, confirmed conn.less service and connection-oriented service. 
In unconfirmed conn.less service a data is sent to receiver. In this case a sender does not know if the sent data has arrived at the receiver. In other words, we don't get any confirmation from the receiver about arrived data. In case of loss data the data will be not resend. If any Correct data arrives, there is no correcting mechanism implemented.
Confirmed conn.less service is a bidirectional communication between sender and receiver. After a sender sends a frame, a receiver sends an acknowledgement as answer. In the case of loss data a frame will be retransmit (after timeout) as long as the sender gets an acknowledgement from the receiver. In confirmed conn.less service there is no flow control implemented. 
In the last kind of service, connection-oriented service, a connection between parties has to be estabilished firstly before we can send any data. We speak of 3-phased communication: connection estabilishment (a sender sends a request to receiver, the receiver confirms it); data transfer (after the receiver gets a frame, sends an acknowledgement to the sender); disconnection (analog to connection estabilishment). In connection-oriented service there is flow control implemented.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | For the Data Link Layer there are 3 service classes: unconfirmed conn.less service, confirmed conn.less service and connection-oriented service. |
| `CE01_C2` | PARTIAL | 0.25/0.5 | In this case a sender does not know if the sent data has arrived at the receiver. In other words, we don't get any confirmation from the receiver about arrived data. In case of loss data the data will be not resend. |
| `CE01_C3` | PARTIAL | 0.25/0.5 | After a sender sends a frame, a receiver sends an acknowledgement as answer. In the case of loss data a frame will be retransmit (after timeout) as long as the sender gets an acknowledgement from the receiver. In confirmed conn.less service there is no flow control implemented. |
| `CE01_C4` | FULL | 0.5/0.5 | We speak of 3-phased communication: connection estabilishment (a sender sends a request to receiver, the receiver confirms it); data transfer (after the receiver gets a frame, sends an acknowledgement to the sender); disconnection (analog to connection estabilishment). In connection-oriented serv… |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
1.unconfirmed connection-less service 2.confirmed connection-less service 3.connection-oriented service.
2. there is flow-control in connection-oriented service. But in other two there's no flow-control, no connect or disconnect.
There is no loss, no duplication, no sequencing error in connection-oriented service.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | 1.unconfirmed connection-less service 2.confirmed connection-less service 3.connection-oriented service. |
| `CE01_C2` | PARTIAL | 0.25/0.5 | But in other two there's no flow-control, no connect or disconnect. |
| `CE01_C3` | PARTIAL | 0.25/0.5 | But in other two there's no flow-control, no connect or disconnect. |
| `CE01_C4` | FULL | 0.5/0.5 | there is flow-control in connection-oriented service. But in other two there's no flow-control, no connect or disconnect. There is no loss, no duplication, no sequencing error in connection-oriented service. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.25 / 3** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
Here are the 3 service classes the data link layer offers: 

1) Unconfirmed connectionLess Service: there is no "connect and disconnect" between sender and receiver. There is no flow control or error management

2) Confirmed connectionLess Service: There is no "connect and disconnect", there is no flow control but there is an acknowledgment for each frame sent. 

3) Connection oriented Service: there is a flow control and a "connect and disconnect" protocol between the sender and the receiver
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | FULL | 1.5/1.5 | 1) Unconfirmed connectionLess Service: there is no "connect and disconnect" between sender and receiver. There is no flow control or error management  2) Confirmed connectionLess Service: There is no "connect and disconnect", there is no flow control but there is an acknowledgment for each frame … |
| `CE01_C2` | PARTIAL | 0.25/0.5 | 1) Unconfirmed connectionLess Service: there is no "connect and disconnect" between sender and receiver. There is no flow control or error management |
| `CE01_C3` | PARTIAL | 0.25/0.5 | 2) Confirmed connectionLess Service: There is no "connect and disconnect", there is no flow control but there is an acknowledgment for each frame sent. |
| `CE01_C4` | PARTIAL | 0.25/0.5 | 3) Connection oriented Service: there is a flow control and a "connect and disconnect" protocol between the sender and the receiver |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE01_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **0 / 3** |
| Human raw / normalized (SAF 0–1) | 0 / 0 |
| **Our system marks** | **0.25 / 3** |
| Absolute error |sys−human| | 0.25 |
| Bias (sys−human) | +0.25 |

**Student answer**

```
1. Flow Control: ensures that a transmitter does not send faster than a receiver can receive
2. Framing: data are packed in a frame, this frame contains e.g. the data, destination address and source 
3. Error Detection: important to ensure that all data has been received correctly. If an error is detected, the receiver may be signalled to send the data again
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE01_C1` | ABSENT | 0/1.5 | — |
| `CE01_C2` | ABSENT | 0/0.5 | — |
| `CE01_C3` | ABSENT | 0/0.5 | — |
| `CE01_C4` | PARTIAL | 0.25/0.5 | 1. Flow Control: ensures that a transmitter does not send faster than a receiver can receive |

*Human evaluator total only: **0/3** (no per-concept human split in SAF).*

========================================================================

## CE04  |  MAE 0.50  |  total marks = 3

### Question

What is "frame bursting"? Also, give 1 advantage and disadvantage compared to the carrier extension.

### Reference

Frame bursting reduces the overhead for transmitting small frames by concatenating a sequence of multiple frames in one single transmission, without ever releasing control of the channel.
Advantage: it is more efficient than carrier extension as single frames not filled up with garbage.
Disadvantage: need frames waiting for transmission or buffering and delay of frames

### Our concepts

- `CE04_C1` (1, select_n, min=2): Define frame bursting as concatenating multiple frames into one transmission without releasing the channel.
  - facets: ['concatenating a sequence of multiple frames', 'one single transmission', 'without ever releasing control of the channel']
- `CE04_C2` (1, synonym_set): Identify the advantage of frame bursting over carrier extension regarding efficiency.
  - facets: ['more efficient / higher efficiency than carrier extension', 'higher transmission rate or improved throughput', 'more user data / not filled with garbage or padding']
- `CE04_C3` (1, synonym_set): Identify the disadvantage of frame bursting regarding transmission requirements or delay.
  - facets: ['need frames waiting for transmission', 'buffering', 'delay of frames']

### Per-student

------------------------------------------------------------------------
### CE04_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Frame bursting allow sender to transmit a Concatenated sequence of multiple frames in a single transmission. It has better efficiency however it needs frames waiting for transmission.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | transmit a Concatenated sequence of multiple frames in a single transmission |
| `CE04_C2` | FULL | 1/1 | It has better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Sending multiple different frames concatenated to each other is called frame bursting. Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. Carrier extension extends the message with unused bits which lower the efficiency.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Sending multiple different frames concatenated to each other is called frame bursting. |
| `CE04_C2` | FULL | 1/1 | However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. Carrier extension extends the message with unused bits which lower the efficiency. |
| `CE04_C3` | FULL | 1/1 | Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Frame Bursting allows sender to transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission.

Advantage as compared to carrier extension is:
-Better efficiency

Disadvantage as compared to carrier extension is:
-it needs frames waiting for transmission
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission |
| `CE04_C2` | FULL | 1/1 | -Better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Frame bursting is a way to increase the speeds of the ethernet protocol in the shared broadcast mode. To meet the minimum frame length requirements at the greater speeds multiple frames are concatenated to a single, larger frame. This allows to detect collisions with faster speeds at the cost of a delay when sending a larger frame. One advantage over the carrier extension is the improved throughput, at the cost of an increased latency (disadvantage).
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | multiple frames are concatenated to a single, larger frame. |
| `CE04_C2` | FULL | 1/1 | One advantage over the carrier extension is the improved throughput |
| `CE04_C3` | FULL | 1/1 | at the cost of an increased latency (disadvantage) |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2.25 / 3** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **1.5 / 3** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
In frame bursting, the sender can transmit multiple frames by concatenating them in single transmission.
The carrier extension provides really low efficiency with only 46byte  user data being transmitted using 512 byte.
Whereas the frame bursting provides a much better performance.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | the sender can transmit multiple frames by concatenating them in single transmission. |
| `CE04_C2` | FULL | 1/1 | Whereas the frame bursting provides a much better performance. |
| `CE04_C3` | ABSENT | 0/1 | — |

*Human evaluator total only: **2.25/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Sender collects and concatenates sequence of multiple frames to send it with single transmission.
+ better efficiency
Disadvantage: needs frames waiting for transmission
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Sender collects and concatenates sequence of multiple frames to send it with single transmission. |
| `CE04_C2` | FULL | 1/1 | + better efficiency |
| `CE04_C3` | FULL | 1/1 | needs frames waiting for transmission |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2.25 / 3** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.25 |
| Bias (sys−human) | +0.25 |

**Student answer**

```
In frame bursting, instead of the sender sending one packet at a time, it sends ten packets at once. The sender waits for the packets until it has ten packets ready to send. Put them together and just then send them.

Advantage: better performance than carrier extension, since more data is sent at a time.

Disadvantage: if there are only one or two packets to send, the sender will be waiting for the remain, to reach the 10 packets. If there are not 10 packets, after a timeout, the sender adds rubbish to the frame (so it has the needed size). So, the packets will be sent with a delay and with unnecessary data.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Put them together and just then send them. |
| `CE04_C2` | FULL | 1/1 | better performance than carrier extension, since more data is sent at a time. |
| `CE04_C3` | FULL | 1/1 | So, the packets will be sent with a delay and with unnecessary data. |

*Human evaluator total only: **2.25/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
To be able to transmit data over lager distances at higher speed and still avoiding collisions you send bigger sequences by collecting several packets and sending them all together.

Advantage: You have a higher efficiency compared to carrier extension. You have a minimum of 70 percent (frame size 64 byte and user data 46 byte) user data compared to a minimum 9 percent of.

Disadvantage: You have a delay in time while waiting for other packets until you have collected enough to send.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | collecting several packets and sending them all together |
| `CE04_C2` | FULL | 1/1 | You have a higher efficiency compared to carrier extension. |
| `CE04_C3` | FULL | 1/1 | You have a delay in time while waiting for other packets until you have collected enough to send. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Using "frame bursting", multiple frames are concatenated sequentially and sent at once. An advange is the higher efficiency compared to "carrier extension", because using "carrier extension", the minimum frame size is increased to 512 byte and filled up with garbage. As a result only ~10% of bytes being sent is used by data. An disadvantage occurres, when the station does not have enough frames to sent, so there might be a delay when waiting for frames to sent. If there is none, padding frames might be sent, but there is still a delay or timeout.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | multiple frames are concatenated sequentially and sent at once |
| `CE04_C2` | FULL | 1/1 | An advange is the higher efficiency compared to "carrier extension", because using "carrier extension", the minimum frame size is increased to 512 byte and filled up with garbage. |
| `CE04_C3` | FULL | 1/1 | so there might be a delay when waiting for frames to sent. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE04_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 3** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2.5 / 3** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
Frame Bursting is a procedure in which many frames are buffered until a specific amount is reached. Then, they are concatenated and sent altogether. This is done to increase the overall frame length.
An advantage is a higher transmission rate with a high efficency. 
A disadvantage is a long/high delay because the sender must wait for the specific amount of frames.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Then, they are concatenated and sent altogether. |
| `CE04_C2` | FULL | 1/1 | An advantage is a higher transmission rate with a high efficency. |
| `CE04_C3` | FULL | 1/1 | A disadvantage is a long/high delay because the sender must wait for the specific amount of frames. |

*Human evaluator total only: **3/3** (no per-concept human split in SAF).*

========================================================================

## CE05  |  MAE 0.50  |  total marks = 4

### Question

What are the objectives of IPv6? Please state at least 4 objectives.

### Reference

To support billions of end-systems.
To reduce routing tables.
To simplify protocol processing with Simplified header.
To increase security.
To support real time data traffic (quality of service).
Flow label, traffic class.
To provide multicasting.
To support mobility (roaming).
To be open for change (future): extension headers for additional change incorporation.
To coexistence with existing protocols.

### Our concepts

- `CE05_C1` (1, synonym_set): State the first IPv6 objective
  - facets: ['support billions of end-systems', 'reduce routing tables']
- `CE05_C2` (1, synonym_set): State the second IPv6 objective
  - facets: ['simplify protocol processing', 'increase security']
- `CE05_C3` (1, synonym_set): State the third IPv6 objective
  - facets: ['support real time data traffic', 'provide multicasting', 'support mobility']
- `CE05_C4` (1, synonym_set): State the fourth IPv6 objective
  - facets: ['open for change', 'coexistence with existing protocols']

### Per-student

------------------------------------------------------------------------
### CE05_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Some of the objectives are: support billion of end-systems, reduce routing tables, simplify protocol processing, increase security, support real ti,e data traffic, provide multicasting, support mobility, be open for change, coexistence with existing protocols
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | support billion of end-systems, reduce routing tables |
| `CE05_C2` | FULL | 1/1 | simplify protocol processing, increase security |
| `CE05_C3` | FULL | 1/1 | support real ti,e data traffic, provide multicasting, support mobility |
| `CE05_C4` | FULL | 1/1 | be open for change, coexistence with existing protocols |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
Longer addresses (16 bytes) should be supported in order to increase the address space such that more destinations can be specified than via IPv4 addresses.

Security means should be integrated into the protocol to increase security when using it (Implementation of IPsec within the IPv6 standard which enables encryption and verification of the authenticity of IP packets).

The protocol processing should be simplified by simplifying the header data.

Real time data traffic with tracked quality of service should be supported by introducing flow labels and traffic classes.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | Longer addresses (16 bytes) should be supported in order to increase the address space such that more destinations can be specified than via IPv4 addresses. |
| `CE05_C2` | FULL | 1/1 | Security means should be integrated into the protocol to increase security when using it |
| `CE05_C3` | FULL | 1/1 | Real time data traffic with tracked quality of service should be supported by introducing flow labels and traffic classes. |
| `CE05_C4` | ABSENT | 0/1 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The objective of IPv6 is to support assigning IP to new systems, and simplify the header.

1. Supporting billions of end systems by providing longer address.
2. Simplifying protocol processing by providing simplified header.
3. Supporting real time data traffic by creating flow label and differentiating traffic class.
4. Support multicasting and mobility or roaming.
5. Open for change in future. like extension header,
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | 1. Supporting billions of end systems by providing longer address. |
| `CE05_C2` | FULL | 1/1 | 2. Simplifying protocol processing by providing simplified header. |
| `CE05_C3` | FULL | 1/1 | 3. Supporting real time data traffic by creating flow label and differentiating traffic class. 4. Support multicasting and mobility or roaming. |
| `CE05_C4` | FULL | 1/1 | 5. Open for change in future. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

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

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | Firstly, to support billions of end-systems. |
| `CE05_C2` | FULL | 1/1 | Thirdly, to simplify protocol processing. Fourthly, to increase security |
| `CE05_C3` | FULL | 1/1 | Fifthly, to support real time data traffic (quality of service) such as flow label, traffic class. |
| `CE05_C4` | FULL | 1/1 | Eighthly, to be open for change (future).  |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **2 / 4** |
| Absolute error |sys−human| | 2 |
| Bias (sys−human) | -2 |

**Student answer**

```
To support billions of end-systems
To reduce routing tables
To simplify protocol processing
To increase security
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | To support billions of end-systems |
| `CE05_C2` | FULL | 1/1 | To simplify protocol processing To increase security |
| `CE05_C3` | ABSENT | 0/1 | — |
| `CE05_C4` | ABSENT | 0/1 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The first main objective for the introduction of IPv6 was the support of more addresses in the network. While IPv4 with 4 byte addresses only allowed roughly about 4 billion participants, IPv6 enables up to 2^128 addresses, what should be enough for the next centuries. This enlargement of the address room became important with the introduction of mobile computing, smart home and internet of things. 
The second objective was to simplify the process of forwarding and building routing tables by simplifying the header of IPv6-addresses, which are now easier and faster to decode for routers. 
Furthermore, the way IPv6 addresses are handled in a network allowed a higher level of security in comparison to IPv4.
IPv6 allows better guarantees for Quality of Service, especially for real time traffic. This is also due to changes of the header of such an IP-packet. 
Another important lesson learnd from the development history of IPv4 and therefore a main objective for IPv6 was to make it adaptive to future developments: So the IPv6 protocol allows introduction of extension headers for future functionalities.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | The second objective was to simplify the process of forwarding and building routing tables by simplifying the header of IPv6-addresses |
| `CE05_C2` | FULL | 1/1 | The second objective was to simplify the process of forwarding and building routing tables by simplifying the header of IPv6-addresses |
| `CE05_C3` | FULL | 1/1 | IPv6 allows better guarantees for Quality of Service, especially for real time traffic. |
| `CE05_C4` | FULL | 1/1 | make it adaptive to future developments: So the IPv6 protocol allows introduction of extension headers for future functionalities. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
1.	Supporting billions of end-systems: With its longer addresses IPv6 can support more end-systems.
2.	Supporting real time data traffic: The flow label field („traffic class“) allows another quality of service.
3.	Simplifying protocol processing: The header in IPv4 is much more complex than the header of IPv6, so with IPv6 the processing of protocols is simpler. 
4.	Openness for potential change in the future: With the option to use the extension headers, IPv6 provides something that can be useful in the future.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | 1.	Supporting billions of end-systems: With its longer addresses IPv6 can support more end-systems. |
| `CE05_C2` | FULL | 1/1 | 3. Simplifying protocol processing: The header in IPv4 is much more complex than the header of IPv6, so with IPv6 the processing of protocols is simpler. |
| `CE05_C3` | FULL | 1/1 | 2. Supporting real time data traffic: The flow label field („traffic class“) allows another quality of service. |
| `CE05_C4` | FULL | 1/1 | 4. Openness for potential change in the future: With the option to use the extension headers, IPv6 provides something that can be useful in the future. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
To support billions of end systems To increase security To support real time data traffic To support mobility To reduce routing tables
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | To support billions of end systems |
| `CE05_C2` | FULL | 1/1 | To increase security |
| `CE05_C3` | FULL | 1/1 | To support real time data traffic To support mobility |
| `CE05_C4` | ABSENT | 0/1 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
- Support more end-systems by using much longer addresses than IPv4
- Simplify protocol processing by using a less complex header (especially no more checksum in header which must recalculated after each hop)
- Provide multicast and anycast
- Usage of extension headers to be open for future changes/extensions
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | - Support more end-systems by using much longer addresses than IPv4 |
| `CE05_C2` | FULL | 1/1 | Simplify protocol processing by using a less complex header |
| `CE05_C3` | FULL | 1/1 | - Provide multicast and anycast |
| `CE05_C4` | FULL | 1/1 | Usage of extension headers to be open for future changes/extensions |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE05_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | -1 |

**Student answer**

```
- support more end-systems by using longer addresses
- reduce the size of the routing tables
- simplify the protocol, to allow routers to process packets faster.
- integrate security
- provide multicasting
- support real time data traffic
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE05_C1` | FULL | 1/1 | - support more end-systems by using longer addresses - reduce the size of the routing tables |
| `CE05_C2` | FULL | 1/1 | - simplify the protocol, to allow routers to process packets faster. - integrate security |
| `CE05_C3` | FULL | 1/1 | - provide multicasting |
| `CE05_C4` | ABSENT | 0/1 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

========================================================================

## CE06  |  MAE 0.50  |  total marks = 4

### Question

What is the "Dynamic Host Configuration Protocol (DHCP)"? What is it used for?

### Reference

The Dynamic Host Configuration Protocol (DHCP) is a network management protocol used in Internet Protocol (IP) networks, whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on the network. Further, DHCP has largely replaced RARP (and BOOTP)
 Uses of DHCP are: Simplifies installation and configuration of end systems. Allows for manual and automatic IP address assignment. May provide additional configuration information (DNS server, netmask, default router, etc.)

### Our concepts

- `CE06_C1` (2, select_n, min=2): Define DHCP as a network management protocol that automates IP address and configuration assignment.
  - facets: ['network management protocol', 'dynamically assigns IP address', 'configures network parameters']
- `CE06_C2` (2, select_n, min=2): Identify the primary uses of DHCP in network administration.
  - facets: ['simplifies installation and configuration', 'allows manual and automatic IP assignment', 'provides additional configuration info like DNS or router']

### Per-student

------------------------------------------------------------------------
### CE06_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2 / 4** |
| Human raw / normalized (SAF 0–1) | 0.5 / 0.5 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 1 |
| Bias (sys−human) | +1 |

**Student answer**

```
The dhcp protocol is a protocol to configure systems that join a network.
It is used to assign ip addresses to systems within the network. 
If a system joins the network it can ask the dhcp server for network configuration and an ip address that it should use in the future.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | It is used to assign ip addresses to systems within the network. If a system joins the network it can ask the dhcp server for network configuration and an ip address |
| `CE06_C2` | PARTIAL | 1/2 | It is used to assign ip addresses to systems within the network. |

*Human evaluator total only: **2/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
DHCP is a network management protocol which extends the functionality of RARP and BOOTP. DHCP simplifies installation and cofiguration of end systems. It also allows for manual and automatic IP address assignment.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is a network management protocol which extends the functionality of RARP and BOOTP. DHCP simplifies installation and cofiguration of end systems. It also allows for manual and automatic IP address assignment. |
| `CE06_C2` | FULL | 2/2 | DHCP simplifies installation and cofiguration of end systems. It also allows for manual and automatic IP address assignment. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
DHCP is a network management protocol in which it simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment, and may provide additional configuration information. DHCP server is used for assignments in which the address is assigned for a limited time only before it expires.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is a network management protocol in which it simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment, and may provide additional configuration information. |
| `CE06_C2` | FULL | 2/2 | simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment, and may provide additional configuration information |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
DHCP is used to assign IP addresses and other configuration to (new) hosts in a network. After an initial DHCP DISCOVER packet of a client the server sends the assigned IP address back with additional information, like DNS server or netmask.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is used to assign IP addresses and other configuration to (new) hosts in a network. |
| `CE06_C2` | FULL | 2/2 | DHCP is used to assign IP addresses and other configuration to (new) hosts in a network. After an initial DHCP DISCOVER packet of a client the server sends the assigned IP address back with additional information, like DNS server or netmask. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **1 / 4** |
| Human raw / normalized (SAF 0–1) | 0.25 / 0.25 |
| **Our system marks** | **3 / 4** |
| Absolute error |sys−human| | 2 |
| Bias (sys−human) | +2 |

**Student answer**

```
DHCP is a newer version of RARP. 
Systems use this protocol to resolve their own IP address in a network from their hardware/MAC address. 
A specific DHCP server assigns the IP addresses and is contacted to resolve them.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | A specific DHCP server assigns the IP addresses and is contacted to resolve them. |
| `CE06_C2` | PARTIAL | 1/2 | A specific DHCP server assigns the IP addresses and is contacted to resolve them. |

*Human evaluator total only: **1/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The Dynamic Host Configuration Protocol (DHCP) is Internet Protocol based on the special server that uses for manually or automatically IP addresses assignment and other network configuration parameters, such as subnet masks and default gateways, to each device on a network so they can communicate with other IP networks.
This server need not be on the same LAN as the requesting host. Since the DHCP server may not be reachable by broadcasting, a DHCP relay agent is needed on each LAN.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | The Dynamic Host Configuration Protocol (DHCP) is a network management protocol used on Internet Protocol networks whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on a network |
| `CE06_C2` | FULL | 2/2 | It is used for simplified installation and configuration of end systems into network. Allows for manual or automatic assignment of IP addresses. May also provide additional configuration information like DNS server, netmask, default router, etc |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Dynamic Host Configuration Protocol (DHCP) is a protocol for managing IP addresses in a TCP / IP network and distributing them to the requesting hosts. With DHCP, every network participant is able to configure itself automatically. 
To set up a network via TCP/IP, it is necessary to carry out an IP configuration on each host. For a TCP/IP network, the following settings must be made on each host:
- Allocation of a unique IP address
- Assign a subnet mask
- Assign the responsible default or standard gateway
- Assign the responsible DNS server
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | Dynamic Host Configuration Protocol (DHCP) is a protocol for managing IP addresses in a TCP / IP network and distributing them to the requesting hosts. With DHCP, every network participant is able to configure itself automatically. |
| `CE06_C2` | FULL | 2/2 | With DHCP, every network participant is able to configure itself automatically. ... - Assign the responsible default or standard gateway - Assign the responsible DNS server |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2 / 4** |
| Human raw / normalized (SAF 0–1) | 0.5 / 0.5 |
| **Our system marks** | **2 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
DHCP is a protocol for automatic or manual allocation of IP addresses to devices, which is usually done by a DHCP server.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | PARTIAL | 1/2 | DHCP is a protocol for automatic or manual allocation of IP addresses to devices |
| `CE06_C2` | PARTIAL | 1/2 | automatic or manual allocation of IP addresses |

*Human evaluator total only: **2/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2 / 4** |
| Human raw / normalized (SAF 0–1) | 0.5 / 0.5 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 2 |
| Bias (sys−human) | +2 |

**Student answer**

```
DHCP simplifies installation and configuration of end systems and allows for manual and automatic IP address assignment. It also may provide additional configuration information.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | allows for manual and automatic IP address assignment and may provide additional configuration information. |
| `CE06_C2` | FULL | 2/2 | DHCP simplifies installation and configuration of end systems, allows for manual and automatic IP address assignment and may provide additional configuration information. |

*Human evaluator total only: **2/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE06_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
DHCP is a protocol that enables devices connected over a network to obtain IP addresses and it also provides network configuration. Both manual and automatic address assignment is possible using DHCP.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE06_C1` | FULL | 2/2 | DHCP is a protocol that enables devices connected over a network to obtain IP addresses and it also provides network configuration. |
| `CE06_C2` | FULL | 2/2 | DHCP is a protocol that enables devices connected over a network to obtain IP addresses and it also provides network configuration. Both manual and automatic address assignment is possible using DHCP. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

========================================================================

## CE07  |  MAE 0.35  |  total marks = 4

### Question

What are extension headers in IPv6 and where are they located in a packet? What is the main advantage of extension headers compared to IPv4?

### Reference

Extension headers are used to extend the fixed IPv6 header with additional, optional network layer information. If present, they are located between the fixed header/main header and payload/upper-layer header/transport-layer header.

Main advantage: One of the following advantages are considered fully correct:
1. It allows the appending of new options without changing the header.
2. IPv6 packets with optional headers are typically processed faster/simpler by intermediate devices as most of the options are ignored (except "Hop-by-Hop Extension") while they are processed by all routers in IPv4 unless ordered otherwise.

### Our concepts

- `CE07_C1` (1.5, select_n, min=2): Define the purpose of IPv6 extension headers
  - facets: ['extend fixed IPv6 header', 'additional optional network layer information']
- `CE07_C2` (1, synonym_set): Identify the location of extension headers in an IPv6 packet
  - facets: ['between fixed header and payload', 'between main header and transport-layer header']
- `CE07_C3` (1.5, synonym_set): Explain the main advantage of extension headers over IPv4
  - facets: ['appending new options without changing the header', 'faster processing by intermediate devices']

### Per-student

------------------------------------------------------------------------
### CE07_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Extension Headers enable you to add additional header information to the already existing header if you really need them. They are placed between the header and the payload, by reducing the payload size if they get appended. The main advantage is, that you can overcome the size problem of the header and add additional information without changing the original header size.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Extension Headers enable you to add additional header information to the already existing header if you really need them. |
| `CE07_C2` | FULL | 1/1 | They are placed between the header and the payload |
| `CE07_C3` | FULL | 1.5/1.5 | add additional information without changing the original header size. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 4** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **2.5 / 4** |
| Absolute error |sys−human| | 0.5 |
| Bias (sys−human) | -0.5 |

**Student answer**

```
The header in IPv6 has a fixed length and is designed to be used for easy processing, it only contains information needed for routing. Any additional information is stored in extension headers. They carry optional information and can be found in between the fixed header and the playload. Since the whole IPv6 packet is only allowed a certain size, these additional extension headers take up space of the payload. The main advantage of extension headers is that they can be added optionally and help to overcome size limitation.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Any additional information is stored in extension headers. They carry optional information |
| `CE07_C2` | FULL | 1/1 | They carry optional information and can be found in between the fixed header and the playload. |
| `CE07_C3` | ABSENT | 0/1.5 | — |

*Human evaluator total only: **3/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **2 / 4** |
| Human raw / normalized (SAF 0–1) | 0.5 / 0.5 |
| **Our system marks** | **1.75 / 4** |
| Absolute error |sys−human| | 0.25 |
| Bias (sys−human) | -0.25 |

**Student answer**

```
Extension Headers are extensions for the normal header. You can support multiple addresses or specify more options for your header and packet, like e.g. authentication.

The Extension Headers are located between the normal header and the payload, they will be attached to the normal header. 

The biggest advantage of Extension Headers is the possibility to use broadcasting.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | PARTIAL | 0.75/1.5 | Extension Headers are extensions for the normal header. You can support multiple addresses or specify more options for your header and packet |
| `CE07_C2` | FULL | 1/1 | The Extension Headers are located between the normal header and the payload |
| `CE07_C3` | ABSENT | 0/1.5 | — |

*Human evaluator total only: **2/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
The extension headers replace the "option-field" in IPv4 and include optional more informations. They are placed between the actual header and the payload. The main advantage is that they can expand the header informations upon need without expanding the fixed header structure.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | they can expand the header informations upon need without expanding the fixed header structure. |
| `CE07_C2` | FULL | 1/1 | They are placed between the actual header and the payload. |
| `CE07_C3` | FULL | 1.5/1.5 | The main advantage is that they can expand the header informations upon need without expanding the fixed header structure. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Extension headers are header that can be added to a packet for a new functionality. Extension headers are present between fixed header and payload. 
Advantages:
1. They allow appending new options without changing fixed header
2. They help in overcoming size limitation on packets.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | They allow appending new options without changing fixed header |
| `CE07_C2` | FULL | 1/1 | Extension headers are present between fixed header and payload. |
| `CE07_C3` | FULL | 1.5/1.5 | 1. They allow appending new options without changing fixed header |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **3 / 4** |
| Human raw / normalized (SAF 0–1) | 0.75 / 0.75 |
| **Our system marks** | **1.75 / 4** |
| Absolute error |sys−human| | 1.25 |
| Bias (sys−human) | -1.25 |

**Student answer**

```
Extension headers are optional fields in IPv6 address, placed between the header and the playload. The main advantage compared to IPv4 is that extension headers allow for extra information to be headed, overcaming the address size limitation
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | PARTIAL | 0.75/1.5 | extension headers allow for extra information to be headed |
| `CE07_C2` | FULL | 1/1 | placed between the header and the playload |
| `CE07_C3` | INCORRECT | 0/1.5 | extension headers allow for extra information to be headed, overcaming the address size limitation |

*Human evaluator total only: **3/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **3.25 / 4** |
| Absolute error |sys−human| | 0.75 |
| Bias (sys−human) | -0.75 |

**Student answer**

```
Extension headers are optional information/options that can be append without changing the fixed header.
the extension headers are located between the header and payload of a packet. 
thanks to the extension headers it is easier to overcome the size limitation
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | PARTIAL | 0.75/1.5 | Extension headers are optional information/options that can be append without changing the fixed header. |
| `CE07_C2` | FULL | 1/1 | the extension headers are located between the header and payload of a packet. |
| `CE07_C3` | FULL | 1.5/1.5 | Extension headers are optional information/options that can be append without changing the fixed header. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Extension headers are optional headers placed between fixed header and payload.
The advantages are the help to overcome size limitation and the possibility to append new options without changing the fixed header.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | They allow appending new options without changing the fixed header. |
| `CE07_C2` | FULL | 1/1 | placed between the fixed header and the payload |
| `CE07_C3` | FULL | 1.5/1.5 | They allow appending new options without changing the fixed header. |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S09

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **4 / 4** |
| Absolute error |sys−human| | 0 |
| Bias (sys−human) | +0 |

**Student answer**

```
Extension headers are to store additional information, such as routing, destination, or fragment.They are optional. so they don't need to be always in a packet. 

They are located between the header and the payload. 

Main advantages compared to IPv4:
1. are optional
2. help to overcome size limitation
3. allow to append new options without changing the fixed header
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | FULL | 1.5/1.5 | Extension headers are to store additional information, such as routing, destination, or fragment. ... allow to append new options without changing the fixed header |
| `CE07_C2` | FULL | 1/1 | They are located between the header and the payload. |
| `CE07_C3` | FULL | 1.5/1.5 | allow to append new options without changing the fixed header |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*

------------------------------------------------------------------------
### CE07_S10

**Marks**

| Source | Value |
|---|---|
| **Human evaluator marks** | **4 / 4** |
| Human raw / normalized (SAF 0–1) | 1 / 1 |
| **Our system marks** | **1.75 / 4** |
| Absolute error |sys−human| | 2.25 |
| Bias (sys−human) | -2.25 |

**Student answer**

```
The extension headers are placed between fixed header and payload. Extension headers have advantages compared to IPv4 because they are optional, help to overcome size limitation, and allow to append new options without changing the fixed header.
```

**Our check (CGR)**

| Concept | Verdict | Our marks | Evidence |
|---|---|---:|---|
| `CE07_C1` | PARTIAL | 0.75/1.5 | The main advantage is that they are optional. |
| `CE07_C2` | FULL | 1/1 | The extension headers are placed between fixed header and payload. |
| `CE07_C3` | ABSENT | 0/1.5 | — |

*Human evaluator total only: **4/4** (no per-concept human split in SAF).*
