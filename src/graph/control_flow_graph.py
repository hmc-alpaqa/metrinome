"""All information that needs to be stored aside from the graph to compute complexity metrics."""
from __future__ import annotations

import os
import re
from typing import Callable, Match, Optional, Tuple, Type, cast
import itertools

from core.env import KnownExtensions
from graph.graph import AdjListGraph, AdjListType, AdjMatGraph, EdgeListGraph, Graph
from utils import calls_function

Option = Callable[['Metadata'], None]


# pylint: disable=dangerous-default-value


class Metadata:
    """Store metadata associated with a CFG."""

    def __init__(self, *options: Option):
        """Create a new metadata object."""
        self.loc: Optional[int] = None
        self.calls: Optional[dict[int, str]] = None
        self.language: Optional[KnownExtensions] = None

        for opt in options:
            opt(self)

    def __str__(self) -> str:
        """Return metadata as string."""
        out = ""
        if self.loc is not None:
            out += f"Lines of code: {self.loc} "
        if self.calls is not None:
            out += f"Calls: {self.calls}"
        return out

    def rich_repr(self) -> list[list[str]]:
        """Return a list of rows that can be used to represent the graph in Rich."""
        return [["Metadata", self.__str__()]]

    @staticmethod
    def with_loc(loc: int) -> Option:
        """Set number of lines of code in metadata."""
        def option(metadata: Metadata) -> None:
            """Apply the option."""
            metadata.loc = loc
        return option

    @staticmethod
    def with_calls(calls: dict[int, str]) -> Option:
        """Initialize calls in a Metadata instance."""
        def option(metadata: Metadata) -> None:
            """Apply the option."""
            metadata.calls = calls
        return option

    @staticmethod
    def with_language(language: KnownExtensions) -> Option:
        """Set the language that was used to create the CFG."""
        def option(metadata: Metadata) -> None:
            """Apply the option."""
            metadata.language = language
        return option


class ControlFlowGraph:
    """
    ControlFlowGraph objects are wrappers for Graphs that contain additional metadata.

    This allow us to compute a more diverse set of complexity metrics without adding
    metadata to the Graph class.
    """

    def __init__(self, graph: Graph, metadata: Metadata = Metadata()):
        """Create a new CFG from any Graph object."""
        self.graph = graph
        self.name = graph.name
        self.metadata = metadata

    def __eq__(self, other: object) -> bool:
        """Check for equality of graphs and metadata."""
        if isinstance(other, Graph):
            return self.graph == other

        if isinstance(other, ControlFlowGraph):
            return self.graph == other.graph and self.name == other.name

        return False

    def __str__(self) -> str:
        """Return string representation of the CFG."""
        if self.metadata is not None:
            return str(self.metadata) + "\n" + str(self.graph)

        return str(self.graph)

    def rich_repr(self) -> list[list[str]]:
        """Return a list of rows that can be used to represent the graph in Rich."""
        return self.metadata.rich_repr() + self.graph.rich_repr()

    @staticmethod
    def check_call(matches) -> Optional[dict[int, str]]:
        """Find and return any functions called on a node."""
        first_match = next(matches)
        node = int(first_match.group(1))
        matches = itertools.chain([first_match], matches)
        for match in matches:
            label = match.group(3)
        # there is the possibility of multiple labels (i.e. calls, start, exit)
        # if any call label occurs, return that (& ignore other labels)
            if "CALLS" in label:
                return {node: label}
        return None

    @staticmethod
    def from_file(filename: str, graph_type: Type[Graph] = AdjListGraph,
                  options: list[Option] = []) -> ControlFlowGraph:
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

        # ATTEMPT TO INSERT JOERN"S MODIFIED DOT FILE IN METRINOME
        # if filename == "/app/code/tmp_dot/even_odd_f2f_cfg.is_even.dot":
        #     name = os.path.split('/app/code/experiments/java/isevenisodd-python-cfgs/1-cfg_modified.dot')[1]
        #     print("!!!!!!!!Changed the dot file!!!!!!!")
        # print("THE FILENAME", filename)
        name = os.path.split(filename)[1]
        calls = {}
        # Initialize graph based on type.
        graph: Graph
        if graph_type is AdjListGraph:
            graph = AdjListGraph(cast(AdjListType, []), 0)
        elif graph_type is EdgeListGraph:
            edges: list[list[int]] = []
            graph = EdgeListGraph(edges, 0)
        elif graph_type is AdjMatGraph:
            # We create the graph using an adjacency list and then convert it.
            # There is probably a better way to do this.
            graph = AdjListGraph([], 0)

        graph.name = os.path.splitext(name)[0]
        with open(filename, "r") as file:
            line: str
            for line in file.readlines()[1:]:

                edge_regex = r"([0-9]*)\s*->\s*([0-9]*)"
                # node_with_label_regex = r"([0-9]*)\s*\[label=\"(.*)\"\]"
                # node with label refers to a line defining a node with a function / recursive call or a start/exit node
                node_with_label_regex = r"([0-9]*)\s*(\[label=\"([^\"]*)\"\]+)"
                node_without_label_regex = r"([0-9]+)"

                # Current line in the dot file represents an edge
                if (match := re.search(edge_regex, line)) is not None:
                    graph.update_with_edge(match)
                # Current line is not an edge - check if it defines a node with a start/exit/call label.
                elif (match := re.search(node_with_label_regex, line)) is not None:
                    matches = re.finditer(node_with_label_regex, line)
                    graph.update_with_node(matches, True)
                    matches = re.finditer(node_with_label_regex, line)
                    call = ControlFlowGraph.check_call(matches)
                    if call is not None:
                        calls.update(call)
                # Current line defines a node without a start/exit/call label
                elif (match := re.search(node_without_label_regex, line)) is not None:
                    matches = re.finditer(node_without_label_regex, line)
                    graph.update_with_node(matches, False)
            if graph.start_node == -1 or graph.end_node == -1:
                raise ValueError("Start and end nodes must both be defined.")

        if graph_type is AdjMatGraph:
            graph = AdjMatGraph(graph.adjacency_matrix(), graph.num_vertices)

        # Eventually will support loc for java and c/c++.
        return ControlFlowGraph(graph, Metadata(*options, Metadata.with_calls(calls)))

    @staticmethod
    def get_calls_structure(graphs: dict[str, ControlFlowGraph]) -> Optional[Tuple[list[list[str]], list[str]]]:
        """Create lists describing the hierarchy of a program's function calls."""
        calls_list = []
        simple_funcs = []
        for graph in graphs.values():
            if graph.metadata is None:
                return None

        for func1 in graphs:
            for func2 in graphs:
                if calls_function(graphs[func1].metadata.calls, func2):
                    calls_list.append([func1, func2])
                if graphs[func2].metadata.calls is None:
                    simple_funcs.append(func2)
        return calls_list, simple_funcs

    @staticmethod
    def stitch(graphs: dict[str, ControlFlowGraph]) -> ControlFlowGraph:
        """Create new CFG by substituting function calls with their graphs."""
        call_structure = ControlFlowGraph.get_calls_structure(graphs)
        if call_structure is not None:
            calls_list, simple_funcs = call_structure

        while calls_list:
            for func_pair in calls_list:
                func0, func1 = func_pair
                if func0 == func1:
                    for _ in range(len(calls_function(graphs[func0].metadata.calls, func1))):
                        node = calls_function(graphs[func0].metadata.calls, func1)[0]
                        graphs[func0] = ControlFlowGraph.recursify(graphs[func0], node)
                    calls_list.remove(func_pair)
                    if func0 not in [i[0] for i in calls_list]:
                        simple_funcs.append(func0)

                elif func1 in simple_funcs:
                    for _ in range(len(calls_function(graphs[func0].metadata.calls, func1))):
                        cfg1, cfg2 = graphs[func0], graphs[func1]
                        if cfg1.metadata.calls is not None:
                            node = calls_function(cfg1.metadata.calls, func1)[0]
                            cfg1.metadata.calls.pop(node)
                            graphs[func0] = ControlFlowGraph.compose(cfg1, cfg2, node)
                    calls_list.remove(func_pair)
                    if func0 not in [i[0] for i in calls_list]:
                        simple_funcs.append(func0)

        return graphs[simple_funcs[-1]]

    @staticmethod
    def compose(cfg1: ControlFlowGraph,
                cfg2: ControlFlowGraph,
                node: int) -> ControlFlowGraph:
        """
        Create a graph by replacing a node of cfg1 with the graph of cfg2.

        The new CFG generated will have the proper function call metadata based on cfg1 and cfg2.
        """
        shift = cfg2.graph.num_vertices - 1
        vertices = list(range(cfg1.graph.num_vertices + shift))

        # Ensures that exit node in subgraph has all the same edges as the replaced node.
        edges_2 = [[i + node, j + node] for [i, j] in cfg2.graph.edge_rules()]

        edges_1 = []
        for edge in cfg1.graph.edge_rules():
            vertex_1 = edge[0]
            vertex_2 = edge[1]
            if edge[0] >= node:
                vertex_1 += shift
            if edge[1] > node:
                vertex_2 += shift

            edges_1.append([vertex_1, vertex_2])

        edges_1 += edges_2

        stitched_graph = EdgeListGraph(edges_1, len(vertices))

        new_calls = {}
        if cfg1.metadata.calls is not None:
            for vertex in cfg1.metadata.calls.keys():
                if vertex > node:
                    new_calls[vertex + shift] = cfg1.metadata.calls[vertex]
                else:
                    new_calls[vertex] = cfg1.metadata.calls[vertex]

        return ControlFlowGraph(stitched_graph, Metadata(Metadata.with_calls(new_calls)))

    @staticmethod
    def recursify(cfg: ControlFlowGraph, node: int) -> ControlFlowGraph:
        """Add an edge from exit node to start node."""
        edges = cfg.graph.edge_rules()
        edges.append([node, cfg.graph.start_node])
        graph = EdgeListGraph(edges, len(cfg.graph.vertices()))
        return ControlFlowGraph(graph, cfg.metadata)
