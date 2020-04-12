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
from metric import npath_complexity
from tests import utils


def npath_runtime():
    """Test the amount of time it takes to run NPath analysis on different sized graphs."""
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
        converter = npath_complexity.NPathComplexity()
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
    converter = npath_complexity.NPathComplexity()
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
# npath_runtime()

# LIST VERSION
# takes 769 seconds to run commons-scxml-0.9/\
#  org_apache_commons_scxml_io_ModelUpdater_updateState_0_basic.dot
# takes very long time to run (interrupted)
#  commons-el/org_apache_commons_el_parser_ELParserTokenManager_jjMoveNfa_1_0_basic

# [('/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/',
# [('maximum', 761.1939623355865), ('minimum', 1.5974044799804688e-05),
#  ('mean', 1.243410007573106), ('median', 2.8133392333984375e-05),
# ('stdev', 30.719201297648244), ('variance', 943.6693283654334)],
# [(761.1939623355865, '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/\
#   org_apache_commons_scxml_io_ModelUpdater_updateState_0_basic.dot')]),
#
# ('/app/examples/cfgs/apache_cfgs/commons-net-3.3/',
# [('maximum', 1.8467767238616943), ('minimum', 1.52587890625e-05),
#  ('mean', 0.0024753327639597767), ('median', 2.7418136596679688e-05),
# ('stdev', 0.05581999264575899), ('variance', 0.0031158715789725874)],
# [(0.19144272804260254, '/app/examples/cfgs/apache_cfgs/commons-net-3.3/\
#   org_apache_commons_net_nntp_Threader_buildContainer_0_basic.dot'),
# (0.15853095054626465, '/app/examples/cfgs/apache_cfgs/commons-net-3.3/\
#   org_apache_commons_net_ftp_FTPClient__openDataConnection__0_basic.dot'),
# (1.8467767238616943, '/app/examples/cfgs/apache_cfgs/commons-net-3.3/\
#   org_apache_commons_net_nntp_Threader_gatherSubjects_0_basic.dot'),
# (0.8057589530944824, '/app/examples/cfgs/apache_cfgs/commons-net-3.3/\
#   org_apache_commons_net_nntp_Article_simplifySubject_0_basic.dot')]),

# ('/app/examples/cfgs/apache_cfgs/commons-codec-1.10/',
# [('maximum', 2.396879196166992), ('minimum', 1.6450881958007812e-05),
#  ('mean', 0.007770059132339931), ('median', 2.8848648071289062e-05),
#  ('stdev', 0.11268775999944443), ('variance', 0.012698531253692387)],
# [(0.38344335556030273, '/app/examples/cfgs/apache_cfgs/commons-codec-1.10/\
#   org_apache_commons_codec_language_ColognePhonetic_colognePhonetic_0_basic.dot'),
# (0.6730148792266846, '/app/examples/cfgs/apache_cfgs/commons-codec-1.10/\
#   org_apache_commons_codec_digest_Sha2Crypt_sha2Crypt_0_basic.dot'),
# (0.28722405433654785, '/app/examples/cfgs/apache_cfgs/commons-codec-1.10/\
#   org_apache_commons_codec_language_DaitchMokotoffSoundex_soundex_0_basic.dot'),
# (2.396879196166992, '/app/examples/cfgs/apache_cfgs/commons-codec-1.10/\
#   org_apache_commons_codec_language_Metaphone_metaphone_0_basic.dot')]),
#
# ('/app/examples/cfgs/apache_cfgs/commons-compress-1.9/',
# [('maximum', 33.450133085250854), ('minimum', 1.621246337890625e-05),
#  ('mean', 0.025039534869780177), ('median', 3.0994415283203125e-05),
# ('stdev', 0.8640603369239266), ('variance', 0.7466002658450895)],
# [(2.0845611095428467, '/app/examples/cfgs/apache_cfgs/commons-compress-1.9/\
#   org_apache_commons_compress_compressors_bzip2_BZip2CompressorOutputStream\
#   _hbMakeCodeLengths_0_basic.dot'),
# (33.450133085250854, '/app/examples/cfgs/apache_cfgs/commons-compress-1.9/\
#   org_apache_commons_compress_compressors_bzip2_BlockSort_mainSort_0_basic.dot')])]

# /app/examples/cfgs/apache_cfgs/commons-el/ (50%)
# [('maximum', 8.366817712783813), ('minimum', 1.6927719116210938e-05),
# ('mean', 0.03202365672410424), ('median', 3.993511199951172e-05),
# ('stdev', 0.5110567798863105), ('variance', 0.26117903226776484)]
