"""."""
import subprocess
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from numpy.linalg import lstsq  # type: ignore
from scipy.optimize import curve_fit  # type: ignore
plt.rcParams["figure.figsize"] = (10, 10)


def exp_function(x_val, coef1, coef2, const_term):
    """."""
    return coef1 * np.exp(coef2 * x_val) + const_term



def cubic_function(x_val, coef1, coef2, coef3, const_term):
    return coef1*(x_val**3) + coef2*(x_val**2) + coef3*x_val + const_term


def quadratic_function(x_val, coef1, coef2, const_term):
    """."""
    return coef1 * (x_val**2) + coef2 * (x_val) + const_term


def generate_graphs(func, field):
    """."""
    root_dir = f"/app/code/tests/cFiles/simpleAlgs"
    subprocess.run(f"mkdir {root_dir}/graphspandas/", shell=True, check=False)
    fig1, ax1 = plt.subplots()
    data = pd.read_csv(f"{root_dir}/frames/{func}.csv")
    times = [float(i.split()[2]) for i in data.iloc[:, 0]]
    ax1.plot(times, data[field], label=func)
    ax1.set(xlabel='depth', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()
    fig1.savefig(f"{root_dir}/graphspandas/{field}_{func}.png".replace("%", "percent"))
    plt.close(fig1)



def main():
    """."""
    functions = ['26_quicksort', '17_edit_dist', '23_mergesort', '50_check_sorted_or_reverse']
    breakpoints = {'26_quicksort': 13, '17_edit_dist': 14, '23_mergesort': 14,
                   '50_check_sorted_or_reverse': 100}
    func_types = {'26_quicksort': exp_function, '17_edit_dist': exp_function,
                  '23_mergesort': exp_function, '50_check_sorted_or_reverse': quadratic_function}
    # fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime",
    #           "UserTime", "SysTime", "PythonTime"]
    # functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3',
    #              '16_binary_search', '12_check_sorted_array', '11_array_max',
    #              '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
    #              '19_longest_common_increasing_subsequence', '14_lexicographic_array_compare',
    #              '17_edit_dist', '20_bubblesort', '21_insertionsort', '22_selectionsort',
    #              '23_mergesort', "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method",
    #              '50_check_sorted_or_reverse', '51_variance', '25_heapsort', '26_quicksort',
    #              '60_array_summary', '61_pos_vel_acc', '62_three_loops_w_break', '63_three_loops_symbolic_bounds' ]

    for func in functions:
        field = "CompletedPaths"
        breakpoint_ = breakpoints[func]
        function_type = func_types[func]
        subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphspandas/",
                       shell=True, check=False)
        fig1, ax1 = plt.subplots()
        data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{func}.csv")
        times = [time for time in [float(i.split()[2])
                                   for i in data.iloc[:, 0]] if time <= breakpoint_]
        data_field = data[field][0:len(times)]
        a, _ = curve_fit(function_type, times, data_field)
        if function_type is quadratic_function:
            function_text = f"{a[0]}x^2+{a[1]}x+{a[2]}"
        elif function_type is exp_function:
            function_text = f"{a[0]} * e^{a[1]}x + {a[2]}"
        elif function_type == cubic_function:
            function_text = f"{a[0]}x^3 + {a[1]}x^2 + {a[2]}x + {a[3]}"
        ax1.plot(times, data_field, "+g", label="original")
        ax1.plot(times, [function_type(t, *a) for t in times], label=function_text)
        ax1.set(xlabel='depth', ylabel=field, title=func)
        ax1.legend()
        ax1.grid()
        root_dir = "/app/code/tests/cFiles/simpleAlgs"
        fig1.savefig(f"{root_dir}/graphspandas/{field}_{func}.png".replace("%", "percent"))
        plt.close(fig1)


if __name__ == "__main__":
    main()
