"""This is used to test the utils that are primarily used in computing APC and path complexity."""
import sys
sys.path.append("/app/code")
import unittest
import utils


class Testutils(unittest.TestCase):
    """Test all of the utils methods."""

    # === roundExpression ===
    def test_round_expression_simple(self) -> None:
        """Check an expression with only numbers and binary operations."""
        # simpleExpression = '1.234567 * 1.123123 + 1.123123 / 1.123123'
        # result = utils.roundExpression(simpleExpression, 3)
        # expectedResult = "1.234 * 1.123 + 1.123 / 1.123"
        # self.assertEqual(result, expectedResult)

    def test_round_expression_polynomial(self) -> None:
        """Check that a polynomial simplies correctly."""
        # polynomialExpression = '1.123123 * x**1 + x**1.123123'
        # simplifiedExpression = utils.roundExpression(polynomialExpression, 3)
        # expectedResult = '1.123 * x**1 + x**1.123'
        # self.assertEqual(simplifiedExpression, expectedResult)

    def test_round_expression_exponential(self) -> None:
        """
        Check that we can round numbers in an expression.

        Coefficients in an exponential expression should be rounded to
        the appropriate number of decimal places
        """
        # exponentialExpression = '1.12 * e**(1.123123*x)'
        # simplifiedExpression = utils.roundExpression(exponentialExpression, 3)
        # expectedResult = '1.12 * e**(1.123*x)'
        # self.assertEqual(expectedResult, simplifiedExpression)

    # === classify ===
    def classify_helper(self, expression, expected) -> None:
        """
        Check that the expression is classified correctly.

        Given some expression and expected classification, verify that
        classify() returns the correct classification
        """
        # classified = utils.classify(expression)
        # self.assertEqual(classified, expected)

    def test_classify_constant(self) -> None:
        """
        Verify that constant expressions are classified correctly.

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

    def test_classify_exponential(self) -> None:
        """Check that classify returns the base of an exponential for exponential expressions."""
        # exponentialExpression = '1 + n + 2^n'
        # expectedClassification = 'ExpBase:2.0'
        # self.classifyHelper(exponentialExpression, expectedClassification)

        # exponentialExpression = '1 + n + 1.5 * 3.1^(2.1*n)'
        # classified = utils.roundExpression(utils.classify(exponentialExpression), 4)
        # expectedClassification = 'ExpBase:10.7611'
        # self.assertEqual(classified, expectedClassification)

    # === getSolutionFromRoots ===
    def test_solution_from_roots(self) -> None:
        """
        Verify that we get the correct solution to recurrence solution.

        The method should return the solution to a linear homogeneous recurrence relation
        from the roots of the charactersic equation.
        """
        # utils.getSolutionFromRoots()
        # self.assertEqual('1', '1')

    # === getRecurrenceSolution ===
    def test_recurrence_solution(self) -> None:
        """Returns the solution to an arbitrary linear homogeneous recurrence relation."""
        # utils.getRecurrenceSolution()
        # self.assertEqual('1', '1')

    # === getTaylorCoeffs ===
    def test_taylor_coeffs(self) -> None:
        """
        Verify that we get the correct coefficients of a Taylor series.

        This should return the coefficients of the Taylor series of a
        rational function (p(x) / q(x) where p and q are polynomials),
        up to a specified degree.
        """
        # utils.getTaylorCoeffs()
        # self.assertEqual('1', '1')

    # === isExponential ===
    def test_is_exponential(self) -> None:
        """
        Test exponential should return True if the expression contains any a^n.

        This should also return True if it includes variants of a^n.
        """
        # result = utils.isExponential('n * 2 + 1.5 - 2^n')
        # resultTwo = utils.isExponential('n + 1 / 2')

        # self.assertEqual(result, True)
        # self.assertEqual(resultTwo, False)

    # === getDegree ===
    def test_get_degree(self) -> None:
        """
        Test the get_degree function.

        For an arbitrary expression, get_egree should return the maximum
        value that 'x'is raised to. Expression with no 'x' have a degree
        of 0. Expressions with other variables, such as (x^2) + n, should
        only return the degree with respect to 'x'.
        """
        # degreeZeroPolynomial = '42'
        # degreeTwoPolynomial = '42 + 1.3*x + 1.341*x^3'
        # polynomialWithParenthesis = '42 + 1.3*x + 1.341*x^(3)'
        # degreeResultOne = utils.getDegree(degreeZeroPolynomial)
        # degreeResultTwo = utils.getDegree(degreeTwoPolynomial, 'x')

        # self.assertEqual(degreeResultOne, 0)
        # self.assertEqual(degreeResultTwo, 3)

    # === big_o===
    def test_big_o_constant(self) -> None:
        """The big_o of a constant should be O(1)."""
        constant_expression = ['1', '2', '3']
        constant_expression_two = ['3', '2', '1']

        big_o_one = utils.big_o(constant_expression)
        big_o_two = utils.big_o(constant_expression_two)

        self.assertEqual(big_o_one, '3')
        self.assertEqual(big_o_two, '1')

    def test_big_o_polynomial(self) -> None:
        """The big_o of a polynomial should be O(x^n) where n is the degree of the polynomial."""
        # Expression One: "1 - x + 6*x^8"
        # Expression Two: = "1.2*x^(8.4) - 3.1*x"

        polynomial_expression = ['1', '-n', '6*n^8']
        polynomial_expression_two = ['1.2 * n^(8.4)', '-3.1 * n']

        big_o_one = utils.big_o(polynomial_expression)
        print("=== STARTING THIS TEST ===")
        big_o_two = utils.big_o(polynomial_expression_two)

        expectedbig_o_one = '6*n^8'
        expectedbig_o_two = '1.2 * n^(8.4)'
        self.assertEqual(expectedbig_o_one, big_o_one)
        self.assertEqual(expectedbig_o_two, big_o_two)

    def test_big_o_exponential(self) -> None:
        """The big_o of an exponential should be O(a^x) where a is the base."""
        # Expression One: "1 + x + .5^x + 2^x"
        # Expression Two: "2*1.01^x + 1.02^x"

        expression = ['1000000', 'x', '.5**x', '2**x']
        expression_two = ['2*1.01**x', '1.02**x']

        big_o_one = utils.big_o(expression)
        big_o_two = utils.big_o(expression_two)

        expectedbig_o_one = '2**x'
        expectedbig_o_two = '1.02**x'

        self.assertEqual(expectedbig_o_one, big_o_one)
        self.assertEqual(expectedbig_o_two, big_o_two)

    # === Timeout ===
    def test_timeout_notimetout(self) -> None:
        """A function that is done before the timeout limit should behave normally."""
        # def foo():
        #     return 7

        # result = 0
        # with utils.Timeout(seconds = 5):
        #     result = foo()
        # self.assertEqual(result, 7)

    def test_timeout_timeout(self) -> None:
        """A function that takes too long to execute should throw an error."""
        # def foo():
        #     sleep(2)

        # with self.assertRaises(TimeoutError):
        #     with utils.Timeout(seconds = 1):
        #         foo()


if __name__ == '__main__':
    unittest.main()
