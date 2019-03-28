import numpy as np 
import re 

class Graph(object):
    def __init__(self, edges, vertices, startNode, endNode):
        self.edges = edges
        self.vertices = vertices
        self.startNode = startNode
        self.endNode = endNode

    def edgeRules(self):
        return self.edges
    
    def vertexCount(self):
        return len(self.vertices)

    def getVertices(self): 
        return self.vertices

    def adjacencyMatrix(self): 
        adjMat = np.zeros((self.endNode + 1, self.endNode + 1))

        # Output the matrix in the same format as the mathematica code...
        # First row = START 
        # Second row = END 
        # Third, n = 2, ..., END - 1

        for edge_one, edge_two in self.edgeRules(): 
            if edge_one == 0: 
                edge_one = 0 
            elif edge_one == self.endNode: 
                edge_one = 1 
            else:
                edge_one += 1 

            if edge_two == 0: 
                edge_two = 0 
            elif edge_two == self.endNode: 
                edge_two = 1 
            else:
                edge_two += 1 


            adjMat[edge_one][edge_two] = 1 

        return adjMat

    @staticmethod
    def fromFile(filename):
        '''
        Returns a Graph object from a .dot file of format

        digraph {
            0 [label="START"]
            2 [label="EXIT"]
            a_i -> a_j
            ...
            a_k  -> a_m
        }
        Returns a Graph object from a .dot file of format

        digraph {
            0 [label="START"]
            2 [label="EXIT"]
            a_i -> a_j
            ...
            a_k  -> a_m
        }
        '''
        edges = []
        vertices = set()
        startNode = None 
        endNode = None 
        ".*->.*" # all of the edges 
        ".*\[label.*\]" # all of the nodes 
        with open(filename, "r") as f:
            for line in f.readlines()[1:]:
                match = re.search("([0-9]*)\s*->\s*([0-9]*)", line)
                if match is None:
                    match = re.search("([0-9]*)\s*\[label=\"(.*)\"\]", line)
                    if match is not None:
                        node = int(match.group(1))
                        node_label = match.group(2) 
                        vertices.add(node)
                        if node_label == "START":
                            startNode = node
                        elif node_label == "EXIT":
                            endNode = node
                else:
                    node1 = int(match.group(1))
                    node2 = int(match.group(2))
                    vertices.add(node1)
                    vertices.add(node2)
                    edges.append([node1, node2])

        return Graph(edges, vertices, startNode, endNode)