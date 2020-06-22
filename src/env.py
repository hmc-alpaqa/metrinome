"""This module manages the temporary directories used in the generation of CFGs."""
import subprocess
from os.path import join, splitext, basename


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
        proc_one = subprocess.Popen(["rm", "-rf", Env.TMP_PATH])
        proc_two = subprocess.Popen(["rm", "-rf", Env.TMP_DOT_PATH])
        proc_two.wait()
        proc_one.wait()
        Env.make_temp()

    @staticmethod
    def make_temp() -> None:
        """Create the temporary dir."""
        try:
            subprocess.check_call(["mkdir", "-p", Env.TMP_PATH])
            subprocess.check_call(["mkdir", "-p", Env.TMP_DOT_PATH])
        except subprocess.CalledProcessError as err:
            print("Error in creating TMP folders.")
            print(err)

    @staticmethod
    def get_output_path(name: str):
        """For a given .jar file, determine what the output path should be for that file."""
        return join(Env.TMP_DOT_PATH, splitext(basename(name))[0])
