from Network import Network
from Peer import Peer

class Interface(object):
	
	def __init__(self, tagDict, network = None):
		self.network = network
		self.tagDict = tagDict
		
	def run():
		command = None
		while command != "/exit":
			command = raw_input("Please type your message, or enter a command, '/connect', '/accept', '/name', '/addPort', '/exit' then hit enter:  \n")
			if command == "/connect":
				connector()
			elif command == "/accept":
				self.network.manualAcceptor()
			elif command == "/name":
				self.network.name()
			elif command == "/addPort":
				self.network.addPort()
			else:
				self.network.sender(command)

		# Close down the network
		self.network.shutdown()
		self.network = None
	
	############### INTERFACE FUNCTION SECTION ###############
	
	#######Needed for network creation#########
	
	def getOwnIP(self):
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
	
	
	def validateIP(self, IP):
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
	
	
	
	def getPort(self):
	"""
	Interactively determine a port. Proposes default, but allows overriding.
	"""
	
	DEFAULT = 12345
	
	port = raw_input("Default port: {}. Enter to continue or type an alternate. ".format(DEFAULT))
	
	if port == "":
		return DEFAULT
	
	return int(port)
	
	##########END OF NETWORK CREATION #############
	
	
	
	
	########## NEEDED FOR NETWORK FUNCTION ##########
	
	def connector(self):
	""" Prompts user for data to connect to another peer, and establishes the connection.
	 
	    Warning. Uses global variable myNetwork."""
		peerIP = raw_input("Enter it your peer's IP address: ")
		peerPort = getPort()
		self.network.connect(peerIP, peerPort)
		
	def netMessage(self, message, peer = None):
		if peer is not None:
			print("From {0!s}: {1!s}".format(peer,message)
		else:
			print(str(message))
			
		
		
	############## END OF NETWORK FUNCTION ###########
	
	
	
	######### ADDITIONAL ########
	
	def printThis(self, toPrint, type = None):
		"""
		Very simple method -- if type is none it prints toPrint, otherwise it returns 
		raw user input with toPrint being used as a prompt
		"""
		if type is not None:
			return raw_input(toPrint)
		else:
			print toPrint
		
	def name(): 
		for peers in list(self.network.peerList):
			print(str(peers) + " " + str(self.network.peerList.index(peers)))
		index = self.printThis("Please enter the index of the peer you would like to name: \n", type = "input")
		name = self.printThis("Please enter the name of the peer you would like to name: \n", type = "input")
		self.network.name(name,index)
		
	def addPort():
		for peers in list(self.network.peerList):
			print(str(peers) + " " + str(self.network.peerList.index(peers)))
		index = int(self.printThis("Please enter the index of the peer you would like to add a port to: \n", type = "input"))
		port = int(self.printThis("Please enter the port for the peer: \n", type = "input"))
		self.network.addPort(port,index)
	#### END OF ADDITIONAL #######
	
	
	
	############## END OF INTERFACE FUNTIONS ##################
	