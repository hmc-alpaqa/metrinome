"""."""
# pylint: skip-file
import subprocess
import re
from subprocess import PIPE
import matplotlib.pyplot as plt  # type: ignore
from log import Log
from klee_utils import KleeUtils
plt.rcParams["figure.figsize"] = (10, 10)


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
    real, user, sys = times[1], times[3], times[5]

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
        res = subprocess.run(timeconfig + cmd, shell=True,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        output = res.stderr
        parsed = parse_klee(output.decode())
        return parsed


def klee_compare(file_name, preferences, depths, inputs, function):
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
                subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done",
                               shell=True, check=True)
                stats_decoded = stats.stdout.decode().split("\n")
                headers = stats_decoded[0].split()[1:]
                values = map(lambda x: float(x), stats_decoded[2].split()[1:])
                stats_dict = dict(zip(headers, values))
                stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _, \
                    stats_dict["RealTime"], stats_dict["UserTime"], stats_dict["SysTime"] = results
                results_dict[(preference, depth, input)] = stats_dict

    return results_dict


def graph_stat(func, preference, max_depths, inputs, results, field):
    """."""
    subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphs/", shell=True)
    fig1, ax1 = plt.subplots()
    depths = [float(i) for i in max_depths]
    for input_ in inputs:
        stats = [results[(preference, i, input_)][field] for i in max_depths]
        ax1.plot(depths, stats, label=input_)
    ax1.set(xlabel='depth', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()

    algs_path = "/app/code/tests/cFiles/simpleAlgs"
    fig1.savefig(f"{algs_path}/graphs/{field}_{func}.png".replace("%", "percent"))
    plt.close(fig1)


def main():
    """."""
    preferences = [""]
    # max_times = ["1min", "3min"]
    max_depths = ["1", "2", "5", "10", "20"]

    # inputs = ["--sym-args 0 1 10 --sym-args 0 2 2 --sym-files 1 8 --sym-stdin 8 --sym-stdout"]
    inputs = [""]

    functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3',
                 '16_binary_search', '12_check_sorted_array', '11_array_max',
                 '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
                 '14_lexicographic_array_compare', '17_edit_dist']
    fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
              "SysTime"]

    for func in functions:
        log = Log()
        kleeu = KleeUtils(log)
        filename = f"/app/code/tests/cFiles/simpleAlgs/{func}.c"
        output = kleeu.show_func_defs(filename)

    for i in output:
        new_name = f"/app/code/tests/cFiles/simpleAlgs/{func}_{i}.c"
        bcname = f"/app/code/tests/cFiles/simpleAlgs/{func}_{i}.bc"
        with open(new_name, "w+") as file:
            file.write(output[i])
        cmd = f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
                -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"
        res = subprocess.run(cmd, shell=True, capture_output=True, check=True)
        results = klee_compare(bcname, preferences, max_depths, inputs, f"{func}_{i}")
        for field in fields:
            graph_stat(func, preferences[0], max_depths, inputs, results, field)


if __name__ == "__main__":
    main()
