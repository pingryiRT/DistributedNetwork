import socket
import sys

# Create a client socket to communicate with the server
host = "localhost"
port = 54321

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to connect to the server
try:
	sock.connect((host, port))
	
except socket.error:
	print("No server running at {}:{}".format(host, port))
	print("Aborting.\n")
	sys.exit(1)
	


# Listen for broadacsts until the server closes the socket
message = " " # Initialize the message just to get into the loop once
while len(message) > 0:
  # If message is over 1024 bytes long, it will be broken into parts.
  message = sock.recv(1024)
  print(message)

# Clean up the open sockets
sock.shutdown(socket.SHUT_RDWR)
sock.close()
