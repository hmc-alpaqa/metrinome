"""compare the fcn call path complexity and recursive path complexity and their run time for 
   files in experiments/function_calls/files/files.txt"""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from lang_to_cfg.cpp import CPPConvert
from core.log import Log, LogLevel
import pandas as pd  # type: ignore
from typing import Union
import time
import os
import sys
from sympy import Number
import sympy
from experiments.optimization import fc_path_complexity_elim_og

class DataCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        log = Log(log_level=LogLevel.DEBUG)
        # log = Log(log_level=LogLevel.REGULAR)
        self.converter = CPPConvert(log)
        self.og_fcapc_computer = fc_path_complexity_elim_og.FunctionCallPathComplexity(log)

    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "ogapc": [],
                     "ogapc_time": [],"exception": [], "exception_type": []})
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
                print('Graph Name: ', graph_name)

                ogapc: Union[str, PathComplexityRes] = {'apc':"na",'pc':"na"}
                exception_type = "na"
                ogruntime = 0.0

                print("======================running og fcn_call_path_complexity for 200 seconds=======================")
                start_time = time.time()
                try:
                    with Timeout(200):
                        ogapc = self.og_fcapc_computer.evaluate(graph, graphs)
                        ogruntime = time.time() - start_time
                        # print(ogapc)
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
                
                new_row = {"file_name": file, "graph_name": graph.name, "ogapc": (ogapc["apc"],ogapc['pc']), 
                        "ogapc_time": ogruntime,
                        'longest for og':get_max_time(ogapc)[0],"longest time":get_max_time(ogapc)[1],"exception_type": exception_type}

                data = data.append(new_row, ignore_index = True)
                data = data[["graph_name", "ogapc","ogapc_time",'longest for og','longest time']]


                print(data[["graph_name", "ogapc","ogapc_time",'longest for og','longest time']])

                # create directory if it doesn't exist
                if not os.path.exists("/app/code/tests/data"):
                    os.makedirs("/app/code/tests/data")
                data.to_csv("/app/code/tests/data/ogapc_data.csv")


def round_tuple_of_exprs(tup, num_digits):
    return tuple(round_expr(expr, num_digits) for expr in tup)
                
def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

def get_max_time(apc):
    if apc == {'apc':"na",'pc':"na"}:
        return ("na",0)
    l = ["graphProcessTime","graphSystemsTime", "gammaTime", "discrimTime", 
        "realnrootsTime", "coeffsTime", 'exprsTime',"soluTime",'UpboundTime',"apcTime2","cleanTime"]
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
