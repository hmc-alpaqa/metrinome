"""Script for running Klee on a series of functions and saving data."""
import subprocess
from subprocess import PIPE
from time import time
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore

from core.env import Env
from core.log import Log
from klee.klee_utils import (KleeOutputPreferencesInfo, KleeUtils,
                             get_stats_dict, klee_command, parse_klee)

plt.rcParams["figure.figsize"] = (10, 10)


KleeCompareResults = Dict[Tuple[str, str],
                          Dict[str, Optional[Union[float, int]]]]


def klee_with_time(file_name: str, output_name: str, preferences: str,
                   max_time: str) -> KleeOutputPreferencesInfo:
    """Run and Klee with specified parameters and return several statistics."""
    with open(file_name, "rb+"):
        timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "

        cmd_params = f"-output-dir={output_name} --max-time={max_time}min"
        cmd = f"time {Env.KLEE_PATH} {preferences} {cmd_params} {file_name}"
        start_time = time()
        res = subprocess.run(timeconfig + cmd, shell=True, check=False,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        final_time = time() - start_time
        return (*parse_klee(res.stderr.decode()), final_time)


def klee_compare_time(file_name: str, preferences: List[str], max_times: List[str], function: str,
                      remove: bool = True) -> KleeCompareResults:
    """
    Run Klee on a certain function.

    Run Klee on the function with a variety of depths and preferences,
    and return the results as a dictionary of dictionaries.
    """
    results_dict = {}
    for preference in preferences:
        for max_time in max_times:
            algs_path = "/app/code/tests/cFiles/fse_2020_benchmark/klee"
            output_file = f"{algs_path}_{preference}_{max_time}_{function}_output"
            output_file = output_file.replace(" ", "_")
            results = klee_with_time(file_name, output_file, preference, max_time)
            stats_params = "--table-format=simple --print-all"
            stats = subprocess.run(f"{Env.KLEE_PATH}-stats {stats_params} {output_file}",
                                   shell=True, stdout=PIPE, stderr=PIPE, check=True)
            if remove:
                subprocess.run(f"rm -rf {output_file}", shell=True, check=False)
            else:
                subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done",
                               shell=True, check=True)
            stats_decoded = stats.stdout.decode().split("\n")
            results_dict[(preference, max_time)] = get_stats_dict(stats_decoded, results)

    return results_dict


def graph_stat_time(func: str, preference: str, max_times: List[str], results: KleeCompareResults,
                    field: str) -> None:
    """Create and save a graph for a certain statistic on a Klee experiment."""
    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/graphs_time/",
                   shell=True, check=False)
    fig1, ax1 = plt.subplots()
    depths = [float(i) for i in max_times]
    stats = [results[(preference, i)][field] for i in max_times]
    ax1.plot(depths, stats, label=func)
    ax1.set(xlabel='time', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()

    algs_path = "/app/code/tests/cFiles/fse_2020_benchmark"
    fig1.savefig(f"{algs_path}/graphs_time/{field}_{func}.png".replace("%", "percent"))
    plt.close(fig1)


def create_pandas_time(results: KleeCompareResults, preference: str,
                       max_times: List[str], fields: List[str]) -> pd.DataFrame:
    """Create a pandas dataframe from the results of a Klee experiment."""
    index = [f'max time {i}' for i in max_times]
    data = [[results[(preference, max_time)][field] for field in fields]
            for max_time in max_times]
    return pd.DataFrame(data, index=index, columns=fields)


def run_klee_time(func: str, array_size: int, max_times: List[str], preferences: List[str],
                  fields: List[str]) -> None:
    """Run the KLEE experiment for a single function."""
    filename = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}.c"
    output = KleeUtils(Log()).show_func_defs(filename, size=array_size)

    for i in output:
        func_actual = func + f"_{i}"
        new_name = f"/app/code/tests/cFiles/fse_2020_benchmark/{func_actual}.c"
        bcname = f"/app/code/tests/cFiles/fse_2020_benchmark/{func_actual}.bc"
        with open(new_name, "w+") as file:
            file.write(output[i])
        subprocess.run(klee_command(bcname, new_name), shell=True, capture_output=True, check=True)
        results = klee_compare_time(bcname, preferences, max_times, func_actual)
        results_frame = create_pandas_time(results, preferences[0], max_times, fields)
        filename = f'/app/code/tests/cFiles/fse_2020_benchmark/frames_time/{func_actual}.csv'
        results_frame.to_csv(filename)
        for field in fields:
            graph_stat_time(func_actual, preferences[0], max_times, results, field)


def main() -> None:
    """
    Run a Klee experiment.

    For each function, runs Klee once with each maximum depth,
    saves the data as a csv, and creates a graph for each field.
    """
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime", "PythonTime"]
    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/frames_time/",
                   shell=True, check=False)
    run_klee_time("32_newtons_method", array_size=100,
                  max_times=list(map(str, range(1, 16))),
                  preferences=["--dump-states-on-halt=false"], fields=fields)


if __name__ == "__main__":
    main()
