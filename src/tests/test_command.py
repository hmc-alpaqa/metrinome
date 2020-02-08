import unittest 
import sys
from contextlib import contextmanager
from io import StringIO
sys.path.append("/app/code/")
import Command

class TestCommand(unittest.TestCase): 
    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err
        
        # Use (out.getvalue().strip(), err.getvalue().strip())
        # to get the values from the captured output. 

    @classmethod
    def setUpClass(cls): 
        cls.validCommands = {
            "klee_replay": (1, 1), 
            "convert": (1, float('inf')),
            "list": (1, 1), 
            "metrics": (1, 1), 
            "show": (2, 2), 
            "analyze": (1, 1), 
            "klee_to_bc": (0, 0), 
            "to_klee_format": (1, 1), 
            "clean_klee_files": (0, 0), 
            "klee": (1, 1), 
            "export": (2, 2), 
            "delete": (2, 2), 
        }

    def setUp(self):
        self.command = Command.Command()
        
    def testNumArgsInvalid(self): 
        with self.captured_output() as (out, err):
            for command in self.validCommands: 
                functionName = "do_" + command 
                method = getattr(self.command, functionName)
                minNumArgs = self.validCommands[command][0]
                maxNumArgs = self.validCommands[command][1]
                if minNumArgs > 0: 
                    #res = method("")
                    pass
                    # TODO: assert that result is none 
                if maxNumArgs != float('inf'):
                    #res = method("a " * (maxNumArgs + 1))
                    pass 
                    # TODO: assert that the result is none

    # ==== Test do_analyze ==== 
    def testAnalyzeAll(self): 
        with self.captured_output() as (out, err):
            self.command.do_analyze("*")

    def testAnalyzeValidName(self): 
        with self.captured_output() as (out, err):
            self.command.do_analyze("some_name")

    def testAnalyzeInvalidName(self): 
        with self.captured_output() as (out, err):
            self.command.do_analyze("invalid_name")

    # ==== do_to_klee_format =====
    def testToKleeFormatInvalidType(self):
        with self.captured_output() as (out, err): 
            # self.command.do_to_klee_format("examplefile.wrongextension")
            pass 

    def testToKleeFormatNonexistantFile(self): 
        with self.captured_output() as (out, err): 
            # self.command.do_to_klee_format("nonexistantfile.c")
            pass 

    def testToKleeFormatValid(self): 
        with self.captured_output() as (out, err): 
            # self.command.do_to_klee_format("examplefile.c")
            pass 

    # ==== Test do_klee_to_bc =====
    def testKleeToBC(self): 
        with self.captured_output() as (out, err):
            pass 

    # ==== Test do_klee_replay ====
    def testKleeReplayInvalidType(self): 
        with self.captured_output() as (out, err):
            self.command.do_klee_replay("somefile.wrongextension") 

    def testKleeReplayNonexistantFile(self): 
        with self.captured_output() as (out, err):
            self.command.do_klee_replay("nonexistantFile.ktest")  

    def testKleeReplayValid(self): 
        with self.captured_output() as (out, err):
            self.command.do_klee_replay("samplefile.ktest")  

    # ==== Test do_convert ===== 
    def testConvertValidType(self): 
        with self.captured_output() as (out, err):
            # self.command.do_convert("testfile.py") # TODO 
            pass 

    def testConvertNonexistantFile(self): 
        with self.captured_output() as (out, err):
            # self.command.do_convert("somefile.py") # TODO 
            pass 

    def testConvertInvalidType(self):
        with self.captured_output() as (out, err):
            # self.command.do_convert("testfile.invalidextension")
            pass # TODO

    # TODO: convert recursive

    # ==== Test do_show =====
    def testShowMetricValid(self):
        with self.captured_output() as (out, err):
            self.command.metrics["foo"] = "123"
            self.command.do_show(Command.OBJ_TYPES.METRIC.value + " " + "foo") 

    def testShowGraphValid(self): 
        with self.captured_output() as (out, err):
            self.command.graphs["foo"] = "123"
            self.command.do_show(Command.OBJ_TYPES.GRAPH.value + " " + "foo") 

    def testShowAllTypesValid(self): 
        with self.captured_output() as (out, err):
            self.command.graphs["foo"] = "123"
            self.command.metrics["foo"] = "123"
            self.command.do_show(Command.OBJ_TYPES.ALL.value + " foo")  

    def testShowAllNamesValid(self): 
        with self.captured_output() as (out, err):
            self.command.graphs["foo"] = "123"
            self.command.graphs["bar"] = "456"
            self.command.do_show(Command.OBJ_TYPES.GRAPH.value + " " + Command.OBJ_TYPES.ALL.value)  

    def testShowMetricInvalid(self): 
        with self.captured_output() as (out, err):
            self.command.do_show(Command.OBJ_TYPES.METRIC.value + " foo")  
    
    # ==== Test do_list =====
    def testListGraphs(self):
        with self.captured_output() as (out, err):
            res = self.command.do_list(Command.OBJ_TYPES.GRAPH.value) 

    def testListMetrics(self):
        with self.captured_output() as (out, err):
            res = self.command.do_list(Command.OBJ_TYPES.METRIC.value)  

    def testListAll(self): 
        with self.captured_output() as (out, err):
            res = self.command.do_list(Command.OBJ_TYPES.ALL.value)

    def testListInvalidType(self): 
        with self.captured_output() as (out, err):
            res = self.command.do_list("Somerandomtype")

    # ==== Test do_delete ======
    def testDeleteGraphValid(self): 
        with self.captured_output() as (out, err):
            objType = Command.OBJ_TYPES.GRAPH
            objName = "sample_graph"
            self.command.graphs['sample_graph'] = 'foo'
            self.command.graphs['sample_graph'] = 'bar'
            self.command.metrics['sample_graph'] = 'abc'
            res = self.command.do_delete(str(objType) + " " + str(objName))

    def testDeleteMetricValid(self): 
        with self.captured_output() as (out, err):
            objType = Command.OBJ_TYPES.METRIC
            objName = "sample_metric"
            self.command.metrics['sample_metric'] = 'foo'
            self.command.metrics['sample_metric'] = 'bar'
            self.command.graphs['sample_metric'] = 'a'
            res = self.command.do_delete(str(objType) + " " + str(objName))

    def testDeleteStatValid(self): 
        with self.captured_output() as (out, err):
            objType = Command.OBJ_TYPES.STAT
            objName = "sample_stat"
            self.command.stats['sample_stat'] = 'foo'
            self.command.stats['sample_stat'] = 'bar'
            self.command.metrics['sample_stat'] = 'a'
            res = self.command.do_delete(str(objType) + " " + str(objName))

    def testDeleteAllTypesValid(self): 
        with self.captured_output() as (out, err):
            objType = Command.OBJ_TYPES.ALL
            objName = "sample_name"
            self.command.graphs['sample_name']  = 'foo'
            self.command.metrics['sample_name'] = 'foo'
            self.command.stats['sample_name']   = 'foo'
            
            self.command.graphs['sample_name']  = 'a'
            self.command.metrics['sample_name'] = 'b'
            self.command.stats['sample_name']   = 'c'
            res = self.command.do_delete(str(objType) + " " + str(objName))
        
    def testDeleteAllNamesValid(self): 
        with self.captured_output() as (out, err):
            # Delete * name
            objType = Command.OBJ_TYPES.GRAPH
            objName = "*"
            self.command.graphs['sample_name']  = 'a'
            self.command.graphs['sample_name'] = 'b'
            self.command.graphs['sample_name']   = 'c'
            
            self.command.metrics['sample_name'] = 'b'
            self.command.stats['sample_name']   = 'c'

            res = self.command.do_delete(str(objType) + " " + str(objName))
    
    #TODO: test invalid

    # ==== 

if __name__ == '__main__':
    unittest.main()