import threading
from ThreadFunctions import threadFunctions


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
			#print("DEBUG: ManualClient thread is running.")
			self.instance.manualClient(self.myIP,self.port)
		elif self.type == "receiver":
			#print("DEBUG: Receiver thread is running.")
			self.instance.receiver()
		elif self.type == "acceptor":
			#print("DEBUG: Acceptor thread is running.")
			self.instance.acceptor(self.myIP, self.port)

