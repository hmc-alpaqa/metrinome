import subprocess, argparse, glob2, os, re, sys, shlex, signal # type: ignore
sys.path.append("/app/code/")
from Graph import Graph
from typing import List, Dict, Any, cast

class CPPConvert():

    def __init__(self, logger) -> None:
        self.logger = logger

    def toGraph(self, filename: str, file_extension: str) -> Dict[str, Graph]:
        '''
        Creates a CFG from a C++ source file.
        '''
        self.logger.d("Creating dot files")
        self.createDotFiles(filename, file_extension)
        self.logger.d("Converting to standard format")
        fileCount = self.convertToStandardFormat(filename)
        self.logger.d(f"File count is: {fileCount}")
        name = os.path.split(filename)[1]
        graphs = {}
        filename = filename.strip(name)
        filename += f"cppConverterTemps/{name}"
        for i in range(fileCount):
            fName = filename + (str(i) + ".dot")
            graphName = os.path.splitext(fName)[0]
            graphName = os.path.split(graphName)[1]
            graphs[graphName] = Graph.fromFile(fName) 
        # self.cleanTemps()
        return graphs 

    def convertToStandardFormat(self, filename: str) -> int:
        '''
        Convert each dot file generated from the .cpp source to the same format
        as the dot files generated from Java CFGs.
        '''
        fNum = 0
        path = os.path.split(filename)[0]
        filename = os.path.split(filename)[1]
        files = glob2.glob(f"{path}/cppConverterTemps/*.dot")
        for name in files:
            if "global" in name.lower():
                os.remove(name)
                files.remove(name)
        for f in files:
            nodes = []
            edges = []
            nodeMap: Dict[str, str] = {}
            counter = 0
            
            # Make a temporary file (with the new content)
            with open(f'cppConverterTemps/{filename}{fNum}.dot', 'w') as newFile:
                with open(f'{f}', "r") as oldFile:
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
                            
                            nodeNameStr = nodeName.groups()[0].strip()
                            nodeMap[nodeNameStr] = str(counter)
                            nodeToAdd = str(counter)
                            if counter == 0:
                                nodeToAdd += " [label=\"START\"]" 

                            nodes.append(nodeToAdd)
                        
                            counter += 1
                        else: 
                            edges += [line]
                # Covers case of leaf CFGs
                if len(nodes) == 1:
                    nodes.append("1")
                    nodes.append("2")
                    counter += 2
                # Create the nodes and then the edges 
                for i, node in enumerate(nodes):
                    if i == counter - 2: 
                        node += "[label=\"EXIT\"]"
                    newFile.write(node + ";" + "\n")
                
                for edge in edges:
                    for name in nodeMap.keys():
                        edge = edge.replace(name, nodeMap[name]) 
                        edge = edge.replace(":s0", "")
                        edge = edge.replace(":s1", "")

                    newFile.write(edge + "\n")
                newFile.write("}")
                fNum += 1
        return fNum
        
    def createDotFiles(self, filepath: str, file_extension: str) -> None:
        '''
        Create a .dot file representing a control flow graph for
        each function from a .cpp file
        '''
        # Make sure the file extension begins with a '.'
        if file_extension[0] != '.':
            file_extension = f".{file_extension}"

        self.logger.d(f"Going to dir: {os.path.split(filepath)[0]}")
        os.chdir(os.path.split(filepath)[0])
        res = subprocess.check_call(["mkdir" , "-p", "cppConverterTemps"])

        c1_str = f"clang++-6.0 -emit-llvm -S {filepath}{file_extension} -o /dev/stdout"
        c2_str = "/usr/lib/llvm-6.0/bin/opt -dot-cfg"
        
        c1 = shlex.split(c1_str)
        c2 = shlex.split(c2_str) 

        self.logger.d(f"Command One: {c1}")
        self.logger.d(f"Command Two: {c2}")

        with subprocess.Popen(c1, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = False) as line1:
            command = line1.stdout
            if line1.stderr is not None: 
                errMsg = line1.stderr.read()
                if len(errMsg) == 0: 
                    self.logger.d(f"Got the following error msg: {str(errMsg)}") 

            with subprocess.Popen(c2, stdin=command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = False) as line2: 
               out, err = line2.communicate() 
                
        files = glob2.glob("*.dot")
        self.logger.d(f"Found the following .dot files: {files}")
        for f in files:
            subprocess.call(["mv", f"{f}", "cppConverterTemps"])
        
    def cleanTemps(self):
        """removes temp files and directories"""
        subprocess.call(["rm", "-r", "cppConverterTemps"]) 
