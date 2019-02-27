from pydot import Graph

def cyclomaticComplexity(g: Graph):
    return len(g.get_edge_list()) - len(g.get_nodes()) + 2