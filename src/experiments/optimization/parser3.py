#parser3.py
# Two parses: The first (parser2.py) can process the system of equations from string type to
# symbol.Add type. The second (parser3.py) can transform the system of equations from string
# type to symbol and then solve it. The solution worked for one of the examples, but not for 
# other.

from sympy import symbols, parse_expr, solve
import re

# Example 1: Solution doesn't match gamma function's solution
system = [
    "-T0 + V0_0*x", 
    "-T1 + V1_0*x", 
    "-V0_0 + V0_1*x + V0_2*x", 
    "-V0_1 + x", 
    "T1*x - V0_2", 
    "-V1_0 + V1_1*x + V1_2*x", 
    "-V1_1 + x", 
    "T0*x - V1_2"
]

# Example 2: Solution matches gamma function's solution
"""system = [
    "-T0 + V0_0*x",
    "-V0_0 + V0_1*x + V0_2*x",
    "-V0_1 + x",
    "T1*x - V0_2"
]"""

# Regular expression pattern to match the symbols
symbol_pattern = re.compile(r'[TVX]\w*')
print(type(symbols("V0_0")))
print(type(symbols("*")))

# Create a set to store the extracted symbols
symbol_set = set()

# Extract symbols from the equations
for equation in system:
    symbols_in_equation = re.findall(symbol_pattern, equation)
    symbol_set.update(symbols_in_equation)

# Create symbols dynamically
symbol_dict = {symbol: symbols(symbol) for symbol in symbol_set}
#printing all symbols
for symbol, value in symbol_dict.items():
    print(f"{symbol}: {type(value)}")

# Create a list to store the parsed equations
equation_exprs = []

# Parse the equations and store the SymPy expressions
for equation in system:
    parsed_equation = parse_expr(equation, local_dict=symbol_dict)
    equation_exprs.append(parsed_equation)

print("Parsed equations system")
for i in range(len(equation_exprs)):
    print(equation_exprs[i])
    print(type(equation_exprs[i]))

# Solve the system of equations
solution = solve(equation_exprs, *list(symbol_dict.values()))

print("Solutions")
# Print the solutions
for variable, value in solution.items():
    print(f"{variable}: {value}")
    print(type(value))