import socket
import pickle
import select
import time

#from Peer import Peer

class Network(object):
	""" A connection to a chatclient network.
	
	A single instance of this class is sufficient for typical usage, although 
	multiple instances may be useful if you want to connect to multiple networks
	and keep them separate in the future, or simultaneously connect as multiple identities.
	"""
	
	#TODO This feels fairly sloppy, but oh well... If someone wants to make a branch to make it
	# less sloppy feel free to
	def __init__(self):
		"""peerList--a list of all the current Peer objects
			Stopper--used to stop everything
			printStopper--used as a poor-man's lock object to control printing output 
		"""
		self.unconfirmedList = []
		self.peerList = []
		self.Stopper = False
		self.printStopper = False
	
	"""def printThis(self, message, type = None):
		 Currently going to be used as a form of lock without actually using locks 
		(because locks are scary)

		# Wait for printing to be available again
		while self.printStopper:
			pass
		
		# Now do the actual printing
		if type == "input": # This is only if it is user-typed input
				self.printStopper = True
				input = raw_input(message)
				self.printStopper = False
				return input
		else:
				self.printStopper = True
				print(message)
				self.printStopper = False"""
	def printThis(self, message, type = None):
		if type == None:
			print(message)
		else:
			return raw_input(message)
			
		
			
	#one thread handling the send connect and accept, one handling the recv, one on auto accept
	
	def manualClient(self, myIP,port):
		while not self.Stopper:
			command = self.printThis("Please type your message, or enter a command, '/connect', '/accept', '/name', then hit enter:  \n",type = "input")

			
			if command == "/connect":
				self.connector(myIP,port)
			elif command == "/accept":
				self.manualAcceptor(myIP,port)
			elif command == "/name":
				self.name(myIP,port)
		#	elif command == "/init":
		#		self.manualInit()
			
			else:
				self.sender(myIP,port,command)	
	
	def name(self,myIP,port):
		for peers in list(self.peerList):
			print(str(peers) + " " + str(self.peerList.index(peers)))
		index = self.printThis("Please enter the index of the peer you would like to name: \n", type = "input")
		name = self.printThis("Please enter the name of the peer you would like to name: \n", type = "input")
		self.peerList[int(index)].name=name
		
		
			
	def manualInit(self):
		for peers in self.peerList:
			if peers.isBlocking == True:
				peers.Sock.setblocking(0)
				self.printThis(str(peers) + " set to non blocking")
				peers.isBlocking = False
	def sender(self, myIP,port, sendMessage):
	
		for peers in list(self.peerList):
			if peers.hasSock == True: # To me: don't you dare change this to if peers.hasSock: actually this one should work but still...
				peers.send(sendMessage)
		self.manualClient(myIP,port)
		
	def connector(self,myIP,port):
		new = self.printThis("Is this a new peer? y/n ", type = "input")
		if new == "y":
			peerIP = self.printThis("Please enter the new peer's IP: ", type = "input")
			peerPort = int(self.printThis("Please enter the new peer's port: ", type = "input"))
			newPeer = peer(peerIP, intPort = peerPort)
			self.peerList.append(newPeer)
		elif new == "n":
			strPeerList = []
			for peers in self.peerList:
				strPeerList.append(str(peers))
			peerIndex = self.printThis("Please identify the peer's index: ", type = "input")
			if self.peerList[peerIndex].port == None:
				peerPort = printThis("Please enter the peer's port: ", type = "input")
			newPeer = self.peerList[peerIndex]
		
				
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((newPeer.IP,newPeer.port))
			newPeer.addSock(sock)
			self.printThis("connected to " + newPeer.IP)
			newPeer.send(port)
		except socket.error:
			self.printThis("Couldn't connect to peer " + str((newPeer.IP,newPeer.port)))
	#	self.manualClient(myIP,port)
	
	def manualAcceptor(self,myIP, port):
		for peers in self.unconfirmedList:
			input = self.printThis("y/n to add: " + str(peers) + " ", type = "input")
			if input == "y":
				self.peerList.append(peers)
	#	self.manualClient(myIP,port)
				
	def acceptor(self,myIP, port):
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind((myIP,port))
		serverSocket.listen(0)
		while not self.Stopper:
			clientSocket, clientAddress = serverSocket.accept() # this section is the problem
			#print(str(clientSocket.getpeername()) + str(type(clientSocket.getpeername())) )
			thisPeer = peer(clientAddress[0],Socket = clientSocket)
		#	message = "0"
		#	while int(message) == 0:
		#		message = thisPeer.receive()
		#	thisPeer.port = int(message)
			if thisPeer not in self.peerList and thisPeer not in self.unconfirmedList:
				self.unconfirmedList.append(thisPeer)
			time.sleep(1)
			#print("Accepted connection from {}".format(clientAddress))	
	

						
										
	def receiver(self):
		""" Goes through all of the peers, and attempts to receive messages from all of the ones
		with a socket; however, currently I believe part of this may be related to my current error
		"""
		while not self.Stopper:
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
					self.printThis("received peerlist: " + str(messageStr) + " from " + str((peers.IP,peers.port)))			
				else:
					for peers in list(self.peerList):
						if peers.Sock == sockets:
							if peers.name != None:
								self.printThis("from " +  peers.name + ": " + str(message))
							else:
								self.printThis("from " +  str((peers.IP,peers.port)) + ": " + str(message))
					
			time.sleep(2)
