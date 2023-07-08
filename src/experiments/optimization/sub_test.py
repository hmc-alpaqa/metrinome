"""
helper function for the test files, end up not using it

to use it, do
    helper = sub_test.Helper()
    apc,runtime, fakenonZeroIndex = helper.callEvaluate(graph,graphs,"apc",100)
"""
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
from sympy import Number
from functools import lru_cache

class Helper:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """..."""
        # log = Log(log_level=LogLevel.DEBUG)
        # log = Log(log_level=LogLevel.REGULAR)
        # self.converter = CPPConvert(log)
        # self.base_path = "/app/code/experiments/function_calls/files/"

    # nfcapc stands for new function call apc, which is the apc computed by fc_path_complexity_final
    # pylint: disable=broad-except
    # @lru_cache(maxsize =None)  # tried to unable caching, but error occurs
    def callEvaluate(self, graph, graphs, metric, tryTime) -> None:
        """Compute the metrics for all files and store the data."""
        log = Log(log_level=LogLevel.DEBUG)
        # self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
        # self.npath_computer = npath_complexity.NPathComplexity(log)

        apc: Union[str, PathComplexityRes] = "na"
        runtime = 0.0
        exception_type = "na"
        nonZeroIndex = 0
        
        if (metric == 'apc'):
            print(f"=========================runing regular path complexity for {tryTime} seconds==========================")
            start_time = time.time()
            try:
                with Timeout(tryTime):
                    self.apc_computer = path_complexity.PathComplexity(log)
                    apc = self.apc_computer.evaluate(graph)
                    runtime = time.time() - start_time
            except Exception as exc:
                exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

        if (metric == 'rapc'):
            print(f"====================running recursive function path complexity for {tryTime} seconds==========================")
            start_time = time.time()
            try:
                with Timeout(tryTime):
                    self.recursive_apc_computer = recursive_path_complexity.RecursivePathComplexity(log)
                    apc = self.recursive_apc_computer.evaluate(graph)
                    runtime = time.time() - start_time
            except Exception as exc:
                print(f"Exception: {exc}")
                exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

        if (metric == 'fcapc'):
            print(f"=====================running old fcn_call_path_complexity for {tryTime} seconds=========================")
            start_time = time.time()
            try:
                with Timeout(tryTime):
                    self.fcn_call_apc_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
                    apc, nonZeroIndex = self.fcn_call_apc_computer.evaluate(graph, graphs)
                    runtime = time.time() - start_time
            except Exception as exc:
                print(f"Exception: {exc}")
                exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

        if (metric == "nfcapc"):
            print(f"======================running new fcn_call_path_complexity for {tryTime} seconds=======================")
            start_time = time.time()
            try:
                with Timeout(tryTime):
                    self.optimized_elim_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
                    apc = self.optimized_elim_computer.evaluate(graph, graphs)
                    runtime = time.time() - start_time
            except Exception as exc:
                exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

        return apc, runtime, nonZeroIndex



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

            


# def round_tuple_of_exprs(tup, num_digits):
#     return tuple(round_expr(expr, num_digits) for expr in tup)
                
# def round_expr(expr, num_digits):
#     return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

# def get_max_time(apc):
#     l = ["graphProcessTime","graphSystemsTime", "gammaTime", "discrimTime", 
#         "realnrootsTime", "genFuncTime", "coeffsTime", "exprsTime","soluTime", "UpboundTime","apcTime2","cleanTime"]
#     maxTime  = apc[l[0]]
#     maxName = 'graphProcessTime'
#     for name in l:
#         if apc[name] > maxTime:
#             maxTime = apc[name]
#             maxName = name
#     maxTime = round(maxTime,3)
#     return (maxName,maxTime)

# def main() -> None:
#     """Compute metrics for many graphs."""
#     data_collector = DataCollector()
#     data_collector.collect()


# if __name__ == "__main__":
#     main()
