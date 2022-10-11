"""
Plots Klee data points on log-linear and log-log scales to
compare fit to different function types.
"""
import subprocess

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

def loglog(data_x: np.ndarray, data_y: np.ndarray, name: str) -> None:
    plt.loglog(data_x, data_y, label="log_log")
    plt.savefig(f"/Users/maxszostak/Documents/HMC/Bang_research/loglog_plots/{name}_loglog.png")
    plt.close()

def loglinear(data_x: np.ndarray, data_y: np.ndarray, name: str) -> None:
    ax = plt.subplot(211)
    ax.set_yscale('log')
    ax.plot(data_x, data_y, label="log_log")
    plt.savefig(f"/Users/maxszostak/Documents/HMC/Bang_research/loglinear_plots/{name}_loglinear.png")
    plt.close()

test1x = [0,1,2,3,4]
test1y = [num**2 for num in test1x]
loglog(test1x,test1y,"test1")
loglinear(test1x,test1y,"test1")

test2x = test1x
test2y = [2**num for num in test2x]
loglog(test2x,test2y,"test2")
loglinear(test2x,test2y,"test2")
