import sys
import time
import enum
import heapq
import socket
import pickle
import datetime
import traceback
import threading
import numpy as np
import xml.etree.ElementTree as ET

"""
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
- LocalOrder: the index (starts from 0) of the sequence number in 
				the node's sequence number list
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
- Every node multicasts a heartbeat message containing the smallest 
sequence number that they are waiting for. This will help a group to 
constitute a consensus on which sequence number should be multicast 
to preserve the total-order on the network by maintaining total-order 
in each sub-group.
*****************************************************************
"""

GLOBAL_PRINT_LOCK = threading.Lock()

class Mode(enum.Enum):
	IDLE = 0
	M_CAST = 1
	D_CAST = 2
	HEARTBEAT = 3
	FINISH = 4

	@staticmethod
	def getModeAsInt(mode):
		if mode == Mode.IDLE:
			return 0

		elif mode == Mode.M_CAST:
			return 1

		elif mode == Mode.D_CAST:
			return 2

		elif mode == Mode.HEARTBEAT:
			return 3

		elif mode == Mode.FINISH:
			return 4

class MulticastNode:

	def __init__(self, name, seq_list, topology, p=5.0, logFile=None, dpoisson=None):
		self.clock_mtx = threading.Lock()
		self.queue_mtx = threading.Lock()
		self.total_order_mutex = threading.Lock()
		self.logging_mtx = threading.Lock()
		self.heartbeat_mtx = threading.Lock()
		self.writer_lock = threading.Lock()
		self.statics_mtx = threading.Lock()

		self.id = int(name[-1])
		self.node_name = name
		self.finished = False
		self.closed = False
		self.seq_list = seq_list
		self.sequence_number = 0
		self.period = p
		self.dpoisson = dpoisson

		self.logging = logFile
		self.writer = None

		# State: (Mode, local order, msg number)
		self.ready = dict()
		self.state = (Mode.IDLE, -1, 0)
		self.ack_table = dict()
		self.del_ack_table = dict()
		self.comm_state = dict()

		self.delivered_nums = dict()
		self.socks = dict()
		self.sock_state = dict()
		self.clock = dict()
		self.queue = []

		self.packet_count = 0
		self.useful_payload = 0.0
		self.total_transmitted_payload = 0.0
		self.total_stable_delivery_time = 0.0

		self.finish_consensus = dict()
		self.stop_events = dict()

		self.network = topology
		self.interfaces = topology[self.node_name]
		for i, k in enumerate(topology):
			self.clock[k] = 0

		for node_ in self.interfaces:
			generated_port = 10000 * self.id + int(node_[-1])
			self.socks[node_] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socks[node_].bind(("10.0.0." + str(self.id), generated_port))
			self.delivered_nums[node_] = []
			self.comm_state[node_] = False
			self.ack_table[node_] = False
			self.del_ack_table[node_] = False
			self.sock_state[node_] = True
			self.ready[node_] = False
			self.stop_events[node_] = threading.Event()

#			self.interfaces[node_] = ("127.0.0.1", 10000*int(node_[-1]) + self.id)
			self.finish_consensus[node_] = dict()
			for num in self.seq_list:
				self.finish_consensus[node_][str(num)] = False

		self.bcSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bcSock.bind(('127.0.0.1', self.id * 10000))

	def setClock(self, name_, clock_, init_):
		self.clock[name_] = clock_

	def updateClock(self, incoming):
		self.clock_mtx.acquire()
		for n, c in incoming.iteritems():
			if c > self.clock[n]:
				self.clock[n] = c
		self.clock_mtx.release()

	def makePacket(self, pType, seq, order=None, dest=None, old_stamp=None):
		data = {'Type': pType, 
				'Source': self.node_name, 
				'Destination': self.interfaces.keys() if pType == 1 else dest, 
				'SequenceNumber': seq, 
				'LocalOrder': self.sequence_number if not order else order, 
				'Timestamp': time.time() if not old_stamp else old_stamp, 
				'Vector': self.clock }

		return pickle.dumps(data)

	def multicast(self, mType, num, order=None):
		self.state = (Mode.M_CAST, self.sequence_number if not order else order, num)
		serialized_msg = self.makePacket(mType, num, order)
		for node in self.interfaces:
			self.socks[node].settimeout(4 * self.period)
			self.socks[node].sendto(serialized_msg, self.interfaces[node])
			self.createLog("{0} - MCAST {1} to node {2}.".format(self.node_name, num, node))

			self.statics_mtx.acquire()
			self.packet_count += 1
			self.total_transmitted_payload += sys.getsizeof(serialized_msg)
			self.statics_mtx.release()

			time.sleep(0.5)

	def deliver(self):
		if not self.queue:
			return

		self.queue_mtx.acquire()
		deliverable = heapq.heappop(self.queue)
		self.queue_mtx.release()

		if self._alreadyProcessed(deliverable[2]['SequenceNumber']):
			return

		delivery_stamp = time.time()
		self.createLog("{0} - Delivering {1}, Received at: {2}...".format(self.node_name, deliverable[2]['SequenceNumber'], 
																				deliverable[2]['Timestamp']))

		self.statics_mtx.acquire()
		self.useful_payload += sys.getsizeof(pickle.dumps(deliverable[2]))
		self.total_stable_delivery_time += delivery_stamp - deliverable[2]['Timestamp']
		self.statics_mtx.release()

		self.updateClock(deliverable[2]['Vector'])

		self.delivered_nums[deliverable[2]['Source']].append((deliverable[0], deliverable[1], deliverable[2]['SequenceNumber'], delivery_stamp))

		self.createLog("{0} - Deliver {1} OK - Source: {2}.".format(self.node_name, deliverable[2]['SequenceNumber'], deliverable[2]['Source']))
		self.createLog('{} - DELIVERY LOGGING...'.format(self.node_name))

		self.logging_mtx.acquire()
		self.logDeliveredMsgs()
		self.logging_mtx.release()

	def onReceive(self, sockHandle, peerName, peerAddr):

		def _alreadyInQueue(seq_num, msg_list):
			for entry in msg_list:
				if entry[2]['SequenceNumber'] == seq_num:
					return True

			return False

		while True:

			if self.stop_events[peerName].is_set():
				break

			if self.finishConsensus():
				self.state = (Mode.FINISH, self.state[1], self.state[2])

			try:

				rawData = sockHandle.recv(1024)
				data = pickle.loads(rawData)
				t = data['Type']

				if t == 1:
					# Regular Multicast message with data
					if self.state[0] == Mode.D_CAST:
						continue

					receipt = time.time()
					if not self._alreadyProcessed(data['SequenceNumber']) and not _alreadyInQueue(data['SequenceNumber'], self.queue):
						self.queue_mtx.acquire()
						heapq.heappush(self.queue, (data['Timestamp'], data['LocalOrder'], data))
						self.queue_mtx.release()

						self.createLog("{0} - M_CAST Received {1} USEFUL - Stamp: {2}, Diff: {3}".format(self.node_name, data['SequenceNumber'], 
											data['Timestamp'], receipt - data['Timestamp']))

						self.statics_mtx.acquire()
						self.useful_payload += sys.getsizeof(rawData)
						self.statics_mtx.release()

					serialized_msg = self.makePacket(2, data['SequenceNumber'])
					sockHandle.sendto(serialized_msg, peerAddr)

					self.statics_mtx.acquire()
					self.packet_count += 1
					self.total_transmitted_payload += sys.getsizeof(serialized_msg)
					self.statics_mtx.release()

					self.createLog("{0} - M_CAST ACK {1} Sent to {2}".format(self.node_name, data['SequenceNumber'], data['Source']))

				elif t == 2:
					# Regular Multicast ACK
					if self.sequence_number >= len(self.seq_list):
						to_be_checked = self.state[2]

					else:
						to_be_checked = self.seq_list[self.sequence_number]

					receipt = time.time()
					if data['SequenceNumber'] != to_be_checked:
						self.createLog("{} - Packet Loss. Retransmission...".format(self.node_name))

						serialized_msg = self.makePacket(1, to_be_checked)
						sockHandle.sendto(serialized_msg, peerAddr)

						self.statics_mtx.acquire()
						self.packet_count += 1
						self.total_transmitted_payload += sys.getsizeof(serialized_msg)
						self.statics_mtx.release()

					else:
						if not self.ack_table[peerName]:
							self.statics_mtx.acquire()
							self.useful_payload += sys.getsizeof(pickle.dumps(data))
							self.statics_mtx.release()

						self.ack_table[peerName] = True

						self.createLog("{0} - M_CAST ACK Received {1} - Stamp: {2}, Diff: {3}".format(self.node_name, data['SequenceNumber'], 
											receipt, receipt - data['Timestamp']))

						if all(self.ack_table.values()):
							# All-or-None mechanism
							self.state = (Mode.D_CAST, self.sequence_number, data['SequenceNumber'])
							self.multicast(4, data['SequenceNumber'])

				elif t == 4:
					# Deliver Request
					receipt = time.time()
					self.createLog("{0} - DELIVER Received {1} USEFUL - Stamp: {2}, Diff: {3}".format(self.node_name, data['SequenceNumber'], 
									receipt, receipt - data['Timestamp']))

					self.total_order_mutex.acquire()
					self.deliver()
					self.total_order_mutex.release()

					time.sleep(1.0)

					serialized_msg = self.makePacket(8, data['SequenceNumber'])
					sockHandle.sendto(serialized_msg, peerAddr)

					self.statics_mtx.acquire()
					self.packet_count += 1
					self.total_transmitted_payload += sys.getsizeof(serialized_msg)
					self.statics_mtx.release()

				elif t == 8:
					# Deliver Request ACK
					if self.state[0] == Mode.M_CAST:
						continue

					receipt = time.time()

					if not self.del_ack_table[data['Source']]:
						self.statics_mtx.acquire()
						self.useful_payload += sys.getsizeof(pickle.dumps(data))
						self.statics_mtx.release()

					self.del_ack_table[data['Source']] = True
					self.createLog("{0} - DELIVER ACK Received from {1} {2} USEFUL - Stamp: {3}, Diff: {4}".format(self.node_name, data['Source'], 
																					data['SequenceNumber'], receipt, receipt - data['Timestamp']))

					self.finish_consensus[data['Source']][str(data['SequenceNumber'])] = True

					if all(self.ack_table.values()) and all(self.del_ack_table.values()):
						# All-or-None mechanism
						self.ack_table = dict.fromkeys(self.ack_table, False)
						self.del_ack_table = dict.fromkeys(self.del_ack_table, False)

						self.total_order_mutex.acquire()
						self.sequence_number += 1
						self.state = (Mode.M_CAST, self.sequence_number, 
									data['SequenceNumber'] if len(self.seq_list) <= self.sequence_number else self.seq_list[self.sequence_number])
						self.total_order_mutex.release()

						consent = True
						for node, cons in self.finish_consensus.iteritems():
							if not cons.get(str(data['SequenceNumber'])):
								consent = False
								break

						if consent:
							self.createLog("{0} - Gave consent that {1} is total-order delivered.".format(self.node_name, data['SequenceNumber']))

				elif t == 16:
					# Heartbeat message
					self.heartbeat_mtx.acquire()
					self.ready[data['Source']] = True
					self.heartbeat_mtx.release()

					self.createLog('{0} - Received HEARTBEAT from {1}'.format(self.node_name, data['Source']))

					heartbeat_msg = self.makePacket(32, 0)
					self.bcSock.sendto(heartbeat_msg, peerAddr)

					self.statics_mtx.acquire()
					self.packet_count += 1
					self.total_transmitted_payload += sys.getsizeof(heartbeat_msg)
					self.useful_payload += sys.getsizeof(heartbeat_msg)
					self.statics_mtx.release()

				elif t == 32:
					# Heartbeat ACK message
					self.heartbeat_mtx.acquire()
					self.ready[data['Source']] = True
					self.heartbeat_mtx.release()

					self.createLog('{0} - Confirms that {1} is alive'.format(self.node_name, data['Source']))

			except socket.timeout as e:

				if self.state[0] == Mode.HEARTBEAT:
					continue

				elif self.state[0] == Mode.M_CAST:
					self.createLog("{0} - Socket Timeout in M_CAST mode. Destination: {1}".format(self.node_name, peerName))
					serialized_msg = self.makePacket(1, data['SequenceNumber'], order=data['LocalOrder'], old_stamp=data['Timestamp'])
					sockHandle.sendto(serialized_msg, peerAddr)

					self.statics_mtx.acquire()
					self.packet_count += 1
					self.total_transmitted_payload += sys.getsizeof(serialized_msg)
					self.statics_mtx.release()

				elif self.state[0] == Mode.D_CAST:
					self.createLog("{0} - Socket Timeout in D_CAST mode. Destination: {1}".format(self.node_name, peerName))
					serialized_msg = self.makePacket(4, data['SequenceNumber'], order=data['LocalOrder'])
					sockHandle.sendto(serialized_msg, peerAddr)

					self.statics_mtx.acquire()
					self.packet_count += 1
					self.total_transmitted_payload += sys.getsizeof(serialized_msg)
					self.statics_mtx.release()

				elif self.state[0] == Mode.FINISH:
					self.createLog("{} - DONE.".format(self.node_name))

			except Exception as e:
				print traceback.format_exc()
				raise e
		return

	def logDeliveredMsgs(self):
		logger = open('DeliveryLog_' + self.node_name + ".txt", 'w')

		logger.write("--------------------------------------------------\n")
		logger.write(str(datetime.datetime.now()) + '\n')
		logger.write("--------------------------------------------------\n")

		for k, v in self.delivered_nums.iteritems():
			for item in v:
				logger.write("From: {0} - TimeStamp: {1} - Sequence Number: {2} - Delivered: {3}.\n".format(k, item[0], item[2], item[3]))

		logger.write('\n')
		logger.close()

	def logStatistics(self, params):
		#logger = open('Statistics_' + self.node_name + ".txt", 'a')

		print "--------------------------------------------------\n"
		print str(datetime.datetime.now()) + '\n'
		print "PPN: {0}, CONF: {1}, Period: {2}, Poisson: {3}".format(params[0], params[1], params[2], params[3])
		print "--------------------------------------------------\n"

		_count, _upayload, _tpayload, _total_time = this_node.getStatistics()

		print "Node:          ", name
		print "Count:         ", _count
		print "Useful payload:", _upayload
		print "Total payload: ", _tpayload
		print "Total time:    ", _total_time
		print "Avg. time:     ", float(_total_time) / _count

		print '\n'
		#logger.close()

	def run(self):
		self.createLog("{0} - Starting with {1}...".format(self.node_name, self.seq_list))

		for node, peer in self.interfaces.iteritems():
			threading.Thread(group=None, target=self.onReceive, name="onReceive_" + node, args=(self.socks[node], node, peer)).start()
		o = 0
		for num in self.seq_list:
			self.clock_mtx.acquire()
			self.clock[self.node_name] += 1
			self.clock_mtx.release()
			
			try:
				self.multicast(1, num, order=o)
			except Exception as e:
				print traceback.format_exc()
				raise e
			if self.dpoisson:
				#poisson_delay = np.random.poisson(self.period + o * self.period)
				poisson_delay = 1. / np.random.poisson(self.dpoisson)
				time.sleep(poisson_delay)

			else:
				time.sleep(self.period)

			o += 1
		time.sleep(300)

	def finish(self, peerName):
		self.createLog("{} - Finished. Cleaning up...".format(self.node_name))

		if all(self.comm_state.values()):
			self.finished = True
			self.closed = True
			self.bcSock.close()

	def finishConsensus(self):
		for k, v in self.finish_consensus.iteritems():
			if not all(v.values()):
				return False

		return True

	def createLog(self, log):
		global GLOBAL_PRINT_LOCK

		if self.logging:
			self.writer_lock.acquire()
			self.writer = open(self.logging, 'a')
			self.writer.write(log + "\n")
			self.writer.close()
			self.writer_lock.release()

		else:
			GLOBAL_PRINT_LOCK.acquire()
			print log
			GLOBAL_PRINT_LOCK.release()

	def isClosed(self):
		return self.closed

	def killThreads(self):
		print "STOPPING THREADS"
		for n in self.interfaces:
			self.stop_events[n].set()

	def _alreadyProcessed(self, seq_num):
		for n, v in self.delivered_nums.iteritems():
			for item in v:
				if item[2] == seq_num:
					return True

		return False or (seq_num in self.seq_list)

	def getStatistics(self):
		self.statics_mtx.acquire()
		saved_count = self.packet_count
		saved_useful_payload = self.useful_payload
		saved_total_payload = self.total_transmitted_payload
		saved_total_time = self.total_stable_delivery_time
		self.statics_mtx.release()

		return saved_count, saved_useful_payload, saved_total_payload, saved_total_time

def parseTopology(topoFile):
	topology = dict()
	topo = ET.parse(topoFile).getroot()
	for node in topo:
		name = node.attrib['name']
		topology[name] = dict()
		for intf in node:
			intf_to = intf.attrib['name']
			ip_addr = intf.attrib['IP']
			port_no = int(intf.attrib['port'])
			topology[name][intf_to] = (ip_addr, port_no)

	return topology

if __name__ == '__main__':
	name = sys.argv[1]
	count = int(sys.argv[2])
	slist = map(int, sys.argv[3:count + 3])
	period = float(sys.argv[count + 3])
	topoFile = sys.argv[count + 4]
	dpoisson = float(sys.argv[count + 5]) if sys.argv[count + 5] != 'None' else None
	logFile = sys.argv[count + 6]
	topology = parseTopology(topoFile)
	this_node = MulticastNode(name, slist, topology, period, logFile, dpoisson)
	this_node.run()
	this_node.killThreads()
	this_node.logStatistics((count, topoFile, period, dpoisson))
	sys.exit(0)
