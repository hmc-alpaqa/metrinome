import re
from abc import ABC, abstractmethod
from collections import defaultdict, deque, Counter
from typing import Union, List
​
​
import numpy as np  # type: ignore
import sympy  # type: ignore
from mpmath import mpc, mpf, polyroots  # type: ignore
from sympy import (Basic, Float, Matrix, Poly, degree, eye, preorder_traversal, simplify, symbols,
                   sympify)
#from graph.control_flow_graph import ControlFlowGraph
#from graph.graph import Graph
​
class Eliminator:
    # graph representation: [namestring, edgelist, calldict]
    def __init__(self, all_graphs: dict, graphname):
        self.graph = all_graphs[graphname]
        self.all_graphs = all_graphs
        self.calldict = defaultdict(list)
        self.dictgraphs = []
        self.systems = []
        self.systemsymbs = []
        self.fullsystem = []
        self.fullsymbs = []
        self.processGraphs()
​
    def processGraphs(self):
        """Given a graph, compute the metric."""
        # TODO: use full name of cfg (file name is deleted here)
        used_graphs = [self.graph[0]]
        graphs_to_process = deque([self.graph])
        while graphs_to_process:
            curr_graph = graphs_to_process.popleft()
            curr_graph_name = curr_graph[0]
            curr_graph_edges = curr_graph[1]
            curr_graph_calls = curr_graph[2]
            fcn_idx = used_graphs.index(curr_graph_name)
            curr_graph_edges = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in curr_graph_edges]
            edgedict = defaultdict(list)
            for edge in curr_graph_edges: #reformatting our list of edges into a dictionary where keys are edge starts, and values are lists of edge ends
                edgedict[edge[0]].append(edge[1])
            self.dictgraphs.append(edgedict)
​
            for node in curr_graph_calls:
                # loop through functions that are called
                for called_fcn in curr_graph_calls[node]:
                    # add graphs to used_graphs
                    if called_fcn in ['START', 'CALLS']:
                        continue
                    if called_fcn not in used_graphs:
                        used_graphs.append(called_fcn)
                        # find graph from all_cfgs, add to graphs_to_process
                        for graph in self.all_graphs:
                            if graph == called_fcn:
                                print("NEW")
                                graphs_to_process.append(self.all_graphs[graph])
                                break
                    # Call (i, j) from function i node j to called_fcn
                    self.calldict[f'{fcn_idx}_{int(node)}'].append(used_graphs.index(called_fcn))
        print(self.calldict)
        print(self.dictgraphs)
​
    def evaluate(self):
        self.graphsToSystems()
        gamma = self.simpleEliminate(self.fullsystem,self.fullsymbs)
        print(gamma)
​
    def graphsToSystems(self):
        systems = []
        systemsymbs = []
        init_eqns = []
        x = symbols("x")
        num_cfgs = len(self.dictgraphs)
        init_nodes = [symbols(f'T{i}') for i in range(num_cfgs)]
        for fcn_idx in range(len(self.dictgraphs)):
            print("FCNIDX:",fcn_idx)
            curr_graph = self.dictgraphs[fcn_idx]
            init_node = init_nodes[fcn_idx]
            system = []
            symbs = []
            for startnode in curr_graph:
                endnodes = curr_graph[startnode]
                expr = 0
                sym = symbols("V" + str(startnode)) #chr(int(startnode) + 65)
                symbs += [sym]
                for node in endnodes:
                    if str(node) in curr_graph: #makes sure the end node is not terminal
                        var = symbols("V" + str(node)) #str(chr(node+ 65))
                        expr = expr + var*x
                    else:
                        expr = expr + x
                
                    for called_fcn_idx in self.calldict[startnode]:
                        expr =  init_nodes[called_fcn_idx] * expr
                        symbs += [init_nodes[called_fcn_idx]]
                system += [expr - sym]
            self.fullsystem += system
            init_eqn = symbols(f'V{fcn_idx}_0')*x - init_node
            system = [init_eqn] + system
            init_eqns.append(init_eqn)
            symbs += [init_node]
            print("SYS: ", fcn_idx, "IS",system)
            self.systems.append(system)
            self.systemsymbs.append(symbs)
            for symb in symbs:
                if symb not in self.fullsymbs:
                    self.fullsymbs.append(symb)
        print(init_eqns)
        print("INIT EQNS ABOVE")
        self.fullsystem = init_eqns + self.fullsystem
        print(self.fullsystem)
        print(self.fullsymbs)
        print(self.systems)
        print(self.systemsymbs)
​
    def simpleEliminate(self, fullsys, fullsym):
        """Takes in a system of equations and gets the gamma function"""
        if len(fullsys) == 1:
            return fullsys[0]
        sub = fullsys[-1] + fullsym[-1]
        if fullsym[-1] in sub.free_symbols:
            for eq in fullsys:
                if fullsym[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, fullsym[-1], dict=True)
                    if len(sol) == 1:
                        sub = sympy.expand(sub.subs(fullsys[-1], sol[0][fullsym[-1]]))
        if fullsym[-1] in sub.free_symbols:
            print("PANIC PANIC not sure how to substitute.")
        for count, eq in enumerate(fullsys):
            if fullsym[-1] in eq.free_symbols:
                fullsys[count] = sympy.expand(eq.subs(fullsym[-1], sub))
        return sympy.expand(self.simpleEliminate(fullsys[:-1], fullsym[:-1]))
​
    def optimizedEliminate(self):
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
            print("PANIC PANIC not sure how to substitute.")
        for count, eq in enumerate(system):
            if symbs[-1] in eq.free_symbols:
                system[count] = sympy.expand(eq.subs(symbs[-1], sub))
        return sympy.expand(self.optimizedEliminate(system[:-1], symbs[:-1]))
​
def main():
    graphname = "odd"
    graphs = {"zero": ["zero",[[0, 1],[0, 2], [1, 2]], {2: ["one"]}],"one":["one",[[0, 1], [1, 2], [1, 3]],{}]}
    graphs = {"zero": ["zero", [[0, 1]], {0: ["one"]}],
              "one": ["one", [[0, 1], [1, 0], [1, 2]], {1: ["two"]}],
              "two": ["two", [[0, 1]], {}]}
    #graphs = {"zero": ["zero",[[0, 1],[0, 2], [1, 2]], {2: ["one"]}],"one":["one",[[0, 1], [1, 2], [1, 3]],{}]}
    graphs = {
        "odd": ["odd", [[0, 1], [0, 2], [1, 3], [2, 3]], {2: ["even"]}],
        "even": ["even", [[0, 1], [0, 2], [1, 3], [2, 3]], {2: ["odd"]}]
    }
    elim = Eliminator(graphs, graphname)
    elim.evaluate()
    #elim.simpleEliminate()
​
if __name__ == "__main__":
    main()