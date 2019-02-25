filepath = $CommandLine[[4]];

filelist = 	If[DirectoryQ[filepath], 
				FileNames["*.dot", filepath, 
				ToExpression[$CommandLine[[5]]]], {filepath}
			];

Get["pathComplexity.m"];
Get["cyclomaticComplexity.m"];
Get["nPathComplexity.m"];
Get["utils.m"];
digits = 2;

Print["test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class, path_cplxty_asym, path_cplxty"];

For[ii = 1, ii < Length[filelist] + 1 , ii++;, 
	filename = filelist[[ii]];
	G = Import[filename];
	cycCompl = cyclomaticComplexity[G];
	nPathCompl = TimeConstrained[nPathComplexity[G],10, "Timeout"];
	pathCompl = pathComplexity[G];
	p1 = pathCompl[[1]];
	p2 = pathCompl[[2]];
	Print[ 	ii, 				",", 
			filename, 			",",
			cycCompl, 			",", 
			nPathCompl, 		",",
			classify[p1,n],		",",
			roundExpression[p1, digits],		",",
			roundExpression[p2, digits]		
		];
];
