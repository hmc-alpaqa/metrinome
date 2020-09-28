"""Graph object allows us to store an interact with Graphs in a variety of ways."""

from typing import List, Optional, DefaultDict, Set, \
    Match, TypeVar, Generic, Union, Dict, cast, Any
from enum import Enum
import re
import os
import collections
import numpy as np  # type: ignore


# ADJ LIST
AdjListType = List[List[int]]
WeightedAdjList = List[List[List[int]]]
AllAdjList = Union[WeightedAdjList, AdjListType]

# EDGE LIST
EdgeListType = List[List[int]]

# GRAPH TYPES
GraphEdgeType = TypeVar("GraphEdgeType", AllAdjList, EdgeListType)


class GraphType(Enum):
    """All of the different ways to represent the graph."""

    ADJACENCY_LIST = "list"
    ADJACENCY_MATRIX = "matrix"
    EDGE_LIST = "edge_list"


class Graph(Generic[GraphEdgeType]):
    """
    Store a directed graph using an adjacency list, edge list, or adjacency matrix.

    Since this is used to store Control Flow Graphs, we also store a start and end node.
    Each vertex is represented as a number, such that

    self.vertices = [0, 1, 2, 3, 4, ...]

    Each edge is represented as a list of two nodes, e.g.

    edge = [1, 2].
    """

    def __init__(self, edges: GraphEdgeType, vertices: List[int], start_node: int,
                 end_node: int,
                 graph_type: GraphType = GraphType.ADJACENCY_LIST) -> None:
        """
        Create a directed graph from a vertex set, edge list, and start/end notes.

        If the graph is not weighted, the edgeList is
        edgeList = [(a, b), (c, d), (e, f), ...]

        If the graph is weighted, the edgeList is
        edgeList = [(a, b, weight), (c, d, weight), (e, f, weight), ...]

        """
        self.edges: Any = edges
        self.vertices: List[int] = vertices
        self.start_node: int = start_node
        self.end_node: int = end_node
        self.weighted: bool = False
        self.name: Optional[str] = None
        self.graph_type = graph_type

    def dot(self) -> str:
        """Convert a Graph object to a .dot file."""
        out = "digraph {\n"
        for node in self.get_vertices():
            out += f"{node}"
            if node == self.start_node:
                out += " [label=\"START\"]"
            elif node == self.end_node:
                out += " [label=\"EXIT\"]"
            out += ";\n"

        if self.graph_type is GraphType.EDGE_LIST:
            for edge_pair in self.edge_rules():
                out += f"{edge_pair[0]} -> {edge_pair[1]};\n"
            out += "}"

        elif self.graph_type is GraphType.ADJACENCY_LIST:
            for vertex in range(self.vertex_count()):
                for vertex_two in self.edge_rules()[vertex]:
                    out += f"{vertex} -> {vertex_two};\n"
            out += "}"

        elif self.graph_type is GraphType.ADJACENCY_MATRIX:
            raise ValueError("Not yet implemented.")

        return out

    def __str__(self) -> str:
        """Return a string representation of the Graph."""
        return f"Edges: {self.edge_rules()}\nTotal Edges: " + \
               f"{len(self.edge_rules())}\nVertices: " + \
               f"{self.get_vertices()}\nStart Node: {self.start_node}" + \
               f"\nEnd Node: {self.end_node}"

    def set_name(self, name: str) -> None:
        """Set the name of the Graph."""
        self.name = name

    def get_parents(self) -> DefaultDict[int, List[int]]:
        """Create a dictionary which maps a node to a list of its parents."""
        if self.graph_type is not GraphType.ADJACENCY_LIST:
            raise NotImplementedError(f"Not possible for graph type {self.graph_type}")

        parents: DefaultDict[int, List[int]] = collections.defaultdict(list)
        for vertex in self.get_vertices():
            for child in self.edges[vertex]:
                parents[child] += [vertex]

        return parents

    def delete_nodes(self, removed_nodes: Set[int]) -> None:
        """
        Given a set of nodes to delete, update the graph.

        Note that this requires renaming nodes in the graph since the nodes are
        supposed to be in sequence (0, ..., n).
        """
        if self.graph_type is not GraphType.ADJACENCY_LIST:
            raise NotImplementedError(f"Not possible for graph type {self.graph_type}")

        # First, we have to figure out what each node will map to in the new graph.
        node_mapping: Dict[int, int] = dict()
        removed_count = 0
        for vertex in self.get_vertices():
            if vertex in removed_nodes:
                removed_count += 1
                continue

            node_mapping[vertex] = vertex - removed_count

        # Figure out what the new edges should be.
        new_edges: List[List[int]] = []
        for vertex in self.get_vertices():
            if vertex in removed_nodes:
                continue

            children = self.edges[vertex]
            if self.weighted:
                new_edge: List[int] = []
                for child in children:
                    child_node = child[0]
                    child_weight = child[1]
                    node_one: int = node_mapping[child_node]
                    new_edge = [node_one, child_weight]
                    new_edges.append(new_edge)
            else:
                new_edges += [[node_mapping[child] for child in children]]

        self.edges = new_edges
        self.start_node = node_mapping[self.start_node]
        self.end_node = node_mapping[self.end_node]

    def convert_to_weighted(self) -> None:
        """Turn a graph that is not weighted into a weighted one."""
        if self.weighted:
            raise ValueError("Already weighted.")

        if self.graph_type is not GraphType.ADJACENCY_LIST:
            raise NotImplementedError(f"Not possible for graph type {self.graph_type}")

        new_edges = []
        weight = 1
        for vertex in self.get_vertices():
            new_edges.append([[node, weight] for node in self.edges[vertex]])

        self.edges = new_edges
        self.weighted = True

    def simplify(self: 'Graph[AdjListType]') -> None:
        """Make the graph smaller."""
        parents = self.get_parents()
        self.convert_to_weighted()

        # Figure out which nodes we have to delete and update the edges.
        removed_vertices = set()
        for vertex in range(self.vertex_count()):
            if len(parents[vertex]) == 1 and len(self.edges[vertex]) == 1:
                parent = parents[vertex][0]
                child = self.edges[vertex][0]
                child_node = child[0]
                child_weight = child[1]

                # Find the correct edge from the parent
                child_of_parent = None
                for i, child_of_parent in enumerate(self.edges[parent]):
                    if child_of_parent[0] == vertex:
                        curr_vertex_of_parent = child_of_parent
                        break

                if child_of_parent[1] != child_weight:
                    print("ERROR! Incoming and outgoing weights should be the same!")

                # Add the child of the current node as a child of the parent with the same weight.
                # First, check if the parent already has the child of the current node as a child.
                found = False
                for i, child_of_parent in enumerate(self.edges[parent]):
                    if child_of_parent[0] == child_node:
                        self.edges[parent][i][1] += child_weight
                        found = True
                        break
                if not found:
                    self.edges[parent].append(child)

                # Remove child from current node.
                self.edges[vertex] = []

                # Remove current vertex from parent.
                self.edges[parent].remove(curr_vertex_of_parent)

                removed_vertices.add(vertex)

        self.delete_nodes(removed_vertices)

    def edge_rules(self) -> EdgeListType:
        """Obtain the edge list."""
        if self.graph_type is GraphType.ADJACENCY_LIST:
            edges: EdgeListType = []

            for vertex in range(len(self.edges)):
                for vertex_two in self.edges[vertex]:
                    if self.weighted:
                        edges.append([vertex, vertex_two[0], vertex_two[1]])
                    else:
                        edges.append([vertex, vertex_two])

            return edges

        if self.graph_type is GraphType.ADJACENCY_MATRIX:
            vertex_count = self.vertex_count()
            edge_list: EdgeListType = []
            for i in range(vertex_count):
                for j in range(vertex_count):
                    if self.weighted and self.edges[i, j] != 0:
                        edge_list.append([i, j, self.edges[i, j]])
                    elif self.edges[i, j] == 1:
                        edge_list.append([i, j])

            return edge_list

        return cast(EdgeListType, self.edges)

    def edge_count(self) -> int:
        """Get the number of edges in the graph."""
        if self.graph_type is GraphType.ADJACENCY_LIST:
            count = 0
            for vertex in range(len(self.edges)):
                count += len(self.edges[vertex])
            return count

        if self.graph_type is GraphType.ADJACENCY_MATRIX:
            return int(np.count_nonzero(self.edges))

        return len(self.edge_rules())

    def vertex_count(self) -> int:
        """Get the number of vertices in the graph."""
        if self.graph_type is GraphType.ADJACENCY_LIST:
            return len(self.edges)

        if self.graph_type is GraphType.ADJACENCY_MATRIX:
            return int(self.edges.shape[0])

        return len(self.vertices)

    def get_vertices(self) -> List[int]:
        """Get the vertex set for the graph."""
        if self.graph_type is GraphType.ADJACENCY_LIST or \
           self.graph_type is GraphType.ADJACENCY_MATRIX:
            return list(range(self.vertex_count()))

        return self.vertices

    def get_start(self) -> int:
        """Get the start node for the graph."""
        return self.start_node

    def get_end(self) -> int:
        """Get the node for the graph."""
        return self.end_node

    def adjacency_matrix(self) -> np.ndarray:
        """
        Obtain the adjacency matrix from the edge list representation.

        We assume the vertices are numbered consecutively, i.e.
            0, 1, 2, ..., end_node

        Due to the way the APC algorithm is implemented, the structure is:

        First  row  -> START
        Second row  -> END
        Other  rows -> n = 2, ..., END - 1
        """
        adj_mat = np.zeros((self.vertex_count(), self.vertex_count()), dtype=np.int8)
        if self.graph_type is GraphType.EDGE_LIST:
            for edge in self.edges:
                vertex_one = edge[0]
                vertex_two = edge[1]
                weight = 1
                if self.weighted:
                    weight = edge[2]

                # Compute the correct index in the matrix.
                vertex_one = self.node_to_index(vertex_one)
                vertex_two = self.node_to_index(vertex_two)
                adj_mat[vertex_one][vertex_two] = weight

            return adj_mat

        if self.graph_type is GraphType.ADJACENCY_LIST:
            for vertex in range(self.vertex_count()):
                vertex_one = self.node_to_index(vertex)
                for vertex_two in self.edges[vertex]:
                    if self.weighted:
                        weight = vertex_two[1]
                        vertex_two = vertex_two[0]
                    else:
                        weight = 1

                    vertex_two = self.node_to_index(vertex_two)
                    adj_mat[vertex_one][vertex_two] = weight

            return adj_mat

        return self.edges

    def adjacency_list(self) -> Union[AdjListType, WeightedAdjList]:
        """Compute the adjacency list for a Graph from its set of edges."""
        if self.graph_type is GraphType.ADJACENCY_LIST:
            return cast(AdjListType, self.edges)

        if self.graph_type is GraphType.EDGE_LIST:
            if self.weighted:
                v_e_dict: WeightedAdjList = [[] for _ in range(self.vertex_count())]
            else:
                v_e_dict_2: AdjListType = [[] for _ in range(self.vertex_count())]

            for edge in self.edge_rules():
                vertex_one = edge[0]
                vertex_two = edge[1]
                weight = 1
                if self.weighted:
                    weight = edge[2]
                    v_e_dict[vertex_one].append([vertex_two, weight])
                else:
                    v_e_dict_2[vertex_one].append(vertex_two)

            if self.weighted:
                return v_e_dict

            return v_e_dict_2

        if self.graph_type is GraphType.ADJACENCY_MATRIX:
            pass

        raise ValueError("Not yet implemented.")

    @staticmethod
    def from_file(filename: str, weighted: bool = False,
                  graph_type: GraphType = GraphType.ADJACENCY_LIST) -> 'AnyGraph':
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
        name = os.path.split(filename)[1]
        # Initialize graph based on type.
        if graph_type is GraphType.ADJACENCY_LIST:
            # v_e_dict: DefaultDict[int, Any] = defaultdict(set)
            # graph = Graph(v_e_dict, None, -1, -1, graph_type)
            graph = Graph(cast(AdjListType, []), [], -1, -1, graph_type)
        elif graph_type is GraphType.EDGE_LIST:
            edges: List[List[int]] = []
            graph = Graph(edges, [], -1, -1, graph_type)
        elif graph_type is GraphType.ADJACENCY_MATRIX:
            # We create the graph using an adjacency list and then convert it.
            # There is probably a better way to do this.
            graph = Graph([], [], -1, -1, GraphType.ADJACENCY_LIST)

        graph.set_name(os.path.splitext(name)[0])

        with open(filename, "r") as file:
            line: str
            for line in file.readlines()[1:]:
                if (match := re.search(r"([0-9]*)\s*->\s*([0-9]*)", line)) is not None:
                    # The current line in the text file represents an edge.
                    graph.update_with_edge(cast(Match[str], match))
                # Current line is not an edge - check if it defines a node.
                elif (match := re.search(r"([0-9]*)\s*\[label=\"(.*)\"\]", line)) is not None:
                    graph.update_with_node(cast(Match[str], match))

            if graph.start_node == -1 or graph.end_node == -1:
                raise ValueError("Start and end nodes must both be defined.")

            graph.weighted = weighted

        if graph_type is GraphType.ADJACENCY_MATRIX:
            graph.edges = graph.adjacency_matrix()
            graph.graph_type = GraphType.ADJACENCY_MATRIX

        return graph

    def node_to_index(self, node: int) -> int:
        """Find the index for the row or column of an adjacency matrix."""
        if node == self.start_node:
            return 0

        if node == self.end_node:
            return 1

        return node + 1

    def update_with_node(self, match: Match[str]) -> None:
        """Create a new vertex when the current line in the dot file is a node."""
        node = int(match.group(1))
        node_label = match.group(2)

        if node_label == "START":
            self.start_node = node
        elif node_label == "EXIT":
            self.end_node = node

        if self.graph_type is GraphType.EDGE_LIST:
            if node not in self.vertices:
                self.vertices.append(node)
        elif self.graph_type is GraphType.ADJACENCY_LIST:
            if len(self.edges) <= node:
                self.edges += [[] for _ in range(((node + 1) - len(self.edges)))]

    def update_with_edge(self, match: Match[str]) -> None:
        """Create new vertices and edges when the current line in the dot file is an edge."""
        node_one = int(match.group(1))
        node_two = int(match.group(2))
        if self.graph_type is GraphType.EDGE_LIST:
            if node_one not in self.vertices:
                self.vertices.append(node_one)
            if node_two not in self.vertices:
                self.vertices.append(node_two)
            self.edges.append([node_one, node_two])
        elif self.graph_type is GraphType.ADJACENCY_LIST:
            if len(self.edges) <= node_one:
                self.edges += [[] for _ in range(((node_one + 1) - len(self.edges)))]

            self.edges[node_one] += [node_two]

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

        adj_list: WeightedAdjList = cast(WeightedAdjList, self.adjacency_list())

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

    def __eq__(self, other: object) -> bool:
        """Check that two Graphs are equal by checking their vertices and edges."""
        if not isinstance(other, Graph):
            return False

        if self.graph_type != other.graph_type:
            raise ValueError("Graph types must be the same.")

        edges_equal = self.edges == other.edge_rules()
        vertices_equal = set(self.vertices) == set(other.get_vertices())
        labels_equal = (self.start_node == other.get_start() and self.end_node == other.get_end())
        return edges_equal and vertices_equal and labels_equal


# pylint: disable=E0601
AnyGraph = Union[Graph[AllAdjList], Graph[EdgeListType]]
