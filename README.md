# CENG532-DistributedComputing-Project
*****************************************************************
THE TOPOLOGY and CONFIGURATION:
- In physical sense, the topology is a star network; however, the 
experiments will assume a different logical topology, which forms a 
ring network, i.e. Chord with each node having 2 neighbours only.

- For the sake of simplicity, the naming convention of the nodes 
in the network is set as 'Ni' for i-th node, e.g. 'N4' for the 4-th
node.

- Each node has a list of sequence numbers of equal length, where 
the numbers are randomly sampled from a range of numbers without 
replacement. For example, a topology of 5 nodes is given and an 
experiment will consist of 10 packets that are shared across 
all nodes in the network, i.e. each node will have 10 / 5 = 2 
packets to multicast its neighbours. The following is a valid 
example of how the sequence numbers can be shared:
	-- Sequence number range: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10} and 
	-- Node N1 has {3, 6}, 
	-- Node N2 has {7, 9}, 
	-- Node N3 has {2, 10}, 
	-- Node N4 has {1, 5} and 
	-- Node N5 has {4, 8}.
	In this case, N4 will be the initiator of whole experiment, 
	since it holds the smallest sequence number, 1.
*****************************************************************

*****************************************************************
NODE STRUCTURE:
- Each node fundamentally has the following:
	-- Id: an integer used in determining the port numbers as 
			a convention
	-- Name: the name of node in the network, a string
	-- Sequence List: a list of sequence numbers that the node 
						will be multicasting
	-- Interfaces: a dict of the neighbours' names mapped to 
					the particular interface for communication
	-- Socks: a dict of sockets to initiate communication with 
				the neighbours
	-- Broadcast Sock: a socket to broadcast heartbeat messages 
						to check whether a node is alive
	-- Clock: a dict of logical clocks for each node
	-- Queue: a queue of incoming packets that are to be 'delivered'
	-- and some more helper variables, data structures, locks etc.
*****************************************************************

*****************************************************************
PACKET CONTENT:
- Type: Packet type
		-- Multicast: 1
		-- Multicast ACK: 2
		-- Deliver Request: 4
		-- Deliver ACK: 8
		-- Heartbeat: 16
		-- Heartbeat ACK: 32
- Source: Node name
- Destination: A list of names of receiver nodes
- SequenceNumber: Sequence number of the packet
- Timestamp: Global timestamp w.r.to the CPU clock
- Vector: Logical clock of the sender node(advanced 1 unit in
			corresponding entry)
*****************************************************************

*****************************************************************
EXECUTION PRINCIPLE:
- Each node periodically sends multicast messages with its logical 
clock for synchronization to its all 'logical' neighbours, i.e. 
w.r.to the logical ring network.

- If the receiving group has received the message w/o any errors, 
then each node in that group will send a Multicast ACK message to 
indicate that it is ready to 'deliver' the message to its application 
layer.

- If the multicast initiator receive a Multicast ACK and the sequence 
numbers match, then the sender sets the corresponding neighbour entry 
of its ACK-table to True. When all entries of that table is set to 
True, then the initiator can multicast a Delivery Request to the 
receiving group of interest.

- Upon receiving the Delivery Request from the initiator, the receiving 
group will process the packet previously received through multicast 
and update their logical clocks accordingly. After having updated, 
each node in the receiving group will send a Delivery ACK message to 
the initiator indicating that it is ready to receive the next regular 
message, i.e. packet with type 1.
*****************************************************************

*****************************************************************
EXECUTION UNDER A PACKET LOSS:
- To be filled ...
*****************************************************************
