from threading import Thread, Event
from time import sleep
import signal 

def roundExpression(expr, digits):
	pass

def myRound(num, prec):
	pass

def classify(expr, val):
	pass

def bigO():
	pass

def timeconstrained(maxTime, message, func, *params):
	stop = Event() 
	
	execThread = Thread(target=func)
	execThread.start() 

	# Block calling thread until execThread is done executing 
	execThread.join(timeout=maxTime)

	stop.set() 
	
class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)
