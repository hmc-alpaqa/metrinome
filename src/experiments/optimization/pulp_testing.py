# Import all classes of PuLP module
from pulp import *

#ACTUAL: System
systems = [
    ["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"],
    ["-T1 + V1_0*x", "-V1_0 + V1_1*x + V1_2*x", "-V1_1 + x", "T0*x - V1_2"]
]

# # Create the problem variable to contain the problem data
# model = LpProblem("FurnitureProblem", LpMaximize)

# ACTUAL: Create the problem variable to contain the problem data
problem = LpProblem("SolvingSystem", LpMinimize)

#ACTUAL: Create LpVariables from the system
# Regular expression pattern to match the symbols
symbol_pattern = re.compile(r'[TVX]\w*')

# Create a list to store the extracted symbols
symbol_set = []

# Extract symbols from the equations
for system in systems:
    for equation in system:
        symbols_in_equation = re.findall(symbol_pattern, equation)
        #print(symbols_in_equation[0])
        #print(type(symbols_in_equation))
        for i in range(len(symbols_in_equation)):
            if symbols_in_equation[i] not in symbol_set:
                symbol_set.append(symbols_in_equation[i])
print(f"symbol set:{symbol_set}")
print(f"symbol's type:{type(symbol_set[0])}")
variables = [LpVariable(var,lowBound=None) for var in symbol_set]
print(f"variables:{variables}")
print(f"variable's type:{type(variables[0])}")

"""
# # Create 3 variables tables, chairs, and bookcases
# x1 = LpVariable("tables", 0, None, LpInteger)
# x2 = LpVariable("chairs", 0, None, LpInteger) 
# x3 = LpVariable("bookcases", 0, None, LpInteger)

# Create maximize objective function
model += 40 * x1 + 30 * x2 + 45 * x3 

"""

# ACtual


# #ACTUAL: Create equations Pulp can read 
# for eqs in systems:
#     lhs = sum(eval(eq) for eq in eqs[:-1])
#     rhs = eval(eqs[-1])
#     problem += lhs == rhs

status = problem.solve()

print(f"Status:{LpStatus[status]}")
#print("Optimal Solution:")
"""
# Create three constraints
model += 2 * x1 + 1 * x2 + 2.5 * x3 <= 60, "Labour"
model += 0.8 * x1 + 0.6 * x2 + 1.0 * x3 <= 16, "Machine"
model += 30 * x1 + 20 * x2 + 30 * x3 <= 400, "wood"
model += x1 >= 10, "tables"

# The problem is solved using PuLP's choice of Solver
model.solve()

# Each of the variables is printed with it's resolved optimum value
for v in model.variables():
    print(v.name, "=", v.varValue)
"""