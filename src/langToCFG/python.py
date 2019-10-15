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

class FunctionVisitor(ast.NodeVisitor): 
    def __init__(self): 
        self.startNode = 0 
        self.endNode = 0 
        self.vertices = [0]
        self.edges = [] 

    
    def visit_Expr(self, node):
        print(node.body)
 
    def visit_Return(self, node):
        print(node)
 
    def visit_Assign(self, node):
        print(node.body)
 
    def visit_For(self, node):
        print(node.body)
 
    def visit_With(self, node):
        print(node.body)
 
    def visit_If(self, node):
        print(node.body)
 
    def visit_Raise(self, node):
        print(node.body)
 
    def visit_Try(self, node):
        print(node.body)
 
    def visit_While(self, node):
        print(node.body)
 
class Visitor(ast.NodeVisitor): 
    def __init__(self) -> None: 
        self.graphs = {}

    def visit_FunctionDef(self, node):
        print(f"at node {node.body}")
        visitor = FunctionVisitor()
        visitor.visit(node)
        graph = Graph(visitor.edges, visitor.vertices, visitor.startNode, visitor.endNode)
        self.graphs[len(self.graphs.keys())] = graph

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
        print(os.getcwd())
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
