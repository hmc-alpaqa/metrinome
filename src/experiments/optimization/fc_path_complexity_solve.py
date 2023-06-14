"""Compute the path complexity and asymptotic path complexity metrics for solve vs nsolve
   called by solve_vs_nsolve"""

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
from scipy.optimize import fsolve
from sympy.utilities import lambdify
import time
import unittest
import math

PathComplexityRes = tuple[Union[float, str], Union[float, str]]

PRECISION = 11

class FunctionCallPathComplexity(ABC):
    """The interface that all metric computers should follow."""

    def __init__(self, logger: Log) -> None:
        """Initialize a new object capable of computing a metric."""
        self.logger = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Function Call Path Complexity"

    def evaluate(self, solve, cfg: ControlFlowGraph, all_cfgs: List[ControlFlowGraph]) -> Union[int, PathComplexityRes]:
        """Given a graph, compute the metric."""
        # adjMatrix = cfg.graph.adjacency_matrix()
        # print(cfg.graph.edge_rules())
        # edgelist = []
        call_list = []
        all_edges = []
        # TODO: use full name of cfg (file name is deleted here)
        used_graphs = [cfg.name.split('.')[1]]
        print('CFG NAME', cfg.name.split('.')[1])
        graphs_to_process = deque([cfg])
        # for rowIndex, row in enumerate(adjMatrix):
        #     for colIndex, value in enumerate(row):
        #         if value ==1:
        #             edgelist += [[rowIndex, colIndex]]
        # ?? function call finding?
        while graphs_to_process:
            cfg = graphs_to_process.popleft()
            fcn_idx = used_graphs.index(cfg.name.split('.')[1])
            for node in cfg.metadata.calls.keys():
                
                # loop through functions that are called
                for called_fcn in cfg.metadata.calls[node].split():
                    # add graphs to used_graphs
                    if called_fcn in ['START', 'CALLS']:
                        continue
                    if called_fcn not in used_graphs:
                        used_graphs.append(called_fcn)
                        # find graph from all_cfgs, add to graphs_to_process
                        for graph_name in all_cfgs:
                            if graph_name.split('.')[1] == called_fcn:
                                graphs_to_process.append(all_cfgs[graph_name])
                                break
                    # Call (i, j) from function i node j to called_fcn
                    call_list.append((f'{fcn_idx}_{int(node)}', used_graphs.index(called_fcn)))
            edge_list = cfg.graph.edge_rules()
            # add fcn_idx to tuple (i, j) where i is fcn_idx and j is node num
            # edge_list = [((fcn_idx, edge[0]), (fcn_idx, edge[1])) for edge in edge_list]
            edge_list = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in edge_list]
            all_edges += edge_list


       
        self.logger.d_msg(f"Edge List: {all_edges}")
        self.logger.d_msg(f"Call List: {call_list}")
        apc = self.fcn_call_apc(all_edges, call_list,solve)
        return apc
    
   

    def fcn_call_apc(self, edgelist, call_list,solve):
        """Calculates the apc of a function that can call other functions """

        timeVal = 0.0

        if edgelist == []:
            return (0, 0)
        gamma = self.gammaFunction(edgelist, call_list)
        self.logger.d_msg(f"Gamma Function: {gamma}")
        discrim = self.calculateDiscrim(gamma)
        self.logger.d_msg(f"Discriminant: {discrim}")
        try:
            numroots = len(self.realnroots(discrim))
        except Exception as e:
            self.logger.e_msg(f"Error: {e}")
            numroots = 0
        if numroots == 0:
            self.logger.d_msg(f"case1")
            T = symbols("T0")
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
                # print(possibleGenFunc)
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
            # nonZeroIndex = 0
            self.logger.d_msg(f"Found all Roots")
            self.logger.d_msg(f"rootsDict: {rootsDict}")
            # while True:
            #     zseries = sympy.series(genFunc, x, 0, nonZeroIndex)
            #     if not type(zseries) == sympy.Order:
            #         break
            #     nonZeroIndex += 1
            # Computing number of nodes and changing from the start index
            # from nonZeroIndex to number of nodes instead
            
            #Creates number of nodes per graph
            #1st step) Identify how many graphs
            sumAllNodes = 0
            graphsNumbers = []
            for i in range(len(edgelist)):
                graphsNumbers.append(int(edgelist[i][0][0]))
                graphsNumbers.append(int(edgelist[i][1][0]))

            graphsNumbers = list(sorted(set(graphsNumbers)))
            print(f"updated graph numbers:{graphsNumbers}")

            numCalls = [0]*len(graphsNumbers)
            #2nd step) Identify how many calls for each graph
            currentCall = 0
            for i in range(len(call_list)):
                currentCall = call_list[i][1]
                numCalls[currentCall] = numCalls[currentCall] + 1
            #include original graph being called
            numCalls[0] += 1
            print(f"num of calls per graph:{numCalls}")
            

            #3rd step) Number of nodes for each graph
            nodes = []
            for i in range(len(edgelist)):
                if edgelist[i][0] not in nodes:
                    nodes.append(edgelist[i][0])
                if edgelist[i][1] not in nodes:
                    nodes.append(edgelist[i][1])
            print(f"nodes list...{nodes}")
            numNodes = len(nodes) 
            self.logger.d_msg(f"numNodes: {numNodes}")

            listOfListsNodesGraphs = [[] for j in range(len(graphsNumbers))]
            for i in range(len(nodes)):
                listOfListsNodesGraphs[int(nodes[i][0])].append(nodes[i])
            
            numberNodesPerGraph = []
            for i in range(len(graphsNumbers)):
                numberNodesPerGraph.append(len(listOfListsNodesGraphs[i]) + 1)
                print(f"number nodes per graph: {numberNodesPerGraph}")

            dot_product = sum([x * y for x, y in zip(numberNodesPerGraph, numCalls)])
            print(f"dot product:{dot_product}")
            
            numNodes = dot_product


            # numNodes += 23
            coeffs = [0]*(numRoots + numNodes) # plus 1 because counts start at 0
            Tseries = sympy.series(genFunc, x, 0, numRoots + numNodes)
            # coeffs = [0]*(2*numRoots + numNodes) # plus 1 because counts start at 0
            # Tseries = sympy.series(genFunc, x, 0, 2*numRoots + numNodes)

            exprs = []
            symbs = [0]*numRoots
            for term in Tseries.args:
                # print(term)
                if not type(term) == sympy.Order:
                    c = str(term).split("*")[0]
                    if c == "x":
                        c = "1"
                    coeffs[self.termPow(term, x)] = int(c)
            self.logger.d_msg(f"coeffs: {coeffs}") # a list of coefficient in tayler series, the ith index represent the coeff of x^i

            #initialize a matrix and base cases, later use numpy.linalg.lstsq to solve the matrix
            matrix = np.empty(shape = (numRoots,numRoots),dtype = complex)
            matrix.fill(0)
            base_cases = np.zeros(numRoots)

            # if (numNodes % 2 == 1):
            #     numNodes += 1

            rows = 0 #to keep track of the rows in the matrix
            # for val in range(numNodes, numNodes+2*numRoots,2):
            for val in range(numNodes, numNodes + numRoots):
                print(f'n is {val}')
                expr = -coeffs[val]
                index = 0 #to keep track of the columns of the matrix
                base_cases[rows] = coeffs[val]
                for rootindex, root in enumerate(rootsDict.keys()):
                    for mj in range(rootsDict[root]):
                        coeff_of_c = (val**mj)*((1/root)**val)
                        expr += symbols(f'c\-{rootindex}\-{mj}')* coeff_of_c
                        coeff_of_c = complex(coeff_of_c) # convert coeff_of_c from sympy.complex to numpy.complex
                        # print(f"coeff_of_c:{coeff_of_c}")
                        # print(f"coeff_of_c type:{type(coeff_of_c)}")
                        matrix[rows][index] = coeff_of_c
                        symbs[index] = symbols(f'c\-{rootindex}\-{mj}') #record the symbols (c's) in a list
                        index += 1
                exprs += [expr]
                rows +=1
            self.logger.d_msg(f"exprs: {exprs}")
            self.logger.d_msg(f"base_cases: {base_cases}")
            self.logger.d_msg(f"matrix: {matrix}")
            # self.logger.d_msg(f"matrix: {matrix[-3][-1]}")
            self.logger.d_msg(f"symbols list: {symbs}")

            # check_exprs = matrix.dot(symbs)
            # check_exprs = check_exprs.flatten().tolist()
            # print(check_exprs)
            # #assert check_exprs == exprs, "no matrix does not equal exprs"
            # print(f"solution of check_exprs{sympy.nsolve(check_exprs, symbs, [0]*numRoots, dict=True)[0]}")
            
            if (solve == 0): #use solve
                start_time = time.time()
                try:
                    with Timeout(seconds = 20):
                        solutions = sympy.solve(exprs)
                        timeVal = time.time()-start_time
                except TimeoutError:
                    print ("SOLVE cannot solve, need help from nsolve!!!")
            elif (solve == 1):
                #[c\-0\-0 + 4*c\-0\-1 + c\-1\-0/(-1/2 - sqrt(3)*I/2)**4 + c\-2\-0/(-1/2 + sqrt(3)*I/2)**4 - 1, 
                # c\-0\-0 + 5*c\-0\-1 + c\-1\-0/(-1/2 - sqrt(3)*I/2)**5 + c\-2\-0/(-1/2 + sqrt(3)*I/2)**5 - 1, 
                # c\-0\-0 + 6*c\-0\-1 + c\-1\-0/(-1/2 - sqrt(3)*I/2)**6 + c\-2\-0/(-1/2 + sqrt(3)*I/2)**6 - 2, 
                # c\-0\-0 + 7*c\-0\-1 + c\-1\-0/(-1/2 - sqrt(3)*I/2)**7 + c\-2\-0/(-1/2 + sqrt(3)*I/2)**7 - 2]
                """ Approach 1
                try:
                    print(exprs)
                    with Timeout(seconds = 50):
                        print(f"symbols for exprs {symbs}")
                        def myFunction(symbs):
                            return [expr.subs(zip(coeffs,list(symbs))) for expr in exprs]
                        print(f"this should be functions{myFunction(symbs)}")
                        print(type(myFunction))
                        initial_guess = np.zeros(len(list(symbs)))
                        print(initial_guess)
                        solutions = fsolve(myFunction,initial_guess) 
                except TimeoutError:
                    print ("FSOLVE cannot solve, need help from nsolve!!!")
                """
                try:
                    print(exprs)
                    with Timeout(seconds = 50):
                        print(f"symbols for exprs {symbs}")
                        eval_exprs = lambdify(list(symbs),exprs)
                        def myFunction(symbs):
                            return eval_exprs(*symbs)
                        print(f"this should be functions {myFunction(symbs)}")
                        print(type(myFunction))
                        initial_guess = np.zeros(len(list(symbs)))
                        print(initial_guess)
                        solutions = fsolve(myFunction, initial_guess, complex) 
                except TimeoutError:
                    print ("FSOLVE cannot solve, need help from nsolve!!!")

            elif (solve == 2): #use matrix
                start_time = time.time()
                print('running msolve...')
                try:
                    with Timeout(seconds = 100):
                        solutions_list_solve = np.linalg.solve(matrix,base_cases) #get the exact solution in decimals
                        # solutions_list_lstsq = np.linalg.lstsq(matrix, base_cases, rcond=None)[0]
                        # solutions = dict(zip(symbs,solutions_list_lstsq))
                        # print(f"solutions using lstsq: {solutions}")
                        solutions = dict(zip(symbs,solutions_list_solve)) #make it into a dictionary so that we can later substitute
                        timeVal = time.time()-start_time
                except TimeoutError:
                    print ("MSOLVE cannot solve, need help from nsolve!!!")

            else: #try nsolve
                start_time = time.time()
                print('running nsolve...')
                solutions = sympy.nsolve(exprs, list(symbs), [0]*numRoots, dict=True)[0]
                timeVal = time.time()- start_time

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
            # self.logger.d_msg(f"pc: {pc}")
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
            pc = sympy.N(1/rStar)**symbols("n")
        self.logger.d_msg(f"pc: {pc}")
        apc = pc
        if type(pc) == sympy.Add:
            apc = big_o(list(pc.args))
        if "I" in str(apc):
            # print(f"printing big o{big_o(list(apc.args))}")
            apc = sympy.simplify(self.clean(apc, symbols("n")))
            #apc = big_o(list(apc.args))
        self.logger.d_msg(f"apc: {apc}")
        return (apc, pc, timeVal)


    def gammaFunction(self, edgelist, call_list):
        """Takes in a list of all edges in a graph, and a list of where function calls are
        located, and calculates a gamma function in terms of x and the start node"""
        # calls: [('0_0', 1), ('0_0', 1), ('1_2', 1)] -> {'(0_0, 1)': 2, '(1_2, 1)': 1}
        edgedict = defaultdict(list)
        for edge in edgelist: #reformatting our list of edges into a dictionary where keys are edge starts, and values are lists of edge ends
            edgedict[edge[0]].append(edge[1])

        # num_cfgs is max i in i_j for all edges + 1
        num_cfgs = max([int(edge[0].split('_')[0]) for edge in edgelist]) + 1

        init_nodes = [symbols(f'T{i}') for i in range(num_cfgs)]
        system = []
        x = symbols('x')
        symbs = []
        for startnode in edgedict:
            endnodes = edgedict[startnode]
            expr = 0
            sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
            symbs += [sym]
            for node in endnodes:
                if str(node) in edgedict: #makes sure the end node is not terminal
                    var = symbols("V" + str(node)) #str(chr(node+ 65))
                    expr = expr + var*x
                else:
                    expr = expr + x
            
                for calling_node, called_fcn_idx in call_list:
                    if calling_node == startnode:
                        expr =  init_nodes[called_fcn_idx] * expr
            system += [expr - sym]

        init_eqns = [symbols(f'V{i}_0')*x - init_nodes[i] for i in range(num_cfgs)]
        symbs = init_nodes + symbs
        print("SYMBS:", symbs)
        full_sys = init_eqns + system
        print('SYSTEM:', full_sys)

        gamma = sympy.expand(self.eliminate(full_sys, symbs))
        return gamma

    def calculateDiscrim(self, polynomial):
        """Takes in a polynomial and calculates its discriminant"""
        # polynomial is not actually a polynomial, it can have fractions
        # so combine it with a common denominator, and then find discriminant of 
        # numerator (since the overall expression is equal to 0, ignore denom)
        polynomial = sympy.fraction(sympy.together(polynomial))[0]
        return sympy.discriminant(polynomial, sympy.symbols("T0"))

    # def calculateDiscrim(self, polynomial):
    #     """Takes in a polynomial and calculates its discriminant"""
    #     # replace all T0's with T in polynomial
    #     polynomial = polynomial.subs(symbols("T0"), symbols("T"))
    #     polynomial = sympy.fraction(sympy.together(polynomial))[0]
    #     terms = polynomial.args
    #     domPow = max([self.termPow(term, "T") for term in terms])
    #     maxcoeff = 0
    #     for term in terms:
    #         if self.termPow(term, "T") == domPow:
    #             newprod = 1
    #             for arg in term.args:
    #                 if not "T" in str(arg):
    #                     newprod *= arg
    #             maxcoeff += newprod

    #     power = int(domPow*(domPow-1)/2)
    #     result = self.resultant(polynomial, sympy.diff(polynomial, symbols("T")), symbols("T"))
    #     self.logger.d_msg(f"resultant: {result}")
    #     self.logger.d_msg(f"maxcoeff: {maxcoeff}")
    #     disc = ((-1)**power)/(maxcoeff)*result
    #     return disc

    # def resultant(self, p, q, symb):
    #     """Calculates the resultant of two polynomials"""
    #     Ppow = 0
    #     Qpow = 0
    #     Pcoeffs = {}
    #     Qcoeffs = {}
    #     for term in p.args:
    #         pow = self.termPow(term, symb)
    #         if pow in Pcoeffs.keys():
    #             Pcoeffs[pow] += term/(symb**pow)
    #         else:
    #             Pcoeffs[pow] = term/(symb**pow)
    #         if  pow > Ppow:
    #             Ppow = pow
    #     for term in q.args:
    #         pow = self.termPow(term, symb)
    #         if pow in Qcoeffs.keys():
    #             Qcoeffs[pow] += term/(symb**pow)
    #         else:
    #             Qcoeffs[pow] = term/(symb**pow)
    #         if  pow > Qpow:
    #             Qpow = pow
    #     MatrixArray = []
    #     for i in range(Ppow + Qpow):
    #         MatrixArray += [[0]*(Ppow + Qpow)]
    #     for i in range(Ppow + 1):
    #         for j in range(Qpow):
    #             if i in Pcoeffs.keys():
    #                 MatrixArray[j][i + j] = Pcoeffs[i]
    #     for i in range(Qpow + 1):
    #         for j in range(Ppow):
    #             if i in Qcoeffs.keys():
    #                 MatrixArray[j + Qpow][i +j] = Qcoeffs[i]
    #     m = Matrix(MatrixArray)
    #     m = m.T
    #     # print(m)
    #     return m.det()

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
                    # print(system)
                    # print(type(system))
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

