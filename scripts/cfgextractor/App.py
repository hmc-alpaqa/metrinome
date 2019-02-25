# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 00:27:11 2014

@author: baki
"""

import glob2

import os
from Log import Log
from Env import Env
from Shell import Shell

class App:
     
    def __init__(self, input_folder, output_folder=None, ext="*.jar"):
        self.log = Log(TAG="APP")        
        self.shell = Shell()
        self.file_list = [input_folder]
        if os.path.isdir(input_folder):
            self.file_list = sorted(glob2.glob(Env.join_path(input_folder, "**/" + ext)))
        self.input_folder = input_folder
        self.output_folder = Env.OUTPUT_PATH
        if output_folder != None:
            self.output_folder = output_folder
            
    
    def __jarToClasses(self, jar_file, cwd=Env.TMP_PATH):
        self.log.i("extracting jar file")
        self.shell.clean(cwd)
        cmd = "jar xf {}".format(jar_file)
        self.shell.runcmd(cmd, cwd=cwd)
        
    def __runCFGExtractor(self, main_class, input_classes, project): 
        output_path = Env.get_output_path(project)
        self.shell.clean(output_path)
        additional_cmd = "-i {} -o {} -p {}".format(input_classes, output_path, "test")
        cmd = "java -jar {} {}".format(
                    Env.CFG_EXTRACTOR, additional_cmd)
        
        self.shell.runcmd(cmd)
    
    def __runPathComplexity(self, cfg_file_path):
        cmd = "/usr/bin/timeout -s 9 20 math -script {} {}".format(Env.MATH_SCRIPT, cfg_file_path)
        return self.shell.runcmd(cmd)
    
    def getResultLine(self, output):
        columns = output.strip(' \t\n\r,').split(',')
        results = []
        for col in columns:
            if col == "":
                continue
            if 'TeXForm' in col:              
                results.append(col[8:-1])
            else:
                results.append(col)
        
        return ",".join(results)
            
    def run(self, option):
        self.log.i("start")
        if option == "":        
            self.shell.clean(Env.TMP_PATH)     
            for file_name in self.file_list:
                if file_name.endswith('sources.jar') or file_name.endswith('javadoc.jar')  or file_name.endswith('tests.jar'):
                    continue
                self.log.v("processing {}".format(file_name))
                self.__jarToClasses(file_name)
                self.__runCFGExtractor("Extractor", Env.TMP_PATH, Env.get_basename(file_name))
                
            self.log.v("finished: please check {} folder for the generated CFGs".format(Env.OUTPUT_PATH))
        elif option == "-c":
            print 'option is not used anymore'            
            #output_csv = Env.get_output_path("complexity_result.csv")
            #outfile =  open(output_csv, 'w')
            
            #for file_name in self.file_list:
               #self.log.v("processing {}".format(file_name))
               #out,err = self.__runPathComplexity(file_name)
               #result = self.getResultLine(out+err)
               #if result.strip() == "":
               #    result = file_name
               #outfile.write("{}\n".format(result))
            #outfile.close()
    
        
    
        
    