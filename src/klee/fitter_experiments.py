# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sio
import math
import os
import subprocess
from sklearn.metrics import mean_squared_error
from pathlib import Path
from inspect import signature
from icecream import ic
import plotly.express as px
import plotly.graph_objects as go


path = Path('../../src/tests/cFiles/example_apc/cleaned_kleedata')
analysis_path = path / 'bestfitanalysis'
plotly_htmls = path / 'plotly_htmls'

for dir_ in [analysis_path, plotly_htmls]:
    if not os.path.exists(dir_):
        os.mkdir(dir_)
# %%


def expon_func(x, A, B):
    return A*np.exp(B*x)


def weird_expon(x, A, B):
    return A*x*np.exp(B*x)


def constant(x, A):
    return A * np.ones(len(x))


def linear(x, A):
    return A*x


def quadratic(x, A, B):
    return A*(x**2) + B*x


def cubic(x, A, B, C):
    return A*(x**3) + B*(x**2) + C*x


def quartic(x, A, B, C, D):
    return A*(x**4) + B*(x**3) + C*(x**2) + D*x


def quintic(x, A, B, C, D, E):
    return A*(x**5) + B*(x**4) + C*(x**3) + D*(x**2) + E*x


def num_params(func):
    return len(signature(func).parameters) - 1


def AIC(resid, n, k):
    ''' corrected AIC, n: num obs, k: num params '''
    return n * np.log(resid/n) + 2*k + (2*(k**2) + 2*k)/(n - k - 0.99999)

# def BIC(resid, obs, params):
#     return obs * np.log(resid/obs) + params * np.log(obs)


# %%
def experiment_plotly(file):
    func_name = file[len('example_apc_functions_'):]
    column_name = 'CompletedPaths'
    fram = pd.read_csv(path / file)
    funcs = [constant, linear, quadratic, cubic,
             expon_func, weird_expon, quartic][::-1]
    numparams = [num_params(func) for func in funcs]

    x = np.array([int(i.split("=")[1]) for i in fram.iloc[:, 1]])
    y = np.array([int(j) for j in fram.loc[:, column_name]])
    # ensure intercept is (0, 0) (default is (1, 0))
    x -= 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='data'))
    fig.update_xaxes(title='Depth')
    fig.update_yaxes(range=[-1, max(y) + 1], title='Number of Completed Paths')

    residuals_dict = {}
    coeffs_dict = {}
    params_dict = {}
    aic_dict = {}
    name_to_func = {}
    with open(analysis_path / file / f"results_{column_name}.txt", "w+") as results_file:
        for i, func in enumerate(funcs):
            try:
                params, _ = sio.curve_fit(func, x, y, maxfev=800000)
            except RuntimeError:
                print("Couldn't fit data")
                return
            residuals = y - func(x, *params)
            # if func.__name__ in ['quadratic', 'cubic', 'quartic']:
            #     print(func.__name__, residuals)
            sum_residuals = np.sum(residuals**2)
            residuals_dict[func.__name__] = sum_residuals
            coeffs_dict[func.__name__] = params
            params_dict[func.__name__] = numparams[i]
            name_to_func[func.__name__] = func
            aic_val = AIC(sum_residuals, len(x), numparams[i])
            aic_dict[func.__name__] = aic_val
            # plt.show()
            # print(
            #     f"{func.__name__} has parameters {params} and residual {sum_residuals} and AIC {str(aic_val)}\n")
            # print(
            #     f"{func.__name__} and AIC {aic_val:3f}\n")

        func_and_AIC = [(func, aic_dict[func]) for func in aic_dict]
        func_and_AIC.sort(key=lambda x: x[1])
        # add plots, default show only top 3 lowest AICs
        for i, (func, aic) in enumerate(func_and_AIC):
            plot_x = np.linspace(min(x), max(x))
            plot_y = name_to_func[func](plot_x, *coeffs_dict[func])
            label = f'{func} {aic:.3f}'
            fig.add_trace(go.Scatter(x=plot_x, y=plot_y,
                                     name=label, mode='lines', visible=None if i < 3 else 'legendonly'))

        min_func = func_and_AIC[0][0]
        print(
            f'Best fit for {func_name} is {min_func} with AIC {func_and_AIC[0][1]}')

        fig.update_layout(title=f'{func_name}: {min_func}')
        fig.write_html(plotly_htmls / f'{func_name}.html')
        fig.show()


# %%
# run for all files
for file in os.listdir(path):
    if "." not in file and os.path.isfile(path / file):
        if not os.path.exists(analysis_path / file):
            os.mkdir(analysis_path / file)
        experiment_plotly(file)

# %%
# single file debugging
file = 'example_apc_functions_quickSort_normal'
file = 'example_apc_functions_max_value_iter_normal'
file = 'example_apc_functions_fib_rec_normal'
file = 'example_apc_functions_power_rec_normal'
file = 'example_apc_functions_' + 'polypath_notrec_eli_normal'
experiment_plotly(file)
# %%


# def experiment(file):
#     column_name = 'CompletedPaths'
#     fram = pd.read_csv(path / file)
#     funcs = [constant, linear, quadratic, cubic,
#              expon_func, weird_expon, quartic][::-1]
#     numparams = [num_params(func) for func in funcs]

#     x = np.array([int(i.split("=")[1]) for i in fram.iloc[:, 1]])
#     y = np.array([int(j) for j in fram.loc[:, column_name]])
#     # ensure intercept is (0, 0) (default is (1, 0))
#     x -= 1
#     plt.plot(x, y, marker='o')
#     plt.show()

#     residuals_dict = {}
#     coeffs_dict = {}
#     params_dict = {}
#     aic_dict = {}
#     bic_dict = {}
#     with open(analysis_path / file / f"results_{column_name}.txt", "w+") as results_file:
#         for i, func in enumerate(funcs):
#             plt.clf()
#             plt.plot(x, y)

#             try:
#                 params, _ = sio.curve_fit(func, x, y, maxfev=800000)
#             except RuntimeError as err:
#                 print("Couldn't fit data")
#                 return
#             residuals = y - func(x, *params)
#             sum_residuals = np.sum(residuals**2)
#             residuals_dict[func.__name__] = sum_residuals
#             coeffs_dict[func.__name__] = params
#             params_dict[func.__name__] = numparams[i]
#             line_y = func(x, *params)
#             plt.plot(x, line_y, label=func.__name__)
#             aic_val = AIC(sum_residuals, len(x), numparams[i])
#             aic_dict[func.__name__] = aic_val
#             plt.legend()
#             plt.savefig(
#                 analysis_path / file / f"graph{column_name}withfits{func.__name__}")
#             plt.show()
#             print(
#                 f"{func.__name__} has parameters {params} and residual {sum_residuals} and AIC {str(aic_val)}\n")
#             # print(
#             #     f"{func.__name__} and AIC {aic_val:3f}\n")

#         min_res = np.inf
#         min_func = ""
#         min_params = None
#         min_AIC = np.inf
#         for func, residual in residuals_dict.items():
#             if aic_dict[func] < min_AIC:
#                 min_res = residual
#                 min_func = func
#                 min_params = coeffs_dict[func]
#                 min_AIC = aic_dict[func]

# print(
#     f"The minimum functional form is {min_func} with AIC {str(min_AIC)} and residual {str(min_res)} with params {str(min_params)}\n")


# file = 'example_apc_functions_quickSort_normal'
# file = 'example_apc_functions_max_value_iter_normal'
# file = 'example_apc_functions_fib_rec_normal'
file = 'example_apc_functions_power_rec_normal'
experiment(file)

# if not os.path.exists(analysis_path):
#     os.mkdir(analysis_path)

# for file in os.listdir(path):
#     if "." not in file and os.path.isfile(path / file):
#         if not os.path.exists(analysis_path / file):
#             os.mkdir(analysis_path / file)
#         print('file name', file.replace('example_apc_functions_', ''))
#         experiment(file)


# %%


# def do_analysis(file, column_name):
#     plt.clf()
#     # print(file.lstrip('example_apc_functions_'))
#     print(file)
#     # last_point = 23
#     fram = pd.read_csv(path / file)
#     if fram.shape[0] < 8:
#         print("NOT ENOUGH DATA")
#         return
#     x = np.array([int(i.split("=")[1]) for i in fram.iloc[:, 1]])
#     y = np.array([int(j) for j in fram.loc[:, column_name]])
#     plt.plot(x, y, marker='o')
#     plt.savefig(
#         analysis_path / file / f"graph{column_name}")
#     funcs = reversed([linear, quadratic, cubic,
#                       expon_func, weird_expon, quartic, quintic])
#     numparams = [num_params(func) for func in funcs]
#     residuals_dict = {}
#     coeffs_dict = {}
#     params_dict = {}
#     aic_dict = {}
#     bic_dict = {}
#     with open(analysis_path / file / f"results_{column_name}.txt", "w+") as results_file:
#         for i, func in enumerate(funcs):
#             plt.clf()
#             plt.plot(x, y)
#             try:
#                 params, _ = sio.curve_fit(func, x, y, maxfev=800000)
#             except RuntimeError as err:
#                 print("Couldn't fit data")
#                 return
#             residuals = y - func(x, *params)
#             sum_residuals = np.sum(residuals**2)
#             residuals_dict[func.__name__] = sum_residuals
#             coeffs_dict[func.__name__] = params
#             params_dict[func.__name__] = numparams[i]
#             line_y = func(x, *params)
#             plt.plot(x, line_y, label=func.__name__)
#             aic_val = AIC(sum_residuals, len(x), numparams[i])
#             aic_dict[func.__name__] = aic_val
#             results_file.write(
#                 f"{func.__name__} has parameters {params} and residual {sum_residuals} and AIC {str(aic_val)}\n")
#             plt.legend()
#             plt.savefig(
#                 analysis_path / file / f"graph{column_name}withfits{func.__name__}")

#         min_res = np.inf
#         min_func = ""
#         min_params = None
#         min_AIC = np.inf
#         for func, residual in residuals_dict.items():
#             if aic_dict[func] < min_AIC:
#                 min_res = residual
#                 min_func = func
#                 min_params = coeffs_dict[func]
#                 min_AIC = aic_dict[func]
#         results_file.write(f"{min_func} has the lowest AIC with AIC {min_AIC}")

#     print(
#         f"The minimum functional form is {min_func} with AIC {str(min_AIC)} and residual {str(min_res)} with params {str(min_params)}\n")


# if not os.path.exists(analysis_path):
#     os.mkdir(analysis_path)

# for file in os.listdir(path):
#     if "." not in file and os.path.isfile(path / file):
#         if not os.path.exists(analysis_path / file):
#             os.mkdir(analysis_path / file)
#         # for column in ["CompletedPaths", "PythonTime"]:
#         for column in ["CompletedPaths"]:
#             do_analysis(file, column)

# %%
