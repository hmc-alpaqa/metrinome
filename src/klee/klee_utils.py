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
        # print(node.decl.type.type.type.names)

        try:
            return_type = node.decl.type.type.type.names[0]
        except AttributeError:
            return_type = None

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

    def generate_assume_loops(self, var_name, dimensions):
        loop_str = ""
        indent = "\t\t"
        for d in range(dimensions):
            loop_str += f"{indent}for (int i{d} = 0; i{d} < SIZE; i{d}++) {{\n"
            indent += "\t"

        # Adding klee_assume statement
        indices = "[" + "][".join(f"i{d}" for d in range(dimensions)) + "]"
        loop_str += f"{indent}klee_assume({var_name}{indices} <= MAX_VALUE);\n"

        # Closing braces
        for d in range(dimensions):
            indent = indent[:-1]
            loop_str += f"{indent}}}\n"

        return loop_str

    def show_single_func_defs(self, filename: str, function_name: str, size: int = 1024,
                            optimized: bool = False) -> dict[str, str]:
        """
        Generate the set of klee-compatible files.
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
        variables = [list(v) for v in func_visitor.vars[function_name]]
        var_names = []

        file_str = "#include <klee/klee.h>\n"
        file_str += f"#include <{filename}>\n"
        file_str += f"#define SIZE {size}\n"
        file_str += f"#define MAX_VALUE 65536\n"
        file_str += "int main() {\n"

        for var in variables:
            brackets = var[0].count('[]') 
            pointers = var[0].count('*')
            if brackets > 0:
                var[0] = var[0].replace("[]", "[SIZE]")
            
            if pointers > 0:
                var[0] = var[0].replace('*', '', pointers)
                var[0] = var[0].replace(';', f"{'[SIZE]' * pointers};", 1)

            file_str += f"\n\t{var[0]}"
            name = uuid.uuid4()
            while name in uuids:
                name = uuid.uuid4()
            uuids.add(name)

            file_str += f"\tklee_make_symbolic(&{var[1]}," + \
                        f" sizeof({var[1]}), \"{str(name).replace('-', '')}\");\n"

            # if dimensions > 0:
            #     file_str += self.generate_assume_loops(var[1], dimensions)

            # Other conditions remain unchanged
            if ('int' in var[0]) and ('[' not in var[0]) and ('*' not in var[0]):
                file_str += f"""\tif (({var[1]}<=0) || ({var[1]}>1024)) {{\n\t\t return 0;}}\n"""
            if ('size_t' in var[0]) and ('[' not in var[0]) and ('*' not in var[0]):
                file_str += f"""\tif (({var[1]}<=0) || ({var[1]}>1024)) {{\n\t\t return 0;}}\n"""

            var_names.append(var[1])

        # Function call and return statements
        if func_visitor.types[function_name] == 'void':
            file_str += f"\t{function_name}({', '.join(var_names)});\n"
            file_str += "\treturn 0;\n"
        elif None in var_names:
            file_str += f"\treturn {function_name}();\n"
        else:
            file_str += f"\treturn {function_name}({', '.join(var_names)});\n"
        file_str += "}\n"
        klee_formatted_files[function_name] = file_str
        return klee_formatted_files

    def show_func_defs(self, filename: str, size: int = 100,
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
            # cppargs = ['-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include', r'-I/usr/include/x86_64-linux-gnu/']
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
            # print(variables)
            # exit(0)
            for var in variables:
                if var[0][-4:] == "[];\n":
                    var[0] = var[0].replace("[]", "[SIZE]")
                
                # if it contains a pointer, we need to make it symbolic same as an array
                # do this by adding SIZE to the end of the declaration
                # for example, int *a; becomes int a[SIZE];
                # we need to do this for each * so int **a; becomes int a[SIZE][SIZE];
                for i in range(var[0].count('*')):
                    # remove the first * from the declaration
                    var[0] = var[0].replace('*', '', 1)
                    # add SIZE to the end of the declaration
                    var[0] = var[0].replace(';', f"[SIZE];", 1)


                file_str += f"\n\t{var[0]}"

                name = uuid.uuid4()
                while name in uuids:
                    name = uuid.uuid4()
                uuids.add(name)
                
                file_str += f"\tklee_make_symbolic(&{var[1]}," + \
                            f" sizeof({var[1]}), \"{str(name).replace('-', '')}\");\n"
                if ('int' in var[0]) and ('[' not in var[0]) and ('*' not in var[0]):
                    file_str += f"""\tif (({var[1]}<-1) || ({var[1]}>1024)) {{\n\t\t return 0;}}\n"""
                if ('size_t' in var[0]) and ('[' not in var[0]) and ('*' not in var[0]):
                    file_str += f"""\tif (({var[1]}<=0) || ({var[1]}>1024)) {{\n\t\t return 0;}}\n"""
                var_names.append(var[1])

            if func_visitor.types[func_name] == 'void':
                file_str += f"\t{func_name}({', '.join(var_names)});\n"
                file_str += "\treturn 0;\n"
            elif None in var_names:
                file_str += f"\treturn {func_name}();\n"
            else:
                file_str += f"\treturn {func_name}({', '.join(var_names)});\n"
            file_str += "}\n"
            klee_formatted_files[func_name] = file_str
        return klee_formatted_files
