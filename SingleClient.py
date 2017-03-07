import socket
import pickle
import threading




class myThread(threading.Thread):
	""" Class used for overriding the default thread constructor, and running each thread.
	Constructor:
	type--String the type of the thread to be used in determining which function it 																																																																																																																																																																																													````````````````````````````````````````````````````should initiate.
	myIP--String the IP of this peer.
	port--the int port of this peer (the one that other peers will use as the second portion of 
	the connect)
	instance--that the thread should operate on the threadFunctions object. Currently only using
	one instance, the test instance of the peer network. The only place where this will likely be
	useful is if in the future we would like to make a single program connect to several networks
	at the same time (ie using one to connect to a network working on solving and another on 
	blockchain
	"""
	
	def __init__(self, type, myIP, port,instance):
		"""Overriding the default constructor"""
		threading.Thread.__init__(self)
		self.type = type
		self.myIP = myIP
		self.port = port
		self.instance = instance

	def run(self):
		if self.type  == "connector":
			print("c") # Test purposes, right now should get c r and a (t is the main thread)
			self.instance.connector(self.myIP,self.port)
		elif self.type == "receiver":
			print("r")
			self.instance.receiver()
		elif self.type == "transmitter":
			print("t")
			self.instance.transmitter()
		elif self.type == "acceptor":
			print("a")
			self.instance.acceptor(self.myIP, self.port)



class peer(object):
	"""The peer object, represents a peer on the network, and has fields:
	stringIP--the IP address of the peer
	intPort--the port of the peer to connect to
	Socket--defaults to None, but can (and should) be overridden for the socket of the peer
	fields:
	IP--stringIP
	port--intPort
	hasSock--boolean if the peer currently has a socket object, but may also be reverted to None
	to shut down a malfunctioning peer
	"""
	
	def __init__(self, stringIP, intPort, Socket = None):
		self.IP = stringIP
		self.port = intPort
			
		# If a socet is provided, use it. Otherwise, document that.
		#TODO Do we really need the bool hasSocket? Can't we just test for `self.socket is None`?
		if Socket is not None:
			self.Sock = Socket
			self.hasSock = True 
		else:
			self.hasSock = False
	
	
	def __str__(self):
		"""
		Returns a string representation of this peer including IPv4 address and whether a socket exists.
		
		Example with a socket:  Peer@192.168.1.4(S)
		Example without socket: Peer@192.168.1.4
		"""
		
		text = "Peer@" + self.IP
		if self.hasSock:
			text += "(S)"
		
		return text
	
	
	def sendable(self):
		""" Returns an instance of peer that is this peer, but a sendable version ie no socket"""
		return peer(self.IP,self.port)
	
	
	def sendPeer(self,sendToPeer):
		""" Used for just sending this peer to another node. """
		#not super necessary, I kind of wanted a different message for when just sending the
		#peer though...
		sendable = self.sendable()
		try:
			sendToPeer.Sock.send(pickle.dumps(sendable))
		except socket.error:
			print("error sending peer " + str((self.IP,self.port)) + " to " + str((sendToPeer.IP,sendToPeer.port)) + ".")
	
	
	def send(self,message):
		""" Send a message to this peer. """
		if self.hasSock == True:
			try:
				self.Sock.send(pickle.dumps(message))
			except socket.error:
				print("error sending message " + message + " to peer " + str((self.IP,self.port)))
				self.hasSock = None
				print("peer removed")
		
	def receive(self):
		""" Receive a message from this peer and print it. """
		if self.hasSock==True:
			try:
				return pickle.loads(self.Sock.recv(1024))
			except socket.error:
				print("error receiving message from " + str((self.IP,self.port)))
				self.hasSock = None
				print("peer removed")

	def addSock(self,Socket):
		""" Add a socket to the peer. """
		self.Sock = Socket 
		self.hasSock = True
		# Aware this looks suspiciously like a setter, I just didn't feel like not doing it...	
	
	
class threadFunctions(object):
	"""threadFunctions (probably a bad name) that the threads run the chatclient
	this is where the work gets done (think of an instance of this as a chatclient network
	although will mainly be usable for multiple instances only if you want to connect to 
	multiple networks and keep them separate in the future
	"""
	
	#TODO This feels fairly sloppy, but oh well... If someone wants to make a branch to make it
	# less sloppy feel free to
	def __init__(self):
		"""peerList--a list of all the current peer objects
			Stopper--used to stop everything
			printStopper--used as a poor-man's lock object to control printing output 
		"""
		self.peerList = []
		self.Stopper = False
		self.printStopper = False
	
	def printThis(self, message, type = None):
		""" Currently going to be used as a form of lock without actually using locks 
		(because locks are scary)"""
		
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
				self.printStopper = False
			
	

#	def checkIfNew(self,newPeer):
#		""" Check whether a given peer is known (already in the peerlist). """
#		
#		check = False
#		for knownPeer in self.peerList:
#			if newPeer.IP == knownPeer.IP and newPeer.port == knownPeer.port:
#					check = True
#		return check
	
	def connector(self,myIP, port):
		""" Goes through the list of peers and attempts to create a socket object to connect
		for them (for any peers that do not currently have a socket already)
		"""
		while not self.Stopper:
			for peers in list(self.peerList):
				if peers.hasSock == False: 
				# To me: don't you dare change this to if not peers.hasSock:
				# if I don't believe me, go to terminal, python, print(not None)
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					try:
						sock.connect((peers.IP,peers.port))
						peers.addSock(sock)
						self.printThis("connected to " + peers.IP)
						mePeer = peer(myIP,port)
						mePeer.sendPeer(peers)
					except socket.error:
						self.printThis("Couldn't connect to peer " + str((peers.IP,peers.port)))
						pass
						
										
	def receiver(self):
		""" Goes through all of the peers, and attempts to receive messages from all of the ones
		with a socket; however, currently I believe part of this may be related to my current error
		"""
		while not self.Stopper:
			for peers in list(self.peerList):
				if peers.hasSock == True: # To me: don't you dare change this to if peers.hasSock: actually this one should work but still...
					message = peers.receive()
					if isinstance(message,peer):
						newPeer = peer(message.IP,message.port) # Think this is the line that is the problem
						message = [newPeer] 
						# If they just sent me themselves I still want to check if
						# I have them already, and I'm basically double checking that 
						# they didn't have a sock by making a new one, and making the list 
						# just that new one
					if type(message) is list:
						self.printThis("received peerlist: " + str(message) + " from " + str((peers.IP,peers.port)))
						for newPeer in message:
							if newPeer not in self.peerList:
								self.peerList.append(newPeer)			
					else:
						self.printThis("from " +  str((peers.IP,peers.port)) + ": " + str(message))
					
					
	def transmitter(self):
		""" Goes through the list of peers and sends the message to them...	"""
		
		sendMessage = ""
		while sendMessage != "/exit":
			sendMessage = self.printThis("message> ","input")
			for peers in list(self.peerList):
				if peers.hasSock == True: # To me: don't you dare change this to if peers.hasSock: actually this one should work but still...
					peers.send(sendMessage)
		self.Stopper = True
	
	
	
	def acceptor(self,myIP, port):
		""" Waits for incoming connections and appends the new peers to list. """
		# Personally I feel	this is likely to be the largest part of my error...
		# I think using the address from the new connection does not work/give the send address
		# I'm probably going to have a version where I can connect it as a peer and not have a port
		# then on receive end have a new type int where it will send its port number, but that's
		# annoying... But I think this is currently what's messing it up...
		
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind((myIP,port))
		serverSocket.listen(0)
		while not self.Stopper:
			# Server socket just accepts incoming connections. When it does accept one,
			# Creates a new client socket for the actual communication.
			clientSocket, clientAddress = serverSocket.accept() # this section is the problem
			#print(str(clientSocket.getpeername()) + str(type(clientSocket.getpeername())) )
			thisPeer = peer(clientAddress[0],clientAddress[1],clientSocket)
			if thisPeer not in self.peerList:
				self.peerList.append(thisPeer)
			toSendList = []
			for peers in list(self.peerList):
				toSendList.append(peers.sendable())
			thisPeer.send(toSendList)
			#print("Accepted connection from {}".format(clientAddress))			
	

def getPort():
	return int(raw_input("Please enter the port number: "))


def getIP():
	""" Attempts to autodetect the user's LAN IP address, and falls back to manual
	entry when autodetect fails.
	
	See http://stackoverflow.com/questions/166506 for details. """
	
	# Send a packet to google who will reply to our IP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com', 53))    
	IP = s.getsockname()[0]
	
  # Make sure the detected IP looks valid, and if not fallback
	while IP[0:3] == "127" or IP == '':
		IP = raw_input("Unable to detect IP adress, please manually type your local IP in: ")
    
	print("Proposed IP is: {}".format(IP))
    
	response = raw_input("If you would like to use a different IP please type it here or press enter to continue: ")
	if response == "":
		return IP 
	return response
    
	
	
	
	
	
	
	

################################## MAIN PROGRAM BELOW ##################################

# print("Your port: ")
port = getPort();

myIP = getIP()

test = threadFunctions()
choice = raw_input("Type y then enter if you are starting a new network: ");
if choice != "y":
	print("Peer's port")
	peerOnePort = getPort()
	print("Same Peer's IP: ")
	peerOneIP = getIP()

	peerOne = peer(peerOneIP,peerOnePort)
	test.peerList.append(peerOne)
	

# This is initializing and starting (it works as it is, the functions themselves are what 
# aren't working right now...)

acceptorThread = myThread("acceptor",myIP,port,test)
receiverThread = myThread("receiver",myIP,port,test)
connectorThread = myThread("connector",myIP,port,test)
acceptorThread.start()
receiverThread.start()
connectorThread.start()

# Running the transmitter on the main thread
print("about to call transmitter")
test.transmitter()


# This should hopefully close a little nicer...
for peers in test.peerList():
	if peers.hasSock:
		peers.hasSock = False # Doing this before to try to prevent an error
		# peers.send() need to send something to initiate shutdown
		peers.Sock.shutdown(socket.SHUT_RDWR)
		peers.Sock.close()

		
