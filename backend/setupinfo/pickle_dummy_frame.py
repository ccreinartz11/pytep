import pandas as pd
import numpy as np

time = np.arange(1, 101)
constant = np.ones(100)
increasing = np.linspace(-1, 1, 100)
decreasing = np.linspace(1, -1, 100)

dummy_frame = pd.DataFrame(
    {
        "time": time,
        "constant": constant,
        "increasing": increasing,
        "decreasing": decreasing,
    }
)
dummy_frame.to_pickle("./../simout/dummy_frame.pkl")
