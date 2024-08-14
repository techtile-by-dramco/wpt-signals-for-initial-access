import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import os

dir_name = "c:/Users/jarne/Documents/GitHub/wpt-signals-for-initial-access/plot/rp-results"
names = ["realistic multi", "realistic single", "ideal single", "ideal multi"]

file_names = [
    "1723549644_multi_tone_m1_realistic",
    "1723550127_one_tone_phase_duration_5_m1_realistic",
    "1723551096_one_tone_phase_duration_5_m1_ideal",
    "1723551712_multi_tone_m1_ideal",
]

def tikzplotlib_fix_ncols(obj):
    """
    workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, which breaks tikzplotlib
    """
    if hasattr(obj, "_ncols"):
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)

fig, ax1 = plt.subplots()

for name, f in zip(names, file_names):
    df = pd.read_csv(
        os.path.join(dir_name, f+".csv"),
        sep=",",
        header=0,
        index_col=None,
        na_values=[0.0],
        parse_dates=True,
    )
    print(df.head())

    # Sort the data
    df_sorted = df[df["gain"] == 84.0]["respons_time"].sort_values()

    df_sorted = df_sorted.to_numpy()

    # Calculate the CDF values
    cdf = np.arange(1, len(df_sorted) + 1) / len(df_sorted)

    # ls = "-" if "single" in name else "--"

    # Plot the CDF
    # ax1.plot(df_sorted, cdf, linestyle = ls, label=name) #marker='.', 
    ax1.plot(df_sorted, cdf, label=name) #marker='.', 

ax1.set_xlabel('Time seconds')
ax1.set_ylabel('CDF')
plt.title('Cumulative Distribution Function (CDF)')
ax1.grid(True)
ax1.legend()
# plt.show()

import tikzplotlib
tikzplotlib_fix_ncols(fig)
tikzplotlib.save(f"{dir_name}/cdf.tex")