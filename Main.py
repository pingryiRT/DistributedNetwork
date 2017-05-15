import socket

from WorkerThread import WorkerThread
from Network import Network

def getPort():
	"""
	Interactively determine a port. Proposes default, but allows overriding.
	"""
	
	DEFAULT = 12345
	
	port = raw_input("Default port: {}. Enter to continue or type an alternate. ".format(DEFAULT))
	
	if port == "":
		return DEFAULT
	
	return int(port)



def getOwnIP():
	""" Attempts to autodetect the user's LAN IP address, and falls back to manual
	entry when autodetect fails.
	
	See http://stackoverflow.com/questions/166506 for details. """
	
	# Send a packet to google who will reply to our IP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com', 53))
	IP = s.getsockname()[0]
	
	# Make sure the detected IP looks valid, and if not fallback
	while not validateIP(IP):
		IP = raw_input("Please enter a valid IP address: ")
	
	return IP



def validateIP(IP):
	'''	Validates an IP address before joining network'''
	sections = IP.split(".") #Creating sections list with IP address split up each period
	
	if len(sections) != 4: #Check for 3 periods
		return False
	
	for section in sections:
		if not section.isdigit(): #Making sure all contents are ints
			return False
		section = int(section)
		if section < 0 or section > 255: #validate range of the number
			return False
	
	if sections[0] == "127": #not loop-back address
		return False
	
	return True
				
######## Functions that could be moved to a separate interface module #####

def connector():
	""" Prompts user for data to connect to another peer, and establishes the connection.
	 
	    Warning. Uses global variable myNetwork."""
	
	peerIP = raw_input("Enter it your peer's IP address: ")
	peerPort = getPort()

	myNetwork.connect(peerIP, peerPort)



def name():
	"""
	Gives a peer a human-redable name identifier.
	The name will be accessible through peer.name
	
	Warning. Uses global variable myNetwork."""
	
	for peer in list(myNetwork.peerList):
		print(str(peer) + " " + str(myNetwork.peerList.index(peer)))
	index = int(raw_input("Please enter the index of the peer you would like to name: "))
	name = raw_input("Please enter the new name: ")
	myNetwork.peerList[int(index)].name = name


def approver():
	"""
	Moves a peer that has connected to this network instance from the
	unconfirmedList to peerList, where messages can be sent and received.
	
	Warning. Uses global variable myNetwork."""
	
	i = 0
	while i < len(myNetwork.unconfirmedList):
		peer = myNetwork.unconfirmedList[i]
		add = raw_input("y/n to add: " + str(peer) + " ").lower()
		if add == "y":
			myNetwork.approve(peer)
		
		i += 1


################################## MAIN PROGRAM BELOW ##################################

myIP = getOwnIP()
print ("Detected IP: " + myIP) 
print("I'll need your port.")
myPort = getPort()

# Initialize a network
myNetwork = Network(myIP, myPort)
adamNode = raw_input("Starting a new network? (y/N): ")

# Add the first peer if the user wants one
if adamNode == "" or adamNode[0].lower()!= "y":
	connector()
	

# Initialize and start the threads
WorkerThread("acceptor", myNetwork).start()
WorkerThread("receiver", myNetwork).start()


# Main program loop
command = None
while command != "/exit":
	command = raw_input("Please type your message, or enter a command, '/connect', '/approve', '/name', '/addPort', '/exit' then hit enter: \n")

	if command == "/connect":
		connector()
	elif command == "/approve":
		approver()
	elif command == "/name":
		name()
	elif command == "/addPort":
		myNetwork.addPort()
#	elif command == "/init":
#		myNetwork.manualInit()
	else:
		myNetwork.send(command)


# Close down the network
myNetwork.shutdown()
		
