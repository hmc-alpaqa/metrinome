"""test file for new function call apc (getrgf)"""
from utils import Timeout
from metric.path_complexity import PathComplexityRes
from metric import fcn_call_path_complexity
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
        self.getrgf_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
        self.converter = CPPConvert(log)

    # nfcapc stands for new function call apc, which is the apc computed by fc_path_complexity_final
    # pylint: disable=broad-except
    # @lru_cache(maxsize =None) #disable caching, but not working

    

    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        data = pd.DataFrame({"file_name": [], "graph_name": [], "getrgfapc": [],
                             "getrgfapc_time": [], "firstHalfTime": [], "getrgfTime":[],
                             "exception": [],"exception_type": [],"case":[],'gamma':[]})
                             
        with open("/app/code/chooseFile.txt") as filess:
            filePath = [line.rstrip() for line in filess]
            print(filePath)
        with open(filePath[0]) as funcs:
            # files = ['/app/code/experiments/recursion/files/catalan-numbers-1.c' ]
            files = [line.rstrip() for line in funcs]

        for i in files:
            file = i.split()[0]
            funcs = i.split()[1:]
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
               
                getrgfapc: Union[str, PathComplexityRes] = {'rfcapc': 'na', "getrgfTime": 'na', "firstHalfTime": 'na'}
                exception_type = "na"
                getrgfruntime = 0.0

                if notin(graph_name, funcs):
                    continue

                print("======================running getrgf fcn_call_path_complexity for 4000 seconds=======================")
                start_time = time.time()
                try:
                    with Timeout(4000):
                        getrgfapc = self.getrgf_computer.evaluate(graph, graphs)
                        print(getrgfapc)
                        getrgfruntime = time.time() - start_time
                        # if "V0_3" in str(getrgfapc["rfcapc"]):
                        #     print("ERROR V0_3 in apc")
                        #     sys.exit()
                        # if getrgfapc['rfcapc'] == 'na':
                        #     print("ERROR apc didn't complete")
                        #     sys.exit()
                        # if str(getrgf['rfcapc']) != "0.150373068898858*1.30927065104311**n":
                        #     print("error incorrect apc:",getrgf['rfcapc'])
                        #     sys.exit()
                except Exception as exc:
                    print(exc)
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                
                new_row = {"file_name": file, "graph_name": graph.name,  "getrgfapc": getrgfapc["rfcapc"], 
                        "getrgfapc_time": getrgfruntime, "longest for getrgf": get_max_time(getrgfapc)[0], "longest time":get_max_time(getrgfapc)[1], 
                        "getrgfTime":getrgfapc["getrgfTime"], "firstHalfTime": getrgfapc['firstHalfTime'],
                        "exception_type": exception_type,'case':getrgfapc['case'],'gamma':getrgfapc['gamma']}

                data = data.append(new_row, ignore_index=True)
                # only keep columns graph_name, rapc, fcapc, num_vertices, edge_count, and runtimes
                data = data[["graph_name", "getrgfapc", "getrgfapc_time", 'getrgfTime', 'firstHalfTime', "longest for getrgf", "longest time",'case','gamma']]

                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                # data['rapc'] = data['rapc'].apply(lambda x: round_tuple_of_exprs(x, 3))
                # print(data[['graph_name', "apc",'rapc',"rapc_time","fcapc","fcapc_time"]])
                print(data[["graph_name", "getrgfapc", "getrgfapc_time", 'getrgfTime', 'firstHalfTime']])


                # create directory if it doesn't exist
                if not os.path.exists("/app/code/experiments/function_calls/data"):
                    os.makedirs("/app/code/experiments/function_calls/data")
                data.to_csv("/app/code/experiments/function_calls/data/getrgfapc_data.csv")


def round_tuple_of_exprs(tup, num_digits):
    return tuple(round_expr(expr, num_digits) for expr in tup)
                
def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})

def get_max_time(apc):
    if apc == {'rfcapc':"na"}:
        return ("na",0)
    l = ["graphProcessTime","graphSystemsTime", "gammaTime", "discrimTime", 
        "realnrootsTime", "genFuncTime", "rootsDictTime","getrgfTime","apcTime2","cleanTime"]
    maxTime  = apc[l[0]]
    maxName = 'graphProcessTime'
    for name in l:
        if type(apc[name]) == float and apc[name] > maxTime:
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
