"""Compute aggregate metrics and compare them."""

from typing import List, Dict, Any, Optional
from math import log
import os
import logging
from collections import defaultdict, Counter
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore


def adjusted_rand_index(function_list: List[Any]) -> float:
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
    for func_one, func_one_index in enumerate(function_list):
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


def average_class_size(input_dict, use_frequencies: bool) -> float:
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
        entropy_value = 0

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


def mutual_information(cluster_list_one, cluster_list_two) -> float:
    """
    Calculate I(cluster_list_one, cluster_list_two).

    @see https://en.wikipedia.org/wiki/Mutual_information
    """
    cond_entropy = 0.
    # Obtain the total size
    # TODO: is this supposed to be cluster_list_one?
    total_size = get_total_size(cluster_list_one)

    # Create a table of all the overlaps
    overlaps: List[List[Any]] = [[[0] for i in range(len(cluster_list_one))]
                                 for j in range(len(cluster_list_two))]
    for i, cluster_one in enumerate(cluster_list_one):
        for j, cluster_two in enumerate(cluster_list_two):
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


def get_total_size(dictionary: Dict[Any, Any]) -> int:
    """Get the sum of lengths of all values in a dictionary."""
    total_size = 0
    for cluster in dictionary:
        total_size += len(dictionary[cluster])

    return total_size


def cluster_entropy(cluster_list) -> float:
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


def entropy(probabilities: List[float]) -> float:
    """
    Return the total entropy of a list representing probability distributions.

    Input: [p_0, p_1, ..., p_n]
    Output: H(p)
    """
    # Check that it is a valid probability distribution.
    if sum(probabilities) != 1:
        raise ValueError("Not a valid probability distribution - does not sum to one.")

    total_entropy = 0.
    for probability in probabilities:
        total_entropy -= probability * log(probability, 2)

    return total_entropy


def check_argument_errors(params) -> None:
    """Throws a ValueError if the set of command line arguments given by the user are invalid."""
    if os.path.isdir(params.getFilepath()):
        if params.getStatsMode():
            raise ValueError("StatsComputer takes a CSV file of results.")

        if params.getRecursive():
            raise ValueError("Recursive mode only applies to directories.")


def log_class_sizes(cyc_to_aoc: float,
                    apc_to_cyc: float,
                    npath_to_apc: float,
                    apc_to_npath: float) -> None:
    """Write the average class size for each metric to the log file."""
    logging.info(f"cyc_to_aoc: {str(cyc_to_aoc)}")
    logging.info(f"apc_to_cyc: {str(apc_to_cyc)}")
    logging.info(f"npath_to_apc: {str(npath_to_apc)}")
    logging.info(f"apc_to_npath: {str(apc_to_npath)}\n")


def joint_entropy(cluster_list_one, cluster_list_two) -> float:
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

    for cluster_one in cluster_list_one:
        for cluster_two in cluster_list_two:
            # Calculate the elements in common between both clusters
            cluster_overlap = len(cluster_one.intersection(cluster_two))
            result -= (cluster_overlap / total_size) * \
                log((cluster_overlap / total_size), 2)

    return result


def conditional_entropy(cluster_list_one, cluster_list_two) -> float:
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
    overlaps: List[List[Any]] = [[[0] for i in range(len(cluster_list_one))]
                                 for j in range(len(cluster_list_two))]
    for i, cluster_one in enumerate(cluster_list_one):
        for j, cluster_two in enumerate(cluster_list_two):
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


class MetricsComparer:
    """Allows the comparison between different metrics such as NPath and APC."""

    def __init__(self, results, location) -> None:
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
        dict_one: Dict[Any, Any] = defaultdict(list)

        # Classify by npath complexity -> path complexity.
        dict_two: Dict[Any, Any] = defaultdict(list)

        # Classify by path complexity -> cyclomatic complexity.
        dict_three: Dict[Any, Any] = defaultdict(list)

        # Classify by path complexity -> npath.
        dict_four: Dict[Any, Any] = defaultdict(list)

        self.cyclomatic_complexities = []
        self.npath_complexities = []
        self.path_complexities = []

        self.dicts: List[Dict[Any, Any]] = [dict_one, dict_two, dict_three, dict_four]
        self.dict_counter: Optional[List[Dict[Any, Any]]] = None

        for res in results:
            cyc_compl = res[1]
            npath_compl = res[2]
            path_compl = res[4]
            dict_one[cyc_compl] += [path_compl]
            dict_two[npath_compl] += [path_compl]
            dict_three[path_compl] += [cyc_compl]
            dict_four[path_compl] += [npath_compl]
            self.cyclomatic_complexities += [cyc_compl]
            self.npath_complexities += [npath_compl]
            self.path_complexities += [npath_compl]

    def log_dicts(self) -> None:
        """Log the dictionaries mapping between complexity metrics to the log file."""
        logging.info("C to APC: ----- " + str(self.dicts[0]))
        logging.info("NPATH to APC: ----- " + str(self.dicts[1]))
        logging.info("APC to C: ------ " + str(self.dicts[2]))
        logging.info("APC to NPATH: ------ " + str(self.dicts[3]) + "\n")

    def compute_metric(self, use_frequencies: bool = True) -> None:
        """Calculate the metrics used to compare APC to Cyclomatic Complexity and NPATH."""
        self.log_dicts()

        # Convert APCs to correct complexity classes.
        temp_dict: Dict[Any, Any] = dict()
        for i in range(0, 2):
            for key in self.dicts[i].keys():
                temp_dict[key] = []
                # temp_dict[key] = list(map(classify, self.dicts[i][key]))
            self.dicts[i] = temp_dict

        temp_dict = dict()
        for i in range(2, 4):
            for key in self.dicts[i].keys():
                temp_dict[key] = []
                # temp_dict[classify(key)] = self.dicts[i][key]
            self.dicts[i] = temp_dict

        self.log_dicts()
        self.aggregate()
        self.log_dicts()

        average_class_sizes = [0.] * 4
        if self.dict_counter is None or len(self.dict_counter) < 4:
            print("self.dict_counter is incorrect.")
            return

        for i in range(0, 4):
            average_class_sizes[i] = average_class_size(self.dict_counter[i], use_frequencies)
        cyc_to_aoc, apc_to_cyc, npath_to_apc, apc_to_npath = average_class_sizes

        log_class_sizes(*average_class_sizes)

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

    def aggregate(self) -> None:
        """
        Count the number of differences between different metrics.

        Iterate through all of the of the dictionaries where each dictionary has
        key value pairs of one of the types:

        (Cyclomatic, APC Complexities), (NPATH, APC Complexities),
        (APC, Cyclomatic Complexities), (APC, NPATH Complexities)

        and creates a dictionary with the same key that maps to the number of different
        complexities (e.g. (Cyclomatic, len(APC Complexities)))
        """
        if self.dicts is None:
            raise ValueError("Empty dictionary.")

        self.dict_counter = self.dicts

        for dictionary in self.dict_counter:
            for key in dictionary.keys():
                dictionary[key] = Counter(dictionary[key])

    def show_plot(self) -> None:
        """Create a histogram for distributions of Cyc. Complexity and NPath over all functions."""
        plt.subplot(2, 1, 1)

        mean = np.mean(self.cyclomatic_complexities)
        std = np.std(self.cyclomatic_complexities)
        plt.hist(self.cyclomatic_complexities, bins=100, label=f"Mean: {mean}\n StdDev: {std}")
        plt.title("Cyclomatic Complexity Distribution")
        plt.ylabel("Counts")
        plt.xlabel("Cyclomatic Complexity")
        plt.legend(loc='upper left')

        plt.subplot(2, 1, 2)
        mean = np.mean(self.npath_complexities)
        std = np.std(self.npath_complexities)
        plt.hist(self.npath_complexities, bins=100, label=f"Mean: {mean}\n StdDev: {std}")
        plt.title("NPath Distribution")
        plt.ylabel("Counts")
        plt.xlabel("NPath Complexity")
        plt.legend()
        plt.show()

    @staticmethod
    def from_csv(file_name: str, location: str) -> Any:
        """
        Create a MetricsComparer object from a results CSV file.

        Tihs generates the MetricsComparer by obtaining the relevant entries from each line.
        Expected file format:

        test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class,
            path_cplxty_asym, path_cplxty
        """
        results: List[Any] = []
        with open(file_name, "r") as file:
            content = file.readlines()[1:]
            for line in content:
                try:
                    file_path = line.strip().split(",")[1]
                    # Don't need ID
                    result: List[Any] = line.strip().split(",")[2:]
                    result = [file_path] + [result[0]] + [result[1]] + result[2:]
                    results.append(result)
                except (IndexError, ValueError) as _:
                    pass

        return MetricsComparer(results, location)
