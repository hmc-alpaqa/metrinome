"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

import sys
sys.path.append("/app/code/")
sys.path.append("/app/code/metric")
from log import Log
from metric import npath_complexity
from tests import unit_utils
from graph import GraphType


def npath_runtime(graph_type, show_info: bool):
    """Test the amount of time it takes to run NPath analysis on different sized graphs."""
    log = Log()
    converter = npath_complexity.NPathComplexity(log)
    unit_utils.run_benchmark(converter, graph_type, show_info)


if __name__ == "__main__":
    npath_runtime(GraphType.EDGE_LIST, show_info=False)
    # npath_runtime(GraphType.ADJACENCY_LIST, show_info=False)
    # npath_runtime(GraphType.ADJACENCY_MATRIX, show_info=False)
