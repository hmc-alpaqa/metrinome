'''
Computes NPathComplexity for a given Graph object.
This works with both the adjacency list representation
and edge list.
'''

import copy
from typing import List
from graph import Graph
from metric import metric

EdgeType = List[int]
NodeType = int

class NPathComplexity(metric.MetricAbstract):
    '''
    NPathComplexity allows us to compute the NPath Complexity of some
    function from its Control Flow Graph.
    '''

    def __init__(self) -> None:
        super(NPathComplexity, self).__init__()

    def name(self) -> str:
        '''
        Returns the name of the metric computed by this class.
        '''
        return "NPath Complexity"

    def neighbors(self, start: NodeType, edges: List[EdgeType]) -> List[NodeType]:
        '''
        LIST METHOD
        Return a list of all the nodes we can get to from a
        given 'start' node
        '''
        return [edge[1] for edge in edges if edge[0] == start]

    def neighbors_dict(self, start: NodeType, edges):
        '''
        DICTIONARY METHOD
        Return a list of all the nodes we can get to from a
        given 'start' node
        '''
        return edges[start]

    def remove_edge(self, edge_list: List[EdgeType], edge: EdgeType) -> List[EdgeType]:
        '''
        LIST METHOD
        Return an edgeList with the specified edge removed.
        '''
        return list(filter(lambda existing_edge: existing_edge != edge, edge_list))

    def remove_edge_dict(self, edges, node, edge):
        '''
        DICT METHOD
        Return an edgeDictionary with the specified edge removed.
        '''
        edge_copy = copy.deepcopy(edges)
        edge_copy[node].remove(edge)
        return edge_copy

    def npath(self, start: NodeType, end: NodeType, edges) -> float:
        '''
        Helper function used to compute NPath Complexity recursively
        '''
        if start == end:
            return 1.

        total = 0.
        for neighbor in self.neighbors(start, edges):
            # Delete the edge [start, u] from the graph
            new_edges = self.remove_edge(edges, [start, neighbor])

            # Recursive call from new edge
            total += self.npath(neighbor, end, new_edges)

        return total

    def npath_dict(self, start: NodeType, end: NodeType, edges) -> float:
        '''
        Helper function used to compute NPath Complexity recursively
        '''
        if start == end:
            return 1.

        total = 0.
        neighbors = self.neighbors_dict(start, edges)
        for neighbor in neighbors:
            # Delete the edge [start, u] from the graph
            new_edges = self.remove_edge_dict(edges, start, neighbor)
            # Recursive call from new edge
            total += self.npath_dict(neighbor, end, new_edges)

        return total

    def evaluate(self, graph: Graph) -> float:
        '''
        LIST
        Compute the NPath complexity of a function given its CFG
        '''
        return self.npath(graph.start_node, graph.end_node, graph.edge_rules())

    def evaluate_dict(self, graph: Graph) -> float:
        '''
        DICT
        Compute the NPath complexity of a function given its CFG
        '''
        return self.npath_dict(graph.start_node, graph.end_node, graph.edge_rules())
