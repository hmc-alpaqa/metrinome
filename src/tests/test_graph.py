import unittest
# from Graph import Graph

class TestGraph(unittest.TestCase):
    # Graph(edges, vertices, startNode, endNode)

    # === Graph::edgeRules ===
    def testEdgeRules_NoEdges(self):
        g = Graph([], [1, 2, 3], 1, 3)
        g.edgeRules()

    # === Graph::vertexCount ===
    def testVertexCount_OneVertex(self):
        g = Graph([], [1], 1, 1)
        g.vertexCount()

    def testVertexCount_ManyVertices(self): 
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        g.vertexCount()

    # === Graph::getVertices ===
    def testGetVertices_OneVertex(self):
        g = Graph([], [1], 1, 1)
        g.getVertices()

    def testVertices_ManyVertices(self): 
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        g.getVertices()

    # === Graph::advacencyMatrix ===
    def testAdjacencyMatrix_NoEdges(self):
        g = Graph([], [1, 2, 3], 1, 3)
        g.adjacencyMatrix()
        
    def testAdjacencyList_NormalGraph(self):
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        g.adjacencyMatrix()

    # === Graph::adjacencyList ===
    def testAdjacencyList_NoEdges(self):
        g = Graph([], [1, 2, 3], 1, 3)
        g.adjacencyList()

    def testAdjacencyList_NormalGraph(self): 
        g = Graph([[1, 2], [2, 3], [2, 4]], [1, 2, 3, 4], 1, 4)
        g.adjacencyList()

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
