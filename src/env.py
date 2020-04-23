"""
Created on Sat Aug  2 20:21:33 2014.

@author: baki
"""

import os


class Env:
    """
    Env stores many of the environment variables for the REPL.

    It also includes useful utility functions relating to environment management.
    """

    ######################################################################################
    # PROJECT FOLDER PATHS ###############################################################
    ######################################################################################

    ROOT_PATH = os.path.abspath(os.getcwd())
    PROJECT_PATH = ROOT_PATH
    OUTPUT_PATH = os.path.abspath(os.path.join(PROJECT_PATH, 'outputs'))
    LIB_PATH = os.path.abspath(os.path.join(PROJECT_PATH, 'libs'))
    SCRIPT_PATH = ROOT_PATH

    CFG_EXTRACTOR = os.path.abspath(os.path.join(PROJECT_PATH, 'langToCFG', 'javaextractor',
                                                 'java', 'cfgextractor.jar'))
    CFG_EXTRACTOR_LIVE = os.path.abspath(
        os.path.join(PROJECT_PATH, 'langToCFG',
                     'javaextractor', 'cfgextractor_decompiled_source',
                     'Extractor.java'))

    # JAVA LIBS
    APACHE_IO_PATH = os.path.abspath(os.path.join(LIB_PATH, 'commons-io-2.4.jar'))
    APACHE_CLI_PATH = os.path.abspath(os.path.join(LIB_PATH, 'commons-cli-1.2.jar'))
    APACHE_LANG_PATH = os.path.abspath(os.path.join(LIB_PATH, 'commons-lang3-3.3.2.jar'))
    APACHE_LOG_PATH = os.path.abspath(os.path.join(LIB_PATH, 'commons-logging-1.2.jar'))
    APACHE_HCLIENT_PATH = os.path.abspath(os.path.join(LIB_PATH, 'httpclient-4.3.6.jar'))
    APACHE_HCORE_PATH = os.path.abspath(os.path.join(LIB_PATH, 'httpcore-4.3.3.jar'))
    APACHE_HMIME_PATH = os.path.abspath(os.path.join(LIB_PATH, 'httpmime-4.3.6.jar'))
    ASM_PATH = os.path.abspath(os.path.join(LIB_PATH, 'asm-all-5.0.3.jar'))

    # RUNTIME TEMP DIRECTORIES
    TMP_PATH = os.path.abspath(os.path.join(OUTPUT_PATH, 'tmp',))

    ######################################################################################
    # FUNCTIONS ##########################################################################
    ######################################################################################

    @staticmethod
    def __get_path(folder='', prefix='', name='', ext=''):
        """
        Create an absolute path based on path information.

        Given a folder, prefix, file name, and file extension,
        join all of them and return an absolute path.
        """
        return os.path.abspath(os.path.join(folder, prefix + os.path.basename(name))) + ext

    @staticmethod
    def get_output_path(name, ext=''):
        """For a given .jar file, determine what the output path should be for that file."""
        if name.endswith('.jar'):
            name = name[:-4]
        return Env.__get_path(folder=Env.OUTPUT_PATH, name=name, ext=ext)

    @staticmethod
    def get_tmp_path(name, ext=''):
        """Given a file name and extension, get the path to it in the temporary folder."""
        return Env.__get_path(folder=Env.TMP_PATH, name=name, ext=ext)

    @staticmethod
    def get_basename(name):
        """Get the path to a file without the file name."""
        return os.path.basename(name)

    @staticmethod
    def get_base_filename(name):
        """Given a path, get the file name."""
        return os.path.basename(name)[:-4]

    @staticmethod
    def get_dirname(name):
        """Given a path, get the directory."""
        return os.path.dirname(name)