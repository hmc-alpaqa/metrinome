import os, subprocess
from os.path import join, abspath, basename, splitext
class Env:
    """
    Env stores many of the environment variables for the REPL.

    It also includes utility functions relating to environment management.
    """

    PROJECT_PATH = "/app/code/"
    TMP_PATH = join(PROJECT_PATH, "tmp")
    OUTPUT_PATH = join(PROJECT_PATH, "output")
    CFG_EXTRACTOR = join(PROJECT_PATH, 'lang_to_cfg/javaextractor/cfgextractor.jar')
    
    LIB_PATH = join(PROJECT_PATH, 'libs')
    CFG_EXTRACTOR_LIVE = join(PROJECT_PATH, 'lang_to_cfg',
        'javaextractor/cfg_extractor/src/main/java/com/hmc/Extractor.java')

    # JAVA LIBS
    APACHE_IO_PATH = join(LIB_PATH, 'commons-io-2.4.jar')
    APACHE_CLI_PATH = join(LIB_PATH, 'commons-cli-1.2.jar')
    APACHE_LANG_PATH = join(LIB_PATH, 'commons-lang3-3.3.2.jar')
    APACHE_LOG_PATH = join(LIB_PATH, 'commons-logging-1.2.jar')
    APACHE_HCLIENT_PATH = join(LIB_PATH, 'httpclient-4.3.6.jar')
    APACHE_HCORE_PATH = join(LIB_PATH, 'httpcore-4.3.3.jar')
    APACHE_HMIME_PATH = join(LIB_PATH, 'httpmime-4.3.6.jar')
    ASM_PATH = join(LIB_PATH, 'asm-all-5.0.3.jar')
    

    @staticmethod
    def clean_temps() -> None:
        """Remove temp files and directories."""
        proc = subprocess.Popen(["rm", "-rf", Env.TMP_PATH])
        Env.make_temp()
    
    @staticmethod
    def make_temp() -> None:
        """Create the temporary dir."""
        subprocess.check_call(["mkdir", "-p", Env.TMP_PATH])

    @staticmethod
    def get_output_path(name):
        """For a given .jar file, determine what the output path should be for that file."""
        return join(Env.OUTPUT_PATH, splitext(name)[0])
