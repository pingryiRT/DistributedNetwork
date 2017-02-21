import socket
import sys
import pickle
import threading


# current problem my dictionary is not unique because my keys will be the same if two 
# are using the same ip which really messes up testing
#I'm still not sure if sockets can be used in the way I am attempting, but this will hopefully
# help me get closer to seeing


class myThread(threading.Thread):
""" Class used for overriding the default thread constructor, and running each thread.
Constructor:
type--String the type of the thread to be used in determining which function it should initiate.
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
			print("c") #test purposes, right now should get c r and a (t is the main thread)
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
			
			
#got a runtime error when iterating dicts told that forcing it into a list can help from 
# stackexchange

class peer():
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
			
		self.hasSock = False
		if Socket is not None:	#if you made it something other than none in call it will
			self.Sock = Socket  #be true
			self.hasSock = True 
	
	def sendable(self):
		""" returns an instance of peer that is this peer, but a sendable version ie no socket"""
		return peer(self.IP,self.port)
		
	def sendPeer(self,sendToPeer):
		"""used for just sending this peer to another node"""
		#not super necessary, I kind of wanted a different message for when just sending the
		#peer though...
		sendable = self.sendable()
		try:
			sendToPeer.Sock.send(pickle.dumps(sendable))
		except socket.error:
			print("error sending peer " + str((self.IP,self.port)) + " to " + str((sendToPeer.IP,sendToPeer.port)) + ".")
			pass
	
	def send(self,message):
	"""send a message to this peer"""
		if self.hasSock == True:
			try:
				self.Sock.send(pickle.dumps(message))
			except socket.error:
				print("error sending message " + message + " to peer " + str((self.IP,self.port)))
				self.hasSock = None
				print("peer removed")
		
	def receive(self):
	"""receive a message from this peer and print it"""
		if self.hasSock==True:
			try:
				return pickle.loads(self.Sock.recv(1024))
			except socket.error:
				print("error receiving message from " + str((self.IP,self.port)))
				self.hasSock = None
				print("peer removed")

	def addSock(self,Socket):
		"""add a socket to the peer"""
		self.Sock = Socket 
		self.hasSock = True
		#aware this looks suspiciously like a setter, I just didn't feel like not doing it...	
	
	
class threadFunctions():
	"""threadFunctions (probably a bad name) that the threads run the chatclient
	this is where the work gets done (think of an instance of this as a chatclient network
	although will mainly be usable for multiple instances only if you want to connect to 
	multiple networks and keep them separate in the future
	"""
	#this feels fairly sloppy, but oh well... If someone wants to make a branch to make it
	#less sloppy feel free to
	def __init__(self):
	"""peerList--a list of all the current peer objects
		Stopper--used to stop everything
		printStopper--used as a poor-man's lock object to control printing output 
	"""
		self.peerList = []
		self.Stopper = False
		self.printStopper = False
	
	def printThis(self, message, type = None):
	""" currently going to be used as a form of lock without actually using locks 
	(because locks are scary)"""
		if type == "input":
			while self.printStopper: 
				if self.printStopper == False:
					self.printStopper = True
					input = raw_input(message)
					self.printStopper = False
					return input
		else:
			while self.printStopper:
				if self.printStopper == False:
					self.printStopper = True
					print(message)
					self.printStopper = False
					break #in case it is true before breaks
	

	def checkIfNew(self,newPeer):
	"""Supposed to check if a given peer is known/already on the peerlist"""
		check = 0
		for knownPeers in list(self.peerList): #casting to a list so we don't have
		# errors with multiple threads
			if newPeer.IP == knownPeers.IP and newPeer.port == knownPeers.port:
					check = 1
		if check == 0:
			return True
		else:
			return False
				
	def connector(self,myIP, port):
	"""Goes through the list of peers and attempts to create a socket object to connect
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
					if peer.isInstance(message):
						newPeer = peer(message.IP,message.port) # think this is the line that is the problem
						message = [newPeer] 
						#If they just sent me themselves I still want to check if
						# I have them already, and I'm basically double checking that 
						# they didn't have a sock by making a new one, and making the list 
						# just that new one
					if type(message) is list:
						self.printThis("received peerlist: " + str(message) + " from " + (peers.IP,peers.port))
						for newPeers in list(message):
							if checkIfNew(newPeers):
								self.peerList.append(newPeers)			
					else:
						self.printThis("from " +  (peers.IP,peers.port) + ": " + str(message))
					
					
	def transmitter(self):
	"""Goes through the list of peers and sends the message to them...
	"""
		sendMessage = ""
		while sendMessage != "/exit":
			sendMessage = self.printThis("message> ","input")
			for peers in list(self.peerList):
				if peers.hasSock == True: # To me: don't you dare change this to if peers.hasSock: actually this one should work but still...
					peers.send(sendMessage)
		self.Stopper = True

	def acceptor(self,myIP, port):
	"""Waits for incoming connections and appends the new peers to list, personally I feel
	this is likely to be the largest part of my error...
	I think using the address from the new connection does not work/give the send address
	I'm probably going to have a version where I can connect it as a peer and not have a port
	then on receive end have a new type int where it will send its port number, but that's
	annoying... But I think this is currently what's messing it up...
	"""
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind((myIP,port))
		serverSocket.listen(0)
		while not self.Stopper:
			# Server socket just accepts incoming connections. When it does accept one,
			# Creates a new client socket for the actual communication.
			clientSocket, clientAddress = serverSocket.accept() # this section is the problem
			#print(str(clientSocket.getpeername()) + str(type(clientSocket.getpeername())) )
			thisPeer = peer(clientAddress[0],clientAddress[1],clientSocket)
			if self.checkIfNew(thisPeer):
				self.peerList.append(thisPeer)
			toSendList = []
			for peers in list(self.peerList):
				toSendList.append(peers.sendable())
			thisPeer.send(toSendList)
			#print("Accepted connection from {}".format(clientAddress))			
	

def getPort():
	return int(raw_input("Please enter the port number: "))
def getIP():
	return (raw_input("Please enter the IP: "))
	
print("Your port: ")
port = getPort();
print("Your IP: ")
myIP = getIP()

print("Peer's port")
peerOnePort = getPort()
print("Same Peer's IP: ")
peerOneIP = getIP()

peerOne = peer(peerOneIP,peerOnePort)

test = threadFunctions()
test.peerList.append(peerOne)

# this is initializing and starting (it works as it is, the functions themselves are what 
# aren't working right now...)
acceptorThread = myThread("acceptor",myIP,port,test)
receiverThread = myThread("receiver",myIP,port,test)
connectorThread = myThread("connector", myIP, port,test)
acceptorThread.start()
receiverThread.start()
connectorThread.start()


test.transmitter() #running the transmitter on the main thread

#this should hopefully close a little nicer...
for peers in test.peerList():
	if peers.hasSock:
		peers.hasSock = False #doing this before to try to prevent an error
		#peers.send() need to send something to initiate shutdown
		peers.Sock.shutdown(socket.SHUT_RDWR)
		peers.Sock.close()
		
