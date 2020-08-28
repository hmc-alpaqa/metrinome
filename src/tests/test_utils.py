"""This is used to test the utils that are primarily used in computing APC and path complexity."""
import sys
sys.path.append("/app/code")
import unittest
from time import sleep
import utils


class Testutils(unittest.TestCase):
    """Test all of the utils methods."""

    # === show_func_defs ===
    def test_show_func_defs(self) -> None:
        """Check that we can get the names of all functions in a C file."""
        names = utils.show_func_defs("/app/code/tests/cFiles/collatz.c")
        self.assertTrue(len(names.keys()) == 1)
        self.assertTrue(list(names.keys())[0] == "countCollatz")

    # === get_solution_from_roots ===
    def test_solution_from_roots(self) -> None:
        """
        Verify that we get the correct solution to recurrence solution.

        The method should return the solution to a linear homogeneous recurrence relation
        from the roots of the charactersic equation.
        """
        # utils.getSolutionFromRoots()
        # self.assertEqual('1', '1')

    # === get_recurrence_solution ===
    def test_recurrence_solution(self) -> None:
        """Returns the solution to an arbitrary linear homogeneous recurrence relation."""
        # utils.getRecurrenceSolution()
        # self.assertEqual('1', '1')

    # === get_taylor_coeffs ===
    def test_taylor_coeffs(self) -> None:
        """
        Verify that we get the correct coefficients of a Taylor series.

        This should return the coefficients of the Taylor series of a
        rational function (p(x) / q(x) where p and q are polynomials),
        up to a specified degree.
        """
        # utils.getTaylorCoeffs()
        # self.assertEqual('1', '1')

    # === big_o ===
    def test_big_o_empty(self) -> None:
        """Check that we can get the big O of an empty expression."""
        big_o = utils.big_o([])
        self.assertEqual(big_o, '0')

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
        def fast_func() -> int:
            """Execute immediately."""
            return 7

        result = 0
        with utils.Timeout(seconds=1):
            result = fast_func()
        self.assertEqual(result, 7)

    def test_timeout_timeout(self) -> None:
        """A function that takes too long to execute should throw an error."""
        def slow_func() -> None:
            sleep(2)

        with self.assertRaises(TimeoutError):
            with utils.Timeout(seconds=1):
                slow_func()


if __name__ == '__main__':
    unittest.main()
