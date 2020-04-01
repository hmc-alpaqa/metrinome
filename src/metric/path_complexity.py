"""Compute the path complexity and asymptotic path complexity metrics."""

import re  # type: ignore
import logging
from typing import Any
from sympy import Matrix, eye, symbols, degree, Poly, simplify, expand, sympify  # type: ignore
from mpmath import polyroots  # type: ignore
from utils import big_o, get_taylor_coeffs, get_solution_from_roots
from graph import Graph
from metric import metric  # type: ignore

# pylint: disable=W0231
# disable super-init-not-called since metric.MetricAbstract is an abstract class and therefore
# __init__ should be implemented.


class PathComplexity(metric.MetricAbstract):
    """Compute the path complexity and APC metrics for arbitrary Graph objects."""

    def __init__(self) -> None:
        """Create a new instance of PathComplexity."""

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Path Complexity"

    def adjacency_matrix(self, graph: Graph) -> Matrix:
        """
        Generate the adjacency matrix used in the path complexity algorithm from a Graph.

        This adds a loop at the correct position required for the algorithm to work.
        """
        adj_mat = graph.adjacency_matrix()
        adj_mat[1][1] = 1
        return Matrix(adj_mat)

    def evaluate(self, graph: Graph) -> Any:
        """
        Compute the path complexity given the CFG of some function.

        Return both the path complexity and the asymptotic path complexity.
        """
        adj_mat = graph.adjacency_matrix()
        adj_mat[1][1] = 1
        new_adjacency = Matrix(adj_mat)

        t_var = symbols('t')
        dimension = adj_mat.shape[0]
        x_mat = eye(dimension) - new_adjacency * t_var
        x_sub = x_mat.copy()
        x_sub.col_del(0)
        x_sub.row_del(1)
        x_det = x_mat.det()
        denominator = Poly(-x_det)
        generating_function = x_sub.det() / denominator

        recurrence_degree = degree(denominator, gen=t_var) + 1
        recurrence_kernel = denominator.all_coeffs()[::-1]

        test = [round(-x, 2) for x in recurrence_kernel]

        roots = polyroots(test, maxsteps=200, extraprec=200)

        logging.info(f"Generating Function: {generating_function}")
        taylor_coeffs = get_taylor_coeffs(generating_function, 2 * dimension + 1)
        base_cases = Matrix(taylor_coeffs[dimension: dimension + recurrence_degree - 1])

        # Should have as many things as the recurrenceKernel
        # l_range = Matrix(list(range(0, recurrence_degree)))
        n_var = symbols('n')
        # n_range = Matrix([n for _ in range(0, recurrence_degree)])

        # Solve the recurrence relation
        terms = get_solution_from_roots(roots)

        coefficients = symbols("C0:" + str(len(terms)))
        if len(coefficients) == 1:
            factors = [i / j for i, j in zip(terms, coefficients)]
        else:
            factors = terms

        matrix = Matrix([[fact.replace(n_var, nval) for fact in factors]
                         for nval in range(1, len(factors) + 1)])

        # try:
        inv_m = matrix**-1
        bounding_solution_terms = (inv_m * base_cases)
        bounding_solution_terms = bounding_solution_terms.dot(Matrix(factors))
        expr_with_abs = str(expand(bounding_solution_terms))

        # Replace all instances of x^n with abs(x)^n
        expr = r"[*]\(([-][0-9]*)\)\*\*n"

        def replace_with_absolute_val(match):
            base = abs(float(match.groups()[0]))
            if base == 1:
                return ""

            return f"{base}**n"

        expr_with_abs = re.sub(expr, replace_with_absolute_val, expr_with_abs)
        expr_with_abs = str(simplify(sympify(expr_with_abs)))

        # Replace all complex numbers with their absolute values
        # expr_with_abs = expr_with_abs

        # Split terms on '+'
        terms = [x.strip() for x in expr_with_abs.split(" + ")]
        new_terms = []
        for term in terms:
            new_terms += str(term).split(" - ")
        apc = big_o(new_terms)

        return (apc, expr_with_abs)
