"""Test methods associated with Graph objects and their conversion to Prism files."""

import unittest
import sys
import tempfile
import re
import numpy as np  # type: ignore
sys.path.append("/app/code/")
from graph import Graph, GraphType


class TestGraphGetters(unittest.TestCase):
    """Test Graph getter methods."""

    # === Graph::node_to_index ===
    def test_node_to_index(self) -> None:
        """Test the node_to_index helper function."""
        graph = Graph([], [1], 0, 5, GraphType.EDGE_LIST)
        self.assertTrue(graph.node_to_index(0) == 0)
        self.assertTrue(graph.node_to_index(5) == 1)
        self.assertTrue(graph.node_to_index(1) == 2)

    # === Graph::get_end ===
    def test_get_end_one_vertex(self) -> None:
        """Check that we can get the end vertex of a Graph with one vertex."""
        graph = Graph([], [1], 0, 1, GraphType.EDGE_LIST)
        end_node = graph.get_end()
        expected = 1
        self.assertEqual(expected, end_node)

    def test_get_end_multiple_vertex(self) -> None:
        """Check that we can get the end vertex of a Graph with multiple vertices."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        end_node = graph.get_end()
        expected = 4
        self.assertEqual(expected, end_node)

    # === Graph::get_start ===
    def test_get_start_one_vertex(self) -> None:
        """Check that we can get the start vertex of a Graph with one vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        start_node = graph.get_start()
        expected = 1
        self.assertEqual(expected, start_node)

    def test_get_start_multiple_vertex(self) -> None:
        """Check that we can get the start vertex of a Graph with multiple vertices."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        start_node = graph.get_start()
        expected = 1
        self.assertEqual(expected, start_node)

    # === Graph::set_name ===
    def test_set_name(self) -> None:
        """Check that can set the name of a Graph."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        graph.set_name("Test graph")
        self.assertEqual(graph.name, "Test graph")

    # === Graph::get_vertices ===
    def test_get_vertices_one_vertex(self) -> None:
        """Test if we can get all of the vertices from a Graph with a single vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        vertices = graph.get_vertices()
        self.assertEqual(vertices, [1])

    def test_vertices_many_vertices(self) -> None:
        """Test if we can get all of the vertices from a Graph with a many vertices."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        vertices = graph.get_vertices()
        self.assertEqual(vertices, [1, 2, 3, 4])

    def test_get_parents(self) -> None:
        """Check that we can get the parents of a graph in adjacency list format."""
        graph = Graph([[0, 1], [1, 2], [1, 3]], [0, 1, 2, 3], 0, 3, GraphType.EDGE_LIST)
        adj_list = graph.adjacency_list()
        graph = Graph(adj_list, [0, 1, 2, 3], 0, 3, GraphType.ADJACENCY_LIST)
        res = graph.get_parents()
        self.assertTrue(0 not in res)
        self.assertTrue(res[1] == [0])
        self.assertTrue(res[2] == [1])
        self.assertTrue(res[3] == [1])

    def test_get_parents_edge_list(self) -> None:
        """Check that we can get an error if we try to get parents of edge list."""
        graph = Graph([[0, 1], [1, 2], [1, 3]], [0, 1, 2, 3], 0, 3, GraphType.EDGE_LIST)
        with self.assertRaises(NotImplementedError):
            graph.get_parents()


class TestGraphInfo(unittest.TestCase):
    """Test Graph methods that count vertices / edges."""

    # === Graph::edge_count ===
    def test_edge_count_no_edges(self) -> None:
        """Check that we can get the number of edges for a Graph with no edges."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        count = graph.edge_count()
        expected = 0
        self.assertEqual(expected, count)

    def test_edge_count_one_edge(self) -> None:
        """Check that we can get the number of edges for a Graph with one edge."""
        graph = Graph([[1, 2]], [1, 2], 1, 2, GraphType.EDGE_LIST)
        count = graph.edge_count()
        expected = 1
        self.assertEqual(expected, count)

    def test_edge_count_multiple_edge(self) -> None:
        """Check that we can get the number of edges for a Graph with multiple edges."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        count = graph.edge_count()
        expected = 3
        self.assertEqual(expected, count)

    # === Graph::vertex_count ===
    def test_vertex_count_one_vertex(self) -> None:
        """Test obtaining the number of vertices from a Graph for a Graph with a single vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        vertex_count = graph.vertex_count()
        self.assertEqual(vertex_count, 1)

    def test_vertex_count_many_vertices(self) -> None:
        """Test obtaining the number of vertices from a Graph for a multiple-vertex Graph."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        vertex_count = graph.vertex_count()
        self.assertEqual(vertex_count, 4)


class TestGraph(unittest.TestCase):
    """Test Graph objects."""

    # === Graph::dot ===
    def test_dot(self) -> None:
        """Check that we can generate a dot file for a Graph."""
        graph = Graph([[0, 1], [1, 2], [1, 3], [3, 4], [3, 5],
                       [2, 7], [4, 6], [5, 6], [6, 7]],
                      [0, 1, 2, 3, 4, 5, 6, 7], 0, 7, GraphType.EDGE_LIST)
        dot = graph.dot()
        with open("/app/code/tests/dotFiles/dotTest.dot", "w+") as file:
            file.write(dot)
        frmfile = graph.from_file("/app/code/tests/dotFiles/dotTest.dot",
                                  graph_type=GraphType.EDGE_LIST)
        self.assertEqual(frmfile, graph)

    # === Graph::update_with_node ===
    def test_update_with_node(self) -> None:
        """Check that we can add a node to a Graph."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        update = re.search(r"([0-9]*)\s*\[label=\"(.*)\"\]", "2 [label=\"EXIT\"]")
        graph.update_with_node(update)
        expected = Graph([], [1, 2], 1, 2, GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)

    # === Graph::update_with_edge ===
    def test_update_with_edge(self) -> None:
        """Check that we can add an edge to a Graph."""
        graph = Graph([], [1, 2], 1, 2, GraphType.EDGE_LIST)
        update = re.search(r"([0-9]*)\s*->\s*([0-9]*)", "1 -> 2")
        graph.update_with_edge(update)
        expected = Graph([[1, 2]], [1, 2], 1, 2, GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)

    # === Graph::__eq__ ===
    def test_eq_same_simple(self) -> None:
        """Verify that equality works."""
        graph1 = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        graph2 = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        self.assertTrue(graph1 == graph2)

    def test_eq_same_complicated(self) -> None:
        """Check that equality works for more complicated Graphs."""
        graph1 = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        graph2 = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        self.assertTrue(graph1 == graph2)

    def test_eq_different(self) -> None:
        """Check that equality fails when the Graphs are different."""
        graph1 = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        graph2 = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        self.assertFalse(graph1 == graph2)

    def test_eq_different_types(self) -> None:
        """Check that equality throws an error when Graphs are different types."""
        graph1 = Graph([], [0], 0, 0, GraphType.EDGE_LIST)
        graph2 = Graph([], [0], 0, 0, GraphType.ADJACENCY_LIST)
        with self.assertRaises(ValueError):
            graph1 == graph2  # pylint: disable=pointless-statement

    # === Graph::__str__ ===
    def test_to_str(self) -> None:
        """Test if we can correctly convert a Graph to a string."""
        graph = Graph([1, 2], [1, 2, 3], 1, 3, graph_type=GraphType.EDGE_LIST)
        expected = "Edges: [1, 2]\nTotal Edges: 2\nVertices: [1, 2, 3]\nStart Node: 1\nEnd Node: 3"
        self.assertEqual(expected, str(graph))

    # # === Graph::edge_rules ===
    def test_edge_rules_no_edges(self) -> None:
        """Test if we can get all of the edges from a Graph."""
        graph = Graph([], [1, 2, 3], 1, 3, GraphType.EDGE_LIST)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [])

    def test_edge_rules_with_edges(self) -> None:
        """Test if we can get all of the edges from a Graph."""
        graph = Graph([[0, 1], [0, 2]], [0, 1, 2], 0, 2, GraphType.EDGE_LIST)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [[0, 1], [0, 2]])

        adjacency_matrix = graph.adjacency_matrix()
        graph = Graph(adjacency_matrix, [0, 1, 2], 0, 2, GraphType.ADJACENCY_MATRIX)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [(0, 1), (0, 2)])

        graph = Graph([[1, 2]], [0, 1, 2], 0, 2, GraphType.ADJACENCY_LIST)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [(0, 1), (0, 2)])

    # # === Graph::adjacency_matrix ===
    def test_adjacency_matrix_no_edges(self) -> None:
        """Test if we can get the adjacency matrix for a Graph with no edges."""
        graph = Graph([], [1, 2, 3], 1, 3, GraphType.EDGE_LIST)
        adj_mat = graph.adjacency_matrix()
        empty_mat = np.zeros((3, 3))
        self.assertTrue((adj_mat == empty_mat).all())

    def test_adjacency_matrix_normal_graph(self) -> None:
        """Test if we can get the adjacency matrix for a Graph with many edges and vertices."""
        graph = Graph([[0, 1], [1, 2], [1, 3]], [0, 1, 2, 3], 0, 3, GraphType.EDGE_LIST)
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

    # # === Graph::adjacency_list ===
    def test_adjacency_list_no_edges(self) -> None:
        """Test if we can get the adjacency list for a graph with no edges."""
        graph = Graph([], [0, 1, 2], 0, 2, GraphType.EDGE_LIST)
        adj_list = graph.adjacency_list()
        for i in adj_list:
            self.assertTrue(len(i) == 0)

    # # === Graph::from_file ===
    def test_from_file_one_vertex(self) -> None:
        """Test if we can get the adjacency list for a graph with no edges."""
        expected = Graph([], [0, 1], 0, 1, GraphType.EDGE_LIST)
        graph = Graph.from_file("/app/code/tests/dotFiles/testsimple.dot",
                                graph_type=GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)
        # Graph.fromFile(None)

    def test_from_file_normal_graph(self) -> None:
        """Test if we can get the adjacency list for a graph with many edges and vertices."""
        expected = Graph([[0, 1], [1, 2], [1, 3], [3, 4], [3, 5],
                          [2, 7], [4, 6], [5, 6], [6, 7]],
                         [0, 1, 2, 3, 4, 5, 6, 7], 0, 7, GraphType.EDGE_LIST)
        graph = Graph.from_file("/app/code/tests/dotFiles/testgraph.dot",
                                graph_type=GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)

    # === Graph::convert_to_weighted ===
    def test_convert_weighted_to_weighted(self) -> None:
        """Check that converting a graph that is already weighted to weighted throws an error."""
        graph = Graph([], [0], start_node=0, end_node=1, graph_type=GraphType.ADJACENCY_LIST)
        graph.convert_to_weighted()
        with self.assertRaises(ValueError):
            graph.convert_to_weighted()

        graph = Graph([], [0], start_node=0, end_node=1, graph_type=GraphType.ADJACENCY_MATRIX)
        with self.assertRaises(NotImplementedError):
            graph.convert_to_weighted()
            

    def test_convert_unweighted_to_weighted(self) -> None:
        """Check that converting a an unweighted graph to weighted sets weights to 1."""
        graph = Graph([[1, 2], [2]], [0, 1, 2], start_node=0, end_node=1,
                      graph_type=GraphType.ADJACENCY_LIST)
        graph.convert_to_weighted()
        self.assertEqual(graph.edges, [[[1, 1], [2, 1]], [[2, 1]]])
        self.assertEqual(graph.vertices, [0, 1, 2])
        self.assertEqual(graph.start_node, 0)

    # === Graph::to_prism ===
    def test_to_prism_one_vertex(self) -> None:
        """Test if we can convert a Graph with one vertex to a PRISM file."""
        graph = Graph([], [0], start_node=0, end_node=1, graph_type=GraphType.ADJACENCY_LIST)
        with self.assertRaises(ValueError):
            graph.to_prism()  # Cannot convert non-weighted.

        graph.convert_to_weighted()
        with tempfile.NamedTemporaryFile() as file:
            to_write = ''.join(graph.to_prism())
            file.write(str.encode(to_write))

    def test_to_prism_normal_graph(self) -> None:
        """Test if we can convert a Graph with many vertices and many edges to a PRISM file."""
        graph = Graph([], [0], start_node=0, end_node=1, graph_type=GraphType.ADJACENCY_LIST)
        graph.convert_to_weighted()
        with tempfile.NamedTemporaryFile() as file:
            to_write = ''.join(graph.to_prism())
            file.write(str.encode(to_write))


if __name__ == '__main__':
    unittest.main()
