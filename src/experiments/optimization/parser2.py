# parser2.py
# Two parses: The first (parser2.py) can process the system of equations from string type to
# symbol.Add type. The second (parser3.py) can transform the system of equations from string
# type to symbol and then solve it. The solution worked for one of the examples, but not for 
# other. 

from sympy import symbols, sympify, parse_expr, srepr, solve
import re


#Current version of parser2.py can print things with type <class 'sympy.core.add.Add'>
#Does not work for ValueError: Error from parse_expr with transformed code: '-'
"""systems = [
    "-T0 + V0_0*x", 
    "-T1 + V1_0*x", 
    "-V0_0 + V0_1*x + V0_2*x", 
    "-V0_1 + x", 
    "T1*x - V0_2", 
    "-V1_0 + V1_1*x + V1_2*x", 
    "-V1_1 + x", 
    "T0*x - V1_2"
]
"""
systems = [
    ["-T0 + V0_0*x", "-V0_0 + V0_1*x + V0_2*x", "-V0_1 + x", "T1*x - V0_2"],
    ["-T1 + V1_0*x", "-V1_0 + V1_1*x + V1_2*x", "-V1_1 + x", "T0*x - V1_2"]
]


# Regular expression pattern to match the symbols
symbol_pattern = re.compile(r'[TVX]\w*')

# Create a set to store the extracted symbols
symbol_set = set()

# Extract symbols from the equations
for system in systems:
    for equation in system:
        symbols_in_equation = re.findall(symbol_pattern, equation)
        #print(symbols_in_equation)
        symbol_set.update(symbols_in_equation)

# Create symbols dynamically
symbol_dict = {symbol: symbols(symbol) for symbol in symbol_set}

# Create a list to store the parsed equations
equation_exprs = []

# Parse the equations and store the SymPy expressions
for system in systems:
    equations = []
    for equation in system:
        print(equation)
        parsed_equation = parse_expr(equation, local_dict=symbol_dict)
        print(parsed_equation)
        print(type(parsed_equation))
        equations.append(parsed_equation)

    equation_exprs.append(equations)

# Print the parsed equations
for system in equation_exprs:
    for equation in system:
        print(type(equation))