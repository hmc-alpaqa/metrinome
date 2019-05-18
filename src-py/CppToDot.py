import subprocess, argparse, glob2, os, re, sys

def parseArguments(args) -> str:
    '''
    Obtain the all of the arguments required (filename) from the command line 
    '''
    parser = argparse.ArgumentParser(description="Obtain Control Flow Graphs from an arbitrary .cpp File")
    parser.add_argument('--filename', '-f', help="Input Filename", required=True)
    args = vars(parser.parse_args(args))
    filename = args['filename']
    return filename 

def convertAllToStandard(): 
    '''
    Convert all of the dot files to standard format files 
    ''' 
    filelist = glob2.glob(os.path.join("ll/", "*.dot"), recursive=False)
    
    for file in filelist: 
        convertToStandardFormat(file)


def convertToStandardFormat(file: str): 
    '''
    Convert each dot file generated from the .cpp source to the same format 
    as the dot files generated from Java CFGs. 

    Note: this is required for the APC, NPath, and Cyclomatic complexity 
    algorithms to work, as they assume the dot files hae a particular 
    format 
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

def createDotFiles(filename):
    '''
    Create a dot file representing a control flow graph for 
    each function from a .cpp file
    '''
    command2 = f"clang++-6.0 -emit-llvm -S ../{filename}.cpp -o {os.path.basename(filename)}.ll"
    command3 = f"opt --dot-cfg {os.path.basename(filename)}.ll"
    command4 = f"rm {os.path.basename(filename)}.ll"
    commands = ["mkdir ll", "cd ll", command2, command3, command4]
    combinedCommands = "; ".join(commands)
    subprocess.call(combinedCommands, shell=True)
    
if __name__ == "__main__":
    '''
    The files will all be created in the ll directory
    '''
    filename = parseArguments(sys.argv[1:])
    createDotFiles(filename)
    convertAllToStandard()