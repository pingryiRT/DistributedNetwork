import socket

from WorkerThread import WorkerThread
from Network import Network


################################## MAIN PROGRAM BELOW ##################################

# Initialize the Interface

tagDict = {}
myInterface = Interface(tagDict)

myIP = myInterface.getOwnIP()
print ("Detected IP: " + myIP) 
print("I'll need your port.")
myPort = myInterface.getPort()


# Initialize a network
myNetwork = Network(myIP, myPort)
adamNode = raw_input("Starting a new network? (y/N): ")

# Add the first peer if the user wants one
if adamNode == "" or adamNode[0].lower()!= "y":
	connector()
	


# Initialize and start the threads







		
