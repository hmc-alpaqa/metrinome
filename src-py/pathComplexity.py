import sympy
from sympy import Matrix, eye, symbols, degree, Poly, fps, Function, simplify, rsolve, init_printing, solve 
from sympy import expand, Abs, limit, sympify, series
from utils import bigO
from math import factorial as fact 
from time import time, sleep

def getTaylorCoeffs(func, n):
	'''
	Given an arbitrary rational function
	''' 
	L = str(series(generatingFunction, x=t, x0=0, n = size)).split('+')
	taylorCoeffs = [sympify(f).subs(t, 1) for f in L]
	return taylorCoeffs

def pathComplexity(G):
	adjMat = G.adjacencyMatrix()
	adjMat[1][1] = 1
	A = Matrix(adjMat)
	
	t = symbols('t')
	dimension = adjMat.shape[0]
	X = eye(dimension) - A*t
	X_sub = X.copy()
	X_sub.col_del(0)
	X_sub.row_del(1)

	Xdet = X.det()
	denominator = Poly(-Xdet)
	generatingFunction = X_sub.det() / denominator
	
	recurrenceDegree = degree(denominator, gen=t) + 1 
	recurrenceKernel = denominator.all_coeffs()[::-1]

	size = 2*dimension + 1

	
	
	baseCases = Matrix(taylorCoeffs[dimension :
	    				dimension + recurrenceDegree - 1])
	 
	
	# Should have as many things as the recurrenceKernel
	lRange = Matrix(list(range(0, recurrenceDegree)))
	n = symbols('n')
	nRange = Matrix([n for _ in range(0, recurrenceDegree)])
	f = Function('f')
	A = Matrix(list(map(f, nRange - lRange))).dot(Matrix(recurrenceKernel))
	print("A: " + str(A))

	symbolicSol = str(rsolve(A, f(n)))
	print("Symbolic Sol: " + str(symbolicSol))
	# Make a list where each is one of [C0, ... CN] terms
	terms = [sympify(term) for term in symbolicSol.split("+")]
	print("TERMS: " + str(terms))

	numEquations = str(len(terms))
	coefficients = symbols("C0:" + numEquations) 
	factors = [i / j for i, j in zip(terms, coefficients)]
	
	invM = Matrix([[fact.replace(n, nval) for fact in factors] for nval in range(1, len(factors)+1)])**-1

	print("InvM: " + str(invM))
	print("BaseCases: " + str(baseCases))
	print("Factors: " + str(Matrix(factors)))
	boundingSolutionTerms = (invM * baseCases).dot(Matrix(factors))

	s = str(expand(boundingSolutionTerms))
	
	# Replace all complex numbers with their absolute values

	# Replace all instances of x^n with abs(x)^n

	# Split terms on '+'
	terms = [x.strip() for x in s.split("+")]
	
	return (bigO(terms, 'n'), 0)        