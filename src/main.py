"""Run the APC REPL."""

from __future__ import annotations

import argparse
import importlib
import logging
import os
import readline
from cmd import Cmd
from typing import Any, List, Tuple

import core.command as command
from core.command import Options
from core.log import Colors, Log

TESTING_MODE = True

# pylint does not understand decorators.
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-public-methods


class Prompt(Cmd):
    """A wrapper for the REPL that allows us to create do_reload."""

    def __init__(self, curr_path: str, debug_mode: bool, multi_threaded: bool = False) -> None:
        """Create a new instance of the REPL."""
        self.command = command.Command(curr_path, debug_mode, multi_threaded, self)
        self.logger = self.command.logger
        if TESTING_MODE:
            setattr(self, "do_reload", self.reload)

        self.prompt = f"{Colors.OKGREEN.value}{self.command.curr_path}{Colors.ENDC.value} > "

        # Dynamically create all of the wrapper functions.
        Prompt.create_commands(self)
        super().__init__()

    def get_names(self) -> List[str]:
        """Get names of all attributes and commands the repl knows about."""
        return super().get_names() + [f"do_{x}" for x in Options.commands]

    def postcmd(self, stop: int, line: str) -> bool:
        """Execute after any command is executed to update the prompt."""
        self.prompt = f"{Colors.OKGREEN.value}{self.command.curr_path}{Colors.ENDC.value} > "
        return False

    # pylint: disable=unused-argument
    def complete_file_path(self, text: str, line: str,
                           begin: int, start: int,
                           folders_only: bool = False) -> List[str]:
        """Enhanced auto-completion for the REPL."""
        # Try to do tab completion on a directory. Text contains the latest paremeter
        # text only contains the latest segment, which splits on / (and other characters)
        # Find the most recent space.
        starting_idx = None
        slash_index = None
        for i, char in enumerate(reversed(line)):
            if char == "/" and slash_index is None:
                slash_index = len(line) - i
            if char == " ":
                starting_idx = len(line) - i
                break
        full_arg = line[starting_idx:]

        if os.path.isdir(full_arg):
            # If this is a folder, get all things in this folder.
            if not folders_only:
                return os.listdir(full_arg)

            return [path for path in os.listdir(full_arg) if
                    os.path.isdir(os.path.join(full_arg, path))]

        # Get the path up to the last "/".
        folder_path = self.command.curr_path
        if slash_index is not None:
            folder_path = line[starting_idx:slash_index]
        logging.info(f"the folder path is: {folder_path}")
        if not folders_only:
            logging.info(f"found {os.listdir(folder_path)}")
            return [match for match in os.listdir(folder_path) if match.startswith(text)]

        return [match for match in os.listdir(folder_path)
                if match.startswith(text) and os.path.isdir(os.path.join(folder_path, match))]

    def complete_list(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Auto-completion for the list command."""
        options = ["metrics", "graphs", "KLEE"]
        return [match for match in options if match.startswith(text)]

    def complete_metrics(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Auto-completion for the metrics command."""
        options = list(self.command.data.graphs.keys())
        return [opt for opt in options if opt.startswith(text)]

    def complete_repl_objects(self, line: str) -> List[str]:
        """Auto-completion for commands that use objects the REPL knows about."""
        args = line.split(" ")
        logging.info(args)
        if len(args) == 2:
            options = ["graph", "metric", "klee"]
            return [opt for opt in options if opt.startswith(args[1])]

        if args[1] == "graph":
            options = list(self.command.data.graphs.keys())
            return [opt for opt in options if opt.startswith(args[2])]

        if args[1] == "metric":
            options = list(self.command.data.metrics.keys())
            return [opt for opt in options if opt.startswith(args[2])]

        if args[1] == "klee":
            stats_list = list(self.command.data.klee_stats.keys())
            formatted_files_list = list(self.command.data.klee_formatted_files.keys())
            bc_files_list = list(self.command.data.bc_files.keys())
            options = stats_list + formatted_files_list + bc_files_list
            return [opt for opt in options if opt.startswith(args[2])]

        return []

    def complete_import(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Auto-completion for the import command."""
        return self.complete_file_path(text, line, begin, end, False)

    def complete_show(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Auto-completion for the show command."""
        return self.complete_repl_objects(line)

    def complete_delete(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Auto-complete for the delete command."""
        return self.complete_repl_objects(line)

    def complete_cd(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Completion for the cd command."""
        return self.complete_file_path(text, line, begin, end, True)

    def complete_rm(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Completion for the rm command."""
        return self.complete_file_path(text, line, begin, end, False)

    def complete_mv(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Completion for the mv command."""
        return []

    def complete_export(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Completion for the export command."""
        return []

    def complete_convert(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Completion for the convert command."""
        return self.complete_file_path(text, line, begin, end, False)

    def complete_to_klee_format(self, text: str, line: str, begin: int, end: int) -> List[str]:
        """Completion for the to_klee_format command."""
        return self.complete_file_path(text, line, begin, end, False)

    def do_convert(self, arguments: str) -> None:
        """Wrap convert command."""
        self.command.do_convert(arguments)

    def reload(self, arguments: str) -> None:
        """Reload the modules."""
        metrics = self.command.data.metrics
        graphs = self.command.data.graphs
        klee_stats = self.command.data.klee_stats
        klee_formatted_files = self.command.data.klee_formatted_files
        bc_files = self.command.data.bc_files

        debug = self.command.debug_mode
        importlib.reload(command)
        if arguments.strip() == "debug":
            debug = True
        elif arguments.strip() == "user":
            debug = False

        self.command = command.Command(self.command.curr_path, debug,
                                       self.command.multi_threaded, self)

        self.command.data.graphs = graphs
        self.command.data.metrics = metrics
        self.command.data.klee_stats = klee_stats
        self.command.data.klee_formatted_files = klee_formatted_files
        self.command.data.bc_files = bc_files

    @staticmethod
    def _create_command(prompt: Prompt, command_name: str) -> None:
        """Create a single do_<command> in Prompt."""
        func_name = f"do_{command_name}"
        wrapped_func = getattr(prompt.command, func_name)

        def cmd(args: str) -> None:
            flags, f_args, valid_args = Prompt.check_args(command_name, args, prompt.logger)
            if valid_args:
                wrapped_func(flags, *f_args)

        # Create the do_<command_name> function in Prompt.
        cmd.__doc__ = wrapped_func.__doc__
        setattr(prompt, func_name, cmd)

    @staticmethod
    def create_commands(prompt: Prompt) -> None:
        """Create all of the do_<command> wrappers in Prompt."""
        for command_name in Options.commands:
            Prompt._create_command(prompt, command_name)

    @staticmethod
    def check_args(command_name: str, args: str, logger: Log) -> Tuple[Options, List[Any], bool]:
        """Parse the string passed in from the command line and obtain flags / parameters."""
        opts = Options.commands[command_name]
        var_args = opts.get_var_args()
        check_recursive = opts.get_recursive()

        num_args, err = opts.get_num_args(), opts.get_err()

        args_list = args.strip().split()
        if len(args_list) < num_args:
            logger.v_msg(err)
            return Options(), [], False

        if len(args_list) > num_args:
            if check_recursive:
                recursive_flag = args_list[0] == "-r" or args_list[0] == "--recursive"
                if not var_args and len(args) == num_args + 1 and recursive_flag:
                    return Options(True), args_list[1:], True

                if var_args and recursive_flag:
                    return Options(True), args_list[1:], True

            if var_args:
                return Options(), args_list, True

            logger.v_msg("Too many arguments provided.")
            return Options(), [], False

        if check_recursive:
            return Options(False), args_list, True

        return Options(), args_list, True


def main() -> None:
    """Parse command line arguments and initialize the REPL."""
    parser = argparse.ArgumentParser(description='Arguments for APC REPL.')
    parser.add_argument('--debug', dest='debug_mode',
                        action='store_true', default=False,
                        help='Turn on debugging mode for more verbose output')
    # parser.add_argument('--multi-threaded', dest="multi_threaded", action='store_true', default=False,
    # help="Turn this on to speed up REPL functions through parallelism.")
    parsed_args = parser.parse_args()

    logging.basicConfig(filename='repl_log.log', level=logging.DEBUG)
    try:
        readline.read_history_file()
    except FileNotFoundError:
        pass
    prompt = Prompt("/app/code",
                    parsed_args.debug_mode)
    prompt.cmdloop(f"{Colors.TITLE.value}" + r"""

             _        _
  /\/\   ___| |_ _ __(_)_ __   ___  _ __ ___   ___
 /    \ / _ \ __| '__| | '_ \ / _ \| '_ ` _ \ / _ \
/ /\/\ \  __/ |_| |  | | | | | (_) | | | | | |  __/
\/    \/\___|\__|_|  |_|_| |_|\___/|_| |_| |_|\___|

""" + f"{Colors.ENDC.value}\nStarting the REPL...")


if __name__ == "__main__":
    main()
