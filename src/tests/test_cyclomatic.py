import unittest
import sys
sys.path.append("/app/code/")
from Graph import Graph
from metric.CyclomaticComplexity import CyclomaticComplexity

class TestCyclomaticComplexity(unittest.TestCase):
    def testCyclomaticComplexity(self):
        edges = [[0, 1], [1, 2], [3, 4]]
        vertices = set([0, 1, 2, 3, 4])
        startNode = 0
        endNode = 4
        graph = Graph(edges, vertices, startNode, endNode)
        result = CyclomaticComplexity().evaluate(graph)
        expectedResult = 3 - 5 + 2  # edges - nodes + 2
        self.assertEqual(result, expectedResult)

if __name__ == '__main__':
    unittest.main()
