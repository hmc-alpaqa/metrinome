"""Test that we can convert Python files to CFGs."""

import unittest


class TestPythonConvert(unittest.TestCase):
    """
    Test the conversion of Python code to CFgs.

    Create python source file containing each of the
    basic building blocks that affect CFGs and verify
    that we can parse all of them correctly.
    """

    def test_expr(self):
        """
        Test that we can correctly parse expressions.

        (e.g. y + x > 0)
        """

    def test_return(self):
        """Test that we can correctly parse return statements."""

    def test_assign(self):
        """Test that we can correct parse assignment of variables."""

    def test_for(self):
        """Test that we can correctly parse for loops."""

    def test_with(self):
        """Test that we can correct parse with blocks."""

    def test_if(self):
        """Test that we can correctly parse if statements."""

    def test_raise(self):
        """Test that we can correctly parse raise expressions."""

    def test_try(self):
        """Test that we can correctly parse try-except blocks."""

    def test_while(self):
        """Test that we can correctly parse while loops."""

    # PythonConvert::to_graph
    def test_to_graph(self):
        """Test that we can correctly convert a file to Graph objects."""


if __name__ == '__main__':
    unittest.main()
