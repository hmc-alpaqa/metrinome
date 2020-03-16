from typing import List, Dict, Any, Callable
import os.path
from os import listdir
from Log import Log, LOG_LEVEL
import readline
from pathlib import Path
import re
import logging
import importlib
import subprocess
import tempfile
import time
from collections import namedtuple
from enum import Enum, auto


from langToCFG import cpp, java, python
from metric import CyclomaticComplexity, NPathComplexity, PathComplexity, Metric
from kleeUtils import KleeUtils

klee_stat = namedtuple("KleeStat", "tests paths instructions delta_t")

'''
List of all the error messages the REPL can throw. 
Use these for maintaining consistency, rather than putting strings directly in the 
log messages. 
'''
MISSING_FILENAME_ERR: str       = "Must provide file name."
MISSING_TYPE_AND_NAME_ERR: str  = "Must specify type and name."
MISSING_NAME_ERR: str           = "Must specify name."
NO_FILE_EXT_ERR: Callable[[str], str] = lambda fname: \
    f"No file extension found for {fname}."
NOT_IMPLEMENTED_ERR: str        = "Not implemened."
EXTENSION_ERR: Callable[[str, str], str]   = lambda target_type, file_extension: \
    f"File extension must be {target_type}, not {file_extension}."

class OBJ_TYPES(Enum): 
    GRAPH  = "graph" 
    METRIC = "metric"
    STAT   = "stat"
    KLEE   = "klee"
    ALL    = "*"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def getType(objType: str): 
        for i in OBJ_TYPES:
            if str(i) == objType or str(i) + "s" == objType: 
                return i

class KNOWN_EXTENSIONS(Enum): 
    C      = ".c"
    Python = ".py"
    BC     = ".bc"

def get_files(path: str, recursiveMode: bool, logger, allowedExtensions: List[str]):
    '''
    get_files returns a list of files from the given path.

    If the path is a file, it returns a singleton containing the file.
    Otherwise, it returns all of the files in the current directory.
    If it is not a valid path, return no files.
    '''
    logger.d(f"Looking for files given path {path}")
    if os.path.isfile(path): 
        logger.d("This is a file.")
        if recursiveMode:
            logger.v("Cannot use recursive mode with filename.")
            return []

        return [path]
    elif os.path.isdir(path):
        logger.d("This is a directory")
        if recursiveMode:   
            allFiles: List[Any] = []
            for extension in allowedExtensions:
                allFiles += Path(path).rglob(f"*{extension}")
            for file in allFiles:
                print(file)
            return allFiles
        else:
            # Get all of the files in this directory
            return [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))]
    else:
        logger.d("Checking if it's a regular expression")
        # Check if it's a regular expression (only allowed at the END of the filename)
        base, file = os.path.split(path)
        logger.d(f"base: {base} file: {file}")
        try:
            regexp = re.compile(file)
            logger.d(f"Successfully compiled as a regular expression")
            allFiles  = []
            if os.path.exists(base):
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
            
            return []

        except (re.error):
            # Try checking for just wildcard operators 
            logger.d("Checking for wildcard operators")
            file.replace(".", "\.")
            file.replace("*", ".*")
            try:
                regexp = re.compile(file)
                # TODO 
                return []
            except re.error:
                return [] 

class API:
    ''' 
    API contains all of the methods exposed to the user.
    These are used to create the REPL.
    '''
    def __init__(self, logger) -> None:
        '''
        Create a new instance of the API.
        '''
        self.controller = Controller(logger)
        self.metrics: Dict[Any, Any] = {}
        self.graphs: Dict[Any, Any] = {}
        self.stats: Dict[Any, Any] = {}

        self.logger = logger 

    def show_metrics(self) -> None:
        if len(self.metrics.keys()) == 0:
            self.logger.v("No metrics available.")
        else:
            self.logger.v("Metric Names: ")
            self.logger.v(" ".join(list(self.metrics.keys())))

    def show_graphs(self) -> None:
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
    def __init__(self, logger) -> None:
        '''
        Create a new instance of Controller, initializing all of the converters 
        required to turn known file types into CFGS.
        '''
        self.logger = logger

        cyclomatic = CyclomaticComplexity.CyclomaticComplexity()
        nPathComplexity = NPathComplexity.NPathComplexity()
        pathComplexity = PathComplexity.PathComplexity()
        self.metricsGenerators: List[Metric.Metric] = [cyclomatic, nPathComplexity, pathComplexity]

        cppConverter = cpp.CPPConvert(self.logger)
        javaConverter = java.JavaConvert()
        pythonConverter = python.PythonConvert()
        self.graphGenerators = {
            ".cpp": cppConverter,
            ".c": cppConverter, 
            ".jar": javaConverter,
            ".class": javaConverter,
            ".java": javaConverter,
            ".py": pythonConverter,
        }

    def getGraphGeneratorNames(self):
        '''
        Get the names of all file extensions we know how to generate 
        CFGs for. 
        '''
        return self.graphGenerators.keys()

    def getGraphGenerator(self, file_extension: str):
        '''
        Given a file extension as a string, return the CFG generator for that 
        file extension. 
        '''
        return self.graphGenerators[file_extension]

class Command:  
    '''
    Command is the implementation of the REPL commands. 
    '''
    def __init__(self, debug_mode: bool, replWrapper) -> None:
        if debug_mode: 
            self.logger = Log(log_level=LOG_LEVEL.DEBUG)
        else: 
            self.logger = Log(log_level=LOG_LEVEL.REGULAR)

        self.logger.d("Debug Mode Enabled")
        self.api = API(self.logger)
        
        self.have_completed = False

        self.controller = Controller(self.logger)
        self.metrics: Dict[Any, Any] = {}
        self.graphs: Dict[Any, Any] = {}
        self.stats: Dict[Any, Any] = {}
        self.klee_stats: Dict[Any, Any] = {}
        self.klee_stat = klee_stat
        
        self.kleeUtils = KleeUtils(self.logger)
        self.kleeFormattedFiles: Dict[str, str] = dict()
        self.bcFiles: Dict[str, Any] = dict()

        self.replWrapper = replWrapper

    def check_num_args(self, args: List[str], num_args: int,
                       err1: str, 
                       err2: str="Too many arguments provided.") -> bool:
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

    def verify_file_type(self, args, target_type: str):
        file = args[0]
        filepath, file_extension = os.path.splitext(file)
        if file_extension == "":
            self.logger.v(NO_FILE_EXT_ERR(file))
            return 0
        elif file_extension.strip() != f".{target_type}":
            self.logger.v(EXTENSION_ERR(target_type, file_extension))
            return 0

        return file

    def do_klee_replay(self, args: str): 
        convertedArgs = self.convert_args(args)
        ok = self.check_num_args(convertedArgs, 1, MISSING_FILENAME_ERR)
        if not ok:
            return

        result = self.verify_file_type(args, "ktest")
        if result == 0:
            return

        path_to_klee_build_dir = '/app/build'
        s = 'export LD_LIBRARY_PATH={path_to_klee_build_dir}/lib/:$LD_LIBRARY_PATH'
        s2 = "gcc -I ../../include -L path-to-klee-build-dir/lib/ get_sign.c -lkleeRuntest"

    def do_convert(self, args: str):
        args = self.convert_args(args)
        if len(args) == 0:
            self.logger.v(MISSING_FILENAME_ERR)
            return

        recursiveMode = False
        if args[0] == "-r" or args[0] == "--recursive":
            recursiveMode = True
            args = args[1:]

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

        self.logger.d(f"Convert files {allFiles}")
        # Make sure files are valid (if using recursive mode this is done automatically in the previous step). 
        for file in allFiles:
            filepath, file_extension = os.path.splitext(file)
            if file_extension not in self.controller.getGraphGeneratorNames():
                if file_extension == "":
                    self.logger.v(NO_FILE_EXT_ERR(file))
                else:
                    self.logger.v(f"Cannot convert {file_extension} for {file}.")
                return

            converter = self.controller.getGraphGenerator(file_extension)
            graph = converter.toGraph(filepath.strip(), file_extension.strip())
            self.logger.v(graph)
            if isinstance(graph, dict):
                self.graphs.update(graph)
            else:
                self.graphs[filepath] = graph

    def do_list(self, args: str):
        convertedArgs = self.convert_args(args)
        ok = self.check_num_args(convertedArgs, 1, 
            "Must specify object type to list (metrics, graphs, or klee).")
        if not ok:
            return

        type = args[0]
        type = OBJ_TYPES.getType(type)
        if type == OBJ_TYPES.METRIC:
            self.api.show_metrics()
        elif type == OBJ_TYPES.GRAPH:
            self.api.show_graphs()
        elif type == OBJ_TYPES.KLEE:
            keys = self.kleeFormattedFiles.keys()
            if len(keys) == 0:
                self.logger.v("No KLEE formatted files available.")
            else:
                self.logger.v("KLEE-Formatted file names: ")
                self.logger.v(" ".join(list(keys)))

            keys = self.bcFiles.keys()
            if len(keys) == 0:
                self.logger.v("No BC files available.")
            else:
                self.logger.v("BC file names: ")
                self.logger.v(" ".join(list(keys)))
        elif type == "*":
            self.api.show_metrics()
            self.api.show_graphs()
        else:
            self.logger.v(f"Type {type} not recognized")

    def do_metrics(self, args: str):
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 1, "Must provide graph name.")
        if not ok:
            return

        name = argsList[0]
        names = [name]
        if name == "*":
            names = list(self.graphs.keys())
        elif name in self.graphs:
            pass
        else:
            try:
                self.logger.d(f"Trying to compile {name} to regexp")
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
            for metricGenerator in self.controller.metricsGenerators:
                self.logger.v(f"Computing {metricGenerator.name()}")
                result = metricGenerator.evaluate(graph)
                results.append((metricGenerator.name(), result))
                self.logger.v(f"Got {result}")

            self.metrics[name] = results

    def do_show(self, args: str):
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 2, "Must specify type (metric/graph) and name.")
        if not ok:
            return
        type = args[0]
        name = args[1]
        names = [name]
        type = OBJ_TYPES.getType(type)
        if type == OBJ_TYPES.METRIC:
            if name == "*":
                names = list(self.metrics.keys())

            for name in names:
                if name in self.metrics:
                    self.logger.v(self.metrics[name])
                else:
                    self.logger.v(f"Metric {name} not found.")
        elif type == OBJ_TYPES.GRAPH:
            if name == "*":
                names = list(self.graphs.keys())

            for name in names:
                if name in self.graphs:
                    self.logger.v(self.graphs[name])
                else:
                    self.logger.v(f"Graph {name} not found.")
        elif type == "*":
            if name == "*":
                names = list(self.metrics.keys()) + [self.graphs.keys()]

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
        elif type == OBJ_TYPES.KLEE:
            for name in names: 
                if name in self.bcFiles:
                    self.logger.v("BC FILE:")
                    self.logger.v(self.bcFiles[name])

                if name in self.kleeFormattedFiles:
                    self.logger.v("KLEE FORMATTED FILES:")
                    self.logger.v(str(self.kleeFormattedFiles)) 
        else:
            self.logger.v(f"Type {type} not recognized.")

    def do_analyze(self, args: str):
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 1, "Must provide metric name.")
        if not ok:
            return

        metric_name = argsList[0]
        metric_names = []
        if metric_name in self.metrics.keys():
            metric_names.append(metric_name)
        elif metric_name == "*":
            metric_names = list(self.metrics.keys())
        else:
            self.logger.v(f"Could not find metric {metric_name}")
            return

        for metric_name in metric_names: 
            metric = self.metrics[metric_name]

    def do_klee_to_bc(self, args: str): 
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 1, "Must provide KLEE formatted name.")
        if not ok:
            return

        name = args[0]
        keys = [name]

        if name not in self.kleeFormattedFiles: 
            self.logger.v(f"Could not find {name}.") 
            return
        
        if name == "*": 
            keys = list(self.kleeFormattedFiles.keys())

        for key in keys: 
            with tempfile.NamedTemporaryFile(delete = True, suffix=".c") as fp:
                self.logger.d(f"Created temporary file {fp.name}")
                self.logger.d(f"Going to write {self.kleeFormattedFiles[name]}") 
                fp.write(self.kleeFormattedFiles[name].encode())
                
                fp.seek(0)
                self.logger.d("FILE CONTENTS")
                self.logger.d(fp.read().decode())

                cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone  -o /dev/stdout {fp.name}"
                res = subprocess.run(cmd, shell=True, capture_output=True)  
                self.bcFiles[name] = res.stdout

    def do_to_klee_format(self, args: str): 
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 1, MISSING_FILENAME_ERR)
        recursiveMode = False
        if not ok: 
            ok = self.check_num_args(argsList, 2, "", "")
            if not ok : 
                return 
            
            if args[0] is "-r": 
                recursiveMode = True
                filePath = args[1] 
            else: 
                return 
        else: 
            filePath = args[0]
            

        self.logger.d(f"Recursive Mode is {recursiveMode}")
        files = get_files(filePath, recursiveMode, self.logger, [str(KNOWN_EXTENSIONS.C)])
        if len(files) == 0:
            self.logger.v(f"Could not find any files for {filePath}") 
            return

        self.logger.d(f"Got files {files}")
        for file in files: 
            kleeFormattedFiles = self.kleeUtils.show_func_defs(file)
            if kleeFormattedFiles is None: 
                return 
            self.kleeFormattedFiles = {**self.kleeFormattedFiles, **kleeFormattedFiles}

    def do_clean_klee_files(self, args: str): 
        convertedArgs = self.convert_args(args)
        ok = self.check_num_args(convertedArgs, 0, NOT_IMPLEMENTED_ERR)
        if not ok:
            return

    def update_klee_stats(self, klee_output, name: str, delta_t):
        s1 = "generated tests = "
        s2 = "completed paths = "
        s3 = "total instructions = "

        generated_tests_index    = klee_output.index(s1) + len(s1) 
        completed_paths_index    = klee_output.index(s2) + len(s2)
        total_instructions_index = klee_output.index(s3) + len(s3)

        p = re.compile("[0-9]+")

        testsMatch = p.match(klee_output[generated_tests_index:])
        pathsMatch = p.match(klee_output[completed_paths_index:])
        instsMatch = p.match(klee_output[total_instructions_index:])

        if testsMatch is not None:
            tests = int(testsMatch.group())
        if pathsMatch is not None:
            paths = int(pathsMatch.group())
        if instsMatch is not None:
            insts = int(instsMatch.group())

        self.klee_stats[name] = self.klee_stat(tests=tests, paths=paths, instructions=insts, delta_t=delta_t)
        self.logger.i("Updated!")

    def do_klee(self, args: str): 
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 1, MISSING_FILENAME_ERR)
        if not ok:
            return

        name = args[0] 
        
        if args[0] in self.bcFiles or args[0] == "*":
            if args[0] == "*": 
                keys = list(self.bcFiles.keys())
            else:
                keys = [name]

            for key in keys: 
                with tempfile.NamedTemporaryFile(delete = True, suffix=".bc") as fp:
                    fileName = fp.name
                    self.logger.d(f"Created temporary file {fileName}")
                
                    thingToWrite = self.bcFiles[key]
                    self.logger.d(f"Writing {thingToWrite}")
                    fp.write(thingToWrite)
                    fp.seek(0)
                    
                    cmd = f"/app/build/bin/klee {fileName}"
                    self.logger.d(f"Going to execute {cmd}")
                    st = time.time() 
                    res = subprocess.run(cmd, shell=True, capture_output=True)
                    delta_t = time.time() - st
                    output = res.stderr
                    self.logger.d(output.decode())
                    self.logger.d("Updating Klee Stats")
                    self.update_klee_stats(output.decode(), key, delta_t)
        else:
            result = self.verify_file_type(args, "bc")
            if result is 0: 
                return 
            
            files = get_files(result, False, self.logger, [str(KNOWN_EXTENSIONS.BC)])
            if len(files) == 0: 
                self.logger.e(f"Could not find any files matching {result}")
                return

            self.logger.d(f"Obtained {files}")

            for file in files:
                cmd = f"/app/build/bin/klee {result}"
                self.logger.d(cmd)
                st = time.time() 
                res = subprocess.run(cmd, shell=True, capture_output=True) 
                delta_t = time.time() - st
                output = res.stderr
                self.logger.d("OUTOUT:") 
                self.logger.d(output.decode())
                self.update_klee_stats(output.decode(), args[0], delta_t)
                
    def do_quit(self, args: str):
        readline.write_history_file()
        convertedArgs = self.convert_args(args)
        self.check_num_args(convertedArgs, 0, "Quitting...")
        raise SystemExit

    def do_export(self, args: str):
        convertedArgs = self.convert_args(args)
        ok = self.check_num_args(convertedArgs, 2, MISSING_TYPE_AND_NAME_ERR)
        if not ok:
            return

        exportType = args[0]
        name = args[1]
        subprocess.check_call(["mkdir" , "-p", "exports"])
        newName = os.path.split(name)[1]
        exportType = OBJ_TYPES.getType(exportType)
        if exportType == OBJ_TYPES.GRAPH:    
            if name in self.graphs:
                with open(f"/app/code/exports/{newName}.dot", "w+") as f:
                    graph = self.graphs[name]
                    f.write(graph.dot())
                    self.logger.i(f"Made file {newName}.dot in /app/code/exports/")
            elif name == "*":
                for graphName in self.graphs.keys():
                    fName = os.path.split(graphName)[1]
                    with open(f"/app/code/exports/{fName}.dot", "w+") as f: 
                        graph = self.graphs[graphName]
                        f.write(graph.dot())
                        self.logger.i(f"Made file {fName}.dot in /app/code/exports/")
            else: 
                self.logger.e(f"{str(exportType).capitalize()} {name} not found.")

        elif exportType == OBJ_TYPES.METRIC:
            if name in self.metrics:
                with open(f"/app/code/exports/{newName}_metrics", "w+") as f:
                    metric = self.metrics[name]
                    f.write(metric)
                    self.logger.i(f"Made file {newName}_metrics in /app/code/exports/")
            elif name == "*":
                for mName in self.metrics.keys():
                    fName = os.path.split(mName)[1]
                    with open(f"/app/code/exports/{fName}_metrics", "w+") as f: 
                        metric = self.metrics[mName]
                        f.write(metric)
                        self.logger.i(f"Made file {fName}_metrics in /app/code/exports/")
            else: 
                self.logger.e(f"{str(exportType).capitalize()} {name} not found.")

        elif exportType == OBJ_TYPES.STAT:
            if name in self.stats:
                with open(f"/app/code/exports/{newName}_stats", "w+") as f:
                    stat = self.stats[name]
                    f.write(stat)
                    self.logger.i(f"Made file {newName}_stats in /app/code/exports/")

            elif name == "*":
                for sName in self.stats.keys():
                    fName = os.path.split(sName)[1]
                    with open(f"/app/code/exports/{fName}_stats", "w+") as f: 
                        stat = self.metrics[sName]
                        f.write(stat)
                        self.logger.i(f"Made file {fName}s_stats in /app/code/exports/.")
            else:
                self.logger.e(f"{str(exportType).capitalize()} {name} not found.")
        
        elif exportType == OBJ_TYPES.KLEE:
            if name in self.kleeFormattedFiles:
                with open(f"/app/code/exports/{newName}_klee.c", "w+") as f:
                    kleeFile = self.kleeFormattedFiles[name]
                    f.write(kleeFile)
                    self.logger.i(f"Made file {newName}_klee.c in /app/code/exports/.")
        else:
            self.logger.v(f"Type {exportType} not recognized.")

    def do_delete(self, args: str): 
        argsList = self.convert_args(args)
        ok = self.check_num_args(argsList, 2, MISSING_TYPE_AND_NAME_ERR)
        if not ok:
            return

        type = args[0]
        name = args[1]
        if type == OBJ_TYPES.GRAPH.value:
            try:
                del self.graphs[name]
            except KeyError:
                self.logger.v(f"{OBJ_TYPES.GRAPH.value.capitalize()} {name} not found.")
        elif type == OBJ_TYPES.METRIC.value:
            try:
                del self.metrics[name]
            except KeyError:
                self.logger.v(f"{OBJ_TYPES.METRIC.value.capitalize()} {name} not found.")
        elif type == OBJ_TYPES.STAT.value:
            try:
                del self.stats[name]
            except KeyError:
                self.logger.v(f"{OBJ_TYPES.STAT.value.capitalize()} {name} not found.")
        elif type == "*":
            found = False
            for dict in [self.graphs, self.metrics, self.stats]:
                try:
                    del dict[name]
                    found = True
                except KeyError:
                    pass
            if not found:
                self.logger.v(f"No {name} found of any type.")
        else:
            self.logger.v(f"Type {type} not recognized.")

    def convert_args(self, args: str):
        '''
        Obtain a list of arguments from a string.
        '''
        return args.strip().split()

    def complete(self, text, state):
        res = self.replWrapper.complete(text, state)
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
