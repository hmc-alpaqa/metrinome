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

from typing import List, Optional, Dict, cast
import ast
import os
# from pprintast import pprintast as ppast
from graph import Graph


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

    def __init__(self) -> None:
        """Create a new instance of the function visitor."""
        self.root: Optional[Node] = None
        self.end_node: Optional[Node] = None
        self.frontier: List[Node] = []

    def update_root(self, node) -> None:
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
        print(f"At expr {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

    def visit_Pass(self, node) -> None:
        print("At pass {node}")
        new_node = Node() 
        if not self.update_root(new_node): 
            self.update_frontier(new_node)

        self.frontier = [new_node]

    def visit_Return(self, node) -> None:
        """Visit a python return statement."""
        print(f"At return {node}.")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = []  # Nothing can come after a return

    def visit_Assign(self, node) -> None:
        """Visit a python assign statement."""
        print(f"At assignment {node}.")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

    def visit_For(self, node) -> None:
        """Visit a python for loop."""
        print(f"At for {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

        # Now visit EACH of the things in the loop
        # This will give us the subgraph. We connect each expression to the next
        for loop_node in node.body:
            print(f"At for loop node {loop_node}")

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
        print(f"At with {node}")

    def visit_If(self, node) -> None:
        """Visit a python if statement."""
        print(f"At if {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]
        print(f"If body: {dir(node)}")

        print(f"{dir(node.test)}")

    # pylint: disable=R0201
    def visit_Raise(self, node) -> None:
        """Visit a python raise."""
        print(f"At raise {node}")

    # pylint: disable=R0201
    def visit_Try(self, node) -> None:
        """Visit a python try statement."""
        print(f"At try {node}")

    def visit_While(self, node) -> None:
        """Visit a python while loop."""
        print(f"At while {node}")
        new_node = Node()
        if not self.update_root(new_node):
            self.update_frontier(new_node)

        self.frontier = [new_node]

        # Now visit EACH of the things in the loop
        # This will give us the subgraph. We connect each expression to the next
        for loop_node in node.body:
            print(f"At loop node {loop_node}")

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

    def __init__(self) -> None:
        """Create a new instance of the Python source code parser."""
        self.graphs: Dict[str, Graph] = {}

    def visit_FunctionDef(self, node) -> None:
        """Call this for each function in the python source file."""
        visitor = FunctionVisitor()
        print(f"Visiting {node.name}")
        visitor.visit(node)

        # Now take the representation and convert it to a graph.py by doing BFS

        L = [visitor.root]  # Keep track of the nodes we still need to visit
        nodes = dict()  # Maps node object to node number
        nodes[visitor.root] = 0

        edge_list = []
        node_list = [0]

        visited = set()

        while len(L) != 0:
            curr_node = L[0]
            L = L[1:]
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

                edge_list.append((nodes[curr_node], nodes[child]))

            L += children

        graph = Graph(edge_list, node_list, nodes[visitor.root], nodes[visitor.end_node])

        self.graphs[node.name] = graph


class PythonConvert():
    """PythonConvert is able to convert from Python source files to graph objects."""

    def __init__(self) -> None:
        """Create a new instance of the python converter."""

    # pylint: disable=R0201
    def to_graph(self, filename: str, file_extension: str) -> Dict[str, Graph]:
        """Create a CFG from a Python source file."""
        print(file_extension)

        path = os.path.join(os.getcwd(), filename) + ".py"
        print(path)
        visitor = Visitor()
        graphs: Dict[str, Graph]
        with open(path, "r") as src:
            root = ast.parse(src.read())
            visitor.visit(root)
            graphs = visitor.graphs

        for key in graphs.keys():
            print(f"==== Graph {key} =====")
            print(graphs[key])

        return graphs
