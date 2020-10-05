"""Various utilities used only for testing and not the main REPL."""
import subprocess
import os
import time
import sys
import glob2
import re
import pandas as pd
from control_flow_graph import ControlFlowGraph
from math import floor
from numpy import mean, std, median  # type: ignore
sys.path.append("/app/code")
from log import Log
from graph import Graph
from utils import Timeout
from typing import List, Any
sys.path.append("/app/code/lang_to_cfg")
from cpp import CPPConvert
sys.path.append("/app/code/metric")
from metric import path_complexity, cyclomatic_complexity, npath_complexity





if __name__ == "__main__":
    # Get all the folders
    # Establish our lists: file_name, dot_name, apc, cyclo, npath, time, exception?
    log = Log()
    data = pd.DataFrame({"file_name": [], "graph_name": [], "apc": [], 
      "cyclo": [], "npath": [], "apc_time": [], "exception": [], "exception_type": []})


    Converter = CPPConvert(log)
    Apc = path_complexity.PathComplexity(log)
    Cyclo = cyclomatic_complexity.CyclomaticComplexity(log)
    Npath = npath_complexity.NPathComplexity(log)
    files = glob2.glob("/app/code/tests/cFiles/fse_2020_benchmark/*.c")
    for file in files:
        print(file)
        graphs = Converter.to_graph(os.path.splitext(file)[0], ".c")
        stitched_graph = ControlFlowGraph.stitch(graphs)
        stitched_graph.name = os.path.splitext(file)[0] + "_stitched"
        graphs[stitched_graph.name] = stitched_graph

        for graph in graphs.values():
            start_time = time.time()
            apc = "na"
            npath = "na"
            cyclo = "na"
            ex = False
            exception_type = "na"
            runtime = 0.0
            try:
                with Timeout(600, ""):
                    apc = Apc.evaluate(graph)
                runtime = time.time() - start_time

            except TimeoutError as exception:
                ex = True 
                exception_type = "Timeout"
            except Exception as v:
                ex = True
                exception_type = "Other"
            if not ex:
                try:
                    with Timeout(200, ""):
                        cyclo = Cyclo.evaluate(graph)
                
                except TimeoutError as exception:
                    ex = True 
                    exception_type = "Timeout"
                except Exception:
                    ex = True
                    exception_type = "Other"
                if not ex:
                    try:
                        with Timeout(200, ""):
                            npath = Npath.evaluate(graph)
            
                    except TimeoutError as exception:
                        ex = True 
                        exception_type = "Timeout"
                    except Exception:
                        ex = True
                        exception_type = "Other"
            new_row = {"file_name": file, "graph_name": graph.name, "apc": apc, 
        "cyclo": cyclo, "npath": npath, "apc_time": runtime, "exception": ex, "exception_type": exception_type}

            data = data.append(new_row, ignore_index = True)
            data.to_csv("/app/code/stitching_data_collection.csv")
    

   





# """Run all CFGs through the converter to create a benchmark."""
# files = (glob2.glob("/app/code/tests/core/separate/*"))

# os.chdir("/app/code/tests/core/separate")
# for file in files: 
#     name = os.path.basename(file)
#     os.chdir(f"/app/code/tests/core/separate/{name}/")
#     f = f".{name}.bc"     
#     subprocess.check_call(["opt", "-dot-cfg", f"{f}"])