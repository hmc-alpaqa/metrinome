"""Script for running Klee on a series of functions and saving data."""
import subprocess
import time
from subprocess import PIPE
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore

from core.log import Log
from klee.klee_utils import KleeUtils, parse_klee

plt.rcParams["figure.figsize"] = (10, 10)


KleeCompareResults = Dict[Tuple[str, str],
                          Dict[str, Optional[Union[float, int]]]]
KleeOutputInfo = Tuple[Optional[int],
                       Optional[int],
                       Optional[int],
                       float, float, float]
KleeOutputPreferencesInfo = Tuple[Optional[int],
                                  Optional[int],
                                  Optional[int],
                                  float, float, float, float]


def klee_with_time(file_name: str, output_name: str,
                   preferences: str,
                   max_time: str) -> KleeOutputPreferencesInfo:
    """Run and Klee with specified parameters and return several statistics."""
    with open(file_name, "rb+"):
        klee_path = "/app/build/bin/klee"
        timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "

        cmd_params = f"-output-dir={output_name} --max-time={max_time}min"
        cmd = f"time {klee_path} {preferences} {cmd_params} {file_name}"
        start_time = time.time()
        res = subprocess.run(timeconfig + cmd, shell=True, check=False,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        final_time = time.time() - start_time
        output = res.stderr
        parsed = parse_klee(output.decode())
        return (*parsed, final_time)


def get_stats_dict(stats_decoded: List[str],
                   results: KleeOutputPreferencesInfo) -> Dict[str, Optional[Union[float, int]]]:
    """Gather the data from Klee into a stats dictionary."""
    headers = stats_decoded[0].split()[1:]
    values = map(float, stats_decoded[2].split()[1:])
    stats_dict: Dict[str, Optional[Union[float, int]]] = dict(zip(headers, values))
    stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _, \
        stats_dict["RealTime"], stats_dict["UserTime"], stats_dict["SysTime"], \
        stats_dict["PythonTime"] = results

    return stats_dict


# def klee_compare_time(file_name: str, preferences: List[str], depths: List[str],
#                  inputs: List[str], function: str,
#                  remove: bool = True) -> KleeCompareResults:
def klee_compare_time(file_name: str, preferences: List[str],
                      max_times: List[str], function: str,
                      remove: bool = True) -> KleeCompareResults:
    """
    Run Klee on a certain function.

    Run Klee on the function with a variety of depths and preferences,
    and return the results as a dictionary of dictionaries.
    """
    klee_path = "/app/build/bin/klee"
    results_dict = {}
    for preference in preferences:
        for max_time in max_times:
            algs_path = "/app/code/tests/cFiles/fse_2020_benchmark/klee"
            output_file = f"{algs_path}_{preference}_{max_time}_{function}_output"
            output_file = output_file.replace(" ", "_")
            results = klee_with_time(file_name, output_file, preference, max_time)
            stats_params = "--table-format=simple --print-all"
            stats = subprocess.run(f"{klee_path}-stats {stats_params} {output_file}",
                                   shell=True, stdout=PIPE, stderr=PIPE, check=True)
            if remove:
                subprocess.run(f"rm -rf {output_file}", shell=True, check=False)
            else:
                subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done",
                               shell=True, check=True)
            stats_decoded = stats.stdout.decode().split("\n")
            results_dict[(preference, max_time)] = get_stats_dict(stats_decoded, results)

    return results_dict


def graph_stat_time(func: str, preference: str, max_times: List[str],
                    results: KleeCompareResults,
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


# def run_klee_experiment(func: str, array_size: int, max_depths: List[str],
#                         preferences: List[str],
#                         fields: List[str], inputs: List[str]) -> None:
def run_klee_time(func: str, array_size: int,
                  max_times: List[str], preferences: List[str],
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
        cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
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
    max_times = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
    # max_times = ["1","2"]
    preferences = ["--dump-states-on-halt=false"]
    # max_depths = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
    #               '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90',
    #               '100']
    # max_depths = ['1', '2']
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime", "PythonTime"]
    array_size = 100

    # functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3',
    #              '16_binary_search', '12_check_sorted_array', '11_array_max',
    #              '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
    #              '19_longest_common_increasing_subsequence', '14_lexicographic_array_compare',
    #              '17_edit_dist', '20_bubblesort', '21_insertionsort', '22_selectionsort',
    #              '23_mergesort', "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method",
    #              '50_check_sorted_or_reverse', '51_variance', '25_heapsort', '26_quicksort',
    #              '60_array_summary', '61_pos_vel_acc', '62_three_loops_w_break',
    #              '63_three_loops_symbolic_bounds']
    functions = ["32_newtons_method"]

    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/frames_time/",
                   shell=True, check=False)
    for func in functions:
        run_klee_time(func, array_size, max_times, preferences, fields)


if __name__ == "__main__":
    main()
