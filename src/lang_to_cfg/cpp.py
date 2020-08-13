"""This module converts C++ source code into Graph objects representing the CFG for the code."""

from typing import Dict, Optional, Tuple, Any
import subprocess
import shlex  # type: ignore
import sys
import os
import re
import glob2  # type: ignore
sys.path.append("/app/code/")
from graph import Graph, GraphType
from log import Log
from env import Env
from lang_to_cfg import converter  # type: ignore

# pylint: disable=R0201


class CPPConvert(converter.ConverterAbstract):
    """Create Graph objects from files."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new instance of the C++ converter."""
        self.logger = logger
        self.edge_pattern = "->"
        self.name_pattern = "([a-zA-Z0-9]+ )"

    def name(self) -> str:
        """Get the name of the CPP converter."""
        return "CPP"

    def to_graph(self, filename: str, file_extension: str) -> Optional[Dict[str, Graph]]:
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
        for i in range(file_count):
            f_name = filename + (str(i) + ".dot")
            graph_name = os.path.splitext(f_name)[0]
            graph_name = os.path.split(graph_name)[1]
            self.logger.d_msg(f"graph_name: {graph_name}")
            graphs[graph_name] = Graph.from_file(f_name, False, GraphType.EDGE_LIST)

        Env.clean_temps()
        return graphs

    def parse_original(self, file: str) -> Tuple[Any, Any, Any, Any]:
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
                is_edge = re.search(self.edge_pattern, line)
                if is_edge is None:
                    node_name = re.match(self.name_pattern, line.lstrip())
                    if node_name is None:
                        continue

                    node_name_str = node_name.groups()[0].strip()
                    node_map[node_name_str] = str(counter)
                    node_to_add = str(counter)
                    if counter == 0:
                        node_to_add += " [label=\"START\"]"

                    nodes.append(node_to_add)

                    counter += 1
                else:
                    edges += [line]

        return nodes, edges, node_map, counter

    def convert_file_to_standard(self, file: str, filename: str,
                                 f_num: Optional[int] = None) -> None:
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
        name = os.path.split(filename)[1]
        if f_num is not None:
            output_name = f'{Env.TMP_DOT_PATH}/{name}{f_num}.dot'
        else:
            output_name = f'{Env.TMP_DOT_PATH}/{name}.dot'

        with open(output_name, 'w') as new_file:
            new_file.write("digraph { \n")

            # Create the nodes and then the edges.
            for i, node in enumerate(nodes):
                if i == counter - 1:
                    node += "[label=\"EXIT\"]"
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

        for i, file in enumerate(files):
            self.convert_file_to_standard(file, filename, i)

        return len(files)

    def create_dot_files(self, filepath: str, file_extension: str) -> None:
        """Create a .dot file representing a CFG for each function from a .cpp file."""
        # Make sure the file extension begins with a '.'
        if file_extension[0] != '.':
            file_extension = f".{file_extension}"

        self.logger.d_msg(f"Going to dir: {os.path.split(filepath)[0]}")
        os.chdir(os.path.split(filepath)[0])
        c1_str = f"clang++-6.0 -emit-llvm -S {filepath}{file_extension} -o-"
        c2_str = "/usr/lib/llvm-6.0/bin/opt -dot-cfg"

        commands = [shlex.split(c1_str), shlex.split(c2_str)]

        self.logger.d_msg(f"Command One: {commands[0]}")
        self.logger.d_msg(f"Command Two: {commands[1]}")

        with subprocess.Popen(commands[0], stdin=None, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=False) as line1:
            command = line1.stdout

            if line1.stderr is not None:
                err_msg = line1.stderr.read()
                if len(err_msg) == 0:
                    self.logger.d_msg(f"Got the following error msg: {str(err_msg)}")

            with subprocess.Popen(commands[1], stdin=command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=False) as line2:
                line2.communicate()

        files = glob2.glob("*.dot")
        self.logger.d_msg(f"Found the following .dot files: {files}")
        for file in files:
            subprocess.call(["mv", file, Env.TMP_PATH])
