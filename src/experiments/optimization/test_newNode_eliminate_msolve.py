"""compare the regular path complexity, recursive path complexity, new fcn calls path complexity, and their run time for 
   files in experiments/optimization/files.txt"""
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
import fc_path_complexity_eliminate
import sub_test
from sympy import Number
from functools import lru_cache

class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level=LogLevel.DEBUG)
        # log = Log(log_level=LogLevel.REGULAR)
        self.converter = CPPConvert(log)
        self.base_path = "/app/code/experiments/function_calls/files/"

    # nfcapc stands for new function call apc, which is the apc computed by fc_path_complexity_final
    # pylint: disable=broad-except
    # @lru_cache(maxsize =None) #disable caching, but not working
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [], "rapc": [],  "nfcapc": [], "fcapc":[], 
                             "cyclo": [], "npath": [], "apc_time": [], "rapc_time": [], "nfcapc_time": [], "fcapc_time":[], 
                             "num_vertices": [], "edge_count": [], "exception": [],
                             "exception_type": []})
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
                print('Graph Name: ', graph_name)
                log = Log(log_level=LogLevel.DEBUG)
                self.apc_computer = path_complexity.PathComplexity(log)
                self.fcn_call_apc_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
                self.optimized_elim_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
                self.recursive_apc_computer = recursive_path_complexity.RecursivePathComplexity(log)
                self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
                self.npath_computer = npath_complexity.NPathComplexity(log)

                apc: Union[str, PathComplexityRes] = "na"
                rapc: Union[str, PathComplexityRes] = "na"
                fcapc: Union[str, PathComplexityRes] = "na"
                nfcapc: Union[str, PathComplexityRes] = {"nfcapc":"na"}
                npath: Union[str, int] = "na"
                cyclo: Union[str, int] = "na"
                exception_type = "na"
                runtime = 0.0
                rruntime = 0.0
                fcruntime = 0.0
                nfcruntime = 0.0
                nonZeroIndex = 0.0
                # fakenonZeroIndex = 0.0

                
                # print("=====================running old fcn_call_path_complexity for 200 seconds=========================")
                # start_time = time.time()
                # try:
                #     with Timeout(200):   
                #         fcapc, nonZeroIndex = self.fcn_call_apc_computer.evaluate(graph, graphs)
                #         fcruntime = time.time() - start_time
                # except Exception as exc:
                #     print(f"Exception: {exc}")
                #     exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                print("======================running new fcn_call_path_complexity for 4000 seconds=======================")
                start_time = time.time()
                try:
                    with Timeout(4000):
                        nfcapc = self.optimized_elim_computer.evaluate(graph, graphs)
                        nfcruntime = time.time() - start_time
                        print(nfcapc)
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"

                # print("====================running recursive function path complexity for 100 seconds==========================")
                # start_time = time.time()
                # try:
                #     with Timeout(100):
                #         rapc = self.recursive_apc_computer.evaluate(graph)
                #         rruntime = time.time() - start_time
                # except Exception as exc:
                #     print(f"Exception: {exc}")
                #     exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
    
                # print("=========================runing regular path complexity for 100 seconds==========================")
                # start_time = time.time()
                # try:
                #     with Timeout(100):
                #         
                #         apc = self.apc_computer.evaluate(graph)
                #         runtime = time.time() - start_time
                # except Exception as exc:
                #     exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                #############################trying sub_test, not working########################
                # sub_test.cache_clear()
                # helper = sub_test.Helper()
                # apc,runtime, fakenonZeroIndex = helper.callEvaluate(graph,graphs,"apc",100)
                #
                # helper = sub_test.Helper()
                # rapc,rruntime, fakenonZeroIndex = helper.callEvaluate(graph,graphs,"rapc",100)
                #
                # helper1 = sub_test.Helper()
                # nfcapc,nfcruntime, fakenonZeroIndex = helper1.callEvaluate(graph,graphs,"nfcapc",4000)
                #
                # helper = sub_test.Helper()
                # fcapc,fcruntime, nonZeroIndex = helper.callEvaluate(graph,graphs,"fcapc",200)
                #
                # helper1 = sub_test.Helper()
                # nfcapc,nfcruntime, fakenonZeroIndex = helper1.callEvaluate(graph,graphs,"nfcapc",4000)
                ##############################################################################

                
                # nfcapc,nfcruntime = callnfcapc(self,graph,graphs,4000)
                # callnfcapc.cache_clear()


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
                #     exception_type = "Timeout" if isinstance(self.optimized_elim_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
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
                           "rapc": rapc, "nfcapc": nfcapc["nfcapc"], 'fcapc':fcapc, "cyclo": cyclo, "npath": npath,
                           "apc_time": runtime, "rapc_time": rruntime, "nfcapc_time": nfcruntime, "fcapc_time":fcruntime,
                           "longest for nfcapc": get_max_time(nfcapc)[0], "longest time":get_max_time(nfcapc)[1],
                           "numNode": nfcapc["numNodes"], "nonZeroIndex": nonZeroIndex,
                           "num_vertices": graph.graph.num_vertices,
                           "edge_count": graph.graph.edge_count(),
                           "exception_type": exception_type}

                data = data.append(new_row, ignore_index=True)
                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes
                data = data[["graph_name", "apc","rapc", "nfcapc", 'fcapc', "apc_time","rapc_time","nfcapc_time",'fcapc_time', "longest for nfcapc", "longest time","numNode","nonZeroIndex"]]

                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                # data['rapc'] = data['rapc'].apply(lambda x: round_tuple_of_exprs(x, 3))
                # print(data[['graph_name', "apc",'rapc',"rapc_time","fcapc","fcapc_time"]])
                print(data[["graph_name","nfcapc_time",'fcapc_time', "longest for nfcapc", "longest time","numNode","nonZeroIndex"]])


                # create directory if it doesn't exist
                if not os.path.exists("/app/code/experiments/optimization/data"):
                    os.makedirs("/app/code/experiments/optimization/data")
                data.to_csv("/app/code/experiments/optimization/data/finalTestData.csv")


######################tried calling helper functions in order to clean up cache, not working#######################
# @lru_cache(maxsize = None)
# def callnfcapc (self,graph,graphs,tryTime):
#     print(f"======================running new fcn_call_path_complexity for {tryTime} seconds=======================")
#     apc: Union[str, PathComplexityRes] = {"nfcapc":"na"}
#     runtime = 0.0
#     log = Log(log_level=LogLevel.DEBUG)
#     self.optimized_elim_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
#     start_time = time.time()
#     try:
#         with Timeout(tryTime): 
#             apc = self.optimized_elim_computer.evaluate(graph, graphs)
#             runtime = time.time() - start_time
#     except Exception as exc:
#         exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
#     return apc, runtime
###################################################################


def round_tuple_of_exprs(tup, num_digits):
    return tuple(round_expr(expr, num_digits) for expr in tup)
                
def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

def get_max_time(apc):
    l = ["graphProcessTime","graphSystemsTime", "gammaTime", "discrimTime", 
        "realnrootsTime", "genFuncTime", "coeffsTime", "exprsTime","soluTime", "UpboundTime","apcTime2","cleanTime"]
    maxTime  = apc[l[0]]
    maxName = 'graphProcessTime'
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
