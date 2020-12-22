"""This module converts C++ source code into Graph objects representing the CFG for the code."""

from typing import Dict, Optional, Tuple, List
from types import FrameType
import subprocess
import shlex
import os
import re
import signal
import glob2  # type: ignore
from core.log import Log
from core.env import Env
from lang_to_cfg import converter
from graph.graph import GraphType
from graph.control_flow_graph import ControlFlowGraph


# pylint: disable=R0201


class CPPConvert(converter.ConverterAbstract):
    """Create Graph objects from files."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new instance of the C++ converter."""
        self.logger = logger
        self._edge_pattern = "->"
        self._name_pattern = "([a-zA-Z0-9]+ )"
        self._optimize = False
        self._call_pattern = r"(@_)[A-Z0-9]{2,}[A-Za-z0-9_]*\("

    def name(self) -> str:
        """Get the name of the CPP converter."""
        return "CPP"

    def to_graph(self,
                 filename: str,
                 file_extension: str) -> Optional[Dict[str, ControlFlowGraph]]:
        """Create a CFG from a C++ source file."""
        Env.make_temp()
        Env.clean_temps()
        self.logger.d_msg(f"Creating dot files for {filename}, {file_extension}")
        self.create_dot_files(filename, file_extension)
        self.logger.d_msg("Converting to standard format")
        file_count = self.convert_to_standard_format(filename)
        self.logger.d_msg(f"File count is: {file_count}")
        if file_count == 0:
            Env.clean_temps()
            return None

        name = os.path.split(filename)[1]
        graphs = {}
        filename = f"{Env.TMP_DOT_PATH}/{name}"
        files = glob2.glob(f"{Env.TMP_DOT_PATH}/*.dot")
        for file in files:
            graph_name = os.path.basename(file)
            self.logger.d_msg(f"graph_name: {graph_name}")
            graphs[graph_name] = ControlFlowGraph.from_file(file, False, GraphType.EDGE_LIST)

        Env.clean_temps()
        return graphs

    def parse_original(self, file: str) -> Tuple[List[str],
                                                 List[str],
                                                 Dict[str, str],
                                                 int]:
        """Obtain all of the Graph information from an existing dot file in the original format."""
        # Read the original files.
        nodes, edges = [], []
        node_map: Dict[str, str] = {}
        counter = 0

        with open(file, "r") as old_file:
            content = old_file.readlines()
            for line in content[1:]:
                line = line.strip()

                # Throw out the label (e.g. label="CFG for 'main' function")
                # for the graph and remove whitespace.
                if line.startswith("label") or line == "":
                    continue

                # If it contains a label (denoted by '[]'), it is a vertex.
                is_edge = re.search(self._edge_pattern, line)
                if is_edge is None:
                    node_name = re.match(self._name_pattern, line.lstrip())
                    if node_name is None:
                        continue

                    node_name_str = node_name.groups()[0].strip()
                    node_map[node_name_str] = str(counter)
                    node_to_add = str(counter)
                    call = re.search(self._call_pattern, line.lstrip())
                    label = ""

                    if counter == 0 and call is not None:
                        call_label = call.group(0)[1:-1]
                        label = f" [label=\"START CALLS {call_label}\"]"
                    elif counter == 0:
                        label = " [label=\"START\"]"
                    elif call is not None:
                        call_label = call.group(0)[1:-1]
                        label = f" [label=\"CALLS {call_label}\"]"

                    node_to_add += label
                    nodes.append(node_to_add)

                    counter += 1
                else:
                    edges += [line]

        return nodes, edges, node_map, counter

    def convert_file_to_standard(self, file: str,
                                 filename: str) -> None:
        """Convert a single file to the standard format."""
        nodes, edges, node_map, counter = self.parse_original(file)

        # Covers case of leaf CFGs.
        if len(nodes) == 1:
            nodes.append("1")
            nodes.append("2")
            edges += ["0 -> 1;"]
            edges += ["1 -> 2;"]
            counter += 2

        # Make a temporary file (with the new content).
        source_name = os.path.basename(filename)
        f_name = os.path.basename(file)
        with open(Env.TMP_DOT_PATH + "/" + source_name + "_" + f_name, 'w') as new_file:
            new_file.write("digraph { \n")

            # Create the nodes and then the edges.
            for i, node in enumerate(nodes):
                if i == counter - 1:
                    node += " [label=\"EXIT\"]"
                new_file.write(node + ";" + "\n")

            for edge in edges:
                for name in node_map:
                    edge = edge.replace(name, node_map[name])
                    edge = edge.replace(":s0", "")
                    edge = edge.replace(":s1", "")

                new_file.write(edge + "\n")
            new_file.write("}")

    def convert_to_standard_format(self, filename: str) -> int:
        """
        Convert the generated .dot files to a common format.

        Each dot file generated from the .cpp source is converted to the same format
        as the dot files generated from Java CFGs.
        """
        files = glob2.glob(f"{Env.TMP_PATH}/*.dot")
        for name in files:
            if "global" in name.lower():
                os.remove(name)
                files.remove(name)

        for file in files:
            self.convert_file_to_standard(file, filename)

        return len(files)

    def create_dot_files(self, filepath: str, file_extension: str) -> None:
        """Create a .dot file representing a CFG for each function from a .cpp file."""
        # Make sure the file extension begins with a '.'
        if file_extension[0] != '.':
            file_extension = f".{file_extension}"

        self.logger.d_msg(f"Going to dir: {os.path.split(filepath)[0]}")
        os.chdir(os.path.split(filepath)[0])

        if self._optimize:
            c1_str = f"clang++-6.0 -emit-llvm -S -O3 {filepath}{file_extension} -o-"
        else:
            c1_str = f"clang++-6.0 -emit-llvm -S {filepath}{file_extension} -o-"\

        c2_str = "/usr/lib/llvm-6.0/bin/opt -dot-cfg"

        commands = [shlex.split(c1_str), shlex.split(c2_str)]

        self.logger.d_msg(f"Command One: {commands[0]}")
        self.logger.d_msg(f"Command Two: {commands[1]}")

        with subprocess.Popen(commands[0], stdin=None, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=False) as line1:
            command = line1.stdout
            if line1.stderr is not None:
                def handler(signum: int, frame: FrameType) -> None:
                    raise TimeoutError("Timed out.")

                signal.signal(signal.SIGALRM, handler)
                error_lines = []
                try:
                    for line in line1.stderr:
                        signal.alarm(5)
                        error_lines.append(str(line))
                except TimeoutError as err:
                    self.logger.d_msg(str(err))

                signal.alarm(0)
                err_msg = ''.join(error_lines)

                if len(err_msg) == 0:
                    self.logger.d_msg(f"Got the following error msg: {str(err_msg)}")

            with subprocess.Popen(commands[1], stdin=command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=False) as line2:
                line2.communicate()

        files = glob2.glob("*.dot")
        self.logger.d_msg(f"Found the following .dot files: {files}")
        for file in files:
            subprocess.call(["mv", file, Env.TMP_PATH])
