"""
Computes Cyclomatic Complexity from any fraph object.
"""

# pylint: disable=W0235
# Disable 'useless super delegation of __init__' because
# this inherits from an abstract class.

from graph import Graph
from metric import metric  # type: ignore


class CyclomaticComplexity(metric.MetricAbstract):
    """
    Compute the Cyclomatic Complexity given some control flow graph.
    """

    def __init__(self) -> None:
        """Initialize an object used to compute the cyclomatic complexity of graphs."""
        super(CyclomaticComplexity, self).__init__()

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Cyclomatic Complexity"

    def evaluate(self, graph: Graph):
        """
        Assuming that G represents the CFG of a function,
        computes the cyclomatic complexity of the function

        Refer to https://en.wikipedia.org/wiki/Cyclomatic_complexity
        """
        return len(graph.edge_rules()) - graph.vertex_count() + 2
