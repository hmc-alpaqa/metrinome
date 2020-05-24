"""The main implementation of the REPL."""

from typing import List, Dict, Any, Callable, Optional
import os.path
from os import listdir
import readline
from pathlib import Path
import re
import subprocess
import tempfile
import time
from collections import namedtuple
from enum import Enum
from log import Log, LogLevel
from metric import path_complexity, cyclomatic_complexity, npath_complexity, metric

from lang_to_cfg import cpp, java, python
from klee_utils import KleeUtils
from utils import Timeout

KleeStat = namedtuple("KleeStat", "tests paths instructions delta_t")

"""
List of all the error messages the REPL can throw.
Use these for maintaining consistency, rather than putting strings directly in the
log messages.
"""
MISSING_FILENAME_ERR: str = "Must provide file name."
MISSING_TYPE_AND_NAME_ERR: str = "Must specify type and name."
MISSING_NAME_ERR: str = "Must specify name."
NO_FILE_EXT_ERR: Callable[[str], str] = lambda f_name: \
    f"No file extension found for {f_name}."
NOT_IMPLEMENTED_ERR: str = "Not implemened."
EXTENSION_ERR: Callable[[str, str], str] = lambda target_type, file_extension: \
    f"File extension must be {target_type}, not {file_extension}."


class ObjTypes(Enum):
    """All of the object types that are stored by the REPL while it is running."""

    GRAPH  = "graph"
    METRIC = "metric"
    STAT   = "stat"
    KLEE   = "klee"
    KLEE_STATS = "klee_stat"
    KLEE_BC = "klee_bc"
    KLEE_FILE = "klee_file"
    ALL    = "*"

    def __str__(self) -> str:
        """Convert one of the enum objects to a string."""
        return str(self.value)

    @staticmethod
    def get_type(obj_type: str):
        """Given an input string, see if there is an enum type that matches it."""
        for i in ObjTypes:
            if str(i) == obj_type.lower() or str(i) + "s" == obj_type.lower():
                return i

        return None


class KnownExtensions(Enum):
    """A list of all the file extensions we know how to work with."""

    C      = ".c"
    Python = ".py"
    BC     = ".bc"


def get_files(path: str, recursive_mode: bool, logger, allowed_extensions: List[str]):
    """
    get_files returns a list of files from the given path.

    If the path is a file, it returns a singleton containing the file.
    Otherwise, it returns all of the files in the current directory.
    If it is not a valid path, return no files.
    """
    logger.d_msg(f"Looking for files given path {path}")
    if os.path.isfile(path):
        logger.d_msg("This is a file.")
        if recursive_mode:
            logger.v_msg("Cannot use recursive mode with filename.")
            return []

        return [path]

    if os.path.isdir(path):
        logger.d_msg("This is a directory")
        if recursive_mode:
            all_files: List[Any] = []
            for extension in allowed_extensions:
                all_files += Path(path).rglob(f"*{extension}")
            for file in all_files:
                print(file)
            return all_files

        # Get all of the files in this directory
        return [f for f in listdir(path) if os.path.isfile(os.path.join(path, f))]

    logger.d_msg("Checking if it's a regular expression")
    # Check if it's a regular expression (only allowed at the END of the filename)
    base, file = os.path.split(path)
    logger.d_msg(f"base: {base} file: {file}")
    try:
        regexp = re.compile(file)
        logger.d_msg(f"Successfully compiled as a regular expression")
        all_files = []
        if os.path.exists(base):
            if recursive_mode:
                all_files += Path(base).rglob("*")  # Get all files in all subdirectories
            else:
                all_files = [f for f in listdir(base) if os.path.isfile(os.path.join(base, f))]

            matched_files = []
            for file in all_files:
                base, name = os.path.split(file)
                if regexp.match(name):
                    matched_files.append(file)

            return matched_files

        return []

    except re.error:
        # Try checking for just wildcard operators
        logger.d_msg("Checking for wildcard operators")
        file.replace(".", r"\.")
        file.replace("*", ".*")
        try:
            regexp = re.compile(file)
            # TODO
        except re.error:
            pass

        return []


class Controller:
    """Store the file extension we know how to generate graphs for and the generators."""

    def __init__(self, logger) -> None:
        """
        Create a new instance of Controller by initializing all of the converters.

        The converters turn known file types into CFGS.
        """
        self.logger = logger

        cyclomatic = cyclomatic_complexity.CyclomaticComplexity()
        npath = npath_complexity.NPathComplexity()
        pathcomplexity = path_complexity.PathComplexity(self.logger)
        self.metrics_generators: List[metric.MetricAbstract] = [cyclomatic, npath, pathcomplexity]

        cpp_converter = cpp.CPPConvert(self.logger)
        java_converter = java.JavaConvert()
        python_converter = python.PythonConvert()
        self.graph_generators = {
            ".cpp": cpp_converter,
            ".c": cpp_converter,
            ".jar": java_converter,
            ".class": java_converter,
            ".java": java_converter,
            ".py": python_converter,
        }

    def get_graph_generator_names(self):
        """Get the names of all file extensions we know how to generate CFGs for."""
        return self.graph_generators.keys()

    def get_graph_generator(self, file_extension: str):
        """Given a file extension as a string, return the CFG generator for that file extension."""
        return self.graph_generators[file_extension]


class Data:
    """Stores all of objects created during the use of the REPL."""

    def __init__(self, logger):
        """Create a new instance of the REPL data."""
        self.metrics: Dict[Any, Any] = {}
        self.graphs: Dict[Any, Any] = {}
        self.stats: Dict[Any, Any] = {}
        self.klee_stats: Dict[Any, Any] = {}
        self.klee_stat = KleeStat
        self.klee_formatted_files: Dict[str, str] = dict()
        self.bc_files: Dict[str, Any] = dict()
        self.logger = logger

    def export_metrics(self, name, new_name):
        """Save a metric  the REPL knows about to an external file."""
        if name in self.metrics:
            with open(f"/app/code/exports/{new_name}_metrics", "w+") as file:
                metric_value = self.metrics[name]
                file.write(metric_value)
                self.logger.i_msg(f"Made file {new_name}_metrics in /app/code/exports/")
        elif name == "*":
            for m_name in self.metrics:
                f_name = os.path.split(m_name)[1]
                with open(f"/app/code/exports/{f_name}_metrics", "w+") as file:
                    metric_value = self.metrics[m_name]
                    file.write(metric_value)
                    self.logger.i_msg(f"Made file {f_name}_metrics in /app/code/exports/")
        else:
            self.logger.e_msg(f"{str(ObjTypes.METRIC).capitalize()} {name} not found.")

    def export_graph(self, name, new_name) -> None:
        """Save a Graph the REPL knows about to an external file."""
        if name in self.graphs:
            with open(f"/app/code/exports/{new_name}.dot", "w+") as file:
                graph = self.graphs[name]
                file.write(graph.dot(True))
                self.logger.i_msg(f"Made file {new_name}.dot in /app/code/exports/")
        elif name == "*":
            for graph_name in self.graphs:
                f_name = os.path.split(graph_name)[1]
                with open(f"/app/code/exports/{f_name}.dot", "w+") as file:
                    graph = self.graphs[graph_name]
                    file.write(graph.dot(True))
                    self.logger.i_msg(f"Made file {f_name}.dot in /app/code/exports/")
        else:
            self.logger.e_msg(f"{str(ObjTypes.GRAPH).capitalize()} {name} not found.")

    # TODO: Klee export *
    def export_bc(self, name, new_name) -> None:
        """Save a BC the REPL knows about to an external file."""
        if name in self.bc_files:
            with open(f"/app/code/exports/{new_name}.bc", "wb+") as file:
                bc_file = self.bc_files[name]
                file.write(bc_file)
                self.logger.i_msg(f"Made file {new_name}.dot in /app/code/exports/")
        else:
            self.logger.e_msg(f"No {str(ObjTypes.KLEE_BC).capitalize()} {name} found.")

    def export_klee_file(self, name, new_name) -> None:
        """Save a Klee formatted file the REPL knows about."""
        if name in self.klee_formatted_files:
            with open(f"/app/code/exports/{new_name}_klee.c", "w+") as file:
                klee_file = self.klee_formatted_files[name]
                file.write(klee_file)
                self.logger.i_msg(f"Made file {new_name}_klee.c in /app/code/exports/.")
        else:
            self.logger.e_msg(f"No {str(ObjTypes.KLEE_FILE).capitalize()} {name} found.")

    def list_graphs(self) -> None:
        """List all of the graphs the REPL knows about."""
        self.logger.i_msg(" Graphs ")
        self.logger.v_msg(" ".join(list(self.graphs.keys())))

    def list_metrics(self) -> None:
        """List all of the metrics the REPL knows about."""
        self.logger.i_msg(" Metrics ")
        self.logger.v_msg(" ".join(list(self.metrics.keys())))

    def list_klee_stats(self) -> None:
        """List all of the KLEE stats the REPL knows about."""
        keys = self.klee_stats.keys()
        if len(keys) == 0:
            self.logger.i_msg("No KLEE Stats available.")
        else:
            self.logger.i_msg("KLEE Stats")
            self.logger.v_msg(" ".join(list(keys)))

    def list_klee_bc(self) -> None:
        """List all of the KLEE BC Files the REPL knows about."""
        keys = self.bc_files.keys()
        if len(keys) == 0:
            self.logger.i_msg("No BC files available.")
        else:
            self.logger.i_msg("BC files")
            self.logger.v_msg(" ".join(list(keys)))

    def list_klee_files(self) -> None:
        """List all of the KLEE Files the REPL knows about."""
        keys = self.klee_formatted_files.keys()
        if len(keys) == 0:
            self.logger.i_msg("No KLEE formatted files available.")
        else:
            self.logger.i_msg("KLEE-Formatted files")
            self.logger.v_msg(" ".join(list(keys)))

    def list_klee(self) -> None:
        """List of all KLEE objects the REPL knows about."""
        self.logger.i_msg(" All KLEE Objects")
        self.list_klee_files()
        self.list_klee_bc()
        self.list_klee_stats()

    def show_graphs(self, name: str, names):
        """Display a Graph we know about to the REPL."""
        if name == "*":
            names = list(self.graphs.keys())

        for graph_name in names:
            if graph_name in self.graphs:
                self.logger.v_msg(self.graphs[graph_name])
            else:
                self.logger.v_msg(f"Graph {graph_name} not found.")

    def show_metric(self, name, names):
        """Display a metric we know about to the REPL."""
        if name == "*":
            names = list(self.metrics.keys())

        for metric_name in names:
            if metric_name in self.metrics:
                self.logger.v_msg(self.metrics[metric_name])
            else:
                self.logger.v_msg(f"Metric {metric_name} not found.")

    def show_klee_files(self, names):
        """Display all files that are formatted to be converted to .bc files."""
        for klee_file_name in names:
            if klee_file_name in self.klee_formatted_files:
                self.logger.i_msg("KLEE FORMATTED FILES:")
                self.logger.v_msg(str(self.klee_formatted_files[klee_file_name]))

    def show_klee_bc(self, names):
        """Display .bc files currently stored in the REPL."""
        for klee_bc_name in names:
            if klee_bc_name in self.bc_files:
                self.logger.i_msg("BC FILES:")
                self.logger.v_msg(self.bc_files[klee_bc_name])

    def show_klee_stats(self, names):
        """Display statistics obtained from executing KLEE."""
        for klee_stats_name in names:
            if klee_stats_name in self.klee_stats:
                self.logger.i_msg("KLEE STATS:")
                self.logger.v_msg(str(self.klee_stats[klee_stats_name]))

    def show_klee(self, names):
        """Display Klee files or .bc files we know about to the REPL."""
        self.show_klee_files(names)
        self.show_klee_bc(names)
        self.show_klee_stats(names)


class Command:
    """Command is the implementation of the REPL commands."""

    def __init__(self, curr_path: str, debug_mode: bool,
                 multi_threaded: bool, repl_wrapper) -> None:
        """Create a new instance of the REPL implementation."""
        if debug_mode:
            self.logger = Log(log_level=LogLevel.DEBUG)
        else:
            self.logger = Log(log_level=LogLevel.REGULAR)

        self.logger.d_msg("Debug Mode Enabled")
        if multi_threaded:
            self.logger.i_msg("Multithreading Enabled")
        self.multi_threaded = multi_threaded
        self.controller = Controller(self.logger)
        self.klee_utils = KleeUtils(self.logger)
        self.data = Data(self.logger)
        self.have_completed = False
        self.repl_wrapper = repl_wrapper
        self.curr_path = curr_path

    def check_num_args(self, args: List[str], num_args: int, check_recursive: bool = False,
                       err1: str = "",
                       err2: str = "Too many arguments provided.") -> bool:
        """
        Check that the number of input arguments in the list is correct.

        This returns True if the args list has num_elements many elements.
        Otherwise, print an error message.
        """
        if len(args) < num_args:
            self.logger.v_msg(err1)
        elif len(args) > num_args:
            if check_recursive:
                return len(args) == num_args + 1
            self.logger.v_msg(err2)
        else:
            return True

        return False

    def verify_file_type(self, args: str, target_type: str):
        """
        Verify that the file extension for the file passed in matches the expected file type.

        The input is the set of arguments passed in to the REPL by the user converted into a
        list.
        """
        file = args[0]
        _, file_extension = os.path.splitext(file)
        if file_extension == "":
            self.logger.v_msg(NO_FILE_EXT_ERR(file))
            return 0

        if file_extension.strip() != f".{target_type}":
            self.logger.v_msg(EXTENSION_ERR(target_type, file_extension))
            return 0

        return file

    def do_klee_replay(self, args: str):
        """Run a generated unit tests against the C source code by providing a ktest file."""
        converted_args = self.convert_args(args)
        valid_args = self.check_num_args(converted_args, 1, False, MISSING_FILENAME_ERR)
        if not valid_args:
            return

        result = self.verify_file_type(converted_args, "ktest")
        if result == 0:
            return

        path_to_klee_build_dir = '/app/build'
        command_one = 'export LD_LIBRARY_PATH={path_to_klee_build_dir}/lib/:$LD_LIBRARY_PATH'
        command_two = "gcc -I ../../include -L path-to-klee-build-dir/lib/ get_sign.c -lkleeRuntest"

        print(path_to_klee_build_dir, command_one, command_two)

    def do_convert(self, args: str) -> None:
        """Convert source code into CFGs."""
        args = self.convert_args(args)
        if len(args) == 0:
            self.logger.v_msg(MISSING_FILENAME_ERR)
            return

        recursive_mode = False
        if args[0] == "-r" or args[0] == "--recursive":
            recursive_mode = True
            args = args[1:]

        # Iterate through all file-like objects.
        all_files = []
        allowed_extensions = list(self.controller.graph_generators.keys())
        for full_path in args:
            files = get_files(full_path, recursive_mode, self.logger, allowed_extensions)
            if files == []:
                self.logger.v_msg(f"Could not get files from: {full_path}")
                return
            all_files += files

        self.logger.d_msg(f"Convert files {all_files}")
        # Make sure files are valid (if using recursive mode
        #  this is done automatically in the previous step).
        for file in all_files:
            filepath, file_extension = os.path.splitext(file)
            if file_extension not in self.controller.get_graph_generator_names():
                if file_extension == "":
                    self.logger.v_msg(NO_FILE_EXT_ERR(file))
                else:
                    self.logger.v_msg(f"Cannot convert {file_extension} for {file}.")
                return

            converter = self.controller.get_graph_generator(file_extension)
            graph = converter.to_graph(filepath.strip(), file_extension.strip())
            self.logger.v_msg(graph)
            if isinstance(graph, dict):
                self.data.graphs.update(graph)
            else:
                self.data.graphs[filepath] = graph

    def do_list(self, args: str) -> None:
        """List objects the REPL knows about."""
        converted_args = self.convert_args(args)
        valid_args = self.check_num_args(converted_args, 1, False,
                                         "Must specify object type to list\
                                         (metrics, graphs, or KLEE type).")
        if not valid_args:
            return

        list_type = converted_args[0]
        list_type = ObjTypes.get_type(list_type)
        if list_type == ObjTypes.METRIC:
            self.data.list_metrics()
        elif list_type == ObjTypes.GRAPH:
            self.data.list_graphs()
        elif list_type == ObjTypes.KLEE_BC:
            self.data.list_klee_bc()
        elif list_type == ObjTypes.KLEE_STATS:
            self.data.list_klee_stats()
        elif list_type == ObjTypes.KLEE_FILE:
            self.data.list_klee_files()
        elif list_type == ObjTypes.KLEE:
            self.data.list_klee()

        elif list_type == ObjTypes.ALL:
            self.data.list_metrics()
            self.data.list_graphs()
            self.data.list_klee()
        else:
            self.logger.v_msg(f"Type {list_type} not recognized")

    def do_metrics(self, args: str) -> None:
        """Compute of one of the known objects for a stored Graph object."""
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 1, False, "Must provide graph name.")
        if not valid_args:
            return

        name = args_list[0]
        names = [name]
        if name == "*":
            names = list(self.data.graphs.keys())
        elif name in self.data.graphs:
            pass
        else:
            try:
                self.logger.d_msg(f"Trying to compile {name} to regexp")
                pattern = re.compile(name)
                for graph_name in self.data.graphs:
                    if pattern.match(graph_name):
                        names.append(graph_name)
            except re.error:
                self.logger.v_msg(f"Error, Graph {name} not found.")
                return

        for name in names:
            graph = self.data.graphs[name]
            self.logger.v_msg(f"Computing metrics for {graph.name}")
            results = []
            for metric_generator in self.controller.metrics_generators:
                self.logger.v_msg(f"Computing {metric_generator.name()}")
                result = metric_generator.evaluate(graph)
                results.append((metric_generator.name(), result))
                self.logger.v_msg(f"Got {result}")

            self.data.metrics[name] = results

    def do_show_klee(self, obj_type, names) -> None:
        """Display the KLEE objects the REPL knows about."""
        if obj_type == ObjTypes.KLEE_BC:
            self.data.show_klee_bc(names)
        elif obj_type == ObjTypes.KLEE_FILE:
            self.data.show_klee_files(names)
        elif obj_type == ObjTypes.KLEE_STATS:
            self.data.show_klee_stats(names)
        elif obj_type == ObjTypes.KLEE:
            self.data.show_klee(names)

    def do_show(self, args: str) -> None:
        """Display objects the REPL knows about."""
        args_list = self.convert_args(args)
        err_msg = "Must specify type (metric, graph, or any KLEE type) and name."
        valid_args = self.check_num_args(args_list, 2, False, err_msg)
        if not valid_args:
            return

        obj_type = args_list[0]
        name = args_list[1]
        names = [name]
        obj_type = ObjTypes.get_type(obj_type)
        self.do_show_klee(obj_type, names)
        if obj_type == ObjTypes.METRIC:
            self.data.show_metric(name, names)
        elif obj_type == ObjTypes.GRAPH:
            self.data.show_graphs(name, names)
        elif obj_type == ObjTypes.ALL:
            if name == "*":
                names = list(self.data.metrics.keys()) + list(self.data.graphs.keys()) + \
                    list(self.data.bc_files.keys()) + \
                    list(self.data.klee_formatted_files.keys()) + \
                    list(self.data.klee_stats.keys())
                names = list(set(names))

            for name in names:
                found = False
                if name in self.data.graphs:
                    self.logger.i_msg("GRAPH")
                    self.logger.v_msg(self.data.graphs[name])
                    found = True
                if name in self.data.metrics:
                    self.logger.i_msg("METRIC")
                    self.logger.v_msg(self.data.metrics[name])
                    found = True
                if name in self.data.bc_files:
                    self.logger.i_msg("BC FILES")
                    self.logger.v_msg(self.data.bc_files[name])
                    found = True
                if name in self.data.klee_formatted_files:
                    self.logger.i_msg("KLEE FILES")
                    self.logger.v_msg(self.data.klee_formatted_files[name])
                    found = True
                if name in self.data.klee_stats:
                    self.logger.i_msg("KLEE STATS")
                    self.logger.v_msg(self.data.klee_stats[name])
                    found = True
                if not found:
                    self.logger.v_msg(f"Object {name} not found.")
        else:
            self.logger.v_msg(f"Type {obj_type} not recognized.")

    def do_analyze(self, args: str) -> None:
        """
        Analyze some set of metrics we have already computed.

        This is currently not implemented, but will likely involve computing some aggregate
        statistics.
        """
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 1, False, "Must provide metric name.")
        if not valid_args:
            return

        metric_name = args_list[0]
        metric_names = []
        if metric_name in self.data.metrics.keys():
            metric_names.append(metric_name)
        elif metric_name == "*":
            metric_names = list(self.data.metrics.keys())
        else:
            self.logger.v_msg(f"Could not find metric {metric_name}")
            return

        for metric_name in metric_names:
            _ = self.data.metrics[metric_name]

    def do_klee_to_bc(self, args: str) -> None:
        """
        Convert a file that is already in a klee-compatible format to a file KLEE can be called on.

        KLEE is called on .bc files which we generate using clang.
        """
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 1, False, "Must provide KLEE formatted name.")
        if not valid_args:
            return

        name = args_list[0]
        keys = [name]

        if name == '*':
            keys = list(self.data.klee_formatted_files.keys())

        elif name not in self.data.klee_formatted_files:
            self.logger.v_msg(f"Could not find {name}.")
            return

        for f_name in keys:
            with tempfile.NamedTemporaryFile(delete=True, suffix=".c") as file:
                self.logger.d_msg(f"Created temporary file {file.name}")
                self.logger.d_msg(f"Going to write {self.data.klee_formatted_files[f_name]}")
                file.write(self.data.klee_formatted_files[f_name].encode())

                file.seek(0)
                self.logger.d_msg("FILE CONTENTS")
                self.logger.d_msg(file.read().decode())

                cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                        -O0 -Xclang -disable-O0-optnone  -o /dev/stdout {file.name}"
                res = subprocess.run(cmd, shell=True, capture_output=True, check=True)
                self.data.bc_files[f_name] = res.stdout

    def do_to_klee_format(self, args: str) -> None:
        """Convert a file with C source code to a format compatible with klee."""
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 1, True, MISSING_FILENAME_ERR)
        if not valid_args:
            return

        recursive_mode = False
        if args_list[0] == "-r":
            recursive_mode = True
            file_path = args_list[1]
        else:
            file_path = args_list[0]

        self.logger.d_msg(f"Recursive Mode is {recursive_mode}")
        files = get_files(file_path, recursive_mode, self.logger, [".c"])
        if len(files) == 0:
            self.logger.v_msg(f"Could not find any files for {file_path}")
            return

        self.logger.d_msg(f"Got files {files}")
        for file in files:
            klee_formatted_files = self.klee_utils.show_func_defs(file)
            if klee_formatted_files is None:
                return
            self.data.klee_formatted_files = {**self.data.klee_formatted_files,
                                              **klee_formatted_files}

    def do_clean_klee_files(self, args: str) -> None:
        """Remove all KLEE-related files created by the REPL."""
        converted_args = self.convert_args(args)
        valid_args = self.check_num_args(converted_args, 0, False, NOT_IMPLEMENTED_ERR)
        if not valid_args:
            return

    def klee_output_indices(self, klee_output):
        """Get the indicies of statistics we care about in the Klee output string."""
        string_one = "generated tests = "
        string_two = "completed paths = "
        string_three = "total instructions = "

        generated_tests_index    = klee_output.index(string_one) + len(string_one)
        completed_paths_index    = klee_output.index(string_two) + len(string_two)
        total_instructions_index = klee_output.index(string_three) + len(string_three)

        return generated_tests_index, completed_paths_index, total_instructions_index

    def update_klee_stats(self, klee_output, name: str, delta_t):
        """Parse and store the results of running klee on some .bc file."""
        indices = self.klee_output_indices(klee_output)
        generated_tests_index    = indices[0]
        completed_paths_index    = indices[1]
        total_instructions_index = indices[2]

        number_regex = re.compile("[0-9]+")

        tests_match = number_regex.match(klee_output[generated_tests_index:])
        paths_match = number_regex.match(klee_output[completed_paths_index:])
        insts_match = number_regex.match(klee_output[total_instructions_index:])

        if tests_match is not None:
            tests = int(tests_match.group())
        if paths_match is not None:
            paths = int(paths_match.group())
        if insts_match is not None:
            insts = int(insts_match.group())

        self.data.klee_stats[name] = self.data.klee_stat(tests=tests, paths=paths,
                                                         instructions=insts, delta_t=delta_t)
        self.logger.i_msg("Updated!")

    def get_klee_file_name(self, args: str) -> Optional[str]:
        """Return the name of the .bc file given a command line argument string."""
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 1, False, MISSING_FILENAME_ERR)
        if not valid_args:
            return None

        return args_list[0]

    def do_klee(self, args: str) -> None:
        """Execute klee on a .bc file stored as an object in the REPL."""
        name = self.get_klee_file_name(args)
        if name is None:
            return

        if name in self.data.bc_files or name == "*":
            if name == "*":
                keys = list(self.data.bc_files.keys())
            else:
                keys = [name]

            for key in keys:
                with tempfile.NamedTemporaryFile(delete=True, suffix=".bc") as file:
                    file_name = file.name
                    self.logger.d_msg(f"Created temporary file {file_name}")

                    thing_to_write = self.data.bc_files[key]
                    self.logger.d_msg(f"Writing")
                    file.write(thing_to_write)
                    file.seek(0)

                    cmd = f"/app/build/bin/klee {file_name}"
                    self.logger.d_msg(f"Going to execute {cmd}")
                    start_time = time.time()

                    try:
                        with Timeout(30, "Klee took too long"):
                            res = subprocess.run(cmd, shell=True, capture_output=True, check=True)

                        delta_t = time.time() - start_time
                        output = res.stderr
                        self.logger.d_msg(output.decode())
                        self.logger.d_msg(f"Runtime: {delta_t} seconds")
                        self.logger.d_msg("Updating Klee Stats")
                        self.update_klee_stats(output.decode(), key, delta_t)
                    except subprocess.CalledProcessError as error:
                        self.logger.e_msg("Could not run klee")
                        self.logger.d_msg(error.stderr)
                        return
                    except TimeoutError as exception:
                        print(exception)
        else:
            result = self.verify_file_type(args, "bc")
            if result == 0:
                return

            files = get_files(result, False, self.logger, [str(KnownExtensions.BC)])
            if len(files) == 0:
                self.logger.e_msg(f"Could not find any files matching {result}")
                return

            self.logger.d_msg(f"Obtained {files}")

            for _ in files:
                cmd = f"/app/build/bin/klee {result}"
                self.logger.d_msg(cmd)
                start_time = time.time()
                res = subprocess.run(cmd, shell=True, capture_output=True, check=True)
                delta_t = time.time() - start_time
                output = res.stderr
                self.logger.d_msg("OUTOUT:")
                self.logger.d_msg(output.decode())
                self.update_klee_stats(output.decode(), name, delta_t)

    def do_quit(self, args: str) -> None:
        """Quit the repl."""
        readline.write_history_file()
        converted_args = self.convert_args(args)
        self.check_num_args(converted_args, 0, False, "Quitting...")
        raise SystemExit

    def do_export(self, args: str) -> None:
        """
        Save some object the REPL knows about to an external file.

        The format it is stored as depends on the object we are storing.
        """
        converted_args = self.convert_args(args)
        valid_args = self.check_num_args(converted_args, 2, False, MISSING_TYPE_AND_NAME_ERR)
        if not valid_args:
            return

        export_type = converted_args[0]
        name = converted_args[1]
        subprocess.check_call(["mkdir", "-p", "exports"])
        export_type = ObjTypes.get_type(export_type)

        new_name = name + "_export"

        if export_type == ObjTypes.GRAPH:
            self.data.export_graph(name, new_name)
        elif export_type == ObjTypes.METRIC:
            self.data.export_metrics(name, new_name)
        elif export_type == ObjTypes.STAT:
            if name in self.data.stats:
                with open(f"/app/code/exports/{new_name}_stats", "w+") as file:
                    stat = self.data.stats[name]
                    file.write(stat)
                    self.logger.i_msg(f"Made file {new_name}_stats in /app/code/exports/")

            elif name == "*":
                for s_name in self.data.stats:
                    f_name = os.path.split(s_name)[1]
                    with open(f"/app/code/exports/{f_name}_stats", "w+") as file:
                        stat = self.data.metrics[s_name]
                        file.write(stat)
                        self.logger.i_msg(f"Made file {f_name}s_stats in /app/code/exports/")
            else:
                self.logger.e_msg(f"{str(export_type).capitalize()} {name} not found.")

        # TODO: Fix exporting as other klee types
        elif export_type == ObjTypes.KLEE_BC:
            self.data.export_bc(name, new_name)
        elif export_type == ObjTypes.KLEE_FILE:
            self.data.export_klee_file(name, new_name)
        elif export_type == ObjTypes.KLEE:
            self.data.export_bc(name, new_name)
            self.data.export_klee_file(name, new_name)
        else:
            self.logger.v_msg(f"Type {export_type} not recognized.")

    def do_cd(self, args: str) -> None:
        """Change the working directory in the REPL."""
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 1, False, MISSING_NAME_ERR)
        if not valid_args:
            return

        new_path = args_list[0]
        if new_path[0] == "/" and not os.path.isdir(new_path):
            self.logger.e_msg("Not a valid directory.")
            return

        if new_path[0] != "/" and not os.path.isdir(os.path.join(self.curr_path, new_path)):
            self.logger.e_msg("Not a valid directory.")
            return

        self.curr_path = os.path.abspath(os.path.join(self.curr_path, new_path))

    def do_ls(self, args: str) -> None:
        """List the arguments in the current working directory."""
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 0, False, "Cannot accept arguments.")
        if not valid_args:
            return

        self.logger.v_msg(" ".join(os.listdir(self.curr_path)))

    def do_delete(self, args: str) -> None:
        """Remove some object the REPL is storing from memory."""
        args_list = self.convert_args(args)
        valid_args = self.check_num_args(args_list, 2, False, MISSING_TYPE_AND_NAME_ERR)
        if not valid_args:
            return

        obj_type = args_list[0]
        self.logger.d_msg(obj_type)
        name = args_list[1]
        known_types_dict = {
            ObjTypes.GRAPH.value: self.data.graphs,
            ObjTypes.METRIC.value: self.data.metrics,
            ObjTypes.STAT.value: self.data.stats,
            ObjTypes.KLEE_BC.value: self.data.bc_files,
            ObjTypes.KLEE_STATS.value: self.data.klee_stats,
            ObjTypes.KLEE_FILE.value: self.data.klee_formatted_files,
        }
        for known_obj_type in known_types_dict:
            if obj_type == known_obj_type:
                try:
                    del known_types_dict[name]
                except KeyError:
                    self.logger.v_msg(f"{known_obj_type.capitalize()} {name} not found.")
                return

        if obj_type == ObjTypes.KLEE.value:
            found = False
            for dictionary in [self.data.klee_stats, self.data.klee_formatted_files,
                               self.data.bc_files]:
                try:
                    del dictionary[name]
                    found = True
                except KeyError:
                    pass
            if not found:
                self.logger.v_msg(f"No {name} found of any KLEE type.")
        elif obj_type == ObjTypes.ALL.value:
            found = False
            for dictionary in [self.data.graphs, self.data.metrics,
                               self.data.stats, self.data.klee_stats,
                               self.data.klee_formatted_files, self.data.bc_files]:
                try:
                    del dictionary[name]
                    found = True
                except KeyError:
                    pass
            if not found:
                self.logger.v_msg(f"No {name} found of any type.")
        else:
            self.logger.v_msg(f"Type {type} not recognized.")

    def convert_args(self, args: str):
        """Obtain a list of arguments from a string."""
        return args.strip().split()
