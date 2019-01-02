#!/usr/bin/python
#Burak Hocaoglu 2035988 M. Rasit Ozdemir 1942606
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
import numpy as np
import sys, os, time

class Topology(Topo):
	# The topology consists of 1 switch in the middle, 1 controller and 5 hosts in a star topology.
	def build(self, n=2):
		# Adding the switch in the middle of the network
		switch = self.addSwitch('s1')

		# Adding hosts with identical link configurations
		for h in range(n):
			# Each host gets 60% of system CPU time.
			host = self.addHost('h%s' % (h+1), cpu=.6/n)
			# Each link between hosts and the switch has 4 Mbit of bandwith, 10 ms of delay,
			# 10% of packet loss rate and 1000 packets as queuing limit. 
			self.addLink(host, switch, bw=4, delay='10ms', loss=10, max_queue_size=1000, use_htb=True)

def initTopo():
	# Regression testing
	topo = Topology(n=5)
	net = Mininet(topo, host = CPULimitedHost, link = TCLink)
	net.start()

def getFileName(topo_type):
	if topo_type == 2:
		return 'configuration2.xml'
	elif topo_type == 3:
		return 'configuration3.xml'
	elif topo_type == 4:
		return 'configuration4.xml'

if __name__ == '__main__':
	setLogLevel('info')

	packets_per_node = int(sys.argv[1])
	topo_type = int(sys.argv[2])
	period = float(sys.argv[3])
	poisson = float(sys.argv[4]) if sys.argv[4] != 'None' else None

	sequence_list = range(1, 5 * packets_per_node + 1)

	sequence_dict = {}

	for i in xrange(5):
		packet_numbers = sorted(np.random.choice(sequence_list, size=packets_per_node, replace=False))
		node_name = 'h%d' % (i + 1)
		sequence_dict[node_name] = packet_numbers
		for j in packet_numbers:
			sequence_list.remove(j)
	
	topo = Topology(n=5)
	net = Mininet(topo, host=CPULimitedHost, link=TCLink)
	net.start()

	'''
	for i in xrange(5):
		node = 'h%d' % (i + 1)
		pid = os.fork()
		if pid == 0:
			start_time = time.time()
			h_i = net.get(node)
			result = h_i.cmd('sudo python Node.py ' + node + ' ' + str(packets_per_node) + ' ' + ' '.join(map(str, sequence_dict[node])) + ' ' + str(period) + ' ' + getFileName(topo_type) + ' ' + poisson + ' LOG_' + node + '.txt')
			
			print result
			#while time.time() - start_time < 120:
			#	time.sleep(1)
		else:
			print "{} - child forked.".format(node)

	time.sleep(125)
	sys.exit(0)
	'''
	
	h1 = net.get('h1')
	h2 = net.get('h2')
	h3 = net.get('h3')
	h4 = net.get('h4')
	h5 = net.get('h5')

#	print h1.cmd('ifconfig -a') 
#	print h2.cmd('ifconfig -a')
#	print h3.cmd('ifconfig -a')
#	print h4.cmd('ifconfig -a')
#	print h5.cmd('ifconfig -a')

	h1.cmd('sudo python Node.py h1 ' + str(packets_per_node) + ' ' + ' '.join(map(str, sequence_dict['h1'])) + ' ' + str(period) + ' ' + getFileName(topo_type) + ' ' + poisson + ' LOG_h1.txt >> output1.txt &')
	h2.cmd('sudo python Node.py h2 ' + str(packets_per_node) + ' ' + ' '.join(map(str, sequence_dict['h2'])) + ' ' + str(period) + ' ' + getFileName(topo_type) + ' ' + poisson + ' LOG_h2.txt >> output2.txt &')
	h3.cmd('sudo python Node.py h3 ' + str(packets_per_node) + ' ' + ' '.join(map(str, sequence_dict['h3'])) + ' ' + str(period) + ' ' + getFileName(topo_type) + ' ' + poisson + ' LOG_h3.txt >> output3.txt &')
	h4.cmd('sudo python Node.py h4 ' + str(packets_per_node) + ' ' + ' '.join(map(str, sequence_dict['h4'])) + ' ' + str(period) + ' ' + getFileName(topo_type) + ' ' + poisson + ' LOG_h4.txt >> output4.txt &')
	h5.cmd('sudo python Node.py h5 ' + str(packets_per_node) + ' ' + ' '.join(map(str, sequence_dict['h5'])) + ' ' + str(period) + ' ' + getFileName(topo_type) + ' ' + poisson + ' LOG_h5.txt >> output5.txt &')
	
	time.sleep(330)
	sys.exit(0)
