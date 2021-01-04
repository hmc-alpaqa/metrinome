"""Script for running Klee on a series of functions and saving data."""

import subprocess
from subprocess import PIPE
from time import time
from typing import List

import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore

from core.log import Log
from klee.klee_utils import (KleeCompareResults, KleeOutputPreferencesInfo,
                             KleeUtils, get_functions_list, graph_stat,
                             klee_compare, parse_klee)

plt.rcParams["figure.figsize"] = (10, 10)


def klee_with_preferences(file_name: str, output_name: str,
                          preferences: str,
                          max_depth: str, input_: str) -> KleeOutputPreferencesInfo:
    """Run and Klee with specified parameters and return several statistics."""
    with open(file_name, "rb+"):
        klee_path = "/app/build/bin/klee"
        timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "

        cmd_params = f"-output-dir={output_name} -max-depth {max_depth}"
        cmd = f"time {klee_path} {preferences} {cmd_params} {file_name} {input_}"
        start_time = time()
        res = subprocess.run(timeconfig + cmd, shell=True, check=False,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        final_time = time() - start_time
        output = res.stderr
        parsed = parse_klee(output.decode())
        return (*parsed, final_time)


def create_pandas(results: KleeCompareResults, preference: str, input_: str,
                  max_depths: List[str], fields: List[str]) -> pd.DataFrame:
    """Create a pandas dataframe from the results of a Klee experiment."""
    index = [f'max depth {i}' for i in max_depths]
    data = [[results[(preference, depth, input_)][field] for field in fields]
            for depth in max_depths]
    return pd.DataFrame(data, index=index, columns=fields)


def run_klee_experiment(func: str, array_size: int, max_depths: List[str],
                        preferences: List[str],
                        fields: List[str], inputs: List[str]) -> None:
    """Run the KLEE experiment for a single function."""
    filename = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}.c"
    output = KleeUtils(Log()).show_func_defs(filename, size=array_size)

    for i in output:
        new_name = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{i}.c"
        bcname = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{i}.bc"
        with open(new_name, "w+") as file:
            file.write(output[i])
        cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        results = klee_compare(bcname, preferences, max_depths, inputs, f"{func}_{i}")
        results_frame = create_pandas(results, preferences[0], inputs[0], max_depths, fields)
        results_frame.to_csv(f'/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}.csv')
        for field in fields:
            graph_stat(func, preferences[0], max_depths, inputs, results, None, field)


def main() -> None:
    """
    Run a Klee experiment.

    For each function, runs Klee once with each maximum depth,
    saves the data as a csv, and creates a graph for each field.
    """
    preferences = ["--dump-states-on-halt=false --max-time=5min"]
    max_depths = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                  '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90',
                  '100']
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime", "PythonTime"]
    inputs = [""]
    array_size = 100
    functions = get_functions_list()

    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/frames/",
                   shell=True, check=False)
    for func in functions:
        run_klee_experiment(func, array_size, max_depths, preferences, fields, inputs)


if __name__ == "__main__":
    main()
