from Graph import Graph 
from langToCFG.javaextractor.App import App 

class JavaConvert(): 
    def __init__(self) -> None: 
        pass 

    def toGraph(self, filename: str, file_extension: str) -> Graph: 
        '''
        Creates a CFG from a Java source file. 
        '''
        if file_extension == ".java" or file_extension == ".class":
            converter = App((filename + file_extension).strip(), export=False)
            converter.runLive(jar=False) 
            return Graph([], [], 0, 1) 

        converter = App((filename + file_extension).strip(), export=False) 
        converter.runLive(jar=True)
        return Graph([], [], 0, 1) 
