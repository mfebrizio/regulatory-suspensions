# %% Initialize
from pathlib import Path
import os

os.chdir("..")
from utils import load_json, load_csv

# load data
p = Path(__file__)
test_dir = p.parents[2].joinpath("data", "raw")
file = next(f for f in os.listdir(test_dir) if "documents" in f)
df = load_json(file, test_dir)
#test_dir = p.parent.joinpath("files")
#df = load_csv("test_data.csv", test_dir)
file = next(f for f in os.listdir(test_dir) if "agencies" in f)
metadata = load_json(file, test_dir, as_dataframe=False, has_metadata=False)


# %% temp

from preprocessing import clean_agencies_column
df2 = clean_agencies_column(df, metadata)


# %%
