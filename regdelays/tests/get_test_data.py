# imports
from pathlib import Path
import os
from random import sample, seed

from pandas import DataFrame

os.chdir("..")
print(os.getcwd())
from utils import load_json, save_json #, save_csv

# load data
p = Path(__file__)
test_dir = p.parent.joinpath("files")
raw_dir = p.parents[2].joinpath("data", "raw")


def get_test_data():
    # load data from documents endpoint
    file = next(f for f in os.listdir(raw_dir) if "documents" in f)
    data = load_json(file, raw_dir, as_dataframe=False)  # as json
    print(f"Total observations: {len(data)}")

    # take random sample of 10k obs
    seed(42)
    sampled_data = sample(data, 10000)
    print(f"Sampled observations: {len(sampled_data)}")

    # save json
    save_json(sampled_data, "test_data.json", test_dir)

    # save dataframe as df
    df = DataFrame(sampled_data)
    with open(test_dir / "test_data.csv", "w", encoding="utf-8") as f:
        df.to_csv(f, index=False, lineterminator=r"\n")
    #save_csv(df, "test_data.csv", test_dir)


if __name__ == "__main__":
    get_test_data()

