"""Various utilities used only for testing and not the main REPL."""

from contextlib import contextmanager
from io import StringIO
import sys
import time
import os
import glob
from math import floor
from numpy import mean, std, median  # type: ignore
from graph import Graph
from utils import Timeout


def run_benchmark(converter):
    """Run all CFGs through the converter to create a benchmark."""
    folders = (glob.glob("/app/examples/cfgs/apache_cfgs/*/"))

    metric_collection = []
    # list of tuples for all cfgs in all folders (seconds, folder, cfg).
    overall_time_list = []

    graph_frac = 5
    folders_frac = len(folders)
    graph_list = []
    
    # test the metrics for each folder in apache_cfgs.
    print(f"Num Folders: {floor(len(folders) / folders_frac)}")
    for folder in folders[0:floor(len(folders) / folders_frac)]:
        graph_list = (glob.glob(folder + "*.dot"))[0:floor(len(graph_list) / graph_frac)]
        # list of tuples for each cfg in folder(seconds, cfg).
        folder_time_list = []
        # create instance of the npath clas.
        print(folder)

        folder_time_list, overall_time_list = get_converter_time(graph_list,
                                                                 converter, folder)

        metric_collection = print_results(folder_time_list,
                                          folder, metric_collection)

    print_overall_results(overall_time_list)


def print_overall_results(overall_time_list):
    """Print the results once the benchmark is done."""
    # print overall metrics for all cfgs.
    print(runtime_metrics(overall_time_list))
    # print cfgs at above +1 stdev away.
    print(runtime_outlier(overall_time_list))


def get_converter_time(graph_list, converter, folder):
    """Run the the converter on all graph files from some folder."""
    # loop through each cfg in each folder.
    folder_time_list = []
    overall_time_list = []

    for i, graph in enumerate(graph_list):
        print(os.path.splitext(graph)[0].split("/")[-1],
              f"{round(100*(i / len(graph_list)))}% done")
        graph_zero = Graph.from_file(graph)
        start_time = time.time()
        try:
            with Timeout(5, 'Path-Complexity took too long'):
                converter.evaluate(graph_zero)

            # Calculate the run time.
            runtime = time.time() - start_time

            # Add runtime to folder-specific list.
            folder_time_list.append((runtime, graph))

            # Add runtime to overall list.
            overall_time_list.append((runtime, folder, graph))
            print(f"Runtime {runtime}")

        except TimeoutError as exception:
            print(exception)

    return folder_time_list, overall_time_list


def print_results(folder_time_list, folder, metric_collection):
    """Print out the results from the benchmark."""
    folder_metrics = runtime_metrics(folder_time_list)
    folder_outliers = runtime_outlier(folder_time_list)
    print("METRICS: ")
    # print metrics at 100% completion of folder.
    print(folder_metrics)
    print("OUTLIERS: ")
    # print list of cfgs at above +1 stdev away.
    print(folder_outliers)
    print("\n\n\n")
    metric_collection = metric_collection.append((folder, folder_metrics, folder_outliers))
    # print overall metrics for all folders so far.
    print(f"COLLECTED METRICS: \n{metric_collection}")
    return metric_collection


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
    print("\n \n")
    return [("maximum", max_val), ("minimum", min_val), ("mean", average),
            ("median", median_val), ("stdev", stdev_val)]


def runtime_outlier(time_list):
    """
    Return all outlier elements.

    Given a list of tuples (runtime, Graph), return the elements of that list that are outliers.
    """
    print("OUTLIERS ")
    times = [x[0] for x in time_list]
    average = mean(times)
    stdev_val = std(times)
    outliers = []
    for time_tuple in time_list:
        if time_tuple[0] > (average + (2 * stdev_val)):
            outliers.append(time_tuple)
    return outliers
