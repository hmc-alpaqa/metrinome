"""
Test the logging methods.

The logger lets us control how much information is displayed in the REPL
and how this information is displayed.
"""

import unittest

from core.log import Colors, Log, LogLevel
from tests.unit_utils import captured_output


class TestLog(unittest.TestCase):
    """Test all of the logger functionality."""

    def test_set_tag(self) -> None:
        """Test that set_tag works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.set_tag("test_tag_2")
            log.v_msg("{} ~ {}")
        expected_msg = "test_tag_2 > {} ~ {}"

        self.assertEqual(expected_msg, out.getvalue().rstrip())
        self.assertTrue(len(err.read()) == 0)

    def test_i(self) -> None:
        """Test that i_msg works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.i_msg("test_msg")
        expected_msg = "test_tag ~~~ TEST_MSG ~~~"

        self.assertEqual(expected_msg, out.getvalue().rstrip())
        self.assertTrue(len(err.read()) == 0)

    def test_v(self) -> None:
        """Test that v_msg works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.v_msg("test_msg")
        expected_msg = "test_tag > test_msg"

        self.assertEqual(expected_msg, out.getvalue().rstrip())
        self.assertTrue(len(err.read()) == 0)

    def test_e(self) -> None:
        """Test that e_msg works correctly."""
        log = Log(tag="test_tag", display_output=True)
        with captured_output() as (out, err):
            log.e_msg("test_msg")
        colors = f"{Colors.WARNING.value} !!! {Colors.ENDC.value}"
        expected_msg = f" test_tag > {colors} test_msg {colors}"

        self.assertEqual(expected_msg, out.getvalue().rstrip())
        self.assertTrue(len(err.read()) == 0)

    def test_d(self) -> None:
        """Test that d_msg works correctly."""
        log = Log(tag="", display_output=True)
        with captured_output() as (out, err):
            log.d_msg("test_msg")

        self.assertTrue(len(out.getvalue().rstrip()) == 0)
        self.assertTrue(len(err.read()) == 0)

        log = Log(tag="test_tag", display_output=True, log_level=LogLevel.DEBUG)
        with captured_output() as (out, err):
            log.d_msg("test_msg", "test_msg2")

        colors = f"{Colors.OKBLUE.value} === DEBUG === {Colors.ENDC.value}"
        expected_msg = f"test_tag{colors}: test_msg\n"
        expected_msg2 = f"test_tag{colors}: test_msg2"

        self.assertEqual(expected_msg + expected_msg2, out.getvalue().rstrip())
        self.assertTrue(len(err.read()) == 0)

        log.tag = ""
        with captured_output() as (out, err):
            log.d_msg("test_msg")

        colors = f"{Colors.OKBLUE.value} === DEBUG === {Colors.ENDC.value}"
        expected_msg = f"{colors}: test_msg"
        self.assertEqual(expected_msg, out.getvalue().rstrip())
        self.assertTrue(len(err.read()) == 0)


if __name__ == '__main__':
    unittest.main()
