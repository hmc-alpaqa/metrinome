# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:47:44 2014

@author: baki
"""

from enum import Enum, auto

class LogLevel(Enum):
    """
    Allow different levels to be set in the logger, indicating
    which messages will actually be displayed.
    """
    DEBUG   = auto()
    REGULAR = auto()

class Log:
    """
    Log is used to print messages to standard out with additional formatting.
    """

    def __init__(self, tag: str = "", display_output: bool = True,
                 log_level=LogLevel.REGULAR) -> None:
        """
        Create a new logger.
        """
        self.tag = tag
        self.display_output = display_output
        self.log_level = log_level

    def set_tag(self, tag: str) -> None:
        """
        Set the tag for the logger.
        This tag will be prepended to all messages.
        """
        self.tag = tag

    def d_msg(self, msg: str) -> None:
        """
        d is used for DEBUGGING, and messages are only displayed if LOG_LEVEL is 'DEBUG'
        """
        if self.display_output and self.log_level is LogLevel.DEBUG:
            print(f"=== DEBUG ===: {msg}")

    def i_msg(self, msg: str) -> None:
        """
        Log an information-level message.
        """
        if self.display_output:
            print(f"{self.tag} ~~~ {msg.upper()} ~~~")

    def v_msg(self, msg: str) -> None:
        """
        Log a verbose-level message.
        """
        if self.display_output:
            print(f"{self.tag} > {msg}")

    def e_msg(self, msg: str) -> None:
        """
        Log an error-level message.
        """
        if self.display_output:
            print(f"{self.tag} > !!! {msg} !!!")
