"""
This module contains the interface that all classes able to compute metrics should
inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any
from graph import Graph


class MetricAbstract(ABC):
    """The interface that all metric computers should follow."""
    @abstractmethod
    def __init__(self) -> None:
        """Initialize a new object capable of computing a metric."""

    @abstractmethod
    def name(self) -> str:
        """Obtain the name of the metric that we are computing."""

    @abstractmethod
    def evaluate(self, graph: Graph) -> Any:
        """Given a graph, compute the metric."""
