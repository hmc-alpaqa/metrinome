"""Test that we can convert Python files to CFGs."""

import unittest
import sys
sys.path.append("/app/code/")
from lang_to_cfg.python import PythonConvert
from graph import Graph

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

    '''
    def test_expr(self):
        """
        Test that we can correctly parse expressions.

        (e.g. y + x > 0)
        """
        res = self.converter.to_graph("pythonFiles/expr", ".py")
        expected = Graph([(0, 1)], [0, 1], 0, 1)
        self.assertTrue(expected == res['expr_func'])

    def test_assign(self):
        """Test that we can correct parse assignment of variables."""
        res = self.converter.to_graph("pythonFiles/assign", ".py")
        expected = Graph([(0, 1), (1, 2)], [0, 1, 2], 0, 2)
        self.assertTrue(expected == res['assign_func'])

    def test_return(self):
        """Test that we can correctly parse return statements."""
        res = self.converter.to_graph("pythonFiles/return", ".py")
        expected = Graph([(0, 1)], [0, 1], 0, 1)
        self.assertTrue(expected == res['return_func'])

    def test_for(self):
        """Test that we can correctly parse for loops."""
        res = self.converter.to_graph("pythonFiles/for", ".py")
        expected = Graph([(0, 1), (0, 2), (1, 3), (3, 0)], [0, 1, 2, 3], 0, 2)
        self.assertTrue(expected == res['for_func'])

    def test_while(self):
        """Test that we can correctly parse while loops."""
        res = self.converter.to_graph("pythonFiles/while", ".py")
        expected = Graph([(0, 1), (1, 2), (2, 1)], [0, 1, 2], 0, 1)
        print(res['while_func'])
        self.assertTrue(expected == res['while_func'])
    '''

    def test_if(self):
        """Test that we can correctly parse if statements."""
        res = self.converter.to_graph("pythonFiles/if", ".py")
        expected = Graph([], [], 0, 0) 
        print(res['if_func'])
        self.assertTrue(res['if_func'] == expected)

    '''
    def test_with(self):
        """Test that we can correct parse with blocks."""
        self.converter.to_graph("pythonFiles/with", ".py")

    def test_raise(self):
        """Test that we can correctly parse raise expressions."""
        self.converter.to_graph("pythonFiles/raise", ".py")

    def test_try(self):
        """Test that we can correctly parse try-except blocks."""
        self.converter.to_graph("pythonFiles/try", ".py")

    # PythonConvert::to_graph
    def test_to_graph(self):
        """Test that we can correctly convert a file to Graph objects."""
        self.converter.to_graph("pythonFiles/graph", ".py")
    '''
if __name__ == '__main__':
    unittest.main()
