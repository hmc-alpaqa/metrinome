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
import copy
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

    def evaluate(self, cfg: ControlFlowGraph, all_cfgs: List[ControlFlowGraph]) -> Union[int, PathComplexityRes]:
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        print("HELLO")
        print("CFG ELIM", cfg)
        calldict, dictgraphs = self.processGraphs(cfg, all_cfgs)
        print("CALLDICT: ",calldict)
        print("DICTGRAPHS: ", dictgraphs)
        print('')
        print("Graph Name: ", cfg.name)
        print("ALL GRAPHS: ", all_cfgs)
        print('')

        graphname = cfg.name
        
        fullsystem, fullsymbols, splitsystems, splitsymbols, lookupDict = self.graphsToSystems(dictgraphs, calldict)
        print("FULLSYSTEM",fullsystem)
        modSystems = copy.deepcopy(splitsystems)
        modSymbols = copy.deepcopy(splitsymbols)
        optimizedSystems = copy.deepcopy(splitsystems)
        optimizedSymbols = copy.deepcopy(splitsymbols)
        print("PLEASE PLEASE PLEASE")
        #ISSUE STARTS W/ SELF.ELIMINATE
        simpleGamma = self.eliminate(fullsystem,fullsymbols)
        print("DONE")
        modGamma = self.modEliminate(modSystems,modSymbols)
        optimizedGamma = self.optimizedEliminate(optimizedSystems, optimizedSymbols, lookupDict)
        
        print('')
        print(f'simpleGamma: {simpleGamma}')
        print(f'modGamma: {modGamma}')
        print(f'simpleGamma = modGamma check: {simpleGamma == modGamma}')
        print('')
        print(f'simpleGamma: {simpleGamma}')
        print(f'optimizedGamma: {optimizedGamma}')
        print(f'simpleGamma = optimizedGamma check: {simpleGamma == optimizedGamma}')

        apc = self.fcn_call_apc(optimizedGamma)
        return apc

    def fcn_call_apc(self, gamma):
        """Calculates the apc of a function that can call other functions """
        if gamma == 0:
            return (0, 0)
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
                with Timeout(seconds = 10, error_message="Root solver Timed Out"):
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
            #self.logger.d_msg(f"pc: {pc}")
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
            apc = sympy.simplify(self.clean(apc, symbols("n")))
            # apc = big_o(list(apc.args))
        self.logger.d_msg(f"apc: {apc}")
        return (apc, pc)
  
    # def gammaFunction(self, edgelist, call_list):
    #     """Takes in a list of all edges in a graph, and a list of where function calls are
    #     located, and calculates a gamma function in terms of x and the start node"""
    #     # calls: [('0_0', 1), ('0_0', 1), ('1_2', 1)] -> {'(0_0, 1)': 2, '(1_2, 1)': 1}
    #     edgedict = defaultdict(list)
    #     for edge in edgelist: #reformatting our list of edges into a dictionary where keys are edge starts, and values are lists of edge ends
    #         edgedict[edge[0]].append(edge[1])
    #     # num_cfgs is max i in i_j for all edges + 1
    #     num_cfgs = max([int(edge[0].split('_')[0]) for edge in edgelist]) + 1
    #     init_nodes = [symbols(f'T{i}') for i in range(num_cfgs)]
    #     system = []
    #     x = symbols('x')
    #     symbs = []
    #     for startnode in edgedict:
    #         endnodes = edgedict[startnode]
    #         expr = 0
    #         sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
    #         symbs += [sym]
    #         for node in endnodes:
    #             if str(node) in edgedict: #makes sure the end node is not terminal
    #                 var = symbols("V" + str(node)) #str(chr(node+ 65))
    #                 expr = expr + var*x
    #             else:
    #                 expr = expr + x
            
    #             for calling_node, called_fcn_idx in call_list:
    #                 if calling_node == startnode:
    #                     expr =  init_nodes[called_fcn_idx] * expr
    #         system += [expr - sym]
    #     init_eqns = [symbols(f'V{i}_0')*x - init_nodes[i] for i in range(num_cfgs)]
    #     symbs = init_nodes + symbs
    #     print("SYMBS:", symbs)
    #     full_sys = init_eqns + system
    #     print('SYSTEM:', full_sys)
    #     gamma = sympy.expand(self.eliminate(full_sys, symbs))
    #     return gamma

#=========================================INTEGRATION IN PROGRESS====================================================================
    def processGraphs(self, graph, all_graphs):
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        print(all_graphs)
        dictgraphs = []
        print(graph)
        used_graphs = [graph.name]
        graphs_to_process = deque([graph])
        
        calldict = defaultdict(list)
        while graphs_to_process:
            curr_graph = graphs_to_process.popleft()
            print(curr_graph)
            curr_graph_name = curr_graph.name
            print(curr_graph_name)
            curr_graph_edges = curr_graph.graph.edge_rules()
            print(curr_graph_edges)
            curr_graph_calls = curr_graph.metadata.calls
            print(curr_graph_calls)
            fcn_idx = used_graphs.index(curr_graph_name)
            print(fcn_idx)
            curr_graph_edges = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in curr_graph_edges]
            print(curr_graph_edges)
            edgedict = defaultdict(list)
            for edge in curr_graph_edges: #reformatting our graph from edgelist form to dictionary form
                edgedict[edge[0]].append(edge[1])
            dictgraphs.append(edgedict)
            print(edgedict)
            for node in curr_graph_calls.keys():
                print(node)
                # loop through functions that are called
                for called_fcn in curr_graph_calls[node].split(" "):
                    # add graphs to used_graphs
                    if called_fcn in ['START', 'CALLS']:
                        continue
                    if called_fcn not in used_graphs:
                        used_graphs.append(called_fcn)
                        # find graph from all_cfgs, add to graphs_to_process
                        for graph in all_graphs:
                            if graph == called_fcn:
                                graphs_to_process.append(all_graphs[graph])
                                break
                    # Call (i, j) from function i node j to called_fcn
                    calldict[f'{fcn_idx}_{int(node)}'].append(used_graphs.index(called_fcn))
        print("D",dictgraphs)
        return calldict, dictgraphs

    # def evaluate(self, all_graphs: dict, graphname):
        
    #     print('')
    #     print("Graph Name: ", graphname)
    #     print("ALL GRAPHS: ", all_graphs)
    #     print('')

    #     graph = all_graphs[graphname]
    #     lookupDict = defaultdict(set)

    #     calldict, dictgraphs = self.processGraphs(graph, all_graphs)
    #     fullsystem, fullsymbols, splitsystems, splitsymbols, lookupDict = self.graphsToSystems(dictgraphs, calldict)

    #     modSystems = copy.deepcopy(splitsystems)
    #     modSymbols = copy.deepcopy(splitsymbols)
    #     optimizedSystems = copy.deepcopy(splitsystems)
    #     optimizedSymbols = copy.deepcopy(splitsymbols)

    #     simpleGamma = self.simpleEliminate(fullsystem,fullsymbols)
    #     modGamma = self.modEliminate(modSystems,modSymbols)
    #     optimizedGamma = self.optimizedEliminate(optimizedSystems, optimizedSymbols, lookupDict)
        
    #     print('')
    #     print(f'simpleGamma: {simpleGamma}')
    #     print(f'modGamma: {modGamma}')
    #     print(f'simpleGamma = modGamma check: {simpleGamma == modGamma}')
    #     print('')
    #     print(f'simpleGamma: {simpleGamma}')
    #     print(f'optimizedGamma: {optimizedGamma}')
    #     print(f'simpleGamma = optimizedGamma check: {simpleGamma == optimizedGamma}')

    def graphsToSystems(self, dictgraphs, calldict):

        lookupDict = defaultdict(set)
        x = symbols("x")
        num_cfgs = len(dictgraphs)
        init_nodes = [symbols(f'T{i}') for i in range(num_cfgs)]
        fullsymbols = init_nodes
        fullsystem = []
        splitsystems = []
        splitsymbols = []
        init_eqns = []

        for fcn_idx in range(len(dictgraphs)):

            curr_graph = dictgraphs[fcn_idx]
            init_node = init_nodes[fcn_idx]
            system = []
            symbs = []

            for startnode in curr_graph:
                endnodes = curr_graph[startnode]
                expr = 0
                sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
                symbs += [sym]
                lookupDict[sym].add(sym)

                for node in endnodes:
                    var = symbols("V" + str(node))
                    lookupDict[var].add(sym)
                    if str(node) in curr_graph: #makes sure the end node is not terminal
                        expr = expr + var*x
                    else:
                        expr = expr + x
                
                for called_fcn_idx in calldict[startnode]:
                    expr =  init_nodes[called_fcn_idx] * expr
                system += [expr - sym]
            
            if init_node not in symbs:
                symbs = [init_node] + symbs
            
            fullsystem += system
            init_eqn = symbols(f'V{fcn_idx}_0')*x - init_node
            lookupDict[symbols(f'V{fcn_idx}_0')].add(init_node)
            system = [init_eqn] + system
            init_eqns.append(init_eqn)
            splitsystems.append(system)
            splitsymbols.append(symbs)
            
            for symb in symbs:
                if symb not in fullsymbols:
                    fullsymbols.append(symb)
        
        fullsystem = init_eqns + fullsystem
        print("FULL SYSTEM:", fullsystem)
        print("FULL SYMBOLS:", fullsymbols)
        print("SPLIT SYSTEMS:", splitsystems)
        print("SPLIT SYMBOLS:", splitsymbols)
        return fullsystem, fullsymbols, splitsystems, splitsymbols, lookupDict

    def modPartialEliminate(self, system, symbs):
        """Takes in a system of equations and gets the gamma function"""
        
        if len(system) == 1:
            return system[0]
        sub = system[-1] + symbs[-1] # what the last symbol in symbs equals
        
        if symbs[-1] in sub.free_symbols: # according to yuki, this is if the last symbol is on both sides
            for eq in system:
                if symbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, symbs[-1], dict=True)
                    if len(sol) == 1:
                        sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
                        break
        
        if symbs[-1] in sub.free_symbols:
            self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
        
        for count, eq in enumerate(system):
            if symbs[-1] in eq.free_symbols:
                system[count] = sympy.expand(eq.subs(symbs[-1], sub))
        
        return self.modPartialEliminate(system[:-1], symbs[:-1])

    def modEliminate(self, systems, symbs):
        """Takes in a system of equations and gets the gamma function"""
        Teqns = []
        
        for idx, system in enumerate(systems):
            Teqn = self.modPartialEliminate(system, symbs[idx])
            Teqns += [Teqn]
        
        Tsyms = [syms[0] for syms in symbs]
        gamma = self.modPartialEliminate(Teqns,Tsyms)
        return gamma

    def optimizedPartialEliminate(self, system, symbs, lookupDict, vertices: bool):
        
        if len(system) == 1:
            return system[0]
        sub = system[-1] + symbs[-1] # what the last symbol in symbs equals
        
        if symbs[-1] in sub.free_symbols: # according to yuki, this is if the last symbol is on both sides
            for eq in system:
                if symbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, symbs[-1], dict=True)
                    if len(sol) == 1:
                        sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
                        break
        
        if symbs[-1] in sub.free_symbols:
            self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
        
        for count, eq in enumerate(system):
            if symbs[-1] in eq.free_symbols:
                system[count] = sympy.expand(eq.subs(symbs[-1], sub))
        
        return self.optimizedPartialEliminate(system[:-1], symbs[:-1], lookupDict, vertices)

    def optimizedEliminate(self, systems, symbs, lookupDict):
        """Takes in a system of equations and gets the gamma function"""
        Teqns = []
        TlookupDict = defaultdict(set)
        for idx, system in enumerate(systems):
            Teqn = self.optimizedPartialEliminate(system, symbs[idx], lookupDict, True)
            for var in Teqn.free_symbols:
                if var == symbols("x"):
                    continue
                TlookupDict[var].add(symbs[idx][0])
            Teqns += [Teqn]
        Tsyms = [syms[0] for syms in symbs]
        gamma = self.optimizedPartialEliminate(Teqns,Tsyms, TlookupDict, False)
        return gamma

    # def simpleEliminate(self, system, symbs):
    #     """Takes in a system of equations and gets the gamma function"""
    #     if len(system) == 1:
    #         return system[0]
    #     sub = system[-1] + symbs[-1]
    #     if symbs[-1] in sub.free_symbols:
    #         for eq in system:
    #             if symbs[-1] in eq.free_symbols:
    #                 sol = sympy.solve(eq, symbs[-1], dict=True)
    #                 if len(sol) == 1:
    #                     sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
    #     if symbs[-1] in sub.free_symbols:
    #         self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
    #     for count, eq in enumerate(system):
    #         if symbs[-1] in eq.free_symbols:
    #             system[count] = sympy.expand(eq.subs(symbs[-1], sub))
    #     return self.simpleEliminate(system[:-1], symbs[:-1])

#======================================END OF INTEGRATION IN PROCESS====================================================

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
        print("IN ELIM OG")
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