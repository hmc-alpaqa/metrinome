
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

PRECISION = 11

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
        # adjMatrix = cfg.graph.adjacency_matrix()
        # print(cfg.graph.edge_rules())
        # edgelist = []
        recurlist = []
        # for rowIndex, row in enumerate(adjMatrix):
        #     for colIndex, value in enumerate(row):
        #         if value ==1:
        #             edgelist += [[rowIndex, colIndex]]
        for node in cfg.metadata.calls.keys():
            for i in range(cfg.metadata.calls[node].count(cfg.name.split(".")[1])):
                recurlist += [int(node)]
        edgelist = cfg.graph.edge_rules()
        # self.logger.d_msg(f"Adjacency Matrix: {adjMatrix}")
        self.logger.d_msg(f"Edge List: {edgelist}")
        self.logger.d_msg(f"Recur List: {recurlist}")
        apc = self.recurapc(edgelist, recurlist)
        return apc

    def recurapc(self, edgelist, recurlist):
        """Calculates the apc of a recursive function"""
        if edgelist == []:
            return (0, 0)
        gamma = self.gammaFunction(edgelist, recurlist)
        self.logger.d_msg(f"Gamma Function: {gamma}")
        discrim = self.calculateDiscrim(gamma)
        self.logger.d_msg(f"Discriminant: {discrim}")
        try:
            numroots = len(self.realnroots(discrim))
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
                if "-" not in str(partialSeries) and gen != 0:
                    possibleGenFunc += [gen]
            if len(possibleGenFunc) == 1:
                genFunc = possibleGenFunc[0]/(1-x)
                self.logger.d_msg(f"Generating Function: {genFunc}")
            else:
                print(possibleGenFunc)
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
            self.logger.d_msg(f"Found all Roots")
            self.logger.d_msg(f"rootsDict: {rootsDict}")
            # Computing number of nodes and changing from the start index
            # from nonZeroIndex to number of nodes instead
            nodes = []
            for i in range(len(edgelist)):
                if edgelist[i][0] not in nodes:
                    nodes.append(edgelist[i][0])
                if edgelist[i][1] not in nodes:
                    nodes.append(edgelist[i][1])
            print(f"nodes list...{nodes}")
            numNodes = len(nodes) 
            self.logger.d_msg(f"numNodes: {numNodes}")
            coeffs = [0]*(numRoots + numNodes)
            Tseries = sympy.series(genFunc, x, 0, numRoots + numNodes)
            exprs = []
            symbs = set()
            for term in Tseries.args:
                if not type(term) == sympy.Order:
                    c = str(term).split("*")[0]
                    if c == "x":
                        c = "1"
                    coeffs[self.termPow(term, x)] = int(c)
            self.logger.d_msg(f"coeffs: {coeffs}")
            for val in range(numNodes, numNodes + numRoots):
                expr = -coeffs[val]

                for rootindex, root in enumerate(rootsDict.keys()):
                    for mj in range(rootsDict[root]):
                        expr += symbols(f'c\-{rootindex}\-{mj}')*(val**mj)*((1/root)**val)
                        symbs.add(symbols(f'c\-{rootindex}\-{mj}'))
                exprs += [expr]
            self.logger.d_msg(f"exprs: {exprs}")
            try:
                with Timeout(seconds = 50, error_message="Root solver Timed Out"):
                    print(f"trying sympy.solve for 50 seconds")
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
            pc = sympy.N(pc)
            self.logger.d_msg(f"pc: {pc}")
            # if type(pc) == sympy.Add:
            #     apc = big_o(list(pc.args))
            # else:
            #     apc = pc
            # self.logger.d_msg(f"apc: {apc}")
        else:
            self.logger.d_msg(f"case2")
            rStar = min(map(lambda x: x if x >10**(-PRECISION) else sympy.oo,self.realnroots(discrim)))
            if type(rStar) == sympy.polys.rootoftools.ComplexRootOf:
                rStar = sympy.N(rStar)
            self.logger.d_msg(f"rStar: {rStar}")
            # apc = sympy.N(1/rStar)**symbols("n")
            pc = sympy.N(1/rStar)**symbols("n")
        apc = pc
        if type(pc) == sympy.Add:
            # pc = simplify(pc)
            apc = big_o(list(pc.args))
        if "I" in str(apc):
            apc = sympy.simplify(self.clean(apc, symbols("n")))
            # apc = big_o(list(apc.args))
        # apc = sympy.N(apc)
        self.logger.d_msg(f"apc: {apc}")
        return (apc, pc)


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
                    add_to_expr = x
                    if node in recurlist:
                        add_to_expr = firstnode*x
                    expr = expr + add_to_expr
            # before, the for loop is indented and it gives the wrong gamma function
            # fixed it by unindent the for loop, this should be correct now (7/10/2023)
            for i in range(recurlist.count(int(startnode))):
                expr = recurexpr * expr #recursion
            system += [expr - sym]
        eq1 = symbols("V0")*x - firstnode # add T = VOX to system
        # all nodes in variable form
        self.logger.d_msg(f"system of equations:{system}")
        eq1 = symbols("V0")*x - firstnode
        symbs = [firstnode]+symbs
        gamma = sympy.expand(self.eliminate([eq1]+system, symbs)) #solves the system of equations for T & x equation
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
        result = self.resultant(polynomial, sympy.diff(polynomial, symbols("T")), symbols("T"))
        self.logger.d_msg(f"resultant: {result}")
        self.logger.d_msg(f"maxcoeff: {maxcoeff}")
        disc = ((-1)**power)/(maxcoeff)*result
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
        sub = system[-1] + symbs[-1] #sub is what the last symbol equals to 
        # print("printing sub..")
        # print(sub)
        # if the last equation has the last symbol on both side
        if symbs[-1] in sub.free_symbols: #free_symbols in this case is all the symbols in sub
            for eq in system: 
                if symbs[-1] in eq.free_symbols: #if the last symbol appears (only once) in the previous equations
                    sol = sympy.solve(eq, symbs[-1], dict=True) #use that equation and solve for the last symbol
                    # sol is a dictionary: [{last symbol: expresion}]
                    # print(f"printing sol: {sol}")
                    if len(sol) == 1:
                        #in the last equation substitute the last symbol ---> the expresion
                        sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]])) 
                        #TODO: suggestion: last equation has already been substituted, symbs[-1] 
                        # should not appear for this point on. No further sub should be needed.
        if symbs[-1] in sub.free_symbols: #if the last symbol is still in sub
            self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")

        #for each equation in the system, find the last symbol, ans substitute it with sub
        for count, eq in enumerate(system):
            if symbs[-1] in eq.free_symbols:
                system[count] = sympy.expand(eq.subs(symbs[-1], sub))
        return self.eliminate(system[:-1], symbs[:-1])


    def clean(self, system, symb):
        """Gets rid of complex numbers and makes things cleaner"""
        if type(system) == str:
            system = sympy.parse_expr(system)
        if "I" in str(system):
            if str(symb) in str(system):
                if type(system) == sympy.Add:
                    newSys = 0
                    for term in system.args:
                        newSys += self.clean(term, symb)
                elif type(system) == sympy.Mul:
                    newSys = 1
                    for term in system.args:
                        newSys *= self.clean(term, symb)
                else:
                    newSys = system
                return newSys
            else:
                return sympy.Abs(system)
        else:
            return system

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
