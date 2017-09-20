import socket
import time
from Interface import Interface
from P2PPlatform import Network
#from WorkerThread import WorkerThread

##########
#TODO check what specifically we need to change to organize our imports and get them working
##########

################################## MAIN PROGRAM BELOW ##################################

# Initialize the Interface


##########
#TODO Formalize XML for tagDict  we also might want to move XML into network
##########
tagDict = {}


myInterface = Interface(tagDict)

############### THIS COULD BE MOVED TO INTERFACE###########
myIP = myInterface.getOwnIP()
print ("Detected IP: " + myIP) 
print("I'll need your port.")
myPort = myInterface.getPort()


# Initialize a network
myNetwork = Network(myIP, myPort,myInterface.netMessage)

interfaceThread = WorkerThread("interface", myInterface)


######
# TODO See if it would be possible to make the two below part of Network, in the __init__
######
receiverThread = WorkerThread("receiver",myNetwork)
acceptorThread = WorkerThread("acceptor",myNetwork)



interfaceThread.start()

######
# TODO See if it would be possible to make the two below part of Network, in the __init__
######
receiverThread.start()
acceptorThread.start()


myInterface.network = myNetwork

# Add the first peer if the user wants one

############################################################
	
while myInterface.network is not None: #with this implementation, when the interface closes, this program closes
	
	######TODO code program logic here #############
	
	time.sleep(3)
