"""Various utilities used only for testing and not the main REPL."""

from contextlib import contextmanager
from io import StringIO
import sys
import time
import os
import glob
from math import floor
from typing import List, Any
from numpy import mean, std, median  # type: ignore
from graph import Graph
from utils import Timeout


def run_benchmark(converter, graph_type, show_info, graph_frac=5,
                  folders_frac=46, timeout_threshold=5):
    """Run all CFGs through the converter to create a benchmark."""
    folders = (glob.glob("/app/examples/cfgs/apache_cfgs/*/"))
    print(f"number of folders: {len(folders)}\n")
    metric_collection: List[Any] = []
    # list of tuples for all cfgs in all folders (seconds, folder, cfg).
    overall_time_list = []
    timeout_total = 0
    # test the metrics for each folder in apache_cfgs.
    print(f"Num Folders: {floor(len(folders) / folders_frac)}")
    for folder in folders[0:floor(len(folders) / folders_frac)]:
        print(f"On folder {folder}")
        graph_list = (glob.glob(folder + "*.dot"))
        graph_list = graph_list[0:floor(len(graph_list) / graph_frac)]
        # list of tuples for each cfg in folder(seconds, cfg).
        print(f"Num Graphs: ", len(graph_list))
        folder_time_list, overall_time_list, timeout_count = get_converter_time(graph_list,
                                                                                converter, folder,
                                                                                timeout_threshold,
                                                                                graph_type,
                                                                                show_info)
        timeout_total += timeout_count

        print_results(folder_time_list, folder, metric_collection, show_info)

    print("======= OVERALL ==========")
    print_overall_results(overall_time_list, timeout_total, timeout_threshold)


def print_overall_results(overall_time_list, timeout_total, timeout_threshold) -> None:
    """Print the results once the benchmark is done."""
    # print overall metrics for all cfgs.
    print(runtime_metrics(overall_time_list))
    # print cfgs at above +1 stdev away.
    print(runtime_outlier(overall_time_list, True))
    print(f"\nTOTAL TIMEOUTS: {timeout_total}\n")
    print(f"TIMEOUT THRESHOLD: {timeout_threshold} Seconds")


def get_converter_time(graph_list, converter, folder, timeout_threshold, graph_type, show_info):
    """Run the the converter on all graph files from some folder."""
    # loop through each cfg in each folder.
    folder_time_list = []
    overall_time_list = []
    timeout_count = 0

    for i, graph in enumerate(graph_list):
        if show_info:
            print(os.path.splitext(graph)[0].split("/")[-1],
                  f"{round(100*(i / len(graph_list)))}% done")
        graph_zero = Graph.from_file(graph, graph_type=graph_type)
        start_time = time.time()
        try:
            with Timeout(timeout_threshold, f'{converter.name()} took too long'):
                res = converter.evaluate(graph_zero)
                print(res)

            # Calculate the run time.
            runtime = time.time() - start_time

            # Add runtime to folder-specific list.
            folder_time_list.append((runtime, graph))

            # Add runtime to overall list.
            overall_time_list.append((runtime, folder, graph))
            if show_info:
                print(f"Runtime {runtime}")

        except TimeoutError as exception:
            if show_info:
                print(exception)
            timeout_count += 1

    return folder_time_list, overall_time_list, timeout_count


def print_results(folder_time_list, folder, metric_collection, show_info):
    """Print out the results from the benchmark."""
    folder_metrics = runtime_metrics(folder_time_list)
    folder_outliers = runtime_outlier(folder_time_list, show_info)
    if show_info:
        print("METRICS: ")
        # print metrics at 100% completion of folder.
        print(folder_metrics)
        print("OUTLIERS: ")
        # print list of cfgs at above +1 stdev away.
        print(folder_outliers)
        print("\n\n")

    metric_collection.append((folder, folder_metrics, folder_outliers))
    if show_info:
        # print overall metrics for all folders so far.
        print(f"COLLECTED METRICS: \n{metric_collection}")


@contextmanager
def captured_output():
    """
    Capture output printed to stdout and stderr.

    Allows us to obtain strings that would normally be printed to
    standard out and standard error. This can be helpful in writing
    unit tests for the REPL as we want to verify that the correct
    strings are propagated to the user.
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def runtime_metrics(time_list):
    """
    Given a list of run times compute a series of statistics.

    These include: max, min, mean, median, stddev, variance.
    """
    times = [x[0] for x in time_list]
    max_val = max(times)
    min_val = min(times)
    average = mean(times)
    median_val = median(times)
    stdev_val = std(times)
    return [("maximum", max_val), ("minimum", min_val), ("mean", average),
            ("median", median_val), ("stdev", stdev_val)]


def runtime_outlier(time_list, show_info):
    """
    Return all outlier elements.

    Given a list of tuples (runtime, Graph), return the elements of that list that are outliers.
    """
    if show_info:
        print("OUTLIERS: ")
    times = [x[0] for x in time_list]
    average = mean(times)
    stdev_val = std(times)
    outliers = []
    for time_tuple in time_list:
        if time_tuple[0] > (average + (2 * stdev_val)):
            outliers.append(time_tuple)
    return outliers
