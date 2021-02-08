# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:47:44 2014.

@author: baki
"""

from enum import Enum, auto


class Colors(Enum):
    """Use these within print or log statements to change output color."""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[35m'
    TITLE = '\033[96m'


class LogLevel(Enum):
    """Set levels in the logger to decide which messages will be displayed."""

    DEBUG   = auto()
    REGULAR = auto()


class Log:
    """Log is used to print messages to standard out with additional formatting."""

    def __init__(self, tag: str = "", display_output: bool = True,
                 log_level: LogLevel = LogLevel.REGULAR) -> None:
        """Create a new logger."""
        self.tag = tag
        self._display_output = display_output
        self._log_level = log_level

    def set_tag(self, tag: str) -> None:
        """Set the tag for the logger. This tag will be prepended to all messages."""
        self.tag = tag

    def d_msg(self, *msgs: str) -> None:
        """Use for debugging. Messages are only displayed if LOG_LEVEL is 'DEBUG'."""
        if self._display_output and self._log_level is LogLevel.DEBUG:
            for msg in msgs:
                debug_str = " === DEBUG === "
                if len(self.tag) == 0:
                    print(f"{Colors.OKBLUE.value}{debug_str}{Colors.ENDC.value}: {msg}")
                else:
                    print(f"{self.tag}{Colors.OKBLUE.value}{debug_str}{Colors.ENDC.value}: {msg}")

    def i_msg(self, *msgs: str) -> None:
        """Log an information-level message."""
        if self._display_output:
            for msg in msgs:
                print(f"{self.tag} ~~~ {msg.upper()} ~~~")

    def v_msg(self, *msgs: str) -> None:
        """Log a verbose-level message."""
        if self._display_output:
            for msg in msgs:
                print(f"{self.tag} > {msg}")

    def e_msg(self, *msgs: str) -> None:
        """Log an error-level message."""
        if self._display_output:
            for msg in msgs:
                beginning = f" {self.tag} > {Colors.WARNING.value} !!! {Colors.ENDC.value} "
                end = f"{msg} {Colors.WARNING.value} !!! {Colors.ENDC.value}"
                print(beginning + end)
