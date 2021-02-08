"""This module manages the temporary directories used in the generation of CFGs."""
import subprocess
from enum import Enum
from os.path import basename, join, splitext


class KnownExtensions(Enum):
    """A list of all the file extensions we know how to work with."""

    C      = ".c"
    Python = ".py"
    BC     = ".bc"
    Java   = ".java"


class Env:
    """
    Env stores many of the environment variables for the REPL.

    It also includes utility functions relating to environment management.
    """

    PROJECT_PATH = "/app/code/"
    TMP_PATH = join(PROJECT_PATH, "tmp")
    TMP_DOT_PATH = join(PROJECT_PATH, "tmp_dot")
    CFG_EXTRACTOR_JAR = join(PROJECT_PATH, 'lang_to_cfg',
                             'javaextractor/cfg_extractor/target/javaextractor.jar')
    KLEE_PATH = "/app/build/bin/klee"

    @staticmethod
    def clean_temps() -> None:
        """Remove temp files and directories."""
        proc_one = subprocess.Popen(["rm", "-rf", Env.TMP_PATH])
        proc_two = subprocess.Popen(["rm", "-rf", Env.TMP_DOT_PATH])
        proc_two.wait()
        proc_one.wait()
        Env.make_temp()

    @staticmethod
    def make_temp() -> None:
        """Create the temporary dir."""
        try:
            subprocess.run(["mkdir", "-p", Env.TMP_PATH], check=True, capture_output=True)
            subprocess.run(["mkdir", "-p", Env.TMP_DOT_PATH], check=True, capture_output=True)
        except subprocess.CalledProcessError as err:
            print("Error in creating TMP folders.")
            print(err)

    @staticmethod
    def get_output_path(name: str) -> str:
        """For a given .jar file, determine what the output path should be for that file."""
        return join(Env.TMP_DOT_PATH, splitext(basename(name))[0])
