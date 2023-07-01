#!/bin/bash

# Set the path to your Python file
#python_file="experiments/optimization/solve_vs_nsolve.py"

# Loop 10 times
# for ((i=1; i<=10; i++))
# do
#     echo "Running iteration $i"
#     python /app/code/experiments/optimization/test_newNode_eliminate_msolve.py
# done

python /app/code/tests/test_apc.py

python /app/code/tests/test_rapc.py

python /app/code/tests/test_fcapc.py

python /app/code/tests/test_nfcapc.py

python /app/code/tests/test_getrgf.py #must run this in order for mergeTestResult to work

python /app/code/tests/mergeTestResult.py




