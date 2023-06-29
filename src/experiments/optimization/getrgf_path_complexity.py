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
import math

PathComplexityRes = tuple[Union[float, str], Union[float, str]]

PRECISION = 11


# """ Finds the root with the maximum rho (1/root) among those. This root 
# will originate the greatest APC.
# Input: rootsDict, dictionary of all roots of the generating function
# Return: maxrho and rhoDict
# """
# def getRhoDict(rootsDict):
#     return 0

# """
# Input: denominator
# Return: q0
# """
# def getQ0(denominator):
#     return 0


# """ Identifies other roots with same magnitude as the root with
# maximum APC.
# Input: rootsDict, rootsAPCDict
# Return: APC
# """
# def getAPC(rhoDict, maxRho, q0, numerator):
#     return 0 

"""
Input:
Return: Denominator of Ak
"""
def calculateAk(q0,rhok,rhoDict):
    denominator = q0
    mult = rhoDict[rhok]
    denominator *= math.factorial(mult-1)
    productory = 1
    for rho in rhoDict:
        if rho != rhok:
            productory *= (1-rho/rhok)^rhoDict[rho]
    denominator *= productory
    return denominator


# x = sympy.Symbol("x")
# f = sympy.Function('f')(x)
# equation = sympy.Eq(f,x**3+x**2)
# numerator = sympy.solve(equation,f)
# numerator = numerator[0]
# rhok = 0.5
"""
Input:
Return:
"""
def shiftAk(numerator, rhok):
    rhokDict = {symbols("x"):1/rhok}
    numeratorAK = numerator.subs(rhokDict)
    # print(numeratorAK)
    return numeratorAK

def main():
    shiftAk(numerator,rhok)


if __name__ == "__main__":
    main()