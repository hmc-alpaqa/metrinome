"""
List of all the error messages Metrinome can throw.

Use these for maintaining consistency, rather than putting strings directly in the log messages.
"""

from typing import Callable

# pylint: disable=pointless-string-statement
MISSING_FILENAME: str = "Must provide file name."
MISSING_TYPE_AND_NAME: str = "Must specify type and name."
MISSING_NAME: str = "Must specify name."
NO_FILE_EXT: Callable[[str], str] = lambda f_name: \
    f"No file extension found for {f_name}."
NOT_IMPLEMENTED: str = "Not implemented."
EXTENSION: Callable[[str, str], str] = lambda target_type, file_extension: \
    f"File extension must be {target_type}, not {file_extension}."


class ReplErrors:
    """A list of REPL specific errors."""

    KLEE_FORMATTED = "Must provide KLEE formatted name."
    CANNOT_ACCEPT_ARGS = "Cannot accept arguments."
    TYPE_TO_LIST = "Must specify object type to list (metrics, graphs, or KLEE type)."
    SPECIFY_TYPE = "Must specify type (metric, graph, or any KLEE type) and name."
    MISSING_PATH_RM = "Missing name of file/directory to delete."
    GRAPH_NAME = "Must provide graph name."
    MISSING_NAME_MKDIR = "Missing directory name."
    NO_ARGS = "No arguments allowed."
    MISSING_NAMES_MV = "Missing name one and name two."
