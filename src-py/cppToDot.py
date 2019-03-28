import subprocess, argparse, glob2, os, re

if __name__ == "__main__":
    # TODO: figure out what the ":s0" and ":s1" are...
    # TODO: (are the start and end nodes correct?)
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--filename', help="Input Filename", required=True)
    args = vars(parser.parse_args())
    filename = args['filename']


    # Create all of the dot files 
    ex0 = "mkdir ll" 
    ex1 = "cd ll"
    ex2 = f"clang++-6.0 -emit-llvm -S ../{filename}.cpp -o {filename}.ll"
    ex3 = f"opt --dot-cfg {filename}.ll"
    ex4 = f"rm {filename}.ll"
    commands = [ex0, ex1, ex2, ex3, ex4]
    test = "; ".join(commands)
    subprocess.call(test, shell=True)
    
    # Get all files in the subdirectory 
    filelist = glob2.glob(os.path.join("ll/", "*.dot"), recursive=False)

    # Update each file to make the format of java CFGs
    for file in filelist: 
        nodes = []
        edges = []
        nodeMap = {}
        counter = 0
        # Make new file (temporary)
        with open(file + 'temp', 'w') as newFile:
            with open(file, "r") as oldFile:
                content = oldFile.readlines()
                newFile.write("digraph { \n")
                for line in content[1:]:
                    line = line.strip()

                    # Throw out the label for the graph and remove whitespace
                    if line.startswith("label") or line == "":
                        continue 

                    # If it contains a label (denoted by '[]'), it is 
                    # an edge 
                    name_pattern = "[a-zA-Z0-9]*"
                    isNode = re.match(name_pattern + " \[", line)
                    isNode = True if isNode is not None else False
                    if isNode:
                        nodeName = re.match(name_pattern + " ", line).group()
                        nodeMap[nodeName.strip()] = str(counter)
                        if counter == 0:
                            nodes += [str(counter) + " [label=\"START\"]"]
                        elif counter == 1: 
                            nodes += [str(counter) + " [label=\"EXIT\"]"]
                        else:  
                            nodes += [str(counter)]

                        counter += 1
                    else: 
                        edges += [line]
            

            for node in nodes:
                newFile.write(node + "\n")
            
            for edge in edges:
                for nodeName in nodeMap.keys():
                    edge = edge.replace(nodeName, nodeMap[nodeName]) 

                edge = edge.replace(":s0", "")
                edge = edge.replace(":s1", "")
                newFile.write(edge + "\n")

            print(nodeMap)