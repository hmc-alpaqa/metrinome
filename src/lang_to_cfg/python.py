"""
Convert AST to CFG recursively.

The idea is to iterate line by line. Lines can be either control-flow relevant or not.
If they are not relevant to control flow, we simply ignore them.
Otherwise, we will call the function recursively. Essentially, when we see a new control-flow
breaking node, we connect it to the previous node, then call it recursively, and it should make
all of the connections. It will return ALL of its leaf nodes that should be connected to the next
thing after the statement returns.
"""

import ast
import os
# from pprintast import pprintast as ppast
import uuid
# pylint: disable=C0103
from typing import Optional, cast

from core.env import KnownExtensions
from core.log import Log
from graph.control_flow_graph import ControlFlowGraph, Metadata
from graph.graph import EdgeListGraph
from lang_to_cfg import converter


class Node:
    """A single node in the graph we convert the code to."""

    def __init__(self, exit_node: bool = False) -> None:
        """Create a new instance of the Graph node."""
        self.children: list[Node] = []
        self.exit_node: bool = exit_node
        self._id = uuid.uuid4()


class FunctionVisitor(ast.NodeVisitor):
    """
    FunctionVisitor handles the traversal through the AST for a single function.

    It includes visitor functions for each type of statement we are interested in.
    """

    def __init__(self, logger: Log = Log()) -> None:
        """Create a new instance of the function visitor."""
        self.root: Optional[Node] = None
        self.end_node: Optional[Node] = None
        self.frontier: list[Node] = []
        self.logger = logger

    def update_root(self, node: Node) -> bool:
        """Given a new node, set it as the root if a root does not exist."""
        if self.root is None:
            self.root = node
            self.end_node = node
            return True

        return False

    def update_frontier(self, node: Node) -> None:
        """Given a next node, set it as the child of all nodes in the frontier."""
        for frontier_node in self.frontier:
            frontier_node.children += [node]
            if frontier_node == self.end_node:
                self.end_node = node

    def standard_visit(self) -> Node:
        """Create a new node and update the graph accordingly."""
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]
        return new_node

    def visit_Expr(self, node: ast.AST) -> None:
        """Visit a python expression."""
        self.logger.d_msg(f"At expr {node}")
        self.standard_visit()

    def visit_Pass(self, node: ast.AST) -> None:
        """Visits a pass statement."""
        self.logger.d_msg(f"At pass {node}")
        self.standard_visit()

    def visit_Return(self, node: ast.Return) -> None:
        """Visit a python return statement."""
        self.logger.d_msg(f"At return {node}.")
        new_node = Node(exit_node=True)
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = []  # Nothing can come after a return

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit a python assign statement."""
        self.logger.d_msg(f"At assignment {node}.")
        self.standard_visit()

    def visit_For(self, node: ast.For) -> None:
        """Visit a python for loop."""
        self.logger.d_msg(f"At for {node}")
        new_node = self.standard_visit()

        # Now visit EACH of the things in the loop.
        # This will give us the subgraph. We connect each expression to the next.
        for loop_node in node.body:
            self.logger.d_msg(f"At for loop node {loop_node}")

            visitor = FunctionVisitor()
            visitor.visit(loop_node)
            for frontier_node in self.frontier:
                visitor.root = cast(Node, visitor.root)
                frontier_node.children += [visitor.root]
            self.frontier = visitor.frontier

        for frontier_node in self.frontier:
            frontier_node.children += [new_node]

        self.frontier = [new_node]

    def visit_With(self, node: ast.With) -> None:
        """Visit a python with statement."""
        self.logger.d_msg(f"At with {node}")
        self.standard_visit()

        # Visit everything inside the with block.
        # This follows the same pattern as the for loop visitor.
        for with_node in node.body:
            self.logger.d_msg(f"At with node {with_node}")

            visitor = FunctionVisitor()
            visitor.visit(with_node)
            if visitor.root is None:
                raise ValueError("Root must be non-nil.")

            self.update_frontier(visitor.root)
            self.frontier = visitor.frontier

    def visit_If(self, node: ast.If) -> None:
        """Visit a python if statement."""
        self.logger.d_msg(f"At if {node}")
        self.standard_visit()

        # Keep track of elements that will become the new frontier once we have looked
        # at ALL the if statements
        new_frontier = []

        # This is the comparison in the if statement
        self.logger.d_msg(f"{dir(node.test)}")

        # Visit the body of the first if block
        visitor = FunctionVisitor()
        visitor.visit(node.body[0])
        for frontier_node in self.frontier:
            if visitor.root is not None:
                frontier_node.children += [visitor.root]

            if visitor.end_node is not None:
                new_frontier += [visitor.end_node]

        i = 0
        # Check that there is another elif (or else statement)
        # Then, check that it is actually of type 'If', as the orself for an
        # else statement will actually get the body of the else
        # (see visit_If @ https://github.com/python/cpython/blob/master/Lib/ast.py)
        while len(node.orelse) != 0 and isinstance(node.orelse[0], ast.If):
            node = node.orelse[0]
            self.logger.d_msg(f"At the {i}th elif: {node}")
            # Visit the body of this elif block
            visitor = FunctionVisitor()
            visitor.visit(node.body[0])
            for frontier_node in self.frontier:
                if visitor.root is not None:
                    frontier_node.children += [visitor.root]
            if visitor.end_node is not None:
                new_frontier += [visitor.end_node]
            i += 1

        # Check if there is an else statement
        if len(node.orelse) != 0:
            # Get the body of the else
            node_list = node.orelse
            visitor = FunctionVisitor()
            visitor.visit(node_list[0])
            for frontier_node in self.frontier:
                if visitor.root is not None:
                    frontier_node.children += [visitor.root]
            if visitor.end_node is not None:
                new_frontier += [visitor.end_node]

        self.frontier = new_frontier

    def visit_Raise(self, node: ast.Raise) -> None:
        """Visit a python raise."""
        self.logger.d_msg(f"At raise {node}")

    def visit_Try(self, node: ast.Try) -> None:
        """Visit a python try statement."""
        self.logger.d_msg(f"At try {node}")

    def visit_While(self, node: ast.While) -> None:
        """Visit a python while loop."""
        self.logger.d_msg(f"At while {node}")
        new_node = self.standard_visit()

        # Now visit EACH of the things in the loop
        # This will give us the subgraph. We connect each expression to the next
        for loop_node in node.body:
            self.logger.d_msg(f"At loop node {loop_node}")

            visitor = FunctionVisitor()
            visitor.visit(loop_node)
            for frontier_node in self.frontier:
                visitor.root = cast(Node, visitor.root)
                frontier_node.children += [visitor.root]
            self.frontier = visitor.frontier

        for frontier_node in self.frontier:
            frontier_node.children += [new_node]

        self.frontier = [new_node]


class Visitor(ast.NodeVisitor):
    """
    Visitor is used to look at Python source code.

    It creates a FunctionVisitor for each function in the class.
    """

    def __init__(self, logger: Log = Log()) -> None:
        """Create a new instance of the Python source code parser."""
        self.graphs: dict[str, ControlFlowGraph] = {}
        self.logger = logger

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Call this for each function in the python source file."""
        if node.end_lineno is None:
            raise ValueError("Cannot get ending line for function.")

        md = Metadata(Metadata.with_loc(int(node.end_lineno) - node.lineno),
                      Metadata.with_language(KnownExtensions.Python))

        self.logger.d_msg(f"Visiting {node.name}")
        visitor = FunctionVisitor(self.logger)
        visitor.visit(node)

        # Now take the representation and convert it to a graph.py by doing BFS.

        nodes_to_visit = [visitor.root]
        nodes = dict()  # Maps node object to node number.
        nodes[visitor.root] = 0

        edge_list = []
        node_list = [0]

        visited = set()
        return_nodes = []

        while len(nodes_to_visit) != 0:
            curr_node = nodes_to_visit[0]
            nodes_to_visit = nodes_to_visit[1:]
            if curr_node in visited:
                continue

            visited.add(curr_node)
            curr_node = cast(Node, curr_node)

            children = list(filter(None, curr_node.children))

            # Create all of the edges we need to from the current node to its children.
            for child in children:
                # Check if we need to create a new node.
                if child not in nodes:
                    nodes[child] = len(node_list)
                    node_list.append(len(node_list))

                edge_list.append([nodes[curr_node], nodes[child]])

            nodes_to_visit += children

            if curr_node.exit_node:
                return_nodes.append(curr_node)

        node_list.append(len(node_list))

        for frontier_node in visitor.frontier:
            edge_list.append([nodes[frontier_node], len(node_list) - 1])

        for return_node in return_nodes:
            edge_list.append([nodes[return_node], len(node_list) - 1])

        cfg = ControlFlowGraph(EdgeListGraph(edge_list, len(node_list)), md)
        cfg.name = node.name

        self.graphs[node.name] = cfg


class PythonConvert(converter.ConverterAbstract):
    """PythonConvert is able to convert from Python source files to graph objects."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new instance of the python converter."""
        self.logger = logger

    def name(self) -> str:
        """Get the name of the Python converter."""
        return "Python"

    def to_graph(self, filename: str, file_extension: str) -> dict[str, ControlFlowGraph]:
        """Create a CFG from a Python source file."""
        path = os.path.join(os.getcwd(), filename) + ".py"
        visitor = Visitor(self.logger)
        graphs: dict[str, ControlFlowGraph]
        with open(path, "r") as src:
            root = ast.parse(src.read())
            visitor.visit(root)
            graphs = visitor.graphs

        for key in graphs.keys():
            self.logger.d_msg(f"==== Graph {key} =====")
            self.logger.d_msg(str(graphs[key]))

        return graphs
