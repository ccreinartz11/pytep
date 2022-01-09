import pickle as pkl
import pandas as pd
import sys

pkl_name = sys.argv[1]
# csv_name = sys.argv[2]

csv_name = pkl_name.replace("pkl", "csv")
csv_name = csv_name.replace("data", "output")

with open(pkl_name, "rb") as f:
    obj = pkl.load(f)

df = pd.DataFrame(obj)
df.to_csv(csv_name)
