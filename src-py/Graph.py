import numpy as np 
import re 

class Graph:
    '''
    Store a directed graph using an adjacency list. Since 
    this is used to store Control Flow Graphs, we also store 
    a start and end node. 
    Each vertex is represented as a number, such that 
    
    self.vertices = [1, 2, 3, 4, 5, ...]
    
    Each edge is represented as a list of two nodes, e.g.

    edge = [1, 2]. 

    We store a list of these edges.
    '''
    def __str__(self):
        return f"Edges: {self.edgeRules()}\nVertices: {self.getVertices()} \nStart Node: {self.startNode} \nEnd Node: {self.endNode}" 

    def __init__(self, edges, vertices, startNode, endNode):
        '''
        Create a directed graph from a vertex set, edge list, 
        and start/end notes. 
        '''
        self.edges = edges
        self.vertices = vertices
        self.startNode = startNode
        self.endNode = endNode

    def edgeRules(self):
        '''
        Obtain the edge list
        '''
        return self.edges
    
    def vertexCount(self):
        '''
        Get the number of vertices in the graph  
        '''
        return len(self.vertices)

    def getVertices(self):
        '''
        Get the vertex set for the graph
        ''' 
        return self.vertices

    def adjacencyMatrix(self):
        '''
        Obtain the adjacency matrix from the edge list representation
        
        We assume the vertices are numbered consecutively, i.e. 
            0, 1, 2, ..., endNode
        
        Due to the way the APC algorithm is implemented, the structure is:

        First  row  -> START 
        Second row  -> END 
        Other  rows -> n = 2, ..., END - 1
        ''' 

        adjMat = np.zeros((self.endNode + 1, self.endNode + 1))
        for edgeOne, edgeTwo in self.edgeRules(): 
            if edgeOne == self.endNode: 
                edgeOne = 1 
            elif edgeOne != 0:
                edgeOne += 1 
 
            if edgeTwo == self.endNode: 
                edgeTwo = 1 
            elif edgeTwo != 0:
                edgeTwo += 1 
            
            adjMat[edgeOne][edgeTwo] = 1 

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
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines[1:]:
                match = re.search("([0-9]*)\s*->\s*([0-9]*)", line)
                if match is None:
                    # Current line is not an edge - check if it defines a node
                    match = re.search("([0-9]*)\s*\[label=\"(.*)\"\]", line)
                    if match is not None:
                        node = int(match.group(1))
                        nodeLabel = match.group(2) 
                        vertices.add(node)
                        if nodeLabel == "START":
                            startNode = node
                        elif nodeLabel == "EXIT":
                            endNode = node
                # The current line in the text file represents an edge 
                else:
                    nodeOne = int(match.group(1))
                    nodeTwo = int(match.group(2))
                    vertices.add(nodeOne)
                    vertices.add(nodeTwo)
                    edges.append([nodeOne, nodeTwo])

        if startNode is None or endNode is None:
            errMsg = "Start and end nodes must " \
                     "both be defined."
            raise ValueError(errMsg)

        return Graph(edges, vertices, startNode, endNode)