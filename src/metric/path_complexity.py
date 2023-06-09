"""Compute the path complexity and asymptotic path complexity metrics."""

import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union

import numpy as np  # type: ignore
import sympy  # type: ignore
from mpmath import mpc, mpf, polyroots  # type: ignore
from sympy import (Basic, Float, Matrix, Poly, degree, eye, preorder_traversal, simplify, symbols,
                   sympify)

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from graph.graph import Graph
from metric import metric
from utils import Timeout, big_o, get_solution_from_roots, get_taylor_coeffs

PathComplexityRes = tuple[Union[float, str], Union[float, str]]


class BaseCaseGetter(ABC):
    """Object capable of computing base cases for path complexity."""

    def __init__(self, logger: Log) -> None:
        """Initialize an object that gets solutions of path(n)."""
        self.logger = logger

    @abstractmethod
    def get(self, graph: Graph, x_mat: Basic, denominator: Basic,
            start_idx: int, num_coeffs: int) -> tuple[np.array, int]:
        """Get path(start_idx) throught path(start_idx + num_coeffs)."""


class BaseCaseBFS(BaseCaseGetter):
    """Get base cases using a breadth first search on the control flow graph."""

    def get(self, graph: Graph, x_mat: Basic, denominator: Basic,
            start_idx: int, num_coeffs: int) -> tuple[np.ndarray, int]:
        """Use a BFS to count all of the paths through the CFG up to a certain depth."""
        end_idx = start_idx + num_coeffs
        depth = 1
        base_cases = [0] * end_idx
        graph_adj = graph.adjacency_list()
        # Count how many paths of length 'depth' can reach each node.
        num_paths = defaultdict(int)
        num_paths[graph.start_node] = 1
        while depth < end_idx:
            # Compute how many paths of length 'depth + 1' can reach each node.
            new_num_paths: defaultdict[int, int] = defaultdict(int)
            for curr_node, curr_paths in num_paths.items():
                for next_node in graph_adj[curr_node]:
                    new_num_paths[next_node] += curr_paths

            # Check how many of these reach the end node.
            base_cases[depth] = new_num_paths[graph.end_node]
            if depth > 0:
                base_cases[depth] += base_cases[depth - 1]
            depth += 1
            num_paths = new_num_paths
        print(f"base cases: {base_cases}")
        all_paths = np.array(base_cases[start_idx: end_idx], dtype="float64")
        print(f"all paths{all_paths}")
        print(f"start_index:{start_idx}")

        return np.array(base_cases[start_idx: end_idx], dtype="float64"), start_idx


class BaseCaseTaylor(BaseCaseGetter):
    """Get base cases using the generating function; significantly slower than BFS."""

    def get(self, graph: Graph, x_mat: Basic, denominator: Basic,
            start_idx: int, num_coeffs: int) -> tuple[np.array, int]:
        """Use taylor coefficients of the generating function to get base cases."""
        print(f"printing graph...{graph}")
        x_sub = x_mat.copy()
        print(x_sub)
        x_sub.col_del(0)
        x_sub.row_del(1)
        print(f"denominator ...{denominator}")
        print(x_sub.det(method="det_LU"))
        generating_function = x_sub.det(method="det_LU") / denominator
        print(f"printing generating function...{generating_function}")
        self.logger.d_msg(f"Getting {num_coeffs} many coeffs.")

        taylor_coeffs, new_start_idx = get_taylor_coeffs(generating_function,
                                                         num_coeffs, num_coeffs)

        if taylor_coeffs is None:
            raise ValueError("Could not obtain taylor coefficients.")
        if new_start_idx is None:
            new_start_idx = 1
        self.logger.d_msg(f"Got taylor coeffs: {taylor_coeffs}, len: {len(taylor_coeffs)}")

        new_start_idx = new_start_idx if new_start_idx is not None else start_idx
        return np.array(taylor_coeffs[new_start_idx: new_start_idx + num_coeffs],
                        dtype='float64'), new_start_idx


class BaseCaseSmart(BaseCaseGetter):
    """Dispatches call to optimal BaseCaseGetter for the given input."""

    def __init__(self, logger: Log):
        """Create a new instance of BaseCaseSmart."""
        self.base_case_bfs = BaseCaseBFS(logger)
        self.base_case_taylor = BaseCaseTaylor(logger)
        super().__init__(logger)

    def get(self, graph: Graph, x_mat: Basic, denominator: Basic,
            start_idx: int, num_coeffs: int) -> tuple[np.array, int]:
        """Try to use BFS and switch to Taylor method if it takes too long."""
        try:
            with Timeout(seconds=10, error_message="BFS Timed Out"):
                return self.base_case_bfs.get(graph, x_mat, denominator, start_idx, num_coeffs)

        except TimeoutError:
            self.logger.d_msg("BFS timed out, using taylor coeff method")
            return self.base_case_taylor.get(graph, x_mat, denominator, start_idx, num_coeffs)

        except Exception:  # pylint: disable=broad-except
            self.logger.d_msg("BFS Failed, trying taylor coeff method")
            return self.base_case_taylor.get(graph, x_mat, denominator, start_idx, num_coeffs)


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

    def get_matrix(self, graph: Graph) -> tuple[Basic, int]:
        """Use the CFG to obtain the taylor series from the generating function."""
        adj_mat = graph.adjacency_matrix()
        adj_mat[1][1] = 1
        new_adjacency = Matrix(adj_mat)

        dimension = adj_mat.shape[0]
        x_mat = eye(dimension) - new_adjacency * self._t_var
        self.logger.d_msg(f"Matrix shape: {x_mat.shape}")

        return x_mat, dimension

    def get_roots(self, x_mat: Basic) -> tuple[int, Poly, list[Union[mpf, mpc]]]:
        """Get the denominator of the generating function and its roots/degree."""
        x_det = x_mat.det()
        denominator = Poly(sympify(-x_det))
        print(f"denominator: {denominator}")
        recurrence_kernel = denominator.all_coeffs()[::-1]
        print(f"recurrence_kernel:{recurrence_kernel}")
        # Doing round(x,2) breaks the code. Not sure why, but the roots for 
        # eq = 0 and -eq = 0 are the same.
        test = [round(-x, 2) for x in recurrence_kernel]
        print(f"test: {test}")
        # test are the coefficients of the denominator of the gen. function from
        # the smallest exponent to the largest. polyroots expects the coefficients
        # from largest to smallest. however, the roots for a polynomial with flipped
        # polynomials is 1/roots of the nonflipped polynomial.
        roots = polyroots(test, maxsteps=250, extraprec=250)
        print(f"print roots: {roots}")
        return degree(denominator, gen=self._t_var), denominator, roots

    # pylint: disable=too-many-locals
    def evaluate(self, cfg: ControlFlowGraph) -> PathComplexityRes:
        """
        Compute the path complexity given the CFG of some function.
        Return both the path complexity and the asymptotic path complexity.
        """
        edge_list = cfg.graph.edge_rules()
        print(f"edge_list:{edge_list}")
        x_mat, dimension = self.get_matrix(cfg.graph)
        print(f"printing matrix..{x_mat}")
        recurrence_degree, denominator, roots = self.get_roots(x_mat)

        base_cases, start_idx = self.base_case_getter.get(cfg.graph, x_mat, denominator,
                                                          dimension, recurrence_degree)

        base_cases = base_cases.transpose()
        # Solve the recurrence relation.
        factors, simplified_factors = get_solution_from_roots(roots)

        self.logger.d_msg(f"Simplified Factors: {simplified_factors}")

        # Creates "matrix" of size recurence_degree (number of roots from denominator) then
        # plug in n values for all unsimplified solutions (factors)
        matrix = np.array([[fact.replace(self._n_var, nval) for fact in factors] for nval in
                          range(start_idx, start_idx + recurrence_degree)],
                          dtype='complex')

        self.logger.d_msg(f"Matrix: {matrix.shape}")
        # Base cases are the terms in the Taylor Series that we will use to compute
        # the closed form.
        self.logger.d_msg(f"Base Cases: {base_cases}, dimension: {dimension}")
        self.logger.d_msg(f"Recurrence Degree: {recurrence_degree}")

        #TODO: Understand why it i not a problem if the rows are not linearly 
        #independent or if they are always linearly independent (check documentation
        #for np.linalg.lstsq)
        # matrix = np.array([[1+2j,3-4j,5+6j,1+2j,3-4j],
        #                     [1+2j,3-4j,5+6j,1+2j,3-4j],
        #                     [1+2j,3-4j,5+6j,1+2j,3-4j],
        #                     [1+2j,3-4j,5+6j,1+2j,3-4j],
        #                     [1+2j,3-4j,5+6j,1+2j,3-4j]])

        # Finds coefficients for closed form equation (the Cs)
        print(f"matrix...{matrix}")
        print(f"liner algebra...{np.linalg.lstsq(matrix, base_cases, rcond=None)}")
        bound_sol_terms = np.linalg.lstsq(matrix, base_cases, rcond=None)[0]

        #TODO: absolute gives a upper bound on path(n), we can use clean function in r_path_complexity and fc_path_complexity 
        # if we want better path(n) that doesn't make -3 becomes +3
        bound_sol_terms = np.absolute(bound_sol_terms)
        self.logger.d_msg(f"Coeffs: {bound_sol_terms}")

        # bound_sol_terms is actually path(n) because we are doing the dot product 
        # between the coefficiencts (the Cs) and the simplified solutions
        bound_sol_terms = bound_sol_terms.transpose().dot(Matrix(simplified_factors))[0]

        self.logger.d_msg(f"bounding_solution_terms: {bound_sol_terms}")

        unrounded_expr = simplify(sympify(bound_sol_terms))
        expr_with_abs = unrounded_expr
        for expr_term in preorder_traversal(unrounded_expr):
            if isinstance(expr_term, Float):
                expr_with_abs = expr_with_abs.subs(expr_term, round(expr_term, 4))

        self.logger.d_msg(f"exp terms: {expr_with_abs}")
        exp_terms_list = list(expr_with_abs.args)
        self.logger.d_msg(f"exp terms is: {exp_terms_list}")
        apc = big_o(exp_terms_list)
        self.logger.d_msg(f"APC is {apc}")

        exp_terms_list = sympify(exp_terms_list)
        terms = str(sum(exp_terms_list))
        if apc not in (0.0, "0"):
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
