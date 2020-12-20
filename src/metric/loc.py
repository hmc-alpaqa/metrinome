"""
Computes NPathComplexity for a given Graph object.

This works with both the adjacency list representation and edge list.
"""

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from metric import metric


class LinesOfCode(metric.MetricAbstract):
    """LoC allows us to compute the lines of code of functions from their CFGs."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new NPathComplexity to compute LoC for CFGs."""
        self.log = logger

    def name(self) -> str:
        """Return the name of the metric computed by this class."""
        return "Lines of Code"

    def evaluate(self, cfg: ControlFlowGraph) -> int:
        """Compute the number of lines of code of a function given its CFG."""
        if cfg.metadata is None:
            raise ValueError("Invalid cfg type.")

        return cfg.metadata.loc
