"""Run the APC REPL."""

from __future__ import annotations

import argparse
import importlib
import logging
import os
import readline
from cmd import Cmd
from functools import wraps
from typing import Any, Callable, List

from core import command
from core.error_messages import (MISSING_FILENAME, MISSING_NAME,
                                 MISSING_TYPE_AND_NAME)
from core.log import Colors

TESTING_MODE = True

# pylint does not understand decorators.
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args
# pylint: disable=too-many-public-methods


def check_args(num_args: int,
               err: str,
               check_recursive: bool = False,
               var_args: bool = False
               ) -> Callable[[Callable[..., None]], Callable[[Prompt, str], None]]:
    """Create decorators that verify REPL functions have valid arguments (factory method)."""
    def decorator(func: Callable[..., None]) -> Callable[[Prompt, str], None]:
        @wraps(func)
        def wrapper(self: Prompt, args: str) -> None:
            args_list = args.strip().split()
            if len(args_list) < num_args:
                self.logger.v_msg(err)
                return

            if len(args_list) > num_args:
                if check_recursive:
                    recursive_flag = args_list[0] == "-r" or args_list[0] == "--recursive"
                    if not var_args and len(args) == num_args + 1 and recursive_flag:
                        func(self, True, *args_list[1:])
                        return

                    if var_args and recursive_flag:
                        func(self, True, *args_list[1:])
                        return

                if var_args:
                    func(self, *args_list)
                    return

                self.logger.v_msg("Too many arguments provided.")
            else:
                if check_recursive:
                    func(self, False, *args_list)
                else:
                    func(self, *args_list)

        return wrapper
    return decorator


class Prompt(Cmd):
    """A wrapper for the REPL that allows us to create do_reload."""

    def __init__(self, curr_path: str, debug_mode: bool, multi_threaded: bool) -> None:
        """Create a new instance of the REPL."""
        self.command = command.Command(curr_path, debug_mode, multi_threaded, self)
        self.logger = self.command.logger
        if TESTING_MODE:
            setattr(self, "do_reload", self.reload)

        self.prompt = f"{Colors.OKGREEN.value}{self.command.curr_path}{Colors.ENDC.value} > "

        super().__init__()

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

    @check_args(1, MISSING_FILENAME, check_recursive=True)
    def do_to_klee_format(self, *args: Any) -> None:
        """
        Create a klee-compatible file.

        Given a C file, create a new modified C file that is in the
        correct format to be converted to a bc file.
        """
        self.command.do_to_klee_format(*args)

    @check_args(1, "Must provide KLEE formatted name.")
    def do_klee_to_bc(self, *args: Any) -> None:
        """Given a C file in the correct format, generate a new .bc file from the given C file."""
        self.command.do_klee_to_bc(*args)

    @check_args(1, MISSING_FILENAME, check_recursive=False, var_args=True)
    def do_klee(self, *args: Any) -> None:
        """
        Execute the klee command on a .bc file.

        This will generate all of the tests automatically and store the resulting metadata
        (e.g. number of tests generated).

        Usage:
        klee <file>
        """
        self.command.do_klee(*args)

    @check_args(1, MISSING_FILENAME)
    def do_klee_replay(self, *args: Any) -> None:
        """
        Execute a test generated by KLEE given a klee test file.

        Usage:
        klee_replay <file>
        """
        self.command.do_klee_replay(*args)

    def do_convert(self, arguments: str) -> None:
        """
        Convert a file containing source code to a Graph object.

        The recursive flag (-r) can also be used.

        Usage:
        convert <file-like>
        convert -r <file-like>
        convert <file-like-1> <file-like-2> ... <file-like-n>
        """
        self.command.do_convert(arguments)

    @check_args(1, MISSING_FILENAME, check_recursive=True, var_args=True)
    def do_import(self, *args: Any) -> None:
        """
        Convert a .dot file representing a cfg into a Graph object.

        The recursive flag (-r) can also be used.

        Usage:
        import <file-like>
        import -r <file-like>
        import <file-like-1> <file-like-2> ... <file-like-n>
        """
        self.command.do_import(*args)

    @check_args(1, "Must specify object type to list (metrics, graphs, or KLEE type).")
    def do_list(self, *args: Any) -> None:
        """
        List all of the objects of a specific type (metrics, graphs, or a KLEE type).

        Usage:
        list <metrics/graphs/KLEE type>
        list *
        """
        self.command.do_list(*args)

    @check_args(2, "Must specify type (metric, graph, or any KLEE type) and name.")
    def do_show(self, *args: Any) -> None:
        """
        Show an object of some type (either metric, graph, or KLEE type).

        Usage
        show <metric/graph/KLEE type> <name>
        show <metric/graph/KLEE type> *
        """
        self.command.do_show(*args)

    @check_args(1, "Must provide graph name.")
    def do_metrics(self, *args: Any) -> None:
        """
        Compute all of the complexity matrics for a Graph object.

        Usage:
        metrics <name>
        metrics *
        """
        self.command.do_metrics(*args)

    @check_args(2, MISSING_TYPE_AND_NAME)
    def do_delete(self, *args: Any) -> None:
        """
        Delete an object (type Graph, Metrics, States, or KLEE type) from memory.

        Usage:
        delete <type> <name>
        """
        self.command.do_delete(*args)

    @check_args(2, MISSING_TYPE_AND_NAME)
    def do_export(self, *args: Any) -> None:
        """
        Save an object (type Graph, Metrics, Stats, KLEE type) to an output file.

        Usage:
        save <type> <name>
        """
        self.command.do_export(*args)

    @check_args(0, "Quit does not accept arguments.")
    def do_quit(self, *args: Any) -> None:
        """Quit the path complexity repl."""
        self.command.do_quit(*args)

    @check_args(1, MISSING_NAME)
    def do_cd(self, *args: Any) -> None:
        """Change the current working directory."""
        self.command.do_cd(*args)

    @check_args(0, "Cannot accept arguments.")
    def do_ls(self, *args: Any) -> None:
        """List the files in the current directory."""
        self.command.do_ls(*args)

    @check_args(2, "Missing name one and name two.")
    def do_mv(self, *args: Any) -> None:
        """Move a file from one directory to another."""
        self.command.do_mv(*args)

    @check_args(1, "Missing name of file/directory to delete.",
                check_recursive=True, var_args=True)
    def do_rm(self, *args: Any) -> None:
        """Remove files permanently."""
        self.command.do_rm(*args)

    @check_args(1, "Missing directory name.")
    def do_mkdir(self, *args: Any) -> None:
        """Make a new directory."""
        self.command.do_mkdir(*args)

    @check_args(0, "Cannot accept arguments.")
    def do_pwd(self, *args: Any) -> None:
        """Print the name of the current directory."""
        self.command.do_pwd(*args)

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


def main() -> None:
    """Parse command line arguments and initialize the REPL."""
    parser = argparse.ArgumentParser(description='Arguments for APC REPL.')
    parser.add_argument('--debug', dest='debug_mode',
                        action='store_true', default=False,
                        help='Turn on debugging mode for more verbose output')
    parser.add_argument('--multi-threaded', dest="multi_threaded",
                        action='store_true', default=False,
                        help="Turn this on to speed up REPL functions through parallelism.")
    parsed_args = parser.parse_args()

    logging.basicConfig(filename='repl_log.log', level=logging.DEBUG)
    try:
        readline.read_history_file()
    except FileNotFoundError:
        pass
    prompt = Prompt("/app/code",
                    parsed_args.debug_mode, parsed_args.multi_threaded)
    prompt.cmdloop(r"""

             _        _
  /\/\   ___| |_ _ __(_)_ __   ___  _ __ ___   ___
 /    \ / _ \ __| '__| | '_ \ / _ \| '_ ` _ \ / _ \
/ /\/\ \  __/ |_| |  | | | | | (_) | | | | | |  __/
\/    \/\___|\__|_|  |_|_| |_|\___/|_| |_| |_|\___|


Starting the REPL...
""")


if __name__ == "__main__":
    main()
