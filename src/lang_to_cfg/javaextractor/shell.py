# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 22:20:01 2014.

@author: baki
"""

import shlex
from subprocess import Popen, PIPE

from log import Log


class Shell:
    """Functions like a basic bash shell."""

    def __init__(self, TAG=""):
        """Create a new instance of Shell."""
        self.log = Log(tag=TAG)
        self.current_process = None
        self.process_output = None

    def set_tag(self, tag):
        """Set the logger tag."""
        self.log.set_tag(tag)

    def runcmd(self, cmd, cwd=None, shell=False):
        """Run a command in the shell."""
        self.log.v_msg("cmd: {}\n  with params: cwd={}, shell={}".format(cmd, cwd, shell))
        args = shlex.split(cmd)
        process = Popen(args, stdout=PIPE, stderr=PIPE, cwd=cwd, shell=shell)
        out, err = process.communicate()
        if out:
            self.log.v_msg("cmd output: {}\n".format(out))
        if err:
            self.log.v_msg("cmd output: {}\n".format(err))

        return out, err

    def runcmd_bgrnd(self, cmd, out=PIPE, cwd=None, shell=False):
        """Run a command in a new process to prevent blocking."""
        cmd_to_log = "cmd: {}\n  with params: out={}, cwd={}, shell={}".format(
            cmd, out, cwd, shell)
        self.log.v_msg(cmd_to_log)
        redirect_to = out
        if out is not PIPE:
            redirect_to = open(out, "w")
        args = shlex.split(cmd)
        process = Popen(args, stdout=redirect_to, stderr=redirect_to,
                        cwd=cwd, shell=shell)
        self.current_process = process
        self.process_output = redirect_to
        return process

    def kill(self, process=None):
        """Kill the specificed process (or current process if not specified)."""
        if process is None:
            process = self.current_process

        # Assign to _ to avoid linter issues.
        _ = process and process.kill()
        _ = self.process_output and self.process_output.close()
        self.current_process = None

    def terminate(self, process=None):
        """Alias for self.kill."""
        self.kill(process)

    def run_grep(self, search, subject, options):
        """Execute a grep search."""
        cmd = "grep {} \"{}\" {}".format(options, search, subject)
        return self.runcmd(cmd)

    def rm_cmd(self, name):
        """Remove a file."""
        cmd = "rm {}".format(name)
        return self.runcmd(cmd)

    def rmdir_cmd(self, name):
        """Remove a directory non-recursively."""
        cmd = "rmdir {}".format(name)
        return self.runcmd(cmd)

    def rmrdir_cmd(self, name):
        """Remove a directory recursively."""
        cmd = "rm -r {}".format(name)
        return self.runcmd(cmd)

    def mv_cmd(self, src, dst):
        """Move a directory."""
        cmd = "mv {} {}".format(src, dst)
        return self.runcmd(cmd)

    def cp_cmd(self, src, dst):
        """Copy a file or file-like object to another location."""
        cmd = "cp -r {} {}".format(src, dst)
        return self.runcmd(cmd)

    def mkdir_cmd(self, name):
        """Move a file or file-like object to another location."""
        cmd = "mkdir {} -p".format(name)
        return self.runcmd(cmd)

    def clean_cmd(self, name):
        """Remove everything from an existing directory."""
        self.rmrdir_cmd(name)
        self.mkdir_cmd(name)
