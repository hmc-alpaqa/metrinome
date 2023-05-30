import re
from abc import ABC, abstractmethod
from collections import defaultdict, deque, Counter
from typing import Union, List


import numpy as np  # type: ignore
import sympy  # type: ignore
from mpmath import mpc, mpf, polyroots  # type: ignore
from sympy import (Basic, Float, Matrix, Poly, degree, eye, preorder_traversal, simplify, symbols,
                   sympify)


class Eliminator:

    def __init(self, systems = []):
        self.systems = systems
        self.fullsystem = [eqn for eqn in system for system in self.systems]
        self.symbs = []
        self.fullsymbs = set()
        #for system in self.systems:
        #    systemsymbs = set()
        #    for eqn in system:

                

    def simpleEliminate(self, system, symbs):
    """Takes in a system of equations and gets the gamma function"""
    if len(system) == 1:
        return system[0]
    sub = system[-1] + symbs[-1]
    if symbs[-1] in sub.free_symbols:
        for eq in system:
            if symbs[-1] in eq.free_symbols:
                sol = sympy.solve(eq, symbs[-1], dict=True)
                if len(sol) == 1:
                    sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
    if symbs[-1] in sub.free_symbols:
        print("PANIC PANIC not sure how to substitute.")
    for count, eq in enumerate(system):
        if symbs[-1] in eq.free_symbols:
            system[count] = sympy.expand(eq.subs(symbs[-1], sub))
    return sympy.expand(self.simpleEliminate(system[:-1], symbs[:-1]))

    def optimizedEliminate(self, system, symbs):
        """Takes in a system of equations and gets the gamma function"""
        if len(system) == 1:
            return system[0]
        sub = system[-1] + symbs[-1]
        if symbs[-1] in sub.free_symbols:
            for eq in system:
                if symbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, symbs[-1], dict=True)
                    if len(sol) == 1:
                        sub = sympy.expand(sub.subs(symbs[-1], sol[0][symbs[-1]]))
        if symbs[-1] in sub.free_symbols:
            print("PANIC PANIC not sure how to substitute.")
        for count, eq in enumerate(system):
            if symbs[-1] in eq.free_symbols:
                system[count] = sympy.expand(eq.subs(symbs[-1], sub))
        return sympy.expand(self.optimizedEliminate(system[:-1], symbs[:-1]))

