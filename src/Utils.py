from threading import Thread, Event
from time import sleep
from sympy import limit, Abs, sympify, series, symbols, Function
from mpmath import polyroots
import signal
import numpy as np
from collections import Counter
from operator import methodcaller
import re

def roundExpression(expr: str, digits: int) -> str:
    '''
    Take some sympy expression represented as a string
    and round all numbers to the given number of decimal
    places
    '''
    regExp = "([0-9]*)\.([0-9]*)"
    def replaceWithRounded(match):
        return match.groups()[0] + "." + match.groups()[1][0:digits]

    return re.sub(regExp, replaceWithRounded, expr)

def classify(expr: str, var="n") -> str:
    '''
    Given an arbitrary expression represented as a
    string, return a value indicating it's 'class'.

    Note: the string cannot have other variables (e.g.
    we cannot classify '2m' in terms of 'n')

    Exponentiation is represented by '^'

    Const: [Value]
    PolyDeg: [Highest Degree of Polynomial]
    ExpBase: [Return the base of expression of the form a^x]
'''
    if expr == '':
        return "Const:0"

    try:
        val = float(str(expr))
        return f"Const:{val}"
    except:
        # If we have anything to the power 'n', then it is exponential 
        val = isExponential(expr, var)
        if val is None:
            degree = getDegree(expr, var)
            return f"PolyDeg:{degree}"

        return f"ExpBase:{val}"

def getSolutionFromRoots(roots):
    '''
    Return the solution to a recurrence relation given the roots of the characteristic
    equation
    '''
    # Round to 4 digits 
    roots = [complex(round(root.real, 6), round(root.imag, 6)) for root in roots]

    # Compute the multiplicy of each root
    rootsWithMultiplicites = Counter(roots)

    # Compute the coefficients of a_n as a list
    solution = []
    for root in rootsWithMultiplicites.keys():
        for i in range(0, rootsWithMultiplicites[root]):
            if root == 1:
                solution += [sympify(f"(n**{i})")]
            else:
                solution += [sympify(f"(n**{i})*{root}**n")]

    return solution

def getRecurrenceSolution(recurrence: str):
    '''
    Returns the coefficients to a homogeneous linear recurrence relation
    represented as a string of the format 

    c_0*f(n) + c_1*f(n-1) + ... + c_k*f(n-k)

    by finding the roots of the characteristic equation
    '''
    # Define symbolic terms 
    n = symbols('n')
    f = Function('f')

    # Regular expression to parse the recurrence relation expression. 
    # RE matches a particular term: Coefficient + f(something)
    matchFunction = 'f\([ a-zA-Z0-9-+]*\)'
    matchObj = re.findall(f'([ +-.0-9]*)(\*)({matchFunction})', recurrence)
    coeffs = []
    for match in matchObj:
        coeffs += [float(match[0].replace(" ", ""))]

    # Normalize such that leading coefficient is 1
    leadingCoeff = coeffs[0]
    coeffs = list(map(lambda coeff: coeff / leadingCoeff, coeffs))

    # Find the roots of the characteristic equation 
    # through arbitrary precision root finding function
    roots = polyroots(coeffs, maxsteps=200, extraprec=200)

    return getSolutionFromRoots(roots)

def getTaylorCoeffs(func, numCoeffs: int):
    '''
    Given an arbitrary rational function
    '''
    t = symbols('t')
    L = str(series(func, x=t, x0=0, n = numCoeffs)).split('+')
    firstElement = L[0]
    firstPower = re.search("\*\*([0-9]*)", str(firstElement))
    firstPower = int(firstPower.groups()[0])
    taylorCoeffs = [0] * firstPower + [sympify(f).subs(t, 1) for f in L]
    return taylorCoeffs

def isExponential(term: str, var = 'n'):
    '''
    If an expression contains an exponential, return its base.
    Otherwise, return None
    '''

    # either ^n or ^(num*n)
    num = "([0-9][0-9]*[.][0-9]*)|([.][0-9][0-9]*)|([0-9][0-9]*)"
    searchString = f"({num})\^{var}"
    results = re.findall(searchString, term)
    maxBase = None
    if results:
        maxBase = max(map(lambda res: float(res[0]), results))

    searchStringWithParens = f"({num})\^\(({num})?\*{var}\)"
    results = re.findall(searchStringWithParens, term)
    if results:
        # a^(bn) should be classified as a^b
        f = lambda res: float(res[0])**float(res[4])
        newBase = max(map(f, results))
        if newBase is not None:
            if maxBase is None or newBase > maxBase:
                maxBase = newBase

    return maxBase

def getDegree(term: str, var="n") -> int:
    '''
    If an expression is a polynomial, return the degree.
    Otherwise, return 0.
    '''
    num = "([0-9][0-9]*[.][0-9]*)|([.][0-9][0-9]*)|([0-9][0-9]*)"
    res = re.findall(f"{var}\^({num})", term)
    foundDeg = 0
    if res:
        foundDeg = max(map(lambda x: float(x[0]), res))

    if foundDeg == 0 and re.search(var, term) is not None:
        return 1.0

    return foundDeg

def bigO(terms):
    '''
    Compute the big O of some expression in terms of 'n'

    The terms should be a list of expressions represented as strings
    '''
    n = symbols('n')

    if len(terms) == 1:
        return terms[0]

    termOne = terms[0]
    termTwo = terms[1]
    lim = limit(Abs(sympify(termTwo) / sympify(termOne)), n, float('inf'))

    if lim == 0:
        return termOne

    return bigO(terms[1:])

class Timeout:
    '''
    Allows us to run a function such that an error is thrown if
    it does not finish within a given amount of time
    '''
    def __init__(self, seconds=1, errorMessage='Timeout') -> None:
        self.seconds = seconds
        self.errorMessage = errorMessage

    def handleTimeout(self, signum, frame):
        raise TimeoutError(self.errorMessage)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handleTimeout)
        signal.alarm(self.seconds)
        
    def __exit__(self, type, value, traceback):
        signal.alarm(0)
