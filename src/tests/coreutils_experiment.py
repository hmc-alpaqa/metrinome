"""Various utilities used only for testing and not the main REPL."""
import os
import time
import sys
import re
from typing import List, Any, Union
import glob2  # type: ignore
import pandas as pd  # type: ignore
sys.path.append("/app/code")
from log import Log
from graph import Graph
from utils import Timeout
sys.path.append("/app/code/lang_to_cfg")
sys.path.append("/app/code/metric")
from metric import path_complexity, cyclomatic_complexity, npath_complexity


def parse_original(file):
    """Obtain all of the Graph information from an existing dot file in the original format."""
    # Read the original files.
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


def convert_file_to_standard(file: str) -> None:
    """Convert a single file to the standard format."""
    nodes, edges, node_map, counter = parse_original(file)

    # Covers case of leaf CFGs.
    if len(nodes) == 1:
        nodes.append("1")
        nodes.append("2")
        edges += ["0 -> 1;"]
        edges += ["1 -> 2;"]
        counter += 2

    filename = os.path.split(file)[1]
    # Make a temporary file (with the new content).
    with open(f'cleaned_{filename}', 'w') as new_file:
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
    """Remove unecessary files."""
    filepath = os.path.split(file)
    fname = filepath[1]
    os.chdir(filepath[0])
    files = glob2.glob("*.dot")
    for fname in files:
        convert_file_to_standard(fname)


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
                apc = converter.evaluate(graph_zero)

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

    # test the metrics for each folder in apache_cfgs.
    print(f"Num Folders: {len(folders)}")
    for folder in folders:
        print(f"On folder {folder}")
        graph_list = (glob.glob(folder + "*.dot"))
        # list of tuples for each cfg in folder(seconds, cfg).
        folder_time_list, overall_time_list, timeout_count = get_converter_time(graph_list,
                                                                                converter, folder,
                                                                                timeout_threshold,
                                                                                graph_type,
                                                                                show_info)


def get_name(path, type):
    """Get the name of a file given its path."""
    if type == "folder":
        return os.path.split(os.path.split(path)[0])[1].replace(".o", ".c")

    if type == "file":
        return os.path.split(path)[1].split("cleaned_cfg.")[1]


if __name__ == "__main__":
    # Get all the folders
    # Establish our lists: file_name, dot_name, apc, cyclo, npath, time, exception?
    log = Log()
    data = pd.DataFrame({"c_file_name": [], "dot_file_name": [], "apc": [],
                         "cyclo": [], "npath": [], "apc_time": [], "exception": [],
                         "exception_type": []})

    folders = (glob2.glob("/app/code/tests/core/separate/*/"))

    Apc = path_complexity.PathComplexity(log)
    Cyclo = cyclomatic_complexity.CyclomaticComplexity(log)
    Npath = npath_complexity.NPathComplexity(log)
    for folder in folders:
        folder_name = get_name(folder, "folder")
        files = glob2.glob(f"{folder}/cleaned_*.dot")
        for file in files:
            file_name = get_name(file, "file")
            graph = Graph.from_file(file)

            start_time = time.time()
            apc = "na"
            npath: Union[str, float] = "na"
            cyclo: Union[str, float] = "na"
            ex = False
            exception_type = "na"
            runtime = 0.0
            try:
                with Timeout(300, ""):
                    apc = Apc.evaluate(graph)
                runtime = time.time() - start_time

            except TimeoutError as exception:
                ex = True
                exception_type = "Timeout"
            except Exception as v:
                print(v)
                ex = True
                exception_type = "Other"
            if not ex:
                try:
                    with Timeout(200, ""):
                        cyclo = Cyclo.evaluate(graph)

                except TimeoutError as exception:
                    ex = True
                    exception_type = "Timeout"
                except Exception:
                    ex = True
                    exception_type = "Other"
                if not ex:
                    try:
                        with Timeout(200, ""):
                            npath = Npath.evaluate(graph)

                    except TimeoutError as exception:
                        ex = True
                        exception_type = "Timeout"
                    except Exception:
                        ex = True
                        exception_type = "Other"
            new_row = {"c_file_name": folder_name, "dot_file_name": file_name, "apc": apc,
                       "cyclo": cyclo, "npath": npath, "apc_time": runtime,
                       "exception": ex, "exception_type": exception_type}

            data = data.append(new_row, ignore_index=True)
            data.to_csv("/app/code/tests/core/final.csv")

# """Run all CFGs through the converter to create a benchmark."""
# files = (glob2.glob("/app/code/tests/core/separate/*"))

# os.chdir("/app/code/tests/core/separate")
# for file in files:
#     name = os.path.basename(file)
#     os.chdir(f"/app/code/tests/core/separate/{name}/")
#     f = f".{name}.bc"
#     subprocess.check_call(["opt", "-dot-cfg", f"{f}"])
