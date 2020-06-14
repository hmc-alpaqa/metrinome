"""Run the APC REPL."""

import readline
import logging
import argparse
import importlib
from cmd import Cmd
import os
from typing import List
import command
from log import Colors

TESTING_MODE = True

# pylint does not understand decorators.
# pylint: disable=no-value-for-parameter
# pylint: disable=too-many-function-args
# pylint: disable=too-many-public-methods


class MyPrompt(Cmd):
    """A wrapper for the REPL that allows us to create do_reload."""

    def __init__(self, curr_path: str, debug_mode: bool, multi_threaded: bool) -> None:
        """Create a new instance of the REPL."""
        self.command = command.Command(curr_path, debug_mode, multi_threaded, self)
        if TESTING_MODE:
            setattr(self, "do_reload", self.reload)

        self.prompt = f"{Colors.OKGREEN.value}{self.command.curr_path}{Colors.ENDC.value} > "

        super(MyPrompt, self).__init__()

    def postcmd(self, stop, line) -> bool:
        """Execute after any command is executed to update the prompt."""
        self.prompt = f"{Colors.OKGREEN.value}{self.command.curr_path}{Colors.ENDC.value} > "
        return False

    # pylint: disable=unused-argument
    def complete_file_path(self, text: str, line: str,
                           begin, start, folders_only=False) -> List[str]:
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

    def complete_list(self, text: str, line: str, begin, end) -> List[str]:
        """Auto-completion for the list command."""
        options = ["metrics", "graphs", "KLEE"]
        return [match for match in options if match.startswith(text)]

    def complete_metrics(self, text: str, line: str, begin, end) -> List[str]:
        """Auto-completion for the metrics command."""
        options = list(self.command.data.graphs.keys())
        return [opt for opt in options if opt.startswith(text)]

    def complete_repl_objects(self, line: str):
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

    def complete_import(self, text: str, line: str, begin, end) -> List[str]:
        """Auto-completion for the import command."""
        return self.complete_file_path(text, line, begin, end, False)

    def complete_show(self, text, line, begin, end) -> List[str]:
        """Auto-completion for the show command."""
        return self.complete_repl_objects(line)

    def complete_delete(self, text, line, begin, end) -> List[str]:
        """Auto-complete for the delete command."""
        return self.complete_repl_objects(line)

    def complete_cd(self, text, line, begin, end) -> List[str]:
        """Completion for the cd command."""
        return self.complete_file_path(text, line, begin, end, True)

    def complete_convert(self, text, line, begin, end) -> List[str]:
        """Completion for the convert command."""
        return self.complete_file_path(text, line, begin, end, False)

    def complete_to_klee_format(self, text, line, begin, end) -> List[str]:
        """Completion for the to_klee_format command."""
        return self.complete_file_path(text, line, begin, end, False)

    def do_to_klee_format(self, arguments: str) -> None:
        """
        Create a klee-compatible file.

        Given a C file, create a new modified C file that is in the
        correct format to be converted to a bc file.
        """
        self.command.do_to_klee_format(arguments)

    def do_klee_to_bc(self, arguments: str) -> None:
        """Given a C file in the correct format, generate a new .bc file from the given C file."""
        self.command.do_klee_to_bc(arguments)

    def do_klee(self, arguments: str) -> None:
        """
        Execute the klee command on a .bc file.

        This will generate all of the tests automatically and store the resulting metadata
        (e.g. number of tests generated).

        Usage:
        klee <file>
        """
        self.command.do_klee(arguments)

    def do_klee_replay(self, arguments: str) -> None:
        """
        Execute a test generated by KLEE given a klee test file.

        Usage:
        klee_replay <file>
        """
        self.command.do_klee_replay(arguments)

    # def do_clean_klee(self, arguments: str) -> None:
    #    """Remove all of the files generated by klee, including the generated tests."""
    #    self.command.do_clean_klee_files(arguments)

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

    def do_import(self, arguments) -> None:
        """
        Convert a .dot file representing a cfg into a Graph object.

        The recursive flag (-r) can also be used.

        Usage:
        import <file-like>
        import -r <file-like>
        import <file-like-1> <file-like-2> ... <file-like-n>
        """
        self.command.do_import(arguments)

    def do_list(self, arguments) -> None:
        """
        List all of the objects of a specific type (metrics, graphs, or a KLEE type).

        Usage:
        list <metrics/graphs/KLEE type>
        list *
        """
        self.command.do_list(arguments)

    def do_show(self, arguments) -> None:
        """
        Show an object of some type (either metric, graph, or KLEE type).

        Usage
        show <metric/graph/KLEE type> <name>
        show <metric/graph/KLEE type> *
        """
        self.command.do_show(arguments)

    def do_metrics(self, arguments: str) -> None:
        """
        Compute all of the complexity matrics for a Graph object.

        Usage:
        metrics <name>
        metrics *
        """
        self.command.do_metrics(arguments)

    # def do_analyze(self, arguments: str) -> None:
    #     """
    #     Perform statistical analysis on a set of generated metrics.

    #     Usage:
    #     analyze <metric names>
    #     """
    #     self.command.do_analyze(arguments)

    def do_delete(self, arguments: str) -> None:
        """
        Delete an object (type Graph, Metrics, States, or KLEE type) from memory.

        Usage:
        delete <type> <name>
        """
        self.command.do_delete(arguments)

    def do_export(self, arguments: str) -> None:
        """
        Save an object (type Graph, Metrics, Stats, KLEE type) to an output file.

        Usage:
        save <type> <name>
        """
        self.command.do_export(arguments)

    def do_quit(self, arguments: str) -> None:
        """Quit the path complexity repl."""
        self.command.do_quit(arguments)

    def do_cd(self, arguments: str) -> None:
        """Change the current working directory."""
        self.command.do_cd(arguments)

    def do_ls(self, arguments) -> None:
        """List the files in the current directory."""
        self.command.do_ls(arguments)

    def do_mv(self, arguments: str) -> None:
        """Move a file from one directory to another."""
        self.command.do_mv(arguments)

    def do_rm(self, arguments: str) -> None:
        """Remove files permanently."""
        self.command.do_rm(arguments)

    def do_mkdir(self, arguments: str) -> None:
        """Make a new directory."""
        self.command.do_mkdir(arguments)

    def do_pwd(self, arguments: str) -> None:
        """Print the name of the current directory."""
        self.command.do_pwd(arguments)

    def reload(self, arguments) -> None:
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


def main():
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
    prompt = MyPrompt(f"/app/code",
                      parsed_args.debug_mode, parsed_args.multi_threaded)
    prompt.cmdloop(r"""

            _       _____          ____
     /\    | |     |  __ \  /\    / __ \     /\
    /  \   | |     | |__) |/  \  | |  | |   /  \
   / /\ \  | |     |  ___// /\ \ | |  | |  / /\ \
  / ____ \ | |____ | |   / ____ \| |__| | / ____ \
 /_/    \_\|______||_|  /_/    \_\\___\_\/_/    \_\

Starting the REPL...
    """)


if __name__ == "__main__":
    main()
