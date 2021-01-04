"""Script for running Klee on a series of functions and saving data."""

import subprocess
from typing import List

from core.log import Log
from klee.klee_utils import (KleeUtils, create_pandas, graph_stat,
                             klee_compare, run_experiment)


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
    """Run the klee experiment."""
    run_experiment("--dump-states-on-halt=false --max-time=5min", ['1', '2', '3', '4'],
                   run_klee_experiment)


if __name__ == "__main__":
    main()
