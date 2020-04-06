"""
Various utilities for the REPL.

This module contains utilities for computing asymptotic path complexity.
It also allows us to execute a block of code such that an error will be thrown
if the execution takes too long by using the Timeout class.
"""

from typing import List
import re
from collections import Counter
import signal
from sympy import limit, Abs, sympify, series, symbols  # type: ignore
from mpmath import polyroots  # type: ignore


def round_expression(expr: str, digits: int) -> str:
    """
    Round all of the numbers in an expression to a given number of decimal places.

    Take some sympy expression represented as a string
    and round all numbers to the given number of decimal places.
    """
    reg_exp = r"([0-9]*)\.([0-9]*)"

    def replace_with_rounded(match):
        return match.groups()[0] + "." + match.groups()[1][0:digits]

    return re.sub(reg_exp, replace_with_rounded, expr)


def classify(expr: str, var="n") -> str:
    """
    Given an arbitrary expression represented as a string, return a value indicating its 'class'.

    Note: the string cannot have other variables (e.g. we cannot classify '2m' in terms of 'n').

    Exponentiation is represented by '^'.

    Const: [Value]
    PolyDeg: [Highest Degree of Polynomial]
    ExpBase: [Return the base of expression of the form a^x]
    """
    if expr == '':
        return "Const:0"

    try:
        val = float(str(expr))
        return f"Const:{val}"
    except ValueError:
        # If we have anything to the power 'n', then it is exponential.
        val = is_exponential(expr, var)
        if val is None:
            degree = get_degree(expr, var)
            return f"PolyDeg:{degree}"

        return f"ExpBase:{val}"


def get_solution_from_roots(roots):
    """Return the solution to a recurrence relation given roots of the characteristic equation."""
    # Round to 4 digits.
    roots = [complex(round(root.real, 6), round(root.imag, 6)) for root in roots]

    # Compute the multiplicy of each root.
    roots_with_multiplicities = Counter(roots)

    # Compute the coefficients of a_n as a list.
    solution = []
    for root in roots_with_multiplicities.keys():
        for i in range(0, roots_with_multiplicities[root]):
            if root == 1:
                solution += [sympify(f"(n**{i})")]
            else:
                solution += [sympify(f"(n**{i})*{root}**n")]

    return solution


def get_recurrence_solution(recurrence: str):
    """
    Return the coefficients to a homogeneous linear recurrence relation.

    This is represented as a string of the format

    c_0*f(n) + c_1*f(n-1) + ... + c_k*f(n-k)

    by finding the roots of the characteristic equation.
    """
    # Define symbolic terms
    # n = symbols('n')
    # f = Function('f')

    # Regular expression to parse the recurrence relation expression.
    # RE matches a particular term: Coefficient + f(something)
    match_function = r'f\([ a-zA-Z0-9-+]*\)'
    match_obj = re.findall(rf'([ +-.0-9]*)(\*)({match_function})', recurrence)
    coeffs: List[float] = []
    for match in match_obj:
        coeffs += [float(match[0].replace(" ", ""))]

    # Normalize such that leading coefficient is 1.
    leading_coeff = coeffs[0]
    coeffs = list(map(lambda coeff: coeff / leading_coeff, coeffs))

    # Find the roots of the characteristic equation
    # through arbitrary precision root finding function.
    roots = polyroots(coeffs, maxsteps=200, extraprec=200)

    return get_solution_from_roots(roots)


def get_taylor_coeffs(func, num_coeffs: int):
    """Given an arbitrary rational function, get its Taylor series coefficients."""
    t_var = symbols('t')
    series_list = str(series(func, x=t_var, x0=0, n=num_coeffs)).split('+')
    first_element = series_list[0]
    first_power = re.search(r"\*\*([0-9]*)", str(first_element))
    if first_power is not None:
        first_power_int = int(first_power.groups()[0])
        taylor_coeffs = [0] * first_power_int + [sympify(f).subs(t_var, 1) for f in series_list]
        return taylor_coeffs

    return None


def is_exponential(term: str, var='n'):
    """If an expression contains an exponential, return its base. Otherwise, return None."""
    # either ^n or ^(num*n)
    num = "([0-9][0-9]*[.][0-9]*)|([.][0-9][0-9]*)|([0-9][0-9]*)"
    search_string = rf"({num})\^{var}"
    results = re.findall(search_string, term)
    max_base = None
    if results:
        max_base = max(map(lambda res: float(res[0]), results))

    search_string_with_parens = rf"({num})\^\(({num})?\*{var}\)"
    results = re.findall(search_string_with_parens, term)
    if results:
        # a^(bn) should be classified as a^b

        def func(res):
            return float(res[0])**float(res[4])

        new_base = max(map(func, results))
        if new_base is not None:
            if max_base is None or new_base > max_base:
                max_base = new_base

    return max_base


def get_degree(term: str, var="n") -> float:
    """If an expression is a polynomial, return the degree. Otherwise, return 0."""
    num = "([0-9][0-9]*[.][0-9]*)|([.][0-9][0-9]*)|([0-9][0-9]*)"
    regexp = rf"{var}\^({num})"
    res = re.findall(regexp, term)
    found_deg = 0.
    if res:
        found_deg = max(map(lambda x: float(x[0]), res))

    if found_deg == 0. and re.search(var, term) is not None:
        return 1.

    return found_deg


def big_o(terms):
    """
    Compute the big O of some expression in terms of 'n'.

    The terms should be a list of expressions represented as strings.
    """
    n_var = symbols('n')
    if len(terms) == 0:
        return 0.0
    if len(terms) == 1:
        return terms[0]

    term_one = terms[0]
    term_two = terms[1]
    lim = limit(Abs(sympify(term_two) / sympify(term_one)), n_var, float('inf'))

    if lim == 0:
        return term_one

    return big_o(terms[1:])


class Timeout:
    """
    Set a maximum amount of a time a block of code can take to execute.

    Allows us to run a block of code such that a TimeoutError is thrown if
    it does not finish within a given amount of time.
    """

    def __init__(self, seconds=1, error_message='Timeout') -> None:
        """Create a new instance of Timeout."""
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        """Execute after self.seconds have passed if the block within it is not done."""
        raise TimeoutError(self.error_message)

    def __enter__(self) -> None:
        """Start the timer when we begin executing the code within the block this class wraps."""
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, err_type, value, traceback) -> None:
        """Stop the timer once the code block is done executing."""
        signal.alarm(0)
