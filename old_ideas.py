	def heartbeatMulticast(self):
		heartbeat_msg = self.makePacket(16, 0)
		
		for node, intf in self.interfaces.iteritems():
			self.bcSock(heartbeat_msg, intf)

	def heartbeatReceive(self, peerAddr):
		while not all(self.ready.values()):
			data = pickle.loads(self.bcSock.recv(1024))
			t = data['Type']

			if t == 16:
				# Heartbeat message
				self.heartbeat_mtx.acquire()
				self.ready[data['Source']] = True
				self.heartbeat_mtx.release()

				self.createLog('{0} - Received HEARTBEAT from {1}'.format(self.node_name, data['Source']))

				heartbeat_msg = self.makePacket(32, 0)
				self.bcSock.sendto(heartbeat_msg, peerAddr)

			elif t == 32:
				# Heartbeat ACK message
				self.heartbeat_mtx.acquire()
				self.ready[data['Source']] = True
				self.heartbeat_mtx.release()

				self.createLog('{0} - Confirms that {1} is alive'.format(self.node_name, data['Source']))