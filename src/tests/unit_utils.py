"""Various utilities used only for testing and not the main REPL."""

from contextlib import contextmanager
from io import StringIO
import sys
from numpy import mean, std, median


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

