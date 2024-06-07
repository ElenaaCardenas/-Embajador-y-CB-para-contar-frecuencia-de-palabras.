The objective of this project is to implement a word frequency counter system using the Ambassador
architecture alongside the Circuit Breaker model. The goal of the project is to efficiently compute the
frequency of words in a very long text by distributing the data into chunks and processing them in parallel
across multiple nodes. Follow the design delivered for homework 3.
Architecture Overview
Ambassador
1. The Ambassador will separate the text and will eliminate any non-word. Use
either strip or regular expressions to clean the text.
2. The Ambassador IS the server and will handle new connections.
3. For the Ambassador, design an identification system for the chunks of words
each node will count.
A proposal was provided in the class by following a pattern of a prefix of A,
B, C, and D for the chunk status, and 0 to n as a suffix to identify each
chunk. The meanings of the prefix are:
A = Available
B = Processing
C = Fail
D = Counted
E.g. “A1”.
4. The Ambassador will handle load balancing, and routing to the nodes.
 For load balancing use a dictionary to separate the list of words with
their respective identifier.
 For accepting new nodes use a dictionary to keep track of the available
nodes and the ones that already ended their task or exit with failure
(the status will be obtained by the outputs of circuit breaker).

5. When a new node is accepted by the Ambassador, a new thread and its respective
circuit breaker instance will be opened.
6. The Ambassador will be able to manage the outputs from the circuit breaker to
take decisions. Remember that no chunks must be left uncounted.
7. After all the loads have been counted, the Ambassador will merge the results
into one last list of word frequencies.
Circuit Breaker (CB)
1. All new connections with the Ambassador will be handled by circuit breaker.
Failure and success handling will be managed here.
Distributed Systems: 2nd Module

2. CB will receive at least two inputs, the identifier that the ambassador
assigned to the node, and the information of the connection to the node. The
list with the words to count is related to the identifier.
3. The errors that the CB will handle are up to you to decide, however, it’s
expected to handle at least disconnections and errors with the node.
Remember to set either a timeout or a series of “try’s” when handling the
errors from the node.
4. The outputs from CB must be handled by the Ambassador. Some failures must be
communicated in some way to the Ambassador. At least your CB architecture must
send the following outputs:
a. If there is a disconnection from the node, CB will send a status of
failure.
b. If the counting was successful, CB will send to the Ambassador both the
status and the counted list.
