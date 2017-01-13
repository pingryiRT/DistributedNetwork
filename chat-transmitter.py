
# Documentation is here: https://docs.python.org/3/library/socket.html
import socket


# Create a server socket to accept incoming connections from clients.
host = 'localhost' # Using localhost only makes the socket visible to client on this system.
port = 54321         # Port can be pretty much any number. This one is easy to remember.

# AF_INET means address format is IPv4
# SOCK_STREAM specifies what kind of socket it is. This one is common.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This makes the socket reuseable immediately after closing the program
# TODO I hope we can eventually remove this line after we are sure our sockets
# are always closed nicely, but maybe it will always be necessary.
# For now it at least reduces cursing while coding :)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Now put that socket to use on the host and port we specified above.
serverSocket.bind((host, port)) # Double parens are important to make the argument a tuple.
serverSocket.listen(0)          # This says not to keep clients queued up in line to connect... I think.

# The server socket is just here to accept incoming connections. When it does
# accept one, it creates a new client socket for the actual communication.
print("Waiting for clients to connect, type Control-C to begin broadcasting")

response = ""
clientList = [] # List of clients that have connected
try:
	while True:
		clientSocket, clientAddress = serverSocket.accept()
		clientList.append(clientSocket) 
except KeyboardInterrupt:
	pass 


# Once we have a connected receiver, begin broadcasting
print("Begin typing messages for broadcast.")
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
