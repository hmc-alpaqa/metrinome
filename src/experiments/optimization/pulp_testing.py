# This is an example of pulp working. Below it, there is an attempt
# to implement it so that it can (1) recognize Cx_y variables and 
# solve the system. This testing has been discontinued since PulP
# cannot handle complex numbers. We also tried Pyomo, but it seems
# to have a similar problem. We would need to separate complex numbers
# into real and complex parts.

from pulp import LpProblem, LpVariable, LpMinimize, LpStatus

# Create a LP problem
problem = LpProblem("SystemOfEquations", LpMinimize)

# Define variables
x = LpVariable("x", lowBound=0)
y = LpVariable("y", lowBound=0)

# Define equations
equation1 = 2 * x + 3 * y == 8
equation2 = x - y == 1

# Add equations to the problem
problem += equation1
problem += equation2

# Solve the problem
status = problem.solve()

# Print the status and optimal values
print("Status:", LpStatus[status])
print("Optimal values:")
print("x =", x.value())
print("y =", y.value())

# from pulp import LpProblem, LpVariable, LpMinimize, lpSum

# # Create a LP problem
# problem = LpProblem("MyLPProblem", LpMinimize)

# # Define variables
# x = LpVariable("x", lowBound=0)
# y = LpVariable("y", lowBound=0)

# # Define objective function
# problem += 2 * x + y

# # Define constraints
# problem += x + y >= 5
# problem += x - y <= 2

# # Solve the problem
# status = problem.solve()

# # Print the status and optimal values
# # print("Status:", LpStatus[status])
# print("Optimal values:")
# print("x =", x.value())
# print("y =", y.value())



# # Import all classes of PuLP module
# pip install pulp
# from pulp import *

# #ACTUAL: System
# # systems = [
# #     ["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"],
# #     ["-T1 + V1_0*x", "-V1_0 + V1_1*x + V1_2*x", "-V1_1 + x", "T0*x - V1_2"]
# # ]

# #systems = ["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"]
# systems = ["C0_0 + 9*C0_1 - C1_0 - 6","C0_0 + 10*C0_1 + C1_0 - 7","C0_0 + 11*C0_1 - C1_0 - 8"]

# # # Create the problem variable to contain the problem data
# # model = LpProblem("FurnitureProblem", LpMaximize)

# # ACTUAL: Create the problem variable to contain the problem data
# problem = LpProblem("SolvingSystem", LpMinimize)

# #ACTUAL: Create LpVariables from the system
# # Regular expression pattern to match the symbols
# symbol_pattern = re.compile(r'[C]\w*')

# # Create a list to store the extracted symbols
# symbol_set = []

# # # Extract symbols from the equations
# # for system in systems:
# #     for equation in system:
# #         symbols_in_equation = re.findall(symbol_pattern, equation)
# #         #print(symbols_in_equation[0])
# #         #print(type(symbols_in_equation))
# #         for i in range(len(symbols_in_equation)):
# #             if symbols_in_equation[i] not in symbol_set:
# #                 symbol_set.append(symbols_in_equation[i])

# #FIX SO THAT IT WORKS FOR A SYSTEM OF ONE GRAPH

# for equation in systems:
#     symbols_in_equation = re.findall(symbol_pattern, equation)
#     #print(symbols_in_equation[0])
#     #print(type(symbols_in_equation))
#     for i in range(len(symbols_in_equation)):
#         if symbols_in_equation[i] not in symbol_set:
#             symbol_set.append(symbols_in_equation[i])

# #Include x as a symbol
# print(f"symbol set:{symbol_set}")
# print(f"symbol's type:{type(symbol_set[0])}")

# C0_0 = LpVariable("C0_0", lowBound = 0)
# C0_1 = LpVariable("C0_0", lowBound = 0)
# C1_0 = LpVariable("C0_0", lowBound = 0)

# #variables = [LpVariable(var,lowBound=None) for var in symbol_set]
# # variables = {var: LpVariable(var,lowBound=None) for var in symbol_set}
# # print(f"variables:{variables}")
# #print(f"variable's type:{type(variables[0])}")

# # Actual

# # #ACTUAL: Create equations Pulp can read 
# # for eqs in systems:
# #     lhs = sum(eval(eq) for eq in eqs[:-1])
# #     rhs = eval(eqs[:-1])
# #     problem += lhs == rhs

# #["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"] 


# # for equation in systems:
# #     problem += eval(equation,{},variables)

# equation1 = C0_0 + 9*C0_1 - C1_0 -6
# problem += equation1

# equation2 = C0_0 + 10*C0_1 + C1_0 - 7
# problem += equation2

# equation3 = C0_0 + 11*C0_1 - C1_0 - 8
# problem += equation3

# status = problem.solve()

# print(f"Status:{LpStatus[status]}")
# #print("Optimal Solution:")

# defined_variables = []
# for var in problem.variables():
#     defined_variables.append(var.name)
# print(f"defined variables:{defined_variables}")
