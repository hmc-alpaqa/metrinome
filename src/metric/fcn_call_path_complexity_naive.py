"""Compute the path complexity and asymptotic path complexity metrics."""
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
import time

PathComplexityRes = tuple[Union[float, str], Union[float, str]]
PRECISION = 11
class FunctionCallPathComplexity(ABC):
    """The interface that all metric computers should follow."""
    def __init__(self, logger: Log) -> None:
        """Initialize a new object capable of computing a metric."""
        self.logger = logger
        self.apc_times = {}
    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Function Call Path Complexity Naive"
    def evaluate(self, cfg: ControlFlowGraph, all_cfgs: List[ControlFlowGraph]) -> Union[int, PathComplexityRes]:
        """Given a graph, compute the metric."""
        # adjMatrix = cfg.graph.adjacency_matrix()
        # print(cfg.graph.edge_rules())
        # edgelist = []
        start_time = time.time()
        call_list = []
        all_edges = []
        # TODO: use full name of cfg (file name is deleted here)
        used_graphs = [cfg.name.split('.')[1]]
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
                        if not any(called_fcn == graph_name.split('.')[1] for graph_name in all_cfgs):
                            continue
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
        self.apc_times["graphProcessTime"] = time.time() - start_time
        apc = self.fcn_call_apc(all_edges, call_list)
        self.apc_times["firstHalfTime"] = self.apc_times["graphProcessTime"] + self.apc_times["graphSystemsTime"] + self.apc_times["gammaTime"]
        print (f"***APC: {self.apc_times}")
        return self.apc_times
        
    def fcn_call_apc(self, edgelist, call_list):
        """Calculates the apc of a function that can call other functions """
        if edgelist == []:
            return (0, 0)
        gamma = self.gammaFunction(edgelist, call_list)
        self.logger.d_msg(f"Gamma Function: {gamma}")
        start_time = time.time()
        discrim = self.calculateDiscrim(gamma)
        self.logger.d_msg(f"Discriminant: {discrim}")
        self.apc_times["discrimTime"] = time.time() - start_time
        start_time = time.time()
        try:
            numroots = len(self.realnroots(discrim))
        except Exception as e:
            self.logger.e_msg(f"Error: {e}")
            numroots = 0
        self.apc_times["realnrootsTime"] = time.time() - start_time

        if numroots == 0:
            self.apc_times['case'] = 1
            self.logger.d_msg(f"case1")
            T = symbols("T0")
            x = symbols("x")
            start_time = time.time()
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
            self.apc_times["genFuncTime"] = time.time() - start_time
            start_time = time.time()
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
            #nonZeroIndex = 0
            self.logger.d_msg(f"Found all Roots")
            self.logger.d_msg(f"numRoots: {numRoots}")
            self.logger.d_msg(f"rootsDict: {rootsDict}")
            self.apc_times["rootsDictTime"] = time.time() - start_time
            # Replacing old nonZeroIndex for numNodes: July 7, 2023
            # while True:
            #     zseries = sympy.series(genFunc, x, 0, nonZeroIndex)
            #     if not type(zseries) == sympy.Order:
            #         break
            #     nonZeroIndex += 1

            # Computing number of nodes and changing from the start index
            # from nonZeroIndex to number of nodes instead
            
            #Creates number of nodes per graph
            #1st step) Identify how many graphs
            start_time = time.time()
            sumAllNodes = 0
            graphsNumbers = []
            for i in range(len(edgelist)):
                graphsNumbers.append(int(edgelist[i][0][0]))
                graphsNumbers.append(int(edgelist[i][1][0]))

            graphsNumbers = list(sorted(set(graphsNumbers)))
            self.logger.d_msg(f"updated graph numbers:{graphsNumbers}")

            numCalls = [0]*len(graphsNumbers)

            #  2nd step) Identify how many calls for each graph
            # but only for graphs that are not calling themselves 
            currentCall = 0
            for i in range(len(call_list)):
                # print(f"edge comes from graph:{int(call_list[i][0][0])}")
                # print(f"edge goes to graph:{call_list[i][1]}")
                if (int(call_list[i][0][0]) !=  call_list[i][1]):
                    currentCall = call_list[i][1]
                    numCalls[currentCall] = numCalls[currentCall] + 1
            #include original graph being called
            numCalls[0] += 1
            self.logger.d_msg(f"num of calls per graph:{numCalls}")

            #3rd step) Number of nodes for each graph
            nodes = []
            for i in range(len(edgelist)):
                if edgelist[i][0] not in nodes:
                    nodes.append(edgelist[i][0])
                if edgelist[i][1] not in nodes:
                    nodes.append(edgelist[i][1])
            self.logger.d_msg(f"nodes list...{nodes}")
            numNodes = len(nodes) 
            self.logger.d_msg(f"numNodes: {numNodes}")

            listOfListsNodesGraphs = [[] for j in range(len(graphsNumbers))]
            for i in range(len(nodes)):
                listOfListsNodesGraphs[int(nodes[i][0])].append(nodes[i])
            
            numberNodesPerGraph = []
            for i in range(len(graphsNumbers)):
                numberNodesPerGraph.append(len(listOfListsNodesGraphs[i]) + 1)

            self.logger.d_msg(f"number nodes per graph:{numberNodesPerGraph}")
            dot_product = sum([x * y for x, y in zip(numberNodesPerGraph, numCalls)])
            self.logger.d_msg(f"dot product (new new node):{dot_product}")
            
            numNodes = dot_product
            
            #self.logger.d_msg(f"nonZeroIndex: {nonZeroIndex}")
            coeffs = [0]*(numRoots + numNodes)
            self.logger.d_msg(f"computing taylor series with {numRoots+numNodes} terms")
            Tseries = sympy.series(genFunc, x, 0, numRoots + numNodes)
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
            for val in range(numNodes, numNodes + numRoots):
                expr = -coeffs[val]
                for rootindex, root in enumerate(rootsDict.keys()):
                    for mj in range(rootsDict[root]):
                        expr += symbols(f'c\-{rootindex}\-{mj}')*(val**mj)*((1/root)**val)
                        symbs.add(symbols(f'c\-{rootindex}\-{mj}'))
                exprs += [expr]
            self.logger.d_msg(f"exprs: {exprs}")
            # self.logger.d_msg(f"exprs type: {type(exprs)}")
            try:
                with Timeout(seconds = 50, error_message="Root solver Timed Out"):
                    self.logger.d_msg(f"trying sympy.solve for 50 seconds")
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
            self.apc_times["naiveMathTime"] = time.time() - start_time
            # Debugging cases in which we drop the coefficient of the APC, Summer 2023
            # self.logger.d_msg(f"pc: {pc}")
            # if type(pc) == sympy.Add:
            #     print("ADD")
            #     apc = big_o(list(pc.args))
            # else:
            #     apc = pc
            #     apc = big_o(list(pc.args))
            #apc = pc
            #self.logger.d_msg(f"apc: {apc}")
        else:
            self.logger.d_msg(f"case2")
            start_time = time.time()
            rStar = min(map(lambda x: x if x >10**(-PRECISION) else sympy.oo,self.realnroots(discrim)))
            if type(rStar) == sympy.polys.rootoftools.ComplexRootOf:
                rStar = sympy.N(rStar)
            self.logger.d_msg(f"rStar: {rStar}")
            pc = sympy.N(1/rStar)**symbols("n")
            self.apc_times["apcTime2"] = time.time() - start_time
            self.apc_times["naiveMathTime"] = "case2"
        start_time = time.time()
        self.logger.d_msg(f"pc: {pc}")
        apc = pc
        if type(pc) == sympy.Add:
            # pc = simplify(pc)
            apc = big_o(list(pc.args))
        if "I" in str(apc):
            apc = sympy.simplify(self.clean(apc, symbols("n")))
            # apc = big_o(list(apc.args))
        self.logger.d_msg(f"apc: {apc}")
        self.apc_times["cleanTime"] = time.time() - start_time
        self.apc_times["pc"] = pc
        self.apc_times["apc"] = apc
        return (apc, pc)
  
    def gammaFunction(self, edgelist, call_list):
        """Takes in a list of all edges in a graph, and a list of where function calls are
        located, and calculates a gamma function in terms of x and the start node"""
        # calls: [('0_0', 1), ('0_0', 1), ('1_2', 1)] -> {'(0_0, 1)': 2, '(1_2, 1)': 1}
        start_time = time.time()
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
                    add_to_expr = x
                    for calling_node, called_fcn_idx in call_list:
                        if calling_node == node:
                            add_to_expr = init_nodes[called_fcn_idx] * add_to_expr
                    expr = expr + add_to_expr
            # before, the for loop is indented and it gives the wrong gamma function
            # fixed it by unindent the for loop, this should be correct now (7/10/2023)
            for calling_node, called_fcn_idx in call_list:
                if calling_node == startnode:
                    expr =  init_nodes[called_fcn_idx] * expr
            system += [expr - sym]
        init_eqns = [symbols(f'V{i}_0')*x - init_nodes[i] for i in range(num_cfgs)]
        symbs = init_nodes + symbs
        full_sys = init_eqns + system
        self.apc_times["graphSystemsTime"] = time.time() - start_time
        start_time = time.time()
        gamma = sympy.simplify(sympy.expand(self.eliminate(full_sys, symbs)))
        # gamma = sympy.expand(self.eliminate(full_sys, symbs))
        self.apc_times["gammaTime"] = time.time() - start_time
        return gamma

    def calculateDiscrim(self, polynomial):
        """Takes in a polynomial and calculates its discriminant"""
        # polynomial is not actually a polynomial, it can have fractions
        # so combine it with a common denominator, and then find discriminant of 
        # numerator (since the overall expression is equal to 0, ignore denom)
        polynomial = sympy.fraction(sympy.together(polynomial))[0]
        # print(f"polynomial {sympy.simplify(polynomial)}")
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
        # print(symbs[-1])
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