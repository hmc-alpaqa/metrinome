"""
Convert AST to CFG recursively.

The idea is to iterate line by line. Lines can be either control-flow relevant or not.
If they are not relevant to control flow, we simply ignore them.
Otherwise, we will call the function recursively. Essentially, when we see a new control-flow
breaking node, we connect it to the previous node, then call it recursively, and it should make
all of the connections. It will return ALL of its leaf nodes that should be connected to the next
thing after the statement returns.
"""

# pylint: disable=C0103
import sys
sys.path.append("/app/code/")
from typing import List, Optional, Dict, cast
import ast
import os
# from pprintast import pprintast as ppast
from log import Log
from graph import Graph, GraphType
from lang_to_cfg import converter  # type: ignore


class Node:
    """A single node in the graph we convert the code to."""

    def __init__(self) -> None:
        """Create a new instance of the Graph node."""
        self.children: List[Node] = []


class FunctionVisitor(ast.NodeVisitor):
    """
    FunctionVisitor handles the traversal through the AST for a single function.

    It includes visitor functions for each type of statement we are interested in.
    """

    def __init__(self, logger=Log()) -> None:
        """Create a new instance of the function visitor."""
        self.root: Optional[Node] = None
        self.end_node: Optional[Node] = None
        self.frontier: List[Node] = []
        self.logger = logger

    def update_root(self, node) -> bool:
        """Given a new node, set it as the root if a root does not exist."""
        if self.root is None:
            self.root = node
            self.end_node = node
            return True

        return False

    def update_frontier(self, node) -> None:
        """Given a next node, set it as the child of all nodes in the frontier."""
        for frontier_node in self.frontier:
            frontier_node.children += [node]
            if frontier_node == self.end_node:
                self.end_node = node

    def visit_Expr(self, node) -> None:
        """Visit a python expression."""
        self.logger.d_msg(f"At expr {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

    def visit_Pass(self, node) -> None:
        """Visits a pass statement."""
        self.logger.d_msg(f"At pass {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

    def visit_Return(self, node) -> None:
        """Visit a python return statement."""
        self.logger.d_msg(f"At return {node}.")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = []  # Nothing can come after a return

    def visit_Assign(self, node) -> None:
        """Visit a python assign statement."""
        self.logger.d_msg(f"At assignment {node}.")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

    def visit_For(self, node) -> None:
        """Visit a python for loop."""
        self.logger.d_msg(f"At for {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

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

    # pylint: disable=R0201
    def visit_With(self, node) -> None:
        """Visit a python with statement."""
        self.logger.d_msg(f"At with {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

        # Visit everything inside the with block.
        # This follows the same pattern as the for loop visitor.
        for with_node in node.body:
            self.logger.d_msg(f"At with node {with_node}")

            visitor = FunctionVisitor()
            visitor.visit(with_node)
            self.update_frontier(visitor.root)
            self.frontier = visitor.frontier

    def visit_If(self, node) -> None:
        """Visit a python if statement."""
        self.logger.d_msg(f"At if {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

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
            node = node.orelse
            visitor = FunctionVisitor()
            visitor.visit(node[0])
            for frontier_node in self.frontier:
                if visitor.root is not None:
                    frontier_node.children += [visitor.root]
            if visitor.end_node is not None:
                new_frontier += [visitor.end_node]

        self.frontier = new_frontier

    # pylint: disable=R0201
    def visit_Raise(self, node) -> None:
        """Visit a python raise."""
        self.logger.d_msg(f"At raise {node}")

    # pylint: disable=R0201
    def visit_Try(self, node) -> None:
        """Visit a python try statement."""
        self.logger.d_msg(f"At try {node}")

    def visit_While(self, node) -> None:
        """Visit a python while loop."""
        self.logger.d_msg(f"At while {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

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

    def __init__(self, logger=Log()) -> None:
        """Create a new instance of the Python source code parser."""
        self.graphs: Dict[str, Graph] = {}
        self.logger = logger

    def visit_FunctionDef(self, node) -> None:
        """Call this for each function in the python source file."""
        visitor = FunctionVisitor()
        self.logger.d_msg(f"Visiting {node.name}")
        visitor.visit(node)

        # Now take the representation and convert it to a graph.py by doing BFS.

        nodes_to_visit = [visitor.root]
        nodes = dict()  # Maps node object to node number.
        nodes[visitor.root] = 0

        edge_list = []
        node_list = [0]

        visited = set()

        while len(nodes_to_visit) != 0:
            curr_node = nodes_to_visit[0]
            nodes_to_visit = nodes_to_visit[1:]
            if curr_node in visited:
                continue

            visited.add(curr_node)
            curr_node = cast(Node, curr_node)
            children = curr_node.children

            # Create all of the edges we need to from the current node to its children.
            for child in children:
                # Check if we need to create a new node.
                if child not in nodes:
                    nodes[child] = len(node_list)
                    node_list.append(len(node_list))

                edge_list.append([nodes[curr_node], nodes[child]])

            nodes_to_visit += children

        if len(visitor.frontier) != 1:
            self.logger.d_msg("Frontier has more than one node.")
            new_node = Node()
            nodes[new_node] = len(node_list)
            node_list.append(len(node_list))
            visitor.end_node = new_node
            for frontier_node in visitor.frontier:
                edge_list.append([nodes[frontier_node], nodes[new_node]])

        graph = Graph(edge_list, node_list, nodes[visitor.root],
                      nodes[visitor.end_node], GraphType.EDGE_LIST)

        self.graphs[node.name] = graph


class PythonConvert(converter.ConverterAbstract):
    """PythonConvert is able to convert from Python source files to graph objects."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger) -> None:
        """Create a new instance of the python converter."""
        self.logger = logger

    def name(self) -> str:
        """Get the name of the Python converter."""
        return "Python"

    # pylint: disable=R0201
    def to_graph(self, filename: str, file_extension: str) -> Dict[str, Graph]:
        """Create a CFG from a Python source file."""
        self.logger.d_msg(file_extension)

        path = os.path.join(os.getcwd(), filename) + ".py"
        self.logger.d_msg(path)
        visitor = Visitor()
        graphs: Dict[str, Graph]
        with open(path, "r") as src:
            root = ast.parse(src.read())
            visitor.visit(root)
            graphs = visitor.graphs

        for key in graphs.keys():
            self.logger.d_msg(f"==== Graph {key} =====")
            self.logger.d_msg(str(graphs[key]))

        return graphs
