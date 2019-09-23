from cmd import Cmd
from metric import CyclomaticComplexity, NPathComplexity, PathComplexity 
from langToCFG import cpp, python, java
import os.path

def check_num_args(args, num_args, err1, err2):
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

def convert_args(args):
    return args.strip().split()

class MyPrompt(Cmd): 

    def __init__(self) -> None:
        cyclomatic = CyclomaticComplexity.CyclomaticComplexity()
        nPathComplexity = NPathComplexity.NPathComplexity() 
        pathComplexity = PathComplexity.PathComplexity() 
        self.metricsGenerators = [cyclomatic, nPathComplexity, pathComplexity] 

        cppConverter = cpp.CPPConvert()
        javaConverter = java.JavaConvert()
        pythonConverter = python.PythonConvert()
        self.graphGenerators = {
            ".cpp": cppConverter, 
            ".java": javaConverter, 
            ".py": pythonConverter, 
        }
        self.metrics = {}
        self.graphs = {}
        self.stats = {} 

        super(MyPrompt, self).__init__()

    def do_convert(self, args): 
        """
        Convert a file containing source code to a Graph object. 

        Usage: 
        convert <file>
        """
        args = convert_args(args) 
        ok = check_num_args(args, 1, "Must provide file name.", "Too many arguments provided.")
        if not ok: 
            return 
        file_name = args[0] 
        filename, file_extension = os.path.splitext(file_name)
        if file_extension not in self.graphGenerators.keys():
            print(f"Cannot convert {file_extension}")
            return
        
        converter = self.graphGenerators[file_extension]
        try: 
            graph = converter.toGraph(filename)
            print(graph)
            self.graphs[filename] = graph
        except FileNotFoundError as e: 
            print("File not found.")

    def do_list(self, args): 
        """
        List all of the objects of a specific type (either metrics or graphs). 

        Usage: 
        list <metrics/graphs>
        """
        args = convert_args(args) 
        ok = check_num_args(args, 1, "Must specify object type to list (metrics or graphs).", "Too many arguments provided.") 
        if not ok: 
            return
        type = args[0]
        if type == "metrics":
            print("Metric Names: ")
            print(" ".join(list(self.metrics.keys())))
        elif type == "graphs":
            print("Graph Names: ")
            print(" ".join(list(self.graphs.keys()))) 
        else:
            print(f"Type {type} not recognized")

    def do_show(self, args): 
        """
        Show an object of some type (either metric or graph).

        Usage 
        show <metric/graph> <name>
        """
        args = convert_args(args)
        ok = check_num_args(args, 2, "Must specify type (metric/graph) and name.", "Too many arguments provided")
        if not ok: 
            return 
        type = args[0]
        name = args[1] 
        if type == "metric":
            print(self.metrics[name]) 
        elif type == "graph":
            print(self.graphs[name])
        else: 
            print(f"Type {type} not recognized")

    def do_metrics(self, args): 
        """
        Compute all of the complexity matrics for a Graph object. 

        Usage: 
        metrics <name>
        """
        args = convert_args(args)
        ok = check_num_args(args, 1, "Must provide graph name.", "Too many arguments provided.")
        if not ok:
            return 

        name = args[0] 
        if name not in self.graphs: 
            print(f"Error, Graph {name} not found.")
            return

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

    def do_save(self, args):
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
                print(f"Type {type} not recognized")

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