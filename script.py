#!/usr/bin/python
#Burak Hocaoglu 2035988 M. Rasit Ozdemir 1942606
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink


class Topology(Topo):

	# The topology consists of 1 switch in the middle, 1 controller and 4 hosts in a star topology.

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

def perfTest():
	# Regression testing
	topo = Topology(n=5)
	net = Mininet(topo, host = CPULimitedHost, link = TCLink)
	net.start()
	#print "Displaying connections on net:"
	#dumpNodeConnections(net.hosts)
	#print "Testing bandwith between h1 and h4:"
	#h1, h4 = net.get('h1', 'h4')
	#net.iperf((h1, h4))
	#net.stop()

if __name__ == '__main__':
	setLogLevel('info')
#topos = { 'mytopo': ( lambda: Topology(n=5) ) }
	perfTest()

	i = 0
	while True:
		i += 1
