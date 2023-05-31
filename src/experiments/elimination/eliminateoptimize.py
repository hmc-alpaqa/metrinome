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

    def __init__(self, systems = []):
        self.systems = systems
        self.fullsystem = [eqn for system in self.systems for eqn in system]
        self.symbs = []
        self.fullsymbs = set()
        self.parse()

    def parse(self):
        for system in self.systems:
            systemsymbs = set()
            for eqn in system:
                eqn.replace("-", "")
                eqn.replace("+", "")
                eqn.replace("*", " ") # delete this text processing & above lines
                eqn.split(" ")
                for symb in eqn:
                    if symb != "": # replace with if symb contains V, T, or x
                        systemsymbs.add(symbols(symb))
                        self.fullsymbs.add(symbols(symb))
            self.symbs += list(systemsymbs)
        self.fullsymbs = list(self.fullsymbs)

    def simpleEliminate(self):
        """Takes in a system of equations and gets the gamma function"""
        if len(self.fullsystem) == 1:
            return self.fullsystem[0]
        sub = self.fullsystem[-1] + self.fullsymbs[-1]
        if self.fullsymbs[-1] in sub.free_symbols:
            for eq in self.fullsystem:
                if self.fullsymbs[-1] in eq.free_symbols:
                    sol = sympy.solve(eq, self.fullsymbs[-1], dict=True)
                    if len(sol) == 1:
                        sub = sympy.expand(sub.subs(self.fullsymbs[-1], sol[0][self.fullsymbs[-1]]))
        if symbs[-1] in sub.free_symbols:
            print("PANIC PANIC not sure how to substitute.")
        for count, eq in enumerate(self.fullsystem):
            if self.fullsymbs[-1] in eq.free_symbols:
                self.fullsystem[count] = sympy.expand(eq.subs(self.fullsymbs[-1], sub))
        return sympy.expand(self.simpleEliminate(self.fullsystem[:-1], self.fullsymbs[:-1]))

    def optimizedEliminate(self):
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

def main():
    systems = [["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"], ["-T1 + V1_0*x", "-V1_0 + V1_1*x + V1_2*x", "-V1_1 + x", "T0*x - V1_2"]]
    elim = Eliminator(systems)
    elim.simpleEliminate()

if __name__ == "__main__":
    main()