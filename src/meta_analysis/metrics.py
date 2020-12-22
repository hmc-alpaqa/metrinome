"""Compute aggregate metrics and compare them."""

import logging
import typing
from collections import defaultdict
from math import log
from typing import DefaultDict, Dict, List, Set, Tuple, Union

from scipy.stats import entropy  # type: ignore


def adjusted_rand_index(function_list: List[int]) -> float:
    """
    Compute the adjusted rand index.

    The rand index is used to compare two different clusterings on a set by looking at all of the
    possible pairs of points in the set.
    """
    n_00 = 0  # In different clusters in both clusterings
    n_11 = 0  # In the same cluster in both clusterings
    n_01 = 0  # Different in the first clustering but not in the second
    n_10 = 0  # Same in the first clustering but not in the second
    # Iterate through all of the (N choose 2) possible pairs
    for func_one_index, func_one in enumerate(function_list):
        for func_two_index in range(func_one_index, len(function_list)):
            pair = (func_one, function_list[func_two_index])
            point_one_apc = pair[0]  # TODO
            point_two_apc = pair[1]  # TODO

            point_one_npath = pair[0]  # TODO
            point_two_npath = pair[1]  # TODO

            if point_one_apc == point_two_apc:
                if point_one_npath == point_two_npath:
                    n_11 += 1
                else:
                    n_10 += 1
            else:
                if point_one_npath == point_two_npath:
                    n_01 += 1
                else:
                    n_00 += 1

    numerator = 2 * (n_00 * n_11 - n_01 * n_10)
    denominator = ((n_00 + n_01) * (n_01 + n_11)) + (n_00 + n_10) * (n_10 + n_11)
    return numerator / denominator


CountingDict = Dict[Union[str, int], typing.Counter[Union[str, int]]]


def average_class_size(input_dict: CountingDict,
                       use_frequencies: bool) -> float:
    """
    Compute the average class size for a dictionary.

    Given some dictionary with key-value pairs
        (Metric1, Metric2),
    where given some value 'x' for Metric1, the dictionary will map to all values
    Metric2 takes on for the set of functions that took on value 'x' for Metric1
    """
    print(use_frequencies)

    num_classes = len(input_dict.keys())
    sum_averages = 0.

    logging.info("Working with: " + str(input_dict))
    logging.info(f"Number of Classes: {num_classes}")
    for key in input_dict.keys():
        total_counts = 0
        entropy_value = 0.

        for count_index in input_dict[key]:
            total_counts += input_dict[key][count_index]

        # Computing the shannon entropy
        for count_index in input_dict[key]:
            count = input_dict[key][count_index]
            prob = count / total_counts
            entropy_value += prob * log(prob)

        entropy_value *= -1

        # If we only have a single value, then the distribution is perfectly uniform
        if len(input_dict[key]) == 1:
            sum_averages += 1.
        # Ratio between entropy of our distribution and uniform (ideal) distribution
        else:
            entropy_ratio = entropy_value / log(len(input_dict[key]))
            logging.info(f"Found {total_counts} many counts for key {key}, \
                            obtaining entropy {entropy_value} \
                            and entropy ratio {entropy_ratio}")
            total = entropy_ratio * len(input_dict[key])
            sum_averages += entropy_ratio * len(input_dict[key])

            print(total)

    return sum_averages / num_classes


def mutual_information(cluster_list_one: Dict[int, Set[int]],
                       cluster_list_two: Dict[int, Set[int]]) -> float:
    """
    Calculate I(cluster_list_one, cluster_list_two).

    @see https://en.wikipedia.org/wiki/Mutual_information
    """
    cond_entropy = 0.
    # Obtain the total size.
    # TODO: is this supposed to be cluster_list_one?
    total_size = get_total_size(cluster_list_one)

    # Create a table of all the overlaps
    overlaps: List[List[int]] = [[0 for i in range(len(cluster_list_one))]
                                 for j in range(len(cluster_list_two))]
    for i, cluster_one in cluster_list_one.items():
        for j, cluster_two in cluster_list_two.items():
            cluster_overlap = len(cluster_one.intersection(cluster_two))
            overlaps[i][j] = cluster_overlap

    for i in range(len(cluster_list_two)):
        # Compute the marginal overlap
        marginal_overlap = 0
        for j in range(len(cluster_list_one)):
            marginal_overlap += overlaps[j][i]

        for j in range(len(cluster_list_one)):
            # Calculate the elements in common between both clusters
            cluster_one = cluster_list_one[i]
            cluster_two = cluster_list_two[j]
            numerator = overlaps[i][j] / total_size
            denominator = marginal_overlap / total_size
            log_param = numerator / denominator
            cond_entropy -= (cluster_overlap / total_size) * log(log_param, 2)

    return cond_entropy


def get_total_size(dictionary: Dict[int, Set[int]]) -> int:
    """Get the sum of lengths of all values in a dictionary."""
    total_size = 0
    for cluster in dictionary:
        total_size += len(dictionary[cluster])

    return total_size


def cluster_entropy(cluster_list: Dict[int, Set[int]]) -> float:
    """
    Calculate the entropy H(X) of a given clustering on a set.

    The input is a dictionary where each entry is a complexity
    class (representing a cluster) with a count (the number of
    things in the cluster)
    """
    total_entropy = 0.
    total_size = 0
    # Obtain the total size
    for cluster in cluster_list.keys():
        total_size += len(cluster_list[cluster])

    # Iterate through the clusters
    for cluster in cluster_list.keys():
        cluster_size = len(cluster_list[cluster])
        probability_list = [1 / cluster_size] * cluster_size
        total_entropy += entropy(probability_list) * (cluster_size / total_size)

    return total_entropy


def joint_entropy(cluster_list_one: Dict[int, Set[int]],
                  cluster_list_two: Dict[int, Set[int]]) -> float:
    """
    Compute H(X, Y).

    @see https://en.wikipedia.org/wiki/Joint_entropy

    The input is two dictionaries where each entry is a complexity class
    (representing a cluster) with a set of functions.
    """
    result = 0.
    total_size = 0

    # Obtain the total size
    for cluster in cluster_list_one.keys():
        total_size += len(cluster_list_one[cluster])

    for cluster_one in cluster_list_one.values():
        for cluster_two in cluster_list_two.values():
            # Calculate the elements in common between both clusters
            cluster_overlap = len(cluster_one.intersection(cluster_two))
            result -= (cluster_overlap / total_size) * \
                log((cluster_overlap / total_size), 2)

    return result


def conditional_entropy(cluster_list_one: Dict[int, Set[int]],
                        cluster_list_two: Dict[int, Set[int]]) -> float:
    """
    Calculate H(cluster_list_one | cluster_list_two).

    @see https://en.wikipedia.org/wiki/Conditional_entropy
    """
    cond_entropy = 0.
    total_size = 0

    # Obtain the total size.
    for cluster in cluster_list_one.keys():
        total_size += len(cluster_list_one[cluster])

    # Create a table of all the overlaps.
    overlaps: List[List[int]] = [[0 for i in range(len(cluster_list_one))]
                                 for j in range(len(cluster_list_two))]
    for i, cluster_one in cluster_list_one.items():
        for j, cluster_two in cluster_list_two.items():
            cluster_overlap = len(cluster_one.intersection(cluster_two))
            overlaps[i][j] = cluster_overlap

    for i in range(len(cluster_list_two)):
        # Compute the marginal overlap.
        marginal_overlap = 0
        for j in range(len(cluster_list_one)):
            marginal_overlap += overlaps[j][i]

        for j in range(len(cluster_list_one)):
            # Calculate the elements in common between both clusters.
            cluster_one = cluster_list_one[i]
            cluster_two = cluster_list_two[j]
            numerator = overlaps[i][j] / total_size
            denominator = marginal_overlap / total_size
            log_param = numerator / denominator
            cond_entropy -= (cluster_overlap / total_size) * log(log_param, 2)

    return cond_entropy


MetricsDictOne = DefaultDict[int, List[str]]
MetricsDictTwo = DefaultDict[str, List[int]]
MetricsCounter = Dict[Union[str, int], typing.Counter[Union[str, int]]]


class MetricsComparer:
    """Allows the comparison between different metrics such as NPath and APC."""

    def __init__(self, results: List[List[Union[str, int]]],
                 location: str) -> None:
        """
        Create a new MetricsComparer object from a list of results.

        Input results list of tuples, each being:
            (Cyclomatic Complexity, NPATH Complexity,
            APC Class, Largest Big-O APC term, APC Expression)

        then, create dictionaries with (key, value) pairs given by
            1. (cyclomatic complexity, path complexity)
            2. (npath complexity, path complexity)
            3. (path complexity, cyclomatic complexity)
            4. (path complexity, npath)
        """
        self.location = location
        self.results = results

        # Classify by cyclomatic complexity -> path complexity.
        dict_one: MetricsDictOne = defaultdict(list)

        # Classify by npath complexity -> path complexity.
        dict_two: MetricsDictOne = defaultdict(list)

        # Classify by path complexity -> cyclomatic complexity.
        dict_three: MetricsDictTwo = defaultdict(list)

        # Classify by path complexity -> npath.
        dict_four: MetricsDictTwo = defaultdict(list)

        self.cyclomatic_complexities = []
        self.npath_complexities = []
        self.path_complexities = []

        self.dicts: Tuple[MetricsDictOne, MetricsDictOne,
                          MetricsDictTwo, MetricsDictTwo] = \
            (dict_one, dict_two, dict_three, dict_four)
        self.dict_counter: List[CountingDict] = []

        for res in results:
            cyc_compl = int(res[1])
            npath_compl = int(res[2])
            path_compl = str(res[4])
            dict_one[cyc_compl] += [path_compl]
            dict_two[npath_compl] += [path_compl]
            dict_three[path_compl] += [cyc_compl]
            dict_four[path_compl] += [npath_compl]
            self.cyclomatic_complexities += [cyc_compl]
            self.npath_complexities += [npath_compl]
            self.path_complexities += [npath_compl]

    def update_graphs(self) -> None:
        """Update dictionaries."""
        # Convert APCs to correct complexity classes.
        temp_dict: MetricsDictOne = defaultdict(list)
        temp_dicts: List[MetricsDictOne] = []
        temp_dicts2: List[MetricsDictTwo] = []
        for metrics_dict in self.dicts[:2]:
            for key in metrics_dict.keys():
                temp_dict[key] = []
                # temp_dict[key] = list(map(classify, self.dicts[i][key]))
            temp_dicts.append(temp_dict)

        temp_dict_2: MetricsDictTwo = defaultdict(list)
        for metrics_dict2 in self.dicts[2:]:
            for metrics_key in metrics_dict2.keys():
                temp_dict_2[metrics_key] = []
                # temp_dict[classify(key)] = self.dicts[i][key]
            temp_dicts2.append(temp_dict_2)

        self.dicts = (temp_dicts[0], temp_dicts[1], temp_dicts2[0], temp_dicts2[1])

    def compute_metric(self, use_frequencies: bool = True) -> None:
        """Calculate the metrics used to compare APC to Cyclomatic Complexity and NPATH."""
        self.update_graphs()
        # self.aggregate()

        average_class_sizes = [0.] * 4
        if self.dict_counter is None or len(self.dict_counter) < 4:
            print("self.dict_counter is incorrect.")
            return

        for i in range(0, 4):
            average_class_sizes[i] = average_class_size(self.dict_counter[i], use_frequencies)
        cyc_to_aoc, apc_to_cyc, npath_to_apc, apc_to_npath = average_class_sizes

        if cyc_to_aoc == apc_to_cyc:
            r_one = 0.
        else:
            r_one = (cyc_to_aoc + apc_to_cyc) / (cyc_to_aoc - apc_to_cyc)

        if npath_to_apc == apc_to_npath:
            r_two = 0.
        else:
            r_two = (npath_to_apc + apc_to_npath) / (npath_to_apc - apc_to_npath)

        print(f"APC to Cyclomatic: {cyc_to_aoc}, \
              apc_to_cyc: {apc_to_cyc}", self.location)
        print(f"APC to Cyclomatic: {npath_to_apc}, \
              apc_to_npath: {apc_to_npath}", self.location)
        print(f"APC to Cyclomatic: {r_one}, \
              APC vs NPATH: {r_two}", self.location)
