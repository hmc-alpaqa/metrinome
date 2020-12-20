"""Script for running Klee on a series of functions and saving data."""
import re
import subprocess
import time
from subprocess import PIPE
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore

from core.log import Log
from klee.klee_utils import KleeUtils

plt.rcParams["figure.figsize"] = (10, 10)


KleeCompareResults = Dict[Tuple[str, str, str],
                          Dict[str, Optional[Union[float, int]]]]
KleeOutputInfo = Tuple[Optional[int],
                       Optional[int],
                       Optional[int],
                       float, float, float]
KleeOutputPreferencesInfo = Tuple[Optional[int],
                                  Optional[int],
                                  Optional[int],
                                  float, float, float, float]


def parse_klee(klee_output: str) -> KleeOutputInfo:
    """Parse output from running Klee."""
    strs_to_match = ["generated tests = ", "completed paths = ", "total instructions = "]
    string_four = "real"
    str_indicies = [klee_output.index(str_to_match) + len(str_to_match)
                    for str_to_match in strs_to_match]

    times = klee_output[klee_output.index(string_four):].split()
    real, user, sys = float(times[1][:-1]), float(times[3][:-1]), float(times[5][:-1])

    number_regex = re.compile("[0-9]+")
    str_matches = [number_regex.match(klee_output[str_idx:]) for str_idx in str_indicies]

    tests, paths, insts = None, None, None
    if str_matches[0] is not None:
        tests = int(str_matches[0].group())
    if str_matches[1] is not None:
        paths = int(str_matches[1].group())
    if str_matches[2] is not None:
        insts = int(str_matches[2].group())

    return tests, paths, insts, real, user, sys


def klee_with_preferences(file_name: str, output_name: str,
                          preferences: str,
                          max_depth: str, input_: str) -> KleeOutputPreferencesInfo:
    """Run and Klee with specified parameters and return several statistics."""
    with open(file_name, "rb+"):
        klee_path = "/app/build/bin/klee"
        timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "

        cmd_params = f"-output-dir={output_name} -max-depth {max_depth}"
        cmd = f"time {klee_path} {preferences} {cmd_params} {file_name} {input_}"
        start_time = time.time()
        res = subprocess.run(timeconfig + cmd, shell=True, check=False,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        final_time = time.time() - start_time
        output = res.stderr
        parsed = parse_klee(output.decode())
        return (*parsed, final_time)


# pylint: disable=too-many-locals
def klee_compare(file_name: str, preferences: List[str], depths: List[str],
                 inputs: List[str], function: str,
                 remove: bool = True) -> KleeCompareResults:
    """
    Run Klee on a certain function.

    Run Klee on the function with a variety of depths and preferences,
    and return the results as a dictionary of dictionaries.
    """
    klee_path = "/app/build/bin/klee"
    results_dict = {}
    for preference in preferences:
        for depth in depths:
            for input_ in inputs:
                algs_path = "/app/code/tests/cFiles/fse_2020_benchmark/klee"
                output_file = f"{algs_path}_{preference}_{depth}_{input_}_{function}_output"
                output_file = output_file.replace(" ", "_")
                results = klee_with_preferences(file_name, output_file, preference, depth, input_)
                stats_params = "--table-format=simple --print-all"
                stats = subprocess.run(f"{klee_path}-stats {stats_params} {output_file}",
                                       shell=True, stdout=PIPE, stderr=PIPE, check=True)
                if remove:
                    subprocess.run(f"rm -rf {output_file}", shell=True, check=False)
                else:
                    subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done",
                                   shell=True, check=True)
                stats_decoded = stats.stdout.decode().split("\n")
                headers = stats_decoded[0].split()[1:]
                values = map(float, stats_decoded[2].split()[1:])
                stats_dict: Dict[str, Optional[Union[float, int]]] = dict(zip(headers, values))
                stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _, \
                    stats_dict["RealTime"], stats_dict["UserTime"], stats_dict["SysTime"], \
                    stats_dict["PythonTime"] = results
                results_dict[(preference, depth, input_)] = stats_dict

    return results_dict


# pylint: disable=too-many-arguments
def graph_stat(func: str, preference: str, max_depths: List[str],
               inputs: List[str], results: KleeCompareResults, results2: KleeCompareResults,
               field: str) -> None:
    """Create and save a graph for a certain statistic on a Klee experiment."""
    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/graphs/",
                   shell=True, check=False)
    fig1, ax1 = plt.subplots()
    depths = [float(i) for i in max_depths]
    for input_ in inputs:
        stats = [results[(preference, i, input_)][field] for i in max_depths]
        ax1.plot(depths, stats, label=func)
        stats2 = [results2[(preference, i, input_)][field] for i in max_depths]
        ax1.plot(depths, stats2, label=func + " optimized")

    ax1.set(xlabel='depth', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()

    algs_path = "/app/code/tests/cFiles/fse_2020_benchmark"
    fig1.savefig(f"{algs_path}/graphs/{field}_{func}.png".replace("%", "percent"))
    plt.close(fig1)


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
    output2 = KleeUtils(Log()).show_func_defs(filename, size=array_size, optimized=True)

    for i, j in zip(output, output2):
        new_name = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{i}.c"
        bcname = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{i}.bc"
        with open(new_name, "w+") as file:
            file.write(output[i])
        cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        results = klee_compare(bcname, preferences, max_depths, inputs, f"{func}_{i}")
        results_frame = create_pandas(results, preferences[0], inputs[0], max_depths, fields)
        results_frame.to_csv(f'/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}_{j}.csv')

        new_name2 = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{j}_optimized.c"
        bcname2 = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{j}_optimized.bc"
        with open(new_name2, "w+") as file:
            file.write(output2[j])
        cmd2 = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                -O0 -Xclang -disable-O0-optnone  -o {bcname2} {new_name2}"
        subprocess.run(cmd2, shell=True, capture_output=True, check=True)
        results2 = klee_compare(bcname2, preferences, max_depths, inputs, f"{func}_{j}_optimized")
        results_frame2 = create_pandas(results2, preferences[0], inputs[0], max_depths, fields)
        filename = f'/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}_{j}_optimized.csv'
        results_frame2.to_csv(filename)
        for field in fields:
            graph_stat(func, preferences[0], max_depths, inputs, results, results2, field)


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
    max_depths = ['1', '2', '3', '4']
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime", "PythonTime"]
    inputs = [""]
    array_size = 100
    functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3',
                 '16_binary_search', '12_check_sorted_array', '11_array_max',
                 '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
                 '19_longest_common_increasing_subsequence', '14_lexicographic_array_compare',
                 '17_edit_dist', '20_bubblesort', '21_insertionsort', '22_selectionsort',
                 '23_mergesort', "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method",
                 '50_check_sorted_or_reverse', '51_variance', '25_heapsort', '26_quicksort',
                 '60_array_summary', '61_pos_vel_acc', '62_three_loops_w_break',
                 '63_three_loops_symbolic_bounds']
    # functions = ['04_prime', '05_parity']
    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/frames/",
                   shell=True, check=False)
    for func in functions:
        run_klee_experiment(func, array_size, max_depths, preferences, fields, inputs)


if __name__ == "__main__":
    main()
