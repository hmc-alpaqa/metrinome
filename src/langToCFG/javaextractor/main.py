#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 23:49:26 2014

@author: baki
"""

import sys
import os
import getopt

from langToCFG.javaextractor.Log import Log
from langToCFG.javaextractor.Env import Env
from langToCFG.javaextractor.App import App

OUTPUT_FOLDER = None
app = None
log = Log(">>")
def main(argv):
    global INPUT_FOLDER, OUTPUT_FOLDER, app
    try:
        opts, args = getopt.getopt(argv,"hci:o:",["inputfile=","output="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfolder>")

    ext = "*.jar"
    for opt, arg in opts:
        if opt == '-h':
            print("test.py -i <inputfile> -o <outputfolder>")
            sys.exit()
        elif opt in ("-i", "--input"):
            INPUT_FOLDER = arg
            log.i('input folder is "' + INPUT_FOLDER + '"')
        elif opt in ("-o", "--output"):
            OUTPUT_FOLDER = arg
            log.i('output folder is "' + OUTPUT_FOLDER + '"')

    if not os.path.isdir(Env.TMP_PATH):
        os.mkdir(Env.TMP_PATH)
    
    app = App(INPUT_FOLDER, OUTPUT_FOLDER, ext=ext)
    app.run()

if __name__ == "__main__":
   main(sys.argv[1:])
   