"""."""
# pylint: skip-file
import subprocess
import time
import re
from subprocess import PIPE
import matplotlib.pyplot as plt  # type: ignore
from log import Log
from klee_utils import KleeUtils
import numpy as np
from scipy.optimize import curve_fit
from numpy.linalg import lstsq
import pandas as pd
plt.rcParams["figure.figsize"] = (10, 10)

def poly(input, coef, deg):
    return [sum([k*(i**j) for j,k in zip(list(range(deg+1))[::-1], coef)]) for i in input]

def exp_function(x, a, b, c):
    return a * np.exp(-b * x) + c

ramp = lambda u: np.maximum( u, 0 )
step = lambda u: ( u > 0 ).astype(float)

def SegmentedLinearReg( X, Y, breakpoints ):
    nIterationMax = 50

    breakpoints = np.sort( np.array(breakpoints) )

    dt = np.min( np.diff(X) )
    ones = np.ones_like(X)

    for i in range( nIterationMax ):
        # Linear regression:  solve A*p = Y
        Rk = [ramp( X - xk ) for xk in breakpoints ]
        Sk = [step( X - xk ) for xk in breakpoints ]
        A = np.array([ ones, X ] + Rk + Sk )
        print(A)
        p =  lstsq(A.transpose(), Y, rcond=None)[0]

        # Parameters identification:
        a, b = p[0:2]
        ck = p[ 2:2+len(breakpoints) ]
        dk = p[ 2+len(breakpoints): ]

        # Estimation of the next break-points:
        newBreakpoints = breakpoints - dk/ck

        # Stop condition
        if np.max(np.abs(newBreakpoints - breakpoints)) < dt/5:
            break

        breakpoints = newBreakpoints
    else:
        print( 'maximum iteration reached' )

    # Compute the final segmented fit:
    Xsolution = np.insert( np.append( breakpoints, max(X) ), 0, min(X) )
    ones =  np.ones_like(Xsolution)
    Rk = [ c*ramp( Xsolution - x0 ) for x0, c in zip(breakpoints, ck) ]

    Ysolution = a*ones + b*Xsolution + np.sum( Rk, axis=0 )

    return Xsolution, Ysolution

def parse_klee(klee_output):
    """."""
    string_one = "generated tests = "
    string_two = "completed paths = "
    string_three = "total instructions = "
    string_four = "real"

    generated_tests_index    = klee_output.index(string_one) + len(string_one)
    completed_paths_index    = klee_output.index(string_two) + len(string_two)
    total_instructions_index = klee_output.index(string_three) + len(string_three)

    times = klee_output[klee_output.index(string_four):].split()
    real, user, sys = float(times[1][:-1]), float(times[3][:-1]), float(times[5][:-1])

    number_regex = re.compile("[0-9]+")

    tests_match = number_regex.match(klee_output[generated_tests_index:])
    paths_match = number_regex.match(klee_output[completed_paths_index:])
    insts_match = number_regex.match(klee_output[total_instructions_index:])

    if tests_match is not None:
        tests = int(tests_match.group())
    if paths_match is not None:
        paths = int(paths_match.group())
    if insts_match is not None:
        insts = int(insts_match.group())
    return tests, paths, insts, real, user, sys


def klee_with_preferences(file_name, output_name, preferences, max_depth, input_):
    """."""
    with open(file_name, "rb+") as file:
        klee_path = "/app/build/bin/klee"
        timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "

        cmd_params = f"-output-dir={output_name} -max-depth {max_depth}"
        cmd = f"time {klee_path} {preferences} {cmd_params} {file_name} {input_}"
        start_time = time.time()
        res = subprocess.run(timeconfig + cmd, shell=True,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        final_time = time.time() - start_time
        output = res.stderr
        parsed = parse_klee(output.decode())
        return (*parsed, final_time)


def klee_compare(file_name, preferences, depths, inputs, function, remove=True):
    """."""
    klee_path = "/app/build/bin/klee"
    results_dict = {}
    for preference in preferences:
        for depth in depths:
            for input in inputs:
                algs_path = "/app/code/tests/cFiles/simpleAlgs/klee"
                output_file = f"{algs_path}_{preference}_{depth}_{input}_{function}_output"
                output_file = output_file.replace(" ", "_")
                results = klee_with_preferences(file_name, output_file, preference, depth, input)
                stats_params = "--table-format=simple --print-all"
                stats = subprocess.run(f"{klee_path}-stats {stats_params} {output_file}",
                                       shell=True, stdout=PIPE, stderr=PIPE, check=True)
                if remove:
                    subprocess.run(f"rm -rf {output_file}", shell=True)
                else:
                    subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done",
                                   shell=True, check=True)
                stats_decoded = stats.stdout.decode().split("\n")
                headers = stats_decoded[0].split()[1:]
                values = map(lambda x: float(x), stats_decoded[2].split()[1:])
                stats_dict = dict(zip(headers, values))
                stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _, stats_dict["RealTime"], \
                stats_dict["UserTime"], stats_dict["SysTime"], stats_dict["PythonTime"] = results
                results_dict[(preference, depth, input)] = stats_dict

    return results_dict


def graph_stat(func, preference, max_depths, inputs, results, field):
    """."""
    subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphs/", shell=True)
    fig1, ax1 = plt.subplots()
    depths = [float(i) for i in max_depths]
    for input_ in inputs:
        stats = [results[(preference, i, input_)][field] for i in max_depths]
        ax1.plot(depths, stats, label=func)
    ax1.set(xlabel='depth', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()

    algs_path = "/app/code/tests/cFiles/simpleAlgs"
    fig1.savefig(f"{algs_path}/graphs/{field}_{func}.png".replace("%", "percent"))
    plt.close(fig1)

def create_pandas(results, preference, input, max_depths, fields):
    index = [f'max depth {i}' for i in max_depths]
    columns = fields
    data = [[results[(preference, depth, input)][field] for field in fields ] for depth in max_depths]
    return pd.DataFrame(data, index=index, columns=columns)



def main():
    """."""
    preferences = ["--dump-states-on-halt=false --max-time=5min"]
    # max_times = ["1min", "3min"]
    max_depths = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '30', '40', '50', '60', '70', '80', '90', '100']
    fields = ["ICov(%)",'BCov(%)',"CompletedPaths","GeneratedTests", "RealTime", "UserTime", "SysTime", "PythonTime"]
    # inputs = ["--sym-args 0 1 10 --sym-args 0 2 2 --sym-files 1 8 --sym-stdin 8 --sym-stdout"]
    inputs = [""]

    # functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3', '16_binary_search', '12_check_sorted_array',
    # '11_array_max', '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
    # '14_lexicographic_array_compare', '17_edit_dist',
    # "20_bubblesort", "21_insertionsort", "22_selectionsort", "23_mergesort",
    # "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method"]
    # functions = ['04_prime', '05_parity']
    # '01_greatestof3', '13_check_arrays_equal', '22_selectionsort', '02_fib', '14_lexicographic_array_compare', '23_mergesort', '03_sign', '15_check_heap_order', '24_quicksort',
#'04_prime', '16_binary_search', '25_heapsort', '05_parity', '17_edit_dist', '26_quicksort', '06_palindrome', '18_longest_common_subsequence', 
    functions = ['30_euclid_GCD', '10_find_val_in_array', '19_longest_common_increasing_subsequence', '31_sieve_of_eratosthenes', '11_array_max', '20_bubblesort', '32_newtons_method', '12_check_sorted_array', '21_insertionsort']

    subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/frames/", shell=True)
    for func in functions:
        log = Log()
        kleeu = KleeUtils(log)
        filename = f"/app/code/tests/cFiles/simpleAlgs/{func}.c"
        output = kleeu.show_func_defs(filename, size=100)

        for i in output:
            new_name = f"/app/code/tests/cFiles/simpleAlgs/{func}_{i}.c"
            bcname = f"/app/code/tests/cFiles/simpleAlgs/{func}_{i}.bc"
            with open(new_name, "w+") as file:
                file.write(output[i])
            cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                    -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"
            res = subprocess.run(cmd, shell=True, capture_output=True, check=True)
            results = klee_compare(bcname, preferences, max_depths, inputs, f"{func}_{i}")
            results_frame = create_pandas(results, preferences[0], inputs[0], max_depths, fields)
            results_frame.to_csv(f'/app/code/tests/cFiles/simpleAlgs/frames/{func}.csv')
            for field in fields:
                graph_stat(func, preferences[0], max_depths, inputs, results, field)



if __name__ == "__main__":
    main()
