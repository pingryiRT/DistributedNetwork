import socket

from WorkerThread import WorkerThread
from Network import Network
from Peer import Peer

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
	print("\nI'll need your first peer's IP")
	peerOneIP = raw_input("Enter it here: ")

	print("\nI'll need the same peer's port")
	peerOnePort = getPort()

	peerOne = Peer(peerOneIP,peerOnePort)
	myNetwork.peerList.append(peerOne)
	

# Initialize and start the threads
WorkerThread("acceptor", myNetwork).start()
WorkerThread("receiver", myNetwork).start()
#WorkerThread("manualClient", myNetwork).start()

# Running the transmitter on the main thread
myNetwork.manualClient()


# Close down the network
myNetwork.shutdown()
		
