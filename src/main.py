"""Run the APC REPL."""

import readline
import logging
import argparse
import importlib
from cmd import Cmd
import command

TESTING_MODE = True


class MyPrompt(Cmd):
    """A wrapper for the REPL that allows us to create do_reload."""

    def __init__(self, debug_mode: bool) -> None:
        """Create a new instance of the REPL."""
        self.command = command.Command(debug_mode, self)
        if TESTING_MODE:
            setattr(self, "do_reload", self.reload)

        super(MyPrompt, self).__init__()

    def do_to_klee_format(self, arguments):
        """
        Create a klee-compatible file.

        Given a C file, create a new modified C file that is in the
        correct format to be converted to a bc file.
        """
        self.command.do_to_klee_format(arguments)

    def do_klee_to_bc(self, arguments):
        """Given a C file in the correct format, generate a new .bc file from the given C file."""
        self.command.do_klee_to_bc(arguments)

    def do_klee(self, arguments):
        """
        Execute the klee command on a .bc file.

        This will generate all of the tests automatically and store the resulting metadata
        (e.g. number of tests generated).

        Usage:
        klee <file>
        """
        self.command.do_klee(arguments)

    def do_klee_replay(self, arguments):
        """
        Execute a test generated by KLEE given a klee test file.

        Usage:
        klee_replay <file>
        """
        self.command.do_klee_replay(arguments)

    def do_clean_klee(self, arguments):
        """Remove all of the files generated by klee, including the generated tests."""
        self.command.do_clean_klee_files(arguments)

    def do_convert(self, arguments):
        """
        Convert a file containing source code to a Graph object.

        The recursive flag (-r) can also be used.

        Usage:
        convert <file-like>
        convert -r <file-like>
        convert <file-like-1> <file-like-2> ... <file-like-n>
        """
        self.command.do_convert(arguments)

    def do_list(self, arguments):
        """
        List all of the objects of a specific type (either metrics or graphs).

        Usage:
        list <metrics/graphs>
        list *
        """
        self.command.do_list(arguments)

    def do_show(self, arguments):
        """
        Show an object of some type (either metric or graph).

        Usage
        show <metric/graph> <name>
        show <metric/graph> *
        """
        self.command.do_show(arguments)

    def do_metrics(self, arguments):
        """
        Compute all of the complexity matrics for a Graph object.

        Usage:
        metrics <name>
        metrics *
        """
        self.command.do_metrics(arguments)

    def do_analyze(self, arguments):
        """
        Perform statistical analysis on a set of generated metrics.

        Usage:
        analyze <metric names>
        """
        self.command.do_analyze(arguments)

    def do_delete(self, arguments):
        """
        Delete an object (type Graph, Metrics, or States) from memory.

        Usage:
        delete <type> <name>
        """
        self.command.do_delete(arguments)

    def do_export(self, arguments):
        """
        Save an object (type Graph, Metrics, or Stats) to an output file.

        Usage:
        save <type> <name>
        """
        self.command.do_export(arguments)

    def do_quit(self, arguments):
        """Quit the path complexity repl."""
        self.command.do_quit(arguments)

    def reload(self, _):
        """Reload the modules."""
        importlib.reload(command)
        self.command = command.Command(True, self)


def main():
    """Parse command line arguments and initialize the REPL."""
    parser = argparse.ArgumentParser(description='Arguments for APC REPL.')
    parser.add_argument('--debug', dest='debug_mode',
                        action='store_true', default=False,
                        help='Turn on debugging mode for more verbose output')
    parsed_args = parser.parse_args()

    logging.basicConfig(filename='repl_log.log', level=logging.DEBUG)
    try:
        readline.read_history_file()
    except FileNotFoundError:
        pass
    prompt = MyPrompt(parsed_args.debug_mode)
    prompt.prompt = '> '
    prompt.cmdloop('Starting path complexity repl...')


if __name__ == "__main__":
    main()
