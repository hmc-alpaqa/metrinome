class Parameters():
	'''
	Store the user-given parameters from the command line.
	'''
	 
	def __init__(self, filepath, recursive, outputFile, statsMode):
		self.filepath = filepath
		self.recursive = recursive
		self.outputFile = outputFile
		self.statsMode = statsMode

	def getRecursive(self):
		'''
		Returns True if we should search for .dot files in any 
		subdirectory  
		'''
		return self.recursive

	def getOutputFile(self):
		'''
		Returns the name of the file that will contain all of the results 
		(Complexities for each function)
		'''
		return self.outputFile

	def getFilepath(self):
		'''
		Returns the initial filepath where we should look for .dot files 
		'''
		return self.filepath

	def getStatsMode(self):
		'''
		Returns True if we should output statistics used to compare the 
		metrics available (APC, Cyclomatic Complexity, NPATH)
		'''
		return self.statsMode
