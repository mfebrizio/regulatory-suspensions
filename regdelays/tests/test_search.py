# %% Initialize
from pathlib import Path
import os

os.chdir("..")
from utils import load_csv

# load data
p = Path(__file__)
test_dir = p.parents[2].joinpath("data", "processed")
file = next(f for f in os.listdir(test_dir) if "documents" in f)
df = load_csv(file, test_dir)

# %%

import pandas as pd

df.groupby("")


# %% 

from search_columns import search_columns

pat = r"""(?:(?<=\bdelay).+\b(?:compliance|effective)\sdate\b) 
                    | (?:\b(?:compliance|effective)\sdate\b.+(?=\bdelay))
                    """
cols = ["title", "action", "dates"]
df2 = search_columns(df, patterns=[pat], columns=cols)

