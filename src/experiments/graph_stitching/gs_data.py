"""Various utilities used only for testing and not the main REPL."""
import os
import time
from typing import Union

import pandas as pd  # type: ignore

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph
from lang_to_cfg.cpp import CPPConvert
from metric import cyclomatic_complexity, npath_complexity, path_complexity
from metric.path_complexity import PathComplexityRes
from utils import Timeout


class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log()
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)
        self.base_path = "/app/code/experiments/icse_experiment/files/"

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [],
                             "cyclo": [], "npath": [], "apc_time": [],
                             "num_vertices": [], "edge_count": [], "exception": [],
                             "exception_type": []})

        with open('/app/code/experiments/graph_stitching/files/files.txt') as funcs:
            files = [line[0:-1] for line in funcs]

        for file in files:
            print(file)
            fname = os.path.splitext(file)[0]
            graphs = self.converter.to_graph(fname, ".c")
            if graphs is None:
                continue
            if isinstance(graphs, dict):
                graphs["stitched"] = ControlFlowGraph.stitch(graphs, name=os.path.basename(fname)+"_full")
            
            graph = graphs["stitched"]

            start_time = time.time()
            apc: Union[str, PathComplexityRes] = "na"
            npath: Union[str, int] = "na"
            cyclo: Union[str, int] = "na"
            ex = False
            exception_type = "na"
            runtime = 0.0
            try:
                with Timeout(300):
                    apc = self.apc_computer.evaluate(graph)
                    runtime = time.time() - start_time
            except Exception as exc:
                ex = True
                exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

            if not ex:
                try:
                    with Timeout(200):
                        cyclo = self.cyclo_computer.evaluate(graph)
                except Exception as exc:
                    ex = True
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                if not ex:
                    try:
                        with Timeout(200):
                            npath = self.npath_computer.evaluate(graph)
                    except Exception as exc:
                        ex = True
                        exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

            new_row = {"file_name": file, "graph_name": graph.name, "apc": apc,
                       "cyclo": cyclo, "npath": npath, "apc_time": runtime,
                       "num_vertices": graph.graph.num_vertices,
                       "edge_count": graph.graph.edge_count(), "exception": ex,
                       "exception_type": exception_type}

            data = data.append(new_row, ignore_index=True)
            data.to_csv("/app/code/experiments/graph_stitching/draft.csv")


def main() -> None:
    """Compute metrics for many graphs."""
    data_collector = DataCollector()
    data_collector.collect()


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
