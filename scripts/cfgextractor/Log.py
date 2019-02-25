# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:47:44 2014

@author: baki
"""

class Log:
    def __init__(self, TAG=""):
        self.TAG = TAG

    def setTag(self, TAG):
        self.TAG = TAG
    
    def i(self, msg):
        print "{} ~~~ {} ~~~".format(self.TAG, msg.upper())
        
    def v(self, msg):
        print "{} > {}".format(self.TAG, msg)

    def e(self, msg):
        print "{} > !!! {} !!!".format(self.TAG, msg)