import time, subprocess, re
from subprocess import PIPE
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.linalg import lstsq
from scipy.optimize import curve_fit
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
        print(A)
        # A = np.array([ ones, X ] + Rk + Sk )
        p =  lstsq(A.transpose(), Y, rcond=None)[0]
        print(p)
        # Parameters identification:
        a = p[0]
        dk = p[1:1+len(breakpoints)]
        b = p[1+len(breakpoints)]
        ck = p[2+len(breakpoints):]
        print(a)
        print(dk)
        print(b)
        print(ck)
        # a, b = p[0:2]
        # ck = p[ 2:2+len(breakpoints) ]
        # dk = p[ 2+len(breakpoints): ]

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

def exp_function(x, a, b, c):
    return a * np.exp(b * x) + c

def quadratic_function(x, a, b, c):
    return a*(x**2) + b*(x) + c

# functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3', '16_binary_search', '12_check_sorted_array',
# '11_array_max', '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
# '14_lexicographic_array_compare', '17_edit_dist',
# "20_bubblesort", "21_insertionsort", "22_selectionsort", "23_mergesort",
# "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method"]
# functions = ['22_selectionsort', '16_binary_search', '25_heapsort']
# breakpoints = {'22_selectionsort':20, '16_binary_search':20, '25_heapsort':12  }
# functions = ['30_euclid_GCD', '11_array_max', '20_bubblesort', '21_insertionsort']
# breakpoints = {'30_euclid_GCD':18, '11_array_max':20, '20_bubblesort':19, '21_insertionsort':20}
# functions = ['50_check_sorted_or_reverse']
# breakpoints = {'50_check_sorted_or_reverse':100}
functions = ['26_quicksort', '17_edit_dist', '23_mergesort']
breakpoints = {'26_quicksort':13, '17_edit_dist':14, '23_mergesort':14}
fields = ["ICov(%)",'BCov(%)',"CompletedPaths","GeneratedTests", "RealTime", "UserTime", "SysTime", "PythonTime"]

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



if __name__ == "__main__":
    # for f in functions:
    #     for field in fields:
    #         generate_graphs(f, field)
    # for f in functions:
    #     for sz in array_sizes:
    #         for field in fields:
    #             temp_func = f+str(sz)
    #             fig1, ax1 = plt.subplots()
    #             data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{temp_func}.csv")
    #             times = [float(i.split()[2]) for i in data.iloc[:,0]]
    #             init_bps = [3]
    #             ax1.plot(times, data[field], label = "OG")
    #             ax1.plot(*SegmentedLinearReg(times, data[field], init_bps), '-r', label="REGRESSION")
    #             ax1.set(xlabel='depth', ylabel=field, title=temp_func)
    #             ax1.legend()
    #             ax1.grid()
    #             fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphspandas/{field}_{temp_func}.png".replace("%","percent"))
    #             plt.close(fig1)
    # bp = [3, 7]
    # X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # Y = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 4, 3, 2, 1]
    # print(SegmentedLinearReg(X, Y, bp, 2))

    for f in functions:
        field = "CompletedPaths"
        breakpoint = breakpoints[f]
        subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphspandas/", shell=True)
        fig1, ax1 = plt.subplots()
        data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{f}.csv")
        times = [time for time in [float(i.split()[2]) for i in data.iloc[:,0]] if time <= breakpoint]
        data_field = data[field][0:len(times)]
        a, b = curve_fit(exp_function, times, data_field)
        ax1.plot(times, data_field, "+g", label="original")
        ax1.plot(times, [exp_function(t, *a) for t in times], label="regression")
        ax1.set(xlabel='depth', ylabel=field, title=f)
        ax1.legend()
        ax1.grid()
        fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphspandas/{field}_{f}.png".replace("%","percent"))
        plt.close(fig1)
        print(f)
        print(f"{a[0]} * e^{a[1]}x + {a[2]}")
        # print(f"{a[0]}x^2+{a[1]}x+{a[2]}")
