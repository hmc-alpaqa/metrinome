# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:47:44 2014

@author: baki
"""

class Log:
    def __init__(self, TAG="", display_output=True):
        self.TAG = TAG
        self.display_output = display_output

    def setTag(self, TAG):
        self.TAG = TAG
    
    def i(self, msg):
        if self.display_output:
            print("{} ~~~ {} ~~~".format(self.TAG, msg.upper()))
        
    def v(self, msg):
        if self.display_output:
            print("{} > {}".format(self.TAG, msg))

    def e(self, msg):
        if self.display_output:
            print("{} > !!! {} !!!".format(self.TAG, msg))