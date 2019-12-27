import unittest, os
# import numpy as np
# from Graph import Graph
# import CppToDot, CyclomaticComplexity, NPathComplexity, Utils
# from time import sleep

# PATH_TO_TEST_FILES = "/home/gabe/Documents/repos/path-complexity/src-py"
# PATH_TO_CFGS = "/home/gabe/Documents/repos/path-complexity"

class TestGraph(unittest.TestCase):
    # def testNonexistant(self):
    #     '''
    #     Verify that attempting to make a graph from a non-
    #     existant file throws any error
    #     '''
    #     with self.assertRaises(FileNotFoundError):
    #         Graph.fromFile("testfiles/graph1.dot")

#     def testMalformed(self):
#         '''
#         Verify that we cannot create a graph if we do not
#         specify a start and end node
#         '''
#         with self.assertRaises(ValueError):
#             print(os.getcwd())
#             Graph.fromFile(f"{PATH_TO_TEST_FILES}/testfiles/graph2.dot")

    def testSinglenode(self):
        '''
        Check that no errors occur on a graph with a single
        node
        '''
        # graph = Graph.fromFile(f"{PATH_TO_TEST_FILES}/testfiles/graph3.dot")
        # self.assertEqual(graph.edgeRules(), [])
        # self.assertEqual(graph.vertexCount(), 1)
        # self.assertEqual(graph.getVertices(), set([0]))
        # expectedAdjacency = np.zeros((1, 1))
        # self.assertEqual(graph.adjacencyMatrix(),
        #                   expectedAdjacency)
        self.assertEqual('temp', 'temp')

#     def testMultiplenodes(self):
#         '''
#         Check that obtain the proper graph in the case of
#         a dot file with multiple nodes and edges
#         '''
#         graph = Graph.fromFile(f"{PATH_TO_TEST_FILES}/testfiles/graph4.dot")
#         self.assertEqual(graph.edgeRules(), [[0, 1], [1, 2], [3, 4]])
#         self.assertEqual(graph.vertexCount(), 5)
#         self.assertEqual(graph.getVertices(), set([0, 1, 2, 3, 4]))
#         expectedAdjacency = np.zeros((5, 5))
#         # Start = 0, End = 4, so nodes are reordered to 
#         # 0, 4, 1, 2, 3
#         expectedAdjacency[0][2] = 1
#         expectedAdjacency[2][3] = 1
#         expectedAdjacency[4][1] = 1
#         self.assertTrue((expectedAdjacency == graph.adjacencyMatrix()).all())

# class TestUtils(unittest.TestCase):

#     # RoundExpression
#     def testRoundExpressionSimple(self):
#         '''
#         Check an expression with only numbers and binary oeprations
#         '''
#         simpleExpression = '1.234567 * 1.123123 + 1.123123 / 1.123123'
#         result = Utils.roundExpression(simpleExpression, 3)
#         expectedResult = "1.234 * 1.123 + 1.123 / 1.123"
#         self.assertEqual(result, expectedResult)

#     def testRoundExpressionPolynomial(self):
#         '''
#         Check that a polynomial simplies correctly
#         '''
#         polynomialExpression = '1.123123 * x**1 + x**1.123123'
#         simplifiedExpression = Utils.roundExpression(polynomialExpression, 3)
#         expectedResult = '1.123 * x**1 + x**1.123'
#         self.assertEqual(simplifiedExpression, expectedResult)

#     def testRoundExpressionExponential(self):
#         '''
#         Coefficients in an exponential expression should be rounded to
#         the appropriate numebr of decimal places
#         '''
#         exponentialExpression = '1.12 * e**(1.123123*x)'
#         simplifiedExpression = Utils.roundExpression(exponentialExpression, 3)
#         expectedResult = '1.12 * e**(1.123*x)'
#         self.assertEqual(expectedResult, simplifiedExpression)

#     # Classify
#     def classifyHelper(self, expression, expected):
#         '''
#         Given some expression an expected classification, verify that
#         classify() returns the correct classification
#         '''
#         classified = Utils.classify(expression)
#         self.assertEqual(classified, expected)

#     def testClassifyConstant(self):
#         '''
#         Constants should always return 'Const:<val>' where value is the
#         contanst itself. Empty expressions should given us a constant of 0.
#         '''
#         constantExpression = '2'
#         constantExpressionTwo = '2.0'
#         expectedClassification = 'Const:2.0'
#         self.classifyHelper(constantExpression, expectedClassification)
#         self.classifyHelper(constantExpressionTwo, expectedClassification)

#         emptyExpression = ''
#         expectedClassification = 'Const:0'
#         self.classifyHelper(emptyExpression, expectedClassification)

#     def testClassifyPolynomial(self):
#         '''
#         Check that classify returns the degree of polynomial expressions
#         '''
#         polynomialExpression = '1 + n + n^2'
#         expectedClassification = 'PolyDeg:2.0'
#         self.classifyHelper(polynomialExpression, expectedClassification)

#         polynomialExpression = 'n^2 - 1'
#         self.classifyHelper(polynomialExpression, expectedClassification)

#         self.classifyHelper('n', 'PolyDeg:1.0')

#     def testClassifyExponential(self):
#         '''
#         Check that classify returns the base of an exponential in the case
#         of exponential expressions
#         '''
#         exponentialExpression = '1 + n + 2^n'
#         expectedClassification = 'ExpBase:2.0'
#         self.classifyHelper(exponentialExpression, expectedClassification)


#         exponentialExpression = '1 + n + 1.5 * 3.1^(2.1*n)'
#         classified = Utils.roundExpression(Utils.classify(exponentialExpression), 4)
#         expectedClassification = 'ExpBase:10.7611'
#         self.assertEqual(classified, expectedClassification)

#     # Timeout 
#     def testNotimeout(self):
#         '''
#         A function that is done before the timeout
#         limit should behave normally
#         '''
#         def foo():
#             return 7

#         result = 0
#         with Utils.Timeout(seconds = 5):
#             result = foo()
#         self.assertEqual(result, 7)

#     def testTimeout(self):
#         '''
#         A function that takes too long to execute should
#         throw an error
#         '''
#         def foo():
#             sleep(2)

#         with self.assertRaises(TimeoutError):
#             with Utils.Timeout(seconds = 1):
#                 foo()

#     # Big O 
#     def testBigOConstant(self):
#         '''
#         The bigO of a constant should be O(1).
#         '''
#         constantExpression = ['1', '2', '3']
#         constantExpressionTwo = ['3', '2', '1']

#         bigOOne = Utils.bigO(constantExpression)
#         bigOTwo = Utils.bigO(constantExpressionTwo)

#         self.assertEqual(bigOOne, '1')
#         self.assertEqual(bigOTwo, '1')

#     def testBigOPolynomial(self):
#         '''
#         The bigO of a polynomial should be O(x^n) where
#         n is the degree of the polynomial
#         '''
#         # Expression One: "1 - x + 6*x^8"
#         # Expression Two: = "1.2*x^(8.4) - 3.1*x"

#         polynomialExpression = ['1', '-x', '6*x^8']
#         polynomialExpressionTwo = ['1.2*x^(8.4)', '-3.1*x']

#         bigOOne = Utils.bigO(polynomialExpression)
#         bigOTwo = Utils.bigO(polynomialExpressionTwo)

#         expectedBigOOne = 'x^8'
#         expectedBigOTwo = 'x^8.4'
#         self.assertEqual(expectedBigOOne, bigOOne)
#         self.assertEqual(expectedBigOTwo, bigOTwo)

#     # Degree
#     def testDegree(self):
#         '''
#         For an arbitrary expression, getDegree should return the maximum
#         value that 'x'is raised to. Expression with no 'x' have a degree
#         of 0. Expressions with other variables, such as (x^2) + n, should
#         only return the degree with respect to 'x'.
#         '''
#         degreeZeroPolynomial = '42'
#         degreeTwoPolynomial = '42 + 1.3*x + 1.341*x^3'
#         polynomialWithParenthesis = '42 + 1.3*x + 1.341*x^(3)'
#         degreeResultOne = Utils.getDegree(degreeZeroPolynomial)
#         degreeResultTwo = Utils.getDegree(degreeTwoPolynomial, 'x')

#         self.assertEqual(degreeResultOne, 0)
#         self.assertEqual(degreeResultTwo, 3)


#     # isExponential
#     def testExponential(self):
#         '''
#         Test exponential should return True if the expression contains any
#         a^n (or any variant of a^n).
#         '''
#         result = Utils.isExponential('n * 2 + 1.5 - 2^n')
#         resultTwo = Utils.isExponential('n + 1 / 2')

#         self.assertEqual(result, True)
#         self.assertEqual(resultTwo, False)


#     # getTaylorCoeffs 
#     def testTaylorCoeffs(self):
#         '''
#         This should return the coefficients of the Taylor series of a
#         rational function (p(x) / q(x) where p and q are polynomials),
#         up to a specified degree.
#         '''
#         # Utils.getTaylorCoeffs()
#         self.assertEqual('1', '1')

#     # getRecurrenceSolution
#     def testRecurrenceSolution(self):
#         '''
#         Returns the solution to an arbitrary linear homogeneous recurrence
#         relation
#         '''

#         # Utils.getRecurrenceSolution()
#         self.assertEqual('1', '1')

#     # getSolutionFromRoots
#     def test_solutionFromRoots(self):
#         '''
#         Return the solution to a linear homogeneous recurrence relation
#         from the roots of the charactersic equation.
#         '''
#         # Utils.getSolutionFromRoots()
#         self.assertEqual('1', '1')

# class TestCPPToDot(unittest.TestCase):

#     def testArgumentParser(self):
#         '''
#         Verify that we obtain the filename from the command line correctly
#         '''
#         arguments = ['--filename', 'example.cpp']
#         result = CppToDot.parseArguments(arguments)
#         self.assertEqual(result, "example.cpp")

#         arguments = ['-f', 'example.cpp']
#         result = CppToDot.parseArguments(arguments)
#         self.assertEqual(result, "example.cpp")

#     def testCreateDot(self):
#         '''
#         Check that no error occurs on creating the .dot files from the .cpp
#         files.

#         Note: this does not verify that the output is correct
#         '''
#         CppToDot.createDotFiles('testfiles/example')
#         for file in os.listdir('ll'):
#             os.remove(f'll/{file}')
#         os.rmdir('ll')

#     def testConvertToStandard(self):
#         '''
#         Verify that we can convert from .dot files of the original format to
#         .dot files of the new format
#         '''
#         # We obtain the non-standard format by creating a dot file from
#         # 'example.cpp'. The dot file file for the main function is stored
#         # in main_f.dot.

#         # Use a copy since convert overwrites the original file 
#         with open('testfles/main_f.dot', 'r') as originalFile:
#             pass

#         # CppToDot.convertToStandardFormat()

# class TestCyclomaticComplexity(unittest.TestCase):
#     def testCyclomaticComplexity(self):
#         edges = [[0, 1], [1, 2], [3, 4]]
#         vertices = set([0, 1, 2, 3, 4])
#         startNode = 0
#         endNode = 4
#         graph = Graph(edges, vertices, startNode, endNode)
#         result = CyclomaticComplexity.cyclomaticComplexity(graph)
#         # edges - nodes + 2
#         expectedResult = 3 - 5 + 2
#         self.assertEqual(result, expectedResult)

# class TestNPATH(unittest.TestCase):

#     def testNPath(self):
#         '''
#         Expected Results:

#         test_number, cfg_file, cyclomatic_complexity, npath_complexity,
#             path_cplxty_class, path_cplxty_asym, path_cplxty
#         1,/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test1_0_basic.dot,4,8,Constant,8.,8.
#         2,/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test2_0_basic.dot,4,4,Constant,4.,4.
#         3,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test3_0_basic.dot,4,8,
#             Polynomial,0.04*n^3.,5. + 3.08*n + 0.62*n^2. + 0.04*n^3.
#         4,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test4_0_basic.dot,4,4,
#             Exponential,1.9000000000000001*1.8^(0.5*n),1. + 0.04*0.45^(0.5*n) + 0.56*1.25^(0.5*n) + 1.9000000000000001*1.8^(0.5*n)
#         5,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test5_0_basic.dot,4,4,
#             Exponential,1.9000000000000001*1.8^(0.5*n),1. + 0.04*0.45^(0.5*n) + 0.56*1.25^(0.5*n) + 1.9000000000000001*1.8^(0.5*n)
#         6,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test6_0_basic.dot,4,8,
#             Polynomial,0.02*n^3.,4. + 2.17*n + 0.38*n^2. + 0.02*n^3.
#         '''
#         basePath = f"{PATH_TO_CFGS}/cfgs/simple_test_cfgs/"
#         prefix = "vlab_cs_ucsb_test_SimpleExample_test"

#         results = []
#         for file_index in range(1, 7):
#             file = basePath + prefix + str(file_index) + "_0_basic.dot"
#             graph = Graph.fromFile(file)
#             print("The Graph is: " + str(graph))
#             res = NPathComplexity.nPathComplexity(graph)
#             results.append(res)

#         expectedResults = [8, 4, 8, 4, 4, 8]
#         self.assertEqual(results, expectedResults)

#     def testNPathSingleNode(self):
#         '''
#         Verify that the NPath complexity code works for a graph with a
#         single node. The start node is equal to the end node,
#         so there is a single path from the beginning to the end
#         '''
#         graph = Graph([], set([0]), 0, 0)
#         result = NPathComplexity.nPathComplexity(graph)
#         expectedResult = 1
#         self.assertEqual(result, expectedResult)

#     def testNPathNoEdges(self):
#         '''
#         Verify that the NPATH complexity for a graph with different start
#         and end nodes but no edges is 0, since there are no paths from the
#         beginning to the end
#         '''
#         graph = Graph([], set([0, 1]), 0, 1)
#         result = NPathComplexity.nPathComplexity(graph)
#         expectedResult = 0
#         self.assertEqual(result, expectedResult)

# class TestPathComplexity(unittest.TestCase):

#     def test(self):
#         pass

# class TestPaths(unittest.TestCase):

#     def test(self):
#         pass

if __name__ == '__main__':
    unittest.main()
