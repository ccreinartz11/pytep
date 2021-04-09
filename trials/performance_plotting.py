import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib import rc
import pandas as pd
import numpy as np
from pathlib import Path

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
plt.rcParams.update({'font.size': 16})

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
    df50 = pd.read_pickle(Path(__file__).parent / 'performance_50hour_simulations.pkl')
    df50 = df50.head(1)
    df100 = pd.read_pickle(Path(__file__).parent / 'performance_100hour_simulations.pkl')
    df100 = df100.head(1)

    mean50 = df50.mean()
    min_mean_50 = mean50.min()
    mean100 = df100.mean()
    min_mean100 = mean100.min()
    
    fig = plt.figure(figsize=(6, 3.2))
    ax = fig.gca()
    plt.plot()
    plt.plot(mean50.index, mean50.values/min_mean_50, 'r', label='50 hours')
    plt.plot(mean100.index, mean100.values/min_mean100, 'b', label='100 hours')
    plt.xscale('log', basex=10)
    fmt=ScalarFormatter(useOffset=False)
    fmt.set_scientific(False)
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_tick_params(labelsize=10)
    ax.xaxis.set_tick_params(labelsize=10)
    ax.yaxis.set_major_locator(plt.MaxNLocator(8))
    plt.ylabel('Performance decrease')
    plt.xlabel('Simulation time between pauses (hours)')
    plt.grid()
    plt.legend(prop={'size': 10})
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'performance_plot.pdf', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()