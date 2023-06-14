import re
from abc import ABC, abstractmethod
from collections import defaultdict, deque, Counter
from typing import Union, List
import numpy as np  # type: ignore
import sympy # type: ignore
from mpmath import mpc, mpf, polyroots  # type: ignore
from sympy import (Basic, Float, Matrix, Poly, degree, eye, preorder_traversal, simplify, symbols,
                   sympify)
import copy
import time
#from graph.control_flow_graph import ControlFlowGraph
#from graph.graph import Graph

# WE R SORRY FOR THE VARIABLE NAMES I PROMISE YOU WE SUFFERED TOO

class Eliminator:
    # graph representation: [namestring, edgelist, calldict]
    # def __init__(self):

    def processGraphs(self, graph, all_graphs):
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        dictgraphs = []
        used_graphs = [graph[0]]
        graphs_to_process = deque([graph])
        calldict = defaultdict(list)
        while graphs_to_process:
            curr_graph = graphs_to_process.popleft()
            curr_graph_name = curr_graph[0]
            curr_graph_edges = curr_graph[1]
            curr_graph_calls = curr_graph[2]
            fcn_idx = used_graphs.index(curr_graph_name)
            curr_graph_edges = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in curr_graph_edges]
            edgedict = defaultdict(list)
            for edge in curr_graph_edges: #reformatting our graph from edgelist form to dictionary form
                edgedict[edge[0]].append(edge[1])
            dictgraphs.append(edgedict)

            for node in curr_graph_calls:
                # loop through functions that are called
                for called_fcn in curr_graph_calls[node]:
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
        return calldict, dictgraphs

    def evaluate(self, all_graphs: dict, graphname):
        
        print('')
        print("Graph Name: ", graphname)
        print("ALL GRAPHS: ", all_graphs)
        print('')

        graph = all_graphs[graphname]
        lookupDict = defaultdict(set)

        calldict, dictgraphs = self.processGraphs(graph, all_graphs)
        fullsystem, fullsymbols, splitsystems, splitsymbols, lookupDict = self.graphsToSystems(dictgraphs, calldict)
        print("DICTGRAPHS", dictgraphs)

        modSystems = copy.deepcopy(splitsystems)
        modSymbols = copy.deepcopy(splitsymbols)
        optimizedSystems = copy.deepcopy(splitsystems)
        optimizedSymbols = copy.deepcopy(splitsymbols)

        simpleGamma = self.simpleEliminate(fullsystem,fullsymbols)
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

    def simpleEliminate(self, system, symbs):
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
        return self.simpleEliminate(system[:-1], symbs[:-1])

def main():

    # made up
    graphs = {
        "zero": ["zero",[[0, 1],[0, 2], [1, 2]], {2: ["one"]}],
        "one":["one",[[0, 1], [1, 2], [1, 3]],{}]
        }
    # board example
    # graphs = {
    #     "zero": ["zero", [[0, 1]], {0: ["one"]}],
    #     "one": ["one", [[0, 1], [1, 0], [1, 2]], {1: ["two"]}],
    #     "two": ["two", [[0, 1]], {}]
    #     }
    # experiments/function_calls/files.even_odd.c
    graphs = {
        "even": ["even", [[0, 1],[0, 2], [1, 3], [1, 2]], {2: ['odd']}],
        "odd": ["odd", [[0, 1], [0, 2], [1, 3], [1, 2]], {2:["even"]}]
    }
    # graphs = {
    #     "gcd": ["gcd", [[0, 1], [1, 2], [1, 6], [2, 3], [2, 4], [3, 5], [4, 5], [5, 1]], {}],
    #     "rec": ["rec", [[0, 1], [0, 2], [1, 3], [2, 3]], {2: ['CALLS', 'rec', 'rec']}],
    #     "split": ["split", [[0, 1], [0, 2], [1, 3], [2, 3]], {1: ['CALLS','rec'], 2: ['CALLS','gcd']}],
    #     "mul_inv": ["mul_inv", [[0, 1], [0, 2], [1, 8], [2, 3], [3, 4], [3, 5], [4, 3], [5, 6], [5, 7], [6, 7], [7, 8]], {}]
    # }

    graphname = "odd"
    elim = Eliminator()
    elim.evaluate(graphs, graphname)

if __name__ == "__main__":
    main()