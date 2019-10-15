from Graph import Graph
from typing import List 

edge = List[int]
node = int
metric = int

class NPathComplexity():
	'''
	NPathComplexity allows us to compute the NPath Complexity of some
	function from its Control Flow Graph. 
	'''

	def __init__(self) -> None:
		pass 

	def name(self) -> str:
		'''
		Returns the name of the metric computed by this class.
		'''
		return "NPath Complexity"

	def neighbors(self, start: node, edges: List[edge]) -> List[node]:
		'''
		Return a list of all the nodes we can get to from a
		given 'start' node
		'''
		return [edge[1] for edge in edges if edge[0] == start]

	def removeEdge(self, edgeList: List[edge], edge: edge) -> List[edge]:
		'''
		Return an edgeList with the specified edge removed.
		'''
		return list(filter(lambda existingEdge: existingEdge != edge, edgeList))

	def npath(self, start: node, end: node, edges) -> metric:
		'''
		Helper function used to compute NPath Complexity recursively
		'''
		if start == end:
			return 1

		total = 0
		for neighbor in self.neighbors(start, edges):
			# Delete the edge [start, u] from the graph 
			newEdges = self.removeEdge(edges, [start, neighbor])

			# Recursive call from new edge 
			total += self.npath(neighbor, end, newEdges)

		return total

	def evaluate(self, g: Graph) -> metric:
		'''
		Compute the NPath complexity of a function given its CFG
		'''
		return self.npath(g.startNode, g.endNode, g.edgeRules())
