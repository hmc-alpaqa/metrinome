import os, glob2, time, argparse, logging 
import matplotlib.pyplot as plt
import numpy as np 
from threading import Thread, Event 
from Graph import Graph
from sys import argv
from PathComplexity import pathComplexity
from CyclomaticComplexity import cyclomaticComplexity
from NPathComplexity import nPathComplexity
from Parameters import Parameters
from Utils import roundExpression, classify, Timeout, isExponential
from multiprocessing import Pool, Value
from collections import defaultdict, Counter
from math import log 
from typing import List

NUM_PROCESSES = 4

class MetricsComparer:
	def __init__(self, results, location):
		'''
		Input results list of tuples, each being:
			(Cyclomatic Complexity, NPATH Complexity, APC Class, Largest Big-O APC term, APC Expression)

		Creates a new MetricsComparer object from a list of results, creating dictionaries
		with (key, value) pairs given by
			1. (cyclomatic complexity, path complexity)
			2. (npath complexity, path complexity)
			3. (path complexity, cyclomatic complexity)
			4. (path complexity, npath)
		'''
		self.location = location
		self.results = results

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
		self.pathComplexities = []

		self.dicts = [d1, d2, d3, d4]

		for res in results:
			cycCompl       = res[1]
			nPathCompl     = res[2]
			pathCompl      = res[4]
			d1[cycCompl]   += [pathCompl]
			d2[nPathCompl] += [pathCompl]
			d3[pathCompl]  += [cycCompl]
			d4[pathCompl]  += [nPathCompl]
			self.cyclomaticComplexities += [cycCompl]
			self.nPathComplexities += [nPathCompl]
			self.pathComplexities += [pathCompl]

	def averageClassSize(self, dict, useFrequencies: bool):
		'''
		Given some dictionary with key-value pairs 
			(Metric1, Metric2),
		where given some value 'x' for Metric1, the dictionary 
		will map to all values Metric2 takes on for the set 
		of functions that took on value 'x' for Metric1 
		'''
		numClasses = len(dict.keys())
		sumAverages = 0

		logging.info("Working with: " + str(dict))
		logging.info(f"Number of Classes: {numClasses}")
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
				logging.info(f"Found {totalCounts} many counts for key {key}, obtaining entropy {entropy} \
					  		 and entropy ratio {entropyRatio}")
				total = entropyRatio * len(dict[key])
				sumAverages += entropyRatio * len(dict[key])

		return sumAverages / numClasses

	def logDicts(self):
		'''
		Log the dictionaries mapping between complexity metrics to the log 
		file 
		'''
		logging.info("C to APC: ----- " + str(self.dicts[0]))
		logging.info("NPATH to APC: ----- " + str(self.dicts[1]))
		logging.info("APC to C: ------ " + str(self.dicts[2]))
		logging.info("APC to NPATH: ------ " + str(self.dicts[3]) + "\n")

	def logClassSizes(self, cycToAPC, APCToCyc, npathToAPC, apcToNPATH): 
		'''
		Writes the average class size for each metric to the log file 
		'''
		logging.info(f"cycToAPC: {str(cycToAPC)}")
		logging.info(f"APCToCyc: {str(APCToCyc)}")
		logging.info(f"NPATHToAPC: {str(npathToAPC)}")
		logging.info(f"APCToNPATH: {str(apcToNPATH)}\n")

	def computeMetric(self, useFrequencies = True):
		'''
		Calculate the metrics used to compare APC to Cyclomatic Complexity 
		and NPATH 
		'''
		self.logDicts()

		# Convert APCs to correct complexity classes 
		tempDict = dict()
		for i in range(0, 2):
			for key in self.dicts[i].keys():
				tempDict[key] = list(map(classify, self.dicts[i][key]))
			self.dicts[i] = tempDict

		tempDict = dict()
		for i in range(2, 4): 
			for key in self.dicts[i].keys():
				tempDict[classify(key)] = self.dicts[i][key]
			self.dicts[i] = tempDict

		self.logDicts()
		self.aggregate()
		self.logDicts()

		averageClassSizes = [0] * 4 
		for i in range(0, 4):
			averageClassSizes[i] = self.averageClassSize(self.dictCounter[i], useFrequencies)
		cycToAPC, apcToCyc, npathToAPC, apcToNPATH = averageClassSizes

		self.logClassSizes(*averageClassSizes)

		if cycToAPC == apcToCyc:
			rOne = 0
		else:
			rOne = (cycToAPC + apcToCyc) / (cycToAPC - apcToCyc)

		if npathToAPC == apcToNPATH:
			rTwo = 0
		else:
			rTwo = (npathToAPC + apcToNPATH) / (npathToAPC - apcToNPATH)

		writeOutput(f"APC to Cyclomatic: {cycToAPC}, APCToCyc: {apcToCyc}", self.location)
		writeOutput(f"APC to Cyclomatic: {npathToAPC}, APCToNPATH: {apcToNPATH}", self.location)
		writeOutput(f"APC to Cyclomatic: {rOne}, APC vs NPATH: {rTwo}", self.location)

	def aggregate(self):
		'''
		Iterate through all of the of the dictionaries where each dictionary has 
		key value pairs of one of the types: 

		(Cyclomatic, APC Complexities), (NPATH, APC Complexities), 
		(APC, Cyclomatic Complexities), (APC, NPATH Complexities)
		
		and creates a dictionary with the same key that maps to the number of different
		complexities (e.g. (Cyclomatic, len(APC Complexities)))
		'''
		self.dictCounter = self.dicts
		for dictionary in self.dictCounter:
			for key in dictionary.keys():
				dictionary[key] = Counter(dictionary[key])

	def showPlot(self):
		'''
		Create a histogram for both the distribution of Cyclomatic Complexity and NPATH 
		over all of the functions. 
		'''
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

	def adjustedRandIndex(self, functionList) -> float:
		'''
		Compute the adjusted rand index, used to compare two different
		clusterings on a set by looking at all oft he possible pairs of
		points in the set.
		'''
		n_00 = 0 # In different clusters in both clusterings 
		n_11 = 0 # In the same cluster in both clusterings
		n_01 = 0 # Different in the first clustering but not in the second
		n_10 = 0 # Same in the first clustering but not in the second 
		# Iterate through all of the (N choose 2) possible pairs  
		for funcOneIndex in range(len(functionList)):
			for funcTwoIndex in range(funcOneIndex, len(functionList)):
				pair = (functionList[funcOneIndex], functionList[funcTwoIndex])
				pointOneAPC = pair[0] # TODO  
				pointTwoAPC = pair[1] # TODO 

				pointOneNPATH = pair[0] # TODO 
				pointTwoNPATH = pair[1] # TODO 

				if pointOneAPC == pointTwoAPC:
					if pointOneNPATH == pointTwoNPATH:
						n_11 += 1
					else:
						n_10 += 1
				else:
					if pointOneNPATH == pointTwoNPATH:
						n_01 += 1
					else:
						n_00 += 1

		numerator = 2*(n_00 * n_11 - n_01 * n_10)
		denominatorOne = (n_00 + n_01) * (n_01 + n_11)
		denominatorTwo =  (n_00 + n_10) * (n_10 + n_11)
		denominator = denominatorOne + denominatorTwo
		return (numerator / denominator)

	@staticmethod
	def fromCSV(filename, location):
		'''
		Create a MetricsComparer object from a results CSV file by
		obtaining the relevant entries from each line.
		Expected file format:

		test_number, cfg_file, cyclomatic_complexity, npath_complexity, path_cplxty_class, path_cplxty_asym, path_cplxty
		'''
		results = []
		with open(filename, "r") as f:
			content = f.readlines()[1:]
			for line in content:
				try:
					filepath = line.strip().split(",")[1]
					# Don't need ID  
					result = line.strip().split(",")[2:]
					result = [filepath] + [float(result[0])] + [float(result[1])] + result[2:]
					results.append(result)
				except (IndexError, ValueError) as e:
					pass #TODO - log?

		return MetricsComparer(results, location)

	def entropy(self, probabilities) -> float:
		'''
		Given some list representing a probability distribution, return the total entropy
		Input: [p_0, p_1, ..., p_n]
		Output: H(p)
		'''
		# Check that it is a valid probability distribution 
		if sum(probabilities) != 1:
			raise ValueError("Not a valid probability distribution - does not sum to one")

		totalEntropy = 0
		for probability in probabilities:
			totalEntropy -= probability * log(probability, 2)

		return totalEntropy

	def clusterEntropy(self, clusterList) -> float:
		'''
		Calculate the entropy H(X) of a given clustering on a set.
		The input is a dictionary where each entry is a complexity
		class (representing a cluster) with a count (the number of
		things in the cluster)
		'''
		totalEntropy = 0
		totalSize = 0
		# Obtain the total size 
		for cluster in clusterList.keys():
			totalSize += len(clusterList[cluster])

		# Iterate through the clusters
		for cluster in clusterList.keys():
			clusterSize = len(clusterList[cluster])
			probabilityList = [1 / clusterSize] * clusterSize
			totalEntropy += self.entropy(probabilityList) * (clusterSize / totalSize)

		return totalEntropy

	def jointEntropy(self, clusterListOne, clusterListTwo) -> float:
		'''
		Compute H(X, Y)

		@see https://en.wikipedia.org/wiki/Joint_entropy

		The input is two dictionaries where each entry is a complexity class
		(representing a cluster) with a set of functions.
		'''
		jointEntropy = 0
		# Obtain the total size 
		for cluster in clusterListOne.keys():
			totalSize += len(clusterListOne[cluster])

		for clusterOne in clusterListOne:
			for clusterTwo in clusterListTwo:
				# Calculate the elements in common between both clusters 
				clusterOverlap = len(clusterOne.intersection(clusterTwo))
				jointEntropy -= (clusterOverlap / totalSize) * log((clusterOverlap / totalSize), 2)

		return jointEntropy

	def conditionalEntropy(self, clusterListOne, clusterListTwo) -> float:
		'''
		Calculate H(clusterListOne | clusterListTwo)

		@see https://en.wikipedia.org/wiki/Conditional_entropy
		'''
		condEntropy = 0
		# Obtain the total size 
		for cluster in clusterListOne.keys():
			totalSize += len(clusterListOne[cluster])

		# Create a table of all the overlaps 
		overlaps = [[[0] for i in range(len(clusterListOne))] for j in range(len(clusterListTwo))]
		for i in range(len(clusterListOne)):
			for j in range(len(clusterListTwo)):
				clusterOne = clusterListOne[i]
				clusterTwo = clusterListTwo[j]
				clusterOverlap = len(clusterOne.intersection(clusterTwo))
				overlaps[i][j] = clusterOverlap

		for i in range(len(clusterListTwo)):
			# Compute the marginal overlap 	
			marginalOverlap = 0
			for j in range(len(clusterListOne)):
				marginalOverlap += clusterOverlap[j][i]

			for j in range(len(clusterListOne)):
				# Calculate the elements in common between both clusters 
				clusterOne = clusterListOne[i]
				clusterTwo = clusterListTwo[j]
				numerator = overlaps[i][j] / totalSize
				denominator = marginalOverlap / totalSize
				logParam = numerator / denominator
				condEntropy -= (clusterOverlap / totalSize) * log(logParam, 2)

		return condEntropy

	def mutualInformation(self, clusterListOne, clusterListTwo) -> float:
		'''
		Calculate I(clusterListOne, clusterListTwo)

		@see https://en.wikipedia.org/wiki/Mutual_information
		'''
		condEntropy = 0
		# Obtain the total size 
		for cluster in clusterListOne.keys(): #TODO: is this supposed to be clusterListOne?
			totalSize += len(clusterListOne[cluster])

		# Create a table of all the overlaps 
		overlaps = [[[0] for i in range(len(clusterListOne))] for j in range(len(clusterListTwo))]
		for i in range(len(clusterListOne)):
			for j in range(len(clusterListTwo)):
				clusterOne = clusterListOne[i]
				clusterTwo = clusterListTwo[j]
				clusterOverlap = len(clusterOne.intersection(clusterTwo))
				overlaps[i][j] = clusterOverlap

		for i in range(len(clusterListTwo)):
			# Compute the marginal overlap 	
			marginalOverlap = 0
			for j in range(len(clusterListOne)):
				marginalOverlap += clusterOverlap[j][i]

			for j in range(len(clusterListOne)):
				# Calculate the elements in common between both clusters 
				clusterOne = clusterListOne[i]
				clusterTwo = clusterListTwo[j]
				numerator = overlaps[i][j] / totalSize
				denominator = marginalOverlap / totalSize
				logParam = numerator / denominator
				condEntropy -= (clusterOverlap / totalSize) * log(logParam, 2)

		return condEntropy

class Main():
	'''
	Handles obtaining parameters from the user, computing the 
	Path Complexity, Cyclomatic Complexity, and NPATH metrics for all 
	.dot files, and calling the MetricsComparer to compare the 3 metrics 
	if specified. 
	'''

	def createArgumentParser(self): 
		'''
		Create a parser to read command line arguments from the user 
		'''
		parser = argparse.ArgumentParser(description="")
		parser.add_argument('-f', '--filename', help="Input filename", required=True)
		parser.add_argument('-r', '--recursive', help="Recursive Mode: look for .dot files in all subfolders", action="store_true", required=False)
		parser.add_argument('-o', '--output', help="Set an output file", required=False)
		parser.add_argument('-s', '--statistics', help="Compute the metric for a given imput file", action="store_true", required=False)
		parser.add_argument('-l', '--log', help="Print logging information to STD_OUT", action="store_true", required=False)
		parser.add_argument('--logfile', help="Specifiy a file that logging information will be written to (instead of STD_OUT)", required=False)
		return parser 

	def checkArgumentErrors(self, params): 
		'''
		Throws a ValueError if the set of command line arguments given by the user 
		are invalid. 
		'''
		if os.path.isdir(params.getFilepath()):
			if params.getStatsMode():
				raise ValueError("StatsComputer takes a CSV file of results.")
		else: 
			# Not a directory, cannot be recursive
			if params.getRecursive():
				raise ValueError("Recursive mode only applies to directories")

	def setLogging(self, args): 
		'''
		Configure logging according to the parameters specified by user 
		'''
		logfile = args['logfile']
		if args['log']:
			if logfile is not None:
				# Will append to existing file by default
				logging.basicConfig(filename=logfile, level=logging.INFO)
			else:
				logging.basicConfig(level=logging.INFO)

	def getFileList(self, filePath: str, recursive: bool) -> List[str]:
		'''
		Obtain a list of the paths to all .dot files from an initial file path.
		Recursive mode will enable searching in subdirectories.
		''' 
		if os.path.isdir(filePath):
			if recursive:
				# recursive glob '**' operator matches 0 or more subdirectories
				fileList = glob2.glob(os.path.join(filePath, "**/*.dot"), recursive=True)
			else:
				fileList = glob2.glob(os.path.join(filePath, "*.dot"), recursive=False)
		else:
			fileList = [filePath]

		return fileList

	def __init__(self):
		'''
		Get the command line arguments from the user and verify that they are valid
		'''
		# Get command line arguments 
		parser = self.createArgumentParser()
		args = vars(parser.parse_args())

		params = Parameters(args['filename'], args['recursive'], args['output'], args['statistics'])

		filePath    = params.getFilepath()
		recursive   = params.getRecursive()
		self.location  = params.getOutputFile()
		statsMode   = params.getStatsMode()

		self.setLogging(args)
		self.checkArgumentErrors(params)
		fileList = self.getFileList(filePath, recursive)

		if statsMode:
			self.computeStatistics(fileList[0])
		else:
			self.computeResults(fileList)
	
	def computeResult(self, fileName: str):
		'''
		Given a single file dot file, compute the APC, Path Complexity,
		Cyclomatic Complexity, and NPATH. 
		'''
		digits = 2
		graph = Graph.fromFile(fileName)
		writeOutput(f"Working on {fileName}", self.location)
		with Timeout(seconds = 10, errorMessage = "Timeout"):
			nPathCompl = nPathComplexity(graph)
	
		try: 
			pathComplexityResult = pathComplexity(graph)
		except: 
			pathComplexityResult = "ERR"

		asymptoticComplexity = pathComplexityResult[0]
		fullPathComplexity = pathComplexityResult[1]
		return (fileName, cyclomaticComplexity(graph), nPathCompl, classify(asymptoticComplexity, "n"), 
				roundExpression(asymptoticComplexity, digits), roundExpression(fullPathComplexity, digits))

	def computeStatistics(self, fileName: str):
		'''
		Given a CSV file with all of the results given by 'computeResults,' 
		calculate the metrics used to compare APC, NPATH, and Cyclomatic 
		Complexity 
		'''
		metrics = MetricsComparer.fromCSV(fileName, self.location)
		metrics.computeMetric()

	def computeResults(self, filelist):
		'''
		Given a list of .dot files, compute the Cyclomatic Complexity, NPATH Complexity, and Path Complexity 
		for all of the files, and write the output to a file/STDOUT
		'''
		writeOutput("test_number, cfg_file, cyclomatic_complexity, npath_complexity, \
					 path_cplxty_class, path_cplxty_asym, path_cplxty", self.location)

		splitFileList = [[] for _ in range(NUM_PROCESSES)]
		for fileIndex in range(len(filelist)):
			splitFileList[fileIndex % len(splitFileList)].append(filelist[fileIndex])

		procPool = Pool(processes = NUM_PROCESSES)
		results = procPool.imap_unordered(self.threadpoolMapper, splitFileList)
		procPool.close()	
		procPool.join()

		for result in results:
			if len(result) != 0: 
				writeOutput(result, self.location)

	def threadpoolMapper(self, fileNames):
		return list(map(self.computeResult, fileNames))

def writeOutput(msg, location):
	'''
	Write a String to STDOUT or a file if specified
	'''
	if location is None: 
		print(msg)
	else:
		if os.path.isfile(location): 
			with open(location, 'w') as file: 
				file.write(msg)

if __name__ == "__main__":
	main = Main() 