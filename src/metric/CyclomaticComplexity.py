from Graph import Graph
from metric import Metric # type: ignore

class CyclomaticComplexity(Metric.Metric):
    '''
    CyclomaticComplexity allows us to compute the Cyclomatic Complexity
    given some control flow graph.
    '''

    def __init__(self) -> None:
        '''
        Initialize an object used to compute the cyclomatic complexity of graphs
        '''
        pass

    def name(self) -> str:
        '''
        Returns the name of the metric computed by this class.
        '''
        return "Cyclomatic Complexity"

    def evaluate(self, g: Graph):
        '''
        Assuming that G represents the CFG of a function,
        computes the cyclomatic complexity of the function

        Refer to https://en.wikipedia.org/wiki/Cyclomatic_complexity
        '''
        return len(g.edgeRules()) - g.vertexCount() + 2
