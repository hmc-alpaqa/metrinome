import unittest
import sys
sys.path.append("/app/code/")
from Graph import Graph
import numpy as np

class TestGraph(unittest.TestCase):
    # Graph(edges, vertices, startNode, endNode)

    # === Graph::__str__ === 
    def testToStr(self): 
        g = Graph([1, 2], [1, 2, 3], 1, 3)
        expected = "Edges: [1, 2]\nVertices: [1, 2, 3]\nStart Node: 1\nEnd Node: 3"
        self.assertEqual(expected, str(g))

    # === Graph::edgeRules ===
    def testEdgeRules_NoEdges(self):
        g = Graph([], [1, 2, 3], 1, 3)
        edge_list = g.edgeRules()
        self.assertEqual(edge_list, [])

    # === Graph::vertexCount ===
    def testVertexCount_OneVertex(self):
        g = Graph([], [1], 1, 1)
        vertex_count = g.vertexCount()
        self.assertEqual(vertex_count, 1)

    def testVertexCount_ManyVertices(self): 
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        vertex_count = g.vertexCount()
        self.assertEqual(vertex_count, 4)

    # === Graph::getVertices ===
    def testGetVertices_OneVertex(self):
        g = Graph([], [1], 1, 1)
        vertices = g.getVertices()
        self.assertEqual(vertices, [1])

    def testVertices_ManyVertices(self): 
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        vertices = g.getVertices()
        self.assertEqual(vertices, [1, 2, 3, 4])

    # === Graph::advacencyMatrix ===
    def testAdjacencyMatrix_NoEdges(self):
        g = Graph([], [1, 2, 3], 1, 3)
        adj_mat = g.adjacencyMatrix()
        empty_arr = np.zeros((4, 4))
        self.assertTrue((adj_mat == empty_arr).all())
        
    def testAdjacencyList_NormalGraph(self):
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        adj_mat = g.adjacencyMatrix()
        expected_mat = [[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 1, 0, 0, 1],
                        [0, 0, 0, 0, 0]]
        self.assertTrue((adj_mat == expected_mat).all())

    # === Graph::adjacencyList ===
    def testAdjacencyList_NoEdges(self):
        g = Graph([], [1, 2, 3], 1, 3)
        adj_list = g.adjacencyList()
        self.assertEqual(adj_list, [[], [], []])

    # === Graph::fromFile ===
    def testFromFile_OneVertex(self):
        # Graph.fromFile(None)
        pass
    
    def testFromFile_NormalGraph(self): 
        # Graph.fromFile(None)
        pass 

    # === Graph::toPrism ===
    def testToPrism_OneVertex(self):
        pass

    def testToPrism_NormalGraph(self): 
        pass 

if __name__ == '__main__':
    unittest.main()
