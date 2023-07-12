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
import cmath

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
    maxMultiplicity = 0
    for root in rootsDict:
        rho = 1/root
        multiplicity = rootsDict[root]
        rhoDict[rho] = rootsDict[root]
        if abs(rho) > abs(maxRho):
            maxRho = rho
            maxMultiplicity = multiplicity
        elif abs(rho) == abs(maxRho):
            maxMultiplicity = max(maxMultiplicity,multiplicity)
    print(maxMultiplicity)
    return rhoDict, maxRho, maxMultiplicity

# """
# Input: denominator
# Return: q0
# """
# def getQ0(denominator):
#     return 0


""" Identifies other roots with same magnitude as the root with
maximum APC.
Input: rootsDict, rootsAPCDict
Return: APC
"""
def getAPC(genFunc, denominator, rootsDict):
    numerator = sympy.simplify(genFunc*denominator)
    rhoDict, maxRho, maxMultiplicity = getRhoDict(rootsDict)
    q0 = getQ0(denominator)
    coeff = 0
    print("rhoDict:",rhoDict)
    print("q0",q0)
    print("numerator",numerator)
    for rho in rhoDict:
        if (abs(rho) == abs(maxRho)) and (rhoDict[rho] == maxMultiplicity):
            Ak = shiftAk(numerator, rho)/calculateAk(q0, rho, rhoDict)
            print("Ak",Ak)
            coeff = coeff + Ak
    apc = sympy.simplify(coeff*(symbols("n")**(maxMultiplicity-1))*abs(maxRho)**symbols("n"))
    # apc = coeff*(symbols("n")**(maxMultiplicity-1))*abs(maxRho)**symbols("n")
    return apc

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
            productory *= (1-rho/rhok)**rhoDict[rho]
    denominator *= productory
    print("denominator:",denominator)
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

    # four bad addition
    # rootsDict = {-1: 4, 1: 5}
    # genFunc = sympy.sympify("-x**11*(x**3 - x**2 + 1)**4/((x - 1)**5*(x + 1)**4)")
    # denominator = sympy.sympify("x**9 - x**8 - 4*x**7 + 4*x**6 + 6*x**5 - 6*x**4 - 4*x**3 + 4*x**2 + x - 1")

    # gcd
    rootsDict = {1: 1, -2**(3/4)/2: 1, 2**(3/4)/2: 1, -2**(3/4)/2j: 1, 2**(3/4)/2j: 1}
    genFunc = sympy.sympify("-x**3/((1 - x)*(2*x**4 - 1))")
    denominator = sympy.sympify("-2*x**5 + 2*x**4 + x - 1")
    

    # nested loops
    rootsDict = {-math.sqrt(1/2 + math.sqrt(5)/2)*1.0j: 1, math.sqrt(1/2 + math.sqrt(5)/2)*1.0j: 1, -math.sqrt(-1/2 + math.sqrt(5)/2): 1, math.sqrt(-1/2 + math.sqrt(5)/2): 1}
    genFunc = sympy.sympify("-x**3*(x + 1)/(x**4 + x**2 - 1)")
    denominator = sympy.sympify("x**4 + x**2 - 1")

    # factorial
    rootsDict = {1: 2, -1/2 - math.sqrt(3)/2j: 1, -1/2 + math.sqrt(3)/2j: 1}
    genFunc = sympy.sympify("-x**3/((1 - x)*(x**3 - 1))")
    denominator = sympy.sympify("-x**4 + x**3 + x - 1")

    # quintuple nested loops
    rootsDict = {-1.87438979182: 1, -0.873796954923: 1, -0.721878492624: 1, 0.721878492624: 1, 0.873796954923: 1, 1.00000000000: 1, 1.87438979182: 1, -0.770941725708j: 1, 0.770941725708j: 1, -1.0970941727j: 1, 1.0970941727j: 1}
    genFunc = sympy.sympify("(-x**11 - 2*x**9 + 3*x**7 + x**5 - x**3)/((1 - x)*(x**10 - 3*x**8 - 3*x**6 + 4*x**4 + x**2 - 1))")
    denominator = sympy.sympify("-x**11 + x**10 + 3*x**9 - 3*x**8 + 3*x**7 - 3*x**6 - 4*x**5 + 4*x**4 - x**3 + x**2 + x - 1")



    # chinese remainder
    rootsDict = {0.804991068573: 1, 1.00000000000: 1, -1.18597548111 - 0.145145955381j: 1, -1.18597548111 + 0.145145955381j: 1,
    -0.5 - 0.866025403784j: 1, -0.5 + 0.866025403784j: 1, -0.449337291814 - 0.823958443448j: 1, -0.449337291814 + 0.823958443448j: 1,
    0.37272450822 - 0.900999789639j: 1, 0.37272450822 + 0.900999789639j: 1, 0.86009273042 - 0.547133194003j: 1,
    0.86009273042 + 0.547133194003j: 1}
    genFunc = sympy.sympify("-x**5/((1 - x)*(x**11 + x**10 + x**6 + x**3 - 1))")
    denominator = sympy.sympify("-x**12 + x**10 - x**7 + x**6 - x**4 + x**3 + x - 1")

    # mul inv
    rootsDict = {1: 2}
    genFunc = sympy.sympify("x**3*(-x**3 + x - 1)/((1 - x)*(x - 1))")
    denominator = sympy.sympify("-x**2 + 2*x - 1")

    # heapify
    rootsDict = {0.723403643775: 1, 1.00000000000: 1, -0.960884364939 - 0.443320753827j: 1, -0.960884364939 + 0.443320753827j: 1,
    -0.701062781122 - 1.06324912517j: 1, -0.701062781122 + 1.06324912517j: 1, -0.164809906067 - 1.08499607754j: 1,
    -0.164809906067 + 1.08499607754j: 1, 0.46505523024 - 0.64469713265j: 1, 0.46505523024 + 0.64469713265j: 1}
    genFunc = sympy.sympify("-x**4*(x**4 + 2*x**3 + 3*x**2 + 2*x + 1)/((1 - x)*(x**9 + 2*x**8 + 3*x**7 + 2*x**6 + x**5 - 1))")
    denominator = sympy.sympify("-x**10 - x**9 - x**8 + x**7 + x**6 + x**5 + x - 1")

    #binomial
    rootsDict = {1.00000000000000: 1, -0.5 - 0.866025403784439j: 1, -0.5 + 0.866025403784439j: 1, 0.724491959000516: 1, -1.22074408460576: 1, 0.248126062802622 + 1.03398206097597j: 1, 0.248126062802622 - 1.03398206097597j: 1}
    genFunc =  sympy.sympify("x**4*(x**5 + 2*x**4 + x**3 - x - 1)/((1 - x)*(x**6 + x**5 + x**4 + x**3 - 1))")
    denominator = sympy.sympify("-x**7 + x**3 + x - 1")

    print(getAPC(genFunc, denominator, rootsDict))

if __name__ == "__main__":
    main()