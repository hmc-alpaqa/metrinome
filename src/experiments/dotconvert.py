import re
def multiConvert(names):
    calls = []
    outputFiles = []
    for name in names: 
        f = open(name, "r")
        l1 = f.readline()
        fl = re.compile('.* \"(.*)\" {')
        calls += [fl.findall(l1)[0]]
    for name in names:
        outputFiles += [convert(name, calls)]
    return outputFiles

def convert(name, calls):
    def flatten(tup):
        sum = ""
        for elem in tup:
            if elem in nodeDict.keys():
                elem = str(nodeDict[elem])
            sum += elem
        return sum
    with open(name, "rbU") as f:
        num_lines = sum(1 for _ in f)
    if num_lines == 5:
        return
    count = 0
    nodeDict = {}
    label = "START"
    f = open(name, "r")
    l1 = f.readline()
    fl = re.compile('(.* )\"(.*)\" ({)')
    firstline = fl.findall(l1)[0]
    name = firstline[1]
    if name[:3] == "&lt":
        return 
    firstline = (firstline[0], firstline[2])
    newname = "/app/code/experiments/function_calls/files/joern/clean/joern." + name + ".dot"
    k = open(newname, "w")
    k.write(flatten(firstline)+ "\n")
    l = f.readline()
    vl = re.compile('\"(\d*)\" \[label = <\((.*)')
    matches = vl.findall(l)
    while matches:
        nodeDict[matches[0][0]] = count
        ll = re.compile('^('+'|'.join(calls) + ')')
        call = ll.findall(matches[0][1])
        if call:
            label = "CALLS " + call[0]
        l = f.readline()
        matches = vl.findall(l)
        if not matches:
            label = "EXIT"
        if label:
            k.write(str(count) +  f" [label=\"{label}\"];\n")
        else:
            k.write(str(count) +  ";\n")
        
        count += 1
        label = ""
    
    vl = re.compile('(  )\"(\d*)\"( -> )\"(\d*)')
    matches = vl.findall(l)
    while(matches != []):
        k.write(flatten(matches[0]) + ";\n")
        l = f.readline()
        matches = vl.findall(l)
    k.write("}")
    return newname

