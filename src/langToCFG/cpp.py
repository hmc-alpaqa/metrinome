import subprocess, argparse, glob2, os, re, sys, shlex
sys.path.append("/app/code/")
from Graph import Graph
from typing import List 

class CPPConvert(): 

    def __init__(self) -> None: 
        pass 

    def toGraph(self, filename: str, file_extension: str) -> List[Graph]: 
        '''
        Creates a CFG from a C++ source file. 
        '''
        self.createDotFiles(filename)
        self.convertToStandardFormat(filename)
        g =  {f'{filename}': Graph.fromFile(filename)}
        self.cleanTemps()
        return g

    def convertToStandardFormat(self, filename: str):
        '''
        Convert each dot file generated from the .cpp source to the same format
        as the dot files generated from Java CFGs.
        '''
        nodes = []
        edges = []
        nodeMap = {}
        counter = 0
        
        # Make a temporary file (with the new content)
        filename = filename.split("/")[-1]
        with open(f'temp/{filename}.dot', 'w') as newFile:
            with open('temp/cfg.main.dot', "r") as oldFile:
                content = oldFile.readlines()
                newFile.write("digraph { \n")
                for line in content[1:]:
                    line = line.strip()

                    # Throw out the label (e.g. label="CFG for 'main' function") for the graph and remove whitespace
                    if line.startswith("label") or line == "":
                        continue 

                    # If it contains a label (denoted by '[]'), it is a vertex
                    edgePattern = "->"
                    namePattern = "([a-zA-Z0-9]+ )"
                    isEdge = re.search(edgePattern, line)
                    if isEdge is None:
                        nodeName = re.match(namePattern, line.lstrip())
                        if nodeName is None:
                            continue 
                        nodeName = nodeName.groups()[0].strip()
                        nodeMap[nodeName] = str(counter)
                        nodeToAdd = str(counter)
                        if counter == 0:
                            nodeToAdd += " [label=\"START\"]" 

                        nodes.append(nodeToAdd)
                    
                        counter += 1
                    else: 
                        edges += [line]
            
            # Create the nodes and then the edges 
            for i, node in enumerate(nodes):
                if i == counter - 2: 
                    node += " [label=\"EXIT\"]"
                newFile.write(node + ";" + "\n")
            
            for edge in edges:
                for nodeName in nodeMap.keys():
                    edge = edge.replace(nodeName, nodeMap[nodeName]) 
                    edge = edge.replace(":s0", "")
                    edge = edge.replace(":s1", "")

                newFile.write(edge + "\n")
            newFile.write("}")
        

    def createDotFiles(self, filepath: str) -> Graph:
        '''
        Create a .dot file representing a control flow graph for 
        each function from a .cpp file
        '''
        
        subprocess.check_call(["mkdir" , "-p", "temp"])
        self.run(f"clang++-6.0 -emit-llvm -S {filepath}.cpp -o /dev/stdout | opt -dot-cfg")
        subprocess.call(["mv", "cfg.main.dot", "temp"])
        
        

    def run(self, cmd):
        """Runs the given command locally and returns the output, err and exit_code."""
        if "|" in cmd:    
            cmd_parts = cmd.split('|')
        else:
            cmd_parts = []
            cmd_parts.append(cmd)
        i = 0
        p = {}
        for cmd_part in cmd_parts:
            cmd_part = cmd_part.strip()
            if i == 0:
                p[i]=subprocess.Popen(shlex.split(cmd_part),stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = False)
            else:
                p[i]=subprocess.Popen(shlex.split(cmd_part),stdin=p[i-1].stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = False)
            i += 1
        (output, err) = p[i-1].communicate()
        exit_code = p[0].wait()
        return str(output), str(err), exit_code 

    
    def cleanTemps(self):
        """removes temp files and directories """
        subprocess.call(["rm", "-r", "temp"])
        files = glob2.glob("*.dot")
        for f in files:
            os.remove(f)
        
if __name__ == "__main__":
    c = CPPConvert()
    c.toGraph("hello", "cpp")
