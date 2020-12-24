"""Graph object allows us to store an interact with Graphs in a variety of ways."""

import collections
from abc import ABC, abstractmethod
from enum import Enum
from typing import (Any, DefaultDict, Dict, Generic, List, Match, Optional,
                    Set, Tuple, TypeVar, Union, cast)

import numpy as np  # type: ignore

# ADJ LIST
AdjListType = List[List[int]]
WeightedAdjList = List[List[List[int]]]
AllAdjList = Union[WeightedAdjList, AdjListType]

# EDGE LIST
EdgeListType = List[List[int]]


class BaseGraph(ABC):
    """
    Store a directed graph using an adjacency list, edge list, or adjacency matrix.

    Since this is used to store Control Flow Graphs, we also store a start and end node.
    Each vertex is represented as a non-negative integer, such that the set of all vertices
    form a list of contiguous natural numbers: [0, 1, 2, ..., n - 1].

    Each edge is represented as a list of two nodes, e.g.

    edge = [1, 2].
    """

    def __init__(self, num_vertices: int):
        """
        Create a directed graph from a vertex set, edge list, and start/end notes.

        If the graph is not weighted, the edgeList is
        edgeList = [(a, b), (c, d), (e, f), ...]

        If the graph is weighted, the edgeList is
        edgeList = [(a, b, weight), (c, d, weight), (e, f, weight), ...]

        """
        self.num_vertices: int = num_vertices
        self.start_node: int = 0
        self.end_node: int = num_vertices - 1
        self.weighted: bool = False
        self.name: Optional[str] = None
        self.calls: Dict[int, str] = {}

    def set_name(self, name: str) -> None:
        """Set the name of the Graph."""
        self.name = name

    def vertices(self) -> List[int]:
        """Get the vertex set for the graph."""
        return list(range(self.num_vertices))

    def node_to_index(self, node: int) -> int:
        """Find the index for the row or column of an adjacency matrix."""
        if node == self.start_node:
            return 0

        if node == self.end_node:
            return 1

        return node + 1

    def __str__(self) -> str:
        """Return a string representation of the Graph."""
        return f"Edges: {self.edge_rules()}\nTotal Edges: " + \
               f"{len(self.edge_rules())}\nVertices: " + \
               f"{self.vertices()}\nStart Node: {self.start_node}" + \
               f"\nEnd Node: {self.end_node}"

    def __eq__(self, other: object) -> bool:
        """Check that two Graphs are equal by checking their vertices and edges."""
        if not isinstance(other, BaseGraph):
            return False

        if self.graph_type != other.graph_type:
            raise ValueError("Graph types must be the same.")

        edges_equal = self.edges == other.edge_rules()
        vertices_equal = self.num_vertices == other.num_vertices
        labels_equal = (self.start_node == other.start_node and self.end_node == other.end_node)
        return edges_equal and vertices_equal and labels_equal

    def _initialize_dot_file(self) -> str:
        out = "digraph {\n"
        for node in self.vertices():
            out += f"{node}"
            if node == self.start_node:
                out += " [label=\"START\"]"
            elif node == self.end_node:
                out += " [label=\"EXIT\"]"
            out += ";\n"

        return out

    @abstractmethod
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
        pass

    @abstractmethod
    def edge_rules(self) -> EdgeListType:
        pass

    @abstractmethod
    def adjacency_list(self) -> Union[AdjListType, WeightedAdjList]:
        """Compute the adjacency list for a Graph from its set of edges."""
        pass

    @abstractmethod
    def dot(self) -> str:
        """Convert a Graph object to a .dot file."""
        pass

    @abstractmethod
    def edge_count(self) -> int:
        """Get the number of edges in the graph."""
        pass

    @abstractmethod
    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        """
        Create a new vertex when the current line in the dot file is a node.

        Note that if there are 'n' nodes in the graph and node 'n + k' needs to be
        created as a result of a call to this function, nodes
        'n + 1', ..., 'n + k - 1' will also be created.
        """

    def _update_with_node_helper(self, match: Match[str], node_label: bool) -> int:
        node = int(match.group(1))
        if node_label:
            label = match.group(2)
            if "CALLS" in label:
                self.calls[node] = label
        if "START" in label:
            self.start_node = node
        if label == "EXIT":
            self.end_node = node

        self.num_vertices = max(self.num_vertices, node + 1)
        return node

    @abstractmethod
    def update_with_edge(self, match: Match[str]) -> None:
        """
        Create new edges when the current line in the dot file is an edge.

        Note that this will throw an error if one of the vertices in the edge has not
        been created yet.
        """

    def _update_with_edge_helper(self, match: Match[str]) -> Tuple[int, int]:
        node_one = int(match.group(1))
        node_two = int(match.group(2))
        # Ensure that vertices have already been created.
        if max(node_one, node_two) + 1 > self.num_vertices:
            raise ValueError("Cannot create new nodes in update_with_edge.")
        return node_one, node_two


class AdjListGraph(BaseGraph):
    def __init__(self, adj_list: AdjListType, num_vertices: int):
        self._adj_list = adj_list
        super().__init__(num_vertices)

    def dot(self) -> str:
        out = self._initialize_dot_file()
        for vertex in range(self.num_vertices):
            for vertex_two in self.edge_rules()[vertex]:
                out += f"{vertex} -> {vertex_two};\n"
        out += "}"
        return out

    def edge_rules(self) -> EdgeListType:
        edges: EdgeListType = []

        for vertex in range(len(self._adj_list)):
            for vertex_two in self._adj_list[vertex]:
                if self.weighted:
                    edges.append([vertex, vertex_two[0], vertex_two[1]])
                else:
                    edges.append([vertex, vertex_two])

        return edges

    def edge_count(self) -> int:
        count = 0
        for vertex in range(len(self._adj_list)):
            count += len(self._adj_list[vertex])
        return count

    def get_parents(self) -> DefaultDict[int, List[int]]:
        """Create a dictionary which maps a node to a list of its parents."""
        parents: DefaultDict[int, List[int]] = collections.defaultdict(list)
        for vertex in self.vertices():
            for child in self._adj_list[vertex]:
                parents[child] += [vertex]

        return parents

    def simplify(self) -> None:
        """Make the graph smaller."""
        parents = self.get_parents()
        self.convert_to_weighted()

        # Figure out which nodes we have to delete and update the edges.
        removed_vertices = set()
        for vertex in range(self.num_vertices):
            if len(parents[vertex]) == 1 and len(self._adj_list[vertex]) == 1:
                parent = parents[vertex][0]
                child = self._adj_list[vertex][0]
                child_node = child[0]
                child_weight = child[1]

                # Find the correct edge from the parent
                child_of_parent = None
                for i, child_of_parent in enumerate(self._adj_list[parent]):
                    if child_of_parent[0] == vertex:
                        curr_vertex_of_parent = child_of_parent
                        break

                if child_of_parent[1] != child_weight:
                    print("ERROR! Incoming and outgoing weights should be the same!")

                # Add the child of the current node as a child of the parent with the same weight.
                # First, check if the parent already has the child of the current node as a child.
                found = False
                for i, child_of_parent in enumerate(self._adj_list[parent]):
                    if child_of_parent[0] == child_node:
                        self._adj_list[parent][i][1] += child_weight
                        found = True
                        break
                if not found:
                    self._adj_list[parent].append(child)

                # Remove child from current node.
                self._adj_list[vertex] = []

                # Remove current vertex from parent.
                self._adj_list[parent].remove(curr_vertex_of_parent)

                removed_vertices.add(vertex)

        self._delete_nodes(removed_vertices)

    def convert_to_weighted(self) -> None:
        """Turn a graph that is not weighted into a weighted one."""
        if self.weighted:
            raise ValueError("Already weighted.")

        new_edges = []
        weight = 1
        for vertex in self.vertices():
            new_edges.append([[node, weight] for node in self._adj_list[vertex]])

        self._adj_list = new_edges
        self.weighted = True

    def _delete_nodes(self, removed_nodes: Set[int]) -> None:
        """
        Given a set of nodes to delete, update the graph.

        Note that this requires renaming nodes in the graph since the nodes are
        supposed to be in sequence (0, ..., n).
        """
        # First, we have to figure out what each node will map to in the new graph.
        node_mapping: Dict[int, int] = dict()
        removed_count = 0
        for vertex in self.vertices():
            if vertex in removed_nodes:
                removed_count += 1
                continue

            node_mapping[vertex] = vertex - removed_count

        # Figure out what the new edges should be.
        new_edges: List[List[int]] = []
        for vertex in self.vertices():
            if vertex in removed_nodes:
                continue

            children = self._adj_list[vertex]
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

        self._adj_list = new_edges
        self.start_node = node_mapping[self.start_node]
        self.end_node = node_mapping[self.end_node]

    def adjacency_matrix(self) -> np.ndarray:
        adj_mat = np.zeros((self.num_vertices, self.num_vertices), dtype=np.int8)
        for vertex in range(self.num_vertices):
            vertex_one = self.node_to_index(vertex)
            for vertex_two in self._adj_list[vertex]:
                if self.weighted:
                    weight = vertex_two[1]
                    vertex_two = vertex_two[0]
                else:
                    weight = 1

                vertex_two = self.node_to_index(vertex_two)
                adj_mat[vertex_one][vertex_two] = weight

        return adj_mat

    def adjacency_list(self) -> Union[AdjListType, WeightedAdjList]:
        return self._adj_list

    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        node = self._update_with_node_helper(match, node_label)
        if len(self._adj_list) <= node:
            self._adj_list += [[] for _ in range(((node + 1) - len(self._adj_list)))]

    def update_with_edge(self, match: Match[str]) -> None:
        node_one, node_two = self._update_with_edge_helper(match)
        if len(self._adj_list) <= node_one:
            self._adj_list += [[] for _ in range(((node_one + 1) - len(self._adj_list)))]

        self._adj_list[node_one] += [node_two]

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
        prism_lines.append(f'\ts: [0..{self.num_vertices}] init {self.start_node}\n')

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


class EdgeListGraph(BaseGraph):
    def __init__(self, edges: EdgeListType, num_vertices: int):
        self._edge_list: EdgeListType = edges
        super().__init__(num_vertices)

    def dot(self) -> str:
        out = self._initialize_dot_file()
        for edge_pair in self.edge_rules():
            out += f"{edge_pair[0]} -> {edge_pair[1]};\n"
        out += "}"
        return out

    def edge_count(self) -> int:
        return len(self._edge_list)

    def edge_rules(self) -> EdgeListType:
        return self._edge_list

    def adjacency_matrix(self) -> np.ndarray:
        adj_mat = np.zeros((self.num_vertices, self.num_vertices), dtype=np.int8)
        for edge in self._edge_list:
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

    def adjacency_list(self) -> Union[AdjListType, WeightedAdjList]:
        if self.weighted:
            v_e_dict: WeightedAdjList = [[] for _ in range(self.num_vertices)]
        else:
            v_e_dict_2: AdjListType = [[] for _ in range(self.num_vertices)]

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

    def update_with_edge(self, match: Match[str]) -> None:
        node_one, node_two = self._update_with_edge_helper(match)
        self._edge_list.append([node_one, node_two])

    def update_with_node(self, match: Match[str], node_label: bool) -> None:
        self._update_with_node_helper(match)


class AdjMatGraph(BaseGraph):
    def __init__(self, adj_mat: np.ndarray, num_vertices: int):
        self._adj_mat: np.ndarray = adj_mat
        super().__init__(num_vertices)

    def edge_count(self) -> int:
        return int(np.count_nonzero(self._adj_mat))

    def edge_rules(self) -> EdgeListType:
        edge_list: EdgeListType = []
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.weighted and self._adj_mat[i, j] != 0:
                    edge_list.append([i, j, self._adj_mat[i, j]])
                elif self._adj_mat[i, j] == 1:
                    edge_list.append([i, j])

        return edge_list

    def adjacency_matrix(self) -> np.ndarray:
        return self._adj_mat

    def adjacency_list(self) -> Union[AdjListType, WeightedAdjList]:
        # TODO
        pass

    def dot(self) -> str:
        # TODO
        pass
