"""Test that we can convert Python files to CFGs."""

import unittest
import sys
sys.path.append("/app/code/")
from lang_to_cfg.python import PythonConvert
from graph import Graph, GraphType


class TestPythonConvert(unittest.TestCase):
    """
    Test the conversion of Python code to CFgs.

    Create python source file containing each of the
    basic building blocks that affect CFGs and verify
    that we can parse all of them correctly.
    """

    def setUp(self):
        """Create an instance of the python converter for each test."""
        self.converter = PythonConvert()
        self.base_path = "/app/code/tests"

    def test_expr(self):
        """
        Test that we can correctly parse expressions.

        (e.g. y + x > 0)
        """
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/expr", ".py")
        expected = Graph([(0, 1), (1, 2)], [0, 1, 2], 0, 2, GraphType.EDGE_LIST)
        self.assertTrue(expected == res['expr_func'])

    def test_assign(self):
        """Test that we can correct parse assignment of variables."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/assign", ".py")
        expected = Graph([(0, 1), (1, 2), (2, 3)], [0, 1, 2, 3], 0, 3, GraphType.EDGE_LIST)
        self.assertTrue(expected == res['assign_func'])

    def test_return(self):
        """Test that we can correctly parse return statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/return", ".py")
        expected = Graph([(0, 1), (1, 2)], [0, 1, 2], 0, 2, GraphType.EDGE_LIST)
        self.assertTrue(expected == res['return_func'])

    def test_for(self):
        """Test that we can correctly parse for loops."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/for", ".py")
        expected = Graph([(0, 1), (1, 2), (1, 3), (2, 4), (4, 1)],
                         [0, 1, 2, 3, 4], 0, 3, GraphType.EDGE_LIST)
        self.assertTrue(expected == res['for_func'])

    def test_while(self):
        """Test that we can correctly parse while loops."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/while", ".py")
        expected = Graph([(0, 1), (1, 2), (2, 3), (3, 2)], [0, 1, 2, 3], 0, 2, GraphType.EDGE_LIST)
        self.assertTrue(expected == res['while_func'])

    def test_if(self):
        """Test that we can correctly parse if statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/if", ".py")
        expected = Graph([(0, 1), (1, 2), (2, 3), (2, 4), (2, 5),
                          (3, 6), (4, 6), (5, 6)], [0, 1, 2, 3, 4, 5, 6], 0, 6, GraphType.EDGE_LIST)
        self.assertTrue(res['if_func'] == expected)

    def test_else(self):
        """Test that we can correctly parse if statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/else", ".py")
        expected = Graph([(0, 1), (1, 2), (2, 3), (2, 4), (2, 5),
                          (2, 6), (3, 7), (4, 7), (5, 7), (6, 7)],
                         [0, 1, 2, 3, 4, 5, 6, 7], 0, 7, GraphType.EDGE_LIST)
        self.assertTrue(res['if_func'] == expected)

    def test_with(self):
        """Test that we can correct parse with blocks."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/with", ".py")
        expected = Graph([(0, 1), (1, 2)], [0, 1, 2], 0, 2, GraphType.EDGE_LIST)
        self.assertTrue(res['with_func'] == expected)

    # Raise and Try not implemented.
    # def test_raise(self):
    #     """Test that we can correctly parse raise expressions."""
    #     self.converter.to_graph(f"{self.base_path}/pythonFiles/raise", ".py")

    # def test_try(self):
    #     """Test that we can correctly parse try-except blocks."""
    #     self.converter.to_graph(f"{self.base_path}/pythonFiles/try", ".py")
    # """


if __name__ == '__main__':
    unittest.main()
