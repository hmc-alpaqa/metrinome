import time, subprocess, re
from subprocess import PIPE
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.linalg import lstsq
plt.rcParams["figure.figsize"] = (10,10)

ramp = lambda u: np.maximum( u, 0 )
step = lambda u: ( u > 0 ).astype(float)

rampdeg = lambda u, degree: u**degree if (u > 0) else 0

def SegmentedLinearReg( X, Y, breakpoints, degree ):
    nIterationMax = 10

    breakpoints = np.sort( np.array(breakpoints) )

    dt = np.min( np.diff(X) )
    ones = np.ones_like(X)

    for i in range( nIterationMax ):
        # Linear regression:  solve A*p = Y
        # Rk = [ramp( X - xk ) for xk in breakpoints ]
        breakpoints_modified = np.concatenate(([0], breakpoints))
        Sk = [step( X - xk ) for xk in breakpoints_modified ]
        degrees = [[ [rampdeg(i, deg) for i in X-xk] for xk in breakpoints_modified] for deg in range(1, degree+1)]
        np.concatenate((Sk, np.concatenate(degrees)))
        A = np.concatenate((Sk, np.concatenate(degrees)))
        # A = np.array([ ones, X ] + Rk + Sk )
        p =  lstsq(A.transpose(), Y, rcond=None)[0]
        print(p)
        # Parameters identification:
        a, b = p[0:2]
        ck = p[ 2:2+len(breakpoints) ]
        dk = p[ 2+len(breakpoints): ]

        # Estimation of the next break-points:
        newBreakpoints = breakpoints - dk/ck

        # Stop condition
        if np.max(np.abs(newBreakpoints - breakpoints)) < dt/5:
            break

        breakpoints = newBreakpoints
    else:
        print( 'maximum iteration reached' )

    # Compute the final segmented fit:
    Xsolution = np.insert( np.append( breakpoints, max(X) ), 0, min(X) )
    ones =  np.ones_like(Xsolution)
    Rk = [ c*ramp( Xsolution - x0 ) for x0, c in zip(breakpoints, ck) ]

    Ysolution = a*ones + b*Xsolution + np.sum( Rk, axis=0 )
    return Xsolution, Ysolution

# def SegmentedLinearReg( X, Y, breakpoints , apple):
#     nIterationMax = 10
#     breakpoints = np.sort( np.array(breakpoints) )
#     dt = np.min( np.diff(X) )
#     ones = np.ones_like(X)
#     for i in range( nIterationMax ):
#         # Linear regression:  solve A*p = Y
#         Rk = [ramp( X - xk ) for xk in breakpoints ]
#         Sk = [step( X - xk ) for xk in breakpoints ]
#         A = np.array([ ones, X ] + Rk + Sk )
#         p =  lstsq(A.transpose(), Y, rcond=None)[0]
#         print(p)
#         # Parameters identification:
#         a, b = p[0:2]
#         ck = p[ 2:2+len(breakpoints) ]
#         dk = p[ 2+len(breakpoints): ]
#         # Estimation of the next break-points:
#         newBreakpoints = breakpoints - dk/ck
#         # Stop condition
#         if np.max(np.abs(newBreakpoints - breakpoints)) < dt/5:
#             break
#         breakpoints = newBreakpoints
#     else:
#         print( 'maximum iteration reached' )
#     # Compute the final segmented fit:
#     Xsolution = np.insert( np.append( breakpoints, max(X) ), 0, min(X) )
#     ones =  np.ones_like(Xsolution)
#     Rk = [ c*ramp( Xsolution - x0 ) for x0, c in zip(breakpoints, ck) ]
#     Ysolution = a*ones + b*Xsolution + np.sum( Rk, axis=0 )
#     return Xsolution, Ysolution

# functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3', '16_binary_search', '12_check_sorted_array',
# '11_array_max', '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
# '14_lexicographic_array_compare', '17_edit_dist',
# "20_bubblesort", "21_insertionsort", "22_selectionsort", "23_mergesort",
# "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method"]
functions = ['11_array_max', '10_find_val_in_array']
fields = ["ICov(%)",'BCov(%)',"CompletedPaths","GeneratedTests", "RealTime", "UserTime", "SysTime", "PythonTime"]
array_sizes = [10, 100]

def generate_graphs(func, field):
    subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphspandas/", shell=True)
    fig1, ax1 = plt.subplots()
    data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{func}.csv")
    times = [float(i.split()[2]) for i in data.iloc[:,0]]
    ax1.plot(times, data[field], label = func)
    ax1.set(xlabel='depth', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()
    fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphspandas/{field}_{func}.png".replace("%","percent"))
    plt.close(fig1)


from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from time import time 

def piecewise_poly(x, params, degree_one, degree_two, bp):
        num_params = degree_one if degree_one is not None else 3
        num_params2 = degree_two if degree_two is not None else 3
        if degree_one is not None:
            fn1 = lambda x: sum([params[i] * x**i for i in range(num_params + 1)])
        else:
            fn1 = lambda x: params[0] + params[1] * (params[2]**x)
        
        if degree_two is not None:
            fn2 = lambda x: sum([params[i + num_params + 1] * x**i for i in range(num_params2 + 1)])
        else:
            fn2 = lambda x: params[num_params + 1] + params[num_params + 2] * (params[num_params + 3]**x)
        return np.piecewise(x, [x < bp, x >= bp], [fn1, fn2])

def fit(X, Y, degree_one, degree_two):
    st = time()
    # Initialize all of the parameters.
    # params = [initial_breakpoint] + \
    num_params = degree_one if degree_one is not None else 3
    num_params2 = degree_two if degree_two is not None else 3
    params = [1 for i in range(num_params + 1)] + \
             [1 for j in range(num_params2 + 1)]
    # Hyperparameter selection - breakpoint
    min_loss = float('inf')
    best_bp = -1
    for i in X:
        fit_func = partial(piecewise_poly, degree_one=degree_one, degree_two=degree_two, bp=i)
            
        # Create a function that takes as make arguments as we have parameters, as well as the 
        # independent variable and the breakpoint value.
        func_to_optimize = lambda x, *params: fit_func(x, params)
        p, e = optimize.curve_fit(func_to_optimize, X, Y, p0=params, maxfev=5000)
        l2_loss = sum((Y - func_to_optimize(X, *p))**2)
        if l2_loss < min_loss:
            best_bp = i
            min_loss = l2_loss

    # Perform the fit
    fit_func = partial(piecewise_poly, degree_one=degree_one, degree_two=degree_two, bp=best_bp)
    # Create a function that takes as make arguments as we have parameters, as well as the 
    # independent variable and the breakpoint value.
    func_to_optimize = lambda x, *params: fit_func(x, params)
    p, e = optimize.curve_fit(func_to_optimize, X, Y, p0=params, maxfev=5000)
    l2_loss = sum((Y - func_to_optimize(X, *p))**2)
    return l2_loss, best_bp
 
if __name__ == "__main__":
    f = "04_prime"
    data = pd.read_csv(f"/Users/gabrielbessler/repos/path-complexity/src/{f}.csv")
    times = [float(i.split()[2]) for i in data.iloc[:,0]]
    data_field = data["CompletedPaths"]
    X = np.array(times)
    Y = np.array(data_field)

    try:
        err1, best_bp1 = fit(X, Y, 1, 1)
    except:
        err1, best_bp1 = float('inf'), None
    try:
        err2, best_bp2 = fit(X, Y, None, 1)
    except:
        err2, best_bp2 = float('inf'), None
    try:
        err3, best_bp3 = fit(X, Y, 1, None)
    except:
        err3, best_bp3 = float('inf'), None
    
    min_val = min(err1, err2, err3)
    if min_val == err1:
        degree_one = 1
        degree_two = 1
        best_bp = best_bp1
    elif min_val == err2:
        degree_one = None
        degree_two = 1
        best_bp = best_bp2
    elif min_val == err3:
        degree_one = 1
        degree_two = None
        best_bp = best_bp3

    fit_func = partial(piecewise_poly, degree_one=degree_one, degree_two=degree_two, bp=best_bp)
    # Create a function that takes as make arguments as we have parameters, as well as the 
    # independent variable and the breakpoint value.
    num_params = degree_one if degree_one is not None else 3
    num_params2 = degree_two if degree_two is not None else 3
    params = [1 for i in range(num_params + 1)] + \
             [1 for j in range(num_params2 + 1)]
    func_to_optimize = lambda x, *params: fit_func(x, params)
    for i in range(len(X)):
        if X[i] > best_bp:
            xd = np.linspace(0, X[i - 2], 100)
            xd2 = np.linspace(X[i-1], X[-1], 100)
            break
    p, e = optimize.curve_fit(func_to_optimize, X, Y, p0=params, maxfev=5000)
    plt.plot(X, Y, "o")
    plt.plot(xd, func_to_optimize(xd, *p), "r")
    plt.plot(xd2, func_to_optimize(xd2, *p), "b")
    plt.legend(["it's a graph", f"Line 1: {p[0:num_params+1]}", f"Line 2: {p[num_params+1:]}"])
    plt.show()
    