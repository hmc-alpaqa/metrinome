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

path = Path('../../src/tests/cFiles/example_apc/cleaned_kleedata')
analysis_path = path/'bestfitanalysis'


def expon_func(x, A, B, C):
    return A*np.exp(B*(x+C))


def weird_expon(x, A, B, C):
    return A*x*np.exp(B*(x+C))


def quadratic(x, A, B, C):
    return A*(x**2) + B*x + C


def cubic(x, A, B, C, D):
    return A*(x**3) + B*(x**2) + C*x + D


def linear(x, A, B):
    return A*x + B


def quartic(x, A, B, C, D, E):
    return B*(x**3) + C*(x**2) + D*x + A*(x**4) + E


def quintic(x, A, B, C, D, E, F):
    return C*(x**3) + D*(x**2) + E*x + B*(x**4) + A*(x**5) + F


# def AIC(resid, obs, params):
#     return obs*np.log(resid/obs)+2*params + (2*(params**2)+2*params)/(obs-params-1)

# def AIC(resid, obs, params):
#     aic = obs * np.log(resid/obs) + 2 * params
#     return aic

def AIC(resid, obs, params):
    return obs*np.log(resid/obs)+2*params + (2*(params**2)+2*params)/(obs-params-1)


def BIC(resid, obs, params):
    bic = obs * np.log(resid/obs) + params * np.log(obs)
    return bic


def do_analysis(file, column_name):
    plt.clf()
    print(file.lstrip('example_apc_functions_'))
    # last_point = 23
    fram = pd.read_csv(path / file)
    if fram.shape[0] < 8:
        print("NOT ENOUGH DATA")
        return
    x = np.array([int(i.split("=")[1]) for i in fram.iloc[:, 1]])
    y = np.array([int(j) for j in fram.loc[:, column_name]])
    plt.plot(x, y, marker='o')
    plt.savefig(
        analysis_path / file / f"graph{column_name}")
    funcs = [expon_func, weird_expon, quadratic,
             cubic, linear, quintic, quartic]
    numparams = [3, 3, 3, 4, 2, 6, 5]
    residuals_dict = {}
    coeffs_dict = {}
    params_dict = {}
    aic_dict = {}
    bic_dict = {}
    with open(analysis_path / file / f"results_{column_name}.txt", "w+") as results_file:
        for i, func in enumerate(funcs):
            plt.clf()
            plt.plot(x, y)
            try:
                params, _ = sio.curve_fit(func, x, y, maxfev=800000)
            except RuntimeError as err:
                print("Couldn't fit data")
                return
            residuals = y - func(x, *params)
            sum_residuals = np.sum(residuals**2)
            residuals_dict[func.__name__] = sum_residuals
            coeffs_dict[func.__name__] = params
            params_dict[func.__name__] = numparams[i]
            line_y = func(x, *params)
            plt.plot(x, line_y, label=func.__name__)
            aic_val = AIC(sum_residuals, len(x), numparams[i])
            aic_dict[func.__name__] = aic_val
            results_file.write(
                f"{func.__name__} has parameters {params} and residual {sum_residuals} and AIC {str(aic_val)}\n")
            plt.legend()
            plt.savefig(
                analysis_path / file / f"graph{column_name}withfits{func.__name__}")

        min_res = np.inf
        min_func = ""
        min_params = None
        min_AIC = np.inf
        for func, residual in residuals_dict.items():
            if aic_dict[func] < min_AIC:
                min_res = residual
                min_func = func
                min_params = coeffs_dict[func]
                min_AIC = aic_dict[func]
        results_file.write(f"{min_func} has the lowest AIC with AIC {min_AIC}")

    print(
        f"The minimum functional form is {min_func} with AIC {str(min_AIC)} and residual {str(min_res)} with params {str(min_params)}\n")

    # # BIC
    # min_res = np.inf
    # min_func = ""
    # min_params = None
    # min_BIC = np.inf
    # for func, residual in residuals_dict.items():
    #     if bic_dict[func] < min_BIC:
    #         min_res = residual
    #         min_func = func
    #         min_params = coeffs_dict[func]
    #         min_BIC = bic_dict[func]
    # results_file.write(f"{min_func} has the lowest BIC with BIC {min_BIC}")

    # print(
    #     f"The minimum functional form is {min_func} with BIC {str(min_BIC)} and residual {str(min_res)} with params {str(min_params)}\n")


if not os.path.exists(analysis_path):
    os.mkdir(analysis_path)

for file in os.listdir(path):
    if "." not in file and os.path.isfile(path / file):
        if not os.path.exists(analysis_path / file):
            os.mkdir(analysis_path / file)
        for column in ["CompletedPaths", "PythonTime"]:
            do_analysis(file, column)

# %%
