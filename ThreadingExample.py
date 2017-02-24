import threading

# First define some example functions

def print_doubles():
	i = 0
	while i < 1000:
		if i % 2 == 0:
			print("The next double is {}".format(i))
		i += 1

def print_primes():
	i = 0
	while i < 1000:
		if is_prime(i):
			print("The next prime is {}".format(i))
		i += 1
		
def is_prime(n):
	""" An intentionally slow algorithm to determine whether the arg is prime. """
	for i in range(2, n):
		if n % i == 0:
			return False
	
	return True

# Now create classes for our new threads
class DoubleThread(threading.Thread):

	def __init__(self, name, threadID):
		threading.Thread.__init__(self)
		self.name = name
		self.id = threadID
	
	def run(self):
		print_doubles()

class PrimeThread(threading.Thread):

	def __init__(self, name, threadID):
		threading.Thread.__init__(self)
		self.name = name
		self.id = threadID
	
	def run(self):
		print_primes()

#### Main Program Below #####
doubleThread = DoubleThread("Hello my name is doubleThread", 1)
primeThread  = PrimeThread ("Hello my name is primeThread",  2)

doubleThread.start()
primeThread.start()

