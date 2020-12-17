"""Computes Cyclomatic Complexity from any Graph object."""

# pylint: disable=W0235
# Disable 'useless super delegation of __init__' because
# this inherits from an abstract class.

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from metric import metric


class CyclomaticComplexity(metric.MetricAbstract):
    """Compute the Cyclomatic Complexity given some control flow graph."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Initialize an object used to compute the cyclomatic complexity of graphs."""
        self.logger = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Cyclomatic Complexity"

    def evaluate(self, cfg: ControlFlowGraph) -> int:
        """
        Compute the cyclomatic complexity of the function.

        The input graph is the CFG of some function.
        Refer to https://en.wikipedia.org/wiki/Cyclomatic_complexity.
        """
        return cfg.graph.edge_count() - cfg.graph.num_vertices + 2
