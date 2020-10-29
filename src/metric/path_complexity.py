"""Compute the path complexity and asymptotic path complexity metrics."""

from collections import deque
from typing import Tuple, List, Union
import re
import sympy  # type: ignore
from sympy import refine, preorder_traversal, Float, Matrix, eye, symbols, degree, Poly, \
    simplify, sympify, Abs, Q, Basic
from mpmath import polyroots  # type: ignore
import numpy as np  # type: ignore
from utils import big_o, get_taylor_coeffs, get_solution_from_roots
from graph import AnyGraph
from control_flow_graph import ControlFlowGraph
from metric import metric
from log import Log
from abc import ABC, abstractmethod

PathComplexityRes = Tuple[Union[float, str], Union[float, str]]

class BaseCaseGetter():
    """Object capable of computing base cases for path complexity."""

    @abstractmethod
    def __init__(self, logger: Log) -> None:
        """Initialize an object that gets solutions of path(n)."""
        self.logger = logger

    @abstractmethod
    def get(self, cfg: ControlFlowGraph, start_idx: int, end_idx: int) -> List[int]:
        """Get path(start_idx) throught path(end_idx)."""
        pass

class BaseCaseBFS(BaseCaseGetter):
    """Get base cases using a breadth first search on the control flow graph."""

    def get(self, graph: AnyGraph, x_mat: Basic, denominator: Basic,
            start_idx: int, end_idx: int) -> List[int]:
        """Use a BFS to count all of the paths through the CFG up to a certain depth."""
        depth = 0
        base_cases = [0] * end_idx
        graph_adj = graph.adjacency_list()
        q = deque([graph.start_node])
        while depth < end_idx:
            new_q = deque()
            while q:
                curr_node = q.pop()
                for next_node in graph_adj[curr_node]:
                    new_q.appendleft(next_node)

                if curr_node == graph.end_node:
                    base_cases[depth] += 1

            if depth > 0:
                base_cases[depth] += base_cases[depth - 1]

            depth += 1
            q = new_q

        return np.matrix(base_cases[start_idx: end_idx], dtype="complex")

class BaseCaseTaylor(BaseCaseGetter):
    """Get base cases using the generating function; significantly slower than BFS."""
    
    def get(self, graph: AnyGraph, x_mat: Basic, denominator: Basic,
            start_idx: int, end_idx: int) -> List[int]:
        """Use taylor coefficients of the generating function to get base cases."""
        x_sub = x_mat.copy()
        x_sub.col_del(0)
        x_sub.row_del(1)
        generating_function = x_sub.det(method="det_LU") / denominator 
        self.logger.d_msg(f"Getting {end_idx} many coeffs.")

        taylor_coeffs = get_taylor_coeffs(generating_function, end_idx)
    
        if taylor_coeffs is None:
            raise ValueError("Could not obtain taylor coefficients.")
        self.logger.d_msg(f"Got taylor coeffs: {taylor_coeffs}, len: {len(taylor_coeffs)}")

        return np.matrix(taylor_coeffs[start_idx: end_idx], dtype='complex')


class PathComplexity(metric.MetricAbstract):
    """Compute the path complexity and asymptotic path complexity metrics."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new instance of PathComplexity."""
        self.logger = logger
        self.base_case_getter = BaseCaseBFS(logger)

        self._t_var = symbols('t')
        self._n_var = symbols('n')

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Path Complexity"

    def faddeev_leverrier(self, adj_mat: np.array) -> np.array:
        """Use the Faddeev-Leverrier algorithm to find coefficients of characteristic poly."""
        dimension = adj_mat.shape[0]
        coefs = np.array([1.])  # coeffs starting from highest degree
        matrix = np.array(adj_mat, dtype="float64")
        for k in range(1, dimension + 1):
            tot = -matrix.trace() / k
            coefs = np.append(coefs, tot)
            matrix += np.diag(np.repeat(tot, dimension))
            matrix = np.dot(adj_mat, matrix)
        return coefs[::-1]

    def get_det_from_char_coefs(self, coefs: np.array, dimension: int) -> Basic:
        """Get determinant from coefs of char. poly and the size of the matrix."""
        terms = []
        for i, coef in enumerate(coefs):
            terms.append(f"{coef} * t**{i}")
        poly = sympify(" + ".join(terms).replace("t", "(1/t)"))
        det = simplify(poly * sympify(f"t**{dimension}"))
        return det

    def get_matrix(self, graph: AnyGraph) -> Tuple[List[Basic],
                                                               int,
                                                               int,
                                                               Basic]:
        """Use the CFG to obtain the taylor series from the generating function."""
        adj_mat = graph.adjacency_matrix()
        adj_mat[1][1] = 1
        new_adjacency = Matrix(adj_mat)

        
        dimension = adj_mat.shape[0]
        x_mat = eye(dimension) - new_adjacency * self._t_var
        self.logger.d_msg(f"Matrix shape: {x_mat.shape}")

        return x_mat, dimension

    def get_roots(self, x_mat):
        x_det = x_mat.det()
        denominator = Poly(sympify(-x_det))
        recurrence_kernel = denominator.all_coeffs()[::-1]
        test = [round(-x, 2) for x in recurrence_kernel]
        roots = polyroots(test, maxsteps=250, extraprec=250)    

        return degree(denominator, gen=self._t_var), denominator, roots

    # pylint: disable=too-many-locals
    def evaluate(self, cfg: ControlFlowGraph) -> PathComplexityRes:
        """
        Compute the path complexity given the CFG of some function.

        Return both the path complexity and the asymptotic path complexity.
        """
        x_mat, dimension = self.get_matrix(cfg.graph)
        recurrence_degree, denominator, roots = self.get_roots(x_mat)

        base_cases = self.base_case_getter.get(cfg.graph, x_mat, denominator, dimension, dimension + recurrence_degree)
        base_cases = base_cases.transpose()
        # Solve the recurrence relation.
        factors, simplified_factors = get_solution_from_roots(roots)
        matrix = np.matrix([[fact.replace(self._n_var, nval) for fact in factors] for nval in
                            range(dimension, dimension + recurrence_degree)],
                           dtype='complex')

        self.logger.d_msg(f"Matrix: {matrix.shape}")
        self.logger.d_msg(f"Base Cases: {base_cases}, dimension: {dimension}")
        self.logger.d_msg(f"Recurrence Degree: {recurrence_degree}")

        bounding_solution_terms = np.linalg.lstsq(matrix, base_cases, rcond=None)[0]
        bounding_solution_terms = bounding_solution_terms.transpose().dot(Matrix(simplified_factors))[0, 0]

        self.logger.d_msg(f"bounding_solution_terms: {bounding_solution_terms}")

        unrounded_expr = simplify(sympify(bounding_solution_terms))
        expr_with_abs = unrounded_expr
        for expr_term in preorder_traversal(unrounded_expr):
            if isinstance(expr_term, Float):
                expr_with_abs = expr_with_abs.subs(expr_term, round(expr_term, 4))

        self.logger.d_msg(f"exp terms: {expr_with_abs}")

        exp_terms = [simplify(arg) for arg in expr_with_abs.args]

        self.logger.d_msg(f"exp terms is: {exp_terms}")

        apc = big_o(exp_terms)

        self.logger.d_msg(f"APC is {apc}")

        exp_terms_list = (*exp_terms, )
        exp_terms_list = sympify(exp_terms_list)
        terms = str(sum(exp_terms_list))
        if apc not in (0.0, "0"):
            self.logger.d_msg("APC is not 0")
            try:
                if degree(apc, gen=self._n_var) != 0:
                    return (sympy.LM(apc), terms)
            except sympy.polys.polyerrors.PolynomialError:
                self.logger.d_msg("APC is not a polynomial.")
                # degree returns an error if apc is not a polynomial.
                if "n" in str(apc):
                    self.logger.d_msg("n is in apc")
                    regex_cleaner = re.search(r'([0-9.]*\*\*n)', str(apc))
                    if regex_cleaner:
                        self.logger.d_msg("regex_cleaner is true")
                        apc = regex_cleaner.groups()[0]
                        self.logger.d_msg(f"apc is: {apc}")

                return (apc, terms)

        return (expr_with_abs, expr_with_abs)
