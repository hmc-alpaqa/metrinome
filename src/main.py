import os.path
from os import listdir
from cmd import Cmd

from langToCFG import cpp, java, python
from metric import CyclomaticComplexity, NPathComplexity, PathComplexity

def check_num_args(args, num_args, err1, err2) -> bool:
    '''
    check_num_args returns True if the args list has num_elements many elements. 
    Otherwise, print an error message. 
    '''
    if len(args) < num_args: 
        print(err1)
        return False 
    elif len(args) > num_args: 
        print(err2)  
        return False 

    return True

def get_files(path):
    '''
    get_files returns a list of files from the given path. 

    If the path is a file, it returns a singleton containing the file. 
    Otherwise, it returns all of the files in the current directory.
    If it is not a valid path, return no files. 
    '''
    if os.path.isfile(path): 
        return [path]
    elif os.path.isdir(path): 
        return [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))] # TODO 
    else: 
        return []

class Controller: 
    def __init__(self) -> None:
        '''
        '''
        cyclomatic = CyclomaticComplexity.CyclomaticComplexity()
        nPathComplexity = NPathComplexity.NPathComplexity() 
        pathComplexity = PathComplexity.PathComplexity() 
        self.metricsGenerators = [cyclomatic, nPathComplexity, pathComplexity] 

        cppConverter = cpp.CPPConvert()
        javaConverter = java.JavaConvert()
        pythonConverter = python.PythonConvert()
        self.graphGenerators = {
            ".cpp": cppConverter, 
            ".jar": javaConverter, 
            ".class": javaConverter,
            ".java": javaConverter,
            ".py": pythonConverter, 
        }

    def getGraphGeneratorNames(self):
        return self.graphGenerators.keys()

    def getGraphGenerator(self, file_extension):
        return self.graphGenerators[file_extension]

class MyPrompt(Cmd): 

    def __init__(self) -> None:
        '''
        '''
        self.controller = Controller()
        self.metrics = {}
        self.graphs = {}
        self.stats = {} 
        super(MyPrompt, self).__init__()

    def convert_args(self, args): 
        '''
        '''
        return args.strip().split()

    def do_convert(self, args): 
        """
        Convert a file containing source code to a Graph object. 

        Usage: 
        convert <file>
        """
        args = self.convert_args(args) 
        ok = check_num_args(args, 1, "Must provide file name.", "Too many arguments provided.")
        if not ok: 
            return 
        full_path = args[0] 
        files = get_files(full_path)
        if files == []:
            print(f"Invalid path: {full_path}")
            return 

        for file in files: 
            filepath, file_extension = os.path.splitext(file)

            if file_extension not in self.controller.getGraphGeneratorNames():
                if file_extension == "":
                    print(f"No file extension found for {file}.")
                else:
                    print(f"Cannot convert {file_extension} for {file}.")
                return
        
            converter = self.controller.getGraphGenerator(file_extension)
            graph = converter.toGraph(filepath.strip(), file_extension.strip())
            print(graph)
            self.graphs[filepath] = graph

    def do_list(self, args): 
        """
        List all of the objects of a specific type (either metrics or graphs). 

        Usage: 
        list <metrics/graphs>
        list * 
        """
        def show_metrics():
            if len(self.metrics.keys()) == 0:
                print("No metrics available.")
            else:
                print("Metric Names: ")
                print(" ".join(list(self.metrics.keys())))

        def show_graphs():
            if len(self.graphs.keys()) == 0:
                print("No graphs available.")
            else:
                print("Graph Names: ")
                print(" ".join(list(self.graphs.keys()))) 

        args = self.convert_args(args) 
        ok = check_num_args(args, 1, "Must specify object type to list (metrics or graphs).", "Too many arguments provided.") 
        if not ok: 
            return
        type = args[0]
        if type == "metrics":
            show_metrics()
        elif type == "graphs":
            show_graphs()
        elif type == "*":
            show_metrics()
            show_graphs()
        else:
            print(f"Type {type} not recognized")

    def do_show(self, args): 
        """
        Show an object of some type (either metric or graph).

        Usage 
        show <metric/graph> <name>
        show <metric/graph> * 
        """
        args = self.convert_args(args)
        ok = check_num_args(args, 2, "Must specify type (metric/graph) and name.", "Too many arguments provided")
        if not ok: 
            return 
        type = args[0]
        name = args[1] 
        names = [name]
        if type == "metric":
            if name == "*": 
                names = self.metrics.keys()

            for name in names:
                if name in self.metrics:
                    print(self.metrics[name]) 
                else:
                    print(f"Metric {name} not found.")
        elif type == "graph":
            if name == "*": 
                names = self.graphs.keys()
            
            for name in names: 
                if name in self.graphs:
                    print(self.graphs[name])
                else: 
                    print(f"Graphs {name} not found.")      
        else: 
            print(f"Type {type} not recognized.")

    def do_metrics(self, args): 
        """
        Compute all of the complexity matrics for a Graph object. 

        Usage: 
        metrics <name>
        metrics * 
        """
        args = convert_args(args)
        ok = check_num_args(args, 1, "Must provide graph name.", "Too many arguments provided.")
        if not ok:
            return 

        name = args[0] 
        names = [name]
        if name == "*":
            names = self.graphs.keys()
        elif name not in self.graphs:
            print(f"Error, Graph {name} not found.")
            return

        for name in names: 
            graph = self.graphs[name]
            print(f"Computing metrics for {graph}")
            results = []
            for metricGenerator in self.metricsGenerators:
                print(f"Computing {metricGenerator.name()}")
                result = metricGenerator.evaluate(graph)
                results.append((metricGenerator.name(), result)) 
                print(f"Got {result}") 

            self.metrics[name] = results 

    def do_analyze(self, args): 
        """
        Perform statistical analysis on a set of generated metrics. 

        Usage: 
        analyze <metric names>
        """
        args = convert_args(args) 
        ok = check_num_args(args, 1, "Must provide metric name.", "Too many arguments provided.")
        if not ok: 
            return 
        metric_name = args[0]
        if metric_name not in self.metrics.keys():
            print(f"Could not find metric {metric_name}")
            return 
        
        metric = self.metrics[metric_name]

    def do_delete(self, args): 
        """
        Delete an object (type Graph, Metrics, or States) from memory. 

        Usage: 
        delete <type> <name>
        """
        ok = check_num_args(args, 2, "Must specify type and name.", "Too many arguments provided.")
        if not ok: 
            return 

        type = args[0]
        name = args[1]
        if type == "graphs": 
            try: 
                del self.graph[name] 
            except KeyError: 
                print(f"Graph {name} not found.")
        elif type == "metrics": 
            try:
                del self.metrics[name]
            except KeyError:
                print(f"Metric {name} not found.")
        elif type == "stats":
            try:
                del self.stats[name] 
            except KeyError:
                print(f"Statistics {name} not found.")
        else:
            print(f"Type {type} not recognized.")

    def do_export(self, args):
        """
        Save an object (type Graph, Metrics, or Stats) to an output file. 

        Usage:
        save <type> <name>
        """
        ok = check_num_args(args, 2, "Must specify type and name.", "Too many arguments provided.")
        if not ok: 
            return 

        type = args[0]
        name = args[1] 
        with open(name, "w+") as f:
            if type == "graphs":
                if name in self.graphs: 
                    graph = self.graphs[name]
                    f.write(graph)
            elif type == "metrics": 
                if name in self.metrics:
                    metric = self.metrics[name]
                    f.write(metric)  
            elif type == "stats":
                if name in self.stats: 
                    stat = self.stats[name] 
                    f.write(stat)
            else:
                print(f"Type {type} not recognized.")

    def do_quit(self, args): 
        """
        Quits the path complexity repl
        """
        args = convert_args(args) 
        check_num_args(args, 0, "Quitting...", "Too many arguments provided.")
        raise SystemExit 

if __name__ == "__main__":
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting path complexity repl...')
