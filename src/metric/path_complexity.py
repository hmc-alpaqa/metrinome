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


PathComplexityRes = Tuple[Union[float, str], Union[float, str]]

class BaseCaseBFS:
    def __init__(self):
        pass

    def get(self, cfg: ControlFlowGraph, start_idx: int, end_idx: int):
        depth = 0
        base_cases = [0] * end_idx
        graph = cfg.graph.adjacency_list()
        q = deque([cfg.graph.start_node])
        while depth < end_idx:
            new_q = deque()
            while q:
                curr_node = q.pop()
                for next_node in graph[curr_node]:
                    new_q.appendleft(next_node)

                if curr_node == cfg.graph.end_node:
                    base_cases[depth] += 1

            if depth > 0:
                print("DEPTH: ", depth, end_idx)
                base_cases[depth] += base_cases[depth - 1]

            depth += 1
            q = new_q

        print("BASE CASES: ", base_cases[start_idx: end_idx])
        return base_cases[start_idx: end_idx]


class PathComplexity(metric.MetricAbstract):
    """Compute the path complexity and asymptotic path complexity metrics."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new instance of PathComplexity."""
        self.logger = logger
        self.base_case_getter = BaseCaseBFS()
        #self.base_case_getter = None

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

    def gen_func_taylor_coeffs(self, graph: AnyGraph) -> Tuple[List[Basic],
                                                               int,
                                                               int,
                                                               Basic]:
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

        recurrence_kernel = denominator.all_coeffs()[::-1]
        test = [round(-x, 2) for x in recurrence_kernel]
        roots = polyroots(test, maxsteps=250, extraprec=250)
        self.logger.d_msg(f"Getting {2 * dimension + 1} many coeffs.")
        if self.base_case_getter is None:
            taylor_coeffs = get_taylor_coeffs(generating_function, 2 * dimension + 1)
        else: 
            taylor_coeffs = []

        if taylor_coeffs is None:
            raise ValueError("Could not obtain taylor coefficients.")

        self.logger.d_msg(f"Got taylor coeffs: {taylor_coeffs}, len: {len(taylor_coeffs)}")

        return taylor_coeffs, dimension, degree(denominator, gen=t_var), roots

    # pylint: disable=too-many-locals
    def evaluate(self, cfg: ControlFlowGraph) -> PathComplexityRes:
        """
        Compute the path complexity given the CFG of some function.

        Return both the path complexity and the asymptotic path complexity.
        """
        taylor_coeffs, dimension, recurrence_degree, roots = self.gen_func_taylor_coeffs(cfg.graph)
        if taylor_coeffs is None:
            return (0.0, 0.0)

        if self.base_case_getter is None:
            base_cases = np.matrix(taylor_coeffs[dimension: dimension + recurrence_degree], dtype='complex')
        else:
            base_cases = np.matrix(self.base_case_getter.get(cfg, dimension, dimension + recurrence_degree))

        n_var = symbols('n')

        # Solve the recurrence relation.
        factors, simplified_factors = get_solution_from_roots(roots)
        matrix = np.matrix([[fact.replace(n_var, nval) for fact in factors] for nval in
                            range(dimension, dimension + recurrence_degree)],
                           dtype='complex')
        base_cases = base_cases.transpose()
        self.logger.d_msg("Got the base cases.")

        self.logger.d_msg(f"Matrix: {matrix.shape}")
        self.logger.d_msg(f"Base Cases: {base_cases}")
        self.logger.d_msg(f"Dimension: {dimension}")
        self.logger.d_msg(f"Recurrence Degree: {recurrence_degree}")

        bounding_solution_terms = np.linalg.lstsq(matrix, base_cases, rcond=None)[0]
        self.logger.d_msg("Got the bounding solution terms.")

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
                if degree(apc, gen=n_var) != 0:
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