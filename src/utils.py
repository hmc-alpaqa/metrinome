"""
Various utilities for the REPL.

This module contains utilities for computing asymptotic path complexity.
It also allows us to execute a block of code such that an error will be thrown
if the execution takes too long by using the Timeout class.
"""

from typing import List, Dict, Optional, Union, Type, Tuple
from types import FrameType, TracebackType
import re
from collections import Counter
import signal
import os
from sympy import limit, Abs, sympify, symbols, Basic, Poly, Mul, Pow  # type: ignore
from mpmath import polyroots, mpc, mpf  # type: ignore
from pycparser import parse_file  # type: ignore


def get_solution_from_roots(roots: List[Union[mpf, mpc]]) -> Tuple[List[Basic], List[Basic]]:
    """Return the solution to a recurrence relation given roots of the characteristic equation."""
    # Round to 4 digits.
    new_roots = (complex(round(root.real, 6), round(root.imag, 6)) for root in roots)

    # Compute the multiplicy of each root.
    roots_with_multiplicities = Counter(new_roots)

    # Compute the coefficients of a_n as a list.
    solution = []
    simplified_solution = []
    for root in roots_with_multiplicities.keys():
        for i in range(roots_with_multiplicities[root]):
            if root == 1:
                term = sympify(f"(n**{i})")
                solution += [term]
                simplified_solution += [term]
            else:
                solution += [sympify(f"(n**{i})*{root}**n")]
                abs_root = Abs(root)
                if abs_root == 1:
                    simplified_solution += [sympify(f"(n**{i})")]
                else:
                    simplified_solution += [sympify(f"(n**{i})*{Abs(root)}**n")]

    return solution, simplified_solution


def get_recurrence_solution(recurrence: str) -> Tuple[List[Basic], List[Basic]]:
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


def get_taylor_coeffs(func: Basic,
                      max_num_coeffs: int,
                      num_coeffs: int,
                      lazy: bool = True) -> Tuple[List[int], Optional[int]]:
    """Given an arbitrary rational function, get its Taylor series coefficients."""
    t_var = symbols('t')

    if lazy:
        taylor_series_generator = func.series(t_var, x0=0, n=None)

        first_nonzero_term = next(taylor_series_generator)
        if isinstance(first_nonzero_term, Pow):
            curr_term_exp = first_nonzero_term.exp
        else:
            # must be Mul
            curr_term_exp = first_nonzero_term.args[1].exp
        new_start_idx = curr_term_exp
        taylor_series = [0] * curr_term_exp + \
            [first_nonzero_term.args[0] if isinstance(first_nonzero_term, Mul) else 1]
        taylor_series += list(map(
            lambda x: int(x.args[0]) if isinstance(x, Mul) else 1,
            [next(taylor_series_generator) for _ in range(num_coeffs)]
        ))

        # Workaround to get all coeffs, since sympy does not return 0 coeffs,
        # Make sure to return coeffs from low -> high order.
        return taylor_series, new_start_idx

    # Get the series but ignore the big-O term that is added by sympy.
    # Note: removeO() makes it go from high order -> low order
    # taylor_series = func.series(t_var, x0=0, n=max_num_coeffs).removeO()
    taylor_series = func.series(t_var, x0=0, n=max_num_coeffs).removeO()
    return Poly(taylor_series).all_coeffs()[::-1], None


def big_o(terms: List[str]) -> str:
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


def show_func_defs(filename: str) -> Dict[str, str]:
    """Return a list of the functions defined in a file."""
    ast = parse_file(filename, use_cpp=True,
                     cpp_args=r'-I/app/pycparser/utils/fake_libc_include')

    names = {}

    for i in ast:
        if str(type(i)) == "<class 'pycparser.c_ast.FuncDef'>":
            names[i.decl.name] = str(i.decl.coord)
        elif str(type(i)) == "<class 'pycparser.c_ast.Decl'>":
            names[i.name + '_decl'] = str(i.coord)
    return names


def calls_function(calls_dict: Dict[int, str], function_cfg: str) -> List[int]:
    """Check if a CFG contains a call to another function."""
    nodes = []
    func_name = os.path.splitext(os.path.splitext(function_cfg)[0])[1][1:]
    for node in calls_dict.keys():
        if calls_dict[node].endswith(func_name):
            nodes.append(node)
    return nodes


class Timeout:
    """
    Set a maximum amount of a time a block of code can take to execute.

    Allows us to run a block of code such that a TimeoutError is thrown if
    it does not finish within a given amount of time.
    """

    def __init__(self, seconds: int = 1, error_message: str = 'Timeout') -> None:
        """Create a new instance of Timeout."""
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum: int, frame: FrameType) -> None:
        """Execute after self.seconds have passed if the block within it is not done."""
        raise TimeoutError(self.error_message)

    def __enter__(self) -> None:
        """Start the timer when we begin executing the code within the block this class wraps."""
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self,
                 err_type: Optional[Type[BaseException]],
                 value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        """Stop the timer once the code block is done executing."""
        signal.alarm(0)
