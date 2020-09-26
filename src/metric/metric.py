"""The interface that all classes able to compute metrics should inherit from."""

from abc import ABC, abstractmethod
from typing import Union, Tuple
from control_flow_graph import ControlFlowGraph
from log import Log


PathComplexityRes = Tuple[Union[float, str], Union[float, str]]


class MetricAbstract(ABC):
    """The interface that all metric computers should follow."""

    @abstractmethod
    def __init__(self, logger: Log) -> None:
        """Initialize a new object capable of computing a metric."""

    @abstractmethod
    def name(self) -> str:
        """Obtain the name of the metric that we are computing."""

    @abstractmethod
    def evaluate(self, cfg: ControlFlowGraph) -> Union[int, PathComplexityRes]:
        """Given a graph, compute the metric."""
