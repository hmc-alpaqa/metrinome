"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

from typing import Type

from core.log import Log
from graph.graph import EdgeListGraph, Graph
from metric import npath_complexity
from tests.unit_utils import Benchmark


def npath_runtime(graph_type: Type[Graph], show_info: bool) -> None:
    """Test the amount of time it takes to run NPath analysis on different sized graphs."""
    log = Log()
    converter = npath_complexity.NPathComplexity(log)
    benchmark = Benchmark(log, show_info)
    benchmark.run_benchmark(converter, graph_type)


if __name__ == "__main__":
    npath_runtime(EdgeListGraph, show_info=False)
