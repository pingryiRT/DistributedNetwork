from threading import Thread
import time
import socket

class WorkerThread(Thread):
  """ 
  Class used for overriding the default thread constructor, and running each thread.
  """
  
  def __init__(self, kind, network, debug = False, Stopper = False):
    """ Initialize the class attributes as outlined here:
    
    * kind -- str -- Which kind of the thread to be used in determining which function it should initiate.
    * network -- Network -- The network instance that the thread should operate on
      This could be  useful is if in the future we would like to make a single program connect to several networks
      at the same time (ie using one to connect to a network working on solving and another on blockchain.)    
    * debug -- bool -- Whether or not to print debugging information.
    """
    
    Thread.__init__(self)
    self.kind = kind
    self.network = network
    self.debug = debug
    self.Stopper = Stopper
    
    # Make this thread a daemon so the terminal doesn't hang on keyboard interrupt.
    self.setDaemon(True)

  def run(self):
    """ Determine which function this thread should run, and make it happen it. """
    print("run")
    if self.kind  == "manualClient":
    	if self.debug:
    		print("DEBUG: ManualClient thread is running.")
    	self.network.manualClient()
    while (not self.Stopper): 
		if self.kind == "receiver":
			if self.debug:
				print("DEBUG: Receiver thread is running.")
			self.network.receiver()
		elif self.kind == "acceptor":
			if self.debug:
				print("DEBUG: Acceptor thread is running.")	
			self.network.acceptor()
		time.sleep(1)
