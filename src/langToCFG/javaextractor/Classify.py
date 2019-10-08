# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:04:16 2015

@author: baki
"""

import getopt
import sys
import os
import glob
import re
import math

from langToCFG.javaextractor.Log import Log
from langToCFG.javaextractor.Shell import Shell
from langToCFG.javaextractor.Env import Env

class Classifier:
    def __init__(self, input_path=None, output_path=None, ext="*.input", TAG=""):
        self.log = Log(TAG=TAG)
        self.shell = Shell()
        self.env = Env()        
        self.input_path = input_path
        self.output_file = output_path
        self.file_list = [self.input_path]
        self.peak_values = []
        if os.path.isdir(self.input_path):
            self.file_list = sorted(glob.glob(Env.join_path(self.input_path, ext)))
    
        
    def match_csv_line(self, string):
        self.result = re.match(r"\s*(?P<id>.+)\s*,\s*(?P<name>.+)\s*,\s*(?P<cyclo>.+)\s*,\s*(?P<npath>.+)\s*,(?P<type>.+),\s*(?P<asym>.+)\s*,\s*(?P<func>.*)", string, re.IGNORECASE)        
        return self.result
        
    def match_const_large_number(self, string):
        self.result = re.match(r".*(?P<num>\d+)\.(?P<dec>\d+)\*\^(?P<exp>\d+).*", string)
        return self.result
        
    def run(self, options=""):
        self.log.i("start")        
        for file_name in self.file_list:
            self.log.v("processing {}".format(file_name))
            file_base = Env.get_base_filename(self.input_path)
            outfile =  open(file_base + '_classified_all.csv', 'w')
            c1file = open(file_base + '_c1.csv', 'w')
            cgt1file = open(file_base + '_cgt1.csv', 'w')
            p1file = open(file_base + '_p1.csv', 'w')
            p2file = open(file_base + '_p2.csv', 'w')
            p3file = open(file_base + '_p3.csv', 'w')
            pgte4file = open(file_base + '_pgte4.csv', 'w')
            e1file = open(file_base + '_e1.csv', 'w')
            e2file = open(file_base + '_e2.csv', 'w')
            e3file = open(file_base + '_e3.csv', 'w')
            egte4file = open(file_base + '_egte4.csv', 'w')
            fixfile = open(file_base + '_fixes_required.csv', 'w')
            
            with open(file_name, 'r') as f:
                for line in f:
                    tofile = None
                    cls = ''
                    cls_line = ''
                    if self.match_csv_line(line):
                        _id = self.result.group('id')
                        name = self.result.group('name')
                        cyclo = self.result.group('cyclo')
                        npath = self.result.group('npath')
                        _type = self.result.group('type')
                        asym = self.result.group('asym')
                        func = self.result.group('func')
                        
                        if _type == 'Constant':
                            
                            if self.match_const_large_number(asym):
                                num = int(self.result.group('num'))
                                dec = int(self.result.group('dec'))
                                exp = int(self.result.group('exp'))
                                value = str(num * math.pow(10, exp) + dec)
                                line = line.replace("," + asym + ",", "," + value + ",")                                
                                asym = value
                                
                            
                            if npath == "Timeout":
                                line = line.replace("Timeout", asym)
                                
                            if re.match(r".*,0,.*", line):
                                print("skipping: " + line)                                
                                continue
                                
                            if re.match(r"^1$", asym):
                                cls = ',1'
                                tofile = c1file
                            elif re.match(r"[\d\*\^\.]+", asym):
                                cls = ',1gt'
                                tofile = cgt1file
                            else:
                                print("fix: " + line)
                                cls = ',c please fix me'
                                tofile = fixfile
                                #raise Exception("check constant extraction")
                                
                            cls_line = line.strip() + cls
                            
                        elif _type == 'Polynomial':
                            
                            if asym == "0." or asym == "0":
                                terms = func.split('+')
                                fix_asym = terms[-1].strip()
                                
                                if asym == "0.":
                                    line = line.replace("Polynomial,0.,", "Polynomial," + fix_asym + ",")
                                else:
                                    line = line.replace("Polynomial,0,", "Polynomial," + fix_asym + ",")
                                asym = fix_asym
                                
                            if re.match(r".*,0,.*", line):
                                print("skipping: " + line)                             
                                continue

                            if re.match(r".*n\^\d{2,}.$", asym):
                                cls = ',p4gte'
                                tofile = pgte4file                              
                            elif re.match(r".*n$", asym):
                                cls = ',p1'
                                tofile = p1file
                            elif re.match(r".*n\^2.$", asym):
                                cls = ',p2'
                                tofile = p2file
                            elif re.match(r".*n\^3.$", asym):
                                cls = ',p3'
                                tofile = p3file
                            elif re.match(r".*n\^\d+.$", asym):
                                cls = ',p4gte'
                                tofile = pgte4file
                            else:
                                print("fix: " + line)
                                cls = ',p please fix me'
                                tofile = fixfile
                                #raise Exception("check polynimal extraction")
                                
                            cls_line = line.strip() + cls
                            
                        elif _type == 'Exponential':
                            if asym == "0." or asym == "0":
                                terms = func.split('+')
                                fix_asym = terms[-1].strip()
                                if asym == "0.":
                                    line = line.replace("Exponential,0.,", "Exponential," + fix_asym + ",")                            
                                else:
                                    line = line.replace("Exponential,0,", "Exponential," + fix_asym + ",") 
                                asym = fix_asym
                            
                            if re.match(r".*,0,.*", line):
                                print("skipping: " + line)                           
                                continue
                                      
                            if re.match(r".*[\*,]1\.?\^.*n.*", asym):
                                print("error: base 1 is not exponential" + line)
       
                            if re.match(r".*\*?\d{2,}\.\d*\^.*n.*", asym):
                                cls = ',e4gte'
                                tofile = egte4file                    
                            elif re.match(r".*\*?1\.\d*\^.*n.*", asym):
                                cls = ',e1_2'
                                tofile = e1file
                            elif re.match(r".*\*?2\.\d*\^.*n.*", asym):
                                cls = ',e2_3'
                                tofile = e2file
                            elif re.match(r".*\*?3\.\d*\^.*n.*", asym):
                                cls = ',e3_4'
                                tofile = e3file
                            elif re.match(r".*\*?[\d.]+\^.*n.*", asym):
                                cls = ',e4gte'
                                tofile = egte4file
                            else:
                                print ("fix: " + line)
                                cls = ',e please fix me'
                                tofile = fixfile
                                #raise Exception("check exponential extraction")
                            cls_line = line.strip() + cls
                        
                        else:
                            print("fix: " + line)
                            cls = 'no class'
                            tofile = fixfile
                            
                        tofile.write(cls_line + '\n')    
                        outfile.write(cls_line + '\n')
                        
            
            outfile.close()
            c1file.close()
            cgt1file.close()
            p1file.close()
            p2file.close()
            p3file.close()
            pgte4file.close()
            e1file.close()
            e2file.close()
            e3file.close()
            egte4file.close()
            fixfile.close()
        self.log.i("end")    

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["input=", "output="])
    except getopt.GetoptError:
        print('test.py -i <input> -o <output>')
        print('*input can be a file or folder')
      #sys.exit(2)
    
    arg_input = None
    arg_output= None
    cmd_option = ""
    ext = "*.csv"
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <input> -o <output>')        
            sys.exit()
        elif opt in ("-i", "--input"):
            arg_input = arg
        elif opt in ("-o", "--output"):
            arg_output = arg
            
    classifier = Classifier(input_path=arg_input, output_path=arg_output, ext=ext, TAG="Classifier")
    classifier.run(options=cmd_option)

if __name__ == "__main__":
   main(sys.argv[1:])
