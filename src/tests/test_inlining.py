"""Test all of the methods associated with inlining."""
import unittest

from inlining.inlining_script import get_lines
from inlining.inlining_script_heuristic import get_lines as get_lines_heuristic


class TestPathComplexity(unittest.TestCase):
    """Test the inlining methods."""

    def test_getlines(self) -> None:
        """Smoke test for getlines in standard inlining."""
        get_lines("/app/code/tests/cFiles/inlining_tests/test-40-un-inlined.c")

    def test_getlines_heuristic(self) -> None:
        """Smoke test for getlines in heuristic inlining."""
        get_lines_heuristic("/app/code/tests/cFiles/inlining_tests/test-40-un-inlined.c")


if __name__ == '__main__':
    unittest.main()
