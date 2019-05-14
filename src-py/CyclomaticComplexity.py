from Graph import Graph 

def cyclomaticComplexity(g: Graph):
    '''
    Assuming that G represents the CFG of a function (as explained in Graph.py),
    computes the cyclomatic complexity of the function

    Refer to https://en.wikipedia.org/wiki/Cyclomatic_complexity
    ''' 
    return len(g.edgeRules()) - g.vertexCount() + 2