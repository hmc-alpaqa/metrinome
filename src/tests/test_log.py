"""
Test the logging methods.

The logger lets us control how much information is displayed in the REPL
and how this information is displayed.
"""

import unittest
import sys
sys.path.append("/app/code")
from tests.utils import captured_output
from log import Log


class TestLog(unittest.TestCase):
    """Test all of the logger functionality."""

    def test_set_tag(self):
        """Test that set_tag works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.set_tag("test_tag_2")
            log.v_msg("{} ~ {}")
        expected_msg = "test_tag_2 > {} ~ {}"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

        print(err)

    def test_i(self):
        """Test that i_msg works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.i_msg("test_msg")
        expected_msg = "test_tag ~~~ TEST_MSG ~~~"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

        print(err)

    def test_v(self):
        """Test that v_msg works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.v_msg("test_msg")
        expected_msg = "test_tag > test_msg"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

        print(err)

    def test_e(self):
        """Test that e_msg works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.e_msg("test_msg")
        expected_msg = "test_tag > !!! test_msg !!!"
        self.assertEqual(expected_msg, out.getvalue().rstrip())

        print(err)


if __name__ == '__main__':
    unittest.main()
