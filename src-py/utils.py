from threading import Thread, Event
from time import sleep
from sympy import limit, Abs, sympify, series, symbols, Function
import signal 
import numpy as np
from collections import Counter
from operator import methodcaller
import re

def roundExpression(expr, digits):
    '''
    '''
    pass

def myRound(num, prec):
    '''
    '''
    pass

def classify(expr, val):
    '''
    '''
    pass

def getRecurrenceSolution(recurrenceRelation):
    '''
    Returns the coefficients to a homogeneous linear recurrence relation
    '''
    # Define symbolic terms 
    n = symbols('n')
    f = Function('f')

    # .m in: -f[-3 + n] + f[-2 + n] + f[-1 + n] - f[n]
    # .m out: (-1.)^n*C[1] + C[2] + n*C[3]
    # Make a recurrence (equivalent to str(<simpify-expr>))
    # TODO: make sure str(<simpify-expr>) will parse in the same order!!
    #recurrence = "-1*f(n) + 1.0*f(n - 1) + 1*f(n - 2) + -1*f(n - 3)"
    recurrence = str(recurrenceRelation)
    print(recurrence)

    # Regular expression to parse the recurrence relation expression. 
    # RE matches a particular term: Coefficient + f(something)
    matchObj = re.findall('([ +-.0-9]*)(\*)(f\([ a-zA-Z0-9-+]*\))', recurrence)
    coeffs = []
    for match in matchObj:
        coeffs += [float(match[0].replace(" ", ""))]

    # Coefficients are originally in order f(n), f(n - k), f(n - k + 1), ...
    # Convert to f(n), f(n - 1), f(n - 2), ...
    coeffs = [coeffs[0]] + coeffs[1:][::-1]

    # Normalize such that leading coefficient is 1
    leadingCoeff = coeffs[0]
    coeffs = list(map(lambda coeff: coeff / leadingCoeff, coeffs))
    print(coeffs)

    # Find the roots of the characteristic equation 
    roots = np.roots(coeffs)
    precisionDigits = 5
    roots = [round(root, precisionDigits) for root in roots]

    # Compute the multiplicy of each root
    rootsWithMultiplicites = Counter(roots)

    # Compute the coefficients of a_n as a list
    a_n = []
    for root in rootsWithMultiplicites.keys():
        for i in range(0, rootsWithMultiplicites[root]):
            a_n += [sympify(f"(n**{i})*{root}**n")]
            
    return a_n

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
    '''
    '''
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
