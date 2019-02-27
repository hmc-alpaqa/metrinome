from Graph import Graph

def cyclomaticComplexity(g: Graph):
    return len(g.edgeRules()) - g.vertexCount() + 2