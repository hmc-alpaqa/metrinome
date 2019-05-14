from Graph import Graph 

def outNeighbors(start, edges):
	'''
	Return a list of all the nodes we can get to from a 
	given 'start' node
	'''
	return [edge[1] for edge in edges if edge[0] == start] 			 				

def removeEdge(edgeList, edge):
	return list(filter(lambda existingEdge: existingEdge != edge, edgeList))

def npath(start, end, edges):
	'''
	Helper function used to compute NPath Complexity recursively 
	'''
	if start == end:
		return 1

	total = 0 
	for neighbor in outNeighbors(start, edges):
		# Delete the edge [start, u] from the graph 
		newEdges = removeEdge(edges, [start, neighbor]) 

		# Recursive call from new edge 
		total += npath(neighbor, end, newEdges)

	return total 

def nPathComplexity(g: Graph):
	'''
	Compute the NPath complexity of a function given its CFG 
	'''
	return npath(g.startNode, g.endNode, g.edgeRules())
