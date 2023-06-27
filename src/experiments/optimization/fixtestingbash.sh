#!/bin/bash

# Set the path to your Python file
#python_file="experiments/optimization/solve_vs_nsolve.py"

# Loop 10 times
for ((i=1; i<=10; i++))
do
    echo "Running iteration $i"
    python experiments/optimization/solve_vs_nsolve.py
done
