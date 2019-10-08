# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 22:20:01 2014

@author: baki
"""

import shlex
from subprocess import Popen, PIPE
import shutil

from langToCFG.javaextractor.Log import Log

class Shell:
    def __init__(self, TAG=""):
        self.log = Log(TAG=TAG)
        self.current_process = None
        self.process_output = None

    def setTag(self, tag):
        self.log.setTag(tag)
        
    def runcmd(self, cmd, cwd=None, shell=False):
        self.log.v("cmd: {}\n  with params: cwd={}, shell={}".format(cmd, cwd, shell))    
        args = shlex.split(cmd)
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=cwd, shell=shell)
        out, err = p.communicate()
        if out:
            self.log.v("cmd output: {}\n".format(out))
        if err:    
            self.log.v("cmd output: {}\n".format(err))             

        return out, err
        
    def runcmdBgrnd(self, cmd, out=PIPE, cwd=None, shell=False):
        self.log.v("cmd: {}\n  with params: out={}, cwd={}, shell={}".format(cmd, out, cwd, shell))
        redirect_to = out        
        if out is not PIPE:
            redirect_to = open(out, "w")
        args = shlex.split(cmd)
        p = Popen(args, stdout=redirect_to, stderr=redirect_to, cwd=cwd, shell=shell)
        self.current_process = p     
        self.process_output = redirect_to        
        return p
        
    def kill(self, process=None):
        if process is None:
            process = self.current_process
        process and process.kill()
        self.process_output and self.process_output.close()
        self.current_process = None
    
    def terminate(self, process=None):
        if process is None:
            process = self.current_process
        process and process.terminate()
        self.process_output and self.process_output.close()
        self.current_process = None
    
    def runGrep(self, search, subject, options):
        cmd = "grep {} \"{}\" {}".format(options, search, subject)
        return self.runcmd(cmd)
        
    def rm(self, name):
        cmd = "rm {}".format(name)
        return self.runcmd(cmd)
        
    def rmdir(self, name):
        cmd = "rmdir {}".format(name)
        return self.runcmd(cmd)
    
    def rmrdir(self, name):
        cmd = "rm -r {}".format(name)
        return self.runcmd(cmd)
        
    def mv(self, src, dst):
        cmd = "mv {} {}".format(src, dst)
        return self.runcmd(cmd)
    
    def cp(self, src, dst):
        cmd = "cp -r {} {}".format(src, dst)
        return self.runcmd(cmd)
        
    def mkdir(self, name):
        cmd = "mkdir {} -p".format(name)
        return self.runcmd(cmd)
        
    def clean(self, name):
        self.rmrdir(name)
        self.mkdir(name)
        