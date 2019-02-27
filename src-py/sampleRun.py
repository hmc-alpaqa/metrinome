from Graph import Graph
from pathComplexity import pathComplexity

if __name__ == "__main__":
    filename = "vlab_cs_ucsb_test_ShimpleExample_test3_0_basic.dot"

    g = Graph.fromFile(filename)
    pc = pathComplexity(g)
