"""Handles work with klee, which does symbollic execution and test generation of C code."""

import re
import subprocess
import uuid
from collections import defaultdict
from subprocess import PIPE
from time import time
from typing import Optional, Union

import pandas as pd  # type: ignore
from pycparser import c_ast, c_generator, parse_file  # type: ignore

from core.env import Env
from core.log import Log

KleeOutputInfo = tuple[Optional[int], Optional[int], Optional[int],
                       float, float, float]
KleeCompareResults = dict[tuple[str, str, str],
                          dict[str, Optional[Union[float, int]]]]
KleeOutputPreferencesInfo = tuple[Optional[int], Optional[int], Optional[int],
                                  float, float, float, float]


def klee_with_opts(file_name: str, output_name: str, preferences: str, max_val: str,
                   max_time: bool, input_: str = "") -> KleeOutputPreferencesInfo:
    """Run and Klee with specified parameters and return several statistics."""
    with open(file_name, "rb+"):
        timeconfig = r"export TIMEFMT=$'real\t%E\nuser\t%U\nsys\t%S'; "

        if max_time:
            cmd_params = f"-output-dir={output_name} --max-time={max_val}min"
            cmd = f"time {Env.KLEE_PATH} {preferences} {cmd_params} {file_name}"
        else:
            cmd_params = f"-output-dir={output_name} -max-depth {max_val}"
            cmd = f"time {Env.KLEE_PATH} {preferences} {cmd_params} {file_name} {input_}"

        start_time = time()
        res = subprocess.run(timeconfig + cmd, shell=True, check=False,
                             executable="/usr/bin/zsh", stdout=PIPE, stderr=PIPE)
        final_time = time() - start_time
        return (*parse_klee(res.stderr.decode()), final_time)


def parse_klee(klee_output: str) -> KleeOutputInfo:
    """Parse output from running Klee."""
    strs_to_match = ["generated tests = ", "completed paths = ", "total instructions = "]
    str_indicies = [klee_output.index(str_to_match) + len(str_to_match)
                    for str_to_match in strs_to_match]

    times = klee_output[klee_output.index("real"):].split()
    real, user, sys = float(times[1][:-1]), float(times[3][:-1]), float(times[5][:-1])

    number_regex = re.compile("[0-9]+")
    str_matches = [number_regex.match(klee_output[str_idx:]) for str_idx in str_indicies]

    tests = int(str_matches[0].group()) if str_matches[0] is not None else None
    paths = int(str_matches[1].group()) if str_matches[1] is not None else None
    insts = int(str_matches[2].group()) if str_matches[2] is not None else None

    return tests, paths, insts, real, user, sys


def klee_cmd(bcname: str, new_name: str) -> str:
    """Get the KLEE command as a string."""
    return f"clang-6.0 -I /app/klee/include -emit-llvm -c -g\
             -O0 -Xclang -disable-O0-optnone  -o {bcname} {new_name}"


def get_functions_list() -> list[str]:
    """Get a list of all file names used for testing klee."""
    return ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3',
            '16_binary_search', '12_check_sorted_array', '11_array_max', '10_find_val_in_array',
            '13_check_arrays_equal', '15_check_heap_order',
            '19_longest_common_increasing_subsequence', '14_lexicographic_array_compare',
            '17_edit_dist', '20_bubblesort', '21_insertionsort', '22_selectionsort',
            '23_mergesort', "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method",
            '50_check_sorted_or_reverse', '51_variance', '25_heapsort', '26_quicksort',
            '60_array_summary', '61_pos_vel_acc', '62_three_loops_w_break',
            '63_three_loops_symbolic_bounds']


def create_pandas(results: KleeCompareResults, preference: str, input_: str,
                  max_depths: list[str], fields: list[str]) -> pd.DataFrame:
    """Create a pandas dataframe from the results of a Klee experiment."""
    index = [f'max depth {i}' for i in max_depths]
    data = [[results[(preference, depth, input_)][field] for field in fields]
            for depth in max_depths]
    return pd.DataFrame(data, index=index, columns=fields)


def get_stats_dict(stats_decoded: list[str],
                   results: KleeOutputPreferencesInfo) -> dict[str, Optional[Union[float, int]]]:
    """Gather the data from Klee into a stats dictionary."""
    headers = stats_decoded[0].split()[1:]
    values = map(float, stats_decoded[2].split()[1:])
    stats_dict: dict[str, Optional[Union[float, int]]] = dict(zip(headers, values))
    stats_dict["GeneratedTests"], stats_dict["CompletedPaths"], _, \
        stats_dict["RealTime"], stats_dict["UserTime"], stats_dict["SysTime"], \
        stats_dict["PythonTime"] = results

    return stats_dict


class FuncVisitor(c_ast.NodeVisitor):
    """
    Look at a single C function an gather the information for Klee.

    The FuncVisitor visits each function once and then visits all of the variable
    definitions in the function definition in order to get their names and types.
    """

    def __init__(self, logger: Log) -> None:
        """Create a new instance of FuncVisitor."""
        self._logger = logger
        self._generator = c_generator.CGenerator()
        self.vars: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
        self.types: defaultdict[str, str] = defaultdict(str)
        super().__init__()

    def define_var(self, name: str, declaration: str, varname: str) -> None:
        """Look at a single variable declaration in the C code."""
        self.vars[name].append((f"{declaration};\n", varname))

    # pylint: disable=C0103
    # disable invalid-name as this name is required by the library.
    def visit_FuncDef(self, node: c_ast.Node) -> None:
        """
        Determine all of the arguments to functions.

        This function is called once for each function in the C source code.
        It determines all of the argument types needed to call the function.
        """
        # Node is a pycparser.c_ast.funcdef
        args = node.decl.type.args  # type ParamList.
        return_type = node.decl.type.type.type.names[0]
        self._logger.i_msg(f"Looking at {node.decl.name}()")
        self.types[node.decl.name] = return_type
        if args is not None:
            params = args.params  # List of TypeDecl.
            for i, param in enumerate(params):
                self._logger.d_msg(f"\tParameter {i}: Name: {param.name}")
                self.define_var(node.decl.name, self._generator.visit(param), param.name)
        else:
            self._logger.d_msg(f"\t{node.decl.name} has no parameters.")


class KleeUtils:
    """
    KleeUtils is used to make working with KLEE much easier in the REPL.

    This is used to parse C code and generate new Klee-compatible
    source code in order to make static analysis much easier.
    """

    def __init__(self, logger: Log) -> None:
        """Create a new instance of KleeUtils."""
        self._logger = logger

    def show_func_defs(self, filename: str, size: int = 10,
                       optimized: bool = False) -> dict[str, str]:
        """
        Generate the set of klee-compatible files.

        Create a new set of files based on an existing file that are formatted properly
        to work with klee.
        """
        self._logger.d_msg(f"Going to parse file {filename}")
        if optimized:
            cppargs = ['-O3', '-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include']
        else:
            cppargs = ['-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include']
        ast = parse_file(filename, use_cpp=True, cpp_path='gcc', cpp_args=cppargs)
        self._logger.d_msg("Going to visit functions.")
        func_visitor = FuncVisitor(self._logger)
        func_visitor.visit(ast)

        uuids: set[uuid.UUID] = set()
        klee_formatted_files = dict()
        for func_name in func_visitor.vars.keys():
            variables = [list(v) for v in func_visitor.vars[func_name]]
            var_names = []

            file_str = "#include <klee/klee.h>\n"
            file_str += f"#include <{filename}>\n"
            file_str += f"#define SIZE {size}\n"
            file_str += "int main() {\n"
            for var in variables:
                if var[0][-4:] == "[];\n":
                    var[0] = var[0].replace("[]", "[SIZE]")

                file_str += f"\n\t{var[0]}"

                name = uuid.uuid4()
                while name in uuids:
                    name = uuid.uuid4()
                uuids.add(name)

                file_str += f"\tklee_make_symbolic(&{var[1]}," + \
                            f" sizeof({var[1]}), \"{str(name).replace('-', '')}\");\n"
                if ('int' in var[0]) and ('[' not in var[0]) and ('*' not in var[0]):
                    file_str += f"""\tif (({var[1]}<-1) || ({var[1]}>1024)) {{\n\t\t return 0;}}\n"""
                var_names.append(var[1])

            if func_visitor.types[func_name] == 'void':
                file_str += f"\t{func_name}({', '.join(var_names)});\n"
                file_str += "\treturn 0;\n"
            else:
                file_str += f"\treturn {func_name}({', '.join(var_names)});\n"
            file_str += "}\n"
            klee_formatted_files[func_name] = file_str
        return klee_formatted_files
