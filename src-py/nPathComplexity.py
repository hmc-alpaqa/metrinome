from Graph import Graph 

def outNeighbors(start, edges):
	pass

def complement():
	pass

def npath(start, end, edges):
	if (start == end):
		return 1

	total = 0 
	for u in range(1, outNeighbors(v, edges)):
		new_edges = complement(edges, [start, u]) 
		total += npath(u, end, new_edges)

	return total 

def nPathComplexity(g: Graph):
	edgeList = g.edgeRules()
	nodes = g.getVertices()
	start = g.startNode
	end = g.endNode
	return npath(start, end, edgeList)
