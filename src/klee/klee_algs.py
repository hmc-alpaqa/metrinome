"""Script for running Klee on a series of functions and saving data."""

import subprocess
from typing import List

from core.log import Log
from klee.klee_utils import (KleeUtils, create_pandas, graph_stat,
                             klee_command, klee_compare, run_experiment)


def run_klee_experiment(func: str, array_size: int, max_depths: List[str],
                        preferences: List[str], fields: List[str], inputs: List[str]) -> None:
    """Run the KLEE experiment for a single function."""
    filename = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}.c"
    output = KleeUtils(Log()).show_func_defs(filename, size=array_size)

    for i in output:
        new_name = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{i}.c"
        bcname = f"/app/code/tests/cFiles/fse_2020_benchmark/{func}_{i}.bc"
        with open(new_name, "w+") as file:
            file.write(output[i])
        subprocess.run(klee_command(bcname, new_name), shell=True, capture_output=True, check=True)
        results = klee_compare(bcname, preferences, max_depths, inputs, f"{func}_{i}")
        results_frame = create_pandas(results, preferences[0], inputs[0], max_depths, fields)
        results_frame.to_csv(f'/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}.csv')
        for field in fields:
            graph_stat(func, preferences[0], max_depths, inputs, results, None, field)


def main() -> None:
    """Run a Klee experiment."""
    max_depths = list(map(str, range(1, 21))) + ['30', '40', '50', '60', '70', '80', '90', '100']
    run_experiment("--dump-states-on-halt=false --max-time=5min", max_depths, run_klee_experiment)


if __name__ == "__main__":
    main()
