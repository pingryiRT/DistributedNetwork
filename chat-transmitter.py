# Here is a basic program file to get us started.

# I think this module may be very helpful for us
# Documentation is here: https://docs.python.org/3/library/socket.html
import socket


# Initialize the socket

host = 'localhost' # localhost just means "this computer"
port = 54321      # port can be pretty much any number. This one is easy to remember.

# Create a server socket to accept incoming connections from clients.
# AF_INET means address format is IPv4
# SOCK_STREAM specifies what kind of socket it is. This one is common.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
	
# Close the sockets before exiting


  	
# Close all sockets
for client in clientList:
	client.close()

serverSocket.close()
