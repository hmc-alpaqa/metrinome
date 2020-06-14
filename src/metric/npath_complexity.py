"""
Computes NPathComplexity for a given Graph object.

This works with both the adjacency list representation and edge list.
"""

import copy
from typing import List
from graph import Graph, GraphType
from metric import metric
from log import Log

EdgeType = List[int]
NodeType = int


class NPathComplexity(metric.MetricAbstract):
    """NPathComplexity allows us to compute the NPath Complexity of functions from their CFGs."""

    def __init__(self, logger: Log=None) -> None:
        """Create a new NPathComplexity to compute NPath for arbitrary Graph objects."""
        self.log = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "NPath Complexity"

    def neighbors_edge_list(self, start: NodeType, edges: List[EdgeType]) -> List[NodeType]:
        """Return a list of all the nodes we can get to from a given 'start' node."""
        return [edge[1] for edge in edges if edge[0] == start]

    def neighbors_adj_list(self, start: NodeType, edges):
        """Return a list of all the nodes we can get to from a given 'start' node."""
        return edges[start]

    def remove_edge_list(self, edge_list: List[EdgeType], edge: EdgeType) -> List[EdgeType]:
        """Return an edgeList with the specified edge removed."""
        i = edge_list.index(edge)
        return edge_list[:i] + edge_list[i + 1:]
        # return list(filter(lambda existing_edge: existing_edge != edge, edge_list))

    def remove_edge_adj_list(self, edges, start, end):
        """Return an edgeDictionary with the specified edge removed."""
        # edge_copy = copy.deepcopy(edges)
        # edge_copy[start].remove(end)
        # return edge_copy
        i = edges[start].index(end)
        return edges[:start] + tuple([edges[start][:i] + edges[start][i + 1:]]) + edges[start + 1:]

    def remove_edge_adj_matrix(self, matrix, node: NodeType, edge: NodeType):
        """Return copy of matrix with the specified edge removed."""
        matrix_copy = copy.deepcopy(matrix)
        matrix_copy[node][edge] = 0
        return matrix_copy

    def npath_adj_list(self, start: NodeType, end: NodeType, edges) -> float:
        """Compute NPath Complexity recursively."""
        if start == end:
            return 1.

        total = 0.
        for neighbor in self.neighbors_adj_list(start, edges):
            # Delete the edge [start, u] from the graph.
            new_edges = self.remove_edge_adj_list(edges, start, neighbor)

            # Recursive call from new edge.
            total += self.npath_adj_list(neighbor, end, new_edges)

        return total

    def npath_edge_list(self, start: NodeType, end: NodeType, edges) -> float:
        """Compute NPath Complexity recursively."""
        if start == end:
            return 1.

        total = 0.
        neighbors = self.neighbors_edge_list(start, edges)
        for neighbor in neighbors:
            # Delete the edge [start, u] from the graph.
            new_edges = self.remove_edge_list(edges, [start, neighbor])
            # Recursive call from new edge.
            total += self.npath_edge_list(neighbor, end, new_edges)

        return total

    def npath_adj_matrix(self, matrix, start: NodeType, end: NodeType, node_index) -> float:
        """Compute NPath Complexity recursively."""
        # first call passes in start (node = node_index = 0), otherwise, pass in node_index

        # node_index for end = 1
        if node_index == 1:
            return 1.

        total = 0.
        for neighbor_index in range(len(matrix[node_index])):
            if matrix[node_index][neighbor_index] == 1:
                # Delete the edge [start, u] from the graph.
                new_matrix = self.remove_edge_adj_matrix(matrix, node_index, neighbor_index)
                # Recursive call from new edge.
                total += self.npath_adj_matrix(new_matrix, start, end, neighbor_index)

        return total

    def evaluate(self, graph: Graph) -> float:
        """Compute the NPath complexity of a function given its CFG."""
        if graph.graph_type is GraphType.ADJACENCY_LIST:
            edges_tuple = tuple(tuple(edges) for edges in graph.edges)
            return self.npath_adj_list(graph.start_node, graph.end_node, edges_tuple)

        if graph.graph_type is GraphType.ADJACENCY_MATRIX:
            return self.npath_adj_matrix(graph.adjacency_matrix(), graph.start_node,
                                         graph.end_node, graph.start_node)

        if graph.graph_type is GraphType.EDGE_LIST:
            return self.npath_edge_list(graph.start_node, graph.end_node, graph.edge_rules())

        return 0.
