# Q-BURST live smoke — write your rubric
## Question (3 marks)
What is "frame bursting"? Also, give 1 advantage and disadvantage compared to the carrier extension.

## Reference answer
Frame bursting reduces the overhead for transmitting small frames by concatenating a sequence of multiple frames in one single transmission, without ever releasing control of the channel.
Advantage :it is more efficient than carrier extension as single frames not filled up with garbage.
Disadvantage :need frames waiting for transmission or buffering and delay of frames

## Your rubric
(paste into `exam.json` → `questions[0].rubric`; optional structured `rubric_items`)

Suggested coarse buckets if you want nesting test:
- Definition (1.5)
- Advantage + disadvantage vs carrier extension (1.5)

## 10 student answers
### BURST_00 — human 3.0/3 (high)
Frame bursting allows the sender to transmit concatenated sequence of multiple frames in single transmission , this is a solution to the problem of the improvement of the speed and its consequences to the length of the cable.
Advantage: It is more efficient than the carrier extension.
Disadvantage: with this you artificially increase the end to end delay, which can be a problem when the frame is critical.

### BURST_01 — human 3.0/3 (high)
T1.Allow sender to transmit concatenated sequence of multiple frames in single transmission .
2.Needs frames waiting for transmission .
3.Better efficiency .

### BURST_02 — human 3.0/3 (high)
The solution for maintaining a high collision domain diameter with increased transmission speed is to also increase the length of the sent frames. Frame bursting in this context means combining multiple small frames to one concatenated sequence of then increased length. This allows collision detection on the same length of line as before with increased speed because incread sequence length and higher transmission speed together mean a unchanged duration of transmission for every node in the network. 
We have to have a look on the advantages and disadvantages of frame bursting, especially in comparison to carrier extension. Carrier extension is another attempt to longer frames by adding more zero-padding bits to every frame with the same data section length as before:

-Advantage: In comparison to carrier extension, the long sequences in frame bursting contain more information, because no (or at least less) zero padding is needed. So the percentage of data per sequence is higher than it is with carrier extension, where most of the package consists of padding fields. So we have a higher efficiency, especially in respect of line usage.

-Disadvantage: Frame bursting needs time of waiting for every node before sending, because a certain amount of frames has to be collected to concatenate them to a sequence of minimum length. So the delay of sending is increased. One has also to think about the best trade-off between waiting time and frame collection, for example when to stop waiting and adding padding zeros.

### BURST_03 — human 2.25/3 (mid_high)
For a shared broadcast mode a tradeoff between distance and efficiency must be done.
One solution is frame bursting : In frame bursting the packet to be transmitted are put together, in a buffer. And after a specific 
wait time, there are 10 packets to be send together. If there is a error, the procedure will be repeated. 
If  the concatenated sequence of multiple packets has no error and all is good, the packets will be sent. 

+1 advantage : Better efficiency compared to 'carrier extension' because no additional "rubbish" data is added to the actual frame,
but in frame bursting it is waited for real data packets to be added in a buffer.

-1 disadvantage : The waiting time could cause delay, because f.e. a sender always has to wait till the buffer is full and till
the data transmission/send could be started.

### BURST_04 — human 2.25/3 (mid_high)
Frame bursting allows the sender to send a concatenated sequence of multiple frames in a single transmission. The efficiency is higher compared too carrier extension because the package length stays the same.

### BURST_05 — human 2.25/3 (mid_high)
In frame bursting, instead of the sender sending one packet at a time, it sends ten packets at once. The sender waits for the packets until it has ten packets ready to send. Put them together and just then send them.

Advantage: better performance than carrier extension, since more data is sent at a time.

Disadvantage: if there are only one or two packets to send, the sender will be waiting for the remain, to reach the 10 packets. If there are not 10 packets, after a timeout, the sender adds rubbish to the frame (so it has the needed size). So, the packets will be sent with a delay and with unnecessary data.

### BURST_06 — human 2.25/3 (mid_high)
In frame bursting, the sender can transmit multiple frames by concatenating them in single transmission.
The carrier extension provides really low efficiency with only 46byte  user data being transmitted using 512 byte.
Whereas the frame bursting provides a much better performance.

### BURST_07 — human 1.5/3 (mid)
Advantage: better efficiency
Disadvantage: needs frame waiting for transmission

### BURST_08 — human 1.5/3 (mid)
Frame bursting is a communication protocol feature for the principle of shared broadcast mode in gigabit ethernet. 
Advantage: frame bursting has a better efficiency than carrier extension. 
Disadvantage: needs frames waiting for transmission

### BURST_09 — human 0.0/3 (low)
Frame bursting is  a Transmission technique which is used to increase the Transmission rate of data Frames in the data link layer.
Advantage:the number of collision chances is reduced.
Disadvantage:Frame Bursting does not address the primary goal of reducing the header Overhead.

