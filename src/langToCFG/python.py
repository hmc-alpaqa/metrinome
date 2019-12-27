from Graph import Graph
import os, ast 
from _ast import Expr, Return, Assign, For, With, If, Raise, Try, While, Break, Continue 
from pprintast import pprintast as ppast
from typing import List

# We will convert AST to CFG recursively.
# The idea is to iterate line by line. 
# Lines can be EITHER control-flow relevant or not. 
# If they are not relevant to control flow, we simply ignore them. 
# Otherwise, we will call the function recursively. Essentially, when we see 
# a new control-flow breaking node, we connect it to the previous node, then
# call it recursively, and it should make all of the connections. It will 
# return ALL of its leaf nodes that should be connected to the next thing after 
# the statement returns. 

class Node:
    def __init__(self):
        self.children = []

class FunctionVisitor(ast.NodeVisitor):

    def comparatorConverter(self, comparator):
        return ""

    def __init__(self):
        self.root = None
        self.frontier = None

    def visit_Expr(self, node):
        print(f"At expr {node}")
        newNode = Node()
        if self.root is None:
            self.root = newNode
        else:
            for node in self.frontier:
                node.children += [newNode]

        self.frontier = [newNode]

    def visit_Return(self, node):
        print(f"At return {node}.")
        newNode = Node()
        if self.root is None:
            self.root = newNode
        else:
            for node in self.frontier:
                node.children += [newNode]

        self.frontier = [] # Nothing can come after a return 

    def visit_Assign(self, node):
        print(f"At assignment {node}.")
        newNode = Node()
        if self.root is None:
            self.root = newNode
        else:
            for node in self.frontier:
                node.children += [newNode]

        self.frontier = [newNode]

    def visit_For(self, node):
        print(f"At for {node}")
        newNode = Node()
        # Add the new node representing the beginning of the loop 
        if self.root is None:
            self.root = newNode
        else:
            for frontierNode in self.frontier:
                frontierNode.children += [newNode]

        self.frontier = [newNode]

        # Now visit EACH of the things in the loop 
        # This will give us the subgraph. We connect each expression to the next 
        for loopNode in node.body: 
            print(f"At for loop node {loopNode}")

            visitor = FunctionVisitor()
            visitor.visit(loopNode)
            for frontierNode in self.frontier:
                frontierNode.children += [visitor.root]
            self.frontier = visitor.frontier

        for frontierNode in self.frontier:
            frontierNode.children += [newNode]

        self.frontier = [newNode]

    def visit_With(self, node):
        print(f"At with {node}")

    def visit_If(self, node):
        print(f"At if {node}")
        newNode = Node()
        # Add the new node representing the beginning of the if statement
        if self.root is None:
            self.root = newNode
        else:
            for frontierNode in self.frontier:
                frontierNode.children += [newNode]

        self.frontier = [newNode]
        print(f"If body: {dir(node)}")

        test = node.test
        print(f"{dir(node.test)}")
        # print(f"If test: {test.col_offset} {test.left} {test.comparators} {test.left} {test.ops}")

    def visit_Raise(self, node):
        print(f"At raise {node}")

    def visit_Try(self, node):
        print(f"At try {node}")
 
    def visit_While(self, node):
        print(f"At while {node}")
        newNode = Node() 
        # Add the new node representing the beginning of the loop
        if self.root is None: 
            self.root = newNode
        else: 
            for frontierNode in self.frontier: 
                frontierNode.children += [newNode]

        self.frontier = [newNode]

        # Now visit EACH of the things in the loop 
        # This will give us the subgraph. We connect each expression to the next 
        for loopNode in node.body: 
            print(f"At loop node {loopNode}")

            visitor = FunctionVisitor() 
            visitor.visit(loopNode)
            for frontierNode in self.frontier:
                frontierNode.children += [visitor.root]
            self.frontier = visitor.frontier 

        for frontierNode in self.frontier:
            frontierNode.children += [newNode] 

        self.frontier = [newNode] 

class Visitor(ast.NodeVisitor): 
    def __init__(self) -> None: 
        self.graphs = {}

    def visit_FunctionDef(self, node):
        visitor = FunctionVisitor()
        print(f"Visiting {node.name}")
        visitor.visit(node)

        # Now take the representation and convert it to a graph.py by doing BFS 

        L = [visitor.root] # Keep track of the nodes we still need to visit
        nodes = dict() # Maps node object to node number
        nodes[visitor.root] = 0

        edgeList = [] 
        nodeList = [0] 
        startNode = 0
        endNode = None 

        visited = set()

        while len(L) != 0:
            currNode = L[0]
            L = L[1:]
            if currNode in visited:
                continue

            visited.add(currNode)
            children = currNode.children

            # Create all of the edges we need to from the current node to its children. 
            for child in children:
                # Check if we need to create a new node.
                if child not in nodes:
                    nodes[child] = len(nodeList)
                    nodeList.append(len(nodeList))

                edgeList.append((nodes[currNode], nodes[child]))

            L += children

        endNode = len(nodeList) - 1
        g = Graph(edgeList, nodeList, startNode, endNode)

        self.graphs[node.name] = g

class PythonConvert():
    def __init__(self) -> None:
        pass

    def astToCFG(self, tree):
        '''
        Convert an AST obtained from the source code to a Control Flow Graph. 
        '''
        return

    def toGraph(self, filename: str, file_extension: str) -> List[Graph]: 
        '''
        Creates a CFG from a Python source file.
        '''
        path = os.path.join(os.getcwd(), filename) + ".py"
        cfg = None
        visitor = Visitor()
        graphs = []
        with open(path, "r") as src:
            root = ast.parse(src.read())
            visitor.visit(root)
            graphs = visitor.graphs

        for key in graphs.keys():
            print(f"==== Graph {key} =====")
            print(graphs[key])
            pass

        return graphs
