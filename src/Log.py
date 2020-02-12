# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:47:44 2014

@author: baki
"""

from enum import Enum, auto

class LOG_LEVEL(Enum): 
    DEBUG   = auto()
    REGULAR = auto()

class Log:
    def __init__(self, TAG="", display_output=True, log_level=LOG_LEVEL.REGULAR):
        self.TAG = TAG
        self.display_output = display_output
        self.log_level = log_level

    def setTag(self, TAG):
        self.TAG = TAG

    def d(self, msg):
        '''
        d is used for DEBUGGING, and messages are only displayed if LOG_LEVEL is 'DEBUG'
        '''
        if self.display_output and self.log_level is LOG_LEVEL.DEBUG: 
            print(f"=== DEBUG ===: {msg}") 

    def i(self, msg):
        if self.display_output:
            print(f"{self.TAG} ~~~ {msg.upper()} ~~~")

    def v(self, msg):
        if self.display_output:
            print(f"{self.TAG} > {msg}")

    def e(self, msg):
        if self.display_output:
            print(f"{self.TAG} > !!! {msg} !!!")
