"""Script for running Klee on a series of functions and saving data."""
import subprocess
import time
import re
from subprocess import PIPE
from typing import List, Optional, Tuple, Dict, Union
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




def klee_with_preferences_general(klee_command):
    """Run and Klee with specified parameters and return several statistics."""
    timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "


    cmd = f"time {klee_command}"
    start_time = time.time()
    # print(timeconfig+cmd)
    res = subprocess.run(timeconfig + cmd, shell=True, check=False,
                         executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
    final_time = time.time() - start_time
    output = res.stderr
    parsed = parse_klee(output.decode())
    return (*parsed, final_time)


def klee_compare_general(filepath, name, xaxis, xlabel, klee_function, klee_path, remove):
    results_dict = {}
    for i in xaxis:
        output_file = f"{filepath}klee_{name}_{xlabel}={i}"
        output_file = output_file.replace(" ", "_")
        klee_command = klee_function(output_file, i)
        results = klee_with_preferences_general(klee_command)
        klee_stats_params = "--table-format=simple --print-all"
        stats = subprocess.run(f"{klee_path}-stats {klee_stats_params} {output_file}", shell=True, stdout=PIPE, stderr=PIPE, check=True)

        if remove:
            subprocess.run(f"rm -rf {output_file}", shell=True, check=False)
        else:
            subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done", shell=True, check=True)
        stats_decoded = stats.stdout.decode().split("\n")
        headers = stats_decoded[0].split()[1:]
        values = map(float, stats_decoded[2].split()[1:])
        stats_dict = dict(zip(headers, values))
        stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _, \
                    stats_dict["RealTime"], stats_dict["UserTime"], stats_dict["SysTime"], \
                    stats_dict["PythonTime"] = results
        results_dict[(name, i)] = stats_dict

    return results_dict


def create_pandas_general(results, name, xaxis, xlabel, fields) -> pd.DataFrame:
    """Create a pandas dataframe from the results of a Klee experiment."""
    index = [f'{xlabel}={i}' for i in xaxis]
    data = [[results[(name, x)][field] for field in fields]
            for x in xaxis]
    return pd.DataFrame(data, index=index, columns=fields)


def generate_files(src_filepath, filepath, func_name, optimized):
    filename = f"{src_filepath}{func_name}.c"
    output = KleeUtils(Log()).show_func_defs(filename, optimized=optimized)
    names = []
    for i in output:
        opt_str = optimized*"optimized"
        new_name = f"{filepath}{func_name}_{i}_{opt_str}.c"
        bcname = f"{filepath}{func_name}_{i}_{opt_str}.bc"
        with open(new_name, "w+") as file:
            file.write(output[i])
        cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        names.append(f"{func_name}_{i}_{opt_str}")
    return names



def run_klee_general(name, filepath, klee_functions, labels, xaxis, xlabel, fields, klee_path, remove):
    results_list = []
    for klee_function, label in zip(klee_functions, labels):
        temp_name = name+label
        results = klee_compare_general(filepath, temp_name, xaxis, xlabel, klee_function, klee_path, remove)
        results_frame = create_pandas_general(results, temp_name, xaxis, xlabel, fields)
        results_frame.to_csv(filepath+temp_name)
        results_list.append(results)

    graph_stat_general(results_list, name, xaxis, xlabel, labels, filepath, fields)

def graph_stat_general(results, name, xaxis, xlabel, labels, filepath, fields):
    for field in fields:
        fig1, ax1 = plt.subplots()
        for label, result_set in zip(labels, results):
            stats = [result_set[(name+label, i)][field] for i in xaxis]
            newxis = [float(i) for i in xaxis]
            ax1.plot(newxis, stats, label=label)
        ax1.set(xlabel=xlabel, ylabel=field, title=name)
        ax1.legend()
        ax1.grid()
        fig1.savefig(f"{filepath}{name}_{field}.png".replace("%", "percent"))
        plt.close(fig1)


def generate_klee_function(klee_path, klee_params_lambda, filepath, klee_file_name):
    combined_filepath = filepath+klee_file_name+".bc"

    return lambda output, var: f"{klee_path} {klee_params_lambda(output, var, combined_filepath)}"


def prepare(klee_path, src_filepath, filepath, file_generation_function, functions, klee_params_lambda, xlabel, labels, xaxis, fields, remove):
    subprocess.run(f"mkdir {filepath}", shell=True, check=False)
    name_tuples = []
    for func in functions:
        name_tuples += file_generation_function(src_filepath, filepath, func)
    for name_tuple in name_tuples:
        klee_functions = [generate_klee_function(klee_path, klee_params_lambda, filepath, name) for name in name_tuple]
        run_klee_general(name_tuple[0], filepath, klee_functions, labels, xaxis, xlabel, fields, klee_path, remove)

def main() -> None:

    klee_path = "/app/build/bin/klee" # location of the klee command
    src_filepath = "/app/code/tests/cFiles/benchmark/kleeversions/" # location of source files to run klee on, end with a slash
    filepath = "/app/code/tests/cFiles/benchmark/kleeversions/kleetest/" # directory to create (if it doesn't exist) and put all results/created files in
                                                                        # both filepaths needs to end with a slash
    # src_filepath = "/app/code/tests/cFiles/fse_2020_benchmark/"
    # filepath =   "/app/code/tests/cFiles/fse_2020_benchmark/kleetest/"
    klee_params_lambda = lambda output, var, filepath: f" --output-dir={output} --max-depth={var} {filepath}"
    # f" --output-dir={output} --max-depth={var} {filepath}"
    # --dump-states-on-halt=false --max-time=5min
    # lambda function to generate klee commands
    # should take in an outpute filepath, a number to vary, and an input filepath
    # shouldn't actually contain the call to klee

    xlabel = "max depth" # label for the x-axis (parameter that is being varied)
    file_generation_function = lambda src_filepath, file_path, file_name: list(zip(generate_files(src_filepath, file_path, file_name, False)))
    # should be a callable object that takes in a source folder, output folder, and file name
    # returns a tuple of names for files, if each was compiled differently (ie optimized vs normal) and also compiles/generates the necessary files for klee

    # functions = ['test-01', 'test-02', 'test-03', 'test-04', 'test-05', 'test-06', 'test-07', 'test-08', 'test-09', 'test-10', 'test-11',
    # 'test-12', 'test-20-un-inlined', 'test-21-un-inlined', 'test-22-un-inlined', 'test-23-un-inlined', 'test-24-un-inlined', 'test-25-un-inlined',
    # 'test-30-un-inlined', 'test-31-un-inlined', 'test-32-un-inlined', 'test-33-un-inlined', 'test-34-un-inlined', 'test-35-un-inlined',
    # 'test-36-un-inlined', 'test-37-un-inlined', 'test-38-un-inlined', 'test-39-un-inlined', 'test-40-un-inlined'] # all the functions to run klee experiments on
    functions = ['02_fib_no_helper', '04_mincoins_no_helper', '05_nCr_no_helper', '07_bubblesort_no_helper', '08_selectionsort_no_helper',
    '09_insertionsort_no_helper', '11_deletevowels_no_helper', '12_deleteword_no_helper', '14_sortascending_no_helper', '15_maxarray_no_helper',
    '17_printarmstrongs_no_helper', '18_binarymultiply_no_helper',
    '19_binarytogray_no_helper', '22_edit_dist_no_helper', '23_mergesort_no_helper', '24_longest_common_increasing_subsequence_no_helper']
    # functions = ['08_selectionsort_no_helper', 'selectionsort']
    # functions = ['selectionsort']
    # functions = ['04_mincoins_no_helper']
    # functions = ['06_binarysearch_no_helper']
    labels = ["normal"] # the labels for the different "compilation methods"
    # xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
    #               '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90',
    #               '100'] # all possible values for the input variable
    # xaxis = ['1', '2', '5']
    xaxis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '15']
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime", "PythonTime"] # all klee output fields that we are interested in
    remove = True # whether klee files should be deleted after the important data is collected. Usually set to True
    prepare(klee_path, src_filepath, filepath, file_generation_function, functions, klee_params_lambda, xlabel, labels, xaxis, fields, remove) #run the experiment




if __name__ == "__main__":
    main()
