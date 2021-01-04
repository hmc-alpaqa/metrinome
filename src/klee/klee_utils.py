"""Handles work with klee, which does symbollic execution and test generation of C code."""

import re
import subprocess
import time
import uuid
from collections import defaultdict
from subprocess import PIPE
from typing import DefaultDict, Dict, List, Optional, Set, Tuple, Union

import pandas as pd  # type: ignore
from pycparser import c_ast, c_generator, parse_file  # type: ignore

from core.log import Log

KleeOutputInfo = Tuple[Optional[int],
                       Optional[int],
                       Optional[int],
                       float, float, float]
KleeCompareResults = Dict[Tuple[str, str, str],
                          Dict[str, Optional[Union[float, int]]]]
KleeOutputPreferencesInfo = Tuple[Optional[int],
                                  Optional[int],
                                  Optional[int],
                                  float, float, float, float]


def create_pandas(results: KleeCompareResults, preference: str, input_: str,
                  max_depths: List[str], fields: List[str]) -> pd.DataFrame:
    """Create a pandas dataframe from the results of a Klee experiment."""
    index = [f'max depth {i}' for i in max_depths]
    data = [[results[(preference, depth, input_)][field] for field in fields]
            for depth in max_depths]
    return pd.DataFrame(data, index=index, columns=fields)


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


class FuncVisitor(c_ast.NodeVisitor):
    """
    Look at a single C function an gather the information for Klee.

    The FuncVisitor visits each function once and then visits all of the variable
    definitions in the function definition in order to get their names and types.
    """

    def __init__(self, logger: Log) -> None:
        """Create a new instance of FuncVisitor."""
        self.logger = logger
        self._generator = c_generator.CGenerator()
        self.vars: DefaultDict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.types: DefaultDict[str, str] = defaultdict(str)
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
        self.logger.i_msg(f"Looking at {node.decl.name}()")
        self.types[node.decl.name] = return_type
        if args is not None:
            params = args.params  # List of TypeDecl.
            for i, param in enumerate(params):
                self.logger.d_msg(f"\tParameter {i}: Name: {param.name}")
                self.define_var(node.decl.name, self._generator.visit(param), param.name)
        else:
            self.logger.d_msg(f"\t{node.decl.name} has no parameters.")


class KleeUtils:
    """
    KleeUtils is used to make working with KLEE much easier in the REPL.

    This is used to parse C code and generate new Klee-compatible
    source code in order to make static analysis much easier.
    """

    def __init__(self, logger: Log) -> None:
        """Create a new instance of KleeUtils."""
        self.logger = logger

    def show_func_defs(self, filename: str, size: int = 10,
                       optimized: bool = False) -> Dict[str, str]:
        """
        Generate the set of klee-compatible files.

        Create a new set of files based on an existing file that are formatted properly
        to work with klee.
        """
        self.logger.d_msg(f"Going to parse file {filename}")
        if optimized:
            cppargs = ['-O3', '-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include']
        else:
            cppargs = ['-nostdinc', '-E', r'-I/app/pycparser/utils/fake_libc_include']
        ast = parse_file(filename, use_cpp=True, cpp_path='gcc', cpp_args=cppargs)
        self.logger.d_msg("Going to visit functions.")
        func_visitor = FuncVisitor(self.logger)
        func_visitor.visit(ast)

        uuids: Set[uuid.UUID] = set()
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

                var_names.append(var[1])

            if func_visitor.types[func_name] == 'void':
                file_str += f"\t{func_name}({', '.join(var_names)});\n"
                file_str += "\treturn 0;\n"
            else:
                file_str += f"\treturn {func_name}({', '.join(var_names)});\n"
            file_str += "}\n"
            klee_formatted_files[func_name] = file_str
        return klee_formatted_files
