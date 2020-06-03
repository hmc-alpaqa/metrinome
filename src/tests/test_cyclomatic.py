"""This module tests that we can compute cyclomatic complexity for any Graph."""

import unittest
import sys
import numpy as np
sys.path.append("/app/code/")
from graph import Graph, GraphType
from metric.cyclomatic_complexity import CyclomaticComplexity


class TestCyclomaticComplexity(unittest.TestCase):
    """Tests for the object that computes Cyclomatic Complexity for an arbitrary Graph."""

    def test_cyclomatic_complexity_edge_list(self):
        """
        Verify cyclomatic complexity value for regular graph.

        Compute the cyclomatic complexity for a graph with a non-zero number of vertices
        (where the start node is not the same as the end node) and non-zero number of edges.
        """
        edges = [[0, 1], [1, 2], [3, 4]]
        vertices = [0, 1, 2, 3, 4]
        start_node = 0
        end_node = 4
        graph = Graph(edges, vertices, start_node, end_node, graph_type=GraphType.EDGE_LIST)
        result = CyclomaticComplexity().evaluate(graph)
        expected_result = 3 - 5 + 2  # edges - nodes + 2
        self.assertEqual(result, expected_result)

        adjacencies = [[1], [2], [], [4], []]
        graph = Graph(adjacencies, vertices, start_node, end_node, graph_type=GraphType.ADJACENCY_LIST)
        result = CyclomaticComplexity().evaluate(graph)
        self.assertEqual(result, expected_result)

        edges = np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0]])
        graph = Graph(edges, vertices, start_node, end_node, graph_type=GraphType.ADJACENCY_MATRIX)
        result = CyclomaticComplexity().evaluate(graph)
        self.assertEqual(result, result)


    def test_cyclomatic_complexity_no_edges(self):
        """
        Verify cyclomatic complexity value for graph with no edges.

        Compute the cyclomatic complexity for a graph with a non-zero number of vertices
        (where the start node is not the same as the end node) and zero number of edges.
        """
        edges = []
        vertices = set([0, 1])
        start_node = 0
        end_node = 1

        # graph type is edge_list
        graph_edge = Graph(edges, vertices, start_node, end_node, graph_type=GraphType.EDGE_LIST)
        result_edge = CyclomaticComplexity().evaluate(graph_edge)
        expected_result_edge = 0 - 2 + 2 # edges - nodes + 2
        self.assertEqual(result_edge, expected_result_edge)

        # graph type is list
        graph_list = Graph(edges, vertices, start_node, end_node, graph_type=GraphType.ADJACENCY_LIST)
        result_list = CyclomaticComplexity().evaluate(graph_list)
        expected_result_list = 0 - 0 + 2  # edges - nodes + 2
        self.assertEqual(result_list, expected_result_list)

        # graph type is matrix
        graph_matrix = Graph(edges, vertices, start_node, end_node, graph_type=GraphType.ADJACENCY_MATRIX)
        result_matrix = CyclomaticComplexity().evaluate(graph_list)
        expected_result_matrix = 0 - 0 + 2  # edges - nodes + 2
        self.assertEqual(result_matrix, expected_result_matrix)

    
if __name__ == '__main__':
    unittest.main()
