import unittest
# from ..Graph import Graph

class TestCyclomaticComplexity(unittest.TestCase):
    def testCyclomaticComplexity(self):
        edges = [[0, 1], [1, 2], [3, 4]]
        vertices = set([0, 1, 2, 3, 4])
        startNode = 0
        endNode = 4
        graph = Graph(edges, vertices, startNode, endNode)
        result = CyclomaticComplexity.cyclomaticComplexity(graph)
        # edges - nodes + 2
        expectedResult = 3 - 5 + 2
        self.assertEqual(result, expectedResult)