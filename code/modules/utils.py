# import dependencies
import json
from pathlib import Path

from pandas import DataFrame


# ----------------------
# Functions for loading and saving data


def load_csv():
    pass


def load_json(file_name: str, 
              dir_path: Path = Path.cwd(),
              as_dataframe = True
              ):
    """Load csv file using `open()` context manager.

    Args:
        file_name (str): _description_
        dir_path (Path, optional): _description_. Defaults to Path.cwd().
        as_df (bool, optional): _description_. Defaults to True.
    """
    file_path = dir_path / file_name
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if as_dataframe:
        df = DataFrame(data["results"])
        return df
    else:
        return data


def save_csv(df: DataFrame, 
             file_name: str, 
             dir_path: Path = Path.cwd()
             ):
    """Export csv file using `open()` context manager.

    Args:
        df (DataFrame): _description_
        file_name (str): _description_
        dir_path (Path, optional): _description_. Defaults to Path.cwd().
    """
    file_path = dir_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False, line_terminator="\n")


def save_json(obj, 
              file_name: str, 
              dir_path: Path = Path.cwd()
              ):
    """Export json file using `open()` context manager.

    Args:
        obj (dict-like): _description_
        file_name (str): _description_
        dir_path (Path, optional): _description_. Defaults to Path.cwd().
    """
    file_path = dir_path / file_name
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4)

