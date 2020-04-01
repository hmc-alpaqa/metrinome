"""Test all methods associated with computing NPath complexity."""

import unittest
from graph import Graph


class TestNPATH(unittest.TestCase):
    """Test the the class able to compute the NPath metric for an arbitrary graph."""

    def test_npath(self):
        """
        Check NPath with actual CFGs obtained from Java code.

        Expected Results:

        test_number, cfg_file, cyclomatic_complexity, npath_complexity,
            path_cplxty_class, path_cplxty_asym, path_cplxty
        1,/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test1_0_basic.dot,4,8,Constant,8.,8.
        2,/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test2_0_basic.dot,4,4,Constant,4.,4.
        3,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test3_0_basic.dot,4,8,
            Polynomial,0.04*n^3.,5. + 3.08*n + 0.62*n^2. + 0.04*n^3.
        4,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test4_0_basic.dot,4,4,
            Exponential,1.9000000000000001*1.8^(0.5*n),1. + 0.04*0.45^(0.5*n) +
            0.56*1.25^(0.5*n) + 1.9000000000000001*1.8^(0.5*n)
        5,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test5_0_basic.dot,4,4,
            Exponential,1.9000000000000001*1.8^(0.5*n),1. + 0.04*0.45^(0.5*n) +
            0.56*1.25^(0.5*n) + 1.9000000000000001*1.8^(0.5*n)
        6,/cfgs/simple_test_cfgs/vlab_cs_ucsb_test_SimpleExample_test6_0_basic.dot,4,8,
            Polynomial,0.02*n^3.,4. + 2.17*n + 0.38*n^2. + 0.02*n^3.
        """
        path_to_cfgs = "todo"
        base_path = f"{path_to_cfgs}/cfgs/simple_test_cfgs/"
        prefix = "vlab_cs_ucsb_test_SimpleExample_test"

        results = []
        for file_index in range(1, 7):
            file = base_path + prefix + str(file_index) + "_0_basic.dot"
            graph = Graph.from_file(file)
            print("The Graph is: " + str(graph))
            res = "todo"
            # res = NPathComplexity.nPathComplexity(graph)
            results.append(res)

        expected_results = [8, 4, 8, 4, 4, 8]
        self.assertEqual(results, expected_results)

    def test_npath_single_node(self):
        """
        Check NPath for single-node Graph.

        Verify that the NPath complexity code works for a graph with a
        single node. The start node is equal to the end node,
        so there is a single path from the beginning to the end.
        """
        graph = Graph([], set([0]), 0, 0)
        result = "todo"
        print(graph)
        # result = NPathComplexity.nPathComplexity(graph)
        expected_result = 1
        self.assertEqual(result, expected_result)

    def test_npath_no_edges(self):
        """
        Check NPath in the case with no edges.

        Verify that the NPATH complexity for a graph with different start
        and end nodes but no edges is 0, since there are no paths from the
        beginning to the end.
        """
        graph = Graph([], set([0, 1]), 0, 1)
        result = "todo"
        print(graph)
        # result = NPathComplexity.nPathComplexity(graph)
        expected_result = 0
        self.assertEqual(result, expected_result)
