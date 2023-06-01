"""Various utilities used only for testing and not the main REPL."""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from metric import cyclomatic_complexity, npath_complexity, path_complexity, fcn_call_path_complexity,recursive_path_complexity
from core.command_data import Data
from lang_to_cfg.cpp import CPPConvert
from core.log import Log, LogLevel
import pandas as pd  # type: ignore
from typing import Union
import time
import os
import sys
from sympy import Number

class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level=LogLevel.DEBUG)
        self.data = Data(log, True)
        # log = Log(log_level=LogLevel.REGULAR)
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.fcn_call_apc_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
        self.recursive_apc_computer = recursive_path_complexity.RecursivePathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)
        self.base_path = "/app/code/experiments/function_calls/files/"

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [], "rapc": [],  "fcapc": [],
                             "cyclo": [], "npath": [], "apc_time": [], "rapc_time": [], "fcapc_time": [],
                             "num_vertices": [], "edge_count": [], "exception": [],
                             "exception_type": []})
        with open('/app/code/experiments/function_calls/files/files.txt') as funcs:
            # files = ['/app/code/experiments/recursion/files/catalan-numbers-1.c' ]

            files = [line.rstrip() for line in funcs]
        
        for file in files:
            print(f"Now analyzing {file}")
            graphs = self.converter.to_graph(os.path.splitext(file)[0], ".c")


            self.data.graphs = graphs
            self.data.show_graphs("*",graphs)

            if graphs is None:
                graphs = self.converter.to_graph(
                    os.path.splitext(file)[0], ".cpp")
            if graphs is None:
                print("No Graphs")
                continue

            for graph_name, graph in graphs.items():
                # if graph_name != 'fcn_calls_cfg._Z9mergeSortPiii.dot':
                # if graph_name != 'fcn_calls_cfg._Z18multi_fact_wrapperi.dot':
                # if graph_name != 'fcn_calls_cfg._Z10fcn_medleyi.dot':
                # if graph_name != 'fcn_calls_cfg._Z15mergeSortSimplePiii.dot':
                    # continue
                print('Graph Name: ', graph_name)
                apc: Union[str, PathComplexityRes] = "na"
                rapc: Union[str, PathComplexityRes] = "na"
                fcapc: Union[str, PathComplexityRes] = "na"
                npath: Union[str, int] = "na"
                cyclo: Union[str, int] = "na"
                exception_type = "na"
                runtime = 0.0
                rruntime = 0.0
                bruntime = 0.0
                start_time = time.time()
                try:
                    with Timeout(2000):
                        # if graph_name != 'fcn_calls_cfg._Z15mergeSortSimplePiii.dot':
                        #     continue
                        fcapc = self.fcn_call_apc_computer.evaluate(graph, graphs)
                        fcruntime = time.time() - start_time
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"

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
                            graph.graph.edges = graph.graph.edges + \
                                [[end, node]]
                        brapc = self.apc_computer.evaluate(graph)
                        bruntime = time.time() - start_time
                        graph.graph.edges = oldEdges
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"

                # start_time = time.time()
                # try:
                #     with Timeout(2000):
                #         rapc = self.recursive_apc_computer.evaluate(graph)
                #         rruntime = time.time() - start_time
                # except Exception as exc:
                #     print(f"Exception: {exc}")
                #     exception_type = "Timeout" if isinstance(
                #         exc, TimeoutError) else "Other"
    
                # start_time = time.time()
                # try:
                #     with Timeout(300):
                #         apc = self.apc_computer.evaluate(graph)
                #         runtime = time.time() - start_time
                # except Exception as exc:
                #     exception_type = "Timeout" if isinstance(
                #         exc, TimeoutError) else "Other"

                # try:
                #     with Timeout(200):
                #         cyclo = self.cyclo_computer.evaluate(graph)
                # except Exception as exc:
                #     exception_type = "Timeout" if isinstance(
                #         exc, TimeoutError) else "Other"

                # try:
                #     with Timeout(200):
                #         npath = self.npath_computer.evaluate(graph)
                # except Exception as exc:
                #     exception_type = "Timeout" if isinstance(
                #         exc, TimeoutError) else "Other"

                new_row = {"file_name": file, "graph_name": graph.name, "apc": apc,
                           "rapc": rapc, "fcapc": fcapc, "cyclo": cyclo, "npath": npath,
                           "apc_time": runtime, "rapc_time": rruntime, "fcapc_time": fcruntime,
                           "num_vertices": graph.graph.num_vertices,
                           "edge_count": graph.graph.edge_count(),
                           "exception_type": exception_type}

                data = data.append(new_row, ignore_index=True)
                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes
                data = data[["graph_name", "fcapc","fcapc_time","num_vertices", "edge_count"]]

                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                # data['rapc'] = data['rapc'].apply(lambda x: round_tuple_of_exprs(x, 3))
                print(data[['graph_name', "fcapc","fcapc_time"]])



                # create directory if it doesn't exist
                if not os.path.exists("/app/code/experiments/function_calls/data"):
                    os.makedirs("/app/code/experiments/function_calls/data")
                data.to_csv(
                    "/app/code/experiments/function_calls/data/functionCallData.csv")

def round_tuple_of_exprs(tup, num_digits):
    return tuple(round_expr(expr, num_digits) for expr in tup)
                
def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})


def main() -> None:
    """Compute metrics for many graphs."""
    data_collector = DataCollector()
    data_collector.collect()


if __name__ == "__main__":
    main()

class Command:
    def show_graphs(self, name: str, names: list[str]) -> None:
        """Display a Graph we know about to the REPL."""
        if name == "*":
            names = list(self.graphs.keys())

        for graph_name in names:
            if graph_name in self.graphs:
                if self.rich:
                    rows = self.graphs[graph_name].rich_repr()
                    table = Table(title=f"Graph {graph_name}")
                    table.add_column("Graph Property", style="cyan")
                    table.add_column("Value", style="magenta")
                    for row in rows:
                        table.add_row(*row)
                    Console().print(table)
                else:
                    self.logger.v_msg(str(self.graphs[graph_name]))
            else:
                self.logger.v_msg(f"Graph {Colors.MAGENTA}{graph_name}{Colors.ENDC} not found.")
 