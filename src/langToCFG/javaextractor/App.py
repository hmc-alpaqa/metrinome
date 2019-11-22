# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 00:27:11 2014

@author: baki
"""

import glob2
import os
from Log import Log
from Env import Env
from langToCFG.javaextractor.Shell import Shell

class App:
     
    def __init__(self, input_file, output_folder=None, display_log_output=True, ext="*.jar", export=True):
        self.log = Log(TAG="APP", display_output=display_log_output)        
        self.shell = Shell()
        self.input_file = input_file
        self.output_folder = Env.OUTPUT_PATH
        if output_folder != None:
            self.output_folder = output_folder
        self.export = export
    
    def __jarToClasses(self, jar_file, cwd=Env.TMP_PATH):
        self.log.i("extracting jar file")
        self.shell.clean(cwd)
        cmd = f"jar xf {jar_file}"
        self.shell.runcmd(cmd, cwd=cwd)
        
    def __runCFGExtractorLive(self, input_class): 
        project = Env.get_basename(input_class)
        output_path = Env.get_output_path(project)
        self.shell.clean(output_path)
        if self.export:
            pass 
        #    additional_cmd = f"-i {input_classes} -o {output_path} -p test"
        else:
            pass
            # additional_cmd = f"-i {input_classes} -p test"
        cmd = f"java -jar {Env.CFG_EXTRACTOR} -i {input_class.strip()} -o {output_path.strip()}"
        print(f"===== HERE IS THE COMMAND === {cmd}") 
        self.shell.runcmd(cmd)

    def __runCFGExtractor(self, main_class, input_classes, project): 
        output_path = Env.get_output_path(project)
        self.shell.clean(output_path)
        if self.export:
            additional_cmd = f"-i {input_classes} -o {output_path} -p test"
        else:
            additional_cmd = f"-i {input_classes} -p test"
        cmd = f"java -jar {Env.CFG_EXTRACTOR} {additional_cmd}"
        
        self.shell.runcmd(cmd)
    
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
    
    def runLive(self, jar=True): 
        self.log.i("start")
        self.shell.clean(Env.TMP_PATH)     
        if self.file_name.endswith('sources.jar') or self.file_name.endswith('javadoc.jar')  or self.file_name.endswith('tests.jar'):
            return
        self.log.v("processing {}".format(self.file_name))
        if jar: 
            self.__jarToClasses(self.file_name)
            
        self.__runCFGExtractorLive(self.file_name)        
        self.log.v("finished: please check {} folder for the generated CFGs".format(Env.OUTPUT_PATH))
