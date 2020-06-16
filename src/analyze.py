import time, subprocess, re
from subprocess import PIPE
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams["figure.figsize"] = (10,10)


functions = ['04_prime', '05_parity', '06_palindrome', '02_fib', '03_sign', '01_greatestof3', '16_binary_search', '12_check_sorted_array',
'11_array_max', '10_find_val_in_array', '13_check_arrays_equal', '15_check_heap_order',
'14_lexicographic_array_compare', '17_edit_dist',
"20_bubblesort", "21_insertionsort", "22_selectionsort", "23_mergesort",
"30_euclid_GCD", "31_sieve_of_eratosthenes", "32_newtons_method"]
fields = ["ICov(%)",'BCov(%)',"CompletedPaths","GeneratedTests", "RealTime", "UserTime", "SysTime", "PythonTime"]

def generate_graphs(func, field):
    subprocess.run("mkdir /app/code/tests/cFiles/simpleAlgs/graphs/", shell=True)
    fig1, ax1 = plt.subplots()
    data = pd.read_csv(f"/app/code/tests/cFiles/simpleAlgs/frames/{func}.csv")
    times = [i.split()[2] for i in data.iloc[:,0]]
    ax1.plot(times, data[field], label = func)
    ax1.set(xlabel='depth', ylabel=field, title=func)
    ax1.legend()
    ax1.grid()
    fig1.savefig(f"/app/code/tests/cFiles/simpleAlgs/graphs/{field}_{func}.png".replace("%","percent"))
    plt.close(fig1)

if __name__ == "__main__":
    for f in functions:
        for field in fields:
            generate_graphs(f, field)
