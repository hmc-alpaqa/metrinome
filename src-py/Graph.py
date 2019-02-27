class Graph(object):
    def __init__(self):
        self.edges = list()
        self.vertices = set()
        self.vertexCount = 0

    def edgeRules(self):
        return self.edges
    
    def vertexCount(self):
        return self.vertexCount

    @staticmethod
    def fromFile(self, filename):
        '''
        Returns a Graph object from a .dot file of format

        digraph {
            0 [label="START"]
            2 [label="EXIT"]
            a_i -> a_j
            ...
            a_k  -> a_m
        }
        '''
        edges = []
        vertices = set()
        with open(filename, "r") as f:
            content = f.readlines()

            for i in f.readlines()[1:]:
                if i[0] == "}":
                    break
                else:
                    pass 
                    
        return Graph() 