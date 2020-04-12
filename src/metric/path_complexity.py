"""Compute the path complexity and asymptotic path complexity metrics."""

import re  # type: ignore
import logging
import numpy as np  # type: ignore
import sympy  # type: ignore
from sympy import refine, preorder_traversal, Add, Float, Matrix, eye, symbols, degree, Poly, \
    simplify, expand, sympify, collect, Abs, Q  # type: ignore
from mpmath import polyroots  # type: ignore
from Utils import big_o, get_taylor_coeffs, get_solution_from_roots
from graph import Graph
from metric import metric  # type: ignore
from typing import Any


class PathComplexity(metric.MetricAbstract):
    """Compute the path complexity and asymptotic path complexity metrics."""
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
        if taylor_coeffs is not None:
            base_cases = np.matrix(taylor_coeffs[dimension:dimension + recurrence_degree - 1],
                                   dtype='complex')
        else:
            return (0.0, 0.0)
        # Should have as many things as the recurrenceKernel
        # l_range = Matrix(list(range(0, recurrence_degree)))
        n_var = symbols('n')

        # n_range = Matrix([n for _ in range(0, recurrence_degree)])

        # Solve the recurrence relation
        terms = get_solution_from_roots(roots)

        
        factors = terms
        matrix = np.matrix([[fact.replace(n_var, nval) for fact in factors]
                           for nval in range(1, len(factors) + 1)], dtype='complex')

        # try:
        base_cases = base_cases.transpose()
        bounding_solution_terms = np.linalg.lstsq(matrix, base_cases, rcond=None)[0]

        bounding_solution_terms = bounding_solution_terms.transpose().dot(Matrix(factors))
        expr_without_abs = bounding_solution_terms[0][0]
        # Replace all instances of x^n with abs(x)^n

        expr_without_abs = str(expr_without_abs)[2:-2]

        expr_without_abs = simplify(sympify(expr_without_abs))
        expr_with_abs = expr_without_abs
        for a in preorder_traversal(expr_without_abs):
            if isinstance(a, Float):
                expr_with_abs = expr_with_abs.subs(a, round(a, 2))

        exp_terms = ([str(Abs(k)) for k in list(expr_with_abs.args)])
        for i in range(len(exp_terms)):
            sv = exp_terms[i]
            sv = sv.replace("Abs(n)", 'n')
            sv = sv.replace("re(n)", 'n')
            sv = sv.replace("im(n)", '0')
            sv = sv.replace("exp", "0*")
            exp_terms[i] = sv

        exp_terms = [simplify(sympify(arg)) for arg in exp_terms]
        exp_terms = [refine(term, Q.real(n_var)) for term in exp_terms]
        exp_terms = list(filter(lambda a: a != 0, exp_terms))

        apc = big_o(exp_terms)

        def convert(list):
            return (*list, )
        exp_terms = convert(exp_terms)

        exp_terms = sympify(exp_terms)
        terms = str(sum(exp_terms))
        if apc != 0.0:
            return (sympy.LM(apc), terms)
        else:
            return(expr_with_abs, expr_with_abs)
