"""computes the various time used in different part of fc_path_complexity, call fc_path_complexity_time"""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from metric import cyclomatic_complexity, npath_complexity, path_complexity, fcn_call_path_complexity, recursive_path_complexity
import fc_path_complexity_time
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
        self.fcn_call_apc_time_computer = fc_path_complexity_time.FunctionCallPathComplexity(log)
        self.recursive_apc_computer = recursive_path_complexity.RecursivePathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)
        self.base_path = "/app/code/experiments/function_calls/files/"

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcessTime": [], "gammaTime": [], "discrimTime":[], "realnrootsTime":[], "coeffsTime": [], 
                             "exprsTime": [],"soluTime":[], "UpboundTime":[], "apcTime2":[],"longest":[]})
        with open('/app/code/experiments/optimization/files.txt') as funcs:
            # files = ['/app/code/experiments/recursion/files/catalan-numbers-1.c' ]

            files = [line.rstrip() for line in funcs]
        
        for file in files:
            print(f"Now analyzing {file}")
            graphs = self.converter.to_graph(os.path.splitext(file)[0], ".c")


            # self.data.graphs = graphs
            # self.data.show_graphs("*",graphs)

            if graphs is None:
                graphs = self.converter.to_graph(
                    os.path.splitext(file)[0], ".cpp")
            if graphs is None:
                print("No Graphs")
                continue
            print("LIST",graphs.items())

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
                fcruntime = 0.0
                start_time = time.time()
                try:
                    with Timeout(2000):
                        # if graph_name != 'fcn_calls_cfg._Z15mergeSortSimplePiii.dot':
                        #     continue
                        fcapc = self.fcn_call_apc_time_computer.evaluate(graph, graphs)
                        fcruntime = time.time() - start_time
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"

                # start_time = time.time()
                # try:
                #     with Timeout(300):
                #         recurlist = []
                #         end = graph.graph.num_vertices - 1
                #         for node in graph.metadata.calls.keys():
                #             if graph.name.split(".")[1] in graph.metadata.calls[node]:
                #                 recurlist += [int(node)]
                #         oldEdges = graph.graph.edges
                #         for node in recurlist:
                #             graph.graph.edges = graph.graph.edges + [[node, 0]]
                #             graph.graph.edges = graph.graph.edges + \
                #                 [[end, node]]
                #         brapc = self.apc_computer.evaluate(graph)
                #         bruntime = time.time() - start_time
                #         graph.graph.edges = oldEdges
                # except Exception as exc:
                #     print(f"Exception: {exc}")
                #     exception_type = "Timeout" if isinstance(
                #         exc, TimeoutError) else "Other"

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
            

                new_row = {"file_name": file, "graph_name": graph.name, "fcapc": (fcapc["apc"]), "gammaTime": fcapc["gammaTime"], "graphProcessTime": fcapc["graphProcessTime"],
                           "discrimTime": fcapc["discrimTime"], "realnrootsTime": fcapc["realnrootsTime"], "coeffsTime": fcapc["coeffsTime"], 
                           "exprsTime": fcapc["exprsTime"], "soluTime":fcapc["soluTime"], "UpboundTime":fcapc["UpboundTime"], "apcTime2": fcapc["apcTime2"],
                           "fcapc_time": fcruntime,"exception_type": exception_type, "longest":get_max_time(fcapc)}

                data = data.append(new_row, ignore_index = True)
                data = data[["graph_name", "fcapc","fcapc_time", "graphProcessTime", "gammaTime", "discrimTime", "realnrootsTime", "coeffsTime", "exprsTime",
                                "soluTime", "UpboundTime", "apcTime2", "longest"]]
                
                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                data['fcapc'] = data['fcapc'].apply(lambda x: round_expr(x, 3))

                print(data[["graph_name", "fcapc","fcapc_time", "graphProcessTime", "gammaTime", "discrimTime", 
                "realnrootsTime", "coeffsTime", "exprsTime",
                "soluTime", "UpboundTime", "apcTime2", "longest"]])



                # create directory if it doesn't exist
                if not os.path.exists("/app/code/experiments/optimization/data"):
                    os.makedirs("/app/code/experiments/optimization/data")
                data.to_csv(
                    "/app/code/experiments/optimization/data/functionCallData.csv")

def round_tuple_of_exprs(tup, num_digits):
    return tuple(round_expr(expr, num_digits) for expr in tup)
                
def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

def get_max_time(apc):
    l = ["gammaTime","discrimTime", "realnrootsTime", "coeffsTime", 
        "exprsTime", "soluTime", "UpboundTime", "apcTime2"]
    maxTime  = apc[l[0]]
    maxName = 'gammaTime'
    for name in l:
        if apc[name] > maxTime:
            maxTime = apc[name]
            maxName = name
    maxTime = round(maxTime,3)
    return (maxName,maxTime)


def main() -> None:
    """Compute metrics for many graphs."""
    data_collector = DataCollector()
    data_collector.collect()


if __name__ == "__main__":
    main()