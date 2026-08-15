# CE04 — no-facets criteria-only (n=8)

Empty `evidence_facets` / keywords / variants. CGR falls back to Target Criteria.
C1 is `synonym_set` (not select_n): channel-hold not required separately.

**MAE no-facets:** 0.125  ·  **MAE with-facets (same 8):** 0.500

------------------------------------------------------------------------
### CE04_S01

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0 |

**Student answer**

```
Frame bursting allow sender to transmit a Concatenated sequence of multiple frames in a single transmission. It has better efficiency however it needs frames waiting for transmission.
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | transmit a Concatenated sequence of multiple frames in a single transmission |
| `CE04_C2` | FULL | 1/1 | It has better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

------------------------------------------------------------------------
### CE04_S02

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0 |

**Student answer**

```
Sending multiple different frames concatenated to each other is called frame bursting. Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. Carrier extension extends the message with unused bits which lower the efficiency.
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sending multiple different frames concatenated to each other is called frame bursting. |
| `CE04_C2` | FULL | 1/1 | However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. |
| `CE04_C3` | FULL | 1/1 | Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. |

------------------------------------------------------------------------
### CE04_S03

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0 |

**Student answer**

```
Frame Bursting allows sender to transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission.

Advantage as compared to carrier extension is:
-Better efficiency

Disadvantage as compared to carrier extension is:
-it needs frames waiting for transmission
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission |
| `CE04_C2` | FULL | 1/1 | -Better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

------------------------------------------------------------------------
### CE04_S04

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0 |

**Student answer**

```
Frame bursting is a way to increase the speeds of the ethernet protocol in the shared broadcast mode. To meet the minimum frame length requirements at the greater speeds multiple frames are concatenated to a single, larger frame. This allows to detect collisions with faster speeds at the cost of a delay when sending a larger frame. One advantage over the carrier extension is the improved throughput, at the cost of an increased latency (disadvantage).
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | multiple frames are concatenated to a single, larger frame. |
| `CE04_C2` | FULL | 1/1 | One advantage over the carrier extension is the improved throughput |
| `CE04_C3` | FULL | 1/1 | at the cost of an increased latency (disadvantage) |

------------------------------------------------------------------------
### CE04_S05

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2.25 / 3** |
| System (no facets) | **2 / 3** |
| System (with facets, prior smoke) | 1.5 / 3 |
| \|err\| no-facets | 0.25 |

**Student answer**

```
In frame bursting, the sender can transmit multiple frames by concatenating them in single transmission.
The carrier extension provides really low efficiency with only 46byte  user data being transmitted using 512 byte.
Whereas the frame bursting provides a much better performance.
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | the sender can transmit multiple frames by concatenating them in single transmission. |
| `CE04_C2` | FULL | 1/1 | Whereas the frame bursting provides a much better performance. |
| `CE04_C3` | ABSENT | 0/1 | — |

------------------------------------------------------------------------
### CE04_S06

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0 |

**Student answer**

```
Sender collects and concatenates sequence of multiple frames to send it with single transmission.
+ better efficiency
Disadvantage: needs frames waiting for transmission
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sender collects and concatenates sequence of multiple frames to send it with single transmission. |
| `CE04_C2` | FULL | 1/1 | + better efficiency |
| `CE04_C3` | FULL | 1/1 | needs frames waiting for transmission |

------------------------------------------------------------------------
### CE04_S07

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **2.25 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0.75 |

**Student answer**

```
In frame bursting, instead of the sender sending one packet at a time, it sends ten packets at once. The sender waits for the packets until it has ten packets ready to send. Put them together and just then send them.

Advantage: better performance than carrier extension, since more data is sent at a time.

Disadvantage: if there are only one or two packets to send, the sender will be waiting for the remain, to reach the 10 packets. If there are not 10 packets, after a timeout, the sender adds rubbish to the frame (so it has the needed size). So, the packets will be sent with a delay and with unnecessary data.
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | instead of the sender sending one packet at a time, it sends ten packets at once. The sender waits for the packets until it has ten packets ready to send. Put them together and just then send them. |
| `CE04_C2` | FULL | 1/1 | better performance than carrier extension, since more data is sent at a time. |
| `CE04_C3` | FULL | 1/1 | if there are only one or two packets to send, the sender will be waiting for the remain, to reach the 10 packets. ... So, the packets will be sent with a delay |

------------------------------------------------------------------------
### CE04_S08

**Marks**

| Source | Value |
|---|---|
| **Human evaluator** | **3 / 3** |
| System (no facets) | **3 / 3** |
| System (with facets, prior smoke) | 2.5 / 3 |
| \|err\| no-facets | 0 |

**Student answer**

```
To be able to transmit data over lager distances at higher speed and still avoiding collisions you send bigger sequences by collecting several packets and sending them all together.

Advantage: You have a higher efficiency compared to carrier extension. You have a minimum of 70 percent (frame size 64 byte and user data 46 byte) user data compared to a minimum 9 percent of.

Disadvantage: You have a delay in time while waiting for other packets until you have collected enough to send.
```

**Our check (no facets)**

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | you send bigger sequences by collecting several packets and sending them all together. |
| `CE04_C2` | FULL | 1/1 | You have a higher efficiency compared to carrier extension. |
| `CE04_C3` | FULL | 1/1 | You have a delay in time while waiting for other packets until you have collected enough to send. |
