import readline
import logging
import Command
import importlib
from cmd import Cmd

TESTING_MODE = True
class MyPrompt(Cmd): 

    def __init__(self) -> None:
        '''
        '''
        self.command = Command.Command()
        if TESTING_MODE: 
            setattr(self, "do_reload", self.reload)
            
        super(MyPrompt, self).__init__()

    def do_convert(self, args): 
        """
        Convert a file containing source code to a Graph object. 
        The recursive flag (-r) 
        Usage: 
        convert <file-like>
        convert -r <file-like>
        convert <file-like-1> <file-like-2> ... <file-like-n>
        """
        self.command.do_convert(args)

    def do_list(self, args): 
        """
        List all of the objects of a specific type (either metrics or graphs). 

        Usage: 
        list <metrics/graphs>
        list * 
        """
        self.command.do_list(args)

    def do_show(self, args): 
        """
        Show an object of some type (either metric or graph).

        Usage 
        show <metric/graph> <name>
        show <metric/graph> * 
        """
        self.command.do_show(args) 

    def do_metrics(self, args): 
        """
        Compute all of the complexity matrics for a Graph object. 

        Usage: 
        metrics <name>
        metrics * 
        """
        self.command.do_metrics(args)
   
    def do_analyze(self, args): 
        """
        Perform statistical analysis on a set of generated metrics. 

        Usage: 
        analyze <metric names>
        """
        self.command.do_analyze(args)

    def do_delete(self, args): 
        """
        Delete an object (type Graph, Metrics, or States) from memory. 

        Usage: 
        delete <type> <name>
        """
        self.command.do_delete(args)

    def do_export(self, args):
        """
        Save an object (type Graph, Metrics, or Stats) to an output file. 

        Usage:
        save <type> <name>
        """
        self.command.do_export(args)

    def do_quit(self, args): 
        """
        Quits the path complexity repl
        """
        self.command.do_quit(args)

    def reload(self, args): 
        '''
        This will reload the modules.
        '''
        importlib.reload(Command)
        self.command = Command.Command()

if __name__ == "__main__":
    logging.basicConfig(filename='repl_log.log',level=logging.DEBUG)
    try: 
        readline.read_history_file()
    except FileNotFoundError: 
        pass 
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting path complexity repl...')
