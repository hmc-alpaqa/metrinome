from threading import Thread, Event
from time import sleep
from sympy import limit, Abs, sympify, series, symbols
import signal 

def roundExpression(expr, digits):
	pass

def myRound(num, prec):
	pass

def classify(expr, val):
	pass

def getTaylorCoeffs(func, numCoeffs):
    '''
    Given an arbitrary rational function
    ''' 
    t = symbols('t')
    L = str(series(func, x=t, x0=0, n = numCoeffs)).split('+')
    taylorCoeffs = [sympify(f).subs(t, 1) for f in L]
    return taylorCoeffs

def breadth_first_search(graph,source):
    """
    This function is the Implementation of the breadth_first_search program
    """
    # Mark each node as not visited
    mark = {}
    for item in graph.keys():
        mark[item] = 0

    queue, output = [],[]

    # Initialize an empty queue with the source node and mark it as explored
    queue.append(source)
    mark[source] = 1
    output.append(source)

    # while queue is not empty
    while queue:
        # remove the first element of the queue and call it vertex
        vertex = queue[0]
        queue.pop(0)
        # for each edge from the vertex do the following
        for vrtx in graph[vertex]:
            # If the vertex is unexplored
            if mark[vrtx] == 0:
                queue.append(vrtx)  # mark it as explored
                mark[vrtx] = 1      # and append it to the queue
                output.append(vrtx) # fill the output vector
    return output

def bigO(terms, sym):
    if len(terms) == 1:
        return terms[0]
    
    termOne = terms[0]
    termTwo = terms[1]
    lim = limit(Abs(sympify(termTwo) / sympify(termOne)), n, float('inf'))
    
    if lim == 0:
        return termOne
    
    return bigO(L[1:], sym)

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
