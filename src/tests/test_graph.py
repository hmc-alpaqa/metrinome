"""Test methods associated with Graph objects and their conversion to Prism files."""

import unittest
import sys
import re
import numpy as np  # type: ignore
sys.path.append("/app/code/")
from graph import Graph, GraphType


class TestGraphGetters(unittest.TestCase):
    """Test Graph getter methods."""

    # === Graph::node_to_index ===
    def test_node_to_index(self):
        """Test the node_to_index helper function."""

    # === Graph::get_end ===
    def test_get_end_one_vertex(self):
        """Check that we can get the end vertex of a Graph with one vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        end_node = graph.get_end()
        expected = 1
        self.assertEqual(expected, end_node)

    def test_get_end_multiple_vertex(self):
        """Check that we can get the end vertex of a Graph with multiple vertices."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        end_node = graph.get_end()
        expected = 4
        self.assertEqual(expected, end_node)

    # === Graph::get_start ===
    def test_get_start_one_vertex(self):
        """Check that we can get the start vertex of a Graph with one vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        start_node = graph.get_start()
        expected = 1
        self.assertEqual(expected, start_node)

    def test_get_start_multiple_vertex(self):
        """Check that we can get the start vertex of a Graph with multiple vertices."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        start_node = graph.get_start()
        expected = 1
        self.assertEqual(expected, start_node)

    # === Graph::set_name ===
    def test_set_name(self):
        """Check that can set the name of a Graph."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        graph.set_name("Test graph")
        self.assertEqual(graph.name, "Test graph")

    # # === Graph::get_vertices ===
    def test_get_vertices_one_vertex(self):
        """Test if we can get all of the vertices from a Graph with a single vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        vertices = graph.get_vertices()
        self.assertEqual(vertices, [1])

    def test_vertices_many_vertices(self):
        """Test if we can get all of the vertices from a Graph with a many vertices."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        vertices = graph.get_vertices()
        self.assertEqual(vertices, [1, 2, 3, 4])


class TestGraph(unittest.TestCase):
    """Test Graph objects."""

    # === Graph::edge_count ===
    def test_edge_count_no_edges(self):
        """Check that we can get the number of edges for a Graph with no edges."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        count = graph.edge_count()
        expected = 0
        self.assertEqual(expected, count)

    def test_edge_count_one_edge(self):
        """Check that we can get the number of edges for a Graph with one edge."""
        graph = Graph([[1, 2]], [1, 2], 1, 2, GraphType.EDGE_LIST)
        count = graph.edge_count()
        expected = 1
        self.assertEqual(expected, count)

    def test_edge_count_multiple_edge(self):
        """Check that we can get the number of edges for a Graph with multiple edges."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        count = graph.edge_count()
        expected = 3
        self.assertEqual(expected, count)

    # === Graph::dot ===
    def test_dot(self):
        """Check that we can generate a dot file for a Graph."""
        graph = Graph([[0, 1], [1, 2], [1, 3], [3, 4], [3, 5],
                       [2, 7], [4, 6], [5, 6], [6, 7]],
                      [0, 1, 2, 3, 4, 5, 6, 7], 0, 7, GraphType.EDGE_LIST)
        dot = graph.dot()
        with open("dotFiles/dotTest.dot", "w+") as file:
            file.write(dot)
        frmfile = graph.from_file("dotFiles/dotTest.dot", graph_type=GraphType.EDGE_LIST)
        self.assertEqual(frmfile, graph)

    # === Graph::update_with_node ===
    def test_update_with_node(self):
        """Check that we can add a node to a Graph."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        update = re.search(r"([0-9]*)\s*\[label=\"(.*)\"\]", "2 [label=\"EXIT\"]")
        graph.update_with_node(update)
        expected = Graph([], [1, 2], 1, 2, GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)

    # === Graph::update_with_edge ===
    def test_update_with_edge(self):
        """Check that we can add an edge to a Graph."""
        graph = Graph([], [1, 2], 1, 2, GraphType.EDGE_LIST)
        update = re.search(r"([0-9]*)\s*->\s*([0-9]*)", "1 -> 2")
        graph.update_with_edge(update)
        expected = Graph([[1, 2]], [1, 2], 1, 2, GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)

    # === Graph::__eq__ ===
    def test_eq_same_simple(self):
        """Verify that equality works."""
        graph1 = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        graph2 = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        self.assertTrue(graph1 == graph2)

    def test_eq_same_complicated(self):
        """Check that equality works for more complicated Graphs."""
        graph1 = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        graph2 = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        self.assertTrue(graph1 == graph2)

    def test_eq_different(self):
        """Check that equality fails when the Graphs are different."""
        graph1 = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        graph2 = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        self.assertFalse(graph1 == graph2)

    # === Graph::__str__ ===
    def test_to_str(self):
        """Test if we can correctly convert a Graph to a string."""
        graph = Graph([1, 2], [1, 2, 3], 1, 3, graph_type=GraphType.EDGE_LIST)
        expected = "Edges: [1, 2]\nVertices: [1, 2, 3]\nStart Node: 1\nEnd Node: 3"
        self.assertEqual(expected, str(graph))

    # # === Graph::edge_rules ===
    def test_edge_rules_no_edges(self):
        """Test if we can get all of the edges from a Graph."""
        graph = Graph([], [1, 2, 3], 1, 3, GraphType.EDGE_LIST)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [])

    # === Graph::vertex_count ===
    def test_vertex_count_one_vertex(self):
        """Test obtaining the number of vertices from a Graph for a Graph with a single vertex."""
        graph = Graph([], [1], 1, 1, GraphType.EDGE_LIST)
        vertex_count = graph.vertex_count()
        self.assertEqual(vertex_count, 1)

    def test_vertex_count_many_vertices(self):
        """Test obtaining the number of vertices from a Graph for a multiple-vertex Graph."""
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4, GraphType.EDGE_LIST)
        vertex_count = graph.vertex_count()
        self.assertEqual(vertex_count, 4)

    # # === Graph::adjacency_matrix ===
    def test_adjacency_matrix_no_edges(self):
        """Test if we can get the adjacency matrix for a Graph with no edges."""
        graph = Graph([], [1, 2, 3], 1, 3, GraphType.EDGE_LIST)
        adj_mat = graph.adjacency_matrix()
        empty_mat = np.zeros((3, 3))
        self.assertTrue((adj_mat == empty_mat).all())

    def test_adjacency_matrix_normal_graph(self):
        """Test if we can get the adjacency matrix for a Graph with many edges and vertices."""
        graph = Graph([[0, 1], [1, 2], [1, 3]], [0, 1, 2, 3], 0, 3, GraphType.EDGE_LIST)
        adj_mat = graph.adjacency_matrix()
        expected_mat = [[0, 0, 1, 0],
                        [0, 0, 0, 0],
                        [0, 1, 0, 1],
                        [0, 0, 0, 0]]
        self.assertTrue((adj_mat == expected_mat).all())

    # # === Graph::adjacency_list ===
    def test_adjacency_list_no_edges(self):
        """Test if we can get the adjacency list for a graph with no edges."""
        graph = Graph([], [0, 1, 2], 0, 2, GraphType.EDGE_LIST)
        adj_list = graph.adjacency_list()
        for i in adj_list:
            self.assertTrue(len(i) == 0)

    # # === Graph::from_file ===
    def test_from_file_one_vertex(self):
        """Test if we can get the adjacency list for a graph with no edges."""
        expected = Graph([], [0, 1], 0, 1, GraphType.EDGE_LIST)
        graph = Graph.from_file("dotFiles/testsimple.dot", graph_type=GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)
        # Graph.fromFile(None)

    def test_from_file_normal_graph(self):
        """Test if we can get the adjacency list for a graph with many edges and vertices."""
        expected = Graph([[0, 1], [1, 2], [1, 3], [3, 4], [3, 5],
                          [2, 7], [4, 6], [5, 6], [6, 7]],
                         [0, 1, 2, 3, 4, 5, 6, 7], 0, 7, GraphType.EDGE_LIST)
        graph = Graph.from_file("dotFiles/testgraph.dot", graph_type=GraphType.EDGE_LIST)
        self.assertEqual(expected, graph)
    #     # Graph.fromFile(None)

    # # === Graph::to_prism ===
    def test_to_prism_one_vertex(self):
        """Test if we can convert a Graph with one vertex to a PRISM file."""

    def test_to_prism_normal_graph(self):
        """Test if we can convert a Graph with many vertices and many edges to a PRISM file."""


if __name__ == '__main__':
    unittest.main()
