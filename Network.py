import socket
import pickle
import select


from Peer import Peer

class Network(object):
	""" A connection to a chatclient network.
	
	A single instance of this class is sufficient for typical usage, although 
	multiple instances may be useful if you want to connect to multiple networks
	and keep them separate in the future, or simultaneously connect as multiple identities.
	"""
	
	
	
	def __init__(self, ip, port):
		"""
		peerList -- a list of all the current Peer objects, which are used to send and receive 
		messages
		Stopper -- used to stop everything
		printStopper -- used as a poor-man's lock object to control printing output 
		ip -- This hosts own IP address as seen by peers on the network
		port -- The port on which this host is running a server
		server -- the server socket object of the network (for other nodes to connect to)
		A name object can be added to peers as a means of providing a unique id
		unconfirmedList -- contains peers that have not been manually accepted by the user
		and are not yet used to send and receive messages
		"""
		
		self.unconfirmedList = []
		self.peerList = []
		self.printStopper = False
		self.ip = ip
		self.port = port
		
		# Create the server socket and make it listen
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind((self.ip, self.port))
		self.server.listen(0)
      	
	
	def printThis(self, message, type = None):
		"""
		Very simple method -- if type is none it prints message, otherwise it returns 
		raw user input with message being used as a prompt
		"""
		if type == None:
			print(message)
		else:
			return raw_input(message)
	
	
	
	def name(self):
		"""
		Gives a peer a unique name identifier (determined by the input of the user)
		The name will be accessible through peer.name
		"""
		for peers in list(self.peerList):
			print(str(peers) + " " + str(self.peerList.index(peers)))
		index = self.printThis("Please enter the index of the peer you would like to name: \n", type = "input")
		name = self.printThis("Please enter the name of the peer you would like to name: \n", type = "input")
		self.peerList[int(index)].name=name
	
	
			
	def addPort(self):
		"""
		Adds a server port to a peer, the peer which has the port added, and the port number
		to be added is determined with user input
		"""
		for peers in list(self.peerList):
			print(str(peers) + " " + str(self.peerList.index(peers)))
		index = int(self.printThis("Please enter the index of the peer you would like to add a port to: \n", type = "input"))
		port = int(self.printThis("Please enter the port for the peer: \n", type = "input"))
		self.peerList[index].port = port
	
	
	def sender(self, sendMessage):
		"""
		Sends message to all peers with a socket
		"""
		for peers in list(self.peerList):
			if peers.hasSock == True: # To me: don't you dare change this to if peers.hasSock: actually this one should work but still...
				peers.send(sendMessage)

	
	def connect(self, ip, port):
		""" Initializes a connection with a socket to a given ip and port, and then creates a 
		new peer object, appends it to the peerList, and adds that socket to the new peer """
		
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((ip, port))
			
		except socket.error:
			self.printThis("Couldn't connect to peer " + str((ip, port)))
		
		finally:
			newPeer = Peer(ip, port)
			self.peerList.append(newPeer)
			newPeer.addSock(sock)
			self.printThis("connected to " + ip)
			
			newPeer.send(self.port)
	
	
	
	def manualAcceptor(self):
		"""
		Moves a peer that has attempted to connect to this network instance from the 
		unconfirmedList to peerList, where messages can be sent and received
		"""
		i = 0
		while i < len(self.unconfirmedList):
			peer = self.unconfirmedList[i]
			input = self.printThis("y/n to add: " + str(peer) + " ", type = "input")
			if input == "y":
				self.peerList.append(peer)
				self.unconfirmedList.remove(peer)

	
	def acceptor(self):
		"""
		Automatically accepts incoming peer conncections, but leaves them in the unconfirmedList
		where messages they attempt to send are not deserialized, and any messages sent by the 
		user will not be forwarded to them
		"""
		clientSocket, clientAddress = self.server.accept() 
		thisPeer = Peer(clientAddress[0],Socket = clientSocket)
		if thisPeer not in self.unconfirmedList:
			self.unconfirmedList.append(thisPeer)
		
		#print("Accepted connection from {}".format(clientAddress))
	
	
	
	def receiver(self):
		""" Goes through all of the peers, and attempts to receive messages from all of the ones
		with a socket
		"""
		sockList=[]
		for peers in self.peerList:
			if peers.hasSock == True:
				sockList.append(peers.Sock)
		receiveOpen,writeOpen,errorSocks = select.select(sockList,[],[],2)#kind of bad, 
			# but I don't currently need to check for writable/errors... if I need to I will later
			# timeout is in 2 seconds
		for sockets in receiveOpen:
			message = pickle.loads(sockets.recv(1024))
			if type(message) is list:
				messageStr = []
				for peers in message:
					messageStr.append(str(peers))
				self.printThis("received peerlist: " + str(messageStr) + " from " + str((peers.ip, peers.port)))
			
			else:
				for peers in list(self.peerList):
					if peers.Sock == sockets:
						if str(message) == "/exit":
							peers.Sock = None
							peers.hasSock = None
							if peers.name != None:
								self.printThis(peers.name + " exited.")
							else:
								self.printThis(str((peers.IP,peers.port)) + " exited.")
						elif peers.name != None:
							self.printThis("from " + peers.name + ": " + str(message))
						else:
							self.printThis("from " + str((peers.IP,peers.port)) + ": " + str(message))
				
		
	
	
	
	def shutdown(self):
		""" Gracefully closes down all sockets for this peer"""
		
		for peer in self.peerList:
			if peer.hasSock:
				peer.hasSock = False # Doing this before to try to prevent an error
				# peers.send() need to send something to initiate shutdown
				peer.Sock.shutdown(socket.SHUT_RDWR)
				peer.Sock.close()

