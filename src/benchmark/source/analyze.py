"""
Plots Klee data points on log-linear and log-log scales to
compare fit to different function types.
"""
import subprocess

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from pathlib import Path
import os
import subprocess

basedir = "/app/code/benchmark"

def create_plots(csv_file: str) -> None:
    """ 
    Given a csv file name in the benchmark/klee_data folder, 
    creates a folder containing 3 plots of its points in the benchmark/plots directory.
    """

    if (csv_file[-7:] != "_normal"):
        return

    # Read csv data into 2 numpy arrays (x and y axes)
    csv_dataframe = pd.read_csv(basedir+"/klee_data/"+csv_file)
    data_x = np.array([int(i.split("=")[1]) for i in csv_dataframe.iloc[:,0]])
    data_y = np.array([int(j) for j in csv_dataframe.loc[:, "CompletedPaths"]])

    # Get the name of the file without the ".csv" extension
    name = csv_file.split(".")[0]

    # Create the 3 plots
    plots_dir = basedir + "/plots" + f"/{name}"
    plots(data_x, data_y, plots_dir, name)

def plots(data_x: np.ndarray, data_y: np.ndarray, fig_path: str, name: str) -> None:
    fig, axs  = plt.subplots(2,2)  # 2 rows, 2 cols

    fig.tight_layout(pad=3.5)
    fig.suptitle(name)

    axs[0][0].set_title("linear")
    axs[0][0].plot(data_x, data_y)

    axs[0][1].set_title("log log")
    axs[0][1].loglog(data_x, data_y)

    axs[1][0].set_title("log linear")
    axs[1][0].set_yscale('log')
    axs[1][0].plot(data_x, data_y)

    fig.delaxes(axs[1][1])

    plt.show()
    plt.savefig(fig_path + "_plots.png")

    plt.close()

for file in os.listdir(basedir+"/klee_data"):
    create_plots(file)
