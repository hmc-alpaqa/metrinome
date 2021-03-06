"""Test the conversion of Java source code to Graph objects representing its CFG."""
import os
import unittest

from core.env import Env
from core.log import Log
from lang_to_cfg.java import JavaConvert


# JavaConvert::to_graph()
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

    # def test_to_graph(self) -> None:
    #     """Test that converting a file with code to a Graph results in the correct Graph."""
    #     converter = JavaConvert(Log())
    #     self.assertTrue(converter.name() == "Java")

    #     Env.clean_temps()
    #     base_path = "/app/examples/src/apache_commons/bins/commons-math3-3.4.1"
    #     filename = "commons-math3-3.4.1"
    #     res = converter.to_graph(f"{base_path}/{filename}", ".jar")
    #     self.assertTrue(len(os.listdir(Env.TMP_PATH)) == 0)
    #     self.assertTrue(len(os.listdir(Env.TMP_DOT_PATH)) == 0)
    #     self.assertIsNotNone(res)
    #     if res is not None:
    #         self.assertTrue(len(list(res.keys())) != 0)

    #     # converter.to_graph("/app/code/", ".class")
    #     # converter.to_graph("/app/code/", ".java")

    def test_single_file(self) -> None:
        """Test that converting a single .class file to a graph."""
        converter = JavaConvert(self.logger)
        self.assertTrue(converter.name() == "Java")

        Env.clean_temps()
        base_path = "/app/code/tests/javaFiles"
        filename = "Factorial"
        res = converter.to_graph(f"{base_path}/{filename}", ".class")
        self.assertTrue(len(os.listdir(Env.TMP_PATH)) == 0)
        self.assertTrue(len(os.listdir(Env.TMP_DOT_PATH)) == 0)
        self.assertIsNotNone(res)
        if res is not None:
            # self.assertTrue(len(list(res.keys())) != 0)
            pass


if __name__ == '__main__':
    unittest.main()
