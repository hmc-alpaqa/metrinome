"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

from core.log import Log
from metric import npath_complexity
from tests import unit_utils
from graph.graph import GraphType


def npath_runtime(graph_type: GraphType, show_info: bool) -> None:
    """Test the amount of time it takes to run NPath analysis on different sized graphs."""
    converter = npath_complexity.NPathComplexity(Log())
    unit_utils.run_benchmark(converter, graph_type, show_info)


if __name__ == "__main__":
    npath_runtime(GraphType.EDGE_LIST, show_info=False)
