"""
Compute aggregate metrics and compare them.

Given two arbitrary metrics we can compute, such as Path Complexity and NPath Complexity,
we often want to know if there is some trend between them. For example, given some set of functions
that all output value 'x' for metric A, it is useful to know how metric B varies across that same
set of functions. Thus, we first aggregate all of our data, create a single dictionary that maps
(metric1, metric2) -> ComparitorDict, where ComparitorDict has metric1 values as keys, and maps a
metric1 value to all metric2 values that occured with the given metric1 values.

Once this is done, we then count how many instances of each value show up.
"""


import typing
from collections import Counter, defaultdict
from itertools import combinations

from core.command import Command, Controller
from core.command_data import MetricRes, MetricsDict
from core.log import Log
from main import Options

AggregateMetricsDict = dict[MetricRes, list[MetricRes]]


class MetricsComparer:
    """Allows the comparison between different metrics such as NPath and APC."""

    def __init__(self, metrics_dict: MetricsDict) -> None:
        """Create a new instance of the MetricsComparer."""
        self.metrics_dict = metrics_dict
        self.metric_names = [x.name() for x in Controller(Log()).metrics_generators]
        aggregate_metrics = self.aggregate()
        self.counter_dict = self.counter(aggregate_metrics)

    def aggregate(self) -> dict[tuple[str, str], AggregateMetricsDict]:
        """For each (metric name 1, metric name 2), map each 'metric 1 val' -> [metric 2 vals]."""
        # Create an empty dictionary that can be used to store the results.
        aggregate_metrics: dict[tuple[str, str], AggregateMetricsDict] = {}
        for metric_name_one, metric_name_two in combinations(self.metric_names, 2):
            aggregate_metrics[(metric_name_one, metric_name_two)] = defaultdict(list)
            aggregate_metrics[(metric_name_two, metric_name_one)] = defaultdict(list)

        # Populate the dictionary with the metric result.
        for metric_vals in self.metrics_dict.values():
            for metric_pair in combinations(metric_vals, 2):
                metric_one_name, metric_one_val = metric_pair[0]
                metric_two_name, metric_two_val = metric_pair[1]
                agg_metrics_dict = aggregate_metrics[(metric_one_name, metric_two_name)]
                agg_metrics_dict[metric_one_val].append(metric_two_val)

        return aggregate_metrics

    def counter(self, aggregate_metrics: dict[tuple[str, str],
                                              AggregateMetricsDict]) -> \
            dict[tuple[str, str],
                 dict[MetricRes, typing.Counter[MetricRes]]]:
        """Create a dict that stores the discrete conditional distributions of each metric pair."""
        counter_dict = {}
        for agg_metrics_key, agg_metrics_dict in aggregate_metrics.items():
            tmp: dict[MetricRes, typing.Counter[MetricRes]] = {}
            for key, val in agg_metrics_dict.items():
                tmp[key] = Counter(val)
            counter_dict[agg_metrics_key] = tmp

        return counter_dict


def test_analysis() -> None:
    """Analyze metric results from test C files."""
    command = Command(curr_path="", debug_mode=False,
                      multi_threaded=False, repl_wrapper=None)
    command.do_convert("/app/code/tests/cFiles/*")
    command.do_metrics(Options(), "*")
    metrics_comparer = MetricsComparer(command.data.metrics)
    print(metrics_comparer.counter_dict)


if __name__ == "__main__":
    test_analysis()
