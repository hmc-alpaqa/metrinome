"""This module converts C++ source code into Graph objects representing the CFG for the code."""

import os
import re
import shlex
import signal
import subprocess
from types import FrameType
from typing import Optional

import glob2  # type: ignore

from core.env import Env, KnownExtensions
from core.log import Log
from graph.control_flow_graph import ControlFlowGraph, Metadata
from graph.graph import EdgeListGraph
from lang_to_cfg import converter


class CPPConvert(converter.ConverterAbstract):
    """Create Graph objects from files."""

    # pylint: disable=super-init-not-called
    def __init__(self, logger: Log) -> None:
        """Create a new instance of the C++ converter."""
        self.logger = logger
        self._edge_pattern = "->"
        self._name_pattern = "([a-zA-Z0-9]+ )"
        self._optimize = False
        # self._call_pattern = r"(@_)[A-Z0-9]{2,}[A-Za-z0-9_]*\("
        # TODO: merge in david's code to correct parsing and other graph conversions
        # For now, this ignores the _Z6 prefix that was previously matched,
        # and we remove the underscore after @
        # this fix was needed to make clang work (instead of clang++)
        self._call_pattern = r"(@)[A-Za-z0-9_]*\("

    def name(self) -> str:
        """Get the name of the CPP converter."""
        return "CPP"

    def to_graph(self,
                 filename: str,
                 file_extension: str) -> Optional[dict[str, ControlFlowGraph]]:
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
        graphs: dict[str, ControlFlowGraph] = {}
        filename = f"{Env.TMP_DOT_PATH}/{name}"
        files = glob2.glob(f"{Env.TMP_DOT_PATH}/*.dot")
        for file in files:
            graph_name = os.path.basename(file)
            self.logger.d_msg(f"graph_name: {graph_name}")
            graph = ControlFlowGraph.from_file(file, EdgeListGraph,
                                               [Metadata.with_language(KnownExtensions.C)])
            graphs[graph_name] = graph
        Env.clean_temps()
        return graphs

    def parse_original(self, file: str) -> tuple[list[str], list[str],
                                                 dict[str, str], int]:
        """Obtain all of the Graph information from an existing dot file in the original format."""
        # Read the original files.
        nodes, edges = [], []
        node_map: dict[str, str] = {}
        counter = 0

        with open(file, "r") as old_file:
            content = old_file.readlines()
            for line in content[1:]:
                line = line.strip()
                # print(line)

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
                    calls = re.finditer(self._call_pattern, line.lstrip())
                    label = ""
                    call_label = ""
                    for call in calls:
                        call_label += " "
                        call_label += call.group(0)[1:-1]
                    if counter == 0 and call_label != "":
                        label = f" [label=\"START CALLS{call_label}\"]"
                    elif counter == 0:
                        label = " [label=\"START\"]"
                    elif call_label != "":
                        label = f" [label=\"CALLS{call_label}\"]"
                    node_to_add += label
                    # print(label)
                    # print(node_to_add)
                    nodes.append(node_to_add)

                    counter += 1
                else:
                    edges += [line]
            # print(node_map)
            # print(edges)
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
        # file:/app/code/tmp/cfg._Z7mul_invii.dot
        f_name = os.path.basename(file)
        # f_name: cfg._Z7mul_invii.dot
        # with open(Env.TMP_DOT_PATH + "/" + source_name + "_" + f_name, 'w') as new_file:
        # print(f"OPEN!!! {open(Env.TMP_DOT_PATH + "/" + source_name + "_" + f_name, 'w+')}")
        with open(Env.TMP_DOT_PATH + "/" + source_name + "_" + f_name, 'w+') as new_file:
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
            new_file.seek(0)

    def convert_to_standard_format(self, filename: str) -> int:
        """
        Convert the generated .dot files to a common format.

        Each dot file generated from the .cpp source is converted to the same format
        as the dot files generated from Java CFGs.
        """
        files = glob2.glob(f"{Env.TMP_PATH}/.*.dot")
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
        self.logger.d_msg(f"filepath: {filepath}")
        self.logger.d_msg(f"Going to dir: {os.path.split(filepath)[0]}")
        os.chdir(os.path.split(filepath)[0])

        if self._optimize:
            c1_str = f"clang{'++' if file_extension == '.cpp' else ''}-6.0 -emit-llvm -S -O3 {filepath}{file_extension} -o-"
        else:
            c1_str = f"clang{'++' if file_extension == '.cpp' else ''}-6.0 -emit-llvm -S {filepath}{file_extension} -o-"
        # 2nd half of command: process compiled files to produce dot files using llvm
        command = c1_str + " | /usr/lib/llvm-6.0/bin/opt -dot-cfg -disable-output -enable-new-pm=0"

        # ============== NEW CLANG FOR RUNNING WITH DOCKER ==========================================
        # 1st part of command: compile c files with clang
        if self._optimize:
            c1_str = f"clang{'++' if file_extension == '.cpp' else ''}-14 -emit-llvm -S -O3 {filepath}{file_extension} -o-"
        else:
            c1_str = f"clang{'++' if file_extension == '.cpp' else ''}-14 -emit-llvm -S {filepath}{file_extension} -o-"
        # 2nd half of command: process compiled files to produce dot files using llvm
        command = c1_str + " | /usr/lib/llvm-14/bin/opt -dot-cfg -disable-output -enable-new-pm=0"
        # ============== NEW CLANG FOR RUNNING WITH DOCKER ==========================================

        self.logger.d_msg(f"Command: {command}")
        # run command in shell
        subprocess.run(command,shell=True)
        # collect resulting dot files
        files = glob2.glob(".*.dot")
        # move files into our environment
        for file in files:
            subprocess.call(["mv", file, Env.TMP_PATH])
