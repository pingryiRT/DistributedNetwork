import socket
import select

from WorkerThread import WorkerThread
from ThreadFunctions import threadFunctions
from Peer import peer

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
acceptorThread = WorkerThread("acceptor",myIP,myPort,test)
receiverThread = WorkerThread("receiver",myIP,myPort,test)
#manualThread = WorkerThread("manualClient", myIP, myPort,test)
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

		
