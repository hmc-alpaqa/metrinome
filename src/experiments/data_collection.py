"""Various utilities used only for testing and not the main REPL."""
import os
import time
from typing import Union

import pandas as pd  # type: ignore

from core.log import Log
from lang_to_cfg.cpp import CPPConvert
from metric import cyclomatic_complexity, npath_complexity, path_complexity
from metric.path_complexity import PathComplexityRes
from utils import Timeout
from rich.progress import track


class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self, log: Log, input_path: str, output_path: str) -> None:
        """Create a new instance of the data collector."""
        self.logger = log
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)
        self.base_path = input_path
        self.output_path = output_path

    # pylint: disable=broad-except
    def collect(self, files: list[str]) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [],
                             "cyclo": [], "npath": [], "apc_time": [],
                             "num_vertices": [], "edge_count": [], "exception": [],
                             "exception_type": []})

        for file in track(files, description="Now analyzing your files: "):
            # self.logger.v_msg(f"Now analyzing {file}")
            graphs = self.converter.to_graph(os.path.splitext(file)[0], ".c")
            if graphs is None:
                continue

            for graph in graphs.values():
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
                data.to_csv(f"{self.output_path}.csv")
