# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 00:27:11 2014

@author: baki
"""

from log import Log
from env import Env
from lang_to_cfg.javaextractor.shell import Shell

class App:
    '''
    App interacts with the java program that extracts CFGs
    from Java source code.
    '''

    def __init__(self, input_file, output_folder=None, display_log_output=True,
                 ext="*.jar", export=True):
        '''
        Create a new instance of the App.
        '''
        self.log = Log(tag="APP", display_output=display_log_output)
        self.shell = Shell()
        self.input_file = input_file
        self.output_folder = Env.OUTPUT_PATH
        if output_folder is not None:
            self.output_folder = output_folder
        self.ext = ext
        self.export = export

    def __jar_to_classes(self, jar_file, cwd=Env.TMP_PATH):
        '''
        '''
        self.log.i_msg("extracting jar file")
        self.shell.clean_cmd(cwd)
        cmd = f"jar xf {jar_file}"
        self.shell.runcmd(cmd, cwd=cwd)

    def __run_cfg_extractor_live(self, input_class):
        '''
        '''
        project = Env.get_basename(input_class)
        output_path = Env.get_output_path(project)
        self.shell.clean_cmd(output_path)
        if self.export:
            pass
        #    additional_cmd = f"-i {input_classes} -o {output_path} -p test"
        else:
            pass
            # additional_cmd = f"-i {input_classes} -p test"
        cmd = f"java -jar {Env.CFG_EXTRACTOR} -i {input_class.strip()}" + \
              f" -o {output_path.strip()}"
        print(f"===== HERE IS THE COMMAND === {cmd}")
        self.shell.runcmd(cmd)

    def __run_cfg_extractor(self, main_class, input_classes, project):
        '''
        Run the java program that will extract the CFG from Java classes.
        '''
        print(f"Got main_class: {main_class}, but not used.")
        output_path = Env.get_output_path(project)
        self.shell.clean_cmd(output_path)
        if self.export:
            additional_cmd = f"-i {input_classes} -o {output_path} -p test"
        else:
            additional_cmd = f"-i {input_classes} -p test"
        cmd = f"java -jar {Env.CFG_EXTRACTOR} {additional_cmd}"

        self.shell.runcmd(cmd)

    def get_result_line(self, output):
        '''
        Parse results obtained by the App of a specific format.
        '''
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

    def run_live(self, jar=True):
        '''
        A wrapper around __run_cfg_extractor_live. This is what should actually be called by
        the REPL as it does additional checks and logging.
        '''
        self.log.i_msg("start")
        self.shell.clean_cmd(Env.TMP_PATH)
        if self.input_file.endswith('sources.jar') or self.input_file.endswith('javadoc.jar') \
           or self.input_file.endswith('tests.jar'):
            return

        self.log.v_msg("processing {}".format(self.input_file))
        if jar:
            self.__jar_to_classes(self.input_file)

        self.__run_cfg_extractor_live(self.input_file)
        self.log.v_msg("finished: please check {} folder for the \
                       generated CFGs".format(Env.OUTPUT_PATH))
