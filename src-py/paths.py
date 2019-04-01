from threading import Thread, Event 
from Graph import Graph
from sys import argv
import os, glob2, time
import argparse
from pathComplexity import pathComplexity
from cyclomaticComplexity import cyclomaticComplexity
from nPathComplexity import nPathComplexity
from utils import roundExpression, classify, timeout, isExponential
from multiprocessing import Pool, Value
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np 
from math import log 

class MetricsCalculator(): 
	def __init__(self, results): 
		# Classify by cyclomatic complexity -> path complexity
		d1 = defaultdict(list)

		# Classify by npath complexity -> path complexity 
		d2 = defaultdict(list)

		# Classify by path complexity -> cyclomatic complexity
		d3 = defaultdict(list)

		# Classify by path complexity -> npath
		d4 = defaultdict(list)

		self.cyclomaticComplexities = []
		self.nPathComplexities = []
		
		self.dicts = [d1, d2, d3, d4]

		for res in results: 
			cycCompl       = res[0]
			nPathCompl     = res[1]
			pathCompl      = res[3]
			try: 
				pathCompl = float(pathCompl)
			except: 
				if isExponential(pathCompl): 
					print("NOooooo")
				else: 
					pathCompl = pathCompl
			d1[cycCompl]   += [pathCompl]
			d2[nPathCompl] += [pathCompl]	
			d3[pathCompl]  += [cycCompl]
			d4[pathCompl]  += [nPathCompl]
			self.cyclomaticComplexities += [cycCompl]
			self.nPathComplexities += [nPathCompl]

	def averageClassSize(self, dict, useFrequencies): 
		numClasses = len(dict.keys())
		sumAverages = 0 
		
		for key in dict.keys():
			totalCounts = 0 
			entropy = 0 

			for countIndex in dict[key]:
				totalCounts += dict[key][countIndex] 
			
			# Computing the shannon entropy 
			for countIndex in dict[key]:
				count = dict[key][countIndex] 
				p = count / totalCounts
				entropy += p * log(p)

			entropy *= -1
			
			# If we only have a single value, then the disbrituion is perfectly uniform
			if len(dict[key]) == 1: 
				sumAverages += 1 
			# Ratio between entropy of our distribution and uniform (ideal) distribution
			else:
				entropyRatio = entropy / log(len(dict[key]))
				total = entropyRatio * len(dict[key])
				sumAverages += entropyRatio * len(dict[key])
			
		return sumAverages / numClasses

	def computeMetric(self, useFrequencies = True):
		print("C to APC: ----- " + str(self.dicts[0]) + "\n")
		print("NPATH to APC: ----- " + str(self.dicts[1]) + "\n")
		print("APC to C: ------ " + str(self.dicts[2]) + "\n")
		print("APC to NPATH: ------ " + str(self.dicts[3]) + "\n")
		
		self.aggregate()
		cyclomaticToAPCCounts = self.dictCounter[0]
		NPathToAPCCounts = self.dictCounter[1]
		APCToCyclomaticCounts = self.dictCounter[2]
		APCToNPathCounts = self.dictCounter[3]

		cycToAPC = self.averageClassSize(cyclomaticToAPCCounts, useFrequencies)
		APCToCyc = self.averageClassSize(APCToCyclomaticCounts, useFrequencies)
		NPATHToAPC = self.averageClassSize(NPathToAPCCounts, useFrequencies)
		APCToNPATH = self.averageClassSize(APCToNPathCounts, useFrequencies)

		if cycToAPC == APCToCyc:
			r1 = 0 
		else: 
			r1 = (cycToAPC + APCToCyc) / (cycToAPC - APCToCyc) 
		
		if NPATHToAPC == APCToNPATH:
			r2 = 0 
		else: 
			r2 = (NPATHToAPC + APCToNPATH) / (NPATHToAPC - APCToNPATH)

		print(f"R1: {r1}, R2: {r2}")

	def aggregate(self): 
		self.dictCounter = self.dicts
		for dictionary in self.dictCounter:
			for key in dictionary.keys():
				dictionary[key] = Counter(dictionary[key]) 
		
	def showPlot(self): 
		plt.subplot(2, 1, 1)
	
		mean = np.mean(self.cyclomaticComplexities)
		std  = np.std(self.cyclomaticComplexities)
		plt.hist(self.cyclomaticComplexities, bins=100, label=f"Mean: {mean}\n StdDev: {std}")
		plt.title("Cyclomatic Complexity Distribution")
		plt.ylabel("Counts")
		plt.xlabel("Cyclomatic Complexity")
		plt.legend(loc='upper left')

		plt.subplot(2,1,2)
		mean = np.mean(self.nPathComplexities)
		std  = np.std(self.nPathComplexities)
		plt.hist(self.nPathComplexities, bins=100, label=f"Mean: {mean}\n StdDev: {std}")
		plt.title("NPath Distribution")
		plt.ylabel("Counts")
		plt.xlabel("NPath Complexity")
		plt.legend()
		plt.show()
	
	@staticmethod 
	def fromCSV(filename):
		results = []
		with open(filename, "r") as f:
			content = f.readlines()[1:]
			for line in content:
				# Dont need ID or filepath
				try:
					result = line.strip().split(",")[2:]
					result = [float(result[0])] + [float(result[1])] + result[2:]
					results.append(result)
				except (IndexError, ValueError) as e: 
					pass #TODO - log?
			
		return MetricsCalculator(results)

class Parameters():
	def __init__(self, filepath, recursive, max_depth, outputFile, statsMode): 
		self.filepath = filepath
		self.recursive = recursive
		self.max_depth = max_depth
	        self.outputFile = outputFile
                self.statsMode = statsMode

	def getRecursive(self): 
		return self.recursive

	def getMaxDepth(self):
		return self.max_depth

	def getOutputFile(self): 
		return self.outputFile

	def getFilepath(self):
		return self.filepath

        def getStatsMode(self):
                return self.statsMode

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


if __name__ == "__main__":

	# Get all command line arguments 
	parser = argparse.ArgumentParser(description="")
	parser.add_argument('--filename', help="Input filename", required=True)
	parser.add_argument('-r', help="Recursive Mode: look for .dot files in all subfolders", action="store_true", required=False)
	parser.add_argument('--maxdepth', help="In recursive mode, only look up to the maximum depth specified", type=int, required=False)
	parser.add_argument('-o', help="Set an output file", required=False)
        parser.add_argument('--statistics', help="Compute the metric for a given imput file", action="store_true", required=False)
	args = vars(parser.parse_args())

	params = Parameters(args['filename'], args['r'], args['maxdepth'], args['o'], args['statistics'])

	filepath    = params.getFilepath() 
	recursive   = params.getRecursive()
	max_depth   = params.getMaxDepth()
	outputFile  = params.getOutputFile()
        statsMode   = params.getStatsMode()

	if params is False and max_depth is not None:
		raise ValueError("Cannot specify max_depth without recursive mode (-r)")

	if os.path.isdir(filepath):
                if statsMode: 
                    raise ValueError("StatsComputer takes a CSV file of results.")
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
        
        if statsMode:      
	    metrics = MetricsCalculator.fromCSV(filelist[0])
	    metrics.computeMetric()
        else:
            writeOutput("test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class, path_cplxty_asym, path_cplxty")

	    p = Pool(processes = 4)
	    results = p.imap_unordered(computeResult, filelist)
	    p.close()
	    p.join()

	    for r in results: 
		print(r)
