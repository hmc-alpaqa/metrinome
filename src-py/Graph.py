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
        Returns a Graph object from a .dot file 
        '''
        return Graph() 