fse_2020_benchmark"""."""
import subprocess
from functools import partial
from typing import Optional
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from numpy.linalg import lstsq  # type: ignore
from scipy import optimize  # type: ignore
plt.rcParams["figure.figsize"] = (10, 10)


def ramp(val):
    """."""
    return np.maximum(val, 0)


def step(val):
    """."""
    return (val > 0).astype(float)


def rampdeg(val, degree):
    """."""
    return val ** degree if (val > 0) else 0


def segmented_linear_reg(data_x, data_y, breakpoints, degree):
    """."""
    n_iteration_max = 10
    breakpoints = np.sort(np.array(breakpoints))
    delta_t = np.min(np.diff(data_x))
    ones = np.ones_like(data_x)

    for _ in range(n_iteration_max):
        # Linear regression: solve A*p = Y
        # Rk = [ramp(data_X - xk) for xk in breakpoints]
        breakpoints_modified = np.concatenate(([0], breakpoints))
        Sk = [step(data_x - xk) for xk in breakpoints_modified]
        degrees = [[[rampdeg(i, deg) for i in data_x - xk] for xk in breakpoints_modified]
                   for deg in range(1, degree + 1)]
        np.concatenate((Sk, np.concatenate(degrees)))
        A = np.concatenate((Sk, np.concatenate(degrees)))
        # A = np.array([ ones, X ] + Rk + Sk)
        p = lstsq(A.transpose(), data_y, rcond=None)[0]
        # Parameters identification:
        a, b = p[0: 2]
        ck = p[2: 2 + len(breakpoints)]
        dk = p[2 + len(breakpoints):]

        # Estimation of the next break-points.
        new_breakpoints = breakpoints - dk / ck

        # Stop condition.
        if np.max(np.abs(new_breakpoints - breakpoints)) < delta_t / 5:
            break

        breakpoints = new_breakpoints
    else:
        print('maximum iteration reached')

    # Compute the final segmented fit:
    solution_x = np.insert(np.append(breakpoints, max(data_x)), 0, min(data_x))
    ones = np.ones_like(solution_x)
    Rk = [c * ramp(solution_x - x0) for x0, c in zip(breakpoints, ck)]

    solution_y = a * ones + b * solution_x + np.sum(Rk, axis=0)
    return solution_x, solution_y

# def segmented_linear_reg(X, Y, breakpoints, apple):
#     n_iteration_max = 10
#     breakpoints = np.sort(np.array(breakpoints))
#     dt = np.min( np.diff(X) )
#     ones = np.ones_like(X)
#     for i in range(n_iteration_max):
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
# fields = ["ICov(%)", 'BCov(%)', "CompletedPaths", "GeneratedTests", "RealTime", "UserTime",
#           "SysTime", "PythonTime"]
# array_sizes = [10, 100]


def generate_graphs(func, field):
    """."""
    root_dir = "/app/code/tests/cFiles/fse_2020_benchmark"
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


def piecewise_poly(x_val, params, degree_one, degree_two, break_point):
    """."""
    num_params = degree_one if degree_one is not None else 3
    num_params2 = degree_two if degree_two is not None else 3
    fns = [0, 0]
    if degree_one is not None:
        fns[0] = lambda x: sum([params[i] * x**i for i in range(num_params + 1)])
    else:
        fns[0] = lambda x: params[0] + params[1] * (params[2]**x)

    if degree_two is not None:
        fns[1] = lambda x: sum([params[i + num_params + 1] * x**i for i in range(num_params2 + 1)])
    else:
        fns[1] = lambda x: params[num_params + 1] + params[num_params + 2] * \
            (params[num_params + 3]**x)
    return np.piecewise(x_val, [x_val < break_point, x_val >= break_point], fns)


def fit(data_x, data_y, degree_one, degree_two):
    """."""
    # Initialize all of the parameters.
    # params = [initial_breakpoint] + \
    num_params = degree_one if degree_one is not None else 3
    num_params2 = degree_two if degree_two is not None else 3
    params = [1 for i in range(num_params + 1)] + \
             [1 for j in range(num_params2 + 1)]
    # Hyperparameter selection - breakpoint.
    min_loss = float('inf')
    best_bp = -1
    for i in data_x:
        fit_func = partial(piecewise_poly, degree_one=degree_one, degree_two=degree_two, bp=i)

        # Create a function that takes as make arguments as we have parameters, as well as the
        # independent variable and the breakpoint value.
        def func_to_optimize(var_x, *params):
            return fit_func(var_x, params)

        fit_res, _ = optimize.curve_fit(func_to_optimize, data_x, data_y, p0=params, maxfev=5000)
        l2_loss = sum((data_y - func_to_optimize(data_x, *fit_res))**2)
        if l2_loss < min_loss:
            best_bp = i
            min_loss = l2_loss

    # Perform the fit.
    fit_func = partial(piecewise_poly, degree_one=degree_one, degree_two=degree_two, bp=best_bp)
    # Create a function that takes as make arguments as we have parameters, as well as the
    # independent variable and the breakpoint value.

    def func_to_optimize(var_x, *params):
        return fit_func(var_x, params)

    fit_res, _ = optimize.curve_fit(func_to_optimize, data_x, data_y, p0=params, maxfev=5000)
    l2_loss = sum((data_y - func_to_optimize(data_x, *fit_res))**2)
    return l2_loss, best_bp


def main():
    """."""
    subprocess.run("mkdir /app/code/tests/cFiles/fse_2020_benchmark/autobpgraphs/", shell=True, check=False)
    field = "CompletedPaths"
    functions = ['01_greatestof3', '13_check_arrays_equal', '22_selectionsort', '02_fib',
                 '14_lexicographic_array_compare', '23_mergesort', '03_sign',
                 '15_check_heap_order', '04_prime', '16_binary_search', '25_heapsort', '05_parity',
                 '17_edit_dist', '06_palindrome', '30_euclid_GCD', '10_find_val_in_array',
                 '19_longest_common_increasing_subsequence', '31_sieve_of_eratosthenes',
                 '11_array_max', '20_bubblesort', '32_newtons_method', '12_check_sorted_array',
                 '21_insertionsort', '51_variance']
    for func in functions:
        print(func)
        data = pd.read_csv(f"/app/code/tests/cFiles/fse_2020_benchmark/frames/{func}.csv")
        times = [float(i.split()[2]) for i in data.iloc[:, 0]]
        data_field = data[field]
        data_x = np.array(times)
        data_y = np.array(data_field)

        try:
            err1, best_bp1 = fit(data_x, data_y, 1, 1)
        except Exception:
            err1, best_bp1 = float('inf'), None
        try:
            err2, best_bp2 = fit(data_x, data_y, None, 1)
        except Exception:
            err2, best_bp2 = float('inf'), None
        try:
            err3, best_bp3 = fit(data_x, data_y, 1, None)
        except Exception:
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

        fit_func = partial(piecewise_poly, degree_one=degree_one, degree_two=degree_two, bp=best_bp)
        # Create a function that takes as make arguments as we have parameters, as well as the
        # independent variable and the breakpoint value.
        num_params = degree_one if degree_one is not None else 3
        num_params2 = degree_two if degree_two is not None else 3
        params = [1 for i in range(num_params + 1)] + \
                 [1 for j in range(num_params2 + 1)]

        def func_to_optimize(var_x, *params):
            """."""
            return fit_func(var_x, params)

        for i, val in enumerate(data_x):
            if val > best_bp:
                xd = np.linspace(0, data_x[i - 2], 100)
                xd2 = np.linspace(data_x[i - 1], data_x[-1], 100)
                break

        fit_res, _ = optimize.curve_fit(func_to_optimize, data_x, data_y, p0=params, maxfev=5000)

        # predicted = func_to_optimize(data_x, *p)

        left = data_x[:list(data_x).index(best_bp)]
        right = data_x[list(data_x).index(best_bp):]
        left_y = data_y[:list(data_x).index(best_bp)]
        right_y = data_y[list(data_x).index(best_bp):]

        # leftmean, rightmean = np.mean(left), np.mean(right)
        # leftstd, rightstd = np.std(left), np.std(right)

        predictedleft = func_to_optimize(left, *fit_res)
        predictedright = func_to_optimize(right, *fit_res)
        leftl2 = np.sqrt(np.sum((left_y - predictedleft)**2)) / len(predictedleft)
        rightl2 = np.sqrt(np.sum((right_y - predictedright)**2)) / len(predictedright)

        if leftl2 != 0:
            leftdiff = np.abs(left_y - predictedleft) / leftl2
        else:
            leftdiff = np.ones_like(left_y)
        if rightl2 != 0:
            rightdiff = np.abs(right_y - predictedright) / rightl2
        else:
            rightdiff = np.ones_like(right_y)

        # leftcentral = leftdiff < 2
        # rightcentral = rightdiff < 2

        x_to_fit = data_x[np.concatenate([leftdiff < 2, rightdiff < 2])]
        y_to_fit = data_y[np.concatenate([leftdiff < 2, rightdiff < 2])]

        fit_res, _ = optimize.curve_fit(func_to_optimize, x_to_fit,
                                        y_to_fit, p0=params, maxfev=5000)
        plt.plot(data_x, data_y, "o")
        plt.plot(xd, func_to_optimize(xd, *fit_res), "r")
        plt.plot(xd2, func_to_optimize(xd2, *fit_res), "b")
        plt.legend(["it's a graph", f"Line 1: {fit_res[0: num_params + 1]}",
                    f"Line 2: {fit_res[num_params + 1:]}"])
        root_dir = "/app/code/tests/cFiles/fse_2020_benchmark"
        plt.savefig(f"{root_dir}/autobpgraphs/{field}_{func}".replace("%", "percent"))
        plt.close()


if __name__ == "__main__":
    main()
