"""Script for running Klee on a series of functions and saving data."""

import subprocess
import sys
from subprocess import PIPE
from typing import Callable, List, Optional

import matplotlib.pyplot as plt  # type: ignore

from core.env import Env
from core.log import Log
from klee.klee_time_test import create_pandas_time, graph_stat_time, klee_compare_time
from klee.klee_utils import (KleeCompareResults, KleeUtils, create_pandas, get_functions_list, get_stats_dict, klee_cmd,
                             klee_with_opts)

KleeExperiment = Callable[[str, int, List[str], List[str], List[str], List[str]], None]
plt.rcParams["figure.figsize"] = (10, 10)


# pylint: disable=cell-var-from-loop


class KleeExperimentHandler:
    """The experiments handler allows us to set options and run klee experiments."""

    def __init__(self, preference: str, max_depths: List[str], optimized: bool = False) -> None:
        """Create a new instance of the experiments handler."""
        self.pref = preference
        self.max_depths = max_depths
        self.array_size = 100
        self.fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime",
                       "UserTime", "SysTime", "PythonTime"]
        self.inputs = [""]
        self.optimized = optimized
        self.c_files_dir = "/app/code/tests/cFiles/fse_2020_benchmark"

    def run_experiment(self) -> None:
        """
        Run a Klee experiment.

        For each function, runs Klee once with each maximum depth,
        saves the data as a csv, and creates a graph for each field.
        """
        subprocess.run(f"mkdir {self.c_files_dir}/frames/", shell=True, check=False)
        list(map(self.klee_experiment, get_functions_list()))

    def klee_compare(self, file_name: str, function: str,
                     remove: bool = True) -> KleeCompareResults:
        """
        Run Klee on a certain function.

        Run Klee on the function with a variety of depths and preferences,
        and return the results as a dictionary of dictionaries.
        """
        results_dict = {}
        for depth in self.max_depths:
            for input_ in self.inputs:
                algs_path = f"{self.c_files_dir}/klee"
                output_file = f"{algs_path}_{self.pref}_{depth}_{input_}_{function}_output"
                output_file = output_file.replace(" ", "_")
                results = klee_with_opts(file_name, output_file, self.pref, depth, False, input_)
                stats_params = "--table-format=simple --print-all"
                stats = subprocess.run(f"{Env.KLEE_PATH}-stats {stats_params} {output_file}",
                                       shell=True, stdout=PIPE, stderr=PIPE, check=True)
                if remove:
                    subprocess.run(f"rm -rf {output_file}", shell=True, check=False)
                else:
                    subprocess.run(f"for f in {output_file}/test*; do rm \"$f\"; done",
                                   shell=True, check=True)
                stats_decoded = stats.stdout.decode().split("\n")
                results_dict[(self.pref, depth, input_)] = get_stats_dict(stats_decoded, results)

        return results_dict

    def klee_experiment_helper(self, func: str, key: str, val: str,
                               optimized: bool = False) -> KleeCompareResults:
        """Run the KLEE experiment for a single function given results from showing func defs."""
        filename = f"{func}_{key}_optimized" if optimized else f"{func}_{key}"
        new_name = f"{self.c_files_dir}/{filename}.c"
        bcname = f"{self.c_files_dir}/{filename}.bc"

        with open(new_name, "w+") as file:
            file.write(val)

        subprocess.run(klee_cmd(bcname, new_name), shell=True, capture_output=True, check=True)
        res = self.klee_compare(bcname, filename)
        frame = create_pandas(res, self.pref, self.inputs[0], self.max_depths, self.fields)
        frame.to_csv(f'{self.c_files_dir}/frames/{filename}.csv')
        return res

    def klee_experiment(self, func: str) -> None:
        """Run the KLEE experiment for a single function."""
        filename = f"{self.c_files_dir}/{func}.c"
        output = KleeUtils(Log()).show_func_defs(filename, size=self.array_size)

        if self.optimized:
            output2 = KleeUtils(Log()).show_func_defs(filename, self.array_size, optimized=True)
            for i, j in zip(output, output2):
                res = self.klee_experiment_helper(func, i, output[i])
                res2 = self.klee_experiment_helper(func, j, output2[j], True)

                list(map(lambda f: self.graph_stat(func, self.pref, res, res2, f), self.fields))
        else:
            for key, val in output.items():
                res = self.klee_experiment_helper(func, key, val)
                list(map(lambda f: self.graph_stat(func, self.pref, res, None, f), self.fields))

    def graph_stat(self, func: str, preference: str, results: KleeCompareResults,
                   results2: Optional[KleeCompareResults], field: str) -> None:
        """Create and save a graph for a certain statistic on a Klee experiment."""
        subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/graphs/",
                       shell=True, check=False)
        fig1, ax1 = plt.subplots()
        depths = list(map(float, self.max_depths))
        for input_ in self.inputs:
            stats = [results[(preference, i, input_)][field] for i in self.max_depths]
            ax1.plot(depths, stats, label=func)
            if results2 is not None:
                stats2 = [results2[(preference, i, input_)][field] for i in self.max_depths]
                ax1.plot(depths, stats2, label=func + " optimized")

        ax1.set(xlabel='depth', ylabel=field, title=func)
        ax1.legend()
        ax1.grid()

        algs_path = "/app/code/tests/cFiles/fse_2020_benchmark"
        fig1.savefig(f"{algs_path}/graphs/{field}_{func}.png".replace("%", "percent"))
        plt.close(fig1)

    def run_klee_time(self, func: str, max_times: List[str]) -> None:
        """Run the KLEE experiment for a single function."""
        filename = f"{self.c_files_dir}/{func}.c"
        output = KleeUtils(Log()).show_func_defs(filename, size=self.array_size)

        for i in output:
            new_name = f"{self.c_files_dir}/{func}_{i}.c"
            bcname = f"{self.c_files_dir}/{func}_{i}.bc"
            with open(new_name, "w+") as file:
                file.write(output[i])
            subprocess.run(klee_cmd(bcname, new_name), shell=True, capture_output=True, check=True)
            results = klee_compare_time(bcname, [self.pref], max_times, f"{func}_{i}")
            results_frame = create_pandas_time(results, self.pref, max_times, self.fields)
            filename = f'{self.c_files_dir}/frames_time/{func}_{i}.csv'
            results_frame.to_csv(filename)
            for field in self.fields:
                graph_stat_time(f"{func}_{i}", self.pref, max_times, results, field)


def main() -> None:
    """Run the klee experiment."""
    opts = "--dump-states-on-halt=false --max-time=5min"
    if sys.argv[1] == "optimized":
        KleeExperimentHandler(opts, ['1', '2', '3', '4'], True).run_experiment()
    elif sys.argv[1] == "normal":
        max_depths = list(map(str, range(1, 21))) + list(map(str, range(30, 110, 10)))
        KleeExperimentHandler(opts, max_depths).run_experiment()
    elif sys.argv[1] == "time_test":
        subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/frames_time/",
                       shell=True, check=False)
        handler = KleeExperimentHandler("--dump-states-on-halt=false", [])
        handler.run_klee_time("32_newtons_method", list(map(str, range(1, 16))))


if __name__ == "__main__":
    main()
