"""Test methods associated with Graph objects and their conversion to Prism files."""

import unittest
import sys
import numpy as np  # type: ignore
sys.path.append("/app/code/")
from graph import Graph, GraphType


class TestGraph(unittest.TestCase):
    """Test Graph objects."""

    # === Graph::node_to_index ===
    def test_node_to_index(self):
        pass

    # === Graph::get_end ===
    def test_get_end(self):
        pass

    # === Graph::get_start ===
    def test_get_start(self):
        pass

    # === Graph::edge_count ===
    def test_edge_count(self):
        pass

    # === Graph::set_name ===
    def test_set_name(self):
        pass

    # === Graph::dot ===
    def test_dot(self):
        pass

    # === Graph::update_with_node ===
    def test_update_with_node(self):
        pass

    # === Graph::update_with_edge ===
    def test_update_with_edge(self):
        pass

    # === Graph::__eq__ ===
    def test_eq(self):
        pass

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
        graph = Graph([], [1, 2, 3], 1, 3, GraphType.EDGE_LIST)
        adj_list = graph.adjacency_list()
        for i in adj_list.keys():
            self.assertTrue(len(adj_list[i]) == 0)

    # # === Graph::from_file ===
    def test_from_file_one_vertex(self):
        """Test if we can get the adjacency list for a graph with no edges."""
        # Graph.fromFile(None)

    def test_from_file_normal_graph(self):
        """Test if we can get the adjacency list for a graph with many edges and vertices."""
    #     # Graph.fromFile(None)

    # # === Graph::to_prism ===
    def test_to_prism_one_vertex(self):
        """Test if we can convert a Graph with one vertex to a PRISM file."""

    def test_to_prism_normal_graph(self):
        """Test if we can convert a Graph with many vertices and many edges to a PRISM file."""
