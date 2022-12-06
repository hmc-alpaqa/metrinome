# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import plotly.express as px


path = Path('../../src/tests/cFiles/example_apc/kleedata')
cleaned_path = path / '../cleaned_kleedata'
if not os.path.exists(cleaned_path):
    os.mkdir(cleaned_path)


def comparedepth(series, depth):
    rowdepth = int(series[0].split("=")[1])
    return rowdepth <= depth


for file in os.listdir(path):
    if "." not in file and os.path.isfile(path / file):
        print(file)
        plt.clf()
        fram = pd.read_csv(path / file)
        x = np.array([int(i.split("=")[1]) for i in fram.iloc[:, 0]])
        y = np.array([int(j) for j in fram.loc[:, "CompletedPaths"]])

        # plt.figure(figsize=(10, 5))
        # plt.xticks(x)
        # plt.title('Completed Paths vs Depth')
        # plt.plot(x, y, marker='.')
        # plt.grid(visible=True)
        # plt.show()

        # plotly
        df = pd.DataFrame({'Depth': x, 'Completed Paths': y})
        fig = px.line(df, x='Depth', y='Completed Paths',
                      title='Completed Paths vs Depth', markers=True)
        fig.show()

        n = int(input("ENTER STOPPING POINT"))
        new_fram = fram.loc[lambda x: x.apply(
            lambda y:comparedepth(y, n), axis=1), :]
        new_fram.to_csv(cleaned_path / file)

        # # cut off values >= final value (completed paths)
        # new_fram = fram.loc[lambda x: x['CompletedPaths']
        #                     < x['CompletedPaths'].iloc[-1], :]
        # # plot time graph after cutting off
        # x = np.array([int(i.split("=")[1]) for i in new_fram.iloc[:, 0]])
        # y = np.array([int(j) for j in new_fram.loc[:, "PythonTime"]])
        # # plt.xticks(np.arange(x[0], x[-1]+1, 1))
        # plt.figure(figsize=(10, 5))
        # plt.xticks(x)
        # plt.title('Python Time vs Truncated Depth')
        # plt.plot(x, y, marker='.')
        # plt.grid(visible=True)
        # plt.show()
        # new_fram.to_csv(cleaned_path / file)
