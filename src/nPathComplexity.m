outNeighbors[v_, edges_] := edges[[ Flatten[Position[ edges, {v, _ } ]] ]][[All,2]];

npath[v_, exit_, edges_] := If[ v == exit,
								1,
								Sum[ npath[u, exit, Complement[edges, {{v,u}}] ], {u, outNeighbors[v,edges]}]
							];

nPathComplexity[G_] := Module[
	{},
	edgeRules = EdgeRules[G];
	edgeList = Transpose[{edgeRules[[All,1]],edgeRules[[All,2]]}];
	start = VertexList[G][[1]];
	exit = VertexList[G][[2]];
	npath[start, exit, edgeList]
];
