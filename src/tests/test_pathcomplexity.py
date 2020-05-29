"""All of the tests for the path complexity and APC computer."""

import unittest
import sys
sys.path.append("/app/code/")
import command

# pylint: disable=no-value-for-parameter


class TestPathComplexity(unittest.TestCase):
    """Test PathComplexity object."""

    def test(self):
        """Compute path complexity for a regular .dot file."""
        repl_wrapper = None
        repl = command.Command("/", False, False, repl_wrapper)
        repl.do_import("-r /app/code/tests/core/cfg.add_field_list.dot3.dot")
        repl.do_list("*")
        repl.do_show("graph /app/code/tests/core/new_cleaned_subset/cfg.add_field_list.dot3")
        repl.do_metrics("*")


if __name__ == '__main__':
    unittest.main()
