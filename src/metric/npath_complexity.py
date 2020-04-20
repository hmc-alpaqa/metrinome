"""
Computes NPathComplexity for a given Graph object.

This works with both the adjacency list representation and edge list.
"""

import copy
from typing import List
from graph import Graph
from metric import metric

EdgeType = List[int]
NodeType = int


class NPathComplexity(metric.MetricAbstract):
    """NPathComplexity allows us to compute the NPath Complexity of functions from their CFGs."""

    def __init__(self, log=None, using_list=True) -> None:
        """Create a new NPathComplexity to compute NPath for arbitrary Graph objects."""
        super(NPathComplexity, self).__init__()
        self.using_list = using_list
        self.log = log

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "NPath Complexity"

    def neighbors(self, start: NodeType, edges: List[EdgeType]) -> List[NodeType]:
        """Return a list of all the nodes we can get to from a given 'start' node."""
        return [edge[1] for edge in edges if edge[0] == start]

    def neighbors_dict(self, start: NodeType, edges):
        """Return a list of all the nodes we can get to from a given 'start' node."""
        return edges[start]

    def remove_edge(self, edge_list: List[EdgeType], edge: EdgeType) -> List[EdgeType]:
        """Return an edgeList with the specified edge removed."""
        return list(filter(lambda existing_edge: existing_edge != edge, edge_list))

    def remove_edge_dict(self, edges, node, edge):
        """Return an edgeDictionary with the specified edge removed."""
        edge_copy = copy.deepcopy(edges)
        edge_copy[node].remove(edge)
        return edge_copy
    
    def node_to_index_helper(self, start, end, node):
        """Finds the index for the row or column of an adjacency matrix"""
        if node == start:
            node_index = 0
        elif node == end:
            node_index = 1
        else:
            node_index = node+1
        return node_index

    def index_to_node_helper(self, start, end, node_index):
        """Finds the index for the row or column of an adjacency matrix"""
        if node_index == 0:
            node = start
        elif node_index == 1:
            node = end
        else:
            node = node_index-1
        return node_index

    def remove_edge_adj(self, matrix, start: NodeType, end: NodeType, node: NodeType, edge: NodeType):
        """Return copy of matrix with the specified edge removed."""
        matrix_copy = copy.deepcopy(matrix)
        node_index = self.node_to_index_helper(start, end, node)
        edge_index = self.node_to_index_helper(start, end, edge)
        matrix_copy[node_index][edge_index] = 0
        return matrix_copy

    def npath(self, start: NodeType, end: NodeType, edges) -> float:
        """Compute NPath Complexity recursively."""
        if start == end:
            return 1.

        total = 0.
        for neighbor in self.neighbors(start, edges):
            # Delete the edge [start, u] from the graph.
            new_edges = self.remove_edge(edges, [start, neighbor])

            # Recursive call from new edge.
            total += self.npath(neighbor, end, new_edges)

        return total

    def npath_dict(self, start: NodeType, end: NodeType, edges) -> float:
        """Compute NPath Complexity recursively."""
        if start == end:
            return 1.

        total = 0.
        neighbors = self.neighbors_dict(start, edges)
        for neighbor in neighbors:
            # Delete the edge [start, u] from the graph.
            new_edges = self.remove_edge_dict(edges, start, neighbor)
            # Recursive call from new edge.
            total += self.npath_dict(neighbor, end, new_edges)

        return total

    def npath_adj(self, matrix, start: NodeType, end: NodeType, node) -> float:
        """Compute NPath Complexity recursively."""
        if node == end:
            return 1.

        total = 0.
        node_index = self.node_to_index_helper(start, end, node)
        for neighbor_index in len(matrix[node_index]):
            if matrix[node_index][neighbor_index] == 1:
                neighbor_node = self.index_to_node_helper(start, end, neighbor_index)
                # Delete the edge [start, u] from the graph.
                new_matrix = self.remove_edge_dict_adj(self, matrix, start, end, node, neighbor_node)
                # Recursive call from new edge.
                total += self.npath_adj(new_matrix, start, end, neighbor_node)

        return total

    def evaluate(self, graph: Graph) -> float:
        """Compute the NPath complexity of a function given its CFG."""
        if self.using_list:
            return self.npath(graph.start_node, graph.end_node, graph.edge_rules())
        elif self.using_adjacency_matrix:
            matrix = self.graph.adjacency_matrix()
            return self.npath_adj(matrix, graph.start_node, graph.end_node, graph.start_node)
        else:
            return self.npath_dict(graph.start_node, graph.end_node, graph.edge_rules())
