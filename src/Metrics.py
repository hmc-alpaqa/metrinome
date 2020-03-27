"""
Metrics is used to compute aggregate metrics and compare them.
"""

from typing import List, Dict, Any
from math import log
import os
import argparse
import logging
from collections import defaultdict, Counter
from multiprocessing import Pool
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
import glob2  # type: ignore
from graph import Graph
from utils import round_expression, classify, Timeout

NUM_PROCESSES = 4


def adjusted_rand_index(function_list) -> float:
    """
    Compute the adjusted rand index, used to compare two different
    clusterings on a set by looking at all oft he possible pairs of
    points in the set.
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


def average_class_size(input_dict, use_frequencies: bool):
    """
    Given some dictionary with key-value pairs
        (Metric1, Metric2),
    where given some value 'x' for Metric1, the dictionary
    will map to all values Metric2 takes on for the set
    of functions that took on value 'x' for Metric1
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

        # If we only have a single value, then the disbrituion is perfectly uniform
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
    Calculate I(cluster_list_one, cluster_list_two)

    @see https://en.wikipedia.org/wiki/Mutual_information
    """
    cond_entropy = 0
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


def get_total_size(dictionary: Dict[Any, Any]):
    """
    Given a dictionary that maps to something that has
    a 'length', sum up all of the lengths in the dictionary.
    """
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


def entropy(probabilities) -> float:
    """
    Given some list representing a probability distribution, return the total entropy
    Input: [p_0, p_1, ..., p_n]
    Output: H(p)
    """
    # Check that it is a valid probability distribution.
    if sum(probabilities) != 1:
        raise ValueError("Not a valid probability distribution - does not sum to one.")

    total_entropy = 0
    for probability in probabilities:
        total_entropy -= probability * log(probability, 2)

    return total_entropy


def check_argument_errors(params):
    """Throws a ValueError if the set of command line arguments given by the user are invalid."""
    if os.path.isdir(params.getFilepath()):
        if params.getStatsMode():
            raise ValueError("StatsComputer takes a CSV file of results.")

        if params.getRecursive():
            raise ValueError("Recursive mode only applies to directories.")


def set_logging(args) -> None:
    """Configure logging according to the parameters specified by user."""
    logfile = args['logfile']
    if args['log']:
        if logfile is not None:
            # Will append to existing file by default
            logging.basicConfig(filename=logfile, level=logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)


def get_file_list(file_path: str, recursive: bool) -> List[str]:
    """
    Obtain a list of the paths to all .dot files from an initial file path.
    Recursive mode will enable searching in subdirectories.
    """
    if os.path.isdir(file_path):
        if recursive:
            # recursive glob '**' operator matches 0 or more subdirectories
            file_list = glob2.glob(os.path.join(file_path, "**/*.dot"), recursive=True)
        else:
            file_list = glob2.glob(os.path.join(file_path, "*.dot"), recursive=False)
    else:
        file_list = [file_path]

    return file_list


def log_class_sizes(cyc_to_aoc, apc_to_cyc, npath_to_apc, apc_to_npath) -> None:
    """Write the average class size for each metric to the log file."""
    logging.info(f"cyc_to_aoc: {str(cyc_to_aoc)}")
    logging.info(f"apc_to_cyc: {str(apc_to_cyc)}")
    logging.info(f"npath_to_apc: {str(npath_to_apc)}")
    logging.info(f"apc_to_npath: {str(apc_to_npath)}\n")


def create_argument_parser():
    """Create a parser to read command line arguments from the user."""
    parser = argparse.ArgumentParser(description="")

    recur_desc = "Recursive Mode: look for .dot files in all subfolders"
    stats_desc = "Compute the metric for a given input file"
    log_desc = "Print logging information to STD_OUT"
    logf_desc = "Specify a file that logging information \
                 will be written to (instead of STD_OUT)"

    parser.add_argument('-f', '--filename', help="Input filename", required=True)
    parser.add_argument('-r', '--recursive', help=recur_desc,
                        action="store_true", required=False)
    parser.add_argument('-o', '--output', help="Set an output file", required=False)
    parser.add_argument('-s', '--statistics', help=stats_desc,
                        action="store_true", required=False)
    parser.add_argument('-l', '--log', help=log_desc, action="store_true", required=False)
    parser.add_argument('--logfile', help=logf_desc, required=False)
    return parser


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
        Input results list of tuples, each being:
            (Cyclomatic Complexity, NPATH Complexity,
            APC Class, Largest Big-O APC term, APC Expression)

        Creates a new MetricsComparer object from a list of results, creating dictionaries
        with (key, value) pairs given by
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

        self.dicts = [dict_one, dict_two, dict_three, dict_four]
        self.dict_counter = None

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
        temp_dict = dict()
        for i in range(0, 2):
            for key in self.dicts[i].keys():
                temp_dict[key] = list(map(classify, self.dicts[i][key]))
            self.dicts[i] = temp_dict

        temp_dict = dict()
        for i in range(2, 4):
            for key in self.dicts[i].keys():
                temp_dict[classify(key)] = self.dicts[i][key]
            self.dicts[i] = temp_dict

        self.log_dicts()
        self.aggregate()
        self.log_dicts()

        average_class_sizes = [0] * 4
        if self.dict_counter is None or len(self.dict_counter) < 4:
            write_output("self.dict_counter is incorrect.")
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

        write_output(f"APC to Cyclomatic: {cyc_to_aoc}, \
                    apc_to_cyc: {apc_to_cyc}", self.location)
        write_output(f"APC to Cyclomatic: {npath_to_apc}, \
                    apc_to_npath: {apc_to_npath}", self.location)
        write_output(f"APC to Cyclomatic: {r_one}, \
                    APC vs NPATH: {r_two}", self.location)

    def aggregate(self):
        """
        Iterate through all of the of the dictionaries where each dictionary has
        key value pairs of one of the types:

        (Cyclomatic, APC Complexities), (NPATH, APC Complexities),
        (APC, Cyclomatic Complexities), (APC, NPATH Complexities)

        and creates a dictionary with the same key that maps to the number of different
        complexities (e.g. (Cyclomatic, len(APC Complexities)))
        """
        self.dict_counter = self.dicts
        for dictionary in self.dict_counter:
            for key in dictionary.keys():
                dictionary[key] = Counter(dictionary[key])

    def show_plot(self) -> None:
        """
        Create a histogram for both the distribution of Cyclomatic Complexity and NPATH
        over all of the functions.
        """
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
    def from_csv(file_name, location):
        """
        Create a MetricsComparer object from a results CSV file by
        obtaining the relevant entries from each line.
        Expected file format:

        test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class,
            path_cplxty_asym, path_cplxty
        """
        results = []
        with open(file_name, "r") as file:
            content = file.readlines()[1:]
            for line in content:
                try:
                    file_path = line.strip().split(",")[1]
                    # Don't need ID
                    result = line.strip().split(",")[2:]
                    result = [file_path] + [float(result[0])] + [float(result[1])] + result[2:]
                    results.append(result)
                except (IndexError, ValueError) as _:
                    pass

        return MetricsComparer(results, location)


class Main():
    """
    Handles obtaining parameters from the user, computing the
    Path Complexity, Cyclomatic Complexity, and NPATH metrics for all
    .dot files, and calling the MetricsComparer to compare the 3 metrics
    if specified.
    """
    def __init__(self) -> None:
        """
        Get the command line arguments from the user and verify that they are valid
        """
        # Get command line arguments
        parser = create_argument_parser()
        args = vars(parser.parse_args())

        # params = Parameters(args['filename'], args['recursive'],
        #  args['output'], args['statistics'])

        # file_path     = params.getFilepath()
        # recursive     = params.getRecursive()
        # self.location = params.getOutputFile()
        # stats_mode    = params.getStatsMode()

        file_path = "tmp"
        recursive = False
        self.location = "tmp"
        stats_mode = "tmp"

        set_logging(args)
        # self.check_argument_errors(params)
        file_list = get_file_list(file_path, recursive)

        if stats_mode:
            self.compute_statistics(file_list[0])
        else:
            self.compute_results(file_list)

    def compute_result(self, file_name: str):
        """
        Given a single file dot file, compute all metrics.

        The metrics computed are: APC, Path Complexity, Cyclomatic Complexity, and NPATH.
        """
        digits = 2
        graph = Graph.from_file(file_name)
        write_output(f"Working on {file_name}", self.location)
        with Timeout(seconds=10, error_message="Timeout"):
            # npath_compl = n_path_complexity(graph)
            pass

        # TODO
        # path_complexity_result = path_complexity(graph)
        path_complexity_result = ("0", "0")
        asymptotic_complexity = path_complexity_result[0]
        full_path_complexity = path_complexity_result[1]

        def cyclomatic_complexity(tmp):
            return 0

        n_path_compl = "tmp"
        return (file_name, cyclomatic_complexity(graph), n_path_compl,
                classify(asymptotic_complexity, "n"),
                round_expression(asymptotic_complexity, digits),
                round_expression(full_path_complexity, digits))

    def compute_statistics(self, file_name: str) -> None:
        """
        Given a CSV file with all of the results given by 'compute_results,'
        calculate the metrics used to compare APC, NPATH, and Cyclomatic
        Complexity.
        """
        metrics = MetricsComparer.from_csv(file_name, self.location)
        metrics.compute_metric()

    def compute_results(self, filelist) -> None:
        """
        Given a list of .dot files, compute the metrics and save the output for all files.

        The metrics are Cyclomatic Complexity, NPATH Complexity, and Path Complexity.
        The output can be written to a file or standard out.
        """
        write_output("test_number, cfg_file, cyclomatic_complexity, npath_complexity, \
                     path_cplxty_class, path_cplxty_asym, path_cplxty", self.location)

        split_file_list: List[Any] = [[] for _ in range(NUM_PROCESSES)]
        for file_index, file in enumerate(filelist):
            split_file_list[file_index % len(split_file_list)].append(file)

        proc_pool = Pool(processes=NUM_PROCESSES)
        results = proc_pool.imap_unordered(self.threadpool_mapper, split_file_list)
        proc_pool.close()
        proc_pool.join()

        for result in results:
            if len(result) != 0:
                write_output("\n".join(list(map(lambda x: str(x)[1:-1], result))), self.location)

    def threadpool_mapper(self, file_names):
        """
        Maps compute_result over a set of file names.
        """
        return list(map(self.compute_result, file_names))


def write_output(msg, location=None):
    """
    Write a String to STDOUT or a file if specified
    """
    if location is None:
        print(msg)
    else:
        if os.path.isfile(location):
            with open(location, 'w') as file:
                file.write(msg)
