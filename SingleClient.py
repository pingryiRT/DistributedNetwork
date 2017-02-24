import socket
import sys
import pickle
import threading

class myThread(threading.Thread):
#	def __init__(self,type): apparently python doesn't like overloaded functions... me sad
#		self.type = type
		
	def __init__(self, type, IP, port,instance):
		threading.Thread.__init__(self)
		self.type = type
		self.IP = IP
		self.port = port
		self.instance = instance
	
		
		
	def run(self):
		if self.type  == "connector":
			print("c")
			self.instance.connector(self.IP,self.port)
		elif self.type == "receiver":
			print("r")
			self.instance.receiver()
		elif self.type == "transmitter":
			print("t")
			self.instance.transmitter()
		elif self.type == "acceptor":
			print("a")
			self.instance.acceptor(self.IP, self.port)
#got a runtime error when iterating dicts told that forcing it into a list can help from 
# stackexchange	
class threadFunctions():
	def __init__(self):
		self.socketDict = {}
		self.peerDict= {}
	
	def connector(self,IP, port):
		while True:
			#print(self.peerDict)
			for keys in list(self.peerDict):
				checker = 0
				for socketKeys in list(self.socketDict):
					if socketKeys == keys:
						checker = 1
				if checker == 0:
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					try:
						sock.connect((keys, self.peerDict[keys]))
						self.socketDict[keys] = sock
						print("connected to " + keys)
						self.socketDict[keys].send(pickle.dumps({IP,port}))
					except socket.error:
						#print("error")
						pass
					
					
					
	def receiver(self):
		while True:
			for keys in list(self.socketDict):
			
				message = pickle.loads(self.socketDict[keys].recv(1024))
				if type(message) is dict:
					for newKeys in list(message):
						check = 0
						for knownKeys in list(self.peerDict):
							if newKeys == knownKeys:
								check = 1
						if check == 0:
							self.peerDict[newKeys] = message[newKeys]
				else:
					print(str(keys) + " " + str(message))
	def transmitter(self):
		sendMessage = ""
		while sendMessage != "/exit":
			sendMessage = (raw_input("message> "))
			for keys in list(self.socketDict):
				self.socketDict[keys].send(pickle.dumps(sendMessage))

	def acceptor(self,IP, port):
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serverSocket.bind((IP, port))
		serverSocket.listen(0)
		while True:
			# Server socket just accepts incoming connections. When it does accept one,
			# Creates a new client socket for the actual communication.
			clientSocket, clientAddress = serverSocket.accept()
			clientSocket.send(pickle.dumps(self.peerDict))
			self.socketDict[clientAddress] = clientSocket
			print("Accepted connection from {}".format(clientAddress))			
	
#	def addToPeer(a,b):
#		peerDict[a] = b
	
	



# Need one thread to 
# 
#
#

#TODO start init connection to first peer 


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

test = threadFunctions()
test.peerDict[peerOneIP] = peerOnePort



acceptorThread = myThread("acceptor",myIP,port,test)
receiverThread = myThread("receiver",myIP,port,test)
connectorThread = myThread("connector", myIP, port,test)
acceptorThread.start()
receiverThread.start()
connectorThread.start()
#transmitterThread = myThread("transmitter", myIP, port)
test.transmitter()

for keys in test.socketDict:
	test.socketDict[keys].close()
