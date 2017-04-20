from threading import Thread


class WorkerThread(Thread):
  """ 
  Class used for overriding the default thread constructor, and running each thread.
  """
  
  def __init__(self, kind, myIP, port, network):
    """ Initialize the class attributes as outlined here:
    
    * kind -- str -- Which kind of the thread to be used in determining which function it should initiate.
    * myIP -- str -- The IP of this peer.
    * port -- int -- The port of this peer (the one that other peers will use as the second portion of the connect)
    * network -- Network -- The network instance that the thread should operate on
      This could be  useful is if in the future we would like to make a single program connect to several networks
      at the same time (ie using one to connect to a network working on solving and another on blockchain.)    
    """
    
    Thread.__init__(self)
    self.kind = kind
    self.myIP = myIP
    self.port = port
    self.network = network
    
    # Make this thread a daemon so the terminal doesn't hang on keyboard interrupt.
    self.setDaemon(True)

  def run(self):
    """ Determine which function this thread should run, and make it happen it. """
    
    if self.kind  == "manualClient":
      #print("DEBUG: ManualClient thread is running.")
      self.network.manualClient(self.myIP,self.port)
      
    elif self.kind == "receiver":
      #print("DEBUG: Receiver thread is running.")
      self.network.receiver()
      
    elif self.kind == "acceptor":
      #print("DEBUG: Acceptor thread is running.")
      self.network.acceptor(self.myIP, self.port)

