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

    # Read csv data into 2 numpy arrays (x and y axes)
    csv_dataframe = pd.read_csv(basedir+"/klee_data/"+csv_file)
    data_x = np.array([int(i.split("=")[1]) for i in csv_dataframe.iloc[:,0]])
    data_y = np.array([int(j) for j in csv_dataframe.loc[:, "CompletedPaths"]])

    # Get the name of the file without the ".csv" extension
    name = csv_file.split(".")[0]

    # Make a directory (if none exists) for this specific dataset within the plots folder
    plots_dir = basedir+f"/plots/{name}_plots"
    Path(plots_dir).mkdir(parents=True, exist_ok=True)

    # Create the 3 plots
    plots_dir += f"/{name}"
    linear_plot(data_x, data_y, plots_dir)
    loglog_plot(data_x, data_y, plots_dir)
    loglinear_plot(data_x, data_y, plots_dir)

def linear_plot(data_x: np.ndarray, data_y: np.ndarray, fig_path: str) -> None:
    plt.plot(data_x, data_y, label="linear")
    plt.savefig(fig_path + "_linear.png")

def loglog_plot(data_x: np.ndarray, data_y: np.ndarray, fig_path: str) -> None:
    plt.loglog(data_x, data_y, label="loglog")
    plt.savefig(fig_path + "_loglog.png")
    plt.close()

def loglinear_plot(data_x: np.ndarray, data_y: np.ndarray, fig_path: str) -> None:
    ax = plt.subplot(211)
    ax.set_yscale('log')
    ax.plot(data_x, data_y, label="loglinear")
    plt.savefig(fig_path + "_loglinear.png")
    plt.close()

for file in os.listdir(basedir+"/klee_data"):
    create_plots(file)
