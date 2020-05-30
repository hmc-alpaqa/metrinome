"""This module tests that we can convert C++ to Graph objects representing its CFG."""

import unittest
import sys
import warnings
sys.path.append("/app/code/")


def ignore_warnings(test_func):
    """For warnings generated by third party code."""
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            test_func(self, *args, **kwargs)
    return do_test


class TestCPPConvert(unittest.TestCase):
    """All tests for the object that converts arbitrary C++ code to Graph objects."""

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

    # @ignore_warnings  # glob2 regex use is deprecated.
    # def test_to_graph(self):
    #     """Check that it returns the correct graphs."""
    #     converter = CPPConvert(Log(log_level=LogLevel.DEBUG))

    #     graph1 = Graph([], set([0, 1]), 0, 1)
    #     graph2 = converter.to_graph("/app/code/tests/cppFiles/blank", ".cpp")
    #     self.assertTrue('blank0' in graph2.keys())
    #     graph2 = graph2['blank0']
    #     self.assertEqual(graph1, graph2)

    #     graph3 = Graph([[0, 1], [0, 2], [1, 5], [2, 3], [2, 4], [3, 5], [4, 6]],
    #                    set([0, 1, 2, 3, 4, 5, 6]), 0, 5)
    #     graph4 = converter.to_graph("/app/code/tests/cppFiles/names", ".cpp")['names0']
    #     self.assertEqual(graph3, graph4)

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
