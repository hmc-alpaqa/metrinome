from Graph import Graph
import os, ast 
from _ast import Expr, Return, Assign, For, With, If, Raise, Try, While, Break, Continue 
from pprintast import pprintast as ppast

# We will convert AST to CFG recursively.
# The idea is to iterate line by line. 
# Lines can be EITHER control-flow relevant or not. 
# If they are not relevant to control flow, we simply ignore them. 
# Otherwise, we will call the function recursively. Essentially, when we see 
# a new control-flow breaking node, we connect it to the previous node, then
# call it recursively, and it should make all of the connections. It will 
# return ALL of its leaf nodes that should be connected to the next thing after 
# the statement returns. 

class Visitor(ast.NodeVisitor): 
    def __init__(self):
        self.startNode = 0 
        self.endNode = 0
        self.vertices = [0] 
        self.edges = []  

    def visitRecurse(self, node):
        body = node.body  
        for i, element in enumerate(body):
            if isinstance(element, Expr):
                # Ignore 
                print("Expression!")
            elif isinstance(element, Return):
                # Last node 
                self.vertices.append(len(vertices))
                print("Return!")
            elif isinstance(element, Assign):
                # Ignore 
                print("Assign!")
            elif isinstance(element, For): 
                # Control Flow Breaking - TODO 
                print("For!")
                # Make new node 
                numCurrNode = len(self.vertices) - 1
                self.vertices.append(numCurrNode + 1)
                # Connect it to prev node 
                self.edges.append([numCurrNode, numCurrNode + 1])
                # Call recursively  
                # endNodes = self.visitRecurse(element)
            elif isinstance(element, If):
                # Control Flow Breaking - TODO 
                print("If!")
                print(element.body)
                print(element.orelse[0].orelse)
                # Make new node 
                numCurrNode = len(self.vertices) - 1
                self.vertices.append(numCurrNode + 1)
                # Connect it to prev node 
                self.edges.append([numCurrNode, numCurrNode + 1])
                # Call recursively  
                # endNodes = self.visitRecurse(element)
            elif isinstance(element, While): 
                # Control Flow Breaking - TODO 
                print("While!")
                # Make a new node 
                numCurrNode = len(self.vertices) - 1
                self.vertices.append(numCurrNode + 1)
                # Connect it to prev node 
                self.edges.append([numCurrNode, numCurrNode + 1])
                # Call recursively
            elif isinstance(element, Break): 
                # Not yet Implemented
                print("Break!")
            elif isinstance(element, Continue): 
                # Not yet implemented
                print("Continue!")
            elif isinstance(element, With): 
                # Not yet implemented 
                print("With!")
            elif isinstance(element, Raise): 
                # Not yet implemented 
                print("Raise!")
            elif isinstance(element, Try):
                # Not yet implemented 
                print("Try!")
            else: 
                print(element) 

        self.endNode = len(self.vertices) - 1  
        
    def visit_FunctionDef(self, node):
        print("=== Function: " + node.name + " ===")
        self.visitRecurse(node) 

class PythonConvert(): 
    def __init__(self) -> None: 
        pass 

    def astToCFG(self, tree): 
        '''
        Convert an AST obtained from the source code to a Control Flow Graph. 
        '''
        return 
    
    def toGraph(self, filename: str, file_extension: str) -> Graph: 
        ''' 
        Creates a CFG from a Python source file. 
        ''' 
        print(os.getcwd())
        path = os.path.join(os.getcwd(), filename) + ".py"
        cfg = None
        visitor = Visitor() 
        with open(path, "r") as src:
            root = ast.parse(src.read())
            visitor.visit(root) 

        return Graph(visitor.edges, visitor.vertices, visitor.startNode, visitor.endNode)  