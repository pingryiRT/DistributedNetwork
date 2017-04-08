import socket
import pickle
import threading
import time
import select


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
		if self.type  == "manualClient":
			#print("MC") # Test purposes, right now should get c r and a (t is the main thread)
			self.instance.manualClient(self.myIP,self.port)
		elif self.type == "receiver":
		#	print("r")
			self.instance.receiver()
		elif self.type == "acceptor":
			#print("a")
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
	
	def __init__(self, stringIP, intPort = None, Socket = None, isBlocking = None):
		self.IP = stringIP
		self.port = intPort
		self.isBlocking = True
			
		# If a socket is provided, use it. Otherwise, document that.
		#TODO Do we really need the bool hasSocket? Can't we just test for `self.socket is None`? 
		if Socket is not None:
			self.Sock = Socket
			self.hasSock = True 
			
		else:
			self.hasSock = False
		self.name = None
	
	def __str__(self):
		"""
		Returns a string representation of this peer including IPv4 address, port and whether a socket exists.
		
		Example with a socket:  Peer@192.168.1.4 12345(S)
		Example without socket: Peer@192.168.1.4 12345
		"""
		
		text = "Peer@" + self.IP + " " + str(self.port)
		if self.hasSock:
			text += "(S)"
		return text
	
	
	
	def __eq__(self, other):
	  """ Compares this peer to another peer for equality. (for == operator) """
	  
	  return self.IP == other.IP and self.port == other.port
	
	
	def __neq__(self, other):
	  """ Compares the peer to another peer for inequality. (for != operator) """
	  
	  return not self == other
	
	
	
	
	def sendable(self):
		""" Returns an instance of peer that is this peer, but a sendable version ie no socket"""
		return peer(self.IP,self.port)
	
	
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
				print("hasSockTrue")
				
				message = pickle.loads(self.Sock.recv(1024))
				print message
			except socket.error:
				print("error receiving message from " + str((self.IP,self.port)))
				#self.hasSock = None
				print("peer not removed")

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
		self.peerList[int(index)].name= name
		
		
			
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
					if peers.name != None:
						self.printThis("from " +  peers.name + ": " + str(message))
					else:
						self.printThis("from " +  str((peers.IP,peers.port)) + ": " + str(message))
					
			time.sleep(2)

def getPort():
	"""
	Interactively determine a port. Proposes default of 12345, but allows overriding.
	"""
	
	port = raw_input("Default port: 12345. Enter to continue or type an alternate. ")
	
	if port == "":
		return 12345
	
	return int(port)



def getOwnIP():
	""" Attempts to autodetect the user's LAN IP address, and falls back to manual
	entry when autodetect fails.
	
	See http://stackoverflow.com/questions/166506 for details. """
	
	# Send a packet to google who will reply to our IP
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('google.com', 53))    
		IP = s.getsockname()[0]
	except:
		print("Afraid I can not detect your IP address, are you connected to the internet?")
		IP = "" #in the event no IP is detected... otherwise you can get a gaierror
  # Make sure the detected IP looks valid, and if not fallback
	while IP[0:3] == "127" or IP == '':
		IP = raw_input("Unable to detect IP adress, please manually type your local IP in: ")
    
    
	response = raw_input("Proposed IP: {}. Enter to continue or type an alternate. ".format(IP))
	
	if response == "":
		return IP 
	return response
    
	

#TODO We should have a separate validateIP function to call from getOwnIP and elsewhere as needed.
	
	
	
	
	

################################## MAIN PROGRAM BELOW ##################################

print("\nI'll need your IP address.")
myIP = getOwnIP()
print("\nI'll need your port.")
myPort = getPort()


test = threadFunctions()
adamNode = raw_input("Starting a new network? (y/n): ")[0].lower()

if adamNode != "y":
	print("\nI'll need your first peer's IP")
	peerOneIP = raw_input("Enter it here: ")

	print("\nI'll need the same peer's port")
	peerOnePort = getPort()

	peerOne = peer(peerOneIP,peerOnePort)
	test.peerList.append(peerOne)
	

# This is initializing and starting (it works as it is, the functions themselves are what 
# aren't working right now...)
acceptorThread = myThread("acceptor",myIP,myPort,test)
receiverThread = myThread("receiver",myIP,myPort,test)
#manualThread = myThread("manualClient", myIP, myPort,test)
acceptorThread.setDaemon(True)
receiverThread.setDaemon(True)
#manualThread.setDaemon(True)
acceptorThread.start()
receiverThread.start()
#manualThread.start()

# Running the transmitter on the main thread
#print("about to call transmitter")
#test.transmitter()
test.manualClient(myIP,myPort)

# This should hopefully close a little nicer...
for peers in test.peerList:
	if peers.hasSock:
		peers.hasSock = False # Doing this before to try to prevent an error
		# peers.send() need to send something to initiate shutdown
		peers.Sock.shutdown(socket.SHUT_RDWR)
		peers.Sock.close()

		
