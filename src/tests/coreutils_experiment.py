"""Various utilities used only for testing and not the main REPL."""

from contextlib import contextmanager
from io import StringIO
import sys
import subprocess
import re
import time
import os
import glob2
from math import floor
from numpy import mean, std, median  # type: ignore
sys.path.append("/app/code")
from log import Log
from graph import Graph
from utils import Timeout
from typing import List, Any
sys.path.append("/app/code/lang_to_cfg")
from cpp import CPPConvert
sys.path.append("/app/code/metric")
from metric import path_complexity




def con(file):
    nodes = []
    edges = []
    node_map: Dict[str, str] = {}
    counter = 0

    with open(f'{file}', "r") as old_file:
        content = old_file.readlines()
        for line in content[1:]:
            line = line.strip()

            # Throw out the label (e.g. label="CFG for 'main' function")
            # for the graph and remove whitespace.
            if line.startswith("label") or line == "":
                continue

            # If it contains a label (denoted by '[]'), it is a vertex.
            is_edge = re.search("->", line)
            if is_edge is None:
                node_name = re.match("([a-zA-Z0-9]+ )", line.lstrip())
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

def convert_file_to_standard(file):
    """Convert a single file to the standard format."""
    nodes, edges, node_map, counter = con(file)

    # Covers case of leaf CFGs.
    if len(nodes) == 1:
        nodes.append("1")
        nodes.append("2")
        counter += 2
    filename = os.path.split(file)[1]
    # Make a temporary file (with the new content).
    with open(f'cleaned/{filename}', 'w') as new_file:
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

def clean(file):
    filepath = os.path.split(file)[0]
    os.chdir(os.path.split(filepath)[0])
    subprocess.check_call(["mkdir", "-p", "cleaned"])
    convert_file_to_standard(file)

def get_converter_time(graph_list, converter, folder):
    """Run the the converter on all graph files from some folder."""
    # loop through each cfg in each folder.
    folder_time_list = []
    overall_time_list = []
    timeout_count = 0

    for i, graph in enumerate(graph_list):
        if show_info:
            print(os.path.splitext(graph)[0].split("/")[-1],
                  f"{round(100*(i / len(graph_list)))}% done")
        graph_zero = Graph.from_file(graph)
        start_time = time.time()
        try:
            with Timeout(timeout_threshold, f'{converter.name()} took too long'):
                apc =  converter.evaluate(graph_zero)

            # Calculate the run time.
            runtime = time.time() - start_time

            # Add runtime to folder-specific list.
            folder_time_list.append((runtime, graph))

            # Add runtime to overall list.
            overall_time_list.append((runtime, folder, graph))
            if show_info:
                print(f"Runtime {runtime}")

        except TimeoutError as exception:
            if show_info:
                print(exception)
            timeout_count += 1

    return folder_time_list, overall_time_list, timeout_count


def run_benchmark(converter):
    """Run all CFGs through the converter to create a benchmark."""
    folders = (glob.glob("/app/code/tests/core/separate/*/"))
    print(f"number of folders: {len(folders)}\n")
    metric_collection: List[Any] = []
    # list of tuples for all cfgs in all folders (seconds, folder, cfg).
    time_list = []
    apc_list = []
    timeout_total = 0
    # test the metrics for each folder in apache_cfgs.
    print(f"Num Folders: {floor(len(folders) / folders_frac)}")
    for folder in folders[0:floor(len(folders) / folders_frac)]:
        print(f"On folder {folder}")
        graph_list = (glob.glob(folder + "*.dot"))
        graph_list = graph_list[0:floor(len(graph_list) / graph_frac)]
        # list of tuples for each cfg in folder(seconds, cfg).
        folder_time_list, overall_time_list, timeout_count = get_converter_time(graph_list,
                                                                                converter, folder,
                                                                                timeout_threshold,
                                                                                graph_type,
                                                                                show_info)







if __name__ == "__main__":
    # Get all the folders
    # Establish our lists: names, apc, cyclomatic, npath, time, exception? 







# """Run all CFGs through the converter to create a benchmark."""
# files = (glob2.glob("/app/code/tests/core/separate/*"))

# os.chdir("/app/code/tests/core/separate")
# for file in files: 
#     name = os.path.basename(file)
#     os.chdir(f"/app/code/tests/core/separate/{name}/")
#     f = f".{name}.bc"     
#     subprocess.check_call(["opt", "-dot-cfg", f"{f}"])        
        