"""compare the regular path complexity, recursive path complexity, new fcn calls path complexity, and their run time for 
   files in experiments/optimization/files.txt
   
   The runtime for each metric depends on the order in which we test it. end up not using this. 
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
import fc_path_complexity_eliminate, fc_path_complexity_elim_og, fc_path_complexity_getrgf
from sympy import Number

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

        # data for all metrics and their overall runtimes
        data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [], "rapc": [],  "fcapc": [], "efcapc":[], "eofcapc":[], "rgfcapc":[],
                             "apc_time": [], "rapc_time": [], "fcapc_time": [], "efcapc_time":[], "eofcapc_time":[], "rgfcapc_time":[],
                             "exception": [], "exception_type": []})

        # time breakdowns for all the metrics in the optimization folder
        elim_data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcess": [], "graphSystems": [],"gamma": [], "discrim":[], "realnroots":[], "rootsDict":[], "coeffs": [], 
                             "genFunc":[], "exprs": [],"solu":[], "upbound":[], "apc2":[],"longest":[]})

        elim_og_data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcess": [], "graphSystems": [],"gamma": [], "discrim":[], "realnroots":[], "rootsDict":[], "coeffs": [], 
                             "genFunc":[], "exprs": [],"solu":[], "upbound":[], "apc2":[],"longest":[]})

        rgf_data = pd.DataFrame({"file_name": [], "graph_name": [], "fcapc": [],"fcapc_time": [],"exception": [], "exception_type": [],
                             "graphProcess": [], "graphSystems": [], "gamma": [], "discrim":[], "realnroots":[], "rootsDict":[], 
                             "genFunc":[], "getrgf": [], "apc2":[],"longest":[]})

        with open('/app/code/experiments/optimization/files.txt') as funcs:
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

                # from metrics folder with no time breakdown
                self.apc_computer = path_complexity.PathComplexity(log)
                self.fcapc_computer = fcn_call_path_complexity.FunctionCallPathComplexity(log)
                self.rapc_computer = recursive_path_complexity.RecursivePathComplexity(log)

                # from optimize folder with time breakdown
                self.elim_fcapc_computer = fc_path_complexity_eliminate.FunctionCallPathComplexity(log)
                self.elim_og_fcapc_computer = fc_path_complexity_elim_og.FunctionCallPathComplexity(log)
                self.rgf_fcapc_computer = fc_path_complexity_getrgf.FunctionCallPathComplexity(log)

                # self.cyclo_computer = cyclomatic_complexity.CyclomaticComplexity(log)
                # self.npath_computer = npath_complexity.NPathComplexity(log)

                apc: Union[str, PathComplexityRes] = "na"
                rapc: Union[str, PathComplexityRes] = "na"
                fcapc: Union[str, PathComplexityRes] = "na"
                efcapc: Union[str, PathComplexityRes] = {"efcapc":"na"}
                eofcapc: Union[str, PathComplexityRes] = {"eofcapc":"na"}
                rgfcapc: Union[str, PathComplexityRes] = {"rgfcapc":"na"}
                # npath: Union[str, int] = "na"
                # cyclo: Union[str, int] = "na"

                exception_type = "na"
                apc_time = 0.0
                rapc_time = 0.0
                fcapc_time = 0.0
                efcapc_time = 0.0
                eofcapc_time = 0.0
                rgfcapc_time = 0.0
                # nonZeroIndex = 0.0
                # fakenonZeroIndex = 0.0

                # running the three metrics in metrics folder
                print("=========================runing regular path complexity for 100 seconds==========================")
                start_time = time.time()
                try:
                    with Timeout(100):
                        apc = self.apc_computer.evaluate(graph)
                        runtime = time.time() - start_time
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                print("====================running recursive function path complexity for 100 seconds==========================")
                start_time = time.time()
                try:
                    with Timeout(100):
                        rapc = self.rapc_computer.evaluate(graph)
                        rapc_time = time.time() - start_time
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                print("=====================running old fcn_call_path_complexity for 200 seconds=========================")
                start_time = time.time()
                try:
                    with Timeout(200):   
                        fcapc = self.fcapc_computer.evaluate(graph, graphs)
                        fcapc_time = time.time() - start_time
                except Exception as exc:
                    print(f"Exception: {exc}")
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"
                
                # running the three metrics in optimization folder (with time breakdown)
                print("=========================runing elim fcn_call_path_complexity for 100 seconds==========================")
                start_time = time.time()
                try:
                    with Timeout(100):
                        efcapc = self.elim_fcapc_computer.evaluate(graph, graphs)
                        efcapc_time = time.time() - start_time
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(exc, TimeoutError) else "Other"

                print("======================running elim_og fcn_call_path_complexity for 4000 seconds=======================")
                start_time = time.time()
                try:
                    with Timeout(4000):
                        eofcapc = self.elim_og_fcapc_computer.evaluate(graph, graphs)
                        eofcapc_time = time.time() - start_time
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"
    
                print("======================running getrgf fcn_call_path_complexity for 4000 seconds=======================")
                start_time = time.time()
                try:
                    with Timeout(4000):
                        rgfcapc = self.rgf_fcapc_computer.evaluate(graph, graphs)
                        rgfcapc_time = time.time() - start_time
                except Exception as exc:
                    exception_type = "Timeout" if isinstance(
                        exc, TimeoutError) else "Other"


                # other path complexities (not asymptotic path complexity); not in use

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

                # data table for fc_path_complexity_eliminate
                print(efcapc)
                new_row = {"file_name": file, "graph_name": graph.name, "fcapc": efcapc["nfcapc"][0],
                           "gamma": efcapc["gammaTime"], "graphProcess": efcapc["graphProcessTime"], "graphSystems":efcapc["graphSystemsTime"],
                           "discrim": efcapc["discrimTime"], "realnroots": efcapc["realnrootsTime"], "rootsDict":efcapc["rootsDictTime"], "genFunc":efcapc["genFuncTime"],
                           "coeffs": efcapc["coeffsTime"], "exprs": efcapc["exprsTime"], "solu":efcapc["soluTime"], 
                           "upbound":efcapc["UpboundTime"], "apcTime2": efcapc["apcTime2"], "clean": efcapc["cleanTime"],
                           "fcapc_time": efcapc_time, "exception_type": exception_type}

                elim_data = elim_data.append(new_row, ignore_index=True)
                elim_data = elim_data[["graph_name", "fcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc", "rootsDict",
                "coeffs", "exprs", "solu", "upbound", "apcTime2", "clean"]]
                print()
                print("PRINTING FC_PATH_COMPLEXITY_ELIMINATE TIME BREAKDOWN")
                print(elim_data[["graph_name", "fcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc", "rootsDict",
                "coeffs", "exprs", "solu", "upbound", "apcTime2", "clean"]])

                # data table for fc_path_complexity_elim_og
                new_row = {"file_name": file, "graph_name": graph.name, "fcapc": eofcapc["apc"],
                           "gamma": eofcapc["gammaTime"], "graphProcess": eofcapc["graphProcessTime"], "graphSystems": eofcapc["graphSystemsTime"],
                           "discrim": eofcapc["discrimTime"], "realnroots": eofcapc["realnrootsTime"], "genFunc": eofcapc["genFuncTime"],
                           "coeffs": eofcapc["coeffsTime"], "exprs": eofcapc["exprsTime"], "solu": eofcapc["soluTime"], 
                           "upbound": eofcapc["UpboundTime"], "apcTime2": eofcapc["apcTime2"], "clean": eofcapc["cleanTime"],
                           "fcapc_time": eofcapc_time, "exception_type": exception_type}
                elim_og_data = elim_og_data.append(new_row, ignore_index=True)
                elim_og_data = elim_og_data[["graph_name", "fcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc",
                "coeffs", "exprs", "solu", "upbound", "apcTime2", "clean"]]
                print()
                print("PRINTING FC_PATH_COMPLEXITY_ELIM_OG TIME BREAKDOWN")
                print(elim_og_data[["graph_name", "fcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc",
                "coeffs", "exprs", "solu", "upbound", "apcTime2", "clean"]])


                # data table for fc_path_complexity_getrgf
                new_row = {"file_name": file, "graph_name": graph.name, "rgfcapc": rgfcapc["rfcapc"],
                           "gamma": rgfcapc["gammaTime"], "graphProcess": rgfcapc["graphProcessTime"], "graphSystems": rgfcapc["graphSystemsTime"],
                           "discrim": rgfcapc["discrimTime"], "realnroots": rgfcapc["realnrootsTime"], "rootsDict":efcapc["rootsDictTime"], "genFunc": rgfcapc["genFuncTime"],
                           "getrgf": rgfcapc["getrgfTime"], "apcTime2": rgfcapc["apcTime2"], "clean":rgfcapc["cleanTime"],
                           "fcapc_time": rgfcapc_time, "exception_type": exception_type}
                rgf_data = rgf_data.append(new_row, ignore_index = True)
                rgf_data = rgf_data[["graph_name", "rgfcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc", "rootsDict",
                "getrgf", "apcTime2", "clean"]]
                print()
                print("PRINTING FC_PATH_COMPLEXITY_GETRGF TIME BREAKDOWN")
                print(rgf_data[["graph_name", "rgfcapc","fcapc_time", "graphProcess", "graphSystems","gamma", "discrim", "realnroots", "genFunc", "rootsDict",
                "getrgf", "apcTime2", "clean"]])

                # data table for all metrics and overall runtimes
                new_row = {"file_name": file, "graph_name": graph.name, 
                           "apc": apc[0], "rapc": rapc[0], "fcapc": fcapc[0],
                           "apc_time": apc_time, "rapc_time": rapc_time, "fcapc_time": fcapc_time,
                           "efcapc": efcapc["nfcapc"], "eofcapc": eofcapc["apc"], "rgfcapc": rgfcapc["rfcapc"],
                           "efcapc_time": efcapc_time, "eofcapc_time": eofcapc_time, "rgfcapc_time": rgfcapc_time,
                           "exception_type": exception_type}
                data = data.append(new_row, ignore_index=True)
                # only keep columns graph_name, metrics and runtimes
                print()
                print("PRINTING FINAL TABLE")
                data = data[["graph_name", "apc","rapc", "fcapc", "efcapc", "eofcapc", "rgfcapc", 
                             "apc_time","rapc_time", "fcapc_time", "efcapc_time", "eofcapc_time", "rgfcapc_time"]]

                # format rapc column decimals to have at most 3 decimal places, e.g. 0.33333333n -> 0.333n
                # data['rapc'] = data['rapc'].apply(lambda x: round_tuple_of_exprs(x, 3))
                print(data[["graph_name", "apc","rapc", "fcapc", "efcapc", "eofcapc", "rgfcapc", 
                             "apc_time","rapc_time", "fcapc_time", "efcapc_time", "eofcapc_time","rgfcapc_time"]])


                # create directory if it doesn't exist
                # if not os.path.exists("/app/code/experiments/optimization/data"):
                #     os.makedirs("/app/code/experiments/optimization/data")
                # data.to_csv("/app/code/experiments/optimization/data/finalTestData.csv")

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
