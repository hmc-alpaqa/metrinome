from threading import Thread, Event 
from Graph import Graph
from sys import argv
import os, glob2, time
from pathComplexity import pathComplexity
from cyclomaticComplexity import cyclomaticComplexity
from nPathComplexity import nPathComplexity
from utils import roundExpression, classify, timeout

if __name__ == "__main__":
	filepath = argv[1]
	level = float(argv[2]) # can be inf - TODO
	filelist = []

	if os.path.isdir(filepath):
		# recursive glob '**' operator matches 0 or more subdirectories
		filelist = glob2.glob(os.path.join(filepath, "**/*.dot"), recursive=True)
	else: 
		filelist = [filepath]

	digits = 2
	print("test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class, path_cplxty_asym, path_cplxty")

	for i in range(1, len(filelist) + 1): 
		filename = filelist[i-1]
		g = Graph.fromFile(filename)
		cycCompl = cyclomaticComplexity(g)
		print("working on " + filename)
		with timeout(seconds = 10, error_message = "Timeout"):
			nPathCompl = nPathComplexity(g)
		try:
			pathCompl = pathComplexity(g)
			p1 = pathCompl[0]
			p2 = pathCompl[1]
		except Exception as e: 
			print(e)
			p1 = 0 
			p2 = 0
		print(i, 				",", 
			filename, 			",",
			cycCompl, 			",", 
			nPathCompl, 		",",
			classify(p1, "n"),	",",
			roundExpression(p1, digits),		",",
			roundExpression(p2, digits))

