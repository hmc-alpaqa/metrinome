"""This module tests that we can convert C++ to Graph objects representing its CFG."""

import os
import unittest

from core.env import Env
from core.log import Log, LogLevel
from graph.control_flow_graph import ControlFlowGraph
from graph.graph import AdjListGraph
from lang_to_cfg.cpp import CPPConvert
from tests.unit_utils import get_test_graph


class TestCPPConvert(unittest.TestCase):
    """All tests for the object that converts arbitrary C++ code to Graph objects."""

    # @ignore_warnings  # glob2 regex use is deprecated.
    def test_to_graph(self) -> None:
        """Check that it returns the correct graphs."""
        converter = CPPConvert(Log(log_level=LogLevel.REGULAR))
        self.assertEqual(converter.name(), "CPP")
        Env.clean_temps()
        graph1 = AdjListGraph([[0, 1], [1, 2]], 3)
        result = converter.to_graph("/app/code/tests/cppFiles/blank", ".cpp")
        self.assertTrue(len(os.listdir(Env.TMP_DOT_PATH)) == 0)
        self.assertTrue(len(os.listdir(Env.TMP_PATH)) == 0)
        self.assertIsNotNone(result)
        if result is not None:
            self.assertTrue("blank_cfg.main.dot" in result)
            self.assertEqual(graph1, result['blank_cfg.main.dot'].graph)

        expected_graph = ControlFlowGraph(get_test_graph())
        graphs = converter.to_graph("/app/code/tests/cppFiles/names", ".cpp")

        # Need to check all graphs since order can vary with environment.
        graph_names = ['names_cfg.main.dot']
        self.assertIsNotNone(graphs)
        if graphs is not None:
            obtained_graphs = [graphs[graph_name].graph for graph_name in graph_names]
            self.assertTrue(expected_graph == res for res in obtained_graphs)

    # @ignore_warnings  # glob regex deprecation warnings.
    # def test_create_dot_files(self):
    #     """Test that it creates a folder for the files."""
    #     count1 = len(glob2.glob("/app/code/tests/cppFiles/*"))
    #     converter = CPPConvert(Log())
    #     converter.create_dot_files("/app/code/tests/cppFiles/blank", ".cpp")
    #     count2 = len(glob2.glob("/app/code/tests/cppFiles/*"))
    #     self.assertEqual(count1 + 1, count2)

    #     temp_folder = "/app/code/tests/cppFiles/cppConverterTemps"
    #     orig_dir = glob2.glob("/app/code/tests/cppFiles/*")
    #     self.assertIn(temp_folder, orig_dir)

    #     # Affirm that dot files are indeed inside the folder
    #     temp_contents = glob2.glob("/app/code/tests/cppFiles/cppConverterTemps/*.dot")
    #     self.assertNotEqual(len(temp_contents), 0)
    #     converter.clean_temps()

    # @ignore_warnings
    # def test_convert_to_standard_format(self):
    #     """Affirm converted files are in standard format (use tempfiles)."""
    #     converter = CPPConvert(Log())
    #     os.chdir("cppFiles")
    #     with open("standardFormat.txt", "r") as standard_format:
    #         subprocess.check_call(["mkdir", "-p", "cppConverterTemps"])
    #         subprocess.call(["cp", "nonStandardFormat.txt",
    #                          "cppConverterTemps/nonStandardFormat.dot"])
    #         converter.convert_to_standard_format("/app/code/tests/cppFiles/nonStandardFormat")
    #         with open("cppConverterTemps/nonStandardFormat0.dot", "r") as converted_format:
    #             self.assertEqual(standard_format.readlines(), converted_format.readlines())
    #     converter.clean_temps()

    # @ignore_warnings
    # def test_clean_temps(self):
    #     """Test that clean_temps() deletes the temp directory."""
    #     converter = CPPConvert(None)
    #     # Create temp directory
    #     subprocess.check_call(["mkdir", "-p", "cppConverterTemps"])
    #     temp_folder = "/app/code/tests/cppConverterTemps"
    #     orig_dir = glob2.glob("/app/code/tests/*")
    #     self.assertIn(temp_folder, orig_dir)
    #     converter.clean_temps()
    #     orig_dir = glob2.glob("/app/code/tests/*")
    #     self.assertNotIn(temp_folder, orig_dir)


if __name__ == '__main__':
    unittest.main()
