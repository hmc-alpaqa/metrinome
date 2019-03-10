from Graph import Graph 

def outNeighbors(start, edges):
	neighbors = []
	for startNode, endNode in edges: 
		if startNode == start: 
			neighbors.append(endNode)

	return neighbors 				

def complement(edgeList, edge):
	newEdgeList = [] 
	for start, end in edgeList:
		if start != edge[0] or end != edge[1] : 
			newEdgeList.append([start, end])
	return newEdgeList

def npath(start, end, edges):
	if (start == end):
		return 1

	total = 0 
	for u in outNeighbors(start, edges):
		# Delete the edge [start, u] from the graph 
		new_edges = complement(edges, [start, u]) 
		# Recursive call from new edge 
		total += npath(u, end, new_edges)

	return total 

def nPathComplexity(g: Graph):
	edgeList = g.edgeRules()
	nodes = g.getVertices()
	start = g.startNode
	end = g.endNode
	return npath(start, end, edgeList)
