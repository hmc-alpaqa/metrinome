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
import sympy
import fc_path_complexity_getrgf
import fc_path_complexity_eliminate

class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level=LogLevel.DEBUG)
        # log = Log(log_level=LogLevel.REGULAR)
        self.converter = CPPConvert(log)
        self.apc_computer = path_complexity.PathComplexity(log)
        self.og_fcapc_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
        self.rfcapc_computer = fc_path_complexity_getrgf.FunctionCallPathComplexity(log)
        self.nfcapc_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
        self.rapc_computer = recursive_path_complexity.RecursivePathComplexity(log)
        self.base_path = "/app/code/experiments/function_calls/files/"

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        rgf_data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcessTime": [], "graphSystemsTime": [], "gammaTime": [], "discrimTime":[], "realnrootsTime":[], "getrgfTime": [], 
                             "apcTime2":[],"longest":[]})
        new_data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcessTime": [], "graphSystemsTime": [],"gammaTime": [], "discrimTime":[], "realnrootsTime":[], "coeffsTime": [], 
                             "genFuncTime":[], "exprsTime": [],"soluTime":[], "UpboundTime":[], "apcTime2":[],"longest":[]})
        with open('/app/code/experiments/optimization/files.txt') as funcs:
            # files = ['/app/code/experiments/recursion/files/catalan-numbers-1.c' ]

            files = [line.rstrip() for line in funcs]

        for file in files:
            print(f"Now analyzing {file}")
            graphs = self.converter.to_graph(os.path.splitext(file)[0], ".c")
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
                apc: Union[str, PathComplexityRes] = "na"
                rapc: Union[str, PathComplexityRes] = "na"
                rfcapc: Union[str, PathComplexityRes] = "na"
                nfcapc: Union[str, PathComplexityRes] = "na"
                exception_type = "na"
                runtime = 0.0
                rruntime = 0.0
                fcruntime = 0.0
                eliminate_runtime = 0.0

                start_time = time.time()
                try:
                    with Timeout(57600):
                        nfcapc = self.nfcapc_computer.evaluate(graph, graphs)
                        nfcapc_runtime = time.time() - start_time
                        print(nfcapc)
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"
                
                new_row = {"file_name": file, "graph_name": graph.name, "nfcapc": nfcapc["nfcapc"], "gamma": nfcapc["gammaTime"], "graphProcess": nfcapc["graphProcessTime"],
                        "graphSystems":nfcapc["graphSystemsTime"], "discrim": nfcapc["discrimTime"], "realnroots": nfcapc["realnrootsTime"], 
                        "genFunc":nfcapc["genFuncTime"],"coeffs": nfcapc["coeffsTime"], 
                        "exprs": nfcapc["exprsTime"], "solu":nfcapc["soluTime"], "Upbound":nfcapc["UpboundTime"], "apcTime2": nfcapc["apcTime2"],
                        "fcapc_time": nfcapc_runtime,"clean":nfcapc["cleanTime"],"exception_type": exception_type,
                        "sum":nfcapc["gammaTime"]+nfcapc["graphProcessTime"]+nfcapc["graphSystemsTime"]+nfcapc["discrimTime"]+nfcapc["realnrootsTime"]
                        +nfcapc["genFuncTime"]+nfcapc["coeffsTime"]+nfcapc["exprsTime"]+nfcapc["soluTime"]+nfcapc["UpboundTime"]+nfcapc["apcTime2"]+nfcapc["cleanTime"]}
                new_data = new_data.append(new_row, ignore_index = True)
                new_data = new_data[["graph_name", "nfcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc","coeffs", "exprs",
                                "solu", "Upbound", "apcTime2", "clean","sum"]]


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

                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes

            for graph_name, graph in graphs.items():

                rfcapc: Union[str, PathComplexityRes] = "na"
                exception_type = "na"
                rfcapc_runtime = 0.0

                start_time = time.time()
                try:
                    with Timeout(200):
                        rfcapc = self.rfcapc_computer.evaluate(graph, graphs)
                        rfcapc_runtime = time.time() - start_time
                        # print(fcapc)
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"
                
                new_row = {"file_name": file, "graph_name": graph.name, "rfcapc": rfcapc["rfcapc"], "gamma": rfcapc["gammaTime"], "graphProcess": rfcapc["graphProcessTime"],
                    "graphSystems":rfcapc["graphSystemsTime"], "discrim": rfcapc["discrimTime"], "realnroots": rfcapc["realnrootsTime"], 
                    "genFunc":rfcapc["genFuncTime"],"getrgf": rfcapc["getrgfTime"], "apcTime2": rfcapc["apcTime2"],
                    "fcapc_time": rfcapc_runtime,"clean":rfcapc["cleanTime"],"exception_type": exception_type,
                    "sum":rfcapc["gammaTime"]+rfcapc["graphProcessTime"]+rfcapc["graphSystemsTime"]+rfcapc["discrimTime"]+rfcapc["realnrootsTime"]
                    +rfcapc["genFuncTime"]+rfcapc["getrgfTime"]+rfcapc["apcTime2"]+rfcapc["cleanTime"]}
                rgf_data = rgf_data.append(new_row, ignore_index = True)
                rgf_data = rgf_data[["graph_name", "rfcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc",
                "getrgf", "apcTime2", "clean","sum"]]

            print(rgf_data[["graph_name", "rfcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", 
            "realnroots", "getrgf","apcTime2","clean"]])

            print(new_data[["graph_name", "nfcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", 
            "realnroots", "genFunc","coeffs", "exprs",
            "solu", "Upbound", "apcTime2","clean"]])

            # create directory if it doesn't exist
            if not os.path.exists("/app/code/experiments/optimization/data"):
                os.makedirs("/app/code/experiments/optimization/data")
            new_data.to_csv(
                "/app/code/experiments/optimization/data/elimData.csv")

            # if not os.path.exists("/app/code/experiments/optimization/data"):
            #     os.makedirs("/app/code/experiments/optimization/data")
            # data.to_csv(
            #     "/app/code/experiments/optimization/data/elimOgData.csv")

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
