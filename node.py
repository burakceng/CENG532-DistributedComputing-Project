import sys
import time
import heapq
import socket
import pickle
import threading

# PACKET CONTENT:
# - Source (address, port)
# - Destination (address, port) set
# - Timestamp
# - Vector clock of the sender node

# Send      - Message, R-ACK, D-ACK
# Receive   - send R-ACK
# Deliver   - send D-ACK to {sender} U {receiver group}

clock_mutex = threading.Lock()
queue_mutex = threading.Lock()

this_name = 'N1'
this_address = '10.0.0.1'
this_port = 5001

isDeliverable = False

this_clock = {'N1': 0, 'N2': 0, 'N3': 0,
			  'N4': 0, 'N5': 0, 'N6': 0 }

IP_table = {'N3': ('10.0.0.3', 7001), 
			'N4': ('10.0.0.4', 8001)}

ACK_table = {'N3': False, 
			 'N4': False }

messageQueue = []

def makePacket(dest, clock):
	global this_name
	# TODO: Construct the network packet suitable to the description above.

	return {'Source': this_name, 'Destination': dest, 'Timestamp': time.time(), 'Vector': clock}

def deliver(data):
	global this_clock, clock_mutex
	# TODO: synchronize own vector clock with the one provided via 'data' argument
	new_clock = dict()

	clock_mutex.acquire()
	for name, c in data.iteritems():
		new_clock[name] = this_clock[name] if this_clock[name] > c else c
	clock_mutex.release()

def multicast(sock, destGroup):
	global this_clock
	# TODO: Multicast the message to the receiver group

	ACK_table = dict.fromkeys(ACK_table, False)
	rGroup = destGroup.keys()
	temp_dict = dict(this_clock)
	msg = pickle.dumps(makePacket(rGroup, temp_dict))

	for i, name in destGroup:
		sock.settimeout(5.0)
		sock.sendTo(msg, destGroup[name])
		threading.Thread(group=None, target=OnReceive, name="OnReceive_" + name, args=(sock, name)).start()

def OnReceive(sock, name):
	global messageQueue
	# TODO: Normally for processing ACKs from the receiver group, if all ACKs are received send deliver command/message to corresponding receiver group
	data = pickle.loads(sock.recv())
	queue_mutex.acquire()
	heapq.heappush(messageQueue, (data['Timestamp'], data))
	queue_mutex.release()

if __name__ == '__main__':

	# TODO: main thread of processing; responsible for receiving thread creation and delivering of the packet content

	# The period of multicast
	period = float(sys.argv[1])

	# A control variable which will indicate the end of an experiment.
	packet_count = 0

	print this_name, "- Starting main thread..."
	print this_name, "- will send a packet per", period, "seconds."

	# For each link that a node has, there will be a new interface, i.e. a separate socket.
	socks = dict()
	for i, name in enumerate(IP_table):
		socks[name] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		socks[name].bind((this_address, this_port + i))

	time.sleep(period)
	while packet_count < 10:

		# Modify local vector clock
		clock_mutex.acquire()
		this_clock[this_name] += 1
		clock_mutex.release()

		# Initiate multicasting the vector clock with additional information. The content of a message is given above.
		multicast(socks, IP_table)

		# A multicast step in the experiment is completed.
		packet_count += 1
		time.sleep(period)

	# Cleanup...
	print this_name, "- End of operation. Killing..."
	sock.close()
