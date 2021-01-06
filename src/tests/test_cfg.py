"""Test methods associated with ControlFlowGraph objects."""

import unittest
from typing import cast

from graph.control_flow_graph import ControlFlowGraph as CFG
from graph.control_flow_graph import Metadata
from graph.graph import EdgeListGraph, EdgeListType
from tests.unit_utils import get_second_test_graph, get_test_graph


class TestMetadata(unittest.TestCase):
    """Test the Metadata object."""

    def test_str_regular_md(self) -> None:
        """Test the string dunder method."""
        metadata = Metadata(Metadata.with_loc(5))
        self.assertTrue("5" in str(metadata))


class TestControlFlowGraph(unittest.TestCase):
    """Test the ControlFlowGraph object."""

    # === Graph::dot ===
    def test_dot(self) -> None:
        """Check that we can generate a dot file for a Graph."""
        graph = get_test_graph()
        dot = graph.dot()
        with open("/app/code/tests/dotFiles/dotTest.dot", "w+") as file:
            file.write(dot)
        frmfile = CFG.from_file("/app/code/tests/dotFiles/dotTest.dot",
                                graph_type=EdgeListGraph)
        self.assertEqual(frmfile.graph, graph)

    # === Graph::from_file ===
    def test_from_file_one_vertex(self) -> None:
        """Test if we can get the adjacency list for a graph with no edges."""
        expected = EdgeListGraph(cast(EdgeListType, []), 2)
        cfg = CFG.from_file("/app/code/tests/dotFiles/testsimple.dot",
                            graph_type=EdgeListGraph)
        self.assertEqual(expected, cfg.graph)
        # Graph.fromFile(None)

    def test_from_file_normal_graph(self) -> None:
        """Test if we can get the adjacency list for a graph with many edges and vertices."""
        expected = get_test_graph()
        cfg = CFG.from_file("/app/code/tests/dotFiles/testgraph.dot",
                            graph_type=EdgeListGraph)
        self.assertEqual(expected, cfg.graph)

    # === Graph::stitch ===
    def test_stitch_normal_graph(self) -> None:
        """Test if we can replace a node with another graph with many edges and vertices."""
        calls = {3: "callee"}
        caller = CFG(get_test_graph(), Metadata(Metadata.with_calls(calls)))
        callee = CFG(get_second_test_graph())
        expected = CFG(EdgeListGraph([[0, 1], [1, 2], [1, 3], [7, 8], [7, 9], [2, 11], [8, 10],
                                     [9, 10], [10, 11], [3, 4], [4, 5], [4, 6], [5, 7], [6, 7]],
                                     12))

        graphs = {"caller": caller, "callee": callee}

        self.assertEqual(CFG.stitch(graphs), expected)
        self.assertEqual(caller, CFG(get_test_graph(), Metadata(Metadata.with_calls(calls))))
        self.assertEqual(callee, CFG(get_second_test_graph()))

    # === Graph::compose ===
    def test_compose_normal(self) -> None:
        """Test if we can compose two graphs."""
        calls = {3: "callee"}
        caller = CFG(get_test_graph(), Metadata(Metadata.with_calls(calls)))
        callee = CFG(get_second_test_graph())
        edges = [[0, 1], [1, 2], [1, 3], [7, 8], [7, 9], [2, 11], [8, 10],
                 [9, 10], [10, 11], [3, 4], [4, 5], [4, 6], [5, 7], [6, 7]]
        expected = CFG(EdgeListGraph(edges, 12))
        res = CFG.compose(caller, callee, 3)

        self.assertEqual(res, expected)
        self.assertEqual(caller, CFG(get_test_graph(), Metadata(Metadata.with_calls(calls))))
        self.assertEqual(callee, CFG(get_second_test_graph()))


if __name__ == '__main__':
    unittest.main()
