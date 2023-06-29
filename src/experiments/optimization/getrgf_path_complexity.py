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
    return 0

"""
Input: denominator
Return: q0
"""
def getQ0(denominator):
    return 0


""" Identifies other roots with same magnitude as the root with
maximum APC.
Input: rootsDict, rootsAPCDict
Return: APC
"""
def getAPC(rhosDict, maxRho, q0, numerator):
    return 0 

"""
Input:
Return: Denominator of Ak
"""
def calculateAk(q0,rhok,rhosDict):
    return 0

"""
Input:
Return:
"""
def shiftAk(numerator, rhok):
    return 0