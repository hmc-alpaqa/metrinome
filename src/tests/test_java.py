"""
This module tests if we can convert Java source code to Graph
objects representing the control flow graphs of the code.
"""
import unittest

# JavaConvert::to_graph()
class TestJavaConvert(unittest.TestCase):
    """
    Contains all of the unit tests to verify that we can successfully
    convert Java source code to Graph objects.
    """
    def test_to_graph(self):
        """
        Test that converting a file with code to a Graph results in the
        correct Graph.
        """

if __name__ == '__main__':
    unittest.main()
