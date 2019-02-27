from pydot import Graph

def outNeighbors(start, edges):
	pass 

def complement():
	pass 

def npath(start, end, edges):
	if (start == end):
		return 1 
	
	u = start 
	total = 0
	while u is not outNeighbors[start, edges]:
		total += npath(u, end, complement(edges, [start, end]))
	return total

def nPathComplexity(g: Graph):
	edgeList = g.get_edges()
	nodes = g.get_node_list()
	start = nodes[0]
	end = nodes[1]
	return npath(start, end, edgeList)