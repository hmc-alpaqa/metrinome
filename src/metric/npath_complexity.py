"""
Computes NPathComplexity for a given Graph object.

This works with both the adjacency list representation and edge list.
"""

import copy
from typing import Tuple

import numpy as np  # type: ignore

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from graph.graph import AdjListGraph, AdjMatGraph, EdgeListType
from metric import metric

EdgeType = list[int]
NodeType = int
AdjList = Tuple[Tuple[int, ...], ...]


class NPathComplexity(metric.MetricAbstract):
    """NPathComplexity allows us to compute the NPath Complexity of functions from their CFGs."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new NPathComplexity to compute NPath for arbitrary Graph objects."""
        self.logger = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "NPath Complexity"

    def neighbors_edge_list(self, start: NodeType, edges: list[EdgeType]) -> list[NodeType]:
        """Return a list of all the nodes we can get to from a given 'start' node."""
        return [edge[1] for edge in edges if edge[0] == start]

    def neighbors_adj_list(self, start: NodeType,
                           edges: AdjList) -> tuple[NodeType, ...]:
        """Return a list of all the nodes we can get to from a given 'start' node."""
        return edges[start]

    def remove_edge_list(self, edge_list: list[EdgeType], edge: EdgeType) -> list[EdgeType]:
        """Return an edgeList with the specified edge removed."""
        i = edge_list.index(edge)
        return edge_list[:i] + edge_list[i + 1:]

    def remove_edge_adj_list(self, edges: AdjList,
                             start: NodeType, end: NodeType) -> AdjList:
        """Return an edgeDictionary with the specified edge removed."""
        i = edges[start].index(end)
        return edges[:start] + tuple([edges[start][:i] + edges[start][i + 1:]]) + edges[start + 1:]

    def remove_edge_adj_matrix(self, matrix: np.ndarray,
                               node: NodeType, edge: NodeType) -> np.ndarray:
        """Return copy of matrix with the specified edge removed."""
        matrix_copy = copy.deepcopy(matrix)
        matrix_copy[node][edge] = 0
        return matrix_copy

    def npath_adj_list(self, start: NodeType, end: NodeType,
                       edges: AdjList) -> float:
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

    def npath_edge_list(self, start: NodeType, end: NodeType, edges: EdgeListType) -> float:
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

    def npath_adj_matrix(self, matrix: np.ndarray, start: NodeType,
                         end: NodeType, node_index: NodeType) -> float:
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

    def evaluate(self, cfg: ControlFlowGraph) -> int:
        """Compute the NPath complexity of a function given its CFG."""
        graph = cfg.graph
        if isinstance(graph, AdjListGraph):
            edges_tuple = tuple(tuple(edges) for edges in graph.edges)
            return int(self.npath_adj_list(graph.start_node, graph.end_node, edges_tuple))

        if isinstance(graph, AdjMatGraph):
            return int(self.npath_adj_matrix(graph.adjacency_matrix(), graph.start_node,
                                             graph.end_node, graph.start_node))

        return int(self.npath_edge_list(graph.start_node, graph.end_node, graph.edge_rules()))
