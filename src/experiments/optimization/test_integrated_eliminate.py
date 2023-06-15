"""compare the fcn call path complexity and recursive path complexity and their run time for 
   files in experiments/function_calls/files/files.txt"""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from metric import cyclomatic_complexity, npath_complexity, path_complexity, fcn_call_path_complexity, recursive_path_complexity
from lang_to_cfg.cpp import CPPConvert
from core.log import Log, LogLevel
import pandas as pd  # type: ignore
from typing import Union
import time
import os
import sys
from sympy import Number
import fc_path_complexity_eliminate
import fc_path_complexity_elim_og

class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level=LogLevel.DEBUG)
        # log = Log(log_level=LogLevel.REGULAR)
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.fcn_call_apc_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
        self.fcn_call_apc_time_computer = fc_path_complexity_elim_og.FunctionCallPathComplexity(log)
        self.optimized_elim_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
        self.recursive_apc_computer = recursive_path_complexity.RecursivePathComplexity(log)
        self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        self.npath_computer = npath_complexity.NPathComplexity(log)
        self.base_path = "/app/code/experiments/function_calls/files/"

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcessTime": [], "graphSystemsTime": [], "gammaTime": [], "discrimTime":[], "realnrootsTime":[], "coeffsTime": [], 
                             "exprsTime": [],"soluTime":[], "UpboundTime":[], "apcTime2":[],"longest":[]})
        data_elim = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcessTime": [], "graphSystemsTime": [],"gammaTime": [], "discrimTime":[], "realnrootsTime":[], "coeffsTime": [], 
                             "genFuncTime":[], "exprsTime": [],"soluTime":[], "UpboundTime":[], "apcTime2":[],"longest":[]})
        with open('/app/code/experiments/optimization/files.txt') as funcs:
            # files = ['/app/code/experiments/recursion/files/catalan-numbers-1.c' ]

            files = [line.rstrip() for line in funcs]

        for file in files:
            print(f"Now analyzing {file}")
            graphs = self.converter.to_graph(os.path.splitext(file)[0], ".c")
            print(graphs)
            if graphs is None:
                graphs = self.converter.to_graph(
                    os.path.splitext(file)[0], ".cpp")
            if graphs is None:
                print("No Graphs")
                continue

            for graph_name, graph in graphs.items():
                print("GRAPH?", graph)
                # if graph_name != 'fcn_calls_cfg._Z9mergeSortPiii.dot':
                # if graph_name != 'fcn_calls_cfg._Z18multi_fact_wrapperi.dot':
                # if graph_name != 'fcn_calls_cfg._Z10fcn_medleyi.dot':
                # if graph_name != 'fcn_calls_cfg._Z15mergeSortSimplePiii.dot':
                    # continue
                print('Graph Name: ', graph_name)
                apc: Union[str, PathComplexityRes] = "na"
                rapc: Union[str, PathComplexityRes] = "na"
                fcapc: Union[str, PathComplexityRes] = "na"
                eliminate_apc: Union[str, PathComplexityRes] = "na"
                npath: Union[str, int] = "na"
                cyclo: Union[str, int] = "na"
                exception_type = "na"
                runtime = 0.0
                rruntime = 0.0
                fcruntime = 0.0
                eliminate_runtime = 0.0
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


                start_time = time.time()
                try:
                    with Timeout(57600):
                        eliminate_apc, elim_times = self.optimized_elim_computer.evaluate(graph, graphs)
                        eliminate_runtime = time.time() - start_time
                        print(elim_times)
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"
 
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

                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes

                # print(fcapc)
                new_row = {"file_name": file, "graph_name": graph.name, "fcapc": (fcapc["apc"]), "graphSystemsTime": fcapc["graphSystemsTime"],"gammaTime": fcapc["gammaTime"], "graphProcessTime": fcapc["graphProcessTime"],
                           "discrimTime": fcapc["discrimTime"], "realnrootsTime": fcapc["realnrootsTime"], "coeffsTime": fcapc["coeffsTime"], 
                           "exprsTime": fcapc["exprsTime"], "soluTime":fcapc["soluTime"], "UpboundTime":fcapc["UpboundTime"], "apcTime2": fcapc["apcTime2"],
                           "fcapc_time": fcruntime,"exception_type": exception_type}

                data = data.append(new_row, ignore_index = True)
                data = data[["graph_name", "fcapc","fcapc_time", "graphProcessTime", "graphSystemsTime","gammaTime", "discrimTime", "realnrootsTime", "coeffsTime", "exprsTime",
                                "soluTime", "UpboundTime", "apcTime2", "longest"]]
                
                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                data['fcapc'] = data['fcapc'].apply(lambda x: round_expr(x, 3))

                new_row = {"file_name": file, "graph_name": graph.name, "fcapc": eliminate_apc[0], "gamma": elim_times["gammaTime"], "graphProcess": elim_times["graphProcessTime"],
                           "graphSystems":elim_times["graphSystemsTime"], "discrim": elim_times["discrimTime"], "realnroots": elim_times["realnrootsTime"], 
                           "genFunc":elim_times["genFuncTime"],"coeffs": elim_times["coeffsTime"], 
                           "exprs": elim_times["exprsTime"], "solu":elim_times["soluTime"], "Upbound":elim_times["UpboundTime"], "apcTime2": elim_times["apcTime2"],
                           "fcapc_time": eliminate_runtime,"clean":elim_times["cleanTime"],"exception_type": exception_type,
                           "sum":elim_times["gammaTime"]+elim_times["graphProcessTime"]+elim_times["graphSystemsTime"]+elim_times["discrimTime"]+elim_times["realnrootsTime"]
                           +elim_times["genFuncTime"]+elim_times["coeffsTime"]+elim_times["exprsTime"]+elim_times["soluTime"]+elim_times["UpboundTime"]+elim_times["apcTime2"]+elim_times["cleanTime"]}
                data_elim = data_elim.append(new_row, ignore_index = True)
                data_elim = data_elim[["graph_name", "fcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc","coeffs", "exprs",
                                "solu", "Upbound", "apcTime2", "clean","sum"]]
                data_elim['fcapc'] = data_elim['fcapc'].apply(lambda x: round_expr(x, 3))

                print(data[["graph_name", "fcapc","fcapc_time", "graphProcessTime", "graphSystemsTime","gammaTime", "discrimTime", 
                "realnrootsTime", "coeffsTime", "exprsTime",
                "soluTime", "UpboundTime", "apcTime2"]])

                print(data_elim[["graph_name", "fcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", 
                "realnroots", "genFunc","coeffs", "exprs",
                "solu", "Upbound", "apcTime2","clean","sum"]])


                 # create directory if it doesn't exist
                if not os.path.exists("/app/code/experiments/optimization/data"):
                    os.makedirs("/app/code/experiments/optimization/data")
                data_elim.to_csv(
                    "/app/code/experiments/optimization/data/solvevsNsolveData.csv")

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
