"""Graph object allows us to store an interact with Graphs in a variety of ways."""

from collections import defaultdict
from typing import List, Tuple, Any, DefaultDict
import re
import numpy as np  # type: ignore


class Graph:
    """
    Store a directed graph using an adjacency list.

    Since this is used to store Control Flow Graphs, we also store a start and end node.
    Each vertex is represented as a number, such that

    self.vertices = [1, 2, 3, 4, 5, ...]

    Each edge is represented as a list of two nodes, e.g.

    edge = [1, 2].

    We store a list of these edges.
    """

    def dot(self, using_list: bool) -> str:
        """Convert a Graph object to a .dot file."""
        out = "digraph {\n"
        for node in self.get_vertices():
            out += f"{node}"
            if node == self.start_node:
                out += " [label=\"START\"]"
            elif node == self.end_node:
                out += " [label=\"EXIT\"]"
            out += ";\n"
        if using_list:
            for edge_pair in self.edge_rules():
                out += f"{edge_pair[0]} -> {edge_pair[1]};\n"
            out += "}"
        else:
            out += '0'
        return out

    def __str__(self) -> str:
        """Return a string representation of the Graph."""
        return f"Edges: {self.edge_rules()}\nVertices: " + \
               f"{self.get_vertices()}\nStart Node: {self.start_node}" + \
               f"\nEnd Node: {self.end_node}"

    def __init__(self, edges, vertices: Any, start_node: int,
                 end_node: int, from_list: bool = False) -> None:
        """
        Create a directed graph from a vertex set, edge list, and start/end notes.

        If the graph is not weighted, the edgeList is
        edgeList = [(a, b), (c, d), (e, f), ...]

        If the graph is weighted, the edgeList is
        edgeList = [(a, b, weight), (c, d, weight), (e, f, weight), ...]

        """
        self.edges = edges
        self.vertices = vertices
        self.start_node = start_node
        self.end_node = end_node
        self.weighted = False

        self.from_list = from_list

    def edge_rules(self) -> List[Tuple[int, int]]:
        """Obtain the edge list (ADD CHANGES IF edge dictionary)."""
        return self.edges

    def vertex_count(self) -> int:
        """Get the number of vertices in the graph (ADD CHANGES IF vertex-edge dictionary)."""
        return len(self.vertices)

    def get_vertices(self) -> List[int]:
        """Get the vertex set for the graph."""
        return self.vertices

    def get_start(self) -> int:
        """Get the start node for the graph."""
        return self.start_node

    def get_end(self) -> int:
        """Get the exit node for the graph."""
        return self.end_node

    def adjacency_matrix(self):
        """
        Obtain the adjacency matrix from the edge list representation.

        We assume the vertices are numbered consecutively, i.e.
            0, 1, 2, ..., end_node

        Due to the way the APC algorithm is implemented, the structure is:

        First  row  -> START
        Second row  -> END
        Other  rows -> n = 2, ..., END - 1
        """
        adj_mat = np.zeros((self.end_node + 1, self.end_node + 1))
        for edge in self.edge_rules():
            vertex_one = edge[0]
            vertex_two = edge[1]
            weight = 1
            if self.weighted:
                weight = edge[2]

            # Compute the correct index in the matrix
            if vertex_one == self.end_node:
                vertex_one = 1
            elif vertex_one != 0:
                vertex_one += 1

            if vertex_two == self.end_node:
                vertex_two = 1
            elif vertex_two != 0:
                vertex_two += 1

            adj_mat[vertex_one][vertex_two] = weight

        return adj_mat

    def adjacency_list(self):
        """Compute the adjacency list for a Graph from its set of edges."""
        adjacency_list = [[] for _ in range(self.vertex_count())]

        for edge in self.edge_rules():
            vertex_one = edge[0]
            vertex_two = edge[1]
            weight = 1
            if self.weighted:
                weight = edge[2]

            adjacency_list[vertex_one].append((vertex_two, weight))

        return adjacency_list

    @staticmethod
    def from_file(filename: str, weighted: bool = False, using_list: bool = True):
        """
        Return a Graph object from a .dot file of format.

        digraph {
            0 [label="START"]
            2 [label="EXIT"]
            a_i -> a_j
            ...
            a_k  -> a_m
        }
        """
        start_node = None
        end_node = None

        if using_list:
            edges = []
            vertices = set()
        else:
            v_e_dict: DefaultDict[int, Any] = defaultdict(set)

        with open(filename, "r") as file:
            for line in file.readlines()[1:]:
                match = re.search(r"([0-9]*)\s*->\s*([0-9]*)", line)
                if match is None:
                    # Current line is not an edge - check if it defines a node
                    match = re.search(r"([0-9]*)\s*\[label=\"(.*)\"\]", line)
                    if match is not None:
                        node = int(match.group(1))
                        node_label = match.group(2)
                    
                        if node_label == "START":
                            start_node = node
                        elif node_label == "EXIT":
                            end_node = node

                        if using_list:
                            vertices.add(node)

                # The current line in the text file represents an edge
                else:
                    node_one = int(match.group(1))
                    node_two = int(match.group(2))
                    if using_list:
                        vertices.add(node_one)
                        vertices.add(node_two)
                        edges.append([node_one, node_two])
                    else:
                        v_e_dict[node_one].add(node_two)


            if start_node is None or end_node is None:
                raise ValueError("Start and end nodes must \
                                 both be defined.")

            if using_list:
                graph = Graph(edges, vertices, start_node, end_node, using_list)
            else:
                graph = Graph(v_e_dict, v_e_dict.keys(), start_node, end_node, using_list)
            graph.weighted = weighted

        return graph

    def to_prism(self) -> List[str]:
        """
        Create a PRISM file based on an existing Graph.

        Assumes the graph is already in the DTMC correct representation (with
        edge weights as probabilities).

        e.g.:
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
        """
        if not self.weighted:
            raise ValueError("Graph is not a Discrete Time Markov Chain (no weights available).")

        prism_lines = []

        # Add the header.
        prism_lines.append('dtmc\n')  # Discrete Time Markov Chain
        prism_lines.append('module test\n')

        # Create all of the nodes we'll use.
        prism_lines.append(f'\ts: [0..{self.vertex_count()}] init {self.start_node}\n')

        adj_list = self.adjacency_list()
        for i in range(len(adj_list)):
            # We know that the vertex corresponds to the index 'i'.
            prism_line = ' + '.join([f"{weight} : (s'={other})" for other, weight in adj_list[i]])
            prism_line += ';\n'
            prism_lines.append(f'\t[] s={i} -> {prism_line}')

        # The terminal node should point to itself.
        prism_lines.append(f"\t[] s={self.end_node} -> (s'={self.end_node});\n")

        # Add the footer.
        prism_lines.append('endmodule')

        return prism_lines

    def __eq__(self, other) -> bool:
        """Check that two Graphs are equal by checking their vertices and edges."""
        sets_equal = (self.edges == other.edge_rules() and self.vertices == other.get_vertices())
        labels_equal = (self.start_node == other.get_start() and self.end_node == other.get_end())
        return sets_equal and labels_equal
