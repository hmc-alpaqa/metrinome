"""Compute the path complexity and asymptotic path complexity metrics."""

from typing import Any
import sys
import re
import sympy  # type: ignore
from sympy import refine, preorder_traversal, Float, Matrix, eye, symbols, degree, Poly, \
    simplify, sympify, Abs, Q  # type: ignore
from mpmath import polyroots  # type: ignore
sys.path.append("/app/code/")
import numpy as np  # type: ignore
from utils import big_o, get_taylor_coeffs, get_solution_from_roots
from graph import Graph
from metric import metric  # type: ignore


class PathComplexity(metric.MetricAbstract):
    """Compute the path complexity and asymptotic path complexity metrics."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger=None) -> None:
        """Create a new instance of PathComplexity."""
        self.logger = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Path Complexity"

    def gen_func_taylor_coeffs(self, graph):
        """Use the CFG to obtain the taylor series from the generating function."""
        adj_mat = graph.adjacency_matrix()
        adj_mat[1][1] = 1
        new_adjacency = Matrix(adj_mat)

        t_var = symbols('t')
        dimension = adj_mat.shape[0]
        x_mat = eye(dimension) - new_adjacency * t_var
        x_sub = x_mat.copy()

        x_sub.col_del(0)
        x_sub.row_del(1)

        self.logger.d_msg(f"Matrix shape: {x_mat.shape}")

        x_det = x_mat.det()

        denominator = Poly(sympify(-x_det))

        generating_function = x_sub.det(method="det_LU") / denominator

        recurrence_degree = degree(denominator, gen=t_var) + 1

        recurrence_kernel = denominator.all_coeffs()[::-1]
        test = [round(-x, 2) for x in recurrence_kernel]
        roots = polyroots(test, maxsteps=250, extraprec=250)
        taylor_coeffs = get_taylor_coeffs(generating_function, 2 * dimension + 1)

        return taylor_coeffs, dimension, recurrence_degree, roots

    # pylint: disable=too-many-locals
    def evaluate(self, graph: Graph) -> Any:
        """
        Compute the path complexity given the CFG of some function.

        Return both the path complexity and the asymptotic path complexity.
        """
        taylor_coeffs, dimension, recurrence_degree, roots = self.gen_func_taylor_coeffs(graph)
        if taylor_coeffs is None:
            return (0.0, 0.0)

        base_cases = np.matrix(taylor_coeffs[dimension: dimension + recurrence_degree - 1],
                               dtype='complex')
        n_var = symbols('n')

        # Solve the recurrence relation.
        factors = get_solution_from_roots(roots)
        matrix = np.matrix([[fact.replace(n_var, nval) for fact in factors]
                            for nval in range(1, len(factors) + 1)], dtype='complex')
        base_cases = base_cases.transpose()
        self.logger.d_msg(f"Got the base cases.")

        bounding_solution_terms = np.linalg.lstsq(matrix, base_cases, rcond=None)[0]
        self.logger.d_msg(f"Got the bounding solution terms.")

        bounding_solution_terms = bounding_solution_terms.transpose().dot(Matrix(factors))
        expr_without_abs = bounding_solution_terms[0][0]
        expr_without_abs = str(expr_without_abs)[2:-2]
        expr_without_abs = simplify(sympify(expr_without_abs))
        expr_with_abs = expr_without_abs
        for expr_term in preorder_traversal(expr_without_abs):
            if isinstance(expr_term, Float):
                expr_with_abs = expr_with_abs.subs(expr_term, round(expr_term, 2))

        exp_terms = [str(Abs(k)) for k in list(expr_with_abs.args)]
        for i, exp_term in enumerate(exp_terms):
            exp_term = exp_term.replace("Abs(n)", 'n')
            exp_term = exp_term.replace("re(n)", 'n')
            exp_term = exp_term.replace("im(n)", '0')
            exp_term = exp_term.replace("exp", "0*")
            exp_terms[i] = exp_term.replace("I", "0")

        exp_terms = [simplify(sympify(arg)) for arg in exp_terms]
        exp_terms = [refine(term, Q.real(n_var)) for term in exp_terms]  # pylint: disable=E1121
        exp_terms = list(filter(lambda a: a != 0, exp_terms))

        apc = big_o(exp_terms)

        exp_terms_list = (*exp_terms, )
        exp_terms_list = sympify(exp_terms_list)
        terms = str(sum(exp_terms_list))
        if apc != 0.0:
            if degree(apc, gen=n_var) != 0:
                return (sympy.LM(apc), terms)

            if "n" in str(apc):
                regex_cleaner = re.search(r'([0-9.]*\*\*n)', str(apc))
                if regex_cleaner:
                    apc = regex_cleaner.groups()[0]
            return(apc, terms)
        return(expr_with_abs, expr_with_abs)
