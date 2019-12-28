import unittest 

class TestGetFiles(unittest.TestCase): 
    def testGetFiles(self): 
        pass 

class TestAPI(unittest.TestCase): 
    # init
    def testInit(self): 
        pass 

    # convert
    def testConvert(self): 
        pass 

    # list_objects 
    def testListObjects(self): 
        pass 

    # metrics 
    def testMetrics(self): 
        pass 

    # show 
    def testShow(self): 
        pass 

    # analyze 
    def testAnalyze(self): 
        pass 

    # export 
    def testExport(self): 
        pass 

    # delete 
    def testDelete(self): 
        pass 

    # show_metrics 
    def testShowMetrics(self): 
        pass 

    # show_graphs 
    def testShowGraphs(self): 
        pass 
    
class TestCommand(unittest.TestCase): 
    # init 
    def testInit(self): 
        pass 

    # check_num_args 
    def testCheckNumArgs(self): 
        pass 

    # do_convert 
    def testDoConvert(self): 
        pass 

    # === do_list ===   
    def testDoList_TooManyArguments(self): 
        pass 

    def testDoList_InvalidType(self): 
        pass 
    
    def testDoList_Metrics(self): 
        pass 

    def testDoList_Graphs(self): 
        pass 

    def testDoList_AllTypes(self): 
        pass 

    # do_metrics 
    def testDoMetrics(self): 
        pass 

    # do_show 
    def testDoShow(self): 
        pass 

    # do_analyze 
    def testDoAnalyze(self): 
        pass 

    # === do_quit ===
    def testDoQuit_TooManyArguments(self): 
        pass 

    def testDoQuit_Valid(self): 
        pass 

    # === do_export ===
    def testDoExport_Metrics(self): 
        pass 

    def testDoExport_Graphs(self): 
        pass
    
    def testDoExport_Stats(self): 
        pass 

    def testDoExport_Wildcard(self):
        pass 

    def testDoExport_UnrecognizedType(self): 
        pass 

    def testDoExport_InvalidName(self): 
        pass 

    # do_delete 
    def testDoDelete(self): 
        pass 

    # convert_args 
    def testConvertArgs(self): 
        pass 

    # complete 
    def testComplete(self): 
        pass

if __name__ == '__main__':
    unittest.main()
