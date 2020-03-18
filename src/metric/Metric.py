from abc import ABC, abstractmethod
from Graph import Graph

class Metric(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, g: Graph):
        pass
