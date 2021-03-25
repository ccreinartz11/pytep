import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def _convert_df_to_plot_format(df):
    x = []
    y = []
    for time_between_pauses in sorted(df.keys()):
        x.append(time_between_pauses)
        y.append(df[time_between_pauses])
    y_min = min(y)
    y = [y_i / y_min for y_i in y]
    df = pd.DataFrame(data=zip(x, y), columns=["x", "y"])
    return df


def main():
    df = pd.read_pickle('trials/performance_100hour_simulations.pkl')


    mean = df.mean()
    std  = df.std()
    plt.plot(mean.index, mean.values, 'b')
    plt.plot(mean.index, mean.values - 2*std.values, '--r')
    plt.plot(mean.index, mean.values + 2*std.values, '--r')
    plt.xscale('log', basex=2)
    plt.ylabel('Time (seconds)')
    plt.xlabel('Simulation time between pauses (hours)')
    plt.show()

if __name__ == '__main__':
    main()