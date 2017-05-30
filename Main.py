import socket
import time
from Interface import Interface
from WorkerThread import WorkerThread
from Network import Network


################################## MAIN PROGRAM BELOW ##################################

# Initialize the Interface

tagDict = {}
myInterface = Interface(tagDict)

############### THIS COULD BE MOVED TO INTERFACE###########
myIP = myInterface.getOwnIP()
print ("Detected IP: " + myIP) 
print("I'll need your port.")
myPort = myInterface.getPort()


# Initialize a network
myNetwork = Network(myIP, myPort,myInterface)
adamNode = raw_input("Starting a new network? (y/N): ")

interfaceThread = WorkerThread("interface", myInterface)
receiverThread = WorkerThread("receiver",myNetwork)
acceptorThread = WorkerThread("acceptor",myNetwork)



interfaceThread.start()
receiverThread.start()
acceptorThread.start()


myInterface.network = myNetwork

# Add the first peer if the user wants one
if adamNode == "" or adamNode[0].lower()!= "y":
	myInterface.connector()
############################################################
	
while myInterface.network is not None: #with this implementation, when the interface closes, this program closes
	
	######TODO code program logic here #############
	
	time.sleep(3)
