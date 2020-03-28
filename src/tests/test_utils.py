"""
This is used to test the utils that are primarily used in computing APC and
path complexity.
"""

import unittest


class TestUtils(unittest.TestCase):
    """
    Test all of the utils methods.
    """

    # === roundExpression ===
    def test_round_expression_simple(self):
        """Check an expression with only numbers and binary operations."""
        # simpleExpression = '1.234567 * 1.123123 + 1.123123 / 1.123123'
        # result = Utils.roundExpression(simpleExpression, 3)
        # expectedResult = "1.234 * 1.123 + 1.123 / 1.123"
        # self.assertEqual(result, expectedResult)

    def test_round_expression_polynomial(self):
        """Check that a polynomial simplies correctly."""
        # polynomialExpression = '1.123123 * x**1 + x**1.123123'
        # simplifiedExpression = Utils.roundExpression(polynomialExpression, 3)
        # expectedResult = '1.123 * x**1 + x**1.123'
        # self.assertEqual(simplifiedExpression, expectedResult)

    def test_round_expression_exponential(self):
        """
        Coefficients in an exponential expression should be rounded to
        the appropriate numebr of decimal places
        """
        # exponentialExpression = '1.12 * e**(1.123123*x)'
        # simplifiedExpression = Utils.roundExpression(exponentialExpression, 3)
        # expectedResult = '1.12 * e**(1.123*x)'
        # self.assertEqual(expectedResult, simplifiedExpression)

    # === classify ===
    def classify_helper(self, expression, expected):
        """
        Given some expression an expected classification, verify that
        classify() returns the correct classification
        """
        # classified = Utils.classify(expression)
        # self.assertEqual(classified, expected)

    def test_classify_constant(self):
        """
        Constants should always return 'Const:<val>' where value is the
        contanst itself. Empty expressions should given us a constant of 0.
        """
        # constantExpression = '2'
        # constantExpressionTwo = '2.0'
        # expectedClassification = 'Const:2.0'
        # self.classifyHelper(constantExpression, expectedClassification)
        # self.classifyHelper(constantExpressionTwo, expectedClassification)

        # emptyExpression = ''
        # expectedClassification = 'Const:0'
        # self.classifyHelper(emptyExpression, expectedClassification)

    def test_classify_polynomial(self):
        """Check that classify returns the degree of polynomial expressions."""
        # polynomialExpression = '1 + n + n^2'
        # expectedClassification = 'PolyDeg:2.0'
        # self.classifyHelper(polynomialExpression, expectedClassification)

        # polynomialExpression = 'n^2 - 1'
        # self.classifyHelper(polynomialExpression, expectedClassification)

        # self.classifyHelper('n', 'PolyDeg:1.0')

    def test_classify_exponential(self):
        """
        Check that classify returns the base of an exponential in the case
        of exponential expressions
        """
        # exponentialExpression = '1 + n + 2^n'
        # expectedClassification = 'ExpBase:2.0'
        # self.classifyHelper(exponentialExpression, expectedClassification)

        # exponentialExpression = '1 + n + 1.5 * 3.1^(2.1*n)'
        # classified = Utils.roundExpression(Utils.classify(exponentialExpression), 4)
        # expectedClassification = 'ExpBase:10.7611'
        # self.assertEqual(classified, expectedClassification)

    # === getSolutionFromRoots ===
    def test_solution_from_roots(self):
        """
        Return the solution to a linear homogeneous recurrence relation
        from the roots of the charactersic equation.
        """
        # Utils.getSolutionFromRoots()
        # self.assertEqual('1', '1')

    # === getRecurrenceSolution ===
    def test_recurrence_solution(self):
        """Returns the solution to an arbitrary linear homogeneous recurrence relation."""
        # Utils.getRecurrenceSolution()
        # self.assertEqual('1', '1')

    # === getTaylorCoeffs ===
    def test_taylor_coeffs(self):
        """
        This should return the coefficients of the Taylor series of a
        rational function (p(x) / q(x) where p and q are polynomials),
        up to a specified degree.
        """
        # Utils.getTaylorCoeffs()
        # self.assertEqual('1', '1')

    # === isExponential ===
    def test_is_exponential(self):
        """
        Test exponential should return True if the expression contains any
        a^n (or any variant of a^n).
        """
        # result = Utils.isExponential('n * 2 + 1.5 - 2^n')
        # resultTwo = Utils.isExponential('n + 1 / 2')

        # self.assertEqual(result, True)
        # self.assertEqual(resultTwo, False)

    # === getDegree ===
    def test_get_degree(self):
        """
        For an arbitrary expression, getDegree should return the maximum
        value that 'x'is raised to. Expression with no 'x' have a degree
        of 0. Expressions with other variables, such as (x^2) + n, should
        only return the degree with respect to 'x'.
        """
        # degreeZeroPolynomial = '42'
        # degreeTwoPolynomial = '42 + 1.3*x + 1.341*x^3'
        # polynomialWithParenthesis = '42 + 1.3*x + 1.341*x^(3)'
        # degreeResultOne = Utils.getDegree(degreeZeroPolynomial)
        # degreeResultTwo = Utils.getDegree(degreeTwoPolynomial, 'x')

        # self.assertEqual(degreeResultOne, 0)
        # self.assertEqual(degreeResultTwo, 3)

    # === bigo ===
    def test_bigo_constant(self):
        """The bigo of a constant should be O(1)."""
        # constantExpression = ['1', '2', '3']
        # constantExpressionTwo = ['3', '2', '1']

        # bigoOne = Utils.bigo(constantExpression)
        # bigoTwo = Utils.bigo(constantExpressionTwo)

        # self.assertEqual(bigoOne, '1')
        # self.assertEqual(bigoTwo, '1')

    def test_bigo_polynomial(self):
        """
        The bigo of a polynomial should be O(x^n) where n is the degree of the polynomial."""
        # Expression One: "1 - x + 6*x^8"
        # Expression Two: = "1.2*x^(8.4) - 3.1*x"

        # polynomialExpression = ['1', '-x', '6*x^8']
        # polynomialExpressionTwo = ['1.2*x^(8.4)', '-3.1*x']

        # bigoOne = Utils.bigo(polynomialExpression)
        # bigoTwo = Utils.bigo(polynomialExpressionTwo)

        # expectedbigoOne = 'x^8'
        # expectedbigoTwo = 'x^8.4'
        # self.assertEqual(expectedbigoOne, bigoOne)
        # self.assertEqual(expectedbigoTwo, bigoTwo)

    # === Timeout ===
    def test_timeout_notimetout(self):
        """A function that is done before the timeout limit should behave normally."""
        # def foo():
        #     return 7

        # result = 0
        # with Utils.Timeout(seconds = 5):
        #     result = foo()
        # self.assertEqual(result, 7)

    def test_timeout_timeout(self):
        """A function that takes too long to execute should throw an error."""
        # def foo():
        #     sleep(2)

        # with self.assertRaises(TimeoutError):
        #     with Utils.Timeout(seconds = 1):
        #         foo()


if __name__ == '__main__':
    unittest.main()
