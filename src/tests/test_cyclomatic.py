"""This module tests that we can compute cyclomatic complexity for any Graph."""

import unittest
import sys
from typing import List
import numpy as np  # type: ignore
sys.path.append("/app/code/")
from graph import Graph, GraphType, AdjListType
from control_flow_graph import ControlFlowGraph as CFG
from metric.cyclomatic_complexity import CyclomaticComplexity
from log import Log


class TestCyclomaticComplexity(unittest.TestCase):
    """Tests for the object that computes Cyclomatic Complexity for an arbitrary Graph."""

    def test_name(self) -> None:
        """Verify that the converter has the correct name."""
        self.assertEqual(CyclomaticComplexity(Log()).name(), "Cyclomatic Complexity")

    def test_cyclomatic_complexity_edge_list(self) -> None:
        """
        Verify cyclomatic complexity value for regular graph.

        Compute the cyclomatic complexity for a graph with a non-zero number of vertices
        (where the start node is not the same as the end node) and non-zero number of edges.
        """
        edges = [[0, 1], [1, 2], [3, 4]]
        vertices = [0, 1, 2, 3, 4]
        start_node = 0
        end_node = 4
        graph = CFG(Graph(edges, vertices, start_node, end_node, graph_type=GraphType.EDGE_LIST))
        result = CyclomaticComplexity(Log()).evaluate(graph)
        expected_result = 3 - 5 + 2  # edges - nodes + 2
        self.assertEqual(result, expected_result)

        adjacencies: AdjListType = [[1], [2], [], [4], []]
        graph = CFG(Graph(adjacencies, vertices, start_node, end_node,
                          graph_type=GraphType.ADJACENCY_LIST))
        result = CyclomaticComplexity(Log()).evaluate(graph)
        self.assertEqual(result, expected_result)

        edges = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])
        graph = CFG(Graph(edges, vertices, start_node, end_node,
                          graph_type=GraphType.ADJACENCY_MATRIX))
        result = CyclomaticComplexity(Log()).evaluate(graph)
        self.assertEqual(result, result)

    def test_cyclomatic_complexity_no_edges(self) -> None:
        """
        Verify cyclomatic complexity value for graph with no edges.

        Compute the cyclomatic complexity for a graph with a non-zero number of vertices
        (where the start node is not the same as the end node) and zero number of edges.
        """
        edges: List[List[int]] = []
        vertices = [0, 1]
        start_node = 0
        end_node = 1

        # graph type is edge_list.
        graph_edge = CFG(Graph(edges, vertices, start_node, end_node,
                               graph_type=GraphType.EDGE_LIST))
        result_edge = CyclomaticComplexity(Log()).evaluate(graph_edge)
        expected_result_edge = 0 - 2 + 2  # edges - nodes + 2
        self.assertEqual(result_edge, expected_result_edge)

        # graph type is list.
        graph_list = CFG(Graph(edges, vertices, start_node, end_node,
                               graph_type=GraphType.ADJACENCY_LIST))
        result_list = CyclomaticComplexity(Log()).evaluate(graph_list)
        expected_result_list = 0 - 0 + 2  # edges - nodes + 2
        self.assertEqual(result_list, expected_result_list)

        # graph type is matrix.
        graph_matrix = CFG(Graph(np.zeros((0, 0), dtype=np.int8), vertices, start_node, end_node,
                                 graph_type=GraphType.ADJACENCY_MATRIX))
        result_matrix = CyclomaticComplexity(Log()).evaluate(graph_matrix)
        expected_result_matrix = 0 - 0 + 2  # edges - nodes + 2
        self.assertEqual(result_matrix, expected_result_matrix)


if __name__ == '__main__':
    unittest.main()
