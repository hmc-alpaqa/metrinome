import sympy, re
from sympy import Matrix, eye, symbols, degree, Poly, fps, Function, simplify, rsolve, init_printing, solve
from sympy import expand, Abs, limit, sympify, series
from Utils import bigO, getTaylorCoeffs, getSolutionFromRoots
from math import factorial as fact
from time import time, sleep
from Graph import Graph
from mpmath import polyroots
import logging

def pathComplexity(G: Graph):
        '''
        Computes the path complexity given the CFG of some function. 

        returns both the path complexity and the asymptotic path complexity 
        '''
        adjMat = G.adjacencyMatrix()
        adjMat[1][1] = 1
        newAdjacency = Matrix(adjMat)
        
        t = symbols('t')
        dimension = adjMat.shape[0]
        xMat = eye(dimension) - newAdjacency * t
        xSub = xMat.copy()
        xSub.col_del(0)        
        xSub.row_del(1)
        xDet = xMat.det()
        denominator = Poly(-xDet)
        generatingFunction = xSub.det() / denominator

        recurrenceDegree = degree(denominator, gen=t) + 1 
        recurrenceKernel = denominator.all_coeffs()[::-1]

        test = [round(-x, 2) for x in recurrenceKernel]

        roots = polyroots(test, maxsteps=200, extraprec=200)
        
        logging.info(f"Generating Function: {generatingFunction}")
        taylorCoeffs = getTaylorCoeffs(generatingFunction, 2 * dimension + 1)
        baseCases = Matrix(taylorCoeffs[dimension :
	    				dimension + recurrenceDegree - 1])
	 
        
	# Should have as many things as the recurrenceKernel
        lRange = Matrix(list(range(0, recurrenceDegree)))
        n = symbols('n')
        nRange = Matrix([n for _ in range(0, recurrenceDegree)])
	
	# Solve the recurrence relation 
        f = Function('f')
        terms = getSolutionFromRoots(roots)

        coefficients = symbols("C0:" + str(len(terms)))
        if len(coefficients) == 1: 
                factors = [i / j for i, j in zip(terms, coefficients)]
        else:
                factors = terms

        m = Matrix([[fact.replace(n, nval) for fact in factors] for nval in range(1, len(factors)+1)])

        # try: 
        invM = m**-1  
        boundingSolutionTerms = (invM * baseCases)
        boundingSolutionTerms = boundingSolutionTerms.dot(Matrix(factors))
        s = str(expand(boundingSolutionTerms))

        # Replace all instances of x^n with abs(x)^n
        expr = "[*]\(([-][0-9]*)\)\*\*n" 
        def replaceWithAbsoluteVal(match):
            base = abs(float(match.groups()[0]))
            if base == 1: 
                return ""

            return f"{base}**n"

        s = re.sub(expr, replaceWithAbsoluteVal, s)
        s = str(simplify(sympify(s)))
        
        # Replace all complex numbers with their absolute values
        s = s

        # Split terms on '+'
        terms = [x.strip() for x in s.split(" + ")]
        newTerms = [] 
        for term in terms: 
                newTerms += str(term).split(" - ")
        APC = bigO(newTerms)

        return (APC, s)