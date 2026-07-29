# CERA outputs — 10 questions (corrected modes)

Pack: `cera_eval_v1_corrected/`

## CE01 · 3.0/3 · 4 concepts

### Question

Name the 3 service classes the Data Link Layer offers and explain the differences between the classes.

### Reference answer

1.unconfirmed connectionless - no ACK, loss of data possible, no flow control, no connect or disconnect.
2.confirmed connectionless - with ACK, no loss of data (timeout and retransmit instead→ duplicates and sequence errors possible), no flow control, no connect or disconnect.
3.connection-oriented - no data loss, duplication or sequencing errors. Instead a 3 phased communication with connect and disconnect, and flow control

### Rubric

```
Total 3 marks:
1) Naming the 3 classes (1.5 marks)
2) Explaining distinguishing properties of each class (1.5 marks)
```

### CERA concepts

#### CE01_C1 — 1.5 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Identify the three service classes offered by the Data Link Layer
- **target_criteria:** FULL requires naming all three classes: unconfirmed connectionless, confirmed connectionless, and connection-oriented
- **facets:** ['unconfirmed connectionless', 'confirmed connectionless', 'connection-oriented']
- **variants:** ['unconfirmed connectionless service', 'confirmed connectionless service', 'connection-oriented service', 'connectionless unconfirmed', 'connectionless confirmed']
- **partial:** 0.5 marks per correctly named class

#### CE01_C2 — 0.5 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Describe the distinguishing properties of unconfirmed connectionless service
- **target_criteria:** FULL requires identifying the lack of ACK, potential data loss, and absence of flow/connection control
- **facets:** ['no ACK', 'loss of data possible', 'no flow control', 'no connect or disconnect']
- **variants:** ['no acknowledgement sent', 'data might be lost', 'no flow management', 'no connection setup or teardown']
- **partial:** 0.125 marks per property present

#### CE01_C3 — 0.5 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Describe the distinguishing properties of confirmed connectionless service
- **target_criteria:** FULL requires identifying the use of ACK, potential for duplicates/sequence errors, and absence of flow/connection control
- **facets:** ['with ACK', 'no loss of data', 'duplicates and sequence errors possible', 'no flow control', 'no connect or disconnect']
- **variants:** ['uses acknowledgements', 'no data loss but potential duplicates', 'sequence errors can occur', 'no flow control or connection management']
- **partial:** 0.1 marks per property present

#### CE01_C4 — 0.5 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Describe the distinguishing properties of connection-oriented service
- **target_criteria:** FULL requires identifying reliable delivery and the use of connection/flow control
- **facets:** ['no data loss', 'no duplication or sequencing errors', '3 phased communication with connect and disconnect', 'flow control']
- **variants:** ['reliable data transfer', 'no errors in sequence or duplicates', 'uses connection setup and teardown', 'includes flow control']
- **partial:** 0.125 marks per property present

---

## CE02 · 3.0/3 · 2 concepts

### Question

Consider the following scenario: You are browsing the web for a very specific and important piece of information. However, you are not quite sure how to find it and adopt an iterative process of refining your query after every search, depending on the shown results and a skim of the first few websites. Is it better to use a connection-oriented or connectionless service for your communication in this scenario? Explain your answer in 1-4 sentences.

### Reference answer

Connectionless, because you will communicate with various partners (websites) for short periods of time. If you would initiate a connection with every website you skim, that would incur a lot of overhead in the connecting and disconnecting phase, just to have very short data transfers.

### Rubric

```
Total 3 marks:
1) Correct identification of service type (1 mark)
2) Reasoning / justification for the choice (2 marks)
```

### CERA concepts

#### CE02_C1 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** Identify that a connectionless service is the appropriate choice for the described web browsing scenario.
- **target_criteria:** Student must correctly identify connectionless service.
- **facets:** ['connectionless']
- **variants:** ['connectionless service', 'connectionless communication', 'use connectionless']
- **partial:** None

#### CE02_C2 — 2.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** Explain that connectionless service is better because it avoids the overhead of establishing and tearing down connections for many short-lived interactions.
- **target_criteria:** any of: avoiding connection overhead / efficiency for short interactions counts as the justification.
- **facets:** ['overhead in connecting and disconnecting', 'unnecessary for short data transfers']
- **variants:** ['avoids setup and teardown costs', 'too much overhead for short web requests', 'connection-oriented is inefficient for many short sessions', 'avoids unnecessary connection management']
- **partial:** 1 mark for identifying overhead or short duration; 2 marks for both or comprehensive explanation.

---

## CE03 · 4.0/4 · 4 concepts

### Question

What is the difference between asynchronous and synchronous transmission mode in the Data Link Layer.

### Reference answer

Asynchronous transmission: Every character a self-contained unit surrounded by a start bit and a stop bit, which is an easy and cheap pattern, but causes low transmission rates.

Synchronous transmission: Several characters pooled to a continuous stream of data (frames), Frames defined by SYN or flag, higher complexity, but higher transmission rates. Requires synchronization between sender and receiver.

### Rubric

```
Total 4 marks:
1) Description of each mode's mechanism (2 marks)
2) Trade-offs / characteristics of each mode (2 marks)
```

### CERA concepts

#### CE03_C1 — 1.0 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Mechanism of asynchronous transmission
- **target_criteria:** FULL requires identifying the use of start and stop bits for individual characters
- **facets:** ['character as self-contained unit', 'surrounded by start and stop bits']
- **variants:** ['uses start/stop bits per byte', 'individual characters framed by start and stop bits', 'each character is independent with start and stop bits']
- **partial:** 0.5 marks for mentioning start/stop bits without explaining the character-level unit

#### CE03_C2 — 1.0 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Mechanism of synchronous transmission
- **target_criteria:** FULL requires identifying the use of frames or continuous streams defined by synchronization markers
- **facets:** ['pooled into continuous stream of data', 'frames defined by SYN or flag', 'requires synchronization between sender and receiver']
- **variants:** ['data sent in continuous frames', 'uses SYN/flag markers to define frames', 'requires clock synchronization between nodes']
- **partial:** 0.5 marks for mentioning frames or synchronization only

#### CE03_C3 — 1.0 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Trade-offs of asynchronous transmission
- **target_criteria:** FULL requires identifying the simplicity/low cost and the resulting low transmission rate
- **facets:** ['easy and cheap pattern', 'low transmission rates']
- **variants:** ['simple and inexpensive but slow', 'low overhead but low speed', 'easy to implement but limited throughput']
- **partial:** 0.5 marks for mentioning either the simplicity or the low rate

#### CE03_C4 — 1.0 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** Trade-offs of synchronous transmission
- **target_criteria:** FULL requires identifying the higher complexity and the resulting higher transmission rate
- **facets:** ['higher complexity', 'higher transmission rates']
- **variants:** ['more complex but faster', 'high overhead but high throughput', 'complex implementation for better speed']
- **partial:** 0.5 marks for mentioning either the complexity or the high rate

---

## CE04 · 3.0/3 · 3 concepts

### Question

What is "frame bursting"? Also, give 1 advantage and disadvantage compared to the carrier extension.

### Reference answer

Frame bursting reduces the overhead for transmitting small frames by concatenating a sequence of multiple frames in one single transmission, without ever releasing control of the channel.
Advantage: it is more efficient than carrier extension as single frames not filled up with garbage.
Disadvantage: need frames waiting for transmission or buffering and delay of frames

### Rubric

```
Total 3 marks:
1) Definition of frame bursting (1 mark)
2) One advantage compared to carrier extension (1 mark)
3) One disadvantage compared to carrier extension (1 mark)
```

### CERA concepts

#### CE04_C1 — 1.0 marks — role=`select_n`, min_count=`2`, legacy_mode=`ANY`

- **knowledge_point:** Define frame bursting as concatenating multiple frames into one transmission without releasing the channel.
- **target_criteria:** FULL = at least 2 of the 3 definition parts present (concatenate multiple frames / one transmission / without releasing channel); PARTIAL = exactly 1 part; ABSENT = 0
- **facets:** ['concatenating a sequence of multiple frames', 'one single transmission', 'without ever releasing control of the channel']
- **variants:** ['sending several frames at once without giving up the channel', 'grouping frames into one transmission to save overhead', 'keeping the channel busy to send multiple frames together', 'combining frames into a single burst transmission']
- **partial:** exactly 1 definition part → 0.5 marks

#### CE04_C2 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** Identify the advantage of frame bursting over carrier extension regarding efficiency.
- **target_criteria:** any of: more efficient / no garbage / not filled with padding counts as the advantage
- **facets:** ['more efficient than carrier extension', 'single frames not filled up with garbage']
- **variants:** ['it avoids wasting space with padding', "it is more efficient because it doesn't use garbage bits", 'it performs better than carrier extension by avoiding filler data', 'it saves bandwidth by not filling frames with useless data']
- **partial:** None

#### CE04_C3 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** Identify the disadvantage of frame bursting regarding transmission requirements or delay.
- **target_criteria:** any of: need frames waiting / buffering / delay of frames counts as the disadvantage
- **facets:** ['need frames waiting for transmission', 'buffering', 'delay of frames']
- **variants:** ['it requires frames to be buffered before sending', 'it introduces latency while waiting for enough frames', 'it causes a delay because it needs to wait for more data', 'it relies on having frames ready to transmit']
- **partial:** None

---

## CE05 · 4.0/4 · 4 concepts

### Question

What are the objectives of IPv6? Please state at least 4 objectives.

### Reference answer

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

### Rubric

```
Total 4 marks:
1) At least 4 valid IPv6 objectives stated (4 marks, 1 per objective)
```

### CERA concepts

#### CE05_C1 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** State the first IPv6 objective
- **target_criteria:** any of: support billions of end-systems / reduce routing tables
- **facets:** ['support billions of end-systems', 'reduce routing tables']
- **variants:** ['support massive number of devices', 'scale to billions of hosts', 'smaller routing tables', 'efficient routing table management']
- **partial:** 0 marks if no valid objective is stated

#### CE05_C2 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** State the second IPv6 objective
- **target_criteria:** any of: simplify protocol processing / increase security
- **facets:** ['simplify protocol processing', 'increase security']
- **variants:** ['simpler header processing', 'streamlined protocol', 'better security', 'enhanced security features']
- **partial:** 0 marks if no valid objective is stated

#### CE05_C3 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** State the third IPv6 objective
- **target_criteria:** any of: support real time data traffic / provide multicasting / support mobility
- **facets:** ['support real time data traffic', 'provide multicasting', 'support mobility']
- **variants:** ['quality of service for real time data', 'multicast support', 'roaming support', 'mobile device support']
- **partial:** 0 marks if no valid objective is stated

#### CE05_C4 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** State the fourth IPv6 objective
- **target_criteria:** any of: open for change / coexistence with existing protocols
- **facets:** ['open for change', 'coexistence with existing protocols']
- **variants:** ['future proofing', 'extensibility', 'backward compatibility', 'interoperability with older protocols']
- **partial:** 0 marks if no valid objective is stated

---

## CE06 · 4.0/4 · 2 concepts

### Question

What is the "Dynamic Host Configuration Protocol (DHCP)"? What is it used for?

### Reference answer

The Dynamic Host Configuration Protocol (DHCP) is a network management protocol used in Internet Protocol (IP) networks, whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on the network. Further, DHCP has largely replaced RARP (and BOOTP)
 Uses of DHCP are: Simplifies installation and configuration of end systems. Allows for manual and automatic IP address assignment. May provide additional configuration information (DNS server, netmask, default router, etc.)

### Rubric

```
Total 4 marks:
1) Definition of DHCP (2 marks)
2) Uses / purpose of DHCP (2 marks)
```

### CERA concepts

#### CE06_C1 — 2.0 marks — role=`select_n`, min_count=`2`, legacy_mode=`ANY`

- **knowledge_point:** Define DHCP as a network management protocol that automates IP address and configuration assignment.
- **target_criteria:** FULL = at least 2 of 3 definition parts (network management protocol / dynamically assigns IP / configures parameters); PARTIAL = exactly 1; ABSENT = 0
- **facets:** ['network management protocol', 'dynamically assigns IP address', 'configures network parameters']
- **variants:** ['A protocol for managing network settings', 'Automated IP address assignment system', 'A tool that gives devices their network configuration automatically', 'Protocol used to set up IP addresses on a network']
- **partial:** exactly 1 definition part → 1.0 mark

#### CE06_C2 — 2.0 marks — role=`select_n`, min_count=`2`, legacy_mode=`ANY`

- **knowledge_point:** Identify the primary uses of DHCP in network administration.
- **target_criteria:** FULL = at least 2 distinct uses from the catalog; PARTIAL = exactly 1; ABSENT = 0
- **facets:** ['simplifies installation and configuration', 'allows manual and automatic IP assignment', 'provides additional configuration info like DNS or router']
- **variants:** ['Makes setting up devices easier', 'Handles both static and dynamic IP allocation', 'Distributes extra settings like DNS and gateway info', 'Reduces manual network setup effort']
- **partial:** exactly 1 use → 1.0 mark

---

## CE07 · 4.0/4 · 3 concepts

### Question

What are extension headers in IPv6 and where are they located in a packet? What is the main advantage of extension headers compared to IPv4?

### Reference answer

Extension headers are used to extend the fixed IPv6 header with additional, optional network layer information. If present, they are located between the fixed header/main header and payload/upper-layer header/transport-layer header.

Main advantage: One of the following advantages are considered fully correct:
1. It allows the appending of new options without changing the header.
2. IPv6 packets with optional headers are typically processed faster/simpler by intermediate devices as most of the options are ignored (except "Hop-by-Hop Extension") while they are processed by all routers in IPv4 unless ordered otherwise.

### Rubric

```
Total 4 marks:
1) What extension headers are (1.5 marks)
2) Where they are located (1 mark)
3) Main advantage over IPv4 (1.5 marks)
```

### CERA concepts

#### CE07_C1 — 1.5 marks — role=`select_n`, min_count=`2`, legacy_mode=`ANY`

- **knowledge_point:** Define the purpose of IPv6 extension headers
- **target_criteria:** FULL = at least 2 parts (extend fixed header / optional network-layer info); PARTIAL = exactly 1; ABSENT = 0
- **facets:** ['extend fixed IPv6 header', 'additional optional network layer information']
- **variants:** ['headers that add extra features to the base IPv6 header', 'optional fields for extra network layer data', 'used to add more information beyond the standard header', 'extra headers for optional network layer functions']
- **partial:** exactly 1 part → 0.75 marks

#### CE07_C2 — 1.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** Identify the location of extension headers in an IPv6 packet
- **target_criteria:** any of: between fixed header and payload / between main header and upper-layer or transport header
- **facets:** ['between fixed header and payload', 'between main header and transport-layer header']
- **variants:** ['placed after the main header but before the data', 'located between the base header and the transport layer', 'inserted after the fixed header and before the upper-layer header']
- **partial:** None

#### CE07_C3 — 1.5 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** Explain the main advantage of extension headers over IPv4
- **target_criteria:** any of: appending new options without changing header / faster processing by intermediate devices (ONE advantage is FULL)
- **facets:** ['appending new options without changing the header', 'faster processing by intermediate devices']
- **variants:** ['allows adding new options without modifying the base header', 'intermediate routers process packets faster because they ignore most options', 'more efficient processing compared to IPv4', 'easier to add new features without header changes']
- **partial:** None

---

## CE08 · 4.0/4 · 3 concepts

### Question

WHAT are the challenges of Mobile Routing compared to routing in fixed and wired networks? Please NAME and DESCRIBE two challenges.

### Reference answer

Possible Challenges:
1.Adaptation: The network has to handle the dynamic positioning of the nodes/topology changes. Additionally, nodes can leave or join the network anywhere (within signal range) at any time.
2.Security: Interception of packets or injection of faulty packages is easily possible in wireless networks. This may necessitate encryption and authentication.
3.Medium Access Control: Wireless networks feature new possibilities for inference and collisions of the transmitted signals.
4.Quality of Service (QoS): Due to the rapidly changing network topology, imprecise network information, and resource constraints of participating nodes, it is challenging to provide the desired QoS.
5.Scalability: Since it is not possible to know the number of participating nodes beforehand, it is vital that routing protocols are capable of dealing with increasing network sizes.
6.Power Consumption: As most mobile devices are battery-powered, power consumption becomes an important optimization factor.

### Rubric

```
Total 4 marks:
1) Naming any 4 valid challenges (1 mark). Catalog: Adaptation, Security, MAC, QoS, Scalability, Power.
2) Describing challenge A (1.5 marks)
3) Describing challenge B (1.5 marks)
```

### CERA concepts

#### CE08_C1 — 1.0 marks — role=`select_n`, min_count=`4`, legacy_mode=`ANY`

- **knowledge_point:** The student names at least four distinct mobile routing challenges from the catalog.
- **target_criteria:** FULL = at least 4 distinct valid challenges named; PARTIAL = 1..3; ABSENT = 0
- **facets:** ['Adaptation', 'Security', 'Medium Access Control', 'Quality of Service', 'Scalability', 'Power Consumption']
- **variants:** ['node mobility', 'packet security', 'MAC issues', 'QoS constraints', 'network scaling', 'battery life']
- **partial:** 1–3 valid names → 0.5 marks

#### CE08_C2 — 1.5 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** The student provides a valid description for the first chosen challenge.
- **target_criteria:** any of: dynamic topology/node movement for Adaptation; packet interception/injection for Security; signal interference/collisions for MAC; topology/resource constraints for QoS; increasing network size for Scalability; battery-powered optimization for Power Consumption.
- **facets:** ['Adaptation: dynamic positioning or node mobility', 'Security: packet interception or injection', 'Medium Access Control: signal interference or collisions', 'Quality of Service: topology changes or resource constraints', 'Scalability: increasing network size', 'Power Consumption: battery-powered optimization']
- **variants:** ['nodes moving around', 'hackers stealing data', 'signals crashing into each other', 'hard to guarantee quality', 'network getting too big', 'saving energy for batteries']
- **partial:** Partial descriptions that capture the core mechanism earn 0.75 marks.

#### CE08_C3 — 1.5 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** The student provides a valid description for the second chosen challenge.
- **target_criteria:** any of: dynamic topology/node movement for Adaptation; packet interception/injection for Security; signal interference/collisions for MAC; topology/resource constraints for QoS; increasing network size for Scalability; battery-powered optimization for Power Consumption.
- **facets:** ['Adaptation: dynamic positioning or node mobility', 'Security: packet interception or injection', 'Medium Access Control: signal interference or collisions', 'Quality of Service: topology changes or resource constraints', 'Scalability: increasing network size', 'Power Consumption: battery-powered optimization']
- **variants:** ['nodes moving around', 'hackers stealing data', 'signals crashing into each other', 'hard to guarantee quality', 'network getting too big', 'saving energy for batteries']
- **partial:** Partial descriptions that capture the core mechanism earn 0.75 marks.

---

## CE09 · 4.0/4 · 2 concepts

### Question

What are the benefits and drawbacks of SDN compared to traditional networking, where each switch/router has to manage forwarding and routing on its own? Describe two benefits and two drawbacks in 1-2 sentences each.

### Reference answer

Benefits:
- Reduced complexity of the switches: They only have to act according to their flow tables and do not have to make any local routing decisions.
- Due to centralized routing, the routing can converge way faster to a global optimum than with decentralized routing because of a global view.
- Increased flexibility: We can update the routing logic on the fly, routers/switches are not limited to hard-coded routing algorithms anymore.

Drawbacks:
- High complexity of the control servers: They have to make all the routing decisions for the (sub)network and can therefore be a bottleneck.
- Centralized routing in distributed systems: The routing completely depends on the control server(s). To achieve better availability and fault tolerance, the number of control servers can be increased. However, this can lead to synchronization and consistency issues.

### Rubric

```
Total 4 marks:
1) Two benefits described (2 marks)
2) Two drawbacks described (2 marks)
```

### CERA concepts

#### CE09_C1 — 2.0 marks — role=`select_n`, min_count=`2`, legacy_mode=`ANY`

- **knowledge_point:** Describe two benefits of SDN compared to traditional networking
- **target_criteria:** FULL = at least 2 distinct benefits from the catalog; PARTIAL = exactly 1; ABSENT = 0
- **facets:** ['reduced switch complexity', 'faster routing convergence due to global view', 'increased flexibility via dynamic routing updates']
- **variants:** ["switches are simpler because they don't make routing decisions", 'centralized control allows faster network convergence', 'routing logic can be changed on the fly', 'no need for hard-coded routing algorithms', 'global view leads to better routing optimization']
- **partial:** exactly 1 benefit → 1.0 mark

#### CE09_C2 — 2.0 marks — role=`select_n`, min_count=`2`, legacy_mode=`ANY`

- **knowledge_point:** Describe two drawbacks of SDN compared to traditional networking
- **target_criteria:** FULL = at least 2 distinct drawbacks from the catalog; PARTIAL = exactly 1; ABSENT = 0
- **facets:** ['control server complexity and bottleneck risk', 'dependency on control server availability', 'synchronization and consistency issues in distributed control']
- **variants:** ['control servers can become a bottleneck', 'the network relies entirely on the control server', 'managing multiple control servers causes consistency problems', 'high complexity in the control plane', 'fault tolerance is difficult to manage']
- **partial:** exactly 1 drawback → 1.0 mark

---

## CE10 · 5.0/5 · 3 concepts

### Question

In the lecture you have learned about congestion control with TCP. Name the 2 phases of congestion control and explain how the Congestion Window (cwnd) and the Slow Start Threshold (ss_thresh) change in each phase (after initialization, where cwnd = 1 and ss_thresh = advertised window size) in 1-4 sentences total.

### Reference answer

Slow start (cwnd less than ss_thresh):
In the slow start phase, cwnd is incremented by one every time a segment is acknowledged. This results in an exponential growth as cwnd is essentially doubled after each Round Trip Time (RTT). This is done until either a packet is lost or ss_thresh is reached. When cwnd >= ss_thresh, the congestion avoidance phase is entered.
After a packet is lost / congestion the following adaption is made in both phases: ss_thresh = cwnd / 2. Then cwnd is reset to 1.

Congestion Avoidance (cwnd >= ss_thresh):
In the congestion avoidance phase, cwnd is incremented more slowly. There are different incrementation strategies, but they usually grow linearly, e.g. only increment cwnd by 1 after all sent segments have been acknowledged. This is done until a packet is lost. Typically, this means that cwnd less than ss_thresh and the slow start phase is entered again.
After a packet is lost / congestion the following adaption is made in both phases: ss_thresh = cwnd / 2. Then cwnd is reset to 1.

### Rubric

```
Total 5 marks:
1) Naming the 2 phases (1 mark)
2) Explaining cwnd/ss_thresh in Slow Start (2 marks)
3) Explaining cwnd/ss_thresh in Congestion Avoidance (2 marks)
```

### CERA concepts

#### CE10_C1 — 1.0 marks — role=`checklist`, legacy_mode=`ALL`

- **knowledge_point:** The student identifies the two phases of TCP congestion control as Slow Start and Congestion Avoidance.
- **target_criteria:** FULL requires naming both Slow Start and Congestion Avoidance
- **facets:** ['Slow Start', 'Congestion Avoidance']
- **variants:** ['Slow-start and congestion avoidance', 'Slow start phase and congestion avoidance phase', 'The two phases are slow start and congestion avoidance']
- **partial:** naming only one phase → 0.5 marks

#### CE10_C2 — 2.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** The student explains that in the Slow Start phase, the congestion window (cwnd) grows exponentially.
- **target_criteria:** any of: cwnd +1 per ACK / doubles each RTT / exponential growth
- **facets:** ['cwnd incremented by one per segment acknowledged', 'exponential growth', 'doubled after each RTT']
- **variants:** ['cwnd grows exponentially in slow start', 'cwnd doubles every round trip time', 'cwnd increases by one for every segment acknowledged', 'slow start causes rapid exponential window growth']
- **partial:** vague growth without mechanism → 1.0 mark

#### CE10_C3 — 2.0 marks — role=`synonym_set`, legacy_mode=`ANY`

- **knowledge_point:** The student explains that in the Congestion Avoidance phase, the congestion window (cwnd) grows linearly.
- **target_criteria:** any of: linear growth of cwnd / +1 after all segments ACKed
- **facets:** ['cwnd grows linearly', 'increment cwnd by 1 after all sent segments acknowledged']
- **variants:** ['cwnd increases linearly in congestion avoidance', 'window grows slowly by one per window of segments', 'linear growth of cwnd', 'cwnd increases by one after all segments are acknowledged']
- **partial:** vague growth without mechanism → 1.0 mark

---
