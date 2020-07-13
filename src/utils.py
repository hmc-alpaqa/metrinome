"""
Various utilities for the REPL.

This module contains utilities for computing asymptotic path complexity.
It also allows us to execute a block of code such that an error will be thrown
if the execution takes too long by using the Timeout class.
"""

from typing import List, Any
import re
from collections import Counter
import signal
from sympy import limit, Abs, sympify, series, symbols  # type: ignore
from mpmath import polyroots  # type: ignore
from pycparser import parse_file  # type: ignore


def get_solution_from_roots(roots: List[Any]):
    """Return the solution to a recurrence relation given roots of the characteristic equation."""
    # Round to 4 digits.
    new_roots = (complex(round(root.real, 6), round(root.imag, 6)) for root in roots)

    # Compute the multiplicy of each root.
    roots_with_multiplicities = Counter(new_roots)

    # Compute the coefficients of a_n as a list.
    solution = []
    for root in roots_with_multiplicities.keys():
        for i in range(roots_with_multiplicities[root]):
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
    series_list = str(series(func, x=t_var, x0=0, n=num_coeffs)).split('+')[::-1]
    first_element = series_list[0]
    first_power = re.search(r"\*\*([0-9]*)", str(first_element))

    if first_power is not None:
        taylor_coeffs = [sympify(f).subs(t_var, 1) for f in series_list]
        return taylor_coeffs

    return None


def big_o(terms):
    """
    Compute the big O of some expression in terms of 'n'.

    The terms should be a list of expressions represented as strings.
    """
    n_var = symbols('n')
    if len(terms) == 0:
        return '0'

    if len(terms) == 1:
        return terms[0]

    term_one = terms[0]
    term_two = terms[1]
    lim = limit(Abs(sympify(term_two) / sympify(term_one)), n_var, float('inf'))

    if lim == 0:
        terms.remove(term_two)
        return big_o(terms)

    return big_o(terms[1:])


def show_func_defs(filename):
    """Return a list of the functions defined in a file."""
    ast = parse_file(filename, use_cpp=True,
                     cpp_args=r'-I/app/pycparser/utils/fake_libc_include')

    names = {}

    for i in ast:
        if str(type(i)) == "<class 'pycparser.c_ast.FuncDef'>":
            names[i.decl.name] = str(i.decl.coord)
    return names


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
