import os
from Node import *

# Every group has 2 receiver nodes and 1 sender node
topology2 = {'N1': {'N2': ('127.0.0.1', 20001), 'N4': ('127.0.0.1', 40001)},
			 'N2': {'N1': ('127.0.0.1', 10002), 'N3': ('127.0.0.1', 30002)},
			 'N3': {'N2': ('127.0.0.1', 20003), 'N5': ('127.0.0.1', 50003)},
			 'N4': {'N1': ('127.0.0.1', 10004), 'N5': ('127.0.0.1', 50004)},
			 'N5': {'N3': ('127.0.0.1', 30005), 'N4': ('127.0.0.1', 40005)}
			}

# TODO: ADD MORE LOGICAL TOPOLOGIES

if __name__ == '__main__':

	number_of_packets_per_node = 2
	number_of_nodes = int(sys.argv[1])
	period = float(sys.argv[2])

	nodes = dict()
	topology = topology2
	processes = dict()

	sequence_list = range(1, number_of_nodes * number_of_packets_per_node + 1)
	for i in xrange(number_of_nodes):
		packet_numbers = sorted(np.random.choice(sequence_list, size=number_of_packets_per_node, replace=False))
		node_name = 'N%d' % (i + 1)

		#nodes[node_name] = MulticastNode(node_name, packet_numbers, topology, period)
		nodes[node_name] = MulticastNode(node_name, packet_numbers, topology, period, logFile="LOG_" + node_name + ".txt")

		for j in packet_numbers:
			sequence_list.remove(j)

	for k, v in nodes.iteritems():
		pid = os.fork()
		if pid == 0:
			v.run()
			while not v.isClosed():
				time.sleep(1)
		else:
			print "{} - Child forked.".format(k)

	start = time.time()
	while not all(map(lambda x: x.isClosed(), nodes.values())):
		time.sleep(1)

	"""
	for k, v in nodes.iteritems():
		if v.isLocalOrderPreserved():
			print k, "- LOCAL ORDER IS PRESERVED."

		else:
			print k, "- LOCAL ORDER IS VIOLATED!!"
	"""

	print "\n#######################################################################"
	print "Took ", time.time() - start, "seconds."
	print "Experiment Done."
