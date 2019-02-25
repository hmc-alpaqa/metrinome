roundExpression[expr_, digits_] := 
	ReplaceAll[	expr, 
		(x_/;NumberQ[x]) -> N[Round[x,10^(-digits)]]
	];     

myRound[num_, prec_] := Module[
	{},
	
	digitList = RealDigits[num][[1]][[Range[prec]]];
	base = RealDigits[num][[2]];
	N[FromDigits[digitList] / 10^(prec - base)]
];

classify[expr_, var_] := If[NumberQ[expr], "Constant", If[PolynomialQ[expr, var], "Polynomial", "Exponential"] ];

bigO[x_ + y_, n_] := 

	If[ Limit[Abs[y / x], n -> Infinity] === 0.,
		x, 
		bigO[y, n]
	];

bigO[x_,n_] := x;
