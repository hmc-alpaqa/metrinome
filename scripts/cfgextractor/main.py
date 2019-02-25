#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 23:49:26 2014

@author: baki
"""

import sys
import os
import getopt

from Log import Log
from Env import Env
from App import App

#INPUT_FOLDER = '/home/baki/RA/complexity/apache_commons'
#INPUT_FOLDER = '/usr/lib/jvm/java-7-oracle/jre/lib'     
#INPUT_FOLDER = '/home/baki/workspaces/default/CFGExtractor/outputs'
#INPUT_FOLDER = '/home/baki/RA/complexity/apache'
#INPUT_FOLDER = None
OUTPUT_FOLDER = None
app = None
log = Log(">>")
def main(argv):
    global INPUT_FOLDER, OUTPUT_FOLDER, app
    try:
        opts, args = getopt.getopt(argv,"hci:o:",["inputfile=","output="])
    except getopt.GetoptError:
        print "test.py -i <inputfile> -o <outputfolder>"
      #sys.exit(2)

    cmd_option = ""
    ext = "*.jar"
    for opt, arg in opts:
        if opt == '-h':
            print "test.py -i <inputfile> -o <outputfolder>"
            sys.exit()
        elif opt in ("-i", "--input"):
            INPUT_FOLDER = arg
            log.i('input folder is "' + INPUT_FOLDER + '"')
        elif opt in ("-o", "--output"):
            OUTPUT_FOLDER = arg
            log.i('output folder is "' + OUTPUT_FOLDER + '"')
        elif opt == '-c':
            cmd_option = "-c"
            ext = "*.dot"

    if not os.path.isdir(Env.TMP_PATH):
        os.mkdir(Env.TMP_PATH)
    
#    cmd_option = "-c"
#    ext = "*.dot"
    app = App(INPUT_FOLDER, OUTPUT_FOLDER, ext=ext)
    app.run(option=cmd_option)

if __name__ == "__main__":
   main(sys.argv[1:])
   