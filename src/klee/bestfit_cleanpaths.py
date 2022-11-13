import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sio
import math
import os
import subprocess
from sklearn.metrics import mean_squared_error
from pathlib import Path


def expon_func(x, A, B, C):
    return A*np.exp(B*(x+C))


def weird_expon(x, A, B, C):
    return A*x*np.exp(B*(x+C))


def quadratic(x, A, B):
    return A*(x**2) + B*x


def cubic(x, A, B, C):
    return A*(x**3) + B*(x**2) + C*x


def linear(x, A):
    return A*x


def quartic(x, A, B, C, D):
    return B*(x**3) + C*(x**2) + D*x + A*(x**4)


def quintic(x, A, B, C, D, E):
    return C*(x**3) + D*(x**2) + E*x + B*(x**4) + A*(x**5)


# def AIC(resid, obs, params):
#     return obs*np.log(resid/obs)+2*params + (2*(params**2)+2*params)/(obs-params-1)

def AIC(resid, obs, params):
    aic = obs * np.log(resid/obs) + 2 * params
    return aic


def BIC(resid, obs, params):
    bic = obs * np.log(resid/obs) + params * np.log(obs)
    return bic


def do_analysis(file, column_name):
    plt.clf()
    print(file)
    # last_point = 23
    fram = pd.read_csv(f"/Users/tomqlam/Desktop/dataforanalysis/{file}")
    if fram.shape[0] < 8:
        print("NOT ENOUGH DATA")
        return
    x = np.array([int(i.split("=")[1]) for i in fram.iloc[:, 1]])
    y = np.array([int(j) for j in fram.loc[:, column_name]])
    plt.plot(x, y)
    plt.savefig(
        f"/Users/tomqlam/Desktop/bestfitanalysis/{file}/graph{column_name}")
    funcs = [expon_func, weird_expon, quadratic,
             cubic, linear, quintic, quartic]
    numparams = [2, 2, 2, 3, 1, 5, 4]
    residuals_dict = {}
    coeffs_dict = {}
    params_dict = {}
    aic_dict = {}
    with open(f"/Users/tomqlam/Desktop/bestfitanalysis/{file}/results_{column_name}.txt", "w+") as results_file:
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
                f"/Users/tomqlam/Desktop/bestfitanalysis/{file}/graph{column_name}withfits{func.__name__}")

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


path = Path('../../src/tests/cFiles/example_apc/kleedata')
analysis_path = path/'bestfitanalysis'
print(path.resolve())
for file in os.listdir(path):
    if "." not in file:
        subprocess.run(
            f"mkdir {analysis_path}/{file}", shell=True)
        for column in ["CompletedPaths", "PythonTime"]:
            do_analysis(file, column)
