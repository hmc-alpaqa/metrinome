"""."""
import subprocess
import matplotlib.pyplot as plt  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from numpy.linalg import lstsq  # type: ignore
from scipy.optimize import curve_fit  # type: ignore
plt.rcParams["figure.figsize"] = (10, 10)


def step(val):
    """."""
    return (val > 0).astype(float)


def ramp(val):
    """."""
    return np.maximum(val, 0)


def rampdeg(val, degree):
    """."""
    return val ** degree if (val > 0) else 0


def segmented_linear_reg(data_x, data_y, breakpoints, degree):
    """."""
    n_iterations_max = 10

    breakpoints = np.sort(np.array(breakpoints))

    delta_t = np.min(np.diff(data_x))
    ones = np.ones_like(data_x)

    for _ in range(n_iterations_max):
        # Linear regression:  solve A*p = data_y
        # Rk = [ramp( X - xk ) for xk in breakpoints ]
        breakpoints_modified = np.concatenate(([0], breakpoints))
        Sk = [step(data_x - xk) for xk in breakpoints_modified]
        degrees = [[[rampdeg(i, deg) for i in data_x - xk] for xk in breakpoints_modified]
                   for deg in range(1, degree + 1)]
        A = np.concatenate((Sk, np.concatenate(degrees)))
        print(A)
        # A = np.array([ ones, X ] + Rk + Sk )
        p = lstsq(A.transpose(), data_y, rcond=None)[0]
        print(p)
        # Parameters identification:
        a = p[0]
        dk = p[1: 1 + len(breakpoints)]
        b = p[1 + len(breakpoints)]
        ck = p[2 + len(breakpoints):]
        print(a, dk, b, ck)
        # a, b = p[0:2]
        # ck = p[ 2:2+len(breakpoints) ]
        # dk = p[ 2+len(breakpoints): ]

        # Estimation of the next break-points:
        new_breakpoints = breakpoints - dk / ck

        # Stop condition
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

# def segmented_linear_reg( X, Y, breakpoints , apple):
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


def exp_function(x_val, coef1, coef2, const_term):
    """."""
    return coef1 * np.exp(coef2 * x_val) + const_term


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
