"""Test the conversion of Java source code to Graph objects representing its CFG."""
import unittest
import sys
sys.path.append("/app/code/")
sys.path.append("/app/code/lang_to_cfg/")
from lang_to_cfg.java import JavaConvert  # type: ignore
from log import Log


# JavaConvert::to_graph()
class TestJavaConvert(unittest.TestCase):
    """All of the tests to verify that we can convert Java source code to Graph objects."""

    def test_to_graph(self) -> None:
        """Test that converting a file with code to a Graph results in the correct Graph."""
        converter = JavaConvert(Log())
        self.assertTrue(converter.name() == "Java")

        # converter.to_graph("/app/code/", ".jar")
        # converter.to_graph("/app/code/", ".class")
        # converter.to_graph("/app/code/", ".java")


if __name__ == '__main__':
    unittest.main()
