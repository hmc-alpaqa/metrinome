import unittest

class TestUtils(unittest.TestCase):

    # === roundExpression ===
    def testRoundExpression_Simple(self): 
        '''
        Check an expression with only numbers and binary oeprations
        '''
        pass
        # simpleExpression = '1.234567 * 1.123123 + 1.123123 / 1.123123'
        # result = Utils.roundExpression(simpleExpression, 3)
        # expectedResult = "1.234 * 1.123 + 1.123 / 1.123"
        # self.assertEqual(result, expectedResult)

    def testRoundExpression_Polynomial(self):
        '''
        Check that a polynomial simplies correctly
        '''
        pass
        # polynomialExpression = '1.123123 * x**1 + x**1.123123'
        # simplifiedExpression = Utils.roundExpression(polynomialExpression, 3)
        # expectedResult = '1.123 * x**1 + x**1.123'
        # self.assertEqual(simplifiedExpression, expectedResult)

    def testRoundExpressionExponential(self):
        '''
        Coefficients in an exponential expression should be rounded to
        the appropriate numebr of decimal places
        '''
        pass 
        # exponentialExpression = '1.12 * e**(1.123123*x)'
        # simplifiedExpression = Utils.roundExpression(exponentialExpression, 3)
        # expectedResult = '1.12 * e**(1.123*x)'
        # self.assertEqual(expectedResult, simplifiedExpression)

    # === classify ===  
    def classifyHelper(self, expression, expected):
        '''
        Given some expression an expected classification, verify that
        classify() returns the correct classification
        '''
        pass    
        # classified = Utils.classify(expression)
        # self.assertEqual(classified, expected)

    def testClassify_Constant(self):
        '''
        Constants should always return 'Const:<val>' where value is the
        contanst itself. Empty expressions should given us a constant of 0.
        '''
        pass 
        # constantExpression = '2'
        # constantExpressionTwo = '2.0'
        # expectedClassification = 'Const:2.0'
        # self.classifyHelper(constantExpression, expectedClassification)
        # self.classifyHelper(constantExpressionTwo, expectedClassification)

        # emptyExpression = ''
        # expectedClassification = 'Const:0'
        # self.classifyHelper(emptyExpression, expectedClassification)

    def testClassify_Polynomial(self):
        '''
        Check that classify returns the degree of polynomial expressions
        '''
        pass 
        # polynomialExpression = '1 + n + n^2'
        # expectedClassification = 'PolyDeg:2.0'
        # self.classifyHelper(polynomialExpression, expectedClassification)

        # polynomialExpression = 'n^2 - 1'
        # self.classifyHelper(polynomialExpression, expectedClassification)

        # self.classifyHelper('n', 'PolyDeg:1.0')

    def testClassify_Exponential(self):
        '''
        Check that classify returns the base of an exponential in the case
        of exponential expressions
        '''
        pass
        # exponentialExpression = '1 + n + 2^n'
        # expectedClassification = 'ExpBase:2.0'
        # self.classifyHelper(exponentialExpression, expectedClassification)

        # exponentialExpression = '1 + n + 1.5 * 3.1^(2.1*n)'
        # classified = Utils.roundExpression(Utils.classify(exponentialExpression), 4)
        # expectedClassification = 'ExpBase:10.7611'
        # self.assertEqual(classified, expectedClassification)

    # === getSolutionFromRoots ===
    def testSolutionFromRoots(self):
        '''
        Return the solution to a linear homogeneous recurrence relation
        from the roots of the charactersic equation.
        '''
        pass
        # Utils.getSolutionFromRoots()
        # self.assertEqual('1', '1')

    # === getRecurrenceSolution ===
    def testRecurrenceSolution(self):
        '''
        Returns the solution to an arbitrary linear homogeneous recurrence
        relation
        '''
        pass 
        # Utils.getRecurrenceSolution()
        # self.assertEqual('1', '1')

    # === getTaylorCoeffs ===
    def testTaylorCoeffs(self):
        '''
        This should return the coefficients of the Taylor series of a
        rational function (p(x) / q(x) where p and q are polynomials),
        up to a specified degree.
        '''
        pass 
        # Utils.getTaylorCoeffs()
        # self.assertEqual('1', '1')

    # === isExponential ===
    def testIsExponential(self):
        '''
        Test exponential should return True if the expression contains any
        a^n (or any variant of a^n).
        '''
        pass
        # result = Utils.isExponential('n * 2 + 1.5 - 2^n')
        # resultTwo = Utils.isExponential('n + 1 / 2')

        # self.assertEqual(result, True)
        # self.assertEqual(resultTwo, False)

    # === getDegree ===
    def testGetDegree(self):
        '''
        For an arbitrary expression, getDegree should return the maximum
        value that 'x'is raised to. Expression with no 'x' have a degree
        of 0. Expressions with other variables, such as (x^2) + n, should
        only return the degree with respect to 'x'.
        '''
        pass
        # degreeZeroPolynomial = '42'
        # degreeTwoPolynomial = '42 + 1.3*x + 1.341*x^3'
        # polynomialWithParenthesis = '42 + 1.3*x + 1.341*x^(3)'
        # degreeResultOne = Utils.getDegree(degreeZeroPolynomial)
        # degreeResultTwo = Utils.getDegree(degreeTwoPolynomial, 'x')

        # self.assertEqual(degreeResultOne, 0)
        # self.assertEqual(degreeResultTwo, 3)

    # === bigO ===
    def testBigO_Constant(self):
        '''
        The bigO of a constant should be O(1).
        '''
        pass
        # constantExpression = ['1', '2', '3']
        # constantExpressionTwo = ['3', '2', '1']

        # bigOOne = Utils.bigO(constantExpression)
        # bigOTwo = Utils.bigO(constantExpressionTwo)

        # self.assertEqual(bigOOne, '1')
        #self.assertEqual(bigOTwo, '1')

    def testBigO_Polynomial(self):
        '''
        The bigO of a polynomial should be O(x^n) where
        n is the degree of the polynomial
        '''
        pass
        # Expression One: "1 - x + 6*x^8"
        # Expression Two: = "1.2*x^(8.4) - 3.1*x"

        # polynomialExpression = ['1', '-x', '6*x^8']
        # polynomialExpressionTwo = ['1.2*x^(8.4)', '-3.1*x']

        # bigOOne = Utils.bigO(polynomialExpression)
        # bigOTwo = Utils.bigO(polynomialExpressionTwo)

        # expectedBigOOne = 'x^8'
        # expectedBigOTwo = 'x^8.4'
        # self.assertEqual(expectedBigOOne, bigOOne)
        # self.assertEqual(expectedBigOTwo, bigOTwo)

    # === Timeout ===
    def testTimeout_NoTimetout(self):
        '''
        A function that is done before the timeout
        limit should behave normally
        '''
        pass
        # def foo():
        #     return 7

        # result = 0
        # with Utils.Timeout(seconds = 5):
        #     result = foo()
        # self.assertEqual(result, 7)

    def testTimeout_Timeout(self): 
        '''
        A function that takes too long to execute should
        throw an error
        '''
        pass
        # def foo():
        #     sleep(2)

        # with self.assertRaises(TimeoutError):
        #     with Utils.Timeout(seconds = 1):
        #         foo()
        
if __name__ == '__main__':
    unittest.main()
