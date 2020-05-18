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


def apc_runtime(graph_type: GraphType):
    """Test the amount of time it takes to run APC analysis on different sized graphs."""
    log = Log()
    converter = path_complexity.PathComplexity(log)
    unit_utils.run_benchmark(converter, graph_type)


if __name__ == "__main__":
    apc_runtime(GraphType.EDGE_LIST)
