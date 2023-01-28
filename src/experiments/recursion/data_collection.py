"""Various utilities used only for testing and not the main REPL."""
import os
import time
from typing import Union

import pandas as pd  # type: ignore

from core.log import Log, LogLevel
from lang_to_cfg.cpp import CPPConvert
from metric import cyclomatic_complexity, npath_complexity, path_complexity, recursive_path_complexity
from metric.path_complexity import PathComplexityRes
from utils import Timeout


class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level = LogLevel.DEBUG)
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.recursive_apc_computer = recursive_path_complexity.RecursivePathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)
        self.base_path = "/app/code/experiments/recursion/files/"

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [], "rapc": [],  "brapc": [],
                             "cyclo": [], "npath": [], "apc_time": [], "rapc_time": [], "brapc_time": [],
                             "num_vertices": [], "edge_count": [], "exception": [],
                             "exception_type": []})
        with open('/app/code/experiments/recursion/files/files.txt') as funcs:
            files = [self.base_path + line.rstrip() for line in funcs]

        for file in files:
            print(f"Now analyzing {file}")
            graphs = self.converter.to_graph(os.path.splitext(file)[0], ".c")
            if graphs is None:
                graphs = self.converter.to_graph(os.path.splitext(file)[0], ".cpp")
            if graphs is None:
                print("No Graphs")
                continue

            for graph in graphs.values():
                start_time = time.time()
                apc: Union[str, PathComplexityRes] = "na"
                rapc: Union[str, PathComplexityRes] = "na"
                brapc= ""
                npath: Union[str, int] = "na"
                cyclo: Union[str, int] = "na"
                exception_type = "na"
                runtime = 0.0
                rruntime = 0.0
                bruntime = 0.0
                try:
                    with Timeout(300):
                        rapc = self.recursive_apc_computer.evaluate(graph)
                        rruntime = time.time() - start_time
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
                start_time = time.time()
                try:
                    with Timeout(300):
                        recurlist = []
                        end = graph.graph.num_vertices - 1
                        for node in graph.metadata.calls.keys():
                            if graph.name.split(".")[1] in graph.metadata.calls[node]:
                                recurlist += [int(node)]
                        oldEdges = graph.graph.edges
                        for node in recurlist:
                            graph.graph.edges = graph.graph.edges + [[node, 0]]
                            graph.graph.edges = graph.graph.edges + [[end, node]]
                        brapc = self.apc_computer.evaluate(graph)
                        bruntime = time.time() - start_time
                        graph.graph.edges = oldEdges
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
                start_time = time.time()
                try:
                    with Timeout(300):
                        apc = self.apc_computer.evaluate(graph)
                        runtime = time.time() - start_time
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
                try:
                    with Timeout(200):
                        cyclo = self.cyclo_computer.evaluate(graph)
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                try:
                    with Timeout(200):
                        npath = self.npath_computer.evaluate(graph)
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                new_row = {"file_name": file, "graph_name": graph.name, "apc": apc,
                           "rapc": rapc, "brapc": brapc, "cyclo": cyclo, "npath": npath,
                           "apc_time": runtime, "rapc_time": rruntime, "brapc_time": bruntime,
                           "num_vertices": graph.graph.num_vertices,
                           "edge_count": graph.graph.edge_count(),
                           "exception_type": exception_type}

                data = data.append(new_row, ignore_index=True)
                data.to_csv(f"/app/code/experiments/recursion/data/recursiveData.csv")

def main() -> None:
    """Compute metrics for many graphs."""
    data_collector = DataCollector()
    data_collector.collect()


if __name__ == "__main__":
    main()
