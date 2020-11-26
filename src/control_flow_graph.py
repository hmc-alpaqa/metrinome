"""All information that needs to be stored aside from the graph to compute complexity metrics."""
import os
import re
from typing import cast, List
from utils import calls_function
from graph import AnyGraph, GraphType, Graph, AdjListType, Dict


class Metadata:
    """Store metadata associated with a CFG."""

    def __init__(self, loc: int):
        """Create a new metadata object."""
        self.loc = loc


class ControlFlowGraph:
    """
    ControlFlowGraph objects are wrappers for Graphs that contain additional metadata.

    This allow us to compute a more diverse set of complexity metrics without adding
    metadata to the Graph class.
    """

    def __init__(self, graph: AnyGraph, metadata: Metadata = None):
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

    @staticmethod
    def from_file(filename: str, weighted: bool = False,
                  graph_type: GraphType = GraphType.ADJACENCY_LIST) -> 'ControlFlowGraph':
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
                    graph.update_with_edge(match)
                # Current line is not an edge - check if it defines a node.
                elif (match := re.search(r"([0-9]*)\s*\[label=\"(.*)\"\]", line)) is not None:
                    graph.update_with_node(match)

            if graph.start_node == -1 or graph.end_node == -1:
                raise ValueError("Start and end nodes must both be defined.")

            graph.weighted = weighted

        if graph_type is GraphType.ADJACENCY_MATRIX:
            graph.edges = graph.adjacency_matrix()
            graph.graph_type = GraphType.ADJACENCY_MATRIX

        return ControlFlowGraph(graph)

    @staticmethod
    def stitch(graphs: Dict[str, 'ControlFlowGraph']) -> 'ControlFlowGraph':
        """Compose a set of graphs to accurately represent a program's CFG."""
        calls_list = []
        simple_funcs = []
        for func1 in graphs.keys():
            for func2 in graphs.keys():
                if calls_function(graphs[func1].graph.calls, func2):
                    calls_list.append([func1, func2])
                if graphs[func2].graph.calls == {}:
                    simple_funcs.append(func2)

        while calls_list:
            for func_pair in calls_list:
                if func_pair[1] in simple_funcs:
                    for _ in range(len(
                        calls_function(graphs[func_pair[0]].graph.calls, func_pair[1])
                    )):
                        graph1, graph2 = graphs[func_pair[0]], graphs[func_pair[1]]
                        node = calls_function(graphs[func_pair[0]].graph.calls, func_pair[1])[0]
                        graphs[func_pair[0]] = ControlFlowGraph.compose(graph1, graph2, node)
                    calls_list.remove(func_pair)
                    if func_pair[0] not in [i[0] for i in calls_list]:
                        simple_funcs.append(func_pair[0])
        stitched_graph = graphs[simple_funcs[-1]]
        return stitched_graph

    @staticmethod
    def compose(graph1: 'ControlFlowGraph',
                graph2: 'ControlFlowGraph',
                node: int) -> 'ControlFlowGraph':
        """Replace a vertex in graph1 with graph2."""
        graph1.graph.calls.pop(node)

        shift = graph2.graph.vertex_count() - 1
        vertices = list(range(graph1.graph.vertex_count() + shift))

        # ensures that exit node in subgraph has all the same edges as the replaced node
        edges_2 = [[i + node, j + node] for [i, j] in graph2.graph.edges]

        edges_1 = []
        for edge in graph1.graph.edges:
            vertex_1 = edge[0]
            vertex_2 = edge[1]
            if edge[0] >= node:
                vertex_1 += shift
            if edge[1] > node:
                vertex_2 += shift

            edges_1.append([vertex_1, vertex_2])

        edges_1 += edges_2

        stitched_graph = Graph(edges_1, vertices, 0,
                               len(vertices) - 1, GraphType.EDGE_LIST)

        new_calls = {}
        for vertex in graph1.graph.calls.keys():
            if vertex > node:
                new_calls[vertex + shift] = graph1.graph.calls[vertex]
            else:
                new_calls[vertex] = graph1.graph.calls[vertex]

        stitched_graph.calls = new_calls

        return ControlFlowGraph(stitched_graph)
