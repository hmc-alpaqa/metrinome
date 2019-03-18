pathComplexity[G_] := Module[
	{},

	A = AdjacencyMatrix[G];
	dimension = VertexCount[G];

	ID = SparseArray[IdentityMatrix[dimension]];
	A[[2]][[2]] = 1;
	
	X = SparseArray[ID - A t];
	Xsubmatrix = X[[ Union[{1}, Range[3,dimension]], Range[2,dimension] ]];

	generatingFunction = Det[Xsubmatrix]/((-1)^(1+2) Det[X]);
	
	recurrenceKernel = CoefficientList[(-1)^(1+2) Det[X],t];
	recurrenceDegree = Length[recurrenceKernel];

	numPaths = Table[SeriesCoefficient[generatingFunction,{t,0,i}],
	                 {i,0,2*dimension}];
	baseCases = numPaths[[ Range[dimension + 1,dimension + recurrenceDegree-1] ]]; 

	recurrence = Total[ recurrenceKernel* Map[ f, Table[n, {recurrenceDegree}] - Range[0,recurrenceDegree-1] ] ];

	symbolicSolution = RSolve[recurrence == 0, f[n], n];
	
	numericSolution = N[symbolicSolution[[1]][[1]][[2]]];
	
	terms = Table[numericSolution[[i]], {i,Length[numericSolution]}];

	coefficients = Table[C[i],{i,Length[numericSolution]}];
	factors = terms / coefficients;

	Print[factors];

	M = Table[factors, {n,1,Length[factors]}];

	Quiet[lf = LinearSolve[M]]; 

	boundingSolutionTerms = lf[baseCases]*factors;
	
	boundingSolution = Expand[Total[boundingSolutionTerms]];

	boundingSolution = Replace[boundingSolution,
	 (Complex[x_, y_]) -> Abs[x+I y], 
	 Infinity] ;
	
	boundingSolution = Replace[boundingSolution, (x_)^n -> Abs[x]^n, Infinity];

	asymptoticComplexity = bigO[boundingSolution, n];

	{asymptoticComplexity, boundingSolution}
];
