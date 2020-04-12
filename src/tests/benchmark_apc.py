"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

from statistics import mean, median, stdev, variance
import sys
import os
import glob
import time
sys.path.append("/app/code/")
sys.path.append("/app/code/metric")
from graph import Graph
from metric import path_complexity
from tests import utils

def apc_runtime():
    """Test the amount of time it takes to run asymptotic path analysis on different sized graphs."""
    folders = (glob.glob("/app/examples/cfgs/apache_cfgs/*/"))
    metric_collection = []
    # list of tuples for all cfgs in all folders (seconds, folder, cfg).
    overall_time_list = []

    # test the metrics for each folder in apache_cfgs.
    for folder in folders:
        graph_list = (glob.glob(folder + "*.dot"))
        # list of tuples for each cfg in folder(seconds, cfg).
        folder_time_list = []
        # create instance of the npath clas.
        converter = path_complexity.PathComplexity()
        print(folder)
        # loop through each cfg in each folder.
        for i, graph in enumerate(graph_list):
            print(os.path.splitext(graph)[0].split("/")[-1],
                  f"{round(100*(i / len(graph_list)))}% done")
            graph_zero = Graph.from_file(graph)
            start_time = time.time()
            converter.evaluate(graph_zero)
            # Calculate the run time.
            runtime = time.time() - start_time
            # Add runtime to folder-specific list
            folder_time_list.append((runtime, graph))
            # Add runtime to overall list
            overall_time_list.append((runtime, folder, graph))
            print(f"Runtime {runtime}")
            # Print metrics at 50% completion of folder
            if round(100 * (i / len(graph_list))) == 50:
                print(utils.runtime_metrics(folder_time_list))

        folder_metrics = utils.runtime_metrics(folder_time_list)
        folder_outliers = utils.runtime_outlier(folder_time_list)
        print("METRICS: ")
        # print metrics at 100% completion of folder.
        print(folder_metrics)
        print("OUTLIERS: ")
        # print list of cfgs at above +1 stdev away.
        print(folder_outliers)
        print(" ")
        print(" ")
        print(" ")
        metric_collection.append((folder, folder_metrics, folder_outliers))
        print("COLLECTED METRICS: ")
        # print overall metrics for all folders so far.
        print(metric_collection)

    # print overall metrics for all cfgs.
    print(utils.runtime_metrics(overall_time_list))
    # print cfgs at above +1 stdev away.
    print(utils.runtime_outlier(overall_time_list))


def main():
    """Execute the tests."""
    # create instance of the npath class
    converter = npath_complexity.PathComplexity()
    graph_zero = Graph.from_file("/app/examples/cfgs/apache_cfgs/commons-net-3.3/\
                                org_apache_commons_net_nntp_Threader_buildContainer_0_basic.dot",
                                 False, True)
    print("list version:")
    print(converter.evaluate(graph_zero))
    graph_one = Graph.from_file("/app/examples/cfgs/apache_cfgs/commons-net-3.3/\
                                org_apache_commons_net_nntp_Threader_buildContainer_0_basic.dot",
                                False, False)
    print("dict version:")
    print(converter.evaluate(graph_one))
