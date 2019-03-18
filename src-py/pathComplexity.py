import sympy
from sympy import Matrix, eye, symbols, degree, Poly, fps, Function, simplify, rsolve, init_printing, solve
from sympy import expand, Abs, limit, sympify, series
from utils import bigO, getTaylorCoeffs, getRecurrenceSolution
from math import factorial as fact
from time import time, sleep
from Graph import Graph

def pathComplexity(G: Graph):
        '''
        '''
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

        taylorCoeffs = getTaylorCoeffs(generatingFunction, 2 * dimension + 1)
        baseCases = Matrix(taylorCoeffs[dimension :
	    				dimension + recurrenceDegree - 1])

        # Should have as many things as the recurrenceKernel
        lRange = Matrix(list(range(0, recurrenceDegree)))
        n = symbols('n')
        nRange = Matrix([n for _ in range(0, recurrenceDegree)])

	# Solve the recurrence relation 
        f = Function('f')
        recurrenceRelation = Matrix(list(map(f, nRange - lRange)))
        recurrenceRelation = recurrenceRelation.dot(Matrix(recurrenceKernel))
        terms = getRecurrenceSolution(recurrenceRelation)

        coefficients = symbols("C0:" + str(len(terms)))
        if len(coefficients) == 1: 
                factors = [i / j for i, j in zip(terms, coefficients)]
        else: 
                factors = terms
        
        print(factors)

        M = Matrix([[fact.replace(n, nval) for fact in factors] for nval in range(1, len(factors)+1)])

        try: 
                invM = M**-1      
                boundingSolutionTerms = (invM * baseCases).dot(Matrix(factors))

                print("=== SOLUTION === " + str(boundingSolutionTerms))
                # s = str(expand(boundingSolutionTerms))
        except: 
                print("=== NOT INVERTIBLE ====")

        return (0, 0)
        # Replace all complex numbers with their absolute values

	# Replace all instances of x^n with abs(x)^n

	# Split terms on '+'
        terms = [x.strip() for x in s.split("+")]

        return (bigO(terms, 'n'), 0)
