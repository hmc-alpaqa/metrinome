"""
Test all of the methods associated with the construction of
Graph objects and their conversion to Prism files.
"""

import unittest
import sys
import numpy as np  # type: ignore
sys.path.append("/app/code/")
from graph import Graph


class TestGraph(unittest.TestCase):
    """
    Test Graph objects.
    """
    # === Graph::__str__ ===
    def test_to_str(self):
        """
        Test if we can correctly convert a Graph to a string.
        """
        graph = Graph([1, 2], [1, 2, 3], 1, 3)
        expected = "Edges: [1, 2]\nVertices: [1, 2, 3]\nStart Node: 1\nEnd Node: 3"
        self.assertEqual(expected, str(graph))

    # === Graph::edgeRules ===
    def test_edge_rules_no_edges(self):
        """
        Test if we can get all of the edges from a Graph.
        """
        graph = Graph([], [1, 2, 3], 1, 3)
        edge_list = graph.edge_rules()
        self.assertEqual(edge_list, [])

    # === Graph::vertex_count ===
    def test_vertex_count_one_vertex(self):
        """
        Test if we can obtain the number of vertices from a Graph
        for a Graph with a single vertex.
        """
        graph = Graph([], [1], 1, 1)
        vertex_count = graph.vertex_count()
        self.assertEqual(vertex_count, 1)

    def test_vertex_count_many_vertices(self):
        """
        Test if we can obtain the number of vertices from a Graph
        for a Graph with many vertices.
        """
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        vertex_count = graph.vertex_count()
        self.assertEqual(vertex_count, 4)

    # === Graph::get_vertices ===
    def test_get_vertices_one_vertex(self):
        """
        Test if we can get all of the vertices from a Graph with a
        single vertex.
        """
        graph = Graph([], [1], 1, 1)
        vertices = graph.get_vertices()
        self.assertEqual(vertices, [1])

    def test_vertices_many_vertices(self):
        """
        Test if we can get all of the vertices from a Graph with a
        many vertices.
        """
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        vertices = graph.get_vertices()
        self.assertEqual(vertices, [1, 2, 3, 4])

    # === Graph::adjacencyMatrix ===
    def test_adjacency_matrix_no_edges(self):
        """
        Test if we can get the adjacency matrix for a Graph
        with no edges.
        """
        graph = Graph([], [1, 2, 3], 1, 3)
        adj_mat = graph.adjacency_matrix()
        empty_arr = np.zeros((4, 4))
        self.assertTrue((adj_mat == empty_arr).all())

    def test_adjacency_matrix_normal_graph(self):
        """
        Test if we can get the adjacency matrix for a Graph
        with many edges and vertices.
        """
        graph = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        adj_mat = graph.adjacency_matrix()
        expected_mat = [[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 1, 0, 0, 1],
                        [0, 0, 0, 0, 0]]
        self.assertTrue((adj_mat == expected_mat).all())

    # === Graph::adjacencyList ===
    def test_adjacency_list_no_edges(self):
        """
        Test if we can get the adjacency list for a graph with
        no edges.
        """
        graph = Graph([], [1, 2, 3], 1, 3)
        adj_list = graph.adjacency_list()
        self.assertEqual(adj_list, [[], [], []])

    # === Graph::fromFile ===
    def test_from_file_one_vertex(self):
        """
        Test if we can get the adjacency list for a graph with
        no edges.
        """
        # Graph.fromFile(None)

    def test_from_file_normal_graph(self):
        """
        Test if we can get the adjacency list for a graph with
        many edges and vertices.
        """
        # Graph.fromFile(None)

    # === Graph::toPrism ===
    def test_to_prism_one_vertex(self):
        """
        Test if we can convert a Graph with one vertex to a
        PRISM file.
        """

    def test_to_prism_normal_graph(self):
        """
        Test if we can convert a Graph with many vertices
        and many edges to a PRISM file.
        """


if __name__ == '__main__':
    unittest.main()
