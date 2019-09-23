from Graph import Graph 

class JavaConvert(): 
    def __init__(self) -> None: 
        pass 

    def toGraph(self, filename: str) -> Graph: 
        '''
        Creates a CFG from a Java source file. 
        '''
        return Graph([], [], 0, 1) 