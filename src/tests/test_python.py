"""Test that we can convert Python files to CFGs."""

import unittest

from core.log import Log
from graph.graph import EdgeListGraph
from lang_to_cfg.python import PythonConvert


class TestPythonConvert(unittest.TestCase):
    """
    Test the conversion of Python code to CFgs.

    Create python source file containing each of the
    basic building blocks that affect CFGs and verify
    that we can parse all of them correctly.
    """

    def setUp(self) -> None:
        """Create an instance of the python converter for each test."""
        self.converter = PythonConvert(Log(display_output=False))
        self.base_path = "/app/code/tests"

    def test_expr(self) -> None:
        """
        Test that we can correctly parse expressions.

        (e.g. y + x > 0)
        """
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/expr", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3]], 4)
        self.assertEqual(expected, res['expr_func'].graph)

    def test_assign(self) -> None:
        """Test that we can correct parse assignment of variables."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/assign", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3], [3, 4]], 5)
        self.assertEqual(expected, res['assign_func'].graph)

    def test_return(self) -> None:
        """Test that we can correctly parse return statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/return", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3]], 4)
        self.assertEqual(expected, res['return_func'].graph)

    def test_for(self) -> None:
        """Test that we can correctly parse for loops."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/for", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [1, 3], [2, 4], [4, 1], [3, 5]], 6)
        self.assertEqual(expected, res['for_func'].graph)

    def test_while(self) -> None:
        """Test that we can correctly parse while loops."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/while", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3], [3, 2], [2, 4]], 5)
        self.assertEqual(expected, res['while_func'].graph)

    def test_if(self) -> None:
        """Test that we can correctly parse if statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/if", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3], [2, 4], [2, 5],
                                 [3, 6], [4, 6], [5, 6]], 7)
        self.assertEqual(res['if_func'], expected)

    def test_else(self) -> None:
        """Test that we can correctly parse if statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/else", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3], [2, 4], [2, 5],
                                 [2, 6], [3, 7], [4, 7], [5, 7], [6, 7]], 8)
        self.assertEqual(res['if_func'], expected)

    def test_with(self) -> None:
        """Test that we can correctly parse with statements."""
        res = self.converter.to_graph(f"{self.base_path}/pythonFiles/with", ".py")
        expected = EdgeListGraph([[0, 1], [1, 2], [2, 3]], 4)
        self.assertEqual(res['with_func'], expected)


if __name__ == '__main__':
    unittest.main()
