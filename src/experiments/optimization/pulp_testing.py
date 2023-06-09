# Import all classes of PuLP module
from pulp import *

#ACTUAL: System
# systems = [
#     ["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"],
#     ["-T1 + V1_0*x", "-V1_0 + V1_1*x + V1_2*x", "-V1_1 + x", "T0*x - V1_2"]
# ]

#systems = ["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"]
systems = ["C0_0 + 9*C0_1 - C1_0 - 6","C0_0 + 10*C0_1 + C1_0 - 7","C0_0 + 11*C0_1 - C1_0 - 8"]

# # Create the problem variable to contain the problem data
# model = LpProblem("FurnitureProblem", LpMaximize)

# ACTUAL: Create the problem variable to contain the problem data
problem = LpProblem("SolvingSystem", LpMinimize)

#ACTUAL: Create LpVariables from the system
# Regular expression pattern to match the symbols
symbol_pattern = re.compile(r'[C]\w*')

# Create a list to store the extracted symbols
symbol_set = []

# # Extract symbols from the equations
# for system in systems:
#     for equation in system:
#         symbols_in_equation = re.findall(symbol_pattern, equation)
#         #print(symbols_in_equation[0])
#         #print(type(symbols_in_equation))
#         for i in range(len(symbols_in_equation)):
#             if symbols_in_equation[i] not in symbol_set:
#                 symbol_set.append(symbols_in_equation[i])

#FIX SO THAT IT WORKS FOR A SYSTEM OF ONE GRAPH

for equation in systems:
    symbols_in_equation = re.findall(symbol_pattern, equation)
    #print(symbols_in_equation[0])
    #print(type(symbols_in_equation))
    for i in range(len(symbols_in_equation)):
        if symbols_in_equation[i] not in symbol_set:
            symbol_set.append(symbols_in_equation[i])

#Include x as a symbol
print(f"symbol set:{symbol_set}")
print(f"symbol's type:{type(symbol_set[0])}")

# variables = [LpVariable(var,lowBound=None) for var in symbol_set]
variables = {var: LpVariable(var,lowBound=None) for var in symbol_set}
print(f"variables:{variables}")
#print(f"variable's type:{type(variables[0])}")

# Actual

# #ACTUAL: Create equations Pulp can read 
# for eqs in systems:
#     lhs = sum(eval(eq) for eq in eqs[:-1])
#     rhs = eval(eqs[:-1])
#     problem += lhs == rhs

#["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"] 


for equation in systems:
    problem += eval(equation,{},variables)

# problem += -T0 + V0_0*x == 0
# problem += -V0_0 + V0_1*x + V0_2*x == 0
# problem += -V0_1 + x == 0
# problem += T1*x - V0_2 == 0

status = problem.solve()

print(f"Status:{LpStatus[status]}")
#print("Optimal Solution:")

defined_variables = []
for var in problem.variables():
    defined_variables.append(var.name)
print(f"defined variables:{defined_variables}")
