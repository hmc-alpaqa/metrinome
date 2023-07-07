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
import time
from sympy.utilities import lambdify
import math
import cmath

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
        return "Function Call Path Complexity"

    def evaluate(self, cfg: ControlFlowGraph, all_cfgs: List[ControlFlowGraph]) -> Union[int, PathComplexityRes]:
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        self.logger.d_msg(f"NEW FCAPC =========================================================")
        self.logger.d_msg(f"graph:{cfg.name.split('.')[1]}")
        graphProcessTime = 0.0
        start_time = time.time()
        calldict, dictgraphs = self.processGraphs(cfg, all_cfgs)
        self.logger.d_msg(f"calldict: {calldict}")
        self.logger.d_msg(f"dictgraphs: {dictgraphs}")
        graphProcessTime = time.time() - start_time
        # print("CALLDICT: ",calldict)
        # print("DICTGRAPHS: ", dictgraphs)
        # print('')
        # print("Graph Name: ", cfg.name)
        # print("ALL GRAPHS: ", all_cfgs)
        # print('')
        graphSystemsTime = 0.0
        start_time = time.time()
        splitsystems, splitsymbols, lookupDict, numNodes, idxDict = self.graphsToSystems(dictgraphs, calldict)
        self.logger.d_msg(f"split systems: {splitsystems}")
        self.logger.d_msg(f"split symbols: {splitsymbols}")
        print(cfg.rich_repr())
        self.logger.d_msg(f"lookup dict: {lookupDict}")
        self.logger.d_msg(f"idx dict: {idxDict}")
        self.logger.d_msg(f"num nodes: {numNodes}")
        graphSystemsTime = time.time() - start_time
        # modSystems = copy.deepcopy(splitsystems)
        # modSymbols = copy.deepcopy(splitsymbols)
        gammaTime = 0.0
        start_time = time.time()
        # optimizedSystems = copy.deepcopy(splitsystems)
        # optimizedSymbols = copy.deepcopy(splitsymbols)
        #ISSUE STARTS W/ SELF.ELIMINATE
        #simpleGamma = self.eliminate(fullsystem,fullsymbols)
        #modGamma = self.modEliminate(modSystems,modSymbols)
        optimizedGamma = self.optimizedEliminate(splitsystems, splitsymbols, lookupDict, idxDict)
        gammaTime = time.time() - start_time
        self.logger.d_msg(f"Gamma Function: {optimizedGamma}, time: {gammaTime}")
        # print(f'simpleGamma: {simpleGamma}')
        # print(f'modGamma: {modGamma}')
        # print(f'simpleGamma = modGamma check: {simpleGamma == modGamma}')
        # print('')
        # print(f'simpleGamma: {simpleGamma}')
        # print(f'optimizedGamma: {optimizedGamma}')
        # print(f'simpleGamma = optimizedGamma check: {simpleGamma == optimizedGamma}')

        self.apc_times["graphProcessTime"] = graphProcessTime
        self.apc_times["graphSystemsTime"] = graphSystemsTime
        self.apc_times["gammaTime"] = gammaTime
        apc = self.fcn_call_apc(optimizedGamma, numNodes)
        self.apc_times["nfcapc"] = apc
        return self.apc_times

    def fcn_call_apc(self, gamma, numNodes):
        """Calculates the apc of a function that can call other functions """
        if gamma == 0:
            return (0, 0)

        discrimTime = 0.0
        realnrootsTime = 0.0
        genFuncTime = 0.0
        rootsDictTime = 0.0
        getrgfTime = 0.0
        apcTime2 = 0.0
        cleanTime = 0.0

        start_time = time.time()
        discrim = self.calculateDiscrim(gamma)
        discrimTime = time.time() - start_time
        self.logger.d_msg(f"Discriminant: {discrim}, time:{discrimTime}")

        start_time = time.time()
        try:
            numroots = len(self.realnroots(discrim))
        except Exception as e:
            self.logger.e_msg(f"Error: {e}")
            numroots = 0
        realnrootsTime = time.time() - start_time
        self.logger.d_msg(f"realnrootsTime:{realnrootsTime}")
        if numroots == 0:
            self.logger.d_msg(f"case1")
            start_time = time.time()
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
                genFunc = sympy.simplify(sympy.factor(genFunc)) # simplifies generating function :)
                self.logger.d_msg(f"Generating Function: {genFunc}")
            else:
                # print(possibleGenFunc)
                self.logger.e_msg("PANIC PANIC Oh dear, not sure which generating function is right")
            genFuncTime = time.time()-start_time
            #rootsDict time starts here
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
            #TODO: do the numerical value of the roots
            #search in bst is taking a long time in getrgf, WHY
            #catalan1 is also taking a long time in getrgf

            numRoots = sum(rootsDict.values())
            # printRoots = {}
            # for root in rootsDict:
            #     printRoots[sympy.N(root)] = rootsDict[root]
            # print("numeric roots dict:",printRoots)
            
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
            rootsDictTime = time.time() - start_time
            self.logger.d_msg(f"Found all Roots")
            newRootsDict = {}
            for root in rootsDict:
                newRootsDict[sympy.N(root)] = rootsDict[root]
            self.logger.d_msg(f"rootsDict: {rootsDict}, time: {rootsDictTime}")
            
            start_time =  time.time()
            apc = self.getAPC(genFunc, denominator, rootsDict)
            getrgfTime = time.time()-start_time
            pc = 'na'

        else:
            self.logger.d_msg(f"case2")
            start_time = time.time()
            rStar = min(map(lambda x: x if x >10**(-PRECISION) else sympy.oo,self.realnroots(discrim)))
            if type(rStar) == sympy.polys.rootoftools.ComplexRootOf:
                rStar = sympy.N(rStar)
            self.logger.d_msg(f"rStar: {rStar}")
            pc = sympy.N(1/rStar)**symbols("n")
            self.logger.d_msg(f"pc: {pc}")
            apc = pc
            apcTime2 = time.time()-start_time

        start_time = time.time()
        if type(apc) == sympy.Add:
            # pc = simplify(pc)
            apc = big_o(list(apc.args))
        if "I" in str(apc):
            apc = sympy.simplify(self.clean(apc, symbols("n")))
        # apc = sympy.N(apc)
        cleanTime = time.time() - start_time

        self.logger.d_msg(f"apc: {apc}, cleanTime: {cleanTime}")
        self.apc_times["discrimTime"] = discrimTime
        self.apc_times["realnrootsTime"] = realnrootsTime
        self.apc_times["genFuncTime"] = genFuncTime
        self.apc_times["rootsDictTime"] = rootsDictTime
        self.apc_times["getrgfTime"] = getrgfTime
        self.apc_times["apcTime2"] = apcTime2
        self.apc_times["cleanTime"] = cleanTime
        self.apc_times["numNodes"] = numNodes
        return (apc, pc)
  
    def processGraphs(self, graph, all_graphs):
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        dictgraphs = []
        used_graphs = [graph.name.split(".")[-1]]
        graphs_to_process = deque([graph])
        calldict = defaultdict(list)
        while graphs_to_process:
            curr_graph = graphs_to_process.popleft()
            curr_graph_name = curr_graph.name
            curr_graph_edges = curr_graph.graph.edge_rules()
            curr_graph_calls = curr_graph.metadata.calls
            fcn_idx = used_graphs.index(curr_graph_name.split(".")[-1])
            curr_graph_edges = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in curr_graph_edges]
            #print(curr_graph_edges)
            edgedict = defaultdict(list)
            nodes = set()
            for edge in curr_graph_edges: #reformatting our graph from edgelist form to dictionary form
                edgedict[edge[0]].append(edge[1])
                nodes.update(edge)
            dictgraphs.append(edgedict)
            for node in curr_graph_calls.keys():
                # loop through functions that are called
                for called_fcn in curr_graph_calls[node].split(" "):
                    # add graphs to used_graphs
                    if called_fcn in ['START', 'CALLS']:
                        continue
                    if called_fcn not in used_graphs:
                        used_graphs.append(called_fcn)
                        # find graph from all_cfgs, add to graphs_to_process
                        for graph in all_graphs:
                            if graph.split(".")[-2] == called_fcn:
                                graphs_to_process.append(all_graphs[graph])
                                break
                    # Call (i, j) from function i node j to called_fcn
                    calldict[f'{fcn_idx}_{int(node)}'].append(used_graphs.index(called_fcn))

        return calldict, dictgraphs

    def graphsToSystems(self, dictgraphs, calldict):
        #print(dictgraphs)
        lookupDict = defaultdict(set)
        idxDict = {}
        x = symbols("x")
        num_cfgs = len(dictgraphs)
        init_nodes = [symbols(f'T{i}') for i in range(num_cfgs)]
        #fullsymbols = init_nodes
        #fullsystem = []
        splitsystems = []
        splitsymbols = []
        init_eqns = []
        numCalls = [0]*len(dictgraphs)
        graphNodes = [set() for i in range(len(dictgraphs))]
        for fcn_idx in range(len(dictgraphs)):
            curr_graph = dictgraphs[fcn_idx]
            init_node = init_nodes[fcn_idx]
            idxDict[init_node] = [0, int(str(init_node)[1:])]
            system = []
            symbs = []
            idx_counter = 1
            for startnode in curr_graph:
                endnodes = curr_graph[startnode]
                expr = 0
                sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
                symbs += [sym]
                lookupDict[sym].add(sym)
                idxDict[sym] = [idx_counter]
                #print(fcn_idx, endnodes)
                for node in endnodes:
                    graphNodes[fcn_idx].add(node)
                    var = symbols("V" + str(node))
                    lookupDict[var].add(sym)
                    if str(node) in curr_graph: #makes sure the end node is not terminal
                        expr = expr + var*x
                    else:                       # node is terminal
                        expr = expr + x
                        for called_fcn_idx in calldict[node]: # edge case: terminal node calls a function (see: fcn_calls/partition)
                            numCalls[called_fcn_idx] += 1

                
                for called_fcn_idx in calldict[startnode]: # handle function calls for all non-terminal nodes  (all nodes in startnodes)
                    numCalls[called_fcn_idx] += 1
                    expr =  init_nodes[called_fcn_idx] * expr
                system += [expr - sym]
                idx_counter = idx_counter + 1
            
            if init_node not in symbs:
                symbs = [init_node] + symbs
            
            #fullsystem += system
            init_eqn = symbols(f'V{fcn_idx}_0')*x - init_node
            lookupDict[symbols(f'V{fcn_idx}_0')].add(init_node)
            system = [init_eqn] + system
            init_eqns.append(init_eqn)
            splitsystems.append(system)
            splitsymbols.append(symbs)
        
        numCalls[0] += 1
        # add 2 nodes not in endnodes for each graph: V[n]_0 & T[n]
        numGraphNodes = [(len(singleGraphNodes) + 2) for singleGraphNodes in graphNodes]
        # dot product is the numNodes for coeffs
        dot_product = sum([x * y for x, y in zip(numGraphNodes, numCalls)])
        return splitsystems, splitsymbols, lookupDict, dot_product, idxDict

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

    # def optimizedPartialEliminate(self, system, symbs, lookupDict, vertices: bool):
    #     if len(system) == 1:
    #         return system[0]
    #     sub = system[-1] + symbs[-1] # what the last symbol in symbs equals
    #     print(symbs[-1])
    #     sol = []
    #     print("hi pls pls pls")
    #     if symbs[-1] in sub.free_symbols: # according to yuki, this is if the last symbol is on both sides
    #         symb_idx = int(str(symbs[-1])[1:].split("_")[-1])
    #         for eqn_symb in lookupDict[symbs[-1]]:
    #             print("EQN SYMB",eqn_symb)
    #             if vertices == False:
    #                 eq_idx = int(str(eqn_symb)[1:])
    #             elif "T" in str(eqn_symb):
    #                 eq_idx = 0
    #             else:
    #                 eq_idx = int(str(eqn_symb)[1:].split("_")[1]) + 1
    #             if eq_idx > symb_idx:
    #                 if (str(eqn_symb)[0] != "T") or (str(symbs[-1])[0] != "V"):
    #                     continue
    #                 else:
    #                     pass
    #             eq = system[eq_idx]
    #             if symbs[-1] in eq.free_symbols:
    #                 sol = sympy.solve(eq, symbs[-1], dict=True)
    #                 print("solve done")
    #                 if len(sol) == 1:
    #                     print(sol)
    #                     #sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
    #                     print("into substitution")
    #                     sub = sub.subs(symbs[-1], sol[0][symbs[-1]])
    #                     print("done w substitution")
    #                     break
        
    #     if symbs[-1] in sub.free_symbols:
    #         self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
        
    #     for eqn_symb in lookupDict[symbs[-1]]:
    #         if vertices == False:
    #                 eq_idx = int(str(eqn_symb)[1:])
    #         elif "T" in str(eqn_symb):
    #             eq_idx = 0
    #         else:
    #             eq_idx = int(str(eqn_symb)[1:].split("_")[1]) + 1

    #         if eq_idx > symb_idx:
    #             if (str(eqn_symb)[0] != "T") or (str(symbs[-1])[0] != "V"):
    #                 continue
    #             else:
    #                 pass
    #         eq = system[eq_idx]
    #         print("SUB EQ",eq)
    #         if symbs[-1] in eq.free_symbols:
    #             system[count] = eq.subs(symbs[-1], sub)
        
    #     return self.optimizedPartialEliminate(system[:-1], symbs[:-1], lookupDict, vertices)


    def optimizedPartialEliminate(self, system, symbs, lookupDict, vertices: bool, idxDict):
        #print("hi")
        #print("LEN",len(system))
        if len(system) == 1:
            return system[0]
        # print("=====run for",symbs[-1])
        # print("b4 making sub var")
        sub = system[-1] + symbs[-1] # what the last symbol in symbs equals
        # print("after making sub var")
        sol = []
        #print("eliminating",symbs[-1])
        if vertices == False:
            symb_idx = idxDict[symbs[-1]][1]
        else:
            symb_idx = idxDict[symbs[-1]][0]
        if symbs[-1] in sub.free_symbols: # according to yuki, this is if the last symbol is on both sides
            for eqn_symb in lookupDict[symbs[-1]]:
                if vertices == False:
                    eq_idx = idxDict[eqn_symb][1]
                else:
                    eq_idx = idxDict[eqn_symb][0]
                if eq_idx > symb_idx:
                    continue
                else:
                    pass
                eq = system[eq_idx]
                if symbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, symbs[-1], dict=True)
                    if len(sol) == 1:
                        #sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
                        sub = sub.subs(symbs[-1], sol[0][symbs[-1]])
                        sub = sympy.simplify(sub)
                        # print("done w substitution")
                        break
        if symbs[-1] in sub.free_symbols:
            self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
        for eqn_symb in lookupDict[symbs[-1]]:
            # print(lookupDict[symbs[-1]])
            # print("eq_symb",eqn_symb)
            if vertices == False:
                # print("case1")
                eq_idx = idxDict[eqn_symb][1]
            else:
                # print("case2")
                eq_idx = idxDict[eqn_symb][0]
                # print(eq_idx)
            if eq_idx <= symb_idx:
                # print("sub eqn found")
                eq = system[eq_idx]
                if symbs[-1] in eq.free_symbols:
                    # print("substitution pt.2")
                    system[eq_idx] = eq.subs(symbs[-1], sub)
                    system[eq_idx] = sympy.simplify(system[eq_idx])
                    if symbs[-1] in system[eq_idx].free_symbols:
                        self.logger.e_msg(f"PANIC PANIC not sure how to substitute.")
                #print("OG SYM",symbs[-1],"IN EQN SYMB",eqn_symb, "LEN IDX",symb_idx, "SUBS IDX",eq_idx, "FIN EQN",system[eq_idx])
                    # print("done w sub pt. 2")
        # for count, eq in enumerate(system):
        #     if symbs[-1] in eq.free_symbols:
        #         system[count] = sympy.expand(eq.subs(symbs[-1], sub))
        # print("run done")
        #print(system)
        return self.optimizedPartialEliminate(system[:-1], symbs[:-1], lookupDict, vertices, idxDict)

    def optimizedEliminate(self, systems, symbs, lookupDict, idxDict):
        # print("IN OPTIMIZED ELIMINATE")
        """Takes in a system of equations and gets the gamma function"""
        Teqns = []
        TlookupDict = defaultdict(set)
        for idx, system in enumerate(systems):
            Teqn = self.optimizedPartialEliminate(system, symbs[idx], lookupDict, True, idxDict)
            Teqn = sympy.simplify(Teqn)
            for var in Teqn.free_symbols:
                if var == symbols("x"):
                    continue
                TlookupDict[var].add(symbs[idx][0])
            Teqns += [Teqn]
            #print(Teqn)
        Tsyms = [syms[0] for syms in symbs]
        print("at t elims")
        print(Teqns)
        gamma = self.optimizedPartialEliminate(Teqns,Tsyms, TlookupDict, False, idxDict)
        gamma = sympy.simplify(gamma)
        return gamma

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

    # def eliminate(self, system, symbs):
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
    #     return self.eliminate(system[:-1], symbs[:-1])

    def getRhoDict(self, rootsDict):
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

    """
    Input: denominator
    Return: q0
    """
    def getQ0(self,denominator):
        q0 = Poly(sympy.expand(denominator)).all_coeffs()[-1]
        return q0


    """ Identifies other roots with same magnitude as the root with
    maximum APC.
    Input: rootsDict, rootsAPCDict
    Return: APC
    """
    def getAPC(self,genFunc, denominator, rootsDict):
        print("in new method")
        numerator = sympy.simplify(genFunc*denominator)
        print(f"numerator:{numerator}")
        rhoDict, maxRho, maxMultiplicity = self.getRhoDict(rootsDict)
        print(f"maxMultiplicity:{maxMultiplicity}")
        q0 = self.getQ0(denominator)
        coeff = 0
        print("rhoDict:",rhoDict)
        print("q0",q0)
        for rho in rhoDict:
            if (abs(rho) == abs(maxRho)) and (rhoDict[rho] == maxMultiplicity):
                Ak = sympy.N(self.shiftAk(numerator, rho)/self.calculateAk(q0, rho, rhoDict))
                print("Ak",Ak)
                coeff = coeff + Ak
                print("coeff",coeff)
        apc = sympy.simplify(coeff*(symbols("n")**(maxMultiplicity-1))*abs(sympy.N(maxRho))**symbols("n"))
        # apc = coeff*(symbols("n")**(maxMultiplicity-1))*abs(maxRho)**symbols("n")
        return apc

    """
    Input:
    Return: Denominator of Ak
    """
    def calculateAk(self,q0,rhok,rhoDict):
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
    def shiftAk(self,numerator, rhok):
        rhokDict = {symbols("x"):1/rhok}
        numeratorAK = numerator.subs(rhokDict)
        # print(numeratorAK)
        return numeratorAK


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