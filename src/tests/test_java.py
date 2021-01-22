"""Test the conversion of Java source code to Graph objects representing its CFG."""
import os
import unittest

from core.env import Env
from core.log import Log
from graph.graph import EdgeListGraph
from lang_to_cfg.java import JavaConvert


class TestJavaConvert(unittest.TestCase):
    """All of the tests to verify that we can convert Java source code to Graph objects."""

    def setUp(self) -> None:
        """Initialize a logger before running each test."""
        self.logger = Log(display_output=False)

    def test_run_cmd(self) -> None:
        """
        Check that running commands works.

        Runcmd should never throw an error, even when the command doesn't workout.
        """
        converter = JavaConvert(self.logger)
        out, err = converter.runcmd("mkdir /")
        self.assertTrue(len(out) == 0)
        self.assertTrue(len(err) != 0)

        out, err = converter.runcmd("ls")
        self.assertTrue(len(out) != 0)
        self.assertTrue(len(err) == 0)

    def test_invalid_name(self) -> None:
        """Check that we cannot convert certain invalid files."""
        self.assertIsNone(JavaConvert(self.logger).to_graph("javadoc", ".jar"))
        self.assertIsNone(JavaConvert(self.logger).to_graph("sources", ".jar"))
        self.assertIsNone(JavaConvert(self.logger).to_graph("tests", ".jar"))

    def test_single_file(self) -> None:
        """Test that converting a single .class file to a graph."""
        converter = JavaConvert(self.logger)
        self.assertTrue(converter.name() == "Java")

        Env.clean_temps()
        base_path = "/app/code/tests/javaFiles"
        filename = "Factorial"
        res = converter.to_graph(f"{base_path}/{filename}", ".java")
        self.assertTrue(len(os.listdir(Env.TMP_PATH)) == 0)
        self.assertTrue(len(os.listdir(Env.TMP_DOT_PATH)) == 0)
        self.assertIsNotNone(res)
        # We expect a graph for init() and one for main().
        # Ignore the init() graph.
        expected_edges = [[0, 1], [1, 5], [0, 2], [2, 5], [0, 3], [3, 5], [0, 4], [4, 5]]
        expected_vertices = 6
        expected_graph = EdgeListGraph(expected_edges, expected_vertices)
        if res is not None:
            self.assertTrue(len(list(res.keys())) != 0)
            self.assertTrue(any((cfg.graph == expected_graph for cfg in res.values())))

    def test_single_file_jar(self) -> None:
        """Test that converting a single .class file to a graph."""
        converter = JavaConvert(self.logger)
        self.assertTrue(converter.name() == "Java")

        Env.clean_temps()
        base_path = "/app/code/tests/javaFiles"
        filename = "Factorial"
        res = converter.to_graph(f"{base_path}/{filename}", ".jar")
        self.assertTrue(len(os.listdir(Env.TMP_PATH)) == 0)
        self.assertTrue(len(os.listdir(Env.TMP_DOT_PATH)) == 0)
        self.assertIsNotNone(res)
        # We expect one graph for init and one for main
        # ignore the init graph
        expected_edges = [[0, 1], [1, 5], [0, 2], [2, 5], [0, 3], [3, 5], [0, 4], [4, 5]]
        expected_vertices = 6
        expected_graph = EdgeListGraph(expected_edges, expected_vertices)
        if res is not None:
            self.assertTrue(len(list(res.keys())) != 0)
            self.assertTrue(any((cfg.graph == expected_graph for cfg in res.values())))


if __name__ == '__main__':
    unittest.main()
