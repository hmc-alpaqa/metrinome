"""The interface that all classes able to compute metrics should inherit from."""

from abc import ABC, abstractmethod
from typing import Any
from graph import Graph


class ConverterAbstract(ABC):
    """The interface that all CFG converters should follow."""

    @abstractmethod
    def __init__(self, logger) -> None:
        """Initialize a new object capable of converting code to a CFG."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of the current converter."""

    @abstractmethod
    def to_graph(self, filename: str, file_extension: str) -> Optional[Dict[str, Graph]]:
        """Given a graph, compute the metric."""
