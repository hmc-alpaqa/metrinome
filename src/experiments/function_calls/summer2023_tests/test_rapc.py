"""test file for recursive apc"""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from metric import recursive_path_complexity
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
        self.rapc_computer = recursive_path_complexity.RecursivePathComplexity(log)
        self.converter = CPPConvert(log)

    # nfcapc stands for new function call apc, which is the apc computed by fc_path_complexity_final
    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "rapc": [], "rapc_time": [],"exception": [],"exception_type": []})
        with open("/app/code/chooseFile.txt") as filess:
            filePath = [line.rstrip() for line in filess]
            print(filePath)
        with open(filePath[0]) as funcs:
            # files = ['/app/code/experiments/recursion/files/catalan-numbers-1.c' ]
            files = [line.rstrip() for line in funcs]

        for i in files:
            file = i.split()[0]
            funcs = i.split()[1:]
            print(f"function that we wish to analyze: {funcs}")
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
                # if graph_name == 'sudoku_f2f_cfg._Z7trycellPii.dot':
                #     new_row = {"file_name": file, "graph_name": graph.name, "rapc": 'na',
                #            "rapc_time": 'na'}
                #     data = data.append(new_row, ignore_index=True)
                #     data = data[["graph_name", "rapc", "rapc_time"]]
                #     print(data[["graph_name", "rapc", "rapc_time"]])

                #     if not os.path.exists("/app/code/experiments/function_calls/data"):
                #         os.makedirs("/app/code/experiments/function_calls/data")
                #     data.to_csv("/app/code/experiments/function_calls/data/rapc_data.csv")
                #     continue

                # if graph_name == 'truncatable_primes_f2f_cfg._Z4leftii.dot':
                #     new_row = {"file_name": file, "graph_name": graph.name, "rapc": 'na',
                #            "rapc_time": 'na'}
                #     data = data.append(new_row, ignore_index=True)
                #     data = data[["graph_name", "rapc", "rapc_time"]]
                #     print(data[["graph_name", "rapc", "rapc_time"]])

                #     if not os.path.exists("/app/code/experiments/function_calls/data"):
                #         os.makedirs("/app/code/experiments/function_calls/data")
                #     data.to_csv("/app/code/experiments/function_calls/data/rapc_data.csv")
                #     continue
                
                rapc: Union[str, PathComplexityRes] = "na"
                exception_type = "na"
                rruntime = 0.0
            
                if notin(graph_name, funcs):
                    continue
                
                if graph_name == "bubble_sort_2_cfg.bubble_sort.dot" or graph_name == "heap_sort_2_cfg.heapSort.dot":
                    new_row = {"file_name": file, "graph_name": graph.name, "rapc": 'na',
                          "rapc_time": 'na'}
                    data = data.append(new_row, ignore_index=True)
                    data = data[["graph_name", "rapc", "rapc_time"]]
                    print(data[["graph_name", "rapc", "rapc_time"]])
                    if not os.path.exists("/app/code/experiments/function_calls/data"):
                        os.makedirs("/app/code/experiments/function_calls/data")
                    data.to_csv("/app/code/experiments/function_calls/data/rapc_data.csv")
                    continue

                print("=========================runing recursive path complexity for 200 seconds==========================")
                start_time = time.time()
                try:
                    with Timeout(200):
                        rapc = self.rapc_computer.evaluate(graph)
                        rruntime = time.time() - start_time
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"


                new_row = {"file_name": file, "graph_name": graph.name, "rapc": rapc,
                           "rapc_time": rruntime,"exception_type": exception_type}

                data = data.append(new_row, ignore_index=True)
                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes
                data = data[["graph_name", "rapc", "rapc_time"]]

                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                # data['rapc'] = data['rapc'].apply(lambda x: round_tuple_of_exprs(x, 3))
                # print(data[['graph_name', "apc",'rapc',"rapc_time","fcapc","fcapc_time"]])
                print(data[["graph_name", "rapc", "rapc_time"]])


                # create directory if it doesn't exist
                if not os.path.exists("/app/code/experiments/function_calls/data"):
                    os.makedirs("/app/code/experiments/function_calls/data")
                data.to_csv("/app/code/experiments/function_calls/data/rapc_data.csv")


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

def notin(graph_name, funcs):
    """check if graph_name is in func"""
    if funcs == []:
        return False
    for func in funcs:
        graphName = graph_name.split(".")[1]
        if func in graphName:
            return False
    return True

def main() -> None:
    """Compute metrics for many graphs."""
    data_collector = DataCollector()
    data_collector.collect()


if __name__ == "__main__":
    main()
