"""
Compute aggregate metrics and compare them.

Given two arbitrary metrics we can compute, such as Path Complexity and NPath Complexity,
we often want to know if there is some trend between them. For example, given some set of functions
that all output value 'x' for metric A, it is useful to know how metric B varies across that same
set of functions. Thus, we first aggregate all of our data, create a single dictionary that maps
(metric1, metric2) -> ComparitorDict, where ComparitorDict has metric1 values as keys, and maps a
metric1 value to all metric2 values that occured with the given metric1 values.

Once this is done, 
"""


from command_data import MetricsDict
from command import Controller
from collections import defaultdict
from itertools import combinations
from typing import Dict, NewVar, MetricRes, List, Tuple
from log import Log


MetricName = NewVar('MetricName', str)
AggregateMetricsDict = Dict[MetricRes, List[MetricRes]]


class MetricsComparer:
    """Allows the comparison between different metrics such as NPath and APC."""

    def __init__(self, metrics_dict: MetricsDict) -> None:
        """TODO"""
        self.metrics_dict = metrics_dict
        self.metric_names = [x.name() for x in Controller(Log()).metrics_generators]
        aggregate_metrics = self.aggregate()

    def aggregate(self) -> Dict[Tuple[MetricName, MetricName], AggregateMetricsDict]:
        """TODO"""
        aggregate_metrics: Dict[Tuple[MetricName, MetricName], AggregateMetricsDict] = {}
        for metric_name_one, metric_name_two in combinations(self.metric_names, 2):
            aggregate_metrics[(metric_name_one, metric_name_two)] = {}
            aggregate_metrics[(metric_name_two, metric_name_one)] = {}

        for metric_vals in self.metrics_dict.values():
            for metric_pair in combinations(metric_vals, 2):
                metric_one_name, metric_one_val = metric_pair[0]
                metric_two_name, metric_two_val = metric_pair[1]
                agg_metrics_dict = aggregate_metrics[(metric_one_name, metric_two_name)]
                agg_metrics_dict[metric_one_val].append(metric_two_val)

        return aggregate_metrics

