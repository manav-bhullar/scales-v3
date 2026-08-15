# CE04 2×2 factorial — facets × criteria

n=8 same smoke students. Run: 2026-07-30T18:02:25.685069+00:00

| Arm | Facets | Criteria | MAE | mean bias (sys−hum) | exact | over | under |
|---|---|---|---:|---:|---:|---:|---:|
| A1 | present | strict | 0.5 | -0.438 | 0 | 1 | 7 |
| A2 | absent | strict | 0.188 | -0.125 | 4 | 1 | 3 |
| A3 | present | holistic | 0.125 | +0.062 | 6 | 1 | 1 |
| A4 | absent | holistic | 0.125 | +0.062 | 6 | 1 | 1 |

## Contrasts (Δ MAE = armB − armA; negative = B better)

```json
{
  "A1_vs_A2_facet_blank_under_strict": -0.312,
  "A1_vs_A3_criteria_rewrite_with_facets": -0.375,
  "A2_vs_A4_criteria_rewrite_without_facets": -0.063,
  "A3_vs_A4_facet_blank_under_holistic": 0.0
}
```

**Winning arm:** A3 (MAE 0.125)

========================================================================

## A1 — facets present + strict select_n criteria

----------------------------------------
### CE04_S01  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | transmit a Concatenated sequence of multiple frames in a single transmission |
| `CE04_C2` | FULL | 1/1 | It has better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S02  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Sending multiple different frames concatenated to each other is called frame bursting. |
| `CE04_C2` | FULL | 1/1 | However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. |
| `CE04_C3` | FULL | 1/1 | Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. |

----------------------------------------
### CE04_S03  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission |
| `CE04_C2` | FULL | 1/1 | -Better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S04  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | multiple frames are concatenated to a single, larger frame. |
| `CE04_C2` | FULL | 1/1 | One advantage over the carrier extension is the improved throughput |
| `CE04_C3` | FULL | 1/1 | at the cost of an increased latency (disadvantage) |

----------------------------------------
### CE04_S05  H=2.25  S=1.5  bias=-0.75

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | the sender can transmit multiple frames by concatenating them in single transmission. |
| `CE04_C2` | FULL | 1/1 | Whereas the frame bursting provides a much better performance. |
| `CE04_C3` | ABSENT | 0/1 | — |

----------------------------------------
### CE04_S06  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Sender collects and concatenates sequence of multiple frames to send it with single transmission. |
| `CE04_C2` | FULL | 1/1 | + better efficiency |
| `CE04_C3` | FULL | 1/1 | needs frames waiting for transmission |

----------------------------------------
### CE04_S07  H=2.25  S=2.5  bias=+0.25

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Put them together and just then send them. |
| `CE04_C2` | FULL | 1/1 | better performance than carrier extension, since more data is sent at a time. |
| `CE04_C3` | FULL | 1/1 | So, the packets will be sent with a delay and with unnecessary data. |

----------------------------------------
### CE04_S08  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | collecting several packets and sending them all together |
| `CE04_C2` | FULL | 1/1 | You have a higher efficiency compared to carrier extension. |
| `CE04_C3` | FULL | 1/1 | You have a delay in time while waiting for other packets until you have collected enough to send. |

========================================================================

## A2 — facets absent + strict criteria

----------------------------------------
### CE04_S01  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | transmit a Concatenated sequence of multiple frames in a single transmission |
| `CE04_C2` | FULL | 1/1 | It has better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S02  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | Sending multiple different frames concatenated to each other is called frame bursting. |
| `CE04_C2` | FULL | 1/1 | However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. |
| `CE04_C3` | FULL | 1/1 | Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. |

----------------------------------------
### CE04_S03  H=3  S=2.5  bias=-0.5

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission |
| `CE04_C2` | FULL | 1/1 | Better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S04  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | multiple frames are concatenated to a single, larger frame. |
| `CE04_C2` | FULL | 1/1 | One advantage over the carrier extension is the improved throughput |
| `CE04_C3` | FULL | 1/1 | at the cost of an increased latency |

----------------------------------------
### CE04_S05  H=2.25  S=2  bias=-0.25

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | the sender can transmit multiple frames by concatenating them in single transmission. |
| `CE04_C2` | FULL | 1/1 | Whereas the frame bursting provides a much better performance. |
| `CE04_C3` | ABSENT | 0/1 | — |

----------------------------------------
### CE04_S06  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sender collects and concatenates sequence of multiple frames to send it with single transmission. |
| `CE04_C2` | FULL | 1/1 | + better efficiency |
| `CE04_C3` | FULL | 1/1 | needs frames waiting for transmission |

----------------------------------------
### CE04_S07  H=2.25  S=2.5  bias=+0.25

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | PARTIAL | 0.5/1 | In frame bursting, instead of the sender sending one packet at a time, it sends ten packets at once. ... Put them together and just then send them. |
| `CE04_C2` | FULL | 1/1 | better performance than carrier extension, since more data is sent at a time. |
| `CE04_C3` | FULL | 1/1 | So, the packets will be sent with a delay |

----------------------------------------
### CE04_S08  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | you send bigger sequences by collecting several packets and sending them all together. |
| `CE04_C2` | FULL | 1/1 | You have a higher efficiency compared to carrier extension. |
| `CE04_C3` | FULL | 1/1 | You have a delay in time while waiting for other packets until you have collected enough to send. |

========================================================================

## A3 — facets present + holistic criteria

----------------------------------------
### CE04_S01  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | transmit a Concatenated sequence of multiple frames in a single transmission |
| `CE04_C2` | FULL | 1/1 | It has better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S02  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sending multiple different frames concatenated to each other is called frame bursting. |
| `CE04_C2` | FULL | 1/1 | However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. |
| `CE04_C3` | FULL | 1/1 | Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. |

----------------------------------------
### CE04_S03  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission |
| `CE04_C2` | FULL | 1/1 | -Better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S04  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | multiple frames are concatenated to a single, larger frame |
| `CE04_C2` | FULL | 1/1 | One advantage over the carrier extension is the improved throughput |
| `CE04_C3` | FULL | 1/1 | at the cost of an increased latency (disadvantage) |

----------------------------------------
### CE04_S05  H=2.25  S=2  bias=-0.25

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | the sender can transmit multiple frames by concatenating them in single transmission. |
| `CE04_C2` | FULL | 1/1 | Whereas the frame bursting provides a much better performance. |
| `CE04_C3` | ABSENT | 0/1 | — |

----------------------------------------
### CE04_S06  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sender collects and concatenates sequence of multiple frames to send it with single transmission. |
| `CE04_C2` | FULL | 1/1 | + better efficiency |
| `CE04_C3` | FULL | 1/1 | needs frames waiting for transmission |

----------------------------------------
### CE04_S07  H=2.25  S=3  bias=+0.75

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Put them together and just then send them. |
| `CE04_C2` | FULL | 1/1 | better performance than carrier extension, since more data is sent at a time. |
| `CE04_C3` | FULL | 1/1 | So, the packets will be sent with a delay |

----------------------------------------
### CE04_S08  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | collecting several packets and sending them all together |
| `CE04_C2` | FULL | 1/1 | You have a higher efficiency compared to carrier extension. |
| `CE04_C3` | FULL | 1/1 | You have a delay in time while waiting for other packets until you have collected enough to send. |

========================================================================

## A4 — facets absent + holistic criteria

----------------------------------------
### CE04_S01  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | transmit a Concatenated sequence of multiple frames in a single transmission |
| `CE04_C2` | FULL | 1/1 | It has better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S02  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sending multiple different frames concatenated to each other is called frame bursting. |
| `CE04_C2` | FULL | 1/1 | However frame bursting increases the efficiency compared to carrier extension, as the amount of user data transferred is higher. |
| `CE04_C3` | FULL | 1/1 | Frame bursting might increase latency, as the sender has to buffer multiple frames until he can start sending a burst. |

----------------------------------------
### CE04_S03  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | transmit CONCATENATED SEQUENCE OF MULTIPLE FRAMES in a single transmission |
| `CE04_C2` | FULL | 1/1 | -Better efficiency |
| `CE04_C3` | FULL | 1/1 | it needs frames waiting for transmission |

----------------------------------------
### CE04_S04  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | multiple frames are concatenated to a single, larger frame. |
| `CE04_C2` | FULL | 1/1 | One advantage over the carrier extension is the improved throughput |
| `CE04_C3` | FULL | 1/1 | at the cost of an increased latency (disadvantage) |

----------------------------------------
### CE04_S05  H=2.25  S=2  bias=-0.25

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | the sender can transmit multiple frames by concatenating them in single transmission. |
| `CE04_C2` | FULL | 1/1 | Whereas the frame bursting provides a much better performance. |
| `CE04_C3` | ABSENT | 0/1 | — |

----------------------------------------
### CE04_S06  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | Sender collects and concatenates sequence of multiple frames to send it with single transmission. |
| `CE04_C2` | FULL | 1/1 | + better efficiency |
| `CE04_C3` | FULL | 1/1 | needs frames waiting for transmission |

----------------------------------------
### CE04_S07  H=2.25  S=3  bias=+0.75

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | instead of the sender sending one packet at a time, it sends ten packets at once. The sender waits for the packets until it has ten packets ready to send. Put them together and just then send them. |
| `CE04_C2` | FULL | 1/1 | better performance than carrier extension, since more data is sent at a time. |
| `CE04_C3` | FULL | 1/1 | if there are only one or two packets to send, the sender will be waiting for the remain, to reach the 10 packets. ... So, the packets will be sent with a delay |

----------------------------------------
### CE04_S08  H=3  S=3  bias=+0

| Concept | Verdict | Marks | Evidence |
|---|---|---:|---|
| `CE04_C1` | FULL | 1/1 | you send bigger sequences by collecting several packets and sending them all together. |
| `CE04_C2` | FULL | 1/1 | You have a higher efficiency compared to carrier extension. |
| `CE04_C3` | FULL | 1/1 | You have a delay in time while waiting for other packets until you have collected enough to send. |
