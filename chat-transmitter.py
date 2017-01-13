
# Documentation is here: https://docs.python.org/3/library/socket.html
import socket

def get_local_ip():
	"""
	A helper function to get this machine's IP address.	
	Returns the IPv4 address as it appears to other	nodes on the network.
	
	This slopppy code is taken from: http://stackoverflow.com/a/1267524
	I have no idea how it works :-/
	"""
	
	return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
	

# Create a server socket to accept incoming connections from clients.
host = get_local_ip() # Using localhost only makes the socket visible to client on this system.
port = 54321          # Port can be pretty much any number. This one is easy to remember.

# AF_INET means address format is IPv4
# SOCK_STREAM specifies what kind of socket it is. This one is common.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This makes the socket reuseable immediately after closing the program
# TODO I hope we can eventually remove this line after we are sure our sockets
# are always closed nicely, but maybe it will always be necessary.
# For now it at least reduces cursing while coding :)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Now put that socket to use on the host and port we specified above
serverSocket.bind((host, port)) # Double make the argument a tuple
serverSocket.listen(0)          # Allow up to 2 clients in the queue

print("Waiting for clients to connect, type Control-C to begin broadcasting")

clientList = [] # List of clients that have connected
try:
	while True:
		# Server socket just accepts incoming connections. When it does accept one,
		# Creates a new client socket for the actual communication.
		clientSocket, clientAddress = serverSocket.accept()
		clientList.append(clientSocket)
		
		print("Accepted connection from {}".format(clientAddress))
		
except KeyboardInterrupt:
	pass 


# Once we have connected receivers, begin broadcasting
print("\n\nBegin typing messages for broadcast.")
print("Type '/exit' to end the program.")
message = ""

# Main loop that listens for messages
while message != "/exit":
	message = raw_input("message> ")
	for client in clientList:
		client.send(message)


  	
# Clean up the open sockets before exiting
for client in clientList:
	# Tell client that socket is shutdown for reading and writing
	client.shutdown(socket.SHUT_RDWR)
	
	# Actually close the socket on this end
	client.close()

serverSocket.close()
