import readline
import logging
import argparse
import Command
import importlib
from cmd import Cmd

TESTING_MODE = True
class MyPrompt(Cmd): 

    def __init__(self, debug_mode) -> None:
        '''
        Create a new instance of the REPL. 
        '''
        self.command = Command.Command(debug_mode)
        if TESTING_MODE: 
            setattr(self, "do_reload", self.reload)
            
        super(MyPrompt, self).__init__()

    def do_to_klee_format(self, args): 
        '''
        Given a C file, create a new modified C file that is in the 
        correct format to be converted to a bc file. 
        '''
        self.command.do_to_klee_format(args)

    def do_klee_to_bc(self, args): 
        '''
        Given a C file in the correct format, generate a new .bc file from 
        the given C file. 
        '''
        self.command.do_klee_to_bc(args)

    def do_klee(self, args): 
        '''
        Execute the klee command on a .bc file. This will 
        generate all of the tests automatically and store 
        the resulting metadata (e.g. number of tests generated). 
        Usage: 
        klee <file>
        '''
        self.command.do_klee(args)

    def do_klee_replay(self, args): 
        '''
        Execute a test generated by KLEE given a klee test file.
        Usage: 
        klee_replay <file>
        ''' 
        self.command.do_klee_replay(args)

    def do_clean_klee(self, args): 
        '''
        Removes all of the files generated by klee, including the generated tests.
        '''
        self.command.do_clean_klee_files(args)

    def do_convert(self, args): 
        '''
        Convert a file containing source code to a Graph object. 
        The recursive flag (-r) can also be used. 
        
        Usage: 
        convert <file-like>
        convert -r <file-like>
        convert <file-like-1> <file-like-2> ... <file-like-n>
        '''
        self.command.do_convert(args)

    def do_list(self, args): 
        '''
        List all of the objects of a specific type (either metrics or graphs). 

        Usage: 
        list <metrics/graphs>
        list * 
        '''
        self.command.do_list(args)

    def do_show(self, args): 
        '''
        Show an object of some type (either metric or graph).

        Usage 
        show <metric/graph> <name>
        show <metric/graph> * 
        '''
        self.command.do_show(args) 

    def do_metrics(self, args): 
        '''
        Compute all of the complexity matrics for a Graph object. 

        Usage: 
        metrics <name>
        metrics * 
        '''
        self.command.do_metrics(args)
   
    def do_analyze(self, args): 
        '''
        Perform statistical analysis on a set of generated metrics. 

        Usage: 
        analyze <metric names>
        '''
        self.command.do_analyze(args)

    def do_delete(self, args): 
        '''
        Delete an object (type Graph, Metrics, or States) from memory. 

        Usage: 
        delete <type> <name>
        '''
        self.command.do_delete(args)

    def do_export(self, args):
        '''
        Save an object (type Graph, Metrics, or Stats) to an output file. 

        Usage:
        save <type> <name>
        '''
        self.command.do_export(args)

    def do_quit(self, args): 
        '''
        Quits the path complexity repl
        '''
        self.command.do_quit(args)

    def reload(self, args): 
        '''
        This will reload the modules.
        '''
        importlib.reload(Command)
        self.command = Command.Command()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for APC REPL.')
    parser.add_argument('--debug', dest='debug_mode',
                        action='store_true', default=False, 
                        help='Turn on debugging mode for more verbose output')
    args = parser.parse_args()

    logging.basicConfig(filename='repl_log.log',level=logging.DEBUG)
    try: 
        readline.read_history_file()
    except FileNotFoundError: 
        pass 
    prompt = MyPrompt(args.debug_mode)
    prompt.prompt = '> '
    prompt.cmdloop('Starting path complexity repl...')
