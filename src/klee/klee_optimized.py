"""Script for running Klee on a series of functions and saving data."""

import subprocess
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt  # type: ignore

from core.log import Log
from klee.klee_utils import KleeUtils, create_pandas, klee_compare

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


# pylint: disable=too-many-locals
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

    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/frames/",
                   shell=True, check=False)
    for func in functions:
        run_klee_experiment(func, array_size, max_depths, preferences, fields, inputs)


if __name__ == "__main__":
    main()
