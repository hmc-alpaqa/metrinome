"""Graph object allows us to store an interact with Graphs in a variety of ways."""

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Generic, Match, Optional, TypeVar

import numpy as np  # type: ignore

AdjListType = list[list[int]]
EdgeListType = list[list[int]]
Type = TypeVar('Type')


# Pylint has trouble understanding the inheritance pattern used in this module.
# pylint: disable=super-init-not-called
# pylint: disable=non-parent-init-called
# pylint: disable=no-member
# pylint: disable=attribute-defined-outside-init
# pylint: disable=access-member-before-definition


class Graph(ABC):
    """
    Store a directed graph using an adjacency list, edge list, or adjacency matrix.

    Since this is used to store Control Flow Graphs, we also store a start and end node.
    Each vertex is represented as a non-negative integer, such that the set of all vertices
    form a list of contiguous natural numbers: [0, 1, 2, ..., n - 1].
    """

    def __init__(self, num_vertices: int):
        """Create a new instance of the graph."""
        self.start_node: int = 0
        self.end_node: int = num_vertices - 1
        self.num_vertices = num_vertices
        self.name: Optional[str] = None

    @abstractmethod
    def vertices(self) -> list[int]:
        """Get the vertex set for the graph."""

    @abstractmethod
    def node_to_index(self, node: int) -> int:
        """Find the index for the row or column of an adjacency matrix."""

    def __str__(self) -> str:
        """Return a string representation of the Graph."""
        return f"Edges: {self.edge_rules()}\nTotal Edges: " + \
               f"{len(self.edge_rules())}\nVertices: " + \
               f"{self.vertices()}\nStart Node: {self.start_node}" + \
               f"\nEnd Node: {self.end_node}"

    @abstractmethod
    def adjacency_matrix(self) -> np.ndarray:
        """
        Obtain the adjacency matrix represnetation of the graph.

        We assume the vertices are numbered consecutively, i.e.
            0, 1, 2, ..., end_node

        Due to the way the APC algorithm is implemented, the structure is:

        First  row  -> START
        Second row  -> END
        Other  rows -> n = 2, ..., END - 1
        """

    @abstractmethod
    def edge_rules(self) -> EdgeListType:
        """Obtain a list of edges, where each each is [node1, node2]."""

    @abstractmethod
    def adjacency_list(self) -> AdjListType:
        """Compute the adjacency list representation of a graph."""

    @abstractmethod
    def dot(self) -> str:
        """Convert a Graph object to a .dot file."""

    @abstractmethod
    def edge_count(self) -> int:
        """Get the number of edges in the graph."""

    @abstractmethod
    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        """
        Create a new vertex when the current line in the dot file is a node.

        Note that if there are 'n' nodes in the graph and node 'n + k' needs to be
        created as a result of a call to this function, nodes
        'n + 1', ..., 'n + k - 1' will also be created.
        """

    @abstractmethod
    def update_with_edge(self, match: Match[str]) -> None:
        """
        Create new edges when the current line in the dot file is an edge.

        Note that this will throw an error if one of the vertices in the edge has not
        been created yet.
        """

    @abstractmethod
    def rich_repr(self) -> list[str]:
        """Returns a list of rows that can be used to construct a table representation in Rich."""


class GenericGraph(Graph, Generic[Type], ABC):
    """A concrete implementation of the Graph interface that graphs can inherit from."""

    def __init__(self, edges: Type, num_vertices: int):
        """
        Create a directed graph from a vertex set, edge list, and start/end notes.

        If the graph is not weighted, the edgeList is
        edgeList = [(a, b), (c, d), (e, f), ...]

        If the graph is weighted, the edgeList is
        edgeList = [(a, b, weight), (c, d, weight), (e, f, weight), ...]
        """
        self.edges: Type = edges
        super().__init__(num_vertices)

    def __eq__(self, other: object) -> bool:
        """Check that two Graphs are equal by checking the graph type, vertices, and edges."""
        if not isinstance(other, GenericGraph):
            return False

        if self.__class__ is not other.__class__:
            return False

        edges_equal = self.edges == other.edges
        vertices_equal = self.num_vertices == other.num_vertices
        labels_equal = (self.start_node == other.start_node and self.end_node == other.end_node)
        return edges_equal and vertices_equal and labels_equal

    def vertices(self) -> list[int]:
        """Get a list of vertices in the graph."""
        return list(range(self.num_vertices))

    def node_to_index(self, node: int) -> int:
        """Find the index for the row or column of an adjacency matrix."""
        if node == self.start_node:
            return 0

        if node == self.end_node:
            return 1

        return node + 1

    def _update_with_node_helper(self, match: Match[str], node_label: bool) -> int:
        """Store start and end nodes."""
        node = int(match.group(1))
        if node_label:
            label = match.group(2)
            if "START" in label:
                self.start_node = node
            if label == "EXIT":
                self.end_node = node

        self.num_vertices = max(self.num_vertices, node + 1)
        return node

    def _update_with_edge_helper(self, match: Match[str]) -> tuple[int, int]:
        """Save edges from dot file."""
        node_one = int(match.group(1))
        node_two = int(match.group(2))
        # Ensure that vertices have already been created.
        if max(node_one, node_two) + 1 > self.num_vertices:
            raise ValueError("Cannot create new nodes in update_with_edge.")
        return node_one, node_two

    def _initialize_dot_file(self) -> str:
        """Create standard format dot file template."""
        out = "digraph {\n"
        for node in self.vertices():
            out += f"{node}"
            if node == self.start_node:
                out += " [label=\"START\"]"
            elif node == self.end_node:
                out += " [label=\"EXIT\"]"
            out += ";\n"

        return out

    def rich_repr(self) -> list[list[[str]]]:
        """Returns a list of rows that can be used to construct a table representation in Rich."""
        return [
            ["Edges", str(self.edge_rules())],
            ["Total Edges", str(self.edge_count())],
            ["Vertices", str(self.vertices())],
            ["Start Node", str(self.start_node)],
            ["End Node", str(self.end_node)]
        ]


class AdjListGraph(GenericGraph[AdjListType], Graph):
    """An adjacency list representation of a graph."""

    def __init__(self, edges: AdjListType, num_vertices: int):
        """Create a new graph from an adjacency list."""
        self.weights: Optional[list[list[int]]] = None
        GenericGraph.__init__(self, edges, num_vertices)

    def dot(self) -> str:
        """Generate a dot file representation of the graph."""
        out = self._initialize_dot_file()
        for vertex in range(self.num_vertices):
            for vertex_two in self.edge_rules()[vertex]:
                out += f"{vertex} -> {vertex_two};\n"
        out += "}"
        return out

    def edge_rules(self) -> EdgeListType:
        """Obtain a list of edges (ignoring weights), where each each is [node1, node2]."""
        edges: EdgeListType = []

        for vertex in range(len(self.edges)):
            for vertex_two in self.edges[vertex]:
                edges.append([vertex, vertex_two])

        return edges

    def edge_count(self) -> int:
        """Count the number of edges in the graph."""
        return sum(map(len, self.edges))

    def get_parents(self) -> defaultdict[int, list[int]]:
        """Create a dictionary which maps a node to a list of its parents."""
        parents: defaultdict[int, list[int]] = defaultdict(list)
        for vertex in self.vertices():
            for child in self.edges[vertex]:
                parents[child] += [vertex]

        return parents

    def simplify(self) -> None:
        """Make the graph smaller."""
        parents = self.get_parents()
        self.convert_to_weighted()
        if self.weights is None:
            raise ValueError("Cannot simplify non-weighted graph.")

        # Figure out which nodes we have to delete and update the edges.
        removed_vertices = set()
        for vertex in range(self.num_vertices):
            if len(parents[vertex]) == 1 and len(self.edges[vertex]) == 1:
                parent = parents[vertex][0]
                child_node = self.edges[vertex][0]
                child_weight = None

                # Find the correct edge from the parent
                child_of_parent = None
                for child_of_parent in self.edges[parent]:
                    if child_of_parent == vertex:
                        curr_vertex_of_parent = child_of_parent
                        weight_from_parent = None
                        break

                if weight_from_parent != child_weight:
                    print("ERROR! Incoming and outgoing weights should be the same!")

                # Add the child of the current node as a child of the parent with the same weight.
                # First, check if the parent already has the child of the current node as a child.
                found = False
                for child_of_parent in self.edges[parent]:
                    if child_of_parent == child_node:
                        # Increment weight
                        found = True
                        break
                if not found:
                    self.edges[parent].append(child_node)

                # Remove child from current node.
                self.edges[vertex] = []

                # Remove current vertex from parent.
                self.edges[parent].remove(curr_vertex_of_parent)

                removed_vertices.add(vertex)

        self._delete_nodes(removed_vertices)

    def convert_to_weighted(self) -> None:
        """Turn a graph that is not weighted into a weighted one."""
        if self.weights is not None:
            raise ValueError("Already weighted.")

        weights = []
        for vertex in self.vertices():
            weights.append([1] * len(self.edges[vertex]))

        self.weights = weights

    def _delete_nodes(self, removed_nodes: set[int]) -> None:
        """
        Given a set of nodes to delete, update the graph.

        Note that this requires renaming nodes in the graph since the nodes are
        supposed to be in sequence (0, ..., n).
        """
        # First, we have to figure out what each node will map to in the new graph.
        node_mapping: dict[int, int] = dict()
        removed_count = 0
        for vertex in self.vertices():
            if vertex in removed_nodes:
                removed_count += 1
                continue

            node_mapping[vertex] = vertex - removed_count

        # Figure out what the new edges should be.
        new_edges: list[list[int]] = []
        for vertex in self.vertices():
            if vertex in removed_nodes:
                continue

            children = self.edges[vertex]
            new_edges += [[node_mapping[child] for child in children]]

        self.edges = new_edges
        self.start_node = node_mapping[self.start_node]
        self.end_node = node_mapping[self.end_node]

    def adjacency_matrix(self) -> np.ndarray:
        """Obtain the adjacency matrix representation of the graph, ignoring weights."""
        adj_mat = np.zeros((self.num_vertices, self.num_vertices), dtype=np.int8)
        for vertex in range(self.num_vertices):
            vertex_one = self.node_to_index(vertex)
            for vertex_two in self.edges[vertex]:
                vertex_two = self.node_to_index(vertex_two)
                adj_mat[vertex_one][vertex_two] = 1

        return adj_mat

    def adjacency_list(self) -> AdjListType:
        """Compute the adjacency list representation of a graph."""
        return self.edges

    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        """Create a new vertex when the current line in the dot file is a node."""
        node = self._update_with_node_helper(match, node_label)
        if len(self.edges) <= node:
            self.edges += [[] for _ in range(((node + 1) - len(self.edges)))]

    def update_with_edge(self, match: Match[str]) -> None:
        """Create new edges when the current line in the dot file is an edge."""
        node_one, node_two = self._update_with_edge_helper(match)
        if len(self.edges) <= node_one:
            self.edges += [[] for _ in range(((node_one + 1) - len(self.edges)))]

        self.edges[node_one] += [node_two]

    def to_prism(self) -> list[str]:
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
        if self.weights is None:
            raise ValueError("Graph is not a Discrete Time Markov Chain (no weights available).")

        prism_lines = []

        # Add the header.
        prism_lines.append('dtmc\n')  # Discrete Time Markov Chain
        prism_lines.append('module test\n')

        # Create all of the nodes we'll use.
        prism_lines.append(f'\ts: [0..{self.num_vertices}] init {self.start_node}\n')

        adj_list = self.adjacency_list()

        for i, neighbors in enumerate(adj_list):
            # We know that the vertex corresponds to the index 'i'.
            prism_line = ' + '.join(
                [f"{self.weights[i][j]} : (s'={neighbor})" for j, neighbor in enumerate(neighbors)]
            )
            prism_line += ';\n'
            prism_lines.append(f'\t[] s={i} -> {prism_line}')

        # The terminal node should point to itself.
        prism_lines.append(f"\t[] s={self.end_node} -> (s'={self.end_node});\n")

        # Add the footer.
        prism_lines.append('endmodule')

        return prism_lines


class EdgeListGraph(GenericGraph[EdgeListType], Graph):
    """An edge list representation of a graph."""

    def __init__(self, edges: EdgeListType, num_vertices: int):
        """Create a new graph from a list of edges."""
        self.weights: Optional[list[int]] = None
        GenericGraph.__init__(self, edges, num_vertices)

    def dot(self) -> str:
        """Generate a dot file representation of the graph."""
        out = self._initialize_dot_file()
        for edge_pair in self.edge_rules():
            out += f"{edge_pair[0]} -> {edge_pair[1]};\n"
        out += "}"
        return out

    def edge_count(self) -> int:
        """Get the number of edges in the graph."""
        return len(self.edges)

    def edge_rules(self) -> EdgeListType:
        """Obtain a list of edges, where each each is [node1, node2]."""
        return self.edges

    def adjacency_matrix(self) -> np.ndarray:
        """Obtain the adjacency matrix represnetation of the graph."""
        adj_mat = np.zeros((self.num_vertices, self.num_vertices), dtype=np.int8)
        for edge in self.edges:
            vertex_one = edge[0]
            vertex_two = edge[1]
            weight = 1
            if self.weights is not None:
                weight = edge[2]

            # Compute the correct index in the matrix.
            vertex_one = self.node_to_index(vertex_one)
            vertex_two = self.node_to_index(vertex_two)
            adj_mat[vertex_one][vertex_two] = weight

        return adj_mat

    def adjacency_list(self) -> AdjListType:
        """Compute the adjacency list representation of a graph ignoring weights."""
        v_e_dict: AdjListType = [[] for _ in self.vertices()]

        for vertex_one, vertex_two in self.edge_rules():
            v_e_dict[vertex_one].append(vertex_two)

        return v_e_dict

    def update_with_edge(self, match: Match[str]) -> None:
        """Create new edges when the current line in the dot file is an edge."""
        node_one, node_two = self._update_with_edge_helper(match)
        self.edges.append([node_one, node_two])

    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        """Create a new vertex when the current line in the dot file is a node."""
        self._update_with_node_helper(match, node_label)


class AdjMatGraph(GenericGraph[np.ndarray], Graph):
    """An adjacency matrix representation of a graph."""

    def __init__(self, adj_mat: np.ndarray, num_vertices: int):
        """Create a new graph from an adjacency matrix."""
        self.weighted: bool = False
        GenericGraph.__init__(self, adj_mat, num_vertices)

    def edge_count(self) -> int:
        """Get the number of edges in the graph."""
        return int(np.count_nonzero(self.edges))

    def edge_rules(self) -> EdgeListType:
        """Obtain a list of edges, where each each is [node1, node2]."""
        edge_list: EdgeListType = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.weighted and self.edges[i, j] != 0:
                    edge_list.append([i, j, self.edges[i, j]])
                elif self.edges[i, j] == 1:
                    edge_list.append([i, j])

        return edge_list

    def adjacency_matrix(self) -> np.ndarray:
        """Obtain the adjacency matrix represnetation of the graph."""
        return self.edges

    def adjacency_list(self) -> AdjListType:
        """Compute the adjacency list representation of a graph."""

    def dot(self) -> str:
        """Generate a dot file representation of the graph."""

    def update_with_edge(self, match: Match[str]) -> None:
        """Create new edges when the current line in the dot file is an edge."""

    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        """Create a new vertex when the current line in the dot file is a node."""
