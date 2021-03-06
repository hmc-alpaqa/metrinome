"""Test methods associated with Graph objects and their conversion to Prism files."""

import re
import tempfile
import unittest
from typing import cast

import numpy as np  # type: ignore

from graph.control_flow_graph import ControlFlowGraph as CFG
from graph.graph import AdjListGraph, AdjListType, AdjMatGraph, EdgeListGraph, EdgeListType, Graph

# pylint: disable=no-member


class TestGraphGetters(unittest.TestCase):
    """Test Graph getter methods."""

    # === Graph::node_to_index ===
    def test_node_to_index(self) -> None:
        """Test the node_to_index helper function."""
        graph = EdgeListGraph(cast(EdgeListType, []), 6)
        self.assertTrue(graph.node_to_index(0) == 0)
        self.assertTrue(graph.node_to_index(5) == 1)
        self.assertTrue(graph.node_to_index(1) == 2)

    # === Graph::get_end ===
    def test_get_end_one_vertex(self) -> None:
        """Check that we can get the end vertex of a Graph with one vertex."""
        graph = EdgeListGraph(cast(EdgeListType, []), 2)
        expected = 1
        self.assertEqual(expected, graph.end_node)

    def test_get_end_multiple_vertex(self) -> None:
        """Check that we can get the end vertex of a Graph with multiple vertices."""
        graph = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        expected = 3
        self.assertEqual(expected, graph.end_node)

    # === Graph::get_start ===
    def test_get_start_one_vertex(self) -> None:
        """Check that we can get the start vertex of a Graph with one vertex."""
        graph = EdgeListGraph(cast(EdgeListType, []), 1)
        expected = 0
        self.assertEqual(expected, graph.start_node)

    def test_get_start_multiple_vertex(self) -> None:
        """Check that we can get the start vertex of a Graph with multiple vertices."""
        graph = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        expected = 0
        self.assertEqual(expected, graph.start_node)

    # === Graph::get_vertices ===
    def test_vertices_one_vertex(self) -> None:
        """Test if we can get all of the vertices from a Graph with a single vertex."""
        graph = EdgeListGraph(cast(EdgeListType, []), 1)
        vertices = graph.vertices()
        self.assertEqual(vertices, [0])

    def test_vertices_many_vertices(self) -> None:
        """Test if we can get all of the vertices from a Graph with a many vertices."""
        graph = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        vertices = graph.vertices()
        self.assertEqual(vertices, [0, 1, 2, 3])

    def test_get_parents(self) -> None:
        """Check that we can get the parents of a graph in adjacency list format."""
        graph = EdgeListGraph([[0, 1], [1, 2], [1, 3]], 4)
        adj_list = graph.adjacency_list()
        graph_two = AdjListGraph(adj_list, 4)
        res = graph_two.get_parents()
        self.assertTrue(0 not in res)
        self.assertTrue(res[1] == [0])
        self.assertTrue(res[2] == [1])
        self.assertTrue(res[3] == [1])


class TestGraphInfo(unittest.TestCase):
    """Test Graph methods that count vertices / edges."""

    # === Graph::edge_count ===
    def test_edge_count_no_edges(self) -> None:
        """Check that we can get the number of edges for a Graph with no edges."""
        graph = EdgeListGraph(cast(EdgeListType, []), 1)
        count = graph.edge_count()
        expected = 0
        self.assertEqual(expected, count)

    def test_edge_count_one_edge(self) -> None:
        """Check that we can get the number of edges for a Graph with one edge."""
        graph = EdgeListGraph([[1, 2]], 2)
        count = graph.edge_count()
        expected = 1
        self.assertEqual(expected, count)

    def test_edge_count_multiple_edge(self) -> None:
        """Check that we can get the number of edges for a Graph with multiple edges."""
        graph = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        count = graph.edge_count()
        expected = 3
        self.assertEqual(expected, count)


class TestGraph(unittest.TestCase):
    """Test Graph objects."""

    # === Graph::dot ===
    def test_dot(self) -> None:
        """Check that we can generate a dot file for a Graph."""
        graph = EdgeListGraph([[0, 1], [1, 2], [1, 3], [3, 4], [3, 5],
                               [2, 7], [4, 6], [5, 6], [6, 7]], 8)
        dot = graph.dot()
        with open("/app/code/tests/dotFiles/dotTest.dot", "w+") as file:
            file.write(dot)
        frmfile = CFG.from_file("/app/code/tests/dotFiles/dotTest.dot",
                                graph_type=EdgeListGraph)
        self.assertEqual(frmfile.graph, graph)

    # === Graph::update_with_node ===
    def test_update_with_node(self) -> None:
        """Check that we can add a node to a Graph."""
        graph = EdgeListGraph(cast(EdgeListType, []), 1)
        update = re.search(r"([0-9]*)\s*\[label=\"(.*)\"\]", "1 [label=\"EXIT\"]")
        if update is None:
            self.fail("Node cannot be None.")

        graph.update_with_node(update, True)
        expected = EdgeListGraph(cast(EdgeListType, []), 2)
        self.assertEqual(expected, graph)

    # === Graph::update_with_edge ===
    def test_update_with_edge(self) -> None:
        """Check that we can add an edge to a Graph."""
        graph = EdgeListGraph(cast(EdgeListType, []), 2)
        update = re.search(r"([0-9]*)\s*->\s*([0-9]*)", "0 -> 1")
        if update is None:
            self.fail("Node cannot be None.")

        graph.update_with_edge(update)
        expected = EdgeListGraph([[0, 1]], 2)
        self.assertEqual(expected, graph)

    # === Graph::__eq__ ===
    def test_eq_same_simple(self) -> None:
        """Verify that equality works."""
        graph1 = EdgeListGraph(cast(EdgeListType, []), 1)
        graph2 = EdgeListGraph(cast(EdgeListType, []), 1)
        self.assertTrue(graph1 == graph2)

    def test_eq_same_complicated(self) -> None:
        """Check that equality works for more complicated Graphs."""
        graph1 = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        graph2 = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        self.assertTrue(graph1 == graph2)

    def test_eq_different(self) -> None:
        """Check that equality fails when the Graphs are different."""
        graph1 = EdgeListGraph(cast(EdgeListType, []), 1)
        graph2 = EdgeListGraph([[1, 2], [2, 3], [2, 4]], 4)
        self.assertFalse(graph1 == graph2)

    def test_eq_different_types(self) -> None:
        """Check that equality throws an error when Graphs are different types."""
        graph1 = EdgeListGraph(cast(EdgeListType, []), 1)
        graph2 = AdjListGraph(cast(AdjListType, []), 1)
        self.assertNotEqual(graph1, graph2)

        other = "foo"
        self.assertNotEqual(graph1, other)

    # === Graph::__str__ ===
    def test_to_str(self) -> None:
        """Test if we can correctly convert a Graph to a string."""
        graph = EdgeListGraph([[1, 2]], 3)
        edge_str = "Edges: [[1, 2]]"
        expected = f"{edge_str}\nTotal Edges: 1\nVertices: [0, 1, 2]\nStart Node: 0\nEnd Node: 2"
        self.assertEqual(expected, str(graph))

    # # === Graph::edge_rules ===
    def test_edge_rules_no_edges(self) -> None:
        """Test if we can get all of the edges from a Graph."""
        graph = EdgeListGraph(cast(EdgeListType, []), 3)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [])

    def test_edge_rules_with_edges(self) -> None:
        """Test if we can get all of the edges from a Graph."""
        graph: Graph
        graph = EdgeListGraph([[0, 1], [0, 2]], 3)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [[0, 1], [0, 2]])

        adjacency_matrix = graph.adjacency_matrix()
        graph = AdjMatGraph(adjacency_matrix, 3)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [[0, 1], [0, 2]])

        graph = AdjListGraph([[1, 2]], 3)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [[0, 1], [0, 2]])

    # # === Graph::adjacency_matrix ===
    def test_adjacency_matrix_no_edges(self) -> None:
        """Test if we can get the adjacency matrix for a Graph with no edges."""
        graph = EdgeListGraph(cast(EdgeListType, []), 3)
        adj_mat = graph.adjacency_matrix()
        empty_mat = np.zeros((3, 3))
        self.assertTrue((adj_mat == empty_mat).all())

    def test_adjacency_matrix_normal_graph(self) -> None:
        """Test if we can get the adjacency matrix for a Graph with many edges and vertices."""
        graph = EdgeListGraph([[0, 1], [1, 2], [1, 3]], 4)
        adj_mat = graph.adjacency_matrix()
        expected_mat = [[0, 0, 1, 0],
                        [0, 0, 0, 0],
                        [0, 1, 0, 1],
                        [0, 0, 0, 0]]
        self.assertTrue((adj_mat == expected_mat).all())

    def test_adjacency_matrix_weighted_graph(self) -> None:
        """Check that we can obtain the adjacency matrix for a weighted Graph."""
        # graph = Graph([[1], [2, 3], []], [0, 1, 2, 3], 0, 3, GraphType.ADJACENCY_LIST)
        # adj_mat = graph.adjacency_matrix()
        # expected_mat = [[0, 0, 1, 0],
        #                 [0, 0, 0, 0],
        #                 [0, 1, 0, 1],
        #                 [0, 0, 0, 0]]
        # self.assertTrue((adj_mat == expected_mat).all())

    # === Graph::adjacency_list ===
    def test_adjacency_list_no_edges(self) -> None:
        """Test if we can get the adjacency list for a graph with no edges."""
        graph = EdgeListGraph(cast(EdgeListType, []), 3)
        adj_list = graph.adjacency_list()
        for i in adj_list:
            self.assertTrue(len(i) == 0)

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
        expected = EdgeListGraph([[0, 1], [1, 2], [1, 3], [3, 4], [3, 5],
                                  [2, 7], [4, 6], [5, 6], [6, 7]], 8)
        cfg = CFG.from_file("/app/code/tests/dotFiles/testgraph.dot",
                            graph_type=EdgeListGraph)
        self.assertEqual(expected, cfg.graph)

    # === Graph::convert_to_weighted ===
    def test_convert_weighted_to_weighted(self) -> None:
        """Check that converting a graph that is already weighted to weighted throws an error."""
        graph = AdjListGraph(cast(AdjListType, [[], []]), num_vertices=2)
        graph.convert_to_weighted()
        with self.assertRaises(ValueError):
            graph.convert_to_weighted()

    def test_convert_unweighted_to_weighted(self) -> None:
        """Check that converting a an unweighted graph to weighted sets weights to 1."""
        graph = AdjListGraph(cast(AdjListType, [[1, 2], [2], []]), 3)
        graph.convert_to_weighted()
        self.assertEqual(graph.edges, [[1, 2], [2], []])
        self.assertEqual(graph.num_vertices, 3)
        self.assertEqual(graph.start_node, 0)

    # === Graph::to_prism ===
    def test_to_prism_one_vertex(self) -> None:
        """Test if we can convert a Graph with one vertex to a PRISM file."""
        graph = AdjListGraph(cast(EdgeListType, [[]]), 1)
        with self.assertRaises(ValueError):
            graph.to_prism()  # Cannot convert non-weighted.

        graph.convert_to_weighted()
        with tempfile.NamedTemporaryFile() as file:
            to_write = ''.join(graph.to_prism())
            file.write(str.encode(to_write))


if __name__ == '__main__':
    unittest.main()
