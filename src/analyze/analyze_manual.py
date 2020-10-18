"""Perform regression to find the best fit function for Klee data."""
import subprocess
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from scipy.optimize import curve_fit  # type: ignore
plt.rcParams["figure.figsize"] = (10, 10)


def exp_function(x_val: np.ndarray, coef1: float, coef2: float, const_term: float) -> np.ndarray:
    """General exponential function with 3 parameters."""
    return coef1 * np.exp(coef2 * x_val) + const_term


def cubic_function(x_val: float, coef1: float, coef2: float,
                   coef3: float, const_term: float) -> float:
    """General cubic function with 4 parameters."""
    return coef1 * (x_val**3) + coef2 * (x_val**2) + coef3 * x_val + const_term


def quadratic_function(x_val: float, coef1: float, coef2: float, const_term: float) -> float:
    """General quadratic function with 3 parameters."""
    return coef1 * (x_val**2) + coef2 * x_val + const_term


def main() -> None:
    """
    Find the best fit function.

    For each file and a given field, and each file having a breakpoint and a function type,
    finds the best fit parameters for the function and saves them to a graph.
    """
    functions = ['26_quicksort', '17_edit_dist', '23_mergesort', '50_check_sorted_or_reverse']
    breakpoints = {'26_quicksort': 13, '17_edit_dist': 14, '23_mergesort': 14,
                   '50_check_sorted_or_reverse': 100}
    func_types = {'26_quicksort': exp_function, '17_edit_dist': exp_function,
                  '23_mergesort': exp_function, '50_check_sorted_or_reverse': quadratic_function}
    field = "CompletedPaths"
    # fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime",
    #           "UserTime", "SysTime", "PythonTime"]
    # functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3',
    #              '16_binary_search', '12_check_sorted_array', '11_array_max',
    #              '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
    #              '19_longest_common_increasing_subsequence', '14_lexicographic_array_compare',
    #              '17_edit_dist', '20_bubblesort', '21_insertionsort', '22_selectionsort',
    #              '23_mergesort', "30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method",
    #              '50_check_sorted_or_reverse', '51_variance', '25_heapsort', '26_quicksort',
    #              '60_array_summary', '61_pos_vel_acc', '62_three_loops_w_break',
    #              '63_three_loops_symbolic_bounds' ]

    for func in functions:
        breakpoint_ = breakpoints[func]
        function_type = func_types[func]
        subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/graphspandas/",
                       shell=True, check=False)
        fig1, ax1 = plt.subplots()
        data = pd.read_csv(f"/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}.csv")
        times = [time for time in [float(i.split()[2])
                                   for i in data.iloc[:, 0]] if time <= breakpoint_]
        data_field = data[field][0:len(times)]
        # pylint: disable=unbalanced-tuple-unpacking
        fitted_coeffs, _ = curve_fit(function_type, times, data_field)
        if function_type is quadratic_function:
            function_text = f"{fitted_coeffs[0]}x^2+{fitted_coeffs[1]}x+{fitted_coeffs[2]}"
        elif function_type is exp_function:
            function_text = f"{fitted_coeffs[0]} * e^{fitted_coeffs[1]}x + {fitted_coeffs[2]}"
        elif function_type is cubic_function:
            function_text = f"{fitted_coeffs[0]}x^3 + {fitted_coeffs[1]}x^2 + " + \
                            f"{fitted_coeffs[2]}x + {fitted_coeffs[3]}"
        ax1.plot(times, data_field, "+g", label="original")
        ax1.plot(times, [function_type(t, *fitted_coeffs) for t in times], label=function_text)
        ax1.set(xlabel='depth', ylabel=field, title=func)
        ax1.legend()
        ax1.grid()
        root_dir = "/app/code/tests/cFiles/fse_2020_benchmark"
        fig1.savefig(f"{root_dir}/graphspandas/{field}_{func}.png".replace("%", "percent"))
        plt.close(fig1)


if __name__ == "__main__":
    main()
