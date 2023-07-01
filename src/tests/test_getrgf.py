"""test file for new function call apc"""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from lang_to_cfg.cpp import CPPConvert
from core.log import Log, LogLevel
import pandas as pd  # type: ignore
from typing import Union
import time
import os
import sys
from experiments.optimization import fc_path_complexity_getrgf
from sympy import Number

class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level=LogLevel.DEBUG)
        self.getrgf_computer = fc_path_complexity_getrgf.FunctionCallPathComplexity(log)
        self.converter = CPPConvert(log)

    # nfcapc stands for new function call apc, which is the apc computed by fc_path_complexity_final
    # pylint: disable=broad-except
    # @lru_cache(maxsize =None) #disable caching, but not working
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "getrgfapc": [],
                             "getrgfapc_time": [], "exception": [],"exception_type": []})
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
               
                nfcapc: Union[str, PathComplexityRes] = {"nfcapc":"na"}
                exception_type = "na"
                nfcruntime = 0.0

                print("======================running getrgf fcn_call_path_complexity for 4000 seconds=======================")
                start_time = time.time()
                try:
                    with Timeout(4000):
                        nfcapc = self.getrgf_computer.evaluate(graph, graphs)
                        nfcruntime = time.time() - start_time
                        print(nfcapc)
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                
                new_row = {"file_name": file, "graph_name": graph.name,  "getrgfapc": nfcapc["nfcapc"], 
                        "getrgfapc_time": nfcruntime, "longest for getrgf": get_max_time(nfcapc)[0], "longest time":get_max_time(nfcapc)[1], "exception_type": exception_type}

                data = data.append(new_row, ignore_index=True)
                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes
                data = data[["graph_name", "getrgfapc", "getrgfapc_time", "longest for getrgf", "longest time"]]

                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                # data['rapc'] = data['rapc'].apply(lambda x: round_tuple_of_exprs(x, 3))
                # print(data[['graph_name', "apc",'rapc',"rapc_time","fcapc","fcapc_time"]])
                print(data[["graph_name", "getrgfapc", "getrgfapc_time", "longest for getrgf", "longest time"]])


                # create directory if it doesn't exist
                if not os.path.exists("/app/code/tests/data"):
                    os.makedirs("/app/code/tests/data")
                data.to_csv("/app/code/tests/data/getrgfapc_data.csv")


def round_tuple_of_exprs(tup, num_digits):
    return tuple(round_expr(expr, num_digits) for expr in tup)
                
def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

def get_max_time(apc):
    l = ["graphProcessTime","graphSystemsTime", "gammaTime", "discrimTime", 
        "realnrootsTime", "genFuncTime", "rootsDictTime","getrgfTime","apcTime2","cleanTime"]
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
