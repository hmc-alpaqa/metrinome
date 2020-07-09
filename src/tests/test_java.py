"""Test the conversion of Java source code to Graph objects representing its CFG."""
import unittest
import sys
import os
sys.path.append("/app/code/")
sys.path.append("/app/code/lang_to_cfg/")
from lang_to_cfg.java import JavaConvert  # type: ignore
from log import Log
from env import Env


# JavaConvert::to_graph()
class TestJavaConvert(unittest.TestCase):
    """All of the tests to verify that we can convert Java source code to Graph objects."""

    def test_invalid_name(self) -> None:
        """Check that we cannot convert certain invalid files."""
        self.assertIsNone(JavaConvert(Log()).to_graph("javadoc", ".jar"))
        self.assertIsNone(JavaConvert(Log()).to_graph("sources", ".jar"))
        self.assertIsNone(JavaConvert(Log()).to_graph("tests", ".jar"))

    def test_to_graph(self) -> None:
        """Test that converting a file with code to a Graph results in the correct Graph."""
        converter = JavaConvert(Log())
        self.assertTrue(converter.name() == "Java")

        Env.clean_temps()
        base_path = "/app/examples/src/apache_commons/bins/commons-math3-3.4.1"
        filename = "commons-math3-3.4.1"
        res = converter.to_graph(f"{base_path}/{filename}", ".jar")
        self.assertTrue(len(os.listdir(Env.TMP_PATH)) == 0)
        self.assertTrue(len(os.listdir(Env.TMP_DOT_PATH)) == 0)
        self.assertIsNotNone(res)
        if res is not None:
            self.assertTrue(len(list(res.keys())) != 0)

        # converter.to_graph("/app/code/", ".class")
        # converter.to_graph("/app/code/", ".java")


if __name__ == '__main__':
    unittest.main()
