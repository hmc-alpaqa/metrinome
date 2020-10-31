"""Various utilities used only for testing and not the main REPL."""
import os
import time
from typing import Union
import glob2  # type: ignore
import pandas as pd  # type: ignore
from log import Log
from utils import Timeout
from lang_to_cfg.cpp import CPPConvert
from metric import path_complexity, cyclomatic_complexity, npath_complexity
from metric.path_complexity import PathComplexityRes


class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log()
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [],
                             "cyclo": [], "npath": [], "apc_time": [],
                             "graph_size": [], "basecasetype": [], "exception": [],
                             "exception_type": []})

        files = glob2.glob("/app/code/tests/cFiles/fse_2020_benchmark/*.c")
        for file in files[2:]:
            print(file)
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
                basecasetype = "BFS"
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
                           "graph_size": len(graph.graph.vertices),
                           "basecasetype": basecasetype, "exception": ex,
                           "exception_type": exception_type}

                data = data.append(new_row, ignore_index=True)
                data.to_csv("/app/code/data_collection_full.csv")


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
