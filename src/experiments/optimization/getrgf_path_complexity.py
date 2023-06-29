# Changes based on theorem of General Expansion Theorem for Rational Generating Functions (GETRGF), 
# which can be found in Chapter 7.3 of the book Concrete Mathematics, by Graham, Knuth and Patashnik.

# This allows us to take in the generating function and return the APC without needing to go through 
# the taylor series coefficients computation and solving the system of equation from these coefficients.

import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union
import numpy as np  # type: ignore
import sympy  # type: ignore
from mpmath import mpc, mpf, polyroots  # type: ignore
from sympy import (Basic, Float, Matrix, Poly, degree, eye, preorder_traversal, simplify, symbols,
                   sympify)

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from graph.graph import Graph
from metric import metric
from utils import Timeout, big_o, get_solution_from_roots, get_taylor_coeffs, calls_function

PathComplexityRes = tuple[Union[float, str], Union[float, str]]

PRECISION = 11


""" Finds the root with the maximum rho (1/root) among those. This root 
will originate the greatest APC.
Input: rootsDict, dictionary of all roots of the generating function
Return: maxrho and rhoDict
"""
def getRhoDict(rootsDict):
    rhoDict = {}
    maxRho = 0
    for root in rootsDict:
        rho = 1/root
        rhoDict[rho] = rootsDict[root]
        if abs(rho) > abs(maxRho):
            maxRho = rho
    return rhoDict, maxRho

"""
Input: denominator
Return: q0
"""
def getQ0(denominator):
    q0 = Poly(sympy.expand(denominator)).all_coeffs()[-1]
    return q0


""" Identifies other roots with same magnitude as the root with
maximum APC.
Input: rootsDict, rootsAPCDict
Return: APC
"""
def getAPC(genFunc, denominator, rootsDict):
    numerator = sympy.simplify(genFunc*denominator)
    rhoDict, maxRho = getRhoDict(rootsDict)
    q0 = getQ0(denominator)
    coeff = 0
    for rho in rhoDict:
        if abs(rho) == abs(maxRho):
            Ak = shiftAk(numerator, rho)/calculateAk(q0, rho, rhoDict)
            coeff = coeff + Ak
    apc = coeff*symbols("n")**(rhoDict[maxRho]-1)*maxrho**symbols("n")
    return apc

"""
Input:
Return: Denominator of Ak
"""
def calculateAk(q0,rhok,rhoDict):
    return 0

"""
Input:
Return:
"""
def shiftAk(numerator, rhok):
    return 0



def main():
    print(getRhoDict({1: 2, 2: 1, 0.6: 1, 0.5 + 0.02j: 2}))
    #x = symbols("x")
    expr = sympy.sympify("(2-x)*(5*x**3 - 1)")
    print(getQ0(expr))


if __name__ == "__main__":
    main()