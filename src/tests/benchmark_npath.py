"""
This file allows us to compare different implementations of the npath computation algorithm.

For example, we could use any of the representations of graphs (adjacency list / matrix) and
compute npath recursively, recursively using memoization, or iteratively through dynamic
programming.
"""

import sys
sys.path.append("/app/code/")
sys.path.append("/app/code/metric")
from log import Log
from metric import npath_complexity
from tests import unit_utils
from graph import Graph
from graph import GraphType


def npath_runtime(graph_type):
    """Test the amount of time it takes to run NPath analysis on different sized graphs."""
    log = Log()
    converter = npath_complexity.NPathComplexity(log)
    unit_utils.run_benchmark(converter, graph_type)


def main():
    """Execute the tests."""
    # create instance of the npath class
    converter = npath_complexity.NPathComplexity()
    base_path = "/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/org_apache_commons_"
    graph_zero = Graph.from_file(f"{base_path}scxml_io_SCXMLParser_addIfRules_0_basic.dot",
                                 False, GraphType.ADJACENCY_LIST)
    graph_one = Graph.from_file(f"{base_path}scxml_io_SCXMLParser_addIfRules_0_basic.dot",
                                False, GraphType.EDGE_LIST)
    graph_two = Graph.from_file(f"{base_path}scxml_io_SCXMLParser_addIfRules_0_basic.dot",
                                False, GraphType.ADJACENCY_MATRIX)
    print("list version:")
    print(converter.evaluate(graph_zero))
    print("dict version:")
    print(converter.evaluate(graph_one))
    print("matrix version:")
    print(converter.evaluate(graph_two))


if __name__ == "__main__":
    npath_runtime(GraphType.EDGE_LIST)
# main()


# LIST VERSION
# [('maximum', 0.010824441909790039), ('minimum', 3.647804260253906e-05),
#  ('mean', 0.000350918651612337), ('median', 0.00011205673217773438),
#  ('stdev', 0.0012025774397812876)]
# OUTLIERS:
# [(0.0076601505279541016, '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/',
#  '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/
#    org_apache_commons_scxml_io_SCXMLSerializer_serializeState_0_basic.dot'),
# (0.010824441909790039, '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/',
#  '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/
#    org_apache_commons_scxml_model_Executable_setParent_0_basic.dot')]

# DICT VERSION
# [('maximum', 0.007207632064819336), ('minimum', 4.1961669921875e-05),
#  ('mean', 0.00024523813862445924), ('median', 0.00011181831359863281),
#  ('stdev', 0.0006659859955008892)]
# OUTLIERS:
# [(0.007207632064819336, '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/',
#  '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/
#   org_apache_commons_scxml_io_SCXMLSerializer_serializeState_0_basic.dot')]

# MATRIX VERSION
# [('maximum', 0.00739598274230957), ('minimum', 4.9591064453125e-05),
#  ('mean', 0.00026635296088604887), ('median', 0.00012946128845214844),
#  ('stdev', 0.0006942695049296839)]
# OUTLIERS:
# [(0.0020546913146972656, '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/',
#  '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/
#    org_apache_commons_scxml_env_SimpleErrorReporter_onError_0_basic.dot'),
# (0.00739598274230957, '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/',
#  '/app/examples/cfgs/apache_cfgs/commons-scxml-0.9/
#    org_apache_commons_scxml_io_SCXMLSerializer_serializeState_0_basic.dot')]

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
