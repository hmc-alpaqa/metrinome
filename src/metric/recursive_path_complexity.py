"""Compute the path complexity and asymptotic path complexity metrics."""

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

class RecursivePathComplexity(ABC):
    """The interface that all metric computers should follow."""

    def __init__(self, logger: Log) -> None:
        """Initialize a new object capable of computing a metric."""
        self.logger = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Recursive Path Complexity"

    def evaluate(self, cfg: ControlFlowGraph) -> Union[int, PathComplexityRes]:
        """Given a graph, compute the metric."""
        adjMatrix = cfg.graph.adjacency_matrix()
        edgelist = []
        recurlist = []
        for rowIndex, row in enumerate(adjMatrix):
            for colIndex, value in enumerate(row):
                if value ==1:
                    edgelist += [[rowIndex, colIndex]]
        for node in cfg.metadata.calls.keys():
            if cfg.metadata.calls[node].split()[1] == cfg.name.split(".")[1]:
                recurlist += [int(node)]
        self.logger.d_msg(f"Adjacency Matrix: {adjMatrix}")
        self.logger.d_msg(f"Edge List: {edgelist}")
        self.logger.d_msg(f"Recur List: {recurlist}")
        apc = self.recurapc(edgelist, recurlist)
        return apc

    def recurapc(self, edgelist, recurlist):
        """Calculates the apc of a recursive function"""
        gamma = self.gammaFunction(edgelist, recurlist)
        self.logger.d_msg(f"Gamma Function: {gamma}")
        discrim = self.calculateDiscrim(gamma)
        self.logger.d_msg(f"Discriminant: {discrim}")
        try:
            numroots = len(sympy.real_roots(discrim))
        except:
            numroots = 0
        if numroots == 0:
            self.logger.d_msg(f"case1")
            T = symbols("T")
            x = symbols("x")
            gens = sympy.solve(gamma,T)
            possibleGenFunc = []
            for gen in gens:
                partialSeries = sympy.series(gen, x, 0, 40)
                if "-" not in str(partialSeries):
                    possibleGenFunc += [gen]
            if len(possibleGenFunc) == 1:
                genFunc = possibleGenFunc[0]/(1-x)
                self.logger.d_msg(f"Generating Function: {genFunc}")
            else:
                self.logger.e_msg("PANIC PANIC Oh dear, not sure which generating function is right")
            denominator = 1
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
            if numRoots < maxPow:
                newRootsDict = {}
                approxroots = sympy.nroots(denominator)
                for root in approxroots:
                    found = False
                    for dictRoot in newRootsDict.keys():
                        if abs(root-dictRoot)<10**(-12):
                            newRootsDict[dictRoot] += 1
                            break
                    if not found:
                        newRootsDict[root] = 1
                rootsDict = newRootsDict
                numRoots = sum(rootsDict.values())
            if numRoots < maxPow:
                raise Exception("Can't find all the roots :(")
            nonZeroIndex = 0
            while True:
                zseries = sympy.series(genFunc, x, 0, nonZeroIndex)
                if not type(zseries) == sympy.Order:
                    break
                nonZeroIndex += 1
            coeffs = [0]*(numRoots + nonZeroIndex)
            Tseries = sympy.series(genFunc, x, 0, numRoots + nonZeroIndex)
            exprs = []
            symbs = set()
            for term in Tseries.args:
                if not type(term) == sympy.Order:
                    c = str(term).split("*")[0]
                    if c == "x":
                        c = "1"
                    coeffs[self.termPow(term, x)] = int(c)
            for val in range(nonZeroIndex, nonZeroIndex + numRoots):
                expr = -coeffs[val]

                for rootindex, root in enumerate(rootsDict.keys()):
                    for mj in range(rootsDict[root]):
                        expr += symbols(f'c\-{rootindex}\-{mj}')*(val**mj)*((1/root)**val)
                        symbs.add(symbols(f'c\-{rootindex}\-{mj}'))
                exprs += [expr]


            try:
                with Timeout(seconds = 200, error_message="Root solver Timed Out"):
                    solutions = sympy.solve(exprs)
            except:
                solutions = sympy.nsolve(exprs, list(symbs), [0]*numRoots, dict=True)[0]
            patheq = 0
            for rootindex, root in enumerate(rootsDict.keys()):
                for mj in range(rootsDict[root]):
                    n = symbols("n")
                    patheq += symbols(f'c\-{rootindex}\-{mj}')*(n**mj)*(abs(1/root)**n)
            if not type(patheq) == int:
                patheq = patheq.subs(solutions)
            apc = patheq
        else:
            self.logger.d_msg(f"case2")
            rStar = min(map(lambda x: x if x > 0 else oo,sympy.real_roots(discrim)))
            apc = (1/rStar)**symbols("n")
        return apc


    def gammaFunction(self, edgelist, recurlist):
        """Takes in a list of all edges in a graph, and a list of where recursive calls are
        located, and calculates a gamma function in terms of x and the start node"""
        edgedict = {}
        for edge in edgelist: #reformatting our list of edges into a dictionary where keys are edge starts, and values are lists of edge ends
            startnode = str(edge[0])
            if startnode in edgedict:
                endnodes = edgedict[startnode] + [edge[1]]
            else:
                endnodes = [edge[1]]
            edgedict[startnode] = endnodes
        system = []
        x = symbols('x')
        accGF = 1/(1-x)
        firstnode = symbols("T")
        recurexpr = firstnode
        symbs = []
        for startnode in edgedict.keys():
            endnodes = edgedict[startnode]
            expr = 0
            sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
            symbs += [sym]
            for node in endnodes:
                if str(node) in edgedict.keys(): #makes sure the end node is not terminal
                    var = symbols("V" + str(node)) #str(chr(node+ 65))
                    expr = expr + var*x
                else:
                    expr = expr + x
                if int(startnode) in recurlist:
                    expr = recurexpr * expr #recursion
            system += [expr - sym]
        eq1 = symbols("V0")*x - firstnode
        symbs = [firstnode]+symbs
        gamma = sympy.expand(self.eliminate([eq1]+system, symbs))
        return gamma


    def calculateDiscrim(self, polynomial):
        """Takes in a polynomial and calculates its discriminant"""
        terms = polynomial.args
        domPow = max([self.termPow(term, "T") for term in terms])
        maxcoeff = 0
        for term in terms:
            if self.termPow(term, "T") == domPow:
                newprod = 1
                for arg in term.args:
                    if not "T" in str(arg):
                        newprod *= arg
                maxcoeff += newprod
        power = int(domPow*(domPow-1)/2)
        disc = ((-1)**power)/(maxcoeff)*self.resultant(polynomial, sympy.diff(polynomial, symbols("T")), symbols("T"))
        return disc

    def resultant(self, p, q, symb):
        """Calculates the resultant of two polynomials"""
        Ppow = 0
        Qpow = 0
        Pcoeffs = {}
        Qcoeffs = {}
        for term in p.args:
            pow = self.termPow(term, symb)
            if pow in Pcoeffs.keys():
                Pcoeffs[pow] += term/(symb**pow)
            else:
                Pcoeffs[pow] = term/(symb**pow)
            if  pow > Ppow:
                Ppow = pow
        for term in q.args:
            pow = self.termPow(term, symb)
            if pow in Qcoeffs.keys():
                Qcoeffs[pow] += term/(symb**pow)
            else:
                Qcoeffs[pow] = term/(symb**pow)
            if  pow > Qpow:
                Qpow = pow
        MatrixArray = []
        for i in range(Ppow + Qpow):
            MatrixArray += [[0]*(Ppow + Qpow)]
        for i in range(Ppow + 1):
            for j in range(Qpow):
                if i in Pcoeffs.keys():
                    MatrixArray[j][i + j] = Pcoeffs[i]
        for i in range(Qpow + 1):
            for j in range(Ppow):
                if i in Qcoeffs.keys():
                    MatrixArray[j + Qpow][i +j] = Qcoeffs[i]
        m = Matrix(MatrixArray)
        m = m.T
        return m.det()

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
        if len(system) == 1:
            return system[0]
        sub = system[-1] + symbs[-1]
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
