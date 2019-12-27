import os.path
from os import listdir
from Log import Log
import readline
from pathlib import Path
import re
import logging
import importlib

from langToCFG import cpp, java, python
from metric import CyclomaticComplexity, NPathComplexity, PathComplexity


def get_files(path, recursiveMode, logger, allowedExtensions):
    '''
    get_files returns a list of files from the given path.

    If the path is a file, it returns a singleton containing the file.
    Otherwise, it returns all of the files in the current directory.
    If it is not a valid path, return no files.
    '''
    if os.path.isfile(path):
        if recursiveMode:
            logger.v("Cannot use recursive mode with filename.")
            return []

        return [path]
    elif os.path.isdir(path):
        if recursiveMode:
            allFiles = []
            for extension in allowedExtensions:
                allFiles += Path(path).rglob(f"*{extension}")
            for file in allFiles:
                print(file)
            return allFiles
        else:
            # Get all of the files in this directory
            return [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        # Check if it's a regular expression (only allowed at the END of the filename 
        base, file = os.path.split(path)
        try:
            regexp = re.compile(file)
            allFiles  = []
            if recursiveMode:
                allFiles += Path(base).rglob("*") # Get all files in all subdirectories 
            else:
                allFiles = [f for f in listdir(base) if os.path.isfile(os.path.join(base, f))]

            matchedFiles = []
            for file in allFiles:
                base, name = os.path.split(file)
                if regexp.match(name):
                    matchedFiles.append(file)

            return matchedFiles

        except re.error:
            # Try checking for just wildcard operators 
            file.replace(".", "\.")
            file.replace("*", ".*")
            try:
                regexp = re.compile(file)
                # TODO 
                return []
            except re.error:
                return [] 

class API:
    ''' API contains all of the methods exposed to the user.
    These are used to create the REPL.'''
    def __init__(self):
        self.controller = Controller()
        self.metrics = {}
        self.graphs = {}
        self.stats = {}

    def convert(self):
        pass

    def list_objects(self):
        pass

    def metrics(self):
        pass

    def show(self):
        pass

    def analyze(self):
        pass

    def export(self):
        pass

    def delete(self):
        pass

    def show_metrics(self):
        if len(self.metrics.keys()) == 0:
            self.logger.v("No metrics available.")
        else:
            self.logger.v("Metric Names: ")
            self.logger.v(" ".join(list(self.metrics.keys())))

    def show_graphs(self):
        if len(self.graphs.keys()) == 0:
            self.logger.v("No graphs available.")
        else:
            self.logger.v("Graph Names: ")
            self.logger.v(" ".join(list(self.graphs.keys())))

class Controller:
    '''
    Controller is the interface used to store which file extension we know
    how to generate graphs for.
    '''
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
        self.logger = Log("Complexity Repl:")

    def getGraphGeneratorNames(self):
        return self.graphGenerators.keys()

    def getGraphGenerator(self, file_extension):
        return self.graphGenerators[file_extension]

class Command:
    def __init__(self):
        self.api = API()
        self.logger = Log()
        self.have_completed = False

        # TODO: move 
        self.controller = Controller()
        self.metrics = {}
        self.graphs = {}
        self.stats = {}

    def check_num_args(self, args, num_args, err1, err2) -> bool:
        '''
        check_num_args returns True if the args list has num_elements many elements.
        Otherwise, print an error message.
        '''
        if len(args) < num_args:
            self.logger.v(err1)
        elif len(args) > num_args:
            self.logger.v(err2)
        else:
            return True

        return False

    def do_convert(self, args):
        args = self.convert_args(args)
        if len(args) == 0:
            self.logger.v("Must provide file name(s).")
            return

        recursiveMode = False
        if args[0] == "-r" or args[0] == "--recursive":
            recursiveMode = True
            args = args[1:]

        if len(args) == 0:
            self.logger.v("Must provide file name(s).")
            return

        # Iterate through all file-like objects
        allFiles = []
        allowedExtensions = list(self.controller.graphGenerators.keys())
        for arg in args:
            full_path = args[0]
            files = get_files(full_path, recursiveMode, self.logger, allowedExtensions)
            if files == []:
                self.logger.v(f"Could not get files from: {full_path}")
                return
            allFiles += files

        # Make sure files are valid (if using recursive mode this is done automatically in the previous step). 
        for file in allFiles:
            filepath, file_extension = os.path.splitext(file)
            if file_extension not in self.controller.getGraphGeneratorNames():
                if file_extension == "":
                    self.logger.v(f"No file extension found for {file}.")
                else:
                    self.logger.v(f"Cannot convert {file_extension} for {file}.")
                return

            converter = self.controller.getGraphGenerator(file_extension)
            graph = converter.toGraph(filepath.strip(), file_extension.strip())
            self.logger.v(graph)
            self.graphs[filepath] = graph

    def do_list(self, args):
        args = self.convert_args(args)
        ok = self.check_num_args(args, 1, "Must specify object type to list (metrics or graphs).", "Too many arguments provided.")
        if not ok:
            return
        type = args[0]
        if type == "metrics":
            self.show_metrics()
        elif type == "graphs":
            self.how_graphs()
        elif type == "*":
            self.show_metrics()
            self.show_graphs()
        else:
            self.logger.v(f"Type {type} not recognized")

    def do_metrics(self, args):
        args = self.convert_args(args)
        ok = self.check_num_args(args, 1, "Must provide graph name.", "Too many arguments provided.")
        if not ok:
            return

        name = args[0]
        names = [name]
        if name == "*":
            names = self.graphs.keys()
        elif name in self.graphs:
            pass
        else:
            try:
                pattern = re.compile(name)
                for graphName in self.graphs.keys():
                    if pattern.match(graphName):
                        names.append(graphName)
            except:
                self.logger.v(f"Error, Graph {name} not found.")
                return

        for name in names:
            graph = self.graphs[name]
            self.logger.v(f"Computing metrics for {graph}")
            results = []
            for metricGenerator in self.metricsGenerators:
                self.logger.v(f"Computing {metricGenerator.name()}")
                result = metricGenerator.evaluate(graph)
                results.append((metricGenerator.name(), result))
                self.logger.v(f"Got {result}")

            self.metrics[name] = results

    def do_show(self, args):
        args = self.convert_args(args)
        ok = self.check_num_args(args, 2, "Must specify type (metric/graph) and name.", "Too many arguments provided")
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
                    self.logger.v(self.metrics[name])
                else:
                    self.logger.v(f"Metric {name} not found.")
        elif type == "graph":
            if name == "*":
                names = self.graphs.keys()

            for name in names:
                if name in self.graphs:
                    self.logger.v(self.graphs[name])
                else:
                    self.logger.v(f"Graph {name} not found.")
        elif type == "*":
            if name == "*":
                names = self.metrics.keys() + [self.graphs.keys()]

            for name in names:
                found = False
                if name in self.graphs:
                    self.logger.v(self.graphs[name])
                    found = True
                if name in self.metrics:
                    self.logger.v(self.metrics[name])
                    found = True
                if not found:
                    self.logger.v(f"Metric or Graph {name} not found.")
        else:
            self.logger.v(f"Type {type} not recognized.")

    def do_analyze(self, args):
        args = self.convert_args(args)
        ok = self.check_num_args(args, 1, "Must provide metric name.", "Too many arguments provided.")
        if not ok:
            return

        metric_name = args[0]
        metric_names = []
        if metric_name in self.metrics.keys():
            metric_names.append(metric_name)
        elif metric_name == "*":
            metric_names = self.metrics.keys()
        else:
            self.logger.v(f"Could not find metric {metric_name}")
            return

        metric = self.metrics[metric_name]

    def do_quit(self, args):
        readline.write_history_file()
        args = self.convert_args(args)
        self.check_num_args(args, 0, "Quitting...", "Too many arguments provided.")
        raise SystemExit

    def do_export(self, args):
        ok = self.check_num_args(args, 2, "Must specify type and name.", "Too many arguments provided.")
        if not ok:
            return

        type = args[0]
        name = args[1]
        with open(name, "w+") as f:
            if type == "graphs":
                if name in self.graphs:
                    graph = self.graphs[name]
                    f.write(graph)
                elif name == "*":
                    for graphName in self.graphs.keys():
                        graph = self.graphs[name]
                        f.write(graph)
            elif type == "metrics":
                if name in self.metrics:
                    metric = self.metrics[name]
                    f.write(metric)
                elif name == "*":
                    for graphName in self.metrics.keys():
                        metric = self.metrics[name]
                        f.write(metric)
            elif type == "stats":
                if name in self.stats:
                    stat = self.stats[name]
                    f.write(stat)
                elif name == "*":
                    for graphName in self.stats.keys():
                        stat = self.stats[name]
                        f.write(stat)
            else:
                self.logger.v(f"Type {type} not recognized.")

    def do_delete(self, args):
        ok = self.check_num_args(args, 2, "Must specify type and name.", "Too many arguments provided.")
        if not ok:
            return

        type = args[0]
        name = args[1]
        if type == "graphs":
            try:
                del self.graph[name]
            except KeyError:
                self.logger.v(f"Graph {name} not found.")
        elif type == "metrics":
            try:
                del self.metrics[name]
            except KeyError:
                self.logger.v(f"Metric {name} not found.")
        elif type == "stats":
            try:
                del self.stats[name]
            except KeyError:
                self.logger.v(f"Statistics {name} not found.")
        elif type == "*":
            found = False
            for dict in [self.graph, self.metrics, self.stats]:
                try:
                    del dict[name]
                    found = True
                except KeyError:
                    pass
            if not found:
                self.logger.v(f"No {name} found of any type.")
        else:
            self.logger.v(f"Type {type} not recognized.")

    def convert_args(self, args):
        '''
        Obtain a list of arguments from a string.
        '''
        return args.strip().split()

    def complete(self, text, state):
        res = super().complete(text, state)
        # Try to do tab completion on a directory. Text contains the latest paremeter
        # text only contains the latest segment, which splits on / (and other characters)
        line = readline.get_line_buffer()
        if res == None:
            if not self.have_completed:
                starting_index = line[::-1].find(text[::-1])
                starting_index = len(line) - starting_index - 1
                if len(text) == 0:
                    starting_index = len(line) - 1
                if starting_index != -1:
                    while starting_index > 0:
                        if line[starting_index] == ' ':
                            break

                        starting_index -= 1
                    path = line[starting_index:]
                else:
                    print("This should not happen")
                    path = ""

                dirPath = path
                if not os.path.isdir(dirPath):
                    if os.path.dirname(dirPath) != "":
                        dirPath = os.path.dirname(dirPath)
                    else:
                        dirPath = "."

                subFiles = os.listdir(dirPath.strip())
                logging.info(f"DirPath {dirPath.strip()}")
                logging.info(f"Sub Files {subFiles}")
                matches = [match for match in subFiles if match.startswith(text)]
                if len(matches) == 1:
                    self.have_completed = True
                    return matches[0]
                else:
                    pass
                    print(f"\n{matches}\n> {line}", end="")
            else:
                self.have_completed = False
        else:
            self.have_completed = True

        return res
