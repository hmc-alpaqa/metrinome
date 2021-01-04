"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

import sys

from core.log import Log
from graph.graph import AdjListGraph
from metric import path_complexity
from tests.unit_utils import Benchmark


def apc_runtime(g_frac: int, f_frac: int, time: int) -> None:
    """Test the amount of time it takes to run APC analysis on different sized graphs."""
    log = Log()
    converter = path_complexity.PathComplexity(log)
    benchmark = Benchmark(log, True)
    if g_frac == 0:
        benchmark.run_benchmark(converter, AdjListGraph)
    else:
        benchmark.run_benchmark(converter, AdjListGraph, g_frac, f_frac, time)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        apc_runtime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 2:
        if sys.argv[1] == "complete":
            apc_runtime(1, 1, 60)
    else:
        apc_runtime(12, 46, 120)
