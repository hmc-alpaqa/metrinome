import re
from abc import ABC, abstractmethod
from collections import defaultdict, deque, Counter
from typing import Union, List

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

PRECISION = 11

class EqnSolverTest:

    def __init__(self, logger: Log) -> None:
        """Initialize a new object capable of computing a metric."""
        self.logger = logger

    def fcn_call_apc(self, full_sys, symbs):
        """Calculates the apc of a function that can call other functions """
        # gamma = self.gammaFunction(edgelist, call_list)
        gamma = sympy.expand(self.eliminate(full_sys, symbs))
        print('GAMMA', gamma)
        self.logger.d_msg(f"Gamma Function: {gamma}")
        discrim = self.calculateDiscrim(gamma)
        self.logger.d_msg(f"Discriminant: {discrim}")
        try:
            # print("hello")
            numroots = len(self.realnroots(discrim))
        except Exception as e:
            self.logger.e_msg(f"Error: {e}")
            numroots = 0
        if numroots == 0:
            self.logger.d_msg(f"case1")
            T = symbols("T0")
            x = symbols("x")
            gens = sympy.solve(gamma,T)
            # print(gens)
            possibleGenFunc = []
            genFunc = None
            for gen in gens:
                partialSeries = sympy.series(gen, x, 0, 40)
                if "-" not in str(partialSeries) and gen != 0:
                    possibleGenFunc += [gen]
            if len(possibleGenFunc) == 1:
                genFunc = possibleGenFunc[0]/(1-x)
                self.logger.d_msg(f"Generating Function: {genFunc}")
            else:
                # print(possibleGenFunc)
                self.logger.e_msg("PANIC PANIC Oh dear, not sure which generating function is right")
            denominator = 1
            if genFunc == None:
                print('***', possibleGenFunc, gens)
            for factor in genFunc.args:
                if type(factor) == sympy.Pow and factor.args[1] < 0:
                    denominator *= 1/factor
            denominator = sympy.expand(denominator)
            maxPow = 0
            for term in denominator.args:
                power = self.termPow(term, symbols("x"))
                if power > maxPow:
                    maxPow = power
            rootsDict = sympy.roots(denominator)
            numRoots = sum(rootsDict.values())
            self.logger.d_msg(f"numRoots: {numRoots}")
            self.logger.d_msg(f"denominator: {denominator}")
            if numRoots < maxPow:
                newRootsDict = {}

                approxroots = sympy.nroots(denominator, n=(PRECISION + 1), maxsteps=1000)

                for root in approxroots:
                    found = False
                    for dictRoot in newRootsDict.keys():
                        if abs(root-dictRoot)<10**(-PRECISION):
                            newRootsDict[dictRoot] += 1
                            found = True
                            break
                    if not found:
                        newRootsDict[root] = 1
                rootsDict = newRootsDict
                numRoots = sum(rootsDict.values())
            if numRoots < maxPow:
                raise Exception("Can't find all the roots :(")
            nonZeroIndex = 0
            self.logger.d_msg(f"Found all Roots")
            self.logger.d_msg(f"rootsDict: {rootsDict}")
            while True:
                zseries = sympy.series(genFunc, x, 0, nonZeroIndex)
                if not type(zseries) == sympy.Order:
                    break
                nonZeroIndex += 1
            self.logger.d_msg(f"nonZeroIndex: {nonZeroIndex}")
            coeffs = [0]*(numRoots + nonZeroIndex)
            Tseries = sympy.series(genFunc, x, 0, numRoots + nonZeroIndex)
            exprs = []
            symbs = set()
            for term in Tseries.args:
                # print(term)
                if not type(term) == sympy.Order:
                    c = str(term).split("*")[0]
                    if c == "x":
                        c = "1"
                    coeffs[self.termPow(term, x)] = int(c)
            self.logger.d_msg(f"coeffs: {coeffs}")
            for val in range(nonZeroIndex, nonZeroIndex + numRoots):
                expr = -coeffs[val]

                for rootindex, root in enumerate(rootsDict.keys()):
                    for mj in range(rootsDict[root]):
                        expr += symbols(f'c\-{rootindex}\-{mj}')*(val**mj)*((1/root)**val)
                        symbs.add(symbols(f'c\-{rootindex}\-{mj}'))
                exprs += [expr]
            self.logger.d_msg(f"exprs: {exprs}")
            try:
                with Timeout(seconds = 200, error_message="Root solver Timed Out"):
                    solutions = sympy.solve(exprs)
            except:
                solutions = sympy.nsolve(exprs, list(symbs), [0]*numRoots, dict=True)[0]
            self.logger.d_msg(f"solutions: {solutions}")
            patheq = 0
            for rootindex, root in enumerate(rootsDict.keys()):
                for mj in range(rootsDict[root]):
                    n = symbols("n")
                    patheq += symbols(f'c\-{rootindex}\-{mj}')*(n**mj)*(abs(1/root)**n)
            self.logger.d_msg(f"patheq: {patheq}")
            if not type(patheq) == int:
                patheq = patheq.subs(solutions)
            pc = patheq
            self.logger.d_msg(f"pc: {pc}")
            if type(pc) == sympy.Add:
                apc = big_o(list(pc.args))
            else:
                apc = pc
            self.logger.d_msg(f"apc: {apc}")
        else:
            self.logger.d_msg(f"case2")
            rStar = min(map(lambda x: x if x >10**(-PRECISION) else sympy.oo,self.realnroots(discrim)))
            if type(rStar) == sympy.polys.rootoftools.ComplexRootOf:
                rStar = sympy.N(rStar)
            self.logger.d_msg(f"rStar: {rStar}")
            apc = sympy.N(1/rStar)**symbols("n")
            pc = sympy.N(1/rStar)**symbols("n")
        if "I" in str(apc):
            apc = sympy.simplify(self.clean(apc, symbols("n")))
            apc = big_o(list(apc.args))
        apc = sympy.N(apc)
        return (apc, pc)

    def calculateDiscrim(self, polynomial):
        """Takes in a polynomial and calculates its discriminant"""
        # polynomial is not actually a polynomial, it can have fractions
        # so combine it with a common denominator, and then find discriminant of 
        # numerator (since the overall expression is equal to 0, ignore denom)
        polynomial = sympy.fraction(sympy.together(polynomial))[0]
        return sympy.discriminant(polynomial, sympy.symbols("T0"))

    def termPow(self, term, symb):
        """for a expression, find the power a symbol is raised to"""
        if not str(symb) in str(term):
            return 0
        if not str(symb)+"**" in str(term):
            return 1
        if type(term) == sympy.Mul:
            args = term.args
            for arg in args:
                if str(symb) in str(arg):
                    return self.termPow(arg, symb)
        if type(term) == sympy.Pow:
            return int(str(term).split("**")[1])
        else:
            self.logger.e_msg(f"PANIC PANIC termPow type is {type(term)}.")
            return 0

    def eliminate(self, system, symbs):
            """Takes in a system of equations and gets the gamma function"""
            print('ELIMINATE', system)
            if len(system) == 1:
                return system[0]
            sub = system[-1] + symbs[-1]
            print('sub', sub)
            if symbs[-1] in sub.free_symbols:
                for eq in system:
                    if symbs[-1] in eq.free_symbols:
                        sol = sympy.solve(eq, symbs[-1], dict=True)
                        if len(sol) == 1:
                            sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
            if symbs[-1] in sub.free_symbols:
                self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
            for count, eq in enumerate(system):
                if symbs[-1] in eq.free_symbols:
                    system[count] = sympy.expand(eq.subs(symbs[-1], sub))
            return self.eliminate(system[:-1], symbs[:-1])
    
    def realnroots(self, eq):
        """Calls nroots then returns the real ones"""
        if "/" in str(eq):
            splitEq = str(eq).split("/")
            numerator = sympy.parse_expr(splitEq[0])
            denominator = sympy.parse_expr(splitEq[1])
            numroots = sympy.nroots(numerator, n=(PRECISION + 1), maxsteps=1000)
            self.logger.d_msg(f"numroots: {numroots}")
            denoroots = sympy.nroots(denominator, n=(PRECISION + 1), maxsteps=1000)
            self.logger.d_msg(f"denoroots: {denoroots}")
            for root in numroots:
                for badRoot in denoroots:
                    if abs(root-badRoot)<10**(-PRECISION):
                        numroots.remove(root)
                        break
            self.logger.d_msg(f"numroots: {numroots}")
            #ask bang about root nonsense
        else:
            numroots = sympy.nroots(eq, n=(PRECISION + 1), maxsteps=1000)
        realnroots = []
        for root in numroots:
            if sympy.Abs(sympy.im(root))<10**(-PRECISION):
                realnroots += [sympy.re(root)]
        return realnroots


