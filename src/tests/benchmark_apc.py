"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

import sys
sys.path.append("/app/code/")
sys.path.append("/app/code/metric")
from metric import path_complexity
from tests import unit_utils
from log import Log
from graph import GraphType


def apc_runtime(g_frac, f_frac, time):
    """Test the amount of time it takes to run APC analysis on different sized graphs."""
    log = Log()
    converter = path_complexity.PathComplexity(log)
    if g_frac == 0:
        unit_utils.run_benchmark(converter, GraphType.ADJACENCY_LIST, True)
    else:
        unit_utils.run_benchmark(converter, GraphType.ADJACENCY_LIST, True, g_frac, f_frac, time)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        apc_runtime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 2:
        if sys.argv[1] == "complete":
            apc_runtime(1, 1, 60)
    else:
        apc_runtime(50, 46, 120)
