import numpy as np
import re
from typing import List, Tuple

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
    def __str__(self) -> str:
        return f"Edges: {self.edgeRules()}\nVertices: {self.getVertices()} \nStart Node: {self.startNode} \nEnd Node: {self.endNode}"

    def __init__(self, edges, vertices: int, startNode: int, endNode: int) -> None:
        '''
        Create a directed graph from a vertex set, edge list,
        and start/end notes.

        If the graph is not weighted, the edgeList is 
        edgeList = [(a, b), (c, d), (e, f), ...]

        If the graph is weighted, the edgeList is 
        edgeList = [(a, b, weight), (c, d, weight), (e, f, weight), ...]

        '''
        self.edges = edges
        self.vertices = vertices
        self.startNode = startNode
        self.endNode = endNode
        self.weighted = False

    def edgeRules(self) -> List[Tuple[int, int]]:
        '''
        Obtain the edge list.
        '''
        return self.edges

    def vertexCount(self) -> int:
        '''
        Get the number of vertices in the graph.
        '''
        return len(self.vertices)

    def getVertices(self) -> List[int]:
        '''
        Get the vertex set for the graph.
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
        for edge in self.edgeRules(): 
            vertexOne = edge[0]
            vertexTwo = edge[1] 
            weight = 1 
            if self.weighted:
                weight = edge[2] 
            
            # Compute the correct index in the matrix 
            if vertexOne == self.endNode: 
                vertexOne = 1 
            elif vertexOne != 0:
                vertexOne += 1 
 
            if vertexTwo == self.endNode: 
                vertexTwo = 1 
            elif vertexTwo != 0:
                vertexTwo += 1 
            
            adjMat[vertexOne][vertexTwo] = weight

        return adjMat

    def adjacencyList(self): 
        adjacencyList = [[] for _ in range(self.vertexCount())]

        for edge in self.edgeRules(): 
            vertexOne = edge[0]
            vertexTwo = edge[1] 
            weight = 1
            if self.weighted:
                weight = edge[2]  

            adjacencyList[vertexOne].append((vertexTwo, weight))

        return adjacencyList      

    @staticmethod
    def fromFile(filename: str, weighted = False): 
        '''
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

        g = Graph(edges, vertices, startNode, endNode)
        g.weighted = weighted 
        return g 

    def toPrism(self):
        '''
        Assumes the graph is already in the DTMC correct representation (with 
        edge weights as probabilities).

        dtmc
        module die

        	// local state
        	s : [0..7] init 0;
        	// value of the die
        	d : [0..6] init 0;
            
        	[] s=0 -> 0.5 : (s'=1) + 0.5 : (s'=2);
        	[] s=1 -> 0.5 : (s'=3) + 0.5 : (s'=4);
        	[] s=2 -> 0.5 : (s'=5) + 0.5 : (s'=6);
        	[] s=3 -> 0.5 : (s'=1) + 0.5 : (s'=7) & (d'=1);
        	[] s=4 -> 0.5 : (s'=7) & (d'=2) + 0.5 : (s'=7) & (d'=3);
        	[] s=5 -> 0.5 : (s'=7) & (d'=4) + 0.5 : (s'=7) & (d'=5);
        	[] s=6 -> 0.5 : (s'=2) + 0.5 : (s'=7) & (d'=6);
        	[] s=7 -> (s'=7);
            
        endmodule
        '''
        if not self.weighted:
            raise ValueError("Graph is not a Discrete Time Markov Chain (no weights available).")
        
        prismLines = []

        # Add the header.
        prismLines.append('dtmc\n') # Discrete Time Markov Chain  
        prismLines.append('module test\n')

        # Create all of the nodes we'll use.
        prismLines.append(f'\ts: [0..{self.vertexCount()}] init {self.startNode}\n')

        adjList = self.adjacencyList() 
        for i in range(len(adjList)): 
            adjacencies = adjList[i]
            # We know that the vertex corresponds to the index 'i'.
            s = ' + '.join([f"{weight} : (s'={other})" for other, weight in adjList[i]])
            s += ';\n'
            prismLines.append(f'\t[] s={i} -> {s}') 

        # The terminal node should point to itself.
        prismLines.append(f"\t[] s={self.endNode} -> (s'={self.endNode});\n")

        # Add the footer.
        prismLines.append('endmodule')

        return prismLines