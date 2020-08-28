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


from collections import Counter, defaultdict
import typing
from typing import Dict, List, Tuple
from itertools import combinations
from log import Log
from command_data import MetricsDict, MetricRes
from command import Controller, Command


AggregateMetricsDict = Dict[MetricRes, List[MetricRes]]


class MetricsComparer:
    """Allows the comparison between different metrics such as NPath and APC."""

    def __init__(self, metrics_dict: MetricsDict) -> None:
        """TODO."""
        self.metrics_dict = metrics_dict
        self.metric_names = [x.name() for x in Controller(Log()).metrics_generators]
        aggregate_metrics = self.aggregate()
        self.counter_dict = self.counter(aggregate_metrics)

    def aggregate(self) -> Dict[Tuple[str, str], AggregateMetricsDict]:
        """TODO."""
        aggregate_metrics: Dict[Tuple[str, str], AggregateMetricsDict] = {}
        for metric_name_one, metric_name_two in combinations(self.metric_names, 2):
            aggregate_metrics[(metric_name_one, metric_name_two)] = defaultdict(list)
            aggregate_metrics[(metric_name_two, metric_name_one)] = defaultdict(list)

        for metric_vals in self.metrics_dict.values():
            for metric_pair in combinations(metric_vals, 2):
                metric_one_name, metric_one_val = metric_pair[0]
                metric_two_name, metric_two_val = metric_pair[1]
                agg_metrics_dict = aggregate_metrics[(metric_one_name, metric_two_name)]
                agg_metrics_dict[metric_one_val].append(metric_two_val)

        return aggregate_metrics

    def counter(self, aggregate_metrics: Dict[Tuple[str, str],
                                              AggregateMetricsDict]) -> \
            Dict[Tuple[str, str],
                 Dict[MetricRes, typing.Counter[MetricRes]]]:
        """TODO."""
        counter_dict = {}
        for agg_metrics_key, agg_metrics_dict in aggregate_metrics.items():
            tmp: Dict[MetricRes, typing.Counter[MetricRes]] = {}
            for key, val in agg_metrics_dict.items():
                tmp[key] = Counter(val)
            counter_dict[agg_metrics_key] = tmp

        return counter_dict


def test_analysis() -> None:
    """TODO."""
    command = Command(curr_path="", debug_mode=False,
                      multi_threaded=False, repl_wrapper=None)
    command.do_convert("/app/code/tests/cFiles/*")
    command.do_metrics("*")
    metrics_comparer = MetricsComparer(command.data.metrics)
    print(metrics_comparer.counter_dict)


if __name__ == "__main__":
    test_analysis()
