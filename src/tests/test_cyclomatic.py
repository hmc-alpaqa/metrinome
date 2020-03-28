"""This module tests that we can compute cyclomatic complexity for any Graph."""

import unittest
import sys
sys.path.append("/app/code/")
from graph import Graph
from metric.cyclomatic_complexity import CyclomaticComplexity


class TestCyclomaticComplexity(unittest.TestCase):
    """Tests for the object that computes Cyclomatic Complexity for an arbitrary Graph."""

    def test_cyclomatic_complexity(self):
        """
        Verify cyclomatic complexity value for regular graph.

        Compute the cyclomatic complexity for a graph with a
        non-zero number of vertices (where the start node is
        not the same as the end node) and non-zero number of
        edges.
        """
        edges = [[0, 1], [1, 2], [3, 4]]
        vertices = set([0, 1, 2, 3, 4])
        start_node = 0
        end_node = 4
        graph = Graph(edges, vertices, start_node, end_node)
        result = CyclomaticComplexity().evaluate(graph)
        expected_result = 3 - 5 + 2  # edges - nodes + 2
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
