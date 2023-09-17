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
        self.logger.d_msg(f"RGF FCAPC =========================================================")
        self.logger.d_msg(f"graph name:{cfg.name.split('.')[1]}")
        self.logger.d_msg(f"cfg repr:{cfg.rich_repr()}")

        # process cfgs into dictionary graphs and call dictionary (graphProcessTime)
        graphProcessTime = 0.0
        start_time = time.time()
        calldict, dictgraphs = self.processGraphs(cfg, all_cfgs)
        self.logger.d_msg(f"calldict: {calldict}")
        self.logger.d_msg(f"dictgraphs: {dictgraphs}")
        graphProcessTime = time.time() - start_time

        # process dictionaries into systems of equations and dictionaries for substitution (graphSystemsTime)
        graphSystemsTime = 0.0
        start_time = time.time()
        splitsystems, splitsymbols, lookupDict, idxDict = self.graphsToSystems(dictgraphs, calldict)
        self.logger.d_msg(f"split systems: {splitsystems}")
        self.logger.d_msg(f"split symbols: {splitsymbols}")
        self.logger.d_msg(f"lookup dict: {lookupDict}")
        self.logger.d_msg(f"idx dict: {idxDict}")
        graphSystemsTime = time.time() - start_time

        # eliminate equations into a single gamma function with variables T0 and x (gammaTime)
        gammaTime = 0.0
        start_time = time.time()
        optimizedGamma = self.optimizedEliminate(splitsystems, splitsymbols, lookupDict, idxDict)
        gammaTime = time.time() - start_time
        self.logger.d_msg(f"Gamma Function: {optimizedGamma}, time: {gammaTime}")
        self.apc_times['gamma'] = optimizedGamma #TODO: delete for real testing

        # calculate apc from gamma function
        apc, pc = self.fcn_call_apc(optimizedGamma)

        self.apc_times["graphProcessTime"] = graphProcessTime
        self.apc_times["graphSystemsTime"] = graphSystemsTime
        self.apc_times["gammaTime"] = gammaTime
        self.apc_times["rfcapc"] = apc

        return self.apc_times

    def fcn_call_apc(self, gamma):
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
        
        # calculate discriminant (discrimTime)
        start_time = time.time()
        discrim = self.calculateDiscrim(gamma)
        discrimTime = time.time() - start_time
        self.logger.d_msg(f"Discriminant: {discrim}, time:{discrimTime}")

        # calculate roots of discriminant (realnrootsTime)
        start_time = time.time()
        try:
            numroots = len(self.realnroots(discrim))
        except Exception as e:
            self.logger.e_msg(f"Error: {e}")
            numroots = 0
        realnrootsTime = time.time() - start_time
        self.logger.d_msg(f"realnrootsTime:{realnrootsTime}")

        # case 1: discriminant has no real roots (getrgf)
        if numroots == 0:
            self.logger.d_msg(f"case1")
            self.apc_times['case'] = 1

            # solve for generating function (genFuncTime)
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
                self.logger.e_msg("PANIC PANIC Oh dear, not sure which generating function is right")
            genFuncTime = time.time()-start_time

            #find roots of denominator (rootsDictTime)
            start_time = time.time()
            denominator = 1
            for factor in genFunc.args:
                if type(factor) == sympy.Pow and factor.args[1] < 0:
                    denominator *= 1/factor
            denominator = sympy.expand(denominator)
            self.logger.d_msg(f"denominator: {denominator}")
            maxPow = 0
            for term in denominator.args:
                power = self.termPow(term, symbols("x"))
                if power > maxPow:
                    maxPow = power
            rootsDict = sympy.roots(denominator)

            numRoots = sum(rootsDict.values())

            if numRoots < maxPow: # cannot solve symbolically for roots, approximating solutions via nroots
                self.logger.d_msg("numRoots < maxPow, approximating roots via nroots")
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

            if numRoots < maxPow: # cannot find all roots, via symbolic or numeric methods
                raise Exception("Can't find all the roots :(")

            rootsDictTime = time.time() - start_time
            self.logger.d_msg(f"Found all Roots")
            self.logger.d_msg(f"rootsDict: {rootsDict}, time: {rootsDictTime}")
            
            # getrgf method (general expansion theorem for rational generating function)
            start_time =  time.time()
            apc = self.getAPC(genFunc, denominator, rootsDict)
            getrgfTime = time.time()-start_time
            pc = 'na'

        # case 2: discriminant has real roots
        else:
            self.logger.d_msg(f"case2")
            self.apc_times['case'] = 2
            start_time = time.time()
            rStar = min(map(lambda x: x if x >10**(-PRECISION) else sympy.oo,self.realnroots(discrim)))
            if type(rStar) == sympy.polys.rootoftools.ComplexRootOf:
                rStar = sympy.N(rStar)
            self.logger.d_msg(f"rStar: {rStar}")
            pc = sympy.N(1/rStar)**symbols("n")
            self.logger.d_msg(f"pc: {pc}")
            apc = pc
            apcTime2 = time.time()-start_time

        # clean apc and report apc
        start_time = time.time()
        if type(apc) == sympy.Add:
            apc = big_o(list(apc.args))
        if "I" in str(apc):
            apc = sympy.simplify(self.clean(apc, symbols("n")))
        cleanTime = time.time() - start_time
        self.logger.d_msg(f"apc: {apc}, cleanTime: {cleanTime}")

        # report times to dictionary
        self.apc_times["discrimTime"] = discrimTime
        self.apc_times["realnrootsTime"] = realnrootsTime
        self.apc_times["genFuncTime"] = genFuncTime
        self.apc_times["rootsDictTime"] = rootsDictTime
        self.apc_times["getrgfTime"] = getrgfTime
        self.apc_times["apcTime2"] = apcTime2
        self.apc_times["cleanTime"] = cleanTime
        return (apc, pc)
  
    def processGraphs(self, graph, all_graphs):
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        dictgraphs = []
        used_graphs = [graph.name.split(".")[-1]]
        graphs_to_process = deque([graph]) # list of graphs left to process for current function (graphs of functions that are called + graph of original function)
        calldict = defaultdict(list)

        # processing a new function graph
        while graphs_to_process:
            curr_graph = graphs_to_process.popleft()
            curr_graph_name = curr_graph.name
            curr_graph_edges = curr_graph.graph.edge_rules()
            curr_graph_calls = curr_graph.metadata.calls
            fcn_idx = used_graphs.index(curr_graph_name.split(".")[-1]) # index graphs for use in systems later
            curr_graph_edges = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in curr_graph_edges] # rename vertices for use in systems later
            edgedict = defaultdict(list)
            nodes = set()
            for edge in curr_graph_edges: #reformatting our graph from edgelist form to dictionary form
                edgedict[edge[0]].append(edge[1])
                nodes.update(edge)
            dictgraphs.append(edgedict) # append to rest of graphs in dictionary form
            for node in curr_graph_calls.keys(): # loop through nodes that call other functions
                for called_fcn in curr_graph_calls[node].split(" "): # loop through functions that are called by that node
                    # add graphs to used_graphs
                    if called_fcn in ['START', 'CALLS']: # label is not an actual call
                        continue
                    if called_fcn not in used_graphs: # if function hasn't been called and processed earlier
                        used_graphs.append(called_fcn) # add new functions being called to used_graphs
                        # find graph from all_cfgs, add to graphs_to_process
                        for graph in all_graphs:
                            if graph.split(".")[-2] == called_fcn:
                                graphs_to_process.append(all_graphs[graph]) # add new functions to list of graphs to process
                                break
                    # add all calls (not just ones to new functions) to calldict: Call (i, j) from function i node j to called_fcn
                    calldict[f'{fcn_idx}_{int(node)}'].append(used_graphs.index(called_fcn))

        return calldict, dictgraphs

    def graphsToSystems(self, dictgraphs, calldict):
        lookupDict = defaultdict(set) # lookupDict is of format {symb: [every symbol whose equation contains symb]}, used for substitution in eliminate
        idxDict = {} # contains the index of each symbol's equation in its respective system (T symbols have 2, depending on vertex or T elimination)
        x = symbols("x")
        num_cfgs = len(dictgraphs)
        init_nodes = [symbols(f'T{i}') for i in range(num_cfgs)]
        splitsystems = [] # (list of lists) list of graphs' systems (each system is a list of symbolic equations)
        splitsymbols = [] # (list of lists) list of graphs' symbols
        init_eqns = [] # list of initial equations

        for fcn_idx in range(len(dictgraphs)): # loop through all function graphs in order
            curr_graph = dictgraphs[fcn_idx]
            init_node = init_nodes[fcn_idx]
            idxDict[init_node] = [0, int(str(init_node)[1:])]
            system = [] # system of eqns for this specific graph
            symbs = [] # list of symbols in this graph's system
            idx_counter = 1 # tracks the index of each symbol's equation in the system
            for startnode in curr_graph: # each non-terminal node/symbol has its own equation, loop builds the expression equal to each non-terminal node
                endnodes = curr_graph[startnode]
                expr = 0
                sym = symbols("V" + str(startnode))
                symbs += [sym] # adding symbol to graph's list of symbols
                lookupDict[sym].add(sym) # adding the symbol to the list of symbols in this symbol's equation
                idxDict[sym] = [idx_counter] # adding the index of this symbol's eqn into the idxDict
                for node in endnodes: # constructing the equation for this node/symbol by looping through each child of the node/symbol
                    var = symbols("V" + str(node))
                    lookupDict[var].add(sym) # adding our parent node/symbol to the lookupDict for each child of the node/symbol
                    if str(node) in curr_graph: #makes sure the child node is not terminal
                        expr = expr + var*x # adding non-terminal nodes/children to the expression
                    else: # child node is terminal
                        add_to_expr = x
                        for called_fcn_idx in calldict[node]: # terminal child node calls function
                            add_to_expr = init_nodes[called_fcn_idx] * add_to_expr # include terminal child's function calls
                        expr = expr + add_to_expr # adding terminal nodes/children to the expression
                
                for called_fcn_idx in calldict[startnode]: # handle function calls for all non-terminal nodes  (all nodes in startnodes)
                    expr =  init_nodes[called_fcn_idx] * expr
                system += [expr - sym]
                idx_counter = idx_counter + 1
            
            if init_node not in symbs:
                symbs = [init_node] + symbs
            
            init_eqn = symbols(f'V{fcn_idx}_0')*x - init_node
            lookupDict[symbols(f'V{fcn_idx}_0')].add(init_node)
            system = [init_eqn] + system
            init_eqns.append(init_eqn)
            splitsystems.append(system)
            splitsymbols.append(symbs)
        
        return splitsystems, splitsymbols, lookupDict, idxDict

    def optimizedPartialEliminate(self, system, symbs, lookupDict, vertices: bool, idxDict):
        if len(system) == 1:
            return system[0]
        sub = system[-1] + symbs[-1] # what the last symbol in symbs equals
        if vertices == False:
            symb_idx = idxDict[symbs[-1]][1]
        else:
            symb_idx = idxDict[symbs[-1]][0]
        if symbs[-1] in sub.free_symbols: # if the last symbol is on both sides, we must solve for it before substituting it out
            subs_options = lookupDict[symbs[-1]] # all the equations in the system containing symbs[-1] (all options for substitution)

            # these 2 lines below implement the sorting of substitution options by simplicity during T elimination
            # they are only necessary to prevent really long gammaTimes from occuring with certain functions (intergrated-digits-squaring-2.c)
            # they can be commented out to return to the older version without this optimization, which is often faster
            if vertices == False:
                subs_options = self.simpleOrder(system, subs_options, idxDict, vertices)

            # loop through substitution options
            for eqn_symb in subs_options:
                if vertices == False:
                    eq_idx = idxDict[eqn_symb][1]
                else:
                    eq_idx = idxDict[eqn_symb][0]
                if eq_idx > symb_idx:
                    continue
                else:
                    pass
                eq = system[eq_idx]
                # extra check that our symbol is in the equation
                if symbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, symbs[-1], dict=True)
                    if len(sol) == 1: # we have found a unique (non-quadratic) solution
                        sub = sub.subs(symbs[-1], sol[0][symbs[-1]])
                        sub = sympy.simplify(sub)
                        break
        if symbs[-1] in sub.free_symbols:
            self.logger.e_msg(f"PANIC PANIC no unique solution found for {symbs[-1]}, not sure how to substitute.")
        for eqn_symb in lookupDict[symbs[-1]]:
            if vertices == False:
                eq_idx = idxDict[eqn_symb][1]
            else:
                eq_idx = idxDict[eqn_symb][0]
            if eq_idx <= symb_idx:
                eq = system[eq_idx]
                if symbs[-1] in eq.free_symbols:
                    system[eq_idx] = eq.subs(symbs[-1], sub)
                    system[eq_idx] = sympy.simplify(system[eq_idx])
                    for symbol in sub.free_symbols:
                        if symbol != symbols("x"):
                            lookupDict[symbol].add(eqn_symb)
                    if symbs[-1] in system[eq_idx].free_symbols:
                        self.logger.e_msg(f"PANIC PANIC failed to substitute solution for {symbs[-1]} not sure how to substitute.")
        return self.optimizedPartialEliminate(system[:-1], symbs[:-1], lookupDict, vertices, idxDict)

    def optimizedEliminate(self, systems, symbs, lookupDict, idxDict):
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
        Tsyms = [syms[0] for syms in symbs]
        gamma = self.optimizedPartialEliminate(Teqns,Tsyms, TlookupDict, False, idxDict)
        gamma = sympy.simplify(gamma)
        return gamma

    def simpleOrder(self, system, symblist, idxDict, vertices):
        """Orders the potential legitimate substitution options for a symbol in order of simplicity"""
        lengthDictionary = {}
        for symb in symblist:
            if vertices:
                idx = idxDict[symb][0]
            else:
                idx = idxDict[symb][1]
            if idx < len(system):
                lengthDictionary[symb] = len(str(system[idx]))
        sorted_symbols_by_simplicity = sorted(lengthDictionary.items(), key=lambda x:x[1], reverse=False)
        sorted_options = [pair[0] for pair in sorted_symbols_by_simplicity]
        return sorted_options


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

    def getRhoDict(self, rootsDict):
        rhoDict = {}
        maxRho = 0
        maxMultiplicity = 0
        for root in rootsDict:
            rho = 1/sympy.N(root)
            multiplicity = rootsDict[root]
            rhoDict[rho] = rootsDict[root]
            if (abs(rho) - abs(maxRho) >= 10**(-10)): #if the difference in the absolute value is greater than 10 decimal
                maxRho = rho
                maxMultiplicity = multiplicity
            elif (abs(abs(rho) - abs(maxRho)) < 10**(-10)): #abs(rho) == abs(maxRho) within 10 decimal
                maxMultiplicity = max(maxMultiplicity,multiplicity)
        maxRho = abs(maxRho)
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

        numerator = sympy.simplify(sympy.factor(genFunc*denominator))
        if sympy.polys.polytools.degree(numerator) >= sympy.polys.polytools.degree(denominator):
            quotient, remainder = sympy.div(numerator, denominator)
            numerator = remainder
        self.logger.d_msg(f"numerator: {numerator}")
        rhoDict, maxRho, maxMultiplicity = self.getRhoDict(rootsDict)
        self.logger.d_msg(f"rhoDict: {rhoDict}")
        self.logger.d_msg(f"maxMultiplicity: {maxMultiplicity}")
        self.logger.d_msg(f"maxMagnitude: {abs(maxRho)}")
        q0 = self.getQ0(denominator)
        coeff = 0
        self.logger.d_msg(f"q0: {q0}")
        for rho in rhoDict:
            if (abs(abs(rho) - maxRho) < 10**(-10)) and (rhoDict[rho] == maxMultiplicity):
                Ak = sympy.N(self.shiftAk(numerator, rho)/self.calculateAk(q0, rho, rhoDict))
                self.logger.d_msg(Ak)
                coeff = coeff + Ak
        self.logger.d_msg(f"coeff: {coeff}")
        apc = sympy.simplify(coeff*(symbols("n")**(maxMultiplicity-1))*sympy.N(maxRho)**symbols("n"))
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
                productory *= (1-sympy.N(rho)/sympy.N(rhok))**rhoDict[rho]
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
    def shiftAk(self,numerator, rhok):
        rhokDict = {symbols("x"):1/rhok}
        numeratorAK = numerator.subs(rhokDict)
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
        else:
            numroots = sympy.nroots(eq, n=(PRECISION + 1), maxsteps=1000)
        realnroots = []
        for root in numroots:
            if sympy.Abs(sympy.im(root))<10**(-PRECISION):
                realnroots += [sympy.re(root)]
        return realnroots