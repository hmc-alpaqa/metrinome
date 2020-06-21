"""
Perform regression on Klee data.

Will try to automatically find the best breakpoint
and the best function type.
"""
import subprocess
from functools import partial
from typing import Optional
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from scipy import optimize  # type: ignore
plt.rcParams["figure.figsize"] = (10, 10)


def ramp(val):
    """Return val if it is positive, 0 otherwise."""
    return np.maximum(val, 0)


def step(val):
    """Return 1 if val is positive, 0 otherwise."""
    return (val > 0).astype(float)


def rampdeg(val, degree: int):
    """Return val^deg if val is positive, 0 otherwise."""
    return val ** degree if (val > 0) else 0


def piecewise_eval(x_val: float, params, degree_one: Optional[int],
                   degree_two: Optional[int], break_point: float):
    """Evaluate a piecewise polynomial at a point."""
    num_params = degree_one if degree_one is not None else 3
    num_params2 = degree_two if degree_two is not None else 3
    fns = []
    if degree_one is not None:
        fns += [lambda x: sum([params[i] * x**i for i in range(num_params + 1)])]
    else:
        fns += [lambda x: params[0] + params[1] * (params[2]**x)]

    if degree_two is not None:
        fns += [lambda x: sum([params[i + num_params + 1] * x**i for i in range(num_params2 + 1)])]
    else:
        fns += [lambda x: params[num_params + 1] + params[num_params + 2] * (
            params[num_params + 3]**x)]
    return np.piecewise(x_val, [x_val < break_point, x_val >= break_point], fns)


def fit(data_x, data_y, degree_one: Optional[int], degree_two: Optional[int]):
    """Find the best breakpoint."""
    # Initialize all of the parameters.
    # params = [initial_breakpoint] + \
    num_params = degree_one if degree_one is not None else 3
    num_params2 = degree_two if degree_two is not None else 3
    params = [1 for i in range(num_params + 1)] + \
             [1 for j in range(num_params2 + 1)]
    # Hyperparameter selection - breakpoint.
    min_loss = float('inf')
    best_bp = -1
    # Create a function that takes as make arguments as we have parameters, as well as the
    # independent variable and the breakpoint value.

    def func_to_optimize(var_x, *params):
        return fit_func(var_x, params)

    for i in data_x:
        fit_func = partial(
            piecewise_eval, degree_one=degree_one, degree_two=degree_two, break_point=i)

        fit_res, _ = optimize.curve_fit(func_to_optimize, data_x, data_y, p0=params, maxfev=5000)
        l2_loss = sum((data_y - func_to_optimize(data_x, *fit_res))**2)
        if l2_loss < min_loss:
            best_bp = i
            min_loss = l2_loss

    # Perform the fit.
    fit_func = partial(
        piecewise_eval, degree_one=degree_one, degree_two=degree_two, break_point=best_bp)
    # Create a function that takes as make arguments as we have parameters, as well as the
    # independent variable and the breakpoint value.

    fit_res, _ = optimize.curve_fit(func_to_optimize, data_x, data_y, p0=params, maxfev=5000)
    l2_loss = sum((data_y - func_to_optimize(data_x, *fit_res))**2)
    return l2_loss, best_bp


def get_best_degree(data_x, data_y):
    """."""
    try:
        err1, best_bp1 = fit(data_x, data_y, 1, 1)
    except RuntimeError:
        err1, best_bp1 = float('inf'), None
    try:
        err2, best_bp2 = fit(data_x, data_y, None, 1)
    except RuntimeError:
        err2, best_bp2 = float('inf'), None
    try:
        err3, best_bp3 = fit(data_x, data_y, 1, None)
    except RuntimeError:
        err3, best_bp3 = float('inf'), None
    min_val = min(err1, err2, err3)
    degree_one: Optional[int]
    degree_two: Optional[int]
    if min_val == err1:
        degree_one = 1
        degree_two = 1
        best_bp = best_bp1
    elif min_val == err2:
        degree_one = None
        degree_two = 1
        best_bp = best_bp2
    else:
        degree_one = 1
        degree_two = None
        best_bp = best_bp3
    return degree_one, degree_two, best_bp


def regression(data_x, data_y, name: str) -> None:
    """Perform the regression with automatic breakpoints for a single function."""
    degree_one, degree_two, best_bp = get_best_degree(data_x, data_y)

    fit_func = partial(
        piecewise_eval, degree_one=degree_one, degree_two=degree_two, break_point=best_bp)
    # Create a function that takes as make arguments as we have parameters, as well as the
    # independent variable and the breakpoint value.
    num_params = degree_one if degree_one is not None else 3
    params = [1 for i in range(num_params + 1)] + \
             [1 for j in range((degree_two if degree_two is not None else 3) + 1)]

    # pylint: disable=W0640
    def func_to_optimize(var_x, *params):
        """."""
        return fit_func(var_x, params)

    for i, val in enumerate(data_x):
        if val > best_bp:
            xd1 = np.linspace(0, data_x[i - 2], 100)
            xd2 = np.linspace(data_x[i - 1], data_x[-1], 100)
            break

    fit_res = optimize.curve_fit(func_to_optimize, data_x, data_y, p0=params, maxfev=5000)[0]
    # predicted = func_to_optimize(data_x, *p)
    # left = data_x[:list(data_x).index(best_bp)]
    # right = data_x[list(data_x).index(best_bp):]
    # left_y = data_y[:list(data_x).index(best_bp)]
    # right_y = data_y[list(data_x).index(best_bp):]
    # predictedleft = func_to_optimize(left, *fit_res)
    # predictedright = func_to_optimize(right, *fit_res)
    # leftl2 = np.sqrt(np.sum((left_y - predictedleft)**2)) / len(predictedleft)
    # rightl2 = np.sqrt(np.sum((right_y - predictedright)**2)) / len(predictedright)
    # if leftl2 != 0:
    #     leftdiff = np.abs(left_y - predictedleft) / leftl2
    # else:
    #     leftdiff = np.ones_like(left_y)
    # if rightl2 != 0:
    #     rightdiff = np.abs(right_y - predictedright) / rightl2
    # else:
    #     rightdiff = np.ones_like(right_y)
    # leftcentral = leftdiff < 2
    # rightcentral = rightdiff < 2
    # x_to_fit = data_x[np.concatenate([leftdiff < 2, rightdiff < 2])]
    # y_to_fit = data_y[np.concatenate([leftdiff < 2, rightdiff < 2])]
    # fit_res, _ = optimize.curve_fit(func_to_optimize, x_to_fit,
    # y_to_fit, p0=params, maxfev=5000)
    plt.plot(data_x, data_y, "o")
    plt.plot(xd1, func_to_optimize(xd1, *fit_res), "r")
    plt.plot(xd2, func_to_optimize(xd2, *fit_res), "b")
    plt.legend(["it's a graph", f"Line 1: {fit_res[0: num_params + 1]}",
                f"Line 2: {fit_res[num_params + 1:]}"])
    root_dir = f"/app/code/tests/cFiles/fse_2020_benchmark/"
    plt.savefig((f"{root_dir}autobpgraphs/{name}").replace("%", "percent"))
    plt.close()


def main() -> None:
    """
    Run regression on each function.

    Tries to automatically find the breakpoints and function types
    that minimize the loss.
    """
    subprocess.run(
        f"mkdir /app/code/tests/cFiles/fse_2020_benchmark/autobpgraphs/", shell=True, check=False)
    functions = ['01_greatestof3', '13_check_arrays_equal', '22_selectionsort', '02_fib',
                 '14_lexicographic_array_compare', '23_mergesort', '03_sign',
                 '15_check_heap_order', '04_prime', '16_binary_search', '25_heapsort', '05_parity',
                 '17_edit_dist', '06_palindrome', '30_euclid_GCD', '10_find_val_in_array',
                 '19_longest_common_increasing_subsequence', '31_sieve_of_eratosthenes',
                 '11_array_max', '20_bubblesort', '32_newtons_method', '12_check_sorted_array',
                 '21_insertionsort', '51_variance']
    field = f"CompletedPaths"
    for func in functions:
        data = pd.read_csv(f"/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}.csv")
        data_x = np.array([float(i.split()[2]) for i in data.iloc[:, 0]])
        data_y = np.array(data[field])
        regression(data_x, data_y, f"{field}_{func}")


if __name__ == "__main__":
    main()
