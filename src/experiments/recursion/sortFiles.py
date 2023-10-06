"""Various utilities used only for testing and not the main REPL."""
import os
import time
from typing import Union

import pandas as pd  # type: ignore

from core.log import Log
from lang_to_cfg.cpp import CPPConvert
from metric import cyclomatic_complexity, npath_complexity, path_complexity, recursive_path_complexity
from metric.path_complexity import PathComplexityRes
from utils import Timeout

import glob

# root_dir needs a trailing slash (i.e. /root/dir/)

class FileSorter:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log()
        self.converter = CPPConvert(log)
        self.base_path = "/app/code/experiments/recursion"

    # pylint: disable=broad-except
    def sort(self) -> None:
        """Compute the metrics for all files and store the data."""

        unsorted = self.base_path + "/unsorted/"

        for filename in glob.iglob(unsorted + '**/*.cpp', recursive=True):
             self.subsort(filename)
        for filename in glob.iglob(unsorted + '**/*.c', recursive=True):
            self.subsort(filename)
        # for filename in os.listdir(unsorted):
        #
        #     f = os.path.join(unsorted, filename)
        #     self.subsort(f)

    def subsort(self, f) -> None:

        sorted = self.base_path + "/files"
        append = sorted + "/files.txt"
        # checking if it is a file
        if os.path.isfile(f):
            print(f"Now analyzing {f}")
            print(os.path.splitext(f)[0])
            graphs = self.converter.to_graph(os.path.splitext(f)[0], ".c")
            # print(graphs)
            if graphs is None:
                graphs = self.converter.to_graph(os.path.splitext(f)[0], ".cpp")
            if graphs is None:
                print("No Graphs")
                return

            for graph in graphs.values():
                # print(graph)
                for node in graph.metadata.calls.keys():
                    if not graph.metadata.calls[node].count(graph.name.split(".")[1]) == 0:
                        filename = f.split("/")[-1]
                        if not os.path.exists(os.path.join(sorted, filename)):
                            os.rename(f, os.path.join(sorted, filename))
                            file1 = open(append, "a")
                            file1.write(filename)
                            file1.write("\n")
                            file1.close()




        #         try:
        #             with Timeout(300):
        #                 rapc = self.recursive_apc_computer.evaluate(graph)
        #                 rruntime = time.time() - start_time
        #         except Exception as exc:
        #             ex = True
        #             exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
        #         start_time = time.time()
        #         if not ex:
        #             try:
        #                 with Timeout(300):
        #                     apc = self.apc_computer.evaluate(graph)
        #                     runtime = time.time() - start_time
        #             except Exception as exc:
        #                 ex = True
        #                 exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
        #
        #             if not ex:
        #                 try:
        #                     with Timeout(200):
        #                         cyclo = self.cyclo_computer.evaluate(graph)
        #                 except Exception as exc:
        #                     ex = True
        #                     exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
        #
        #                 if not ex:
        #                     try:
        #                         with Timeout(200):
        #                             npath = self.npath_computer.evaluate(graph)
        #                     except Exception as exc:
        #                         ex = True
        #                         exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
        #
        #         new_row = {"file_name": file, "graph_name": graph.name, "apc": apc,
        #                    "rapc": rapc, "cyclo": cyclo, "npath": npath,
        #                    "apc_time": runtime, "rapc_time": rruntime,
        #                    "num_vertices": graph.graph.num_vertices,
        #                    "edge_count": graph.graph.edge_count(), "exception": ex,
        #                    "exception_type": exception_type}
        #
        #         data = data.append(new_row, ignore_index=True)
        #         data.to_csv(f"/app/code/experiments/recursion/data/recursiveData.csv")

def main() -> None:
    """Compute metrics for many graphs."""
    file_sorter = FileSorter()
    file_sorter.sort()


if __name__ == "__main__":
    main()
