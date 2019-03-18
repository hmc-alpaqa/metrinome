from threading import Thread, Event 
from Graph import Graph
from sys import argv
import os, glob2, time
import argparse
from pathComplexity import pathComplexity
from cyclomaticComplexity import cyclomaticComplexity
from nPathComplexity import nPathComplexity
from utils import roundExpression, classify, timeout
from multiprocessing import Pool, Value
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np 

class Parameters():
	def __init__(self, filepath, recursive, max_depth, outputFile): 
		self.filepath = filepath
		self.recursive = recursive
		self.max_depth = max_depth
		self.outputFile = outputFile

	def getRecursive(self): 
		return self.recursive

	def getMaxDepth(self):
		return self.max_depth

	def getOutputFile(self): 
		return self.outputFile

	def getFilepath(self):
		return self.filepath
	

def getResultsFromCSV(filename):
	'''
	'''
	results = []
	with open(filename, "r") as f:
		content = f.readlines()[1:]
		for line in content:
			# Dont need ID or filepath
			try:
				result = line.split(",")[1:]
				print(result)
				result = [result[0]] + [float(result[1])] + [float(result[2])] + result[2:]
				results.append(result)
			except (IndexError, ValueError) as e: 
				pass #TODO - log?
		
	return results

def writeOutput(msg):
	print(msg)

def computeResult(filename):
	g = Graph.fromFile(filename)
	writeOutput("working on " + filename)
	with timeout(seconds = 10, error_message = "Timeout"):
		nPathCompl = nPathComplexity(g)
	pathCompl = pathComplexity(g)
	p1 = pathCompl[0]
	p2 = pathCompl[1]
	return (filename, cyclomaticComplexity(g), nPathCompl, classify(p1, "n"), roundExpression(p1, digits), roundExpression(p2, digits))

def getStatistics(results):
	# Classify by cyclomatic complexity -> path complexity
	d1 = defaultdict(list)

	# Classify by npath complexity -> path complexity 
	d2 = defaultdict(list)

	# Classify by path complexity -> cyclomatic complexity
	d3 = defaultdict(list)

	# Classify by path complexity -> npath
	d4 = defaultdict(list)

	cyclomaticComplexities = []
	nPathComplexities = []
	
	dicts = [d1, d2, d3, d4]

	for res in results: 
		print(res)
		cycCompl       = res[1]
		nPathCompl     = res[2]
		pathCompl      = res[3]
		d1[cycCompl]   += [pathCompl]
		d2[nPathCompl] += [pathCompl]	
		d3[pathCompl]  += [cycCompl]
		d4[pathCompl]  += [nPathCompl]
		cyclomaticComplexities += [cycCompl]
		nPathComplexities += [nPathCompl]
	
	print(d1)
	print(d2)
	print(d3)
	print(d4)

	print("=== Aggregating... ===")

	for dictionary in dicts:
		for key in dictionary.keys():
			dictionary[key] = Counter(dictionary[key]) 

	print(d1)
	print(d2)
	print(d3)
	print(d4)

	print("=== Plotting... ===")

	plt.subplot(2,1,1)
	
	mean = np.mean(cyclomaticComplexities)
	std  = np.std(cyclomaticComplexities)
	plt.hist(cyclomaticComplexities, bins=100, label=f"Mean: {mean}\n StdDev: {std}")
	plt.title("Cyclomatic Complexity Distribution")
	plt.ylabel("Counts")
	plt.xlabel("Cyclomatic Complexity")
	plt.legend(loc='upper left')

	plt.subplot(2,1,2)
	mean = np.mean(nPathComplexities)
	std  = np.std(nPathComplexities)
	plt.hist(nPathComplexities, bins=100, label=f"Mean: {mean}\n StdDev: {std}")
	plt.title("NPath Distribution")
	plt.ylabel("Counts")
	plt.xlabel("NPath Complexity")
	plt.legend()
	plt.show()


if __name__ == "__main__":

	# === GET STATISTICS FROM CSV EXAMPLE ===  
	# r = getResultsFromCSV("../results/java_cfg_small_sample_results.csv")
	# getStatistics(r)

	# Get all command line arguments 
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('--filename', help="Input filename", required=True)
	parser.add_argument('-r', help="Recursive Mode: look for .dot files in all subfolders", action="store_true", required=False)
	parser.add_argument('--maxdepth', help="In recursive mode, only look up to the maximum depth specified", type=int, required=False)
	parser.add_argument('-o', help="Set an output file", required=False)
	args = vars(parser.parse_args())

	params = Parameters(args['filename'], args['r'], args['maxdepth'], args['o'])

	filepath    = params.getFilepath() 
	recursive   = params.getRecursive()
	max_depth   = params.getMaxDepth()
	outputFile  = params.getOutputFile()

	if params is False and max_depth is not None:
		raise ValueError("Cannot specify max_depth without recursive mode (-r)")

	if os.path.isdir(filepath):
		if recursive:
			if max_depth is None:
				# recursive glob '**' operator matches 0 or more subdirectories
				filelist = glob2.glob(os.path.join(filepath, "**/*.dot"), recursive=True)	
			else:
				print("Not supported yet")
				filelist = []
		else:
			filelist = glob2.glob(os.path.join(filepath, "*.dot"), recursive=False)	
	else: 
		# Not a directory, cannot be recursive
		if recursive:
			raise ValueError("Recursive mode only applies to directories")
		filelist = [filepath]

	digits = 2

	writeOutput("test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class, path_cplxty_asym, path_cplxty")

	filelist = filelist

	# Use map with shared Value instead?
	p = Pool(processes = 4)
	results = p.imap_unordered(computeResult, filelist)
	p.close()
	p.join()

	getStatistics(results)