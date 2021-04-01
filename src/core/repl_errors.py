"""
List of all the error messages Metrinomeme can throw.

Use these for maintaining consistency, rather than putting strings directly in the log messages.
"""

from typing import Callable

# pylint: disable=pointless-string-statement
MISSING_FILENAME: str = "Must provide file name."
MISSING_TYPE_AND_NAME: str = "Must specify type and name."
MISSING_NAME: str = "Must specify name."
MISSING_OUTPUT_PATH: str = "Must provide output path."
NO_FILE_EXT: Callable[[str], str] = lambda f_name: \
    f"No file extension found for {f_name}."
NOT_IMPLEMENTED: str = "Not implemened."
EXTENSION: Callable[[str, str], str] = lambda target_type, file_extension: \
    f"File extension must be {target_type}, not {file_extension}."
