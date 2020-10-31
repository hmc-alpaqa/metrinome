"""All of the tests for the path complexity and APC computer."""

import unittest
import command

# pylint: disable=no-value-for-parameter


class TestPathComplexity(unittest.TestCase):
    """Test PathComplexity object."""

    def test(self) -> None:
        """Compute path complexity for a regular .dot file."""
        repl_wrapper = None
        repl = command.Command("/", True, False, repl_wrapper)
        root_dir = "/app/examples/cfgs/simple_test_cfgs"
        filename = "vlab_cs_ucsb_test_SimpleExample_test6_0_basic.dot"
        repl.do_import(False,
                       f"{root_dir}/{filename}")
        repl.do_metrics("*")


if __name__ == '__main__':
    unittest.main()
