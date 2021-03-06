"""Various utilities used only for testing and not the main REPL."""
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import glob2  # type: ignore
import pandas as pd  # type: ignore

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph as CFG
from metric import cyclomatic_complexity, metric, npath_complexity, path_complexity
from utils import Timeout

PathComplexityRes = Tuple[Union[float, str], Union[float, str]]


def parse_original(file: str) -> Tuple[List[str], List[str], Dict[str, str], int]:
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


def clean(file: str) -> None:
    """Remove unecessary files."""
    filepath = os.path.split(file)
    fname = filepath[1]
    os.chdir(filepath[0])
    files = glob2.glob("*.dot")
    for fname in files:
        convert_file_to_standard(fname)


def get_converter_time(graph_list: List[str],
                       converter: metric.MetricAbstract,
                       folder: str,
                       timeout_threshold: int, show_info: bool = False
                       ) -> Tuple[List[Tuple[float, str]],
                                  List[Tuple[float, str, str]],
                                  int]:
    """Run the the converter on all graph files from some folder."""
    # loop through each cfg in each folder.
    folder_time_list = []
    overall_time_list = []
    timeout_count = 0

    for i, graph in enumerate(graph_list):
        if show_info:
            print(os.path.splitext(graph)[0].split("/")[-1],
                  f"{round(100*(i / len(graph_list)))}% done")
        graph_obj = CFG.from_file(graph)
        start_time = time.time()
        try:
            with Timeout(timeout_threshold, f'{converter.name()} took too long'):
                apc = converter.evaluate(graph_obj)

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


def run_benchmark(converter: metric.MetricAbstract,
                  timeout_threshold: int,
                  show_info: bool = False) -> None:
    """Run all CFGs through the converter to create a benchmark."""
    folders = (glob2.glob("/app/code/tests/core/separate/*/"))
    print(f"number of folders: {len(folders)}\n")
    # list of tuples for all cfgs in all folders (seconds, folder, cfg).

    # test the metrics for each folder in apache_cfgs.
    print(f"Num Folders: {len(folders)}")
    for folder in folders:
        print(f"On folder {folder}")
        graph_list = (glob2.glob(folder + "*.dot"))
        # list of tuples for each cfg in folder(seconds, cfg).
        folder_time_list, overall_time_list, timeout_count = get_converter_time(graph_list,
                                                                                converter, folder,
                                                                                timeout_threshold,
                                                                                show_info)


def get_name(path: str, path_type: str) -> str:
    """Get the name of a file given its path."""
    if path_type == "folder":
        return os.path.split(os.path.split(path)[0])[1].replace(".o", ".c")

    if path_type == "file":
        return os.path.split(path)[1].split("cleaned_cfg.")[1]

    return ""


def main() -> None:
    """Run the coreutils experiment."""
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
            cfg = CFG.from_file(file)

            start_time = time.time()
            apc: Union[str, PathComplexityRes] = "na"
            npath: Union[str, float] = "na"
            cyclo: Union[str, float] = "na"
            ex = False
            exception_type = "na"
            runtime = 0.0
            try:
                with Timeout(300, ""):
                    apc = Apc.evaluate(cfg)
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
                        cyclo = Cyclo.evaluate(cfg)

                except TimeoutError as exception:
                    ex = True
                    exception_type = "Timeout"
                except Exception:
                    ex = True
                    exception_type = "Other"
                if not ex:
                    try:
                        with Timeout(200, ""):
                            npath = Npath.evaluate(cfg)

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


if __name__ == "__main__":
    main()

# """Run all CFGs through the converter to create a benchmark."""
# files = (glob2.glob("/app/code/tests/core/separate/*"))

# os.chdir("/app/code/tests/core/separate")
# for file in files:
#     name = os.path.basename(file)
#     os.chdir(f"/app/code/tests/core/separate/{name}/")
#     f = f".{name}.bc"
#     subprocess.check_call(["opt", "-dot-cfg", f"{f}"])
