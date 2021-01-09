"""All of the tests for the path complexity and APC computer."""

import unittest

import metric.path_complexity as pc
from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from tests.unit_utils import get_test_graph

# pylint: disable=no-value-for-parameter


class TestPathComplexity(unittest.TestCase):
    """Test PathComplexity object."""

    def setUp(self) -> None:
        """Initialize a logger before running each test."""
        self.logger = Log()

    def test_pathcomplexity(self) -> None:
        """Compute path complexity for a regular .dot file."""
        converter = pc.PathComplexity(self.logger)
        self.assertEqual("Path Complexity", converter.name())
        cfg = ControlFlowGraph(get_test_graph())
        apc, path_complexity = converter.evaluate(cfg)
        self.assertEqual(apc, 3)
        self.assertEqual(path_complexity, 3)

    def test_basecase_bfs(self) -> None:
        """Verify that BaseCaseBFS obtains initial pc values."""
        base_case_getter = pc.BaseCaseBFS(self.logger)
        graph = get_test_graph()
        start_idx, num_coeffs = 2, 5
        x_mat = None
        denominator = None
        base_case_getter.get(graph, x_mat, denominator, start_idx, num_coeffs)

    def test_basecase_taylor(self) -> None:
        """Verify that BaseCaseTaylor obtains initial pc values."""
        # base_case_getter = pc.BaseCaseTaylor(self.logger)


if __name__ == '__main__':
    unittest.main()
