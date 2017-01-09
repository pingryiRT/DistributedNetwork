# Here is a basic program file to get us started.

# I think this module may be very helpful for us
# Documentation is here: https://docs.python.org/3/library/socket.html
import socket


# Initialize the socket

host = 'localhost' # localhost just means "this computer"
port = 54321       # port can be pretty much any number. This one is easy to remember.

# Create a server socket to accept incoming connections from clients.
# AF_INET meant address format is IPv4
# SOCK_STREAM specifies what kind of socket it is. This one is common.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Now put that socket to use on the host and port we specified above.
serverSocket.bind((host, port)) # Double parens are important to make the argument a tuple.
serverSocket.listen(0)          # This says not to keep clients queued up in line to connect... I think.

# The server socket is just here to accept incoming connections. When it does
# accept one, it creates a new client socket for the actual communication.
print("Waiting for clients to connect")

response = ""
clientList = [] # List of clients that have connected
while response != "y":
	response = raw_input("Type enter to wait for a new client to connect, or type 'y' to stop searching for clients")
	if response == "y":
		break
	else:
		clientSocket, clientAddress = serverSocket.accept()
		clientList.append(clientSocket) 


# Infinte loop that waits for the user to type a message, then transmits it.
while True:
  message = raw_input("Enter the next message to send: ")
  for client in clientList:
 	 client.send(message)
  	
# Ideally we should always close our sockets, but currently this program won't
# because it can only be quit by using ctrl + C.
clientSocket.close()
serverSocket.close()
