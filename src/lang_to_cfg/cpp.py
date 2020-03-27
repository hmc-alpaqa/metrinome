"""
This module converts C++ source code into Graph objects representing
the CFG for the code.
"""

from typing import Dict
import subprocess
import shlex  # type: ignore
import sys
import os
import re
import glob2  # type: ignore
from graph import Graph
sys.path.append("/app/code/")

# pylint: disable=R0201


class CPPConvert():
    """
    Creates Graph objects from files.
    """

    def __init__(self, logger) -> None:
        self.logger = logger

    def to_graph(self, filename: str, file_extension: str) -> Dict[str, Graph]:
        """
        Creates a CFG from a C++ source file.
        """
        self.logger.d("Creating dot files")
        self.create_dot_files(filename, file_extension)
        self.logger.d("Converting to standard format")
        file_count = self.convert_to_standard_format(filename)
        self.logger.d(f"File count is: {file_count}")
        name = os.path.split(filename)[1]
        graphs = {}
        filename = filename.strip(name)
        filename += f"cppConverterTemps/{name}"
        for i in range(file_count):
            f_name = filename + (str(i) + ".dot")
            graph_name = os.path.splitext(f_name)[0]
            graph_name = os.path.split(graph_name)[1]
            graphs[graph_name] = Graph.from_file(f_name)
        # self.cleanTemps()
        return graphs

    def convert_file_to_standard(self, f_num, filename, file):
        nodes = []
        edges = []
        node_map: Dict[str, str] = {}
        counter = 0

        # Make a temporary file (with the new content)
        with open(f'cppConverterTemps/{filename}{f_num}.dot', 'w') as new_file:
            with open(f'{file}', "r") as old_file:
                content = old_file.readlines()
                new_file.write("digraph { \n")
                for line in content[1:]:
                    line = line.strip()

                    # Throw out the label (e.g. label="CFG for 'main' function")
                    # for the graph and remove whitespace.
                    if line.startswith("label") or line == "":
                        continue

                    # If it contains a label (denoted by '[]'), it is a vertex
                    edge_pattern = "->"
                    name_pattern = "([a-zA-Z0-9]+ )"
                    is_edge = re.search(edge_pattern, line)
                    if is_edge is None:
                        node_name = re.match(name_pattern, line.lstrip())
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

            # Covers case of leaf CFGs
            if len(nodes) == 1:
                nodes.append("1")
                nodes.append("2")
                counter += 2

            # Create the nodes and then the edges
            for i, node in enumerate(nodes):
                if i == counter - 2:
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
        Convert each dot file generated from the .cpp source to the same format
        as the dot files generated from Java CFGs.
        """
        path = os.path.split(filename)[0]
        filename = os.path.split(filename)[1]
        files = glob2.glob(f"{path}/cppConverterTemps/*.dot")
        for name in files:
            if "global" in name.lower():
                os.remove(name)
                files.remove(name)

        for f_num, file in enumerate(files):
            self.convert_file_to_standard(f_num, filename, file)

        return len(files) - 1

    def create_dot_files(self, filepath: str, file_extension: str) -> None:
        """
        Create a .dot file representing a control flow graph for
        each function from a .cpp file
        """
        # Make sure the file extension begins with a '.'
        if file_extension[0] != '.':
            file_extension = f".{file_extension}"

        self.logger.d(f"Going to dir: {os.path.split(filepath)[0]}")
        os.chdir(os.path.split(filepath)[0])
        res = subprocess.check_call(["mkdir", "-p", "cppConverterTemps"])
        print(res)

        c1_str = f"clang++-6.0 -emit-llvm -S {filepath}{file_extension} -o /dev/stdout"
        c2_str = "/usr/lib/llvm-6.0/bin/opt -dot-cfg"

        commands = [shlex.split(c1_str), shlex.split(c2_str)]

        self.logger.d(f"Command One: {commands[0]}")
        self.logger.d(f"Command Two: {commands[1]}")

        with subprocess.Popen(commands[0], stdin=None, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=False) as line1:
            command = line1.stdout
            if line1.stderr is not None:
                err_msg = line1.stderr.read()
                if len(err_msg) == 0:
                    self.logger.d(f"Got the following error msg: {str(err_msg)}")

            with subprocess.Popen(commands[1], stdin=command, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, shell=False) as line2:
                out, err = line2.communicate()
                print(out, err)

        files = glob2.glob("*.dot")
        self.logger.d(f"Found the following .dot files: {files}")
        for file in files:
            subprocess.call(["mv", f"{file}", "cppConverterTemps"])

    def clean_temps(self):
        """removes temp files and directories"""
        subprocess.call(["rm", "-r", "cppConverterTemps"])
