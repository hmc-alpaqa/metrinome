"""This module tests that we can compute cyclomatic complexity for any Graph."""

import unittest
from typing import List

import numpy as np  # type: ignore

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph as CFG
from graph.graph import AdjListGraph, AdjListType, EdgeListGraph
from metric.cyclomatic_complexity import CyclomaticComplexity


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
        vertices = 5
        graph = CFG(EdgeListGraph(edges, vertices))
        result = CyclomaticComplexity(Log()).evaluate(graph)
        expected_result = 3 - 5 + 2  # edges - nodes + 2
        self.assertEqual(result, expected_result)

        adjacencies: AdjListType = [[1], [2], [], [4], []]
        graph = CFG(AdjListGraph(adjacencies, vertices))
        result = CyclomaticComplexity(Log()).evaluate(graph)
        self.assertEqual(result, expected_result)

        edges = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])
        graph = CFG(AdjListGraph(edges, vertices))
        result = CyclomaticComplexity(Log()).evaluate(graph)
        self.assertEqual(result, result)

    def test_cyclomatic_complexity_no_edges(self) -> None:
        """
        Verify cyclomatic complexity value for graph with no edges.

        Compute the cyclomatic complexity for a graph with a non-zero number of vertices
        (where the start node is not the same as the end node) and zero number of edges.
        """
        edges: List[List[int]] = []
        vertices = 2

        # graph type is edge_list.
        graph_edge = CFG(AdjListGraph(edges, vertices))
        result_edge = CyclomaticComplexity(Log()).evaluate(graph_edge)
        expected_result_edge = 0 - 2 + 2  # edges - nodes + 2
        self.assertEqual(result_edge, expected_result_edge)

        # graph type is list.
        graph_list = CFG(AdjListGraph(edges, vertices))
        result_list = CyclomaticComplexity(Log()).evaluate(graph_list)
        expected_result_list = 0 - 2 + 2  # edges - nodes + 2
        self.assertEqual(result_list, expected_result_list)

        # graph type is matrix.
        graph_matrix = CFG(AdjListGraph(np.zeros((0, 0), dtype=np.int8), vertices))
        result_matrix = CyclomaticComplexity(Log()).evaluate(graph_matrix)
        expected_result_matrix = 0 - 2 + 2  # edges - nodes + 2
        self.assertEqual(result_matrix, expected_result_matrix)


if __name__ == '__main__':
    unittest.main()
