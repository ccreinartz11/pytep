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
    dict50 = pd.read_pickle("performance_50hours")
    df50 = _convert_df_to_plot_format(dict50)
    dict100 = pd.read_pickle("performance_100hours")
    df100 = _convert_df_to_plot_format(dict100)
    f, ax = plt.subplots(figsize=(5, 5))
    ax.set(xscale="linear", yscale="linear")
    sns.lineplot(data=df50[df50["x"] <= 5], x="x", y="y", ax=ax)
    sns.lineplot(data=df100[df100["x"] <= 5], x="x", y="y", ax=ax)
    plt.show()


if __name__ == '__main__':
    main()