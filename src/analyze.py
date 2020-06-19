import time, subprocess, re
from subprocess import PIPE
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy.linalg import lstsq
from scipy.optimize import curve_fit
plt.rcParams["figure.figsize"] = (10,10)


def exp_function(x, a, b, c):
    return a * np.exp(b * x) + c

def quadratic_function(x, a, b, c):
    return a*(x**2) + b*(x) + c

def cubic_function(x, a, b, c, d):
    return a*(x**3) + b*(x**2) + c*x + d



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

    functions = ["60_array_summary"]
    breakpoints = {"60_array_summary":20}
    func_types = {"60_array_summary":exp_function}
    fields = ["ICov(%)",'BCov(%)',"CompletedPaths","GeneratedTests", "RealTime", "UserTime", "SysTime", "PythonTime"]
    # functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3', '16_binary_search', '12_check_sorted_array',
    # '11_array_max', '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order', '19_longest_common_increasing_subsequence',
    # '14_lexicographic_array_compare', '17_edit_dist', '20_bubblesort', '21_insertionsort', '22_selectionsort', '23_mergesort', '60_array_summary',
    # "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method", '50_check_sorted_or_reverse', '51_variance', '25_heapsort', '26_quicksort']


    for f in functions:
        field = "CompletedPaths"
        breakpoint = breakpoints[f]
        function_type = func_types[f]
        subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphspandas/", shell=True)
        fig1, ax1 = plt.subplots()
        data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{f}.csv")
        times = [time for time in [float(i.split()[2]) for i in data.iloc[:,0]] if time <= breakpoint]
        data_field = data[field][0:len(times)]
        a, b = curve_fit(function_type, times, data_field)
        if function_type == quadratic_function:
            function_text = f"{a[0]}x^2+{a[1]}x+{a[2]}"
        elif function_type == exp_function:
            function_text = f"{a[0]} * e^{a[1]}x + {a[2]}"
        elif function_type == cubic_function:
            function_text = f"{a[0]}x^3 + {a[1]}x^2 + {a[2]}x + {a[3]}"
        ax1.plot(times, data_field, "+g", label="original")
        ax1.plot(times, [function_type(t, *a) for t in times], label=function_text)
        ax1.set(xlabel='depth', ylabel=field, title=f)
        ax1.legend()
        ax1.grid()
        fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphspandas/{field}_{f}.png".replace("%","percent"))
        plt.close(fig1)
