"""Tests for env.py."""
import sys
sys.path.append("/app/code/")
sys.path.append("/app/code/tests")
from os.path import join
from os import listdir
import unittest
from unit_utils import captured_output  # type: ignore
from env import Env


class TestEnv(unittest.TestCase):
    """Test all of the functions relating to the environment."""

    def test_clean_temp(self) -> None:
        """Test the clean_temps function."""
        path_one = Env.TMP_DOT_PATH
        path_two = Env.TMP_PATH
        with open(f"{join(path_one, 'test_file')}", "w") as new_file:
            new_file.write("test file")

        with open(f"{join(path_two, 'test_file')}", "w") as new_file:
            new_file.write("test file")

        Env.clean_temps()

        self.assertTrue(len(listdir(path_one)) == 0)
        self.assertTrue(len(listdir(path_two)) == 0)

    def test_make_temp(self) -> None:
        """Test the make_temp function."""
        with captured_output() as (out, err):
            Env.make_temp()
            Env.make_temp()

        self.assertTrue(len(out.getvalue().strip()) == 0)
        self.assertTrue(len(err.getvalue().strip()) == 0)

        tmp_path = Env.TMP_PATH
        Env.TMP_PATH = "/sys/tmp"
        with captured_output() as (out, err):
            Env.make_temp()
        Env.TMP_PATH = tmp_path

        self.assertTrue(len(out.getvalue().strip()) != 0)

    def test_get_output_path(self) -> None:
        """Test the get_output_path function."""
        self.assertTrue(Env.get_output_path("/app/code/test.foo") == "/app/code/tmp_dot/test")


if __name__ == '__main__':
    unittest.main()
