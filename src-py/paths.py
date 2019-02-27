from pathComplexity import pathComplexity
from cyclomaticComplexity import cyclomaticComplexity
from nPathComplexity import nPathComplexity
from utils import roundExpression, classify

if __name__ == "__main__":
	filepath = ''

	digits = 2
	print("test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class, path_cplxty_asym, path_cplxty")

	for i in range(1, len() + 1): 
		filename = filelist[[i]]
		G = Import[filename]
		cycCompl = cyclomaticComplexity(G)
		nPathCompl = TimeConstrained(nPathComplexity[G], 10, "Timeout")
		pathCompl = pathComplexity(G)
		p1 = pathCompl[[1]]
		p2 = pathCompl[[2]]
		print(i, 				",", 
			filename, 			",",
			cycCompl, 			",", 
			nPathCompl, 		",",
			classify(p1, n),	",",
			roundExpression(p1, digits),		",",
			roundExpression(p2, digits))