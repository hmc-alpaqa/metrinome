import re
from abc import ABC, abstractmethod
from collections import defaultdict, deque, Counter
from typing import Union, List


import numpy as np  # type: ignore
import sympy  # type: ignore
from mpmath import mpc, mpf, polyroots  # type: ignore
from sympy import (Basic, Float, Matrix, Poly, degree, eye, preorder_traversal, simplify, symbols,
                   sympify)
from graph.control_flow_graph import ControlFlowGraph
from graph.graph import Graph

class Eliminator:

    def __init__(self, systems = []):
        self.systems = systems
        self.fullsystem = [eqn for system in self.systems for eqn in system]
        self.symbs = []
        self.fullsymbs = set()
        self.parse()

    def graphsToSystems(self, graph: Tuple, all_graphs: List[tuple]):
        """Given a graph, compute the metric."""
        call_list = []
        dictgraphs = []
        # TODO: use full name of cfg (file name is deleted here)
        used_graphs = [graph]
        #print('CFG NAME', cfg.name.split('.')[1])
        graphs_to_process = deque([graph])
        while graphs_to_process:
            curr_graph = graphs_to_process.popleft()
            curr_graph_edges = curr_graph[0]
            curr_graph_calls = curr_graph[1]
            fcn_idx = used_graphs.index(curr_graph)
            edgedict = defaultdict(list)
            calldict = defaultdict(list)
            for edge in curr_graph_edges: #reformatting our list of edges into a dictionary where keys are edge starts, and values are lists of edge ends
                edgedict[edge[0]].append(edge[1])
            for node in curr_graph_calls:
                call_list = []
                # loop through functions that are called
                for called_fcn in curr_graph_calls[node]:
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
            # add fcn_idx to tuple (i, j) where i is fcn_idx and j is node num
            # edge_list = [((fcn_idx, edge[0]), (fcn_idx, edge[1])) for edge in edge_list]
            edge_list = [(f'{fcn_idx}_{edge[0]}', f'{fcn_idx}_{edge[1]}') for edge in edge_list]
            all_edges.append(edge_list)

    def parse(self):
        x = symbols("x")
        for system in self.systems:
            syms = []
            for eqn in system:
                eqn.split(" ")
                for symb in eqn:
                    if ("V" in symb) or ("T" in symb): # replace with if symb contains V, T, or x
                        syms.append(symb)
                eqn = sympify(eqn, locals=symbols(syms))
        print(self.systems)
                        #self.fullsymbs.add(symbols(symb))
            #self.symbs += list(systemsymbs)
        #self.fullsymbs = list(self.fullsymbs)

        #num_cfgs = max([int(edge[0].split('_')[0]) for edge in edgelist]) + 1
    '''
        init_nodes = [symbols(f'T{i}') for i in range(len(edgedict))]
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
        print("INIT:",init_eqns)
        symbs = init_nodes + symbs
        print("SYMBS:", symbs)
        full_sys = init_eqns + system
        print('SYSTEM', full_sys)
        '''

    def simpleEliminate(self):
        """Takes in a system of equations and gets the gamma function"""
        if len(self.fullsystem) == 1:
            return self.fullsystem[0]
        sub = self.fullsystem[-1] + self.fullsymbs[-1]
        if self.fullsymbs[-1] in sub.free_symbols:
            for eq in self.fullsystem:
                if self.fullsymbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, self.fullsymbs[-1], dict=True)
                    if len(sol) == 1:
                        sub = sympy.expand(sub.subs(self.fullsymbs[-1], sol[0][self.fullsymbs[-1]]))
        if symbs[-1] in sub.free_symbols:
            print("PANIC PANIC not sure how to substitute.")
        for count, eq in enumerate(self.fullsystem):
            if self.fullsymbs[-1] in eq.free_symbols:
                self.fullsystem[count] = sympy.expand(eq.subs(self.fullsymbs[-1], sub))
        return sympy.expand(self.simpleEliminate(self.fullsystem[:-1], self.fullsymbs[:-1]))

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

def main():
    systems = [["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"], ["-T1 + V1_0*x", "-V1_0 + V1_1*x + V1_2*x", "-V1_1 + x", "T0*x - V1_2"]]
    edgedict = [{"T0":["V0_0"],"V0_0":["V0_1","V0_2"],"V0_1":["V0_3"],"V0_2":[]}]
    elim = Eliminator(systems)
    #elim.simpleEliminate()

if __name__ == "__main__":
    main()