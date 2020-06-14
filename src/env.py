"""This module manages the temporary directories used in the generation of CFGs."""
import subprocess
from os.path import join, splitext


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

    @staticmethod
    def clean_temps() -> None:
        """Remove temp files and directories."""
        _ = subprocess.Popen(["rm", "-rf", Env.TMP_PATH])
        _ = subprocess.Popen(["rm", "-rf", Env.TMP_DOT_PATH])
        Env.make_temp()

    @staticmethod
    def make_temp() -> None:
        """Create the temporary dir."""
        subprocess.check_call(["mkdir", "-p", Env.TMP_PATH])
        subprocess.check_call(["mkdir", "-p", Env.TMP_DOT_PATH])

    @staticmethod
    def get_output_path(name):
        """For a given .jar file, determine what the output path should be for that file."""
        return join(Env.TMP_DOT_PATH, splitext(name)[0])
