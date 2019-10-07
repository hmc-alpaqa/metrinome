import subprocess, argparse, glob2, os, re, sys
from Graph import Graph

class CPPConvert(): 

    def __init__(self) -> None: 
        pass 

    def toGraph(self, filename: str, file_extension: str) -> Graph: 
        '''
        Creates a CFG from a C++ source file. 
        '''
        self.createDotFiles(filename)
        self.convertToStandardFormat("test")
        return Graph.fromFile("test")

    def convertToStandardFormat(self, file: str):
        '''
        Convert each dot file generated from the .cpp source to the same format
        as the dot files generated from Java CFGs.
        '''
        nodes = []
        edges = []
        nodeMap = {}
        counter = 0

        # Make a temporary file (with the new content)
        with open(file + 'temp', 'w') as newFile:
            with open(file, "r") as oldFile:
                content = oldFile.readlines()
                newFile.write("digraph { \n")
                for line in content[1:]:
                    line = line.strip()

                    # Throw out the label for the graph and remove whitespace
                    if line.startswith("label") or line == "":
                        continue 

                    # If it contains a label (denoted by '[]'), it is an edge 
                    namePattern = "[a-zA-Z0-9]*"
                    isNode = re.match(namePattern + " \[", line)
                    if isNode is not None:
                        nodeName = re.match(namePattern + " ", line).group().strip()
                        nodeMap[nodeName] = str(counter)
                        nodeToAdd = str(counter)
                        if counter == 0:
                            nodeToAdd += " [label=\"START\"]" 
                        elif counter == 1: 
                            nodeToAdd += " [label=\"EXIT\"]"

                        nodes.append(line)
                        counter += 1
                    else: 
                        edges += [line]
            
            # Create the nodes and then the edges 
            for node in nodes:
                newFile.write(node + "\n")
            
            for edge in edges:
                for nodeName in nodeMap.keys():
                    edge = edge.replace(nodeName, nodeMap[nodeName]) 

                edge = edge.replace(":s0", "")
                edge = edge.replace(":s1", "")
                newFile.write(edge + "\n")

    def createDotFiles(self, filename: str):
        '''
        Create a .dot file representing a control flow graph for 
        each function from a .cpp file
        '''
        command = f"clang++-6.0 -emit-llvm -S ../{filename}.cpp -o /dev/stdout | opt --dot-cfg"
        commands = ["mkdir ll", "cd ll", command]
        combinedCommands = "; ".join(commands)
        subprocess.call(combinedCommands, shell=True)
        