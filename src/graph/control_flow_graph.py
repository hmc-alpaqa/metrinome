"""All information that needs to be stored aside from the graph to compute complexity metrics."""
from __future__ import annotations

import os
import re
from typing import Callable, Dict, List, Match, Optional, Type, cast

from graph.graph import AdjListGraph, AdjListType, AdjMatGraph, EdgeListGraph, Graph
from utils import calls_function

Option = Callable[['Metadata'], None]


class Metadata:
    """Store metadata associated with a CFG."""

    def __init__(self, *options: Option):
        """Create a new metadata object."""
        self.loc: Optional[int] = None
        self.calls: Dict[int, str] = {}

        for opt in options:
            opt(self)

    def __str__(self) -> str:
        """Return metadata as string."""
        return f"Lines of code: {self.loc}, Calls: {self.calls}"

    @staticmethod
    def with_loc(loc: int) -> Option:
        """Set number of lines of code in metadata."""
        def option(metadata: Metadata) -> None:
            """Apply the option."""
            metadata.loc = loc
        return option

    @staticmethod
    def with_calls(calls: Dict[int, str]) -> Option:
        """Initialize calls in a Metadata instance."""
        def option(metadata: Metadata) -> None:
            """Apply the option."""
            metadata.calls = calls
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

    @staticmethod
    def check_call(match: Match[str]) -> Optional[Dict[int, str]]:
        """Find and return any functions called on a node."""
        node = int(match.group(1))
        label = match.group(2)
        if "CALLS" in label:
            return {node: label}
        return None

    @staticmethod
    def from_file(filename: str, graph_type: Type[Graph] = AdjListGraph) -> ControlFlowGraph:
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
        calls = {}
        # Initialize graph based on type.
        graph: Graph
        if graph_type is AdjListGraph:
            graph = AdjListGraph(cast(AdjListType, []), 0)
        elif graph_type is EdgeListGraph:
            edges: List[List[int]] = []
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
                node_with_label_regex = r"([0-9]*)\s*\[label=\"(.*)\"\]"
                node_without_label_regex = r"([0-9]+)"
                if (match := re.search(edge_regex, line)) is not None:
                    # The current line in the text file represents an edge.
                    graph.update_with_edge(match)
                # Current line is not an edge - check if it defines a node.
                elif (match := re.search(node_with_label_regex, line)) is not None:
                    graph.update_with_node(match, True)
                    call = ControlFlowGraph.check_call(match)
                    if call is not None:
                        calls.update(call)
                elif (match := re.search(node_without_label_regex, line)) is not None:
                    graph.update_with_node(match, False)

            if graph.start_node == -1 or graph.end_node == -1:
                raise ValueError("Start and end nodes must both be defined.")

        if graph_type is AdjMatGraph:
            graph = AdjMatGraph(graph.adjacency_matrix(), graph.num_vertices)

        # Eventually will support loc for java and c/c++.
        return ControlFlowGraph(graph, Metadata(Metadata.with_calls(calls)))

    @staticmethod
    def stitch(graphs: Dict[str, ControlFlowGraph]) -> ControlFlowGraph:
        """Create new CFG by substituting function calls with their graphs."""
        calls_list = []
        simple_funcs = []
        for graph in graphs.values():
            if graph.metadata is None:
                return None

        for func1 in graphs:
            for func2 in graphs:
                if calls_function(graphs[func1].metadata.calls, func2):
                    if func1 != func2:
                        calls_list.append([func1, func2])
                if graphs[func2].metadata.calls == {}:
                    simple_funcs.append(func2)

        while calls_list:
            for func_pair in calls_list:
                if func_pair[1] in simple_funcs:
                    for _ in range(len(
                        calls_function(graphs[func_pair[0]].metadata.calls, func_pair[1])
                    )):
                        cfg1, cfg2 = graphs[func_pair[0]], graphs[func_pair[1]]
                        node = calls_function(graphs[func_pair[0]].metadata.calls, func_pair[1])[0]
                        cfg1.metadata.calls.pop(node)
                        graphs[func_pair[0]] = ControlFlowGraph.compose(cfg1, cfg2, node)
                    calls_list.remove(func_pair)
                    if func_pair[0] not in [i[0] for i in calls_list]:
                        simple_funcs.append(func_pair[0])

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
        for vertex in cfg1.metadata.calls.keys():
            if vertex > node:
                new_calls[vertex + shift] = cfg1.metadata.calls[vertex]
            else:
                new_calls[vertex] = cfg1.metadata.calls[vertex]

        return ControlFlowGraph(stitched_graph, Metadata(Metadata.with_calls(new_calls)))
